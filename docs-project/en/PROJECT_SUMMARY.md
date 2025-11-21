# 项目重构总结

## 🎯 重构目标

1. **后台发布 → 静态生成**: Django 后台发布文章自动生成静态 HTML
2. **GitHub Pages 部署**: 静态站点部署到 https://pangu-immortal.github.io
3. **保持自定义样式**: 使用现有科技风样式,不引入三方模板
4. **完整文档**: 提供详细的开发和部署文档

## ✅ 已完成功能

### 1. 静态站点生成系统

**核心文件**:
- `app/management/commands/generate_static_site.py` - 静态生成命令
- `app/signals.py` - 自动触发信号
- `app/apps.py` - 信号注册

**功能特性**:
- ✅ 将所有 Django 模板渲染为静态 HTML
- ✅ 支持分页和标签筛选
- ✅ 自动复制 static 和 media 资源
- ✅ 生成 sitemap.xml
- ✅ 输出到 `docs/` 目录供 GitHub Pages 使用

**自动触发**:
- 文章创建/编辑/删除 → 自动重新生成
- 标签变更 → 自动重新生成
- 评论变更 → 自动重新生成

### 2. 模板双模式支持

**修改的模板**:
- `templates/base.html` - 导航链接适配
- `templates/list.html` - 文章列表和分页链接
- `templates/detail.html` - 文章详情和评论区

**实现方式**:
```django
{% if is_static %}
  <!-- 静态模式: 使用 .html 文件链接 -->
  <a href="article_1.html">文章标题</a>
{% else %}
  <!-- 动态模式: 使用 Django URL -->
  <a href="/articles/1/">文章标题</a>
{% endif %}
```

### 3. GitHub 部署配置

**创建的文件**:
- `.gitignore` - Git 忽略规则 (排除数据库,保留 docs/)
- `DEPLOYMENT.md` - 快速部署指南
- `README.md` - 完整文档 (已重写)

**部署流程**:
```bash
# 1. 生成静态站点
python manage.py generate_static_site

# 2. 提交到 Git
git add docs/
git commit -m "Update: 新增文章"

# 3. 推送到 GitHub
git push origin main

# 4. GitHub Pages 自动部署
```

## 📋 项目架构

```
发布流程:
Django 后台编辑文章
    ↓ (保存)
触发 post_save 信号
    ↓
自动执行 generate_static_site 命令
    ↓
渲染模板为静态 HTML → docs/
复制 static 资源 → docs/static/
复制 media 文件 → docs/media/
生成 sitemap.xml
    ↓
开发者执行 Git 操作
    ↓
git add docs/ && git commit && git push
    ↓
GitHub Pages 自动部署
    ↓
https://pangu-immortal.github.io 更新
```

## 📂 新增/修改的文件

### 新增文件
```
app/management/
├── __init__.py
└── commands/
    ├── __init__.py
    └── generate_static_site.py      # 静态生成核心逻辑

app/signals.py                        # 自动触发信号

.gitignore                            # Git 配置
DEPLOYMENT.md                         # 快速部署指南
test_static_generation.sh             # 测试脚本
```

### 修改文件
```
README.md                             # 重写完整文档
templates/base.html                   # 导航链接双模式
templates/list.html                   # 列表页双模式
templates/detail.html                 # 详情页双模式
app/apps.py                           # 注册信号
```

## 🚀 使用指南

### 本地开发

1. **激活环境**:
   ```bash
   conda activate RunProject
   python manage.py runserver
   ```

2. **后台管理**:
   - 访问: http://127.0.0.1:8000/admin/
   - 创建/编辑文章
   - 保存后自动生成静态站点

3. **查看生成结果**:
   ```bash
   ls docs/
   ```

### 部署到 GitHub Pages

#### 首次部署

1. **创建仓库**:
   - 仓库名: `Pangu-Immortal/pangu-immortal.github.io`
   - 可见性: Public

2. **初始化 Git**:
   ```bash
   git init
   git remote add origin https://github.com/Pangu-Immortal/pangu-immortal.github.io.git
   ```

