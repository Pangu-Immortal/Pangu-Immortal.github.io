"""
API视图模块
为Vue前端提供JSON格式的数据接口
"""

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core import serializers
from django.core.files.base import ContentFile
from django.conf import settings
from functools import wraps
import json
import base64
import re
from .models import Article, Tag, Comment, BoardMessage


def cors_headers(view_func):
    """添加CORS响应头的装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response, JsonResponse):
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    return wrapper


@cors_headers
@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])  # 🔒 安全：只允许 GET
def api_article_list(request):
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)
    try:
        if request.method == "GET":
            tag_name = request.GET.get("tag")
            page = int(request.GET.get("page", 1))
            qs = Article.objects.filter(is_hidden=False).order_by("-published_at")
            if tag_name:
                tag = get_object_or_404(Tag, name=tag_name)
                qs = qs.filter(tags=tag)
            paginator = Paginator(qs, 10)
            page_obj = paginator.get_page(page)
            articles = []
            for article in page_obj.object_list:
                cover_url = ""
                if article.cover:
                    cover_url = request.build_absolute_uri(article.cover.url) if hasattr(request, 'build_absolute_uri') else article.cover.url
                articles.append({
                    "id": article.id,
                    "title": article.title,
                    "cover": cover_url,
                    "summary": article.content_md[:200] + "..." if len(article.content_md) > 200 else article.content_md,
                    "published_at": article.published_at.strftime("%Y-%m-%d %H:%M"),
                    "tags": [{"id": tag.id, "name": tag.name} for tag in article.tags.all()]
                })
            all_tags = Tag.objects.all()
            tags_data = [{"id": tag.id, "name": tag.name} for tag in all_tags]
            return JsonResponse({
                "ok": True,
                "data": {
                    "articles": articles,
                    "tags": tags_data,
                    "pagination": {
                        "current_page": page_obj.number,
                        "total_pages": page_obj.paginator.num_pages,
                        "has_next": page_obj.has_next(),
                        "has_previous": page_obj.has_previous(),
                        "total_count": paginator.count
                    }
                }
            })
        else:
            try:
                body = json.loads(request.body.decode() or "{}")
            except Exception:
                body = {}
            title = (body.get("title") or "").strip()
            content_md = body.get("content_md") or body.get("content") or ""
            tags = body.get("tags") or []
            cover_data = body.get("cover") or ""
            is_hidden = bool(body.get("is_hidden", False))
            allow_comment = bool(body.get("allow_comment", body.get("allow_comments", True)))
            if not title or not content_md:
                return JsonResponse({"ok": False, "msg": "标题或内容不能为空"}, status=400)
            article = Article.objects.create(
                title=title,
                content_md=content_md,
                is_hidden=is_hidden,
                allow_comment=allow_comment,
            )
            if isinstance(tags, list):
                for name in tags:
                    if not isinstance(name, str):
                        continue
                    tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
                    article.tags.add(tag_obj)
            if isinstance(cover_data, str) and cover_data.startswith("data:image/"):
                match = re.match(r"data:image/(\w+);base64,(.+)", cover_data)
                if match:
                    ext = match.group(1)
                    b64 = match.group(2)
                    try:
                        content = base64.b64decode(b64)
                        filename = f"cover_{article.id}.{ext}"
                        article.cover.save(filename, ContentFile(content), save=True)
                    except Exception:
                        pass
            return JsonResponse({
                "ok": True,
                "data": {
                    "id": article.id,
                    "title": article.title,
                    "content_md": article.content_md,
                    "cover": article.cover.url if article.cover else "",
                    "published_at": article.published_at.strftime("%Y-%m-%d %H:%M"),
                    "tags": [{"id": t.id, "name": t.name} for t in article.tags.all()],
                    "allow_comment": article.allow_comment
                }
            })
    except Exception as e:
        return JsonResponse({"ok": False, "msg": f"文章接口错误: {str(e)}"}, status=500)


@cors_headers
@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])  # 🔒 安全：只允许 GET
def api_article_detail(request, pk):
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)
    try:
        article = get_object_or_404(Article, pk=pk)
        if request.method == "GET":
            if article.is_hidden:
                return JsonResponse({"ok": False, "msg": "文章不可见"}, status=404)
            comments = article.comments.filter(is_hidden=False)
            comments_data = []
            for comment in comments:
                avatar_url = ""
                if comment.avatar:
                    avatar_url = request.build_absolute_uri(comment.avatar.url) if hasattr(request, 'build_absolute_uri') else comment.avatar.url
                comments_data.append({
                    "id": comment.id,
                    "nickname": comment.nickname,
                    "city": comment.city,
                    "content": comment.content,
                    "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
                    "avatar": avatar_url
                })
            cover_url = ""
            if article.cover:
                cover_url = request.build_absolute_uri(article.cover.url) if hasattr(request, 'build_absolute_uri') else article.cover.url
            article_data = {
                "id": article.id,
                "title": article.title,
                "content_md": article.content_md,
                "cover": cover_url,
                "published_at": article.published_at.strftime("%Y-%m-%d %H:%M"),
                "tags": [{"id": tag.id, "name": tag.name} for tag in article.tags.all()],
                "allow_comment": article.allow_comment,
                "comments": comments_data
            }
            return JsonResponse({"ok": True, "data": article_data})
        elif request.method == "PUT":
            try:
                body = json.loads(request.body.decode() or "{}")
            except Exception:
                body = {}
            title = body.get("title")
            content_md = body.get("content_md") or body.get("content")
            tags = body.get("tags")
            cover_data = body.get("cover")
            if title is not None:
                article.title = str(title).strip()
            if content_md is not None:
                article.content_md = content_md
            if isinstance(tags, list):
                article.tags.clear()
                for name in tags:
                    if not isinstance(name, str):
                        continue
                    tag_obj, _ = Tag.objects.get_or_create(name=name.strip())
                    article.tags.add(tag_obj)
            if isinstance(cover_data, str):
                if cover_data.startswith("data:image/"):
                    match = re.match(r"data:image/(\w+);base64,(.+)", cover_data)
                    if match:
                        ext = match.group(1)
                        b64 = match.group(2)
                        try:
                            content = base64.b64decode(b64)
                            filename = f"cover_{article.id}.{ext}"
                            article.cover.save(filename, ContentFile(content), save=False)
                        except Exception:
                            pass
                elif cover_data == "":
                    article.cover = None
            is_hidden = body.get("is_hidden")
            if is_hidden is not None:
                article.is_hidden = bool(is_hidden)
            allow_comment = body.get("allow_comment")
            if allow_comment is None and "allow_comments" in body:
                allow_comment = body.get("allow_comments")
            if allow_comment is not None:
                article.allow_comment = bool(allow_comment)
            article.save()
            return JsonResponse({
                "ok": True,
                "data": {
                    "id": article.id,
                    "title": article.title,
                    "content_md": article.content_md,
                    "cover": article.cover.url if article.cover else "",
                    "published_at": article.published_at.strftime("%Y-%m-%d %H:%M"),
                    "tags": [{"id": t.id, "name": t.name} for t in article.tags.all()],
                    "allow_comment": article.allow_comment
                }
            })
        elif request.method == "DELETE":
            article.delete()
            return JsonResponse({"ok": True})
        return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
    except Exception as e:
        return JsonResponse({"ok": False, "msg": f"文章详情接口错误: {str(e)}"}, status=500)


@cors_headers
def api_about_info(request):
    """
    API: 获取关于作者信息
    """
    try:
        from .views import AUTHOR_BIO
        return JsonResponse({
            "ok": True,
            "data": {
                "bio": AUTHOR_BIO
            }
        })
    except Exception as e:
        return JsonResponse({
            "ok": False,
            "msg": f"获取关于信息失败: {str(e)}"
        }, status=500)


@cors_headers
def api_board_messages(request):
    """
    API: 获取留言板消息
    """
    try:
        qs = BoardMessage.objects.filter(is_hidden=False).order_by("-created_at")
        messages_data = []
        for message in qs:
            avatar_url = ""
            if message.avatar:
                avatar_url = request.build_absolute_uri(message.avatar.url) if hasattr(request, 'build_absolute_uri') else message.avatar.url
            messages_data.append({
                "id": message.id,
                "nickname": message.nickname,
                "city": message.city,
                "content": message.content,
                "created_at": message.created_at.strftime("%Y-%m-%d %H:%M"),
                "avatar": avatar_url
            })
        return JsonResponse({
            "ok": True,
            "data": {
                "messages": messages_data
            }
        })
    except Exception as e:
        return JsonResponse({
            "ok": False,
            "msg": f"获取留言板消息失败: {str(e)}"
        }, status=500)


@cors_headers
@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_submit_comment(request):
    """
    API: 提交评论（支持JSON和form-data）
    """
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)
    try:
        # 支持JSON和form-data两种格式
        if request.content_type and 'application/json' in request.content_type:
            try:
                body = json.loads(request.body.decode() or "{}")
                article_id = body.get('article_id')
                content = body.get('content', '').strip()
            except Exception:
                return JsonResponse({"ok": False, "msg": "JSON解析失败"}, status=400)
        else:
            article_id = request.POST.get('article_id')
            content = request.POST.get('content', '').strip()
        
        if not article_id or not content:
            return JsonResponse({
                "ok": False,
                "msg": "缺少必要参数"
            }, status=400)
        
        # 验证文章是否存在
        try:
            article = Article.objects.get(pk=article_id, is_hidden=False)
        except Article.DoesNotExist:
            return JsonResponse({
                "ok": False,
                "msg": "文章不存在"
            }, status=404)
        
        # 检查是否允许评论
        if not article.allow_comment:
            return JsonResponse({
                "ok": False,
                "msg": "该文章不允许评论"
            }, status=403)
        
        # 使用views中的逻辑：复用昵称和头像
        from .views import _client_key, _ensure_avatars_pool, _get_city_from_ip
        from django.core.cache import cache
        from pathlib import Path
        import random

        ckey = _client_key(request)
        profile = cache.get(f"comment:profile:{ckey}")
        if not profile:
            _ensure_avatars_pool()
            avatar_files = sorted((Path(settings.MEDIA_ROOT) / "avatars").glob("icon_*.png"))
            avatar_rel = f"avatars/{Path(random.choice(avatar_files)).name}" if avatar_files else ""
            nickname = f"道友{random.randint(100000, 999999)}"
            city = _get_city_from_ip(request)  # 使用真实 IP 城市
            profile = {"nickname": nickname, "avatar": avatar_rel, "city": city}
            cache.set(f"comment:profile:{ckey}", profile, 60 * 60 * 24 * 30)
        
        # 创建评论
        comment = Comment.objects.create(
            article=article,
            content=content,
            nickname=profile["nickname"],
            city=profile["city"],
            avatar=profile["avatar"],
            is_hidden=False
        )
        
        avatar_url = ""
        if comment.avatar:
            avatar_url = request.build_absolute_uri(comment.avatar.url) if hasattr(request, 'build_absolute_uri') else comment.avatar.url
        return JsonResponse({
            "ok": True,
            "msg": "评论提交成功",
            "data": {
                "id": comment.id,
                "nickname": comment.nickname,
                "city": comment.city,
                "avatar": avatar_url,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M")
            }
        })
        
    except Exception as e:
        return JsonResponse({
            "ok": False,
            "msg": f"评论提交失败: {str(e)}"
        }, status=500)


@cors_headers
@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def api_submit_message(request):
    """
    API: 提交留言（支持JSON和form-data）
    """
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)
    try:
        # 支持JSON和form-data两种格式
        if request.content_type and 'application/json' in request.content_type:
            try:
                body = json.loads(request.body.decode() or "{}")
                content = body.get('content', '').strip()
            except Exception:
                return JsonResponse({"ok": False, "msg": "JSON解析失败"}, status=400)
        else:
            content = request.POST.get('content', '').strip()
        
        if not content:
            return JsonResponse({
                "ok": False,
                "msg": "留言内容不能为空"
            }, status=400)
        
        # 复用随机昵称与头像逻辑
        from .views import _client_key, _ensure_avatars_pool, _get_city_from_ip
        from django.core.cache import cache
        from pathlib import Path
        import random

        ckey = _client_key(request)
        profile = cache.get(f"comment:profile:{ckey}")
        if not profile:
            _ensure_avatars_pool()
            avatar_files = sorted((Path(settings.MEDIA_ROOT) / "avatars").glob("icon_*.png"))
            avatar_rel = f"avatars/{Path(random.choice(avatar_files)).name}" if avatar_files else ""
            nickname = f"道友{random.randint(100000, 999999)}"
            city = _get_city_from_ip(request)  # 使用真实 IP 城市
            profile = {"nickname": nickname, "avatar": avatar_rel, "city": city}
            cache.set(f"comment:profile:{ckey}", profile, 60 * 60 * 24 * 30)
        
        msg = BoardMessage.objects.create(
            content=content,
            nickname=profile["nickname"],
            city=profile["city"],
            avatar=profile["avatar"],
            is_hidden=False
        )
        
        avatar_url = ""
        if msg.avatar:
            avatar_url = request.build_absolute_uri(msg.avatar.url) if hasattr(request, 'build_absolute_uri') else msg.avatar.url
        return JsonResponse({
            "ok": True,
            "msg": "留言提交成功",
            "data": {
                "id": msg.id,
                "nickname": msg.nickname,
                "city": msg.city,
                "avatar": avatar_url,
                "content": msg.content,
                "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M")
            }
        })
        
    except Exception as e:
        return JsonResponse({
            "ok": False,
            "msg": f"留言提交失败: {str(e)}"
        }, status=500)