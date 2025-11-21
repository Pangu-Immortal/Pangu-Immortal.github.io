# 🚀 快速部署指南 - GitHub Pages

本文档是 README.md 的精简版,专注于 GitHub Pages 部署步骤。

---

## 前提条件

✅ 已完成本地开发环境搭建
✅ 已在 Django 后台创建了至少一篇文章
✅ 已测试 `python manage.py generate_static_site` 命令成功

---

## 一、创建 GitHub 仓库

### 1. 访问 GitHub 创建仓库

🔗 [https://github.com/new](https://github.com/new)

### 2. 填写仓库信息

| 选项 | 值 |
|------|-----|
| 仓库名称 | `Pangu-Immortal.github.io` ⚠️ 必须是这个格式 |
| 描述 | 盘古大仙洞府 - 个人博客 |
| 可见性 | **Public** (公开) |
| 初始化选项 | 全部不勾选 |

### 3. 点击 **Create repository**

---

## 二、本地配置 Git

### 1. 初始化仓库 (如果还没有)

```bash
cd /Users/qihao/PycharmProjects/RunProject
git init
```

### 2. 配置 Git 用户信息

```bash
git config user.name "Pangu-Immortal"
git config user.email "your_email@example.com"
```

### 3. 添加远程仓库

```bash
git remote add origin https://github.com/Pangu-Immortal/pangu-immortal.github.io.git
```

---

## 三、生成静态站点并推送

### 1. 生成静态站点

```bash
# 激活 conda 环境
conda activate RunProject

# 生成静态站点到 docs/ 目录
python manage.py generate_static_site
```

**检查生成结果**:
```bash
ls docs/
# 应该看到: index.html, list.html, article_*.html, static/, media/
```

### 2. 提交到 Git

```bash
# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: Blog project with static site"
```

### 3. 推送到 GitHub

```bash
# 首次推送
git branch -M main
git push -u origin main
```

**如果提示权限错误,请看下一节 "配置 GitHub 认证"**

---

## 四、配置 GitHub 认证 (重要)

### 方式一: SSH 密钥 (推荐)

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"
# 一路回车即可

# 2. 复制公钥
cat ~/.ssh/id_ed25519.pub
# 复制输出的内容 (以 ssh-ed25519 开头)

# 3. 添加到 GitHub
# 访问: https://github.com/settings/keys
# 点击 "New SSH key"
# Title: MacBook Pro (随意命名)
# Key: 粘贴刚才复制的公钥
# 点击 "Add SSH key"

# 4. 修改远程仓库地址为 SSH
git remote set-url origin git@github.com:Pangu-Immortal/pangu-immortal.github.io.git

# 5. 重新推送
git push -u origin main
```

### 方式二: Personal Access Token (PAT)

```bash
# 1. 生成 Token
# 访问: https://github.com/settings/tokens
# 点击 "Generate new token (classic)"
# Note: Blog deployment
# Expiration: No expiration (或选择时间)
# Scopes: 勾选 "repo"
# 点击 "Generate token"
# ⚠️ 复制 Token (只显示一次,务必保存)

# 2. 推送时使用 Token
git push -u origin main
# Username: Pangu-Immortal
# Password: 粘贴刚才的 Token (不是 GitHub 密码)
```

---

## 五、启用 GitHub Pages

### 1. 进入仓库设置

🔗 [https://github.com/Pangu-Immortal/pangu-immortal.github.io/settings/pages](https://github.com/Pangu-Immortal/pangu-immortal.github.io/settings/pages)

或者:
1. 进入仓库主页
2. 点击 **Settings**
3. 左侧菜单找到 **Pages**

### 2. 配置发布源

| 设置项 | 值 |
|--------|-----|
| Source | Deploy from a branch |
| Branch | **main** |
| Folder | **/docs** ⚠️ 必须选择 /docs |

### 3. 点击 **Save**

### 4. 等待部署完成

1-2 分钟后,页面顶部会显示:

```
✅ Your site is published at https://pangu-immortal.github.io/
```

### 5. 访问网站

🔗 [https://pangu-immortal.github.io](https://pangu-immortal.github.io)

---

## 六、日常更新流程

每次发布新文章后:

```bash
# 1. 在 Django 后台保存文章后,会自动生成静态站点到 docs/

# 2. 提交更新
git add docs/
git commit -m "Update: 新增文章《你的文章标题》"

# 3. 推送
git push origin main

# 4. 等待 1-2 分钟访问网站
```

---

## 七、故障排查

### 问题 1: 推送失败 (权限错误)

```
remote: Permission to Pangu-Immortal/pangu-immortal.github.io.git denied
```

**解决**: 检查是否配置了 SSH 密钥或 PAT (见第四节)

### 问题 2: GitHub Pages 显示 404

**检查清单**:
- [ ] 仓库名是否为 `Pangu-Immortal.github.io`?
- [ ] 仓库是否设置为 **Public**?
- [ ] Pages 设置是否选择了 `/docs` 目录?
- [ ] `docs/` 目录是否包含 `index.html`?
- [ ] 是否等待了 1-2 分钟?

```bash
# 验证 docs/ 目录
ls docs/index.html
# 如果不存在,重新生成
python manage.py generate_static_site
```

### 问题 3: 样式丢失

**原因**: 静态资源路径问题

**解决**:
```bash
# 检查静态资源
ls docs/static/
ls docs/media/

# 如果为空,重新生成
python manage.py generate_static_site
```

### 问题 4: 图片无法显示

**检查 media 目录**:
```bash
ls docs/media/covers/
ls docs/media/avatars/
```

如果为空,确认本地 `media/` 目录有文件,然后重新生成。

---

## 八、进阶配置 (可选)

### 自定义域名

如果你有自己的域名:

1. 在 `docs/` 目录创建 `CNAME` 文件:
   ```bash
   echo "yourdomain.com" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. 在域名 DNS 设置中添加 CNAME 记录:
   ```
   Type: CNAME
   Name: @ (或 www)
   Value: pangu-immortal.github.io
   ```

3. 回到 GitHub Pages 设置,输入自定义域名并保存

---

## 九、完整命令速查

```bash
# 生成静态站点
python manage.py generate_static_site

# Git 基本操作
git status                      # 查看状态
git add docs/                   # 添加 docs/ 目录
git commit -m "Update: xxx"     # 提交
git push origin main            # 推送

# 查看远程仓库
git remote -v

# 查看提交历史
git log --oneline

# 强制推送 (谨慎使用)
git push -f origin main
```

---

## 十、获取帮助

遇到问题?

1. 查看完整文档: [README.md](README.md)
2. 提交 Issue: [https://github.com/Pangu-Immortal/pangu-immortal.github.io/issues](https://github.com/Pangu-Immortal/pangu-immortal.github.io/issues)
3. 参考 GitHub Pages 官方文档: [https://docs.github.com/pages](https://docs.github.com/pages)

---

**祝你部署成功! 🎉**
