# Antonelli - GitHub 部署命令
# 复制以下命令到终端执行

cd ~/.openclaw/workspace/projects/antonelli

# 配置 Git
git config user.name "Mason"
git config user.email "mason@example.com"

# 确保远程仓库正确
git remote remove origin 2>/dev/null
git remote add origin https://github.com/streitenjavis/antonelli.git

# 查看状态
echo "=== Git 状态 ==="
git status

echo ""
echo "=== 准备推送 ==="
echo "远程仓库: $(git remote get-url origin)"
echo ""
echo "执行推送命令:"
echo "git push -u origin main"
echo ""
echo "提示: 如果要求输入密码，请使用 GitHub Personal Access Token"
echo "创建 Token: https://github.com/settings/tokens"
