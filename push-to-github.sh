#!/bin/bash
# 手动执行脚本 - 复制到终端运行

echo "🚀 Antonelli GitHub 上传脚本"
echo "=============================="

# 进入项目目录
cd ~/.openclaw/workspace/projects/antonelli

# 配置 Git
git config user.name "Mason"
git config user.email "mason@example.com"

# 检查远程仓库
if ! git remote get-url origin &>/dev/null; then
    echo "添加远程仓库..."
    git remote add origin https://github.com/streitenjavis/antonelli.git
fi

# 推送代码
echo "推送到 GitHub..."
git push -u origin main

echo ""
echo "✅ 如果提示输入用户名密码:"
echo "   用户名: 你的 GitHub 用户名"
echo "   密码: 你的 Personal Access Token"
echo ""
echo "创建 Token: https://github.com/settings/tokens"
