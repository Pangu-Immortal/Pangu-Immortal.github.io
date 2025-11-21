#!/bin/bash
# 盘古大仙洞府 - 一键部署脚本
# 用于快速初始化和部署博客到 GitHub Pages

set -e  # 遇到错误立即退出

echo "========================================="
echo "  盘古大仙洞府 - GitHub Pages 部署向导"
echo "========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 conda
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ 未找到 conda${NC}"
    echo "请先安装 Miniconda: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# 激活环境
echo -e "${YELLOW}→ 激活 RunProject 环境...${NC}"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate RunProject 2>/dev/null || {
    echo -e "${RED}❌ RunProject 环境不存在${NC}"
    echo "请先创建环境: conda create -n RunProject python=3.13 -y"
    exit 1
}

# 检查 Django
if ! python -c "import django" 2>/dev/null; then
    echo -e "${YELLOW}→ 安装依赖...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✓ 环境准备完成${NC}"
echo ""

# 检查 Git
if [ ! -d .git ]; then
    echo -e "${YELLOW}→ 初始化 Git 仓库...${NC}"
    git init
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
fi

# 检查远程仓库
if ! git remote | grep -q origin; then
    echo ""
    echo "请输入 GitHub 仓库地址 (格式: https://github.com/用户名/用户名.github.io.git):"
    read -r repo_url
    git remote add origin "$repo_url"
    echo -e "${GREEN}✓ 远程仓库已添加${NC}"
fi

# 生成静态站点
echo ""
echo -e "${YELLOW}→ 生成静态站点...${NC}"
python manage.py generate_static_site

if [ ! -d docs ]; then
    echo -e "${RED}❌ 静态站点生成失败${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 静态站点生成成功${NC}"
echo ""

# 显示生成结果
echo "生成的文件:"
ls -lh docs/ | head -8
echo ""

# Git 操作
echo -e "${YELLOW}→ 准备提交到 Git...${NC}"
git add .

# 检查是否有需要提交的内容
if git diff --cached --quiet; then
    echo -e "${YELLOW}⚠️  没有需要提交的更改${NC}"
else
    echo "请输入提交信息 (默认: Update blog site):"
    read -r commit_msg
    commit_msg=${commit_msg:-"Update blog site"}

    git commit -m "$commit_msg"
    echo -e "${GREEN}✓ 已提交到本地仓库${NC}"
    echo ""

    # 询问是否推送
    echo "是否推送到 GitHub? (y/n)"
    read -r push_confirm

    if [ "$push_confirm" = "y" ] || [ "$push_confirm" = "Y" ]; then
        echo -e "${YELLOW}→ 推送到 GitHub...${NC}"

        # 检查是否是首次推送
        if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} &>/dev/null; then
            git branch -M main
            git push -u origin main
        else
            git push
        fi

        echo -e "${GREEN}✓ 推送成功!${NC}"
        echo ""
        echo "========================================="
        echo -e "${GREEN}部署完成!${NC}"
        echo "========================================="
        echo ""
        echo "后续步骤:"
        echo "1. 访问仓库设置: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/settings/pages"
        echo "2. 在 Source 中选择: Branch: main, Folder: /docs"
        echo "3. 点击 Save"
        echo "4. 等待 1-2 分钟后访问你的博客"
        echo ""
    else
        echo -e "${YELLOW}已取消推送${NC}"
        echo "你可以稍后手动推送: git push origin main"
    fi
fi

echo ""
echo -e "${GREEN}🎉 完成!${NC}"
