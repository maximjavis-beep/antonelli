# GitHub + Vercel 自动部署指南

## 1. 创建 GitHub 仓库

### 方法 A: 使用 GitHub CLI (已安装)
```bash
# 登录 GitHub
gh auth login

# 创建仓库
gh repo create antonelli --public --source=. --push
```

### 方法 B: 手动创建
1. 访问 https://github.com/new
2. 仓库名: `antonelli`
3. 选择 Public
4. 不要初始化 (不要勾选 README)
5. 创建后运行：
```bash
git remote add origin https://github.com/YOUR_USERNAME/antonelli.git
git branch -M main
git push -u origin main
```

## 2. 连接 Vercel

### 在 Vercel Dashboard:
1. 访问 https://vercel.com/new
2. 选择 "Import Git Repository"
3. 选择你的 `antonelli` 仓库
4. 部署

### 配置环境变量:
在 Vercel 项目 Settings → Environment Variables:
```
VERCEL_TOKEN = your_vercel_token
VERCEL_ORG_ID = your_org_id
VERCEL_PROJECT_ID = your_project_id
```

获取方式:
```bash
npx vercel login
npx vercel env pull
```

## 3. 配置 GitHub Secrets

在 GitHub 仓库 Settings → Secrets and variables → Actions:

添加以下 Secrets:
- `VERCEL_TOKEN` - Vercel Token
- `VERCEL_ORG_ID` - Vercel Organization ID
- `VERCEL_PROJECT_ID` - Vercel Project ID

## 4. 自动更新配置

### GitHub Actions (已配置)
每天自动更新 (UTC 00:00 = 北京时间 08:00)

手动触发:
- 访问 GitHub 仓库 → Actions → Update Data and Deploy
- 点击 "Run workflow"

### 本地定时任务 (可选)
```bash
# 编辑 crontab
crontab -e

# 添加每天 8 点自动更新
0 8 * * * cd /Users/streitenjavis/.openclaw/workspace/projects/antonelli && ./auto-update.sh >> /tmp/antonelli-update.log 2>&1
```

## 5. 目录结构

```
antonelli/
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions 配置
├── web/                     # 网站文件 (部署到 Vercel)
│   ├── index.html
│   ├── data.db
│   └── vercel.json
├── fetch_rss.py            # RSS 抓取
├── build_site.py           # 网站生成
├── auto-update.sh          # 本地自动更新脚本
└── README.md
```

## 6. 更新流程

### 自动更新 (推荐)
1. GitHub Actions 每天自动运行
2. 抓取 RSS → 生成网站 → 提交代码 → 部署到 Vercel

### 手动更新
```bash
cd ~/.openclaw/workspace/projects/antonelli
./auto-update.sh
```

### 仅部署 (不更新数据)
在 GitHub Actions 页面选择 "Run workflow"，勾选 "仅部署"

## 7. 自定义域名

Vercel 部署后:
1. 进入 Vercel Dashboard → 项目 → Settings → Domains
2. 添加: `rss.shaojiujidi.com`
3. DNS 已配置，自动验证

## 8. 监控

- **GitHub Actions 日志**: 仓库 → Actions
- **Vercel 部署日志**: Vercel Dashboard → 项目 → Deployments
- **网站访问**: https://rss.shaojiujidi.com

## 9. 备份

PDF 备份自动保存在:
```
~/Antonelli/YYYYMMDD/Antonelli-YYYYMMDD-HHMM.pdf
```

## 快速开始

```bash
# 1. 进入项目目录
cd ~/.openclaw/workspace/projects/antonelli

# 2. 创建 GitHub 仓库
gh repo create antonelli --public --source=. --push

# 3. 在 Vercel 导入仓库并部署
# 访问 https://vercel.com/new

# 4. 配置 Secrets 后，自动更新即生效
```
