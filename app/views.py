from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.core.cache import cache
from .models import Article, Tag, Comment, BoardMessage
import markdown as md
import bleach
import hashlib
import random
from pathlib import Path
from django.conf import settings
from PIL import Image, ImageDraw

AUTHOR_BIO = "这里是《盘古大仙洞府》——记录技术、思考与灵感的地方。"


def index(request: HttpRequest):
    """首页：显示作者简介与科技风入口"""
    return render(request, "index.html", {"bio": AUTHOR_BIO})


def article_list(request: HttpRequest):
    """文章列表：支持标签筛选与分页"""
    tag_name = request.GET.get("tag")
    qs = Article.objects.filter(is_hidden=False).order_by("-published_at")
    active_tag = None
    if tag_name:
        active_tag = get_object_or_404(Tag, name=tag_name)
        qs = qs.filter(tags=active_tag)
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    tags = Tag.objects.all()
    return render(request, "list.html", {"page_obj": page_obj, "tags": tags, "active_tag": active_tag})


def article_detail(request: HttpRequest, pk: int):
    """文章详情：底部评论列表"""
    article = get_object_or_404(Article, pk=pk, is_hidden=False)
    comments = article.comments.filter(is_hidden=False)
    # Markdown -> 安全 HTML
    allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({"p", "pre", "code", "img", "h1", "h2", "h3", "h4", "h5", "h6", "table", "thead", "tbody", "tr", "th", "td", "blockquote"})
    html = md.markdown(article.content_md, extensions=["extra", "fenced_code", "tables", "codehilite"])
    html = bleach.clean(html, tags=allowed_tags, attributes={"*": ["class", "id"], "img": ["src", "alt"]}, strip=True)
    return render(request, "detail.html", {"article": article, "comments": comments, "article_html": html})


def about(request: HttpRequest):
    return render(request, "about.html")

def admin_responsive_test(request: HttpRequest):
    """响应式管理后台测试页面"""
    return render(request, "admin/responsive_test.html")


def board(request: HttpRequest):
    messages = BoardMessage.objects.filter(is_hidden=False).order_by('-created_at')
    return render(request, "board.html", {"messages": messages})


def _client_key(request: HttpRequest) -> str:
    ua = request.META.get("HTTP_USER_AGENT", "")
    ip = request.META.get("REMOTE_ADDR", "")
    key_raw = f"{ip}|{ua}"
    return hashlib.md5(key_raw.encode()).hexdigest()


def _get_city_from_ip(request: HttpRequest) -> str:
    """从 IP 地址获取城市信息"""
    ip = request.META.get("REMOTE_ADDR", "")

    # 本地/内网 IP 默认值
    if not ip or ip in ["127.0.0.1", "localhost"] or ip.startswith("192.168.") or ip.startswith("10."):
        return "未知星域"

    try:
        # 使用免费的 IP 地理位置 API
        import urllib.request
        import json

        # 使用 ip-api.com (免费，无需 API key，每分钟45次请求)
        url = f"http://ip-api.com/json/{ip}?lang=zh-CN&fields=city,country"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            city = data.get('city', '')
            country = data.get('country', '')

            if city and country:
                return f"{country}·{city}"
            elif city:
                return city
            elif country:
                return country
            else:
                return "未知星域"
    except Exception as e:
        # 发生任何错误都返回默认值
        return "未知星域"


def _ensure_avatars_pool():
    """如不存在则生成 30 个简易彩色方块 icon 作为随机头像"""
    pool_dir = Path(settings.MEDIA_ROOT) / "avatars"
    pool_dir.mkdir(parents=True, exist_ok=True)
    existing = list(pool_dir.glob("icon_*.png"))
    if len(existing) >= 30:
        return
    # 移除固定 seed，让每次生成真正随机的颜色
    for i in range(30):
        # 生成鲜艳的随机颜色（避免太暗）
        color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        img = Image.new("RGB", (128, 128), color)
        draw = ImageDraw.Draw(img)
        # 简单几何装饰 - 白色方框
        draw.rectangle([16, 16, 112, 112], outline=(255, 255, 255), width=4)
        img.save(pool_dir / f"icon_{i+1:02d}.png")


@require_POST
def submit_comment(request: HttpRequest):
    """匿名评论提交：复用昵称与头像，简易城市占位"""
    article_id = int(request.POST.get("article_id", 0))
    content = (request.POST.get("content") or "").strip()
    article = get_object_or_404(Article, pk=article_id, is_hidden=False)
    if not article.allow_comment:
        return JsonResponse({"ok": False, "msg": "评论区已关闭"}, status=400)
    if not content or len(content) < 2:
        return JsonResponse({"ok": False, "msg": "评论内容过短"}, status=400)

    # 简易限流：同一客户端 30 秒一次
    ckey = _client_key(request)
    if cache.get(f"comment:cooldown:{ckey}"):
        return JsonResponse({"ok": False, "msg": "操作过于频繁"}, status=429)
    cache.set(f"comment:cooldown:{ckey}", 1, 30)

    # 随机昵称与头像（同客户端复用）
    profile = cache.get(f"comment:profile:{ckey}")
    if not profile:
        _ensure_avatars_pool()
        avatar_files = sorted((Path(settings.MEDIA_ROOT) / "avatars").glob("icon_*.png"))
        avatar_rel = f"avatars/{Path(random.choice(avatar_files)).name}" if avatar_files else ""
        nickname = f"道友{random.randint(100000, 999999)}"
        city = _get_city_from_ip(request)  # 使用真实 IP 城市
        profile = {"nickname": nickname, "avatar": avatar_rel, "city": city}
        cache.set(f"comment:profile:{ckey}", profile, 60 * 60 * 24 * 30)

    Comment.objects.create(
        article=article,
        nickname=profile["nickname"],
        city=profile["city"],
        avatar=profile["avatar"],
        content=content,
    )
    return JsonResponse({"ok": True})
