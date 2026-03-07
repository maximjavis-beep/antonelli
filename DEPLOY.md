# Antonelli Vercel 部署指南

## 项目结构

```
antonelli/
├── api/
│   └── index.py         # Vercel API 路由
├── web/
│   └── index.html       # 生成的静态网站
├── data.db              # SQLite 数据库
├── config.json          # 配置文件
├── fetch_rss.py         # RSS 抓取脚本
├── generate_report.py   # 报告生成脚本
├── build_site.py        # 网站生成脚本
├── requirements.txt     # Python 依赖
└── vercel.json          # Vercel 配置
```

## 部署步骤

### 1. 准备项目

确保所有文件已准备好：

```bash
cd projects/antonelli
python3 build_site.py  # 生成网站
```

### 2. 部署到 Vercel

#### 方式一: Vercel CLI (推荐)

```bash
# 登录 Vercel
npx vercel login

# 部署
npx vercel --prod
```

#### 方式二: Git 集成

1. 在 GitHub 创建仓库
2. 推送代码:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/antonelli.git
git push -u origin main
```
3. 在 Vercel Dashboard 导入项目

#### 方式三: Vercel Dashboard 手动上传

1. 压缩项目文件夹 (不包含 node_modules)
2. 访问 https://vercel.com/new
3. 选择 "Import Git Repository" 或拖拽上传

### 3. 配置自定义域名

1. 在 Vercel Dashboard 进入项目设置
2. 点击 "Domains"
3. 添加域名: `rss.shaojiujidi.com`
4. 按提示配置 DNS (已配置好)

### 4. 设置自动更新 (可选)

在 Vercel Dashboard 设置 Cron Job:
- 进入项目 Settings > Cron Jobs
- 添加: `0 8 * * *` (每天 8 点)
- 命令: `python3 fetch_rss.py && python3 build_site.py`

## 环境变量

在 Vercel Dashboard 设置:
- `UPDATE_TOKEN`: 用于触发更新的安全令牌

## API 端点

- `GET /api/stats` - 获取统计信息
- `GET /api/articles` - 获取最新文章
- `GET /api/articles/{region}` - 按地区获取文章

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 抓取数据
python3 fetch_rss.py

# 生成网站
python3 build_site.py

# 本地预览
python3 -m http.server 8080 --directory web
```

## 更新网站

```bash
# 重新抓取并生成
python3 fetch_rss.py
python3 build_site.py

# 重新部署
npx vercel --prod
```
