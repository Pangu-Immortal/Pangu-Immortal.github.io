"""
Django 管理命令: 生成静态站点到 docs/ 目录
用于 GitHub Pages 部署

使用方法:
    python manage.py generate_static_site

功能:
    1. 渲染所有页面为静态 HTML
    2. 收集静态资源 (CSS/JS/图片)
    3. 复制 media 文件 (封面/头像)
    4. 生成站点地图
    5. 输出到 docs/ 目录供 GitHub Pages 使用
"""

from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from pathlib import Path
import shutil
import markdown as md
import bleach

from app.models import Article, Tag, Comment, BoardMessage


class Command(BaseCommand):
    help = '生成静态站点到 docs/ 目录用于 GitHub Pages'

    def __init__(self):
        super().__init__()
        self.output_dir = Path(settings.BASE_DIR) / 'docs'
        self.author_bio = "这里是《盘古大仙洞府》——记录技术、思考与灵感的地方。"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始生成静态站点...'))

        # 清空并重建输出目录
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)

        # 1. 生成首页
        self.generate_index()

        # 2. 生成文章列表页(含分页)
        self.generate_article_list()

        # 3. 生成所有文章详情页
        self.generate_article_details()

        # 4. 生成关于页面
        self.generate_about()

        # 5. 生成留言板页面
        self.generate_board()

        # 6. 复制静态资源
        self.copy_static_files()

        # 7. 复制 media 文件
        self.copy_media_files()

        # 8. 生成 sitemap
        self.generate_sitemap()

        # 9. 生成 .nojekyll (GitHub Pages 需要)
        (self.output_dir / '.nojekyll').touch()

        self.stdout.write(self.style.SUCCESS(f'✓ 静态站点已生成到: {self.output_dir}'))
        self.stdout.write(self.style.SUCCESS(f'  可以提交到 GitHub 仓库并在仓库设置中启用 GitHub Pages (从 docs/ 目录)'))

    def generate_index(self):
        """生成首页"""
        html = render_to_string('index.html', {
            'bio': self.author_bio,
            'is_static': True,
            'current_page': 'index'
        })
        self._write_html('index.html', html)
        self.stdout.write('  ✓ 生成首页')

    def generate_article_list(self):
        """生成文章列表页(分页)"""
        from django.core.paginator import Paginator

        articles = Article.objects.filter(is_hidden=False).order_by('-published_at')
        tags = Tag.objects.all()

        # 生成主列表页(第1页)
        paginator = Paginator(articles, 10)
        for page_num in paginator.page_range:
            page_obj = paginator.get_page(page_num)
            html = render_to_string('list.html', {
                'page_obj': page_obj,
                'tags': tags,
                'active_tag': None,
                'is_static': True,
                'current_page': 'list'
            })

            if page_num == 1:
                self._write_html('list.html', html)
            else:
                self._write_html(f'list_page_{page_num}.html', html)

        # 生成标签筛选页
        for tag in tags:
            tag_articles = articles.filter(tags=tag)
            tag_paginator = Paginator(tag_articles, 10)

            for page_num in tag_paginator.page_range:
                page_obj = tag_paginator.get_page(page_num)
                html = render_to_string('list.html', {
                    'page_obj': page_obj,
                    'tags': tags,
                    'active_tag': tag,
                    'is_static': True,
                    'current_page': 'list'
                })

                filename = f'list_tag_{tag.name}_page_{page_num}.html' if page_num > 1 else f'list_tag_{tag.name}.html'
                self._write_html(filename, html)

        self.stdout.write(f'  ✓ 生成文章列表页 ({len(articles)} 篇文章)')

    def generate_article_details(self):
        """生成所有文章详情页"""
        articles = Article.objects.filter(is_hidden=False)

        for article in articles:
            comments = article.comments.filter(is_hidden=False)

            # Markdown -> HTML
            allowed_tags = bleach.sanitizer.ALLOWED_TAGS.union({
                'p', 'pre', 'code', 'img', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote'
            })
            html_content = md.markdown(
                article.content_md,
                extensions=['extra', 'fenced_code', 'tables', 'codehilite']
            )
            html_content = bleach.clean(
                html_content,
                tags=allowed_tags,
                attributes={'*': ['class', 'id'], 'img': ['src', 'alt']},
                strip=True
            )

            html = render_to_string('detail.html', {
                'article': article,
                'comments': comments,
                'article_html': html_content,
                'is_static': True,
                'current_page': 'list'
            })

            self._write_html(f'article_{article.pk}.html', html)

        self.stdout.write(f'  ✓ 生成文章详情页 ({articles.count()} 篇)')

    def generate_about(self):
        """生成关于页面"""
        html = render_to_string('about.html', {
            'is_static': True,
            'current_page': 'about'
        })
        self._write_html('about.html', html)
        self.stdout.write('  ✓ 生成关于页面')

    def generate_board(self):
        """生成留言板页面"""
        messages = BoardMessage.objects.filter(is_hidden=False).order_by('-created_at')
        html = render_to_string('board.html', {
            'is_static': True,
            'current_page': 'board',
            'messages': messages
        })
        self._write_html('board.html', html)
        self.stdout.write('  ✓ 生成留言板页面')

    def copy_static_files(self):
        """复制静态资源"""
        static_src = Path(settings.BASE_DIR) / 'static'
        static_dest = self.output_dir / 'static'

        if static_src.exists():
            shutil.copytree(static_src, static_dest, dirs_exist_ok=True)
            self.stdout.write('  ✓ 复制静态资源 (CSS/JS)')

        # 复制 staticfiles (collectstatic 的输出)
        staticfiles_src = Path(settings.BASE_DIR) / 'staticfiles'
        if staticfiles_src.exists():
            shutil.copytree(staticfiles_src, static_dest, dirs_exist_ok=True)
            self.stdout.write('  ✓ 复制 staticfiles')

    def copy_media_files(self):
        """复制 media 文件 (封面、头像等)"""
        media_src = Path(settings.MEDIA_ROOT)
        media_dest = self.output_dir / 'media'

        if media_src.exists():
            shutil.copytree(media_src, media_dest, dirs_exist_ok=True)
            self.stdout.write('  ✓ 复制 media 文件 (封面/头像)')

    def generate_sitemap(self):
        """生成 sitemap.xml"""
        articles = Article.objects.filter(is_hidden=False)

        sitemap_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
            '  <url>',
            '    <loc>https://pangu-immortal.github.io/</loc>',
            f'    <lastmod>{timezone.now().strftime("%Y-%m-%d")}</lastmod>',
            '    <changefreq>weekly</changefreq>',
            '    <priority>1.0</priority>',
            '  </url>',
        ]

        for article in articles:
            sitemap_lines.extend([
                '  <url>',
                f'    <loc>https://pangu-immortal.github.io/article_{article.pk}.html</loc>',
                f'    <lastmod>{article.published_at.strftime("%Y-%m-%d")}</lastmod>',
                '    <changefreq>monthly</changefreq>',
                '    <priority>0.8</priority>',
                '  </url>',
            ])

        sitemap_lines.append('</urlset>')

        sitemap_path = self.output_dir / 'sitemap.xml'
        sitemap_path.write_text('\n'.join(sitemap_lines), encoding='utf-8')
        self.stdout.write('  ✓ 生成 sitemap.xml')

    def _write_html(self, filename: str, content: str):
        """写入 HTML 文件"""
        file_path = self.output_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
