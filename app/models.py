from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from django.conf import settings
import os


def upload_cover_path(instance, filename):
    # 保存到 media/covers/年/月/文件名
    return f"covers/{timezone.now().strftime('%Y/%m')}/{filename}"


class Tag(models.Model):
    """标签模型：用于对文章进行分类与筛选"""
    name = models.CharField("名称", max_length=32, unique=True)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Article(models.Model):
    """文章模型：存储 Markdown 内容、封面、标签与发布时间"""
    title = models.CharField("标题", max_length=200, blank=True, default='')
    content_md = models.TextField("内容（Markdown）", blank=True, default='')
    cover = models.ImageField("预览图", upload_to=upload_cover_path, blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True, related_name="articles")
    published_at = models.DateTimeField("发布时间", default=timezone.now)
    is_hidden = models.BooleanField("是否隐藏", default=False)
    # allow_comment 字段已移除（评论功能已删除）

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "文章"
        verbose_name_plural = "文章"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """保存后为封面写入网站名称水印"""
        super().save(*args, **kwargs)
        if self.cover:
            try:
                cover_path = Path(settings.MEDIA_ROOT) / self.cover.name
                if cover_path.exists():
                    img = Image.open(cover_path).convert("RGBA")
                    watermark_text = "盘古大仙洞府"
                    # 动态计算字号
                    font_size = max(14, int(min(img.size) * 0.04))
                    try:
                        font = ImageFont.truetype("Arial.ttf", font_size)
                    except Exception:
                        font = ImageFont.load_default()
                    text_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
                    draw = ImageDraw.Draw(text_layer)
                    text_w, text_h = draw.textsize(watermark_text, font=font)
                    margin = int(min(img.size) * 0.02)
                    x = img.width - text_w - margin
                    y = img.height - text_h - margin
                    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 120))
                    watermarked = Image.alpha_composite(img, text_layer).convert("RGB")
                    watermarked.save(cover_path)
            except Exception:
                # 忽略水印异常，确保保存流程不被阻断
                pass


# 评论和留言板功能已移除
# 理由：GitHub Pages 纯静态托管，无法保存用户提交的数据
# 如需此类功能，建议使用第三方服务（Disqus、Giscus、Utterances）
