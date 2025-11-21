# 盘古大仙洞府

> Django + GitHub Pages 静态博客系统

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 特性

- 🎨 **AI 科技主题首页** - 动画机器人、3D 网格背景、浮动粒子
- ✍️ **Markdown 文章** - 支持 Markdown 编写，自动渲染
- 🏷️ **标签分类** - 文章标签管理和筛选
- 🔒 **安全可靠** - 只读 API，无数据篡改风险
- 📱 **响应式设计** - 适配各种设备
- 🚀 **自动部署** - 推送代码自动部署到 GitHub Pages

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Pangu-Immortal/Pangu-Immortal.github.io.git
cd Pangu-Immortal.github.io
```

### 2. 配置 Conda 环境

#### 初始化 Conda（首次使用需要）

```bash
# 初始化 conda（根据你的 shell 类型选择）
conda init bash    # 如果使用 bash
conda init zsh     # 如果使用 zsh

# 重新加载配置
source ~/.bashrc   # bash 用户
source ~/.zshrc    # zsh 用户
```

#### 激活 Conda 环境

```bash
# 激活 base 环境
conda activate base

# 或激活项目特定环境（如果已创建）
conda activate your_env_name
```

#### 验证环境

```bash
# 检查 Python 版本
python --version

# 检查 conda 环境
conda info --envs
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 使用项目提供的环境配置脚本
source scripts/dev.sh
```

### 5. 初始化数据库

```bash
# 运行数据库迁移
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
python manage.py runserver
```

访问：
- **前台首页**：http://127.0.0.1:8000/
- **管理后台**：http://127.0.0.1:8000/backend/
- **默认账号**：admin / admin123（如已预创建）

## 📝 发布文章流程

### 方式一：完整手动流程

```bash
# 1. 确保在 conda 环境中
conda activate base
source scripts/dev.sh

# 2. 访问后台创建/编辑文章
# 打开浏览器：http://127.0.0.1:8000/backend/
# 使用管理员账号登录，创建或编辑文章

# 3. 生成静态站点
python manage.py generate_static_site

# 4. 提交并推送到 GitHub
git add .
git commit -m "📝 新增文章：文章标题"
git push origin main
```

### 方式二：直接操作数据库

```bash
# 进入 Django Shell
conda activate base
source scripts/dev.sh
python manage.py shell

# 在 Shell 中创建文章
from app.models import Article, Tag
from django.utils import timezone

# 创建标签
tag1 = Tag.objects.create(name="技术")
tag2 = Tag.objects.create(name="教程")

# 创建文章
article = Article.objects.create(
    title="文章标题",
    content_md="# 标题\n\n文章内容...",
    published_at=timezone.now(),
    is_hidden=False
)
article.tags.add(tag1, tag2)

# 退出 Shell（Ctrl+D）

# 生成静态站点并推送
python manage.py generate_static_site
git add .
git commit -m "📝 新增文章：文章标题"
git push origin main
```

## 📖 完整文档

详细文档请查看：**[GUIDE.md](GUIDE.md)**

包含：
- 完整使用说明
- API 文档
- 故障排查
- 最佳实践

## 🎨 首页效果

- 🌌 全屏 AI 主题渐变背景
- 🤖 CSS 动画机器人（浮动、眨眼、挥手）
- ✨ 3D 网格背景动画
- 💫 50 个浮动粒子效果
- 🌈 渐变发光标题

## 🛠️ 技术栈

- **后端**：Django 5.0
- **数据库**：SQLite
- **Markdown**：MarkdownX
- **样式**：CSS3 + 动画
- **部署**：GitHub Pages
- **环境管理**：Conda + 自定义环境脚本

## ⚙️ 常用命令

### 环境相关

```bash
# 激活 conda 环境
conda activate base

# 加载项目环境变量
source scripts/dev.sh

# 查看当前环境
conda info --envs
which python
```

### 数据库相关

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 进入数据库 Shell
python manage.py dbshell

# 进入 Django Shell
python manage.py shell
```

### 静态文件生成

```bash
# 生成静态站点到 docs/ 目录
python manage.py generate_static_site

# 查看生成的文件
ls -la docs/
```

### Git 操作

```bash
# 查看状态
git status

# 添加所有改动
git add .

# 提交改动
git commit -m "提交信息"

# 推送到远程
git push origin main

# 查看提交历史
git log --oneline -10
```

## 🔧 故障排查

### 问题1：无法找到 python 命令

**原因**：未激活 conda 环境

**解决**：
```bash
conda activate base
```

### 问题2：Django 模块未找到

**原因**：依赖未安装或环境变量未加载

**解决**：
```bash
source scripts/dev.sh
pip install -r requirements.txt
```

### 问题3：后台无法登录

**原因**：未创建管理员账号

**解决**：
```bash
python manage.py createsuperuser
# 或使用预设账号：admin / admin123
```

### 问题4：静态文件生成失败

**原因**：数据库未迁移或文章格式错误

**解决**：
```bash
python manage.py migrate
python manage.py generate_static_site
# 查看详细错误信息
```

### 问题5：Git 推送失败

**原因**：权限不足或网络问题

**解决**：
```bash
# 检查远程仓库
git remote -v

# 使用 token 推送（替换 YOUR_TOKEN）
git push https://YOUR_TOKEN@github.com/Pangu-Immortal/Pangu-Immortal.github.io.git main
```

## 📝 License

MIT License

## 👤 作者

盘古大仙

- Website: https://pangu-immortal.github.io/
- GitHub: [@Pangu-Immortal](https://github.com/Pangu-Immortal)

---

**⭐ 如果觉得不错，请给个 Star！**
