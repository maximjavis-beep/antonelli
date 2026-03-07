# Antonelli 部署指南

## 由于 CLI 需要登录，请使用以下方法部署：

### 方法 1: Vercel Dashboard (推荐)

1. 访问 https://vercel.com/new
2. 选择 "Upload" 选项
3. 上传 `web/` 文件夹中的所有文件
4. 项目会自动部署

### 方法 2: GitHub 集成

1. 在 GitHub 创建新仓库
2. 推送代码：
```bash
cd ~/.openclaw/workspace/projects/antonelli
git init
git add web/
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/antonelli.git
git push -u origin main
```
3. 在 Vercel 导入 GitHub 仓库

### 方法 3: Vercel CLI (需要登录)

```bash
npx vercel login
npx vercel --prod
```

## 已准备好的文件

- `web/index.html` - 主页面 (67KB)
- `web/data.db` - 数据库 (150条资讯)
- `web/vercel.json` - Vercel 配置

## 自定义域名

部署完成后，在 Vercel Dashboard：
1. 进入项目 Settings → Domains
2. 添加 `rss.shaojiujidi.com`
3. DNS 已配置，会自动验证

## 网站预览

本地预览：
```bash
cd ~/.openclaw/workspace/projects/antonelli/web
python3 -m http.server 8080
# 访问 http://localhost:8080
```
