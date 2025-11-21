from django.contrib import admin, messages
from django.utils.html import format_html
from django import forms
from django.urls import path, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from markdownx.widgets import MarkdownxWidget
from .models import Article, Tag
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "article_count")
    search_fields = ("name",)
    ordering = ("name",)
    
    # 使用粉色系模板
    change_list_template = "admin/pink_tag_list.html"
    enable_nav_sidebar = False
    
    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = "文章数量"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "published_at", "is_hidden", "cover_thumb")
    list_filter = ("is_hidden", "published_at", "tags")
    search_fields = ("title", "content_md")
    filter_horizontal = ("tags",)
    date_hierarchy = "published_at"
    actions = ["make_hidden", "make_visible"]
    
    # 使用自定义粉色系模板
    change_list_template = "admin/pink_article_list.html"
    change_form_template = "admin/pink_article_form.html"
    delete_confirmation_template = "admin/pink_delete_confirmation.html"
    enable_nav_sidebar = False

    class ArticleForm(forms.ModelForm):
        class Meta:
            model = Article
            fields = "__all__"
            widgets = {
                "content_md": MarkdownxWidget(),
            }

        class Media:
            css = {
                'all': [
                    'markdownx/css/markdownx.css',
                ]
            }
            js = [
                'markdownx/js/markdownx.js',
            ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # 移除所有字段的必填验证
            for field_name, field in self.fields.items():
                field.required = False
                if field_name == 'title':
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'placeholder': '请输入文章标题'
                    })
                elif field_name == 'content_md':
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'rows': 20,
                        'placeholder': '请输入文章内容（支持Markdown格式）'
                    })
                elif field_name == 'cover':
                    field.widget.attrs.update({
                        'class': 'form-control',
                        'accept': 'image/*'
                    })
                elif field_name == 'published_at':
                    field.widget.attrs.update({
                        'readonly': True,
                        'class': 'form-control'
                    })
                    field.help_text = "发布时间将在保存时自动设置为当前时间"
        
        def clean(self):
            # 跳过所有验证，直接返回清理后的数据
            return self.cleaned_data

    form = ArticleForm

    fieldsets = (
        ("文章内容", {
            "fields": ("title", "content_md", "cover", "tags"),
            "description": "填写文章标题、内容（支持Markdown格式）、上传封面图片并选择标签"
        }),
        ("发布设置", {
            "fields": ("is_hidden", "allow_comment"),
            "description": "控制文章的可见性和评论功能"
        }),
    )
    readonly_fields = ("published_at",)
    
    # 移除不存在的静态资源引用，避免404日志噪音

    def cover_thumb(self, obj):
        if obj.cover:
            return format_html('<img src="{}" height="40"/>', obj.cover.url)
        return "-"

    cover_thumb.short_description = "预览图"

    @admin.action(description="隐藏所选文章")
    def make_hidden(self, request, queryset):
        queryset.update(is_hidden=True)

    @admin.action(description="显示所选文章")
    def make_visible(self, request, queryset):
        queryset.update(is_hidden=False)

    def save_model(self, request, obj, form, change):
        # 直接保存，不做任何验证
        # 从 POST 数据直接设置字段值
        if 'title' in request.POST:
            obj.title = request.POST.get('title', '未命名文章') or '未命名文章'
        if 'content_md' in request.POST:
            obj.content_md = request.POST.get('content_md', '') or ''
        if 'is_hidden' in request.POST:
            obj.is_hidden = request.POST.get('is_hidden') == 'on'
        else:
            obj.is_hidden = False
        
        # 处理封面图片
        if 'cover' in request.FILES:
            obj.cover = request.FILES['cover']
        
        # 设置发布时间
        if not change and not obj.published_at:
            obj.published_at = timezone.now()
        
        # 发布操作：确保显示
        if '_publish' in request.POST:
            obj.is_hidden = False

        # 直接保存对象，跳过所有验证
        try:
            # 使用 update_fields 绕过模型验证
            obj.save(force_insert=not change, force_update=change)
            
            # 手动保存 tags
            if 'tags' in request.POST:
                obj.tags.clear()
                tag_ids = request.POST.getlist('tags')
                from .models import Tag
                for tag_id in tag_ids:
                    try:
                        tag = Tag.objects.get(pk=tag_id)
                        obj.tags.add(tag)
                    except (Tag.DoesNotExist, ValueError):
                        pass
        except Exception as e:
            logger.error("Error saving article: %s", str(e))
            messages.error(request, f'保存失败: {str(e)}')
            return

        # 成功提示
        if '_publish' in request.POST:
            messages.success(request, f'🎉 文章发布成功')
        elif '_continue' in request.POST:
            messages.success(request, f'💾 文章已保存，继续编辑')
        elif change:
            messages.success(request, f'✅ 文章更新成功')
        else:
            messages.success(request, f'💾 文章创建成功')

    def response_add(self, request, obj, post_url_continue=None):
        # 消息已在 save_model 中添加，这里只处理重定向
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_add'))
        elif '_continue' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_change', args=[obj.pk]))
        elif '_publish' in request.POST:
            return HttpResponseRedirect(f"{reverse('custom_admin:app_article_changelist')}?published=1#published")
        elif '_save' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))
        return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))

    def response_change(self, request, obj):
        # 消息已在 save_model 中添加，这里只处理重定向
        if '_addanother' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_add'))
        elif '_publish' in request.POST:
            return HttpResponseRedirect(f"{reverse('custom_admin:app_article_changelist')}?published=1#published")
        elif '_continue' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_change', args=[obj.pk]))
        elif '_save' in request.POST:
            return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))
        return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))

    def add_view(self, request, form_url='', extra_context=None):
        """重写添加视图，完全绕过表单验证"""
        if request.method == 'POST':
            # 直接创建对象，不经过表单验证
            obj = Article()
            obj.title = request.POST.get('title', '未命名文章') or '未命名文章'
            obj.content_md = request.POST.get('content_md', '') or ''
            obj.is_hidden = request.POST.get('is_hidden') == 'on'
            obj.allow_comment = request.POST.get('allow_comment', 'on') == 'on'
            obj.published_at = timezone.now()
            
            # 处理封面图片
            if 'cover' in request.FILES:
                obj.cover = request.FILES['cover']
            
            # 发布操作
            if '_publish' in request.POST:
                obj.is_hidden = False
            
            # 直接保存
            try:
                obj.save()
                
                # 保存标签
                if 'tags' in request.POST:
                    tag_ids = request.POST.getlist('tags')
                    from .models import Tag
                    for tag_id in tag_ids:
                        try:
                            tag = Tag.objects.get(pk=tag_id)
                            obj.tags.add(tag)
                        except (Tag.DoesNotExist, ValueError):
                            pass
                
                # 成功提示
                if '_publish' in request.POST:
                    messages.success(request, '🎉 文章发布成功')
                elif '_continue' in request.POST:
                    messages.success(request, '💾 文章已保存，继续编辑')
                    return HttpResponseRedirect(reverse('custom_admin:app_article_change', args=[obj.pk]))
                elif '_addanother' in request.POST:
                    messages.success(request, '💾 文章创建成功')
                    return HttpResponseRedirect(reverse('custom_admin:app_article_add'))
                else:
                    messages.success(request, '💾 文章创建成功')
                
                return HttpResponseRedirect(f"{reverse('custom_admin:app_article_changelist')}?published=1#published")
            except Exception as e:
                logger.error("Error saving article: %s", str(e))
                messages.error(request, f'保存失败: {str(e)}')
        
        # GET 请求，显示表单
        return super().add_view(request, form_url, extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """重写编辑视图，完全绕过表单验证"""
        if request.method == 'POST' and object_id:
            try:
                obj = Article.objects.get(pk=object_id)
                
                # 直接更新字段，不经过表单验证
                if 'title' in request.POST:
                    obj.title = request.POST.get('title', '未命名文章') or '未命名文章'
                if 'content_md' in request.POST:
                    obj.content_md = request.POST.get('content_md', '') or ''
                if 'is_hidden' in request.POST:
                    obj.is_hidden = request.POST.get('is_hidden') == 'on'
                else:
                    obj.is_hidden = False
                if 'allow_comment' in request.POST:
                    obj.allow_comment = request.POST.get('allow_comment') == 'on'
                else:
                    obj.allow_comment = True
                
                # 处理封面图片
                if 'cover' in request.FILES:
                    obj.cover = request.FILES['cover']
                
                # 发布操作
                if '_publish' in request.POST:
                    obj.is_hidden = False
                
                # 直接保存
                obj.save()
                
                # 保存标签
                if 'tags' in request.POST:
                    obj.tags.clear()
                    tag_ids = request.POST.getlist('tags')
                    from .models import Tag
                    for tag_id in tag_ids:
                        try:
                            tag = Tag.objects.get(pk=tag_id)
                            obj.tags.add(tag)
                        except (Tag.DoesNotExist, ValueError):
                            pass
                
                # 成功提示
                if '_publish' in request.POST:
                    messages.success(request, '🎉 文章发布成功')
                    return HttpResponseRedirect(f"{reverse('custom_admin:app_article_changelist')}?published=1#published")
                elif '_continue' in request.POST:
                    messages.success(request, '💾 文章已保存，继续编辑')
                    return HttpResponseRedirect(reverse('custom_admin:app_article_change', args=[obj.pk]))
                elif '_addanother' in request.POST:
                    messages.success(request, '✅ 文章更新成功')
                    return HttpResponseRedirect(reverse('custom_admin:app_article_add'))
                else:
                    messages.success(request, '✅ 文章更新成功')
                    return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))
            except Article.DoesNotExist:
                messages.error(request, '文章不存在')
                return HttpResponseRedirect(reverse('custom_admin:app_article_changelist'))
            except Exception as e:
                logger.error("Error updating article: %s", str(e))
                messages.error(request, f'保存失败: {str(e)}')
        
        # GET 请求，显示表单
        return super().changeform_view(request, object_id, form_url, extra_context)




class CustomAdminSite(admin.AdminSite):
    site_header = "🌸 盘古大仙洞府后台"
    site_title = "🌸 盘古大仙洞府后台"
    index_title = "管理面板"
    login_template = "admin/pink_login.html"

    def index(self, request, extra_context=None):
        """自定义粉色系管理面板首页"""
        context = {
            **self.each_context(request),
            'title': self.index_title,
            'article_count': Article.objects.count(),
            'tag_count': Tag.objects.count(),
            'visible_count': Article.objects.filter(is_hidden=False).count(),
            'recent_articles': Article.objects.select_related().order_by('-published_at')[:5],
            **(extra_context or {}),
        }

        request.current_app = self.name
        return render(request, 'admin/pink_index.html', context)

# 创建自定义管理站点
admin_site = CustomAdminSite(name='custom_admin')

# 注册模型到自定义管理站点
admin_site.register(Article, ArticleAdmin)
admin_site.register(Tag, TagAdmin)

# 保留默认admin的注册，但使用自定义站点作为主要界面
admin.site.site_header = "盘古大仙洞府后台"
admin.site.site_title = "盘古大仙洞府后台"
admin.site.index_title = "管理面板"