3. **配置认证** (选一种):
   - **SSH** (推荐):
     ```bash
     ssh-keygen -t ed25519 -C "your_email@example.com"
     cat ~/.ssh/id_ed25519.pub
     # 添加到 GitHub: Settings → SSH and GPG keys
     git remote set-url origin git@github.com:Pangu-Immortal/pangu-immortal.github.io.git
     ```

   - **PAT** (Personal Access Token):
     - 生成: https://github.com/settings/tokens
     - 勾选 `repo` 权限
     - 推送时使用 token 作为密码

4. **生成并推送**:
   ```bash
   python manage.py generate_static_site
   git add .
   git commit -m "Initial commit: Blog with static site"
   git branch -M main
   git push -u origin main
   ```

5. **启用 GitHub Pages**:
   - 进入仓库 Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main`
   - Folder: `/docs` ⚠️ 必须选 /docs
   - 点击 Save

6. **等待部署**:
   - 1-2 分钟后访问: https://pangu-immortal.github.io

#### 日常更新

```bash
# 1. 在后台保存文章 (自动生成静态站点)

# 2. 提交更新
git add docs/
git commit -m "Update: 新增文章《文章标题》"
git push origin main

# 3. 等待 1-2 分钟访问网站
```

## 🔧 技术细节

### 静态生成命令

**核心逻辑**:
```python
# app/management/commands/generate_static_site.py

1. 清空 docs/ 目录
2. 渲染首页 (index.html)
3. 渲染文章列表 (含分页和标签筛选)
4. 渲染所有文章详情页
5. 渲染关于/留言板页面
6. 复制 static/ → docs/static/
7. 复制 media/ → docs/media/
8. 生成 sitemap.xml
9. 创建 .nojekyll (GitHub Pages 需要)
```

### 信号自动触发

**触发条件**:
```python
# app/signals.py

@receiver([post_save, post_delete], sender=Article)
def regenerate_on_article_change(sender, instance, **kwargs):
    call_command('generate_static_site')

# 同样适用于 Tag 和 Comment
```

### 模板适配

**静态模式判断**:
```django
{% if is_static %}
  <a href="list.html">文章列表</a>
  <img src="media/covers/image.jpg">
{% else %}
  <a href="/articles/">文章列表</a>
  <img src="{{ article.cover.url }}">
{% endif %}
```

## ⚠️ 注意事项

### 不要提交到 GitHub 的文件

- ❌ `db.sqlite3` - 数据库 (已在 .gitignore)
- ❌ `media/` - 原始上传文件 (已在 .gitignore)
- ❌ `staticfiles/` - 收集的静态文件
- ✅ `docs/` - **必须提交** (GitHub Pages 发布源)

### 数据安全

- 数据库 `db.sqlite3` 只存在本地
- 定期备份:
  ```bash
  python manage.py dumpdata > backup.json
  ```
- 恢复:
  ```bash
  python manage.py loaddata backup.json
  ```

### 静态站点限制

- ❌ 评论功能不可用 (需要后端)
- ❌ 搜索功能受限
- ✅ 文章阅读完全正常
- ✅ 标签筛选正常
- ✅ 分页导航正常

## 🐛 常见问题

### Q: 推送失败 (权限错误)?
**A**: 配置 SSH 密钥或 PAT (见 DEPLOYMENT.md 第四节)

### Q: GitHub Pages 显示 404?
**A**: 检查:
- 仓库名是否为 `<用户名>.github.io`
- 仓库是否 Public
- Pages 设置是否选择 `/docs`
- `docs/index.html` 是否存在

### Q: 样式丢失?
**A**:
```bash
python manage.py generate_static_site
ls docs/static/  # 检查是否存在
```

### Q: 如何禁用自动生成?
**A**: 编辑 `app/signals.py`,注释掉信号函数

## 📚 文档索引

- **[README.md](README.md)** - 完整文档 (开发 + 部署 + FAQ)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 快速部署指南
- **本文档** - 重构总结和技术细节

## 🎉 重构成果

✅ **后台发布 → 自动生成静态站点**
✅ **静态站点 → GitHub Pages 一键部署**
✅ **保持自定义科技风样式**
✅ **完整文档 (开发 + 部署 + 交接)**

---

**项目重构完成! 现在可以开始使用了!** 🚀

下一步:
1. 在 Django 后台创建文章测试
2. 执行 `python manage.py generate_static_site`
3. 按照 DEPLOYMENT.md 推送到 GitHub
4. 在 https://pangu-immortal.github.io 查看效果
