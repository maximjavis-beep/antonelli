#!/bin/bash
# Antonelli 部署脚本

echo "🍷 Antonelli 部署到 Vercel"
echo "============================"

# 检查 vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI 未安装"
    echo "请运行: npm i -g vercel"
    exit 1
fi

# 确保数据存在
echo "📊 检查数据..."
if [ ! -f "data.db" ]; then
    echo "⚠️ 数据库不存在，先运行抓取..."
    python3 fetch_rss.py
fi

# 生成网站
echo "🌐 生成网站..."
python3 build_site.py

# 部署到 Vercel
echo "🚀 部署到 Vercel..."
vercel --prod

echo ""
echo "✅ 部署完成！"
echo "网站: https://rss.shaojiujidi.com"
