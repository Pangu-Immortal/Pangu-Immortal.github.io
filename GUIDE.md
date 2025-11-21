# 📖 网站管理指南

> 盘古大仙洞府 - Django + GitHub Pages 静态博客系统

---

## 🚀 快速开始

### 1. 本地开发

```bash
# 启动开发服务器
cd /Users/qihao/PycharmProjects/Pangu-Immortal.github.io
source scripts/dev.sh
python manage.py runserver
```

访问：
- **前台**：http://127.0.0.1:8000/
- **后台**：http://127.0.0.1:8000/backend/

---

## ✍️ 发布文章

### 完整流程

```bash
# 1. 启动服务器
python manage.py runserver

# 2. 访问后台创建文章
# http://127.0.0.1:8000/backend/
# 点击"文章" → "添加文章"
# 填写标题、内容（Markdown）、封面、标签

# 3. 生成静态站点
python manage.py generate_static_site

# 4. 提交到 Git
git add .
git commit -m "📝 新增文章: 文章标题"
git push origin main

# 5. 等待部署（1-2 分钟）
# 访问 https://pangu-immortal.github.io/
```

### 快速发布脚本

```bash
# 使用已有的发布脚本
./scripts/publish.sh
```

---

## 🗑️ 删除数据

### 删除文章

```bash
# 1. 访问后台
http://127.0.0.1:8000/backend/

# 2. 点击"文章"
# 3. 勾选要删除的文章
# 4. 选择"删除所选的文章"
# 5. 确认删除
```

### Django Shell 方式

```bash
python manage.py shell
```

```python
from app.models import Article, Tag

# 删除单篇文章
Article.objects.get(id=1).delete()

# 批量删除
Article.objects.filter(title__contains='关键词').delete()

# 删除所有文章（危险！）
Article.objects.all().delete()
```

### ⚠️ 重要

**删除后必须重新生成静态站点**：

```bash
python manage.py generate_static_site
git add .
git commit -m "🗑️ 删除数据"
git push origin main
```

---

## 🏗️ 架构说明

### 技术栈

- **后端**：Django 5.0
- **模板**：Django Templates
- **部署**：GitHub Pages（静态托管）
- **管理**：Django Admin（粉色主题）

### 工作原理

1. **本地开发**：Django 动态渲染
2. **生成静态**：`generate_static_site` 命令生成 HTML
3. **部署**：推送 `docs/` 目录到 GitHub
4. **访问**：GitHub Pages 托管静态文件

### 数据模型

```python
# 文章
class Article(models.Model):
    title = models.CharField("标题", max_length=200)
    content_md = models.TextField("内容（Markdown）")
    cover = models.ImageField("封面")
    tags = models.ManyToManyField(Tag)
    published_at = models.DateTimeField("发布时间")
    is_hidden = models.BooleanField("是否隐藏")

# 标签
class Tag(models.Model):
    name = models.CharField("名称", max_length=32)
```

**注意**：评论和留言板功能已移除（GitHub Pages 无法保存用户数据）

---

## 📁 目录结构

```
Pangu-Immortal.github.io/
├── app/                    # Django 应用
│   ├── models.py          # 数据模型
│   ├── views.py           # 视图函数
│   ├── api_views.py       # API 接口
│   ├── urls.py            # URL 路由
│   ├── admin.py           # 后台管理
│   └── management/        # 管理命令
│       └── commands/
│           └── generate_static_site.py
├── templates/             # 模板文件
│   ├── base.html         # 基础模板
│   ├── index.html        # AI 主题首页
│   ├── list.html         # 文章列表
│   ├── detail.html       # 文章详情
│   └── about.html        # 关于页面
├── static/               # 静态资源
├── media/                # 上传文件
├── docs/                 # 生成的静态站点
├── db.sqlite3            # SQLite 数据库
├── manage.py             # Django 管理工具
└── scripts/
    ├── dev.sh            # 开发环境脚本
    └── publish.sh        # 发布脚本
```

