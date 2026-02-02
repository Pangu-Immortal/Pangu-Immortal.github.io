

# 盘古大仙洞府

<div align="center">

![萌萌计数器](https://count.getloli.com/get/@Pangu-Immortal.github.io?theme=rule34)

</div>

<p align="center">
  <b>⭐ 点击 <a href="https://github.com/Pangu-Immortal/Pangu-Immortal.github.io">Star</a>，关注不迷路 ⭐</b>
</p>

> Django + GitHub Pages 静态博客系统

[![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Conda](https://img.shields.io/badge/Conda-RunProject-brightgreen.svg)](https://docs.conda.io/)
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

> **⚠️ 重要**：本项目必须在 `RunProject` conda 环境中运行，Python 版本为 3.14

#### 初始化 Conda（首次使用需要）

```bash
# 初始化 conda（根据你的 shell 类型选择）
conda init bash    # 如果使用 bash
conda init zsh     # 如果使用 zsh

# 重新加载配置
source ~/.bashrc   # bash 用户
source ~/.zshrc    # zsh 用户
```

#### 创建项目专属环境（如果尚未创建）

```bash
# 创建名为 RunProject 的 Python 3.14 环境
conda create -n RunProject python=3.14 -y

# 列出所有环境，确认创建成功
conda env list
```

#### 激活 RunProject 环境

```bash
# 激活项目环境（所有后续操作都必须在此环境中）
conda activate RunProject
```

#### 验证环境

```bash
# 检查当前环境名称（应显示 RunProject）
echo $CONDA_DEFAULT_ENV

# 检查 Python 版本（应显示 3.14.x）
python --version

# 检查 conda 环境列表（RunProject 前应有 * 标记）
conda info --envs
```

### 3. 安装依赖

```bash
# 确保在 RunProject 环境中
conda activate RunProject

# 安装项目依赖
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 确保在 RunProject 环境中
conda activate RunProject

# 使用项目提供的环境配置脚本
source scripts/dev.sh
```

### 5. 初始化数据库

```bash
# 确保在 RunProject 环境中
conda activate RunProject
source scripts/dev.sh

# 运行数据库迁移
python manage.py migrate

# 创建管理员账号
python manage.py createsuperuser
```

### 6. 启动开发服务器

```bash
# 确保在 RunProject 环境中
conda activate RunProject
source scripts/dev.sh

# 启动服务器
python manage.py runserver
```

访问：
- **前台首页**：http://127.0.0.1:8000/
- **管理后台**：http://127.0.0.1:8000/backend/

## 📝 发布文章流程

> **⚠️ 所有操作必须在 RunProject conda 环境中执行**

### 方式一：完整手动流程

```bash
# 1. 激活 RunProject 环境并加载配置
conda activate RunProject
source scripts/dev.sh

# 2. 启动开发服务器（如果未启动）
python manage.py runserver

# 3. 访问后台创建/编辑文章
# 打开浏览器：http://127.0.0.1:8000/backend/
# 使用管理员账号登录，创建或编辑文章

# 4. 生成静态站点
python manage.py generate_static_site

# 5. 提交并推送到 GitHub
git add .
git commit -m "📝 新增文章：文章标题"
git push origin main
```

### 方式二：直接操作数据库（高级用户）

```bash
# 1. 激活 RunProject 环境并加载配置
conda activate RunProject
source scripts/dev.sh

# 2. 进入 Django Shell
python manage.py shell

# 3. 在 Shell 中创建文章
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

# 退出 Shell（Ctrl+D 或 exit()）

# 4. 生成静态站点并推送
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
- **Python**：3.14
- **数据库**：SQLite
- **Markdown**：MarkdownX
- **样式**：CSS3 + 动画
- **部署**：GitHub Pages
- **环境管理**：Conda (RunProject 环境) + 自定义环境脚本

## ⚙️ 常用命令

> **⚠️ 所有命令必须在 RunProject conda 环境中执行**

### 环境相关

```bash
# 激活 RunProject 环境（所有操作的第一步）
conda activate RunProject

# 加载项目环境变量
source scripts/dev.sh

# 查看当前环境（应显示 RunProject 前有 * 标记）
conda info --envs

# 查看 Python 路径（应指向 RunProject 环境）
which python

# 查看 Python 版本（应显示 3.14.x）
python --version

# 查看当前激活的环境名称
echo $CONDA_DEFAULT_ENV
```

### 数据库相关

```bash
# 激活环境（如果尚未激活）
conda activate RunProject
source scripts/dev.sh

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
# 激活环境（如果尚未激活）
conda activate RunProject
source scripts/dev.sh

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

### 问题1：无法找到 python 命令或 Python 版本不对

**原因**：未激活 RunProject conda 环境

**解决**：
```bash
# 激活 RunProject 环境
conda activate RunProject

# 验证环境
echo $CONDA_DEFAULT_ENV  # 应输出: RunProject
python --version         # 应输出: Python 3.14.x
```

### 问题2：Django 模块未找到

**原因**：依赖未安装或环境变量未加载

**解决**：
```bash
# 确保在 RunProject 环境中
conda activate RunProject

# 加载环境变量
source scripts/dev.sh

# 重新安装依赖
pip install -r requirements.txt
```

### 问题3：conda activate 命令不可用

**原因**：conda 未初始化

**解决**：
```bash
# 初始化 conda（根据 shell 类型）
conda init bash  # 或 conda init zsh

# 重新加载配置
source ~/.bashrc  # 或 source ~/.zshrc

# 关闭并重新打开终端，然后再次尝试
conda activate RunProject
```

### 问题4：后台无法登录

**原因**：未创建管理员账号

**解决**：
```bash
# 在 RunProject 环境中
conda activate RunProject
source scripts/dev.sh

# 创建超级用户
python manage.py createsuperuser

# 或使用预设账号：admin / admin123
```

### 问题5：静态文件生成失败

**原因**：数据库未迁移或文章格式错误

**解决**：
```bash
# 在 RunProject 环境中
conda activate RunProject
source scripts/dev.sh

# 运行迁移
python manage.py migrate

# 生成静态站点（查看详细错误）
python manage.py generate_static_site
```

### 问题6：Git 推送失败

**原因**：权限不足或网络问题

**解决**：
```bash
# 检查远程仓库
git remote -v

# 使用 token 推送（替换 YOUR_TOKEN）
git push https://YOUR_TOKEN@github.com/Pangu-Immortal/Pangu-Immortal.github.io.git main
```

### 问题7：找不到 RunProject 环境

**原因**：环境尚未创建

**解决**：
```bash
# 创建 RunProject 环境
conda create -n RunProject python=3.14 -y

# 激活环境
conda activate RunProject

# 安装依赖
pip install -r requirements.txt
```

## 📝 License

MIT License

## 👤 作者

盘古大仙

- Website: https://pangu-immortal.github.io/
- GitHub: [@Pangu-Immortal](https://github.com/Pangu-Immortal)

---

**⭐ 如果觉得不错，请给个 Star！**

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Pangu-Immortal/Pangu-Immortal.github.io&type=Date)](https://star-history.com/#Pangu-Immortal/Pangu-Immortal.github.io&Date)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
