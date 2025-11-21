# 🚀 命令速查表

快速参考常用命令。

---

## 📦 环境管理

```bash
# 激活环境
conda activate RunProject

# 安装依赖
pip install -r requirements.txt

# 退出环境
conda deactivate
```

---

## 🗄️ 数据库操作

```bash
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 备份数据
python manage.py dumpdata > backup.json

# 恢复数据
python manage.py loaddata backup.json
```

---

## 🚀 开发服务器

```bash
# 启动开发服务器
python manage.py runserver

# 指定端口
python manage.py runserver 8080

# 允许外部访问
python manage.py runserver 0.0.0.0:8000
```

**访问地址**:
- 前台: http://127.0.0.1:8000/
- 后台: http://127.0.0.1:8000/admin/

---

## 📄 静态站点生成

```bash
# 生成静态站点到 docs/
python manage.py generate_static_site

# 查看生成结果
ls docs/

# 查看生成的文章
ls docs/article_*.html

# 检查静态资源
ls docs/static/
ls docs/media/
```

---

## 🔧 Git 操作

### 初始化

```bash
# 初始化仓库
git init

# 添加远程仓库
git remote add origin https://github.com/Pangu-Immortal/pangu-immortal.github.io.git

# 查看远程仓库
git remote -v

# 修改远程仓库地址
git remote set-url origin <新地址>
```

### 日常操作

```bash
# 查看状态
git status

# 添加文件
git add .                    # 添加所有
git add docs/                # 只添加 docs/
git add README.md            # 添加单个文件

# 提交
git commit -m "提交信息"

# 推送
git push origin main         # 推送到 main 分支
git push -u origin main      # 首次推送 (设置上游)

# 拉取
git pull origin main
```

### 分支操作

```bash
# 查看分支
git branch

# 创建分支
git branch dev

# 切换分支
git checkout dev

# 创建并切换
git checkout -b feature-new

# 重命名当前分支
git branch -M main
```

### 查看历史

```bash
# 查看提交历史
git log

# 简洁格式
git log --oneline

# 查看最近 5 条
git log --oneline -5

# 查看差异
git diff                     # 未暂存的修改
git diff --cached            # 已暂存的修改
```

---

## 🌐 GitHub Pages 部署

### 一键部署

```bash
# 使用部署脚本
bash deploy.sh
```

### 手动部署

```bash
# 1. 生成静态站点
python manage.py generate_static_site

# 2. 提交
git add docs/
git commit -m "Update: 新增文章"

# 3. 推送
git push origin main
```

---

## 🔍 调试命令

```bash
# Django Shell
python manage.py shell

# 检查项目配置
python manage.py check

# 收集静态文件
python manage.py collectstatic

# 清空数据库 (危险!)
python manage.py flush

# 查看所有命令
python manage.py help
```

---

## 📊 文件操作

```bash
# 查看项目结构
tree -L 2 -I '__pycache__|node_modules'

# 统计代码行数
find . -name "*.py" -not -path "./venv/*" | xargs wc -l

# 查看磁盘使用
du -sh docs/
du -sh media/

# 清理缓存
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete
```

---

## 🧪 测试命令

```bash
# 运行测试
python manage.py test

# 运行特定测试
python manage.py test app.tests.TestArticle

# 测试静态生成
bash test_static_generation.sh
```

---

## 🔐 SSH 密钥管理

```bash
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 测试 GitHub 连接
ssh -T git@github.com

# 添加密钥到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

---

## 📝 快速工作流

### 发布新文章

```bash
# 1. 启动服务器
conda activate RunProject
python manage.py runserver

# 2. 在浏览器中访问后台并发布文章
# http://127.0.0.1:8000/admin/

# 3. 保存后自动生成静态站点

# 4. 提交并推送
git add docs/
git commit -m "Update: 新增文章《文章标题》"
git push origin main

# 5. 等待 1-2 分钟访问网站
# https://pangu-immortal.github.io
```

### 修改样式

```bash
# 1. 编辑模板或静态文件
# templates/ 或 static/

# 2. 重新生成
python manage.py generate_static_site

# 3. 提交推送
git add .
git commit -m "Update: 修改样式"
git push origin main
```

---

## 🆘 紧急命令

```bash
# 回退到上一次提交
git reset --hard HEAD~1

# 强制推送 (谨慎使用!)
git push -f origin main

# 放弃本地修改
git checkout -- .

# 查看远程仓库状态
git remote show origin

# 重新克隆 (全新开始)
cd ..
rm -rf RunProject
git clone <仓库地址>
```

---

## 📚 帮助文档

```bash
# Django 命令帮助
python manage.py help <command>

# Git 命令帮助
git help <command>

# 查看 Python 包版本
pip list | grep Django

# 查看项目依赖
pip freeze
```

---

## 🔗 快速链接

| 功能 | 地址 |
|------|------|
| 本地前台 | http://127.0.0.1:8000/ |
| 本地后台 | http://127.0.0.1:8000/admin/ |
| GitHub 仓库 | https://github.com/Pangu-Immortal/pangu-immortal.github.io |
| 线上博客 | https://pangu-immortal.github.io |
| GitHub Pages 设置 | https://github.com/Pangu-Immortal/pangu-immortal.github.io/settings/pages |
| SSH 密钥设置 | https://github.com/settings/keys |
| Token 生成 | https://github.com/settings/tokens |

---

**💡 提示**: 将本文件加入书签,随时查阅!