---

## 🔒 API 说明

### 可用 API（只读）

- `GET /api/articles/` - 获取文章列表
- `GET /api/articles/<id>/` - 获取文章详情
- `GET /api/about/` - 获取关于信息

### 安全措施

✅ 所有写入 API 已禁用（POST/PUT/DELETE）
✅ 只允许读取操作（GET）
✅ 无数据篡改风险

---

## 💾 数据备份

### 备份数据库

```bash
# 创建备份
cp db.sqlite3 backups/db.sqlite3.$(date +%Y%m%d_%H%M%S)

# 备份媒体文件
cp -r media backups/media.$(date +%Y%m%d_%H%M%S)
```

### 恢复备份

```bash
# 恢复数据库
cp backups/db.sqlite3.backup db.sqlite3

# 恢复媒体文件
cp -r backups/media.backup/* media/
```

---

## 🎨 首页设计

### AI 科技主题

- 🌌 渐变背景
- 🤖 CSS 动画机器人
- ✨ 3D 网格背景
- 💫 浮动粒子效果
- 🌈 发光标题
- 🔘 "探索宇宙"按钮

### 自定义

修改 `templates/index.html` 调整首页样式。

---

## 🛠️ 常用命令

```bash
# 启动开发服务器
python manage.py runserver

# 创建管理员账号
python manage.py createsuperuser

# 生成静态站点
python manage.py generate_static_site

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# Django Shell
python manage.py shell

# 收集静态文件
python manage.py collectstatic
```

---

## 🚨 故障排查

### 问题 1：删除文章后 GitHub Pages 还显示

**原因**：未重新生成静态站点

**解决**：
```bash
python manage.py generate_static_site
git add . && git commit -m "更新" && git push
```

### 问题 2：推送失败

**原因**：网络问题或认证失败

**解决**：
```bash
# 使用 Token 推送
git push https://TOKEN@github.com/Pangu-Immortal/Pangu-Immortal.github.io.git main

# 或配置 SSH
git remote set-url origin git@github.com:Pangu-Immortal/Pangu-Immortal.github.io.git
```

### 问题 3：首页显示异常

**原因**：浏览器缓存

**解决**：
- 强制刷新：Ctrl+Shift+R（Windows）或 Cmd+Shift+R（Mac）
- 清除浏览器缓存

---

## 📊 部署状态

### GitHub Pages 配置

1. 访问：https://github.com/Pangu-Immortal/Pangu-Immortal.github.io/settings/pages
2. 设置：
   - Source: Deploy from a branch
   - Branch: **main**
   - Folder: **/docs**

### 查看部署

- **部署日志**：https://github.com/Pangu-Immortal/Pangu-Immortal.github.io/actions
- **线上站点**：https://pangu-immortal.github.io/

---

## 📝 Git 工作流

### 标准流程

```bash
# 1. 查看状态
git status

# 2. 添加更改
git add .

# 3. 提交
git commit -m "📝 描述信息"

# 4. 推送
git push origin main
```

### Commit 规范

- 📝 新增文章
- 🗑️ 删除数据
- 🎨 样式调整
- 🐛 修复问题
- 🔒 安全更新
- 📚 文档更新

---

## 🆘 获取帮助

- **Django 文档**：https://docs.djangoproject.com/
- **Markdown 语法**：https://markdown.com.cn/
- **GitHub Pages**：https://pages.github.com/

---

## 📋 检查清单

### 发布前

- [ ] 文章内容无误
- [ ] 标题和封面正确
- [ ] 标签已设置
- [ ] 本地预览正常

### 发布后

- [ ] 生成静态站点
- [ ] Git 提交推送
- [ ] 等待部署完成
- [ ] 线上验证效果

---

**最后更新**：2025-11-21
**版本**：v2.0
**状态**：✅ 生产就绪
