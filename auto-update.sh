#!/bin/bash
# Antonelli 自动更新脚本
# 可以添加到 cron 定时任务

set -e

echo "🍷 Antonelli 自动更新"
echo "======================"

# 切换到项目目录
cd "$(dirname "$0")"

# 获取当前时间
TIMESTAMP=$(date +'%Y-%m-%d %H:%M')
echo "📅 更新时间: $TIMESTAMP"

# 更新 RSS 数据
echo "📡 抓取 RSS 数据..."
python3 fetch_rss.py

# 生成网站
echo "🌐 生成网站..."
python3 build_site.py

# Git 提交
echo "💾 提交更改..."
git add web/ data.db reports/
git commit -m "Auto-update: $TIMESTAMP" || echo "无更改需要提交"

# 推送到 GitHub (如果配置了远程仓库)
if git remote get-url origin &>/dev/null; then
    echo "🚀 推送到 GitHub..."
    git push origin main
fi

echo "✅ 更新完成!"
echo ""
echo "下次更新时间: $(date -v+1d +'%Y-%m-%d 08:00' 2>/dev/null || echo '明天 08:00')"
