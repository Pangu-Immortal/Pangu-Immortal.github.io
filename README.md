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

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动开发服务器

```bash
source scripts/dev.sh
python manage.py runserver
```

访问：
- 前台：http://127.0.0.1:8000/
- 后台：http://127.0.0.1:8000/backend/

### 4. 创建管理员

```bash
python manage.py createsuperuser
```

## 📝 发布文章

```bash
# 1. 访问后台创建文章
http://127.0.0.1:8000/backend/

# 2. 生成静态站点
python manage.py generate_static_site

# 3. 推送到 GitHub
git add .
git commit -m "📝 新增文章"
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

## 📝 License

MIT License

## 👤 作者

盘古大仙

- Website: https://pangu-immortal.github.io/
- GitHub: [@Pangu-Immortal](https://github.com/Pangu-Immortal)

---

**⭐ 如果觉得不错，请给个 Star！**
