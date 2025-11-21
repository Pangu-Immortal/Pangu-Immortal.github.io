# ✅ GitHub Pages 部署检查清单

在部署到 GitHub Pages 前,请按顺序完成以下检查。

---

## 📋 部署前检查

### 1. 本地环境

- [ ] Conda 环境 `RunProject` 已创建
- [ ] 已安装所有依赖 (`pip install -r requirements.txt`)
- [ ] 数据库已迁移 (`python manage.py migrate`)
- [ ] 已创建超级用户
- [ ] 本地开发服务器可以正常运行

### 2. 文章内容

- [ ] 至少创建了 1 篇测试文章
- [ ] 文章标题已填写
- [ ] 文章内容已填写 (Markdown)
- [ ] 文章未设置为隐藏
- [ ] 如有封面图,已成功上传

### 3. 静态生成测试

- [ ] 执行 `python manage.py generate_static_site` 成功
- [ ] `docs/` 目录已创建
- [ ] `docs/index.html` 存在
- [ ] `docs/list.html` 存在
- [ ] `docs/article_*.html` 存在
- [ ] `docs/static/` 目录存在
- [ ] `docs/media/` 目录存在 (如有上传文件)

验证命令:
```bash
ls docs/
ls docs/article_*.html
ls docs/static/
```

---

## 🔧 Git 配置

### 4. Git 初始化

- [ ] 已执行 `git init`
- [ ] `.gitignore` 文件存在
- [ ] 已添加远程仓库 `origin`

验证命令:
```bash
git status
git remote -v
```

### 5. GitHub 认证

选择其中一种方式:

**方式 A: SSH 密钥** (推荐)
- [ ] 已生成 SSH 密钥
- [ ] 公钥已添加到 GitHub
- [ ] 远程地址设置为 SSH 格式 (`git@github.com:...`)
- [ ] 可以连接 GitHub (`ssh -T git@github.com`)

**方式 B: Personal Access Token**
- [ ] 已生成 PAT (带 `repo` 权限)
- [ ] 已保存 Token (只显示一次)
- [ ] 远程地址设置为 HTTPS 格式

---

## 🌐 GitHub 仓库配置

### 6. 仓库创建

- [ ] 仓库名称为 `<用户名>.github.io` 格式
- [ ] 仓库设置为 **Public** (公开)
- [ ] 没有勾选 "Add a README file"
- [ ] 仓库已成功创建

### 7. 首次推送

- [ ] 已执行 `git add .`
- [ ] 已执行 `git commit -m "Initial commit"`
- [ ] 已执行 `git branch -M main`
- [ ] 已执行 `git push -u origin main`
- [ ] 推送成功,无报错

---

## 📄 GitHub Pages 配置

### 8. Pages 设置

访问: `https://github.com/<用户名>/<仓库名>/settings/pages`

- [ ] Source: Deploy from a branch
- [ ] Branch: **main**
- [ ] Folder: **/docs** ⚠️ 必须选择 /docs
- [ ] 已点击 **Save** 按钮
- [ ] 页面顶部显示 "Your site is live at ..."

### 9. 部署验证

- [ ] 等待 1-2 分钟
- [ ] 访问 `https://<用户名>.github.io` 可以打开
- [ ] 首页显示正常
- [ ] 点击"动态"可以看到文章列表
- [ ] 点击文章可以查看详情
- [ ] 样式加载正常 (科技风深色主题)
- [ ] 图片显示正常 (如有)

---

## 🔄 后续更新流程

### 10. 发布新文章

每次发布新文章后:

- [ ] 在 Django 后台保存文章
- [ ] 检查 `docs/` 目录已更新
- [ ] 执行 `git add docs/`
- [ ] 执行 `git commit -m "Update: 新增文章《标题》"`
- [ ] 执行 `git push origin main`
- [ ] 等待 1-2 分钟
- [ ] 在线上查看新文章

---

## 🐛 故障排查

### 如果推送失败

- [ ] 检查网络连接
- [ ] 检查 SSH 密钥或 PAT 是否正确
- [ ] 执行 `git remote -v` 确认远程仓库地址
- [ ] 查看错误信息并搜索解决方案

### 如果 Pages 显示 404

- [ ] 确认仓库名是 `<用户名>.github.io`
- [ ] 确认仓库是 Public
- [ ] 确认 Pages 设置选择了 `/docs` 目录
- [ ] 确认 `docs/index.html` 存在
- [ ] 等待 5 分钟后重试
- [ ] 查看 Actions 标签页是否有部署失败

### 如果样式丢失

- [ ] 确认 `docs/static/` 存在
- [ ] 重新执行 `python manage.py generate_static_site`
- [ ] 提交并推送更新

---

## 📚 文档参考

- **完整文档**: [README.md](README.md)
- **快速部署**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **命令速查**: [COMMANDS.md](COMMANDS.md)
- **项目总结**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 🎉 完成标志

当以下所有条件满足时,部署成功:

✅ 可以访问 `https://<用户名>.github.io`
✅ 页面样式正常
✅ 可以查看文章列表
✅ 可以打开文章详情
✅ 图片正常显示 (如有)
✅ 标签筛选正常工作

---

**🎊 恭喜你完成部署!**

如有问题,请参考:
- [常见问题](README.md#常见问题)
- [故障排查](DEPLOYMENT.md#故障排查)
