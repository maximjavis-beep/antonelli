# 🍷 Antonelli - 项目完成总结

## 项目概述

**Antonelli** 是一个全球酒类行业情报追踪系统，自动抓取 RSS 新闻并生成静态网站。

## 已完成功能

### ✅ 核心功能
- [x] RSS 自动抓取 (9个信源)
- [x] 数据库存储 (SQLite)
- [x] 静态网站生成
- [x] 四地区分类 (中国/欧洲/美洲/亚洲)
- [x] 新窗口打开链接
- [x] PureCut 品牌标识
- [x] PDF 自动备份

### ✅ 部署配置
- [x] Vercel 配置文件
- [x] GitHub Actions 自动部署
- [x] 定时自动更新 (每天 08:00)
- [x] 本地自动更新脚本

### ✅ 数据源
| 地区 | 信源 |
|------|------|
| 北美 | Wine Enthusiast, The Spirits Business, Brewbound |
| 欧洲 | Decanter, The Drinks Business, Wine-Searcher |
| 日本 | Nomunication, Sake World |
| 亚太 | The Shout |

## 文件结构

```
projects/antonelli/
├── web/                      # 网站目录 (部署用)
│   ├── index.html           # 主页面
│   ├── data.db              # 数据库
│   └── vercel.json          # Vercel 配置
├── .github/workflows/        # GitHub Actions
│   └── deploy.yml           # 自动部署配置
├── fetch_rss.py             # RSS 抓取
├── build_site.py            # 网站生成
├── auto-update.sh           # 本地自动更新
├── config.json              # 配置文件
├── requirements.txt         # Python 依赖
├── GITHUB-SETUP.md          # GitHub 设置指南
└── README.md                # 项目说明
```

## 部署步骤

### 1. 创建 GitHub 仓库
```bash
# 方法 A: GitHub CLI
gh auth login
gh repo create antonelli --public --source=. --push

# 方法 B: 手动
# 1. 访问 https://github.com/new 创建仓库
# 2. git remote add origin https://github.com/YOUR_USERNAME/antonelli.git
# 3. git push -u origin main
```

### 2. 部署到 Vercel
```bash
# 方法 A: Vercel CLI
npx vercel login
npx vercel --prod

# 方法 B: Vercel Dashboard
# 1. 访问 https://vercel.com/new
# 2. 导入 GitHub 仓库
# 3. 自动部署
```

### 3. 配置自定义域名
1. Vercel Dashboard → 项目 → Settings → Domains
2. 添加: `rss.shaojiujidi.com`
3. DNS 已配置，自动验证

### 4. 配置自动更新
在 GitHub 仓库 Settings → Secrets:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## 使用方法

### 手动更新
```bash
cd ~/.openclaw/workspace/projects/antonelli
./auto-update.sh
```

### 本地预览
```bash
cd ~/.openclaw/workspace/projects/antonelli/web
python3 -m http.server 8080
# 访问 http://localhost:8080
```

### 定时任务
```bash
# 每天 8 点自动更新
crontab -e
# 添加:
0 8 * * * cd ~/.openclaw/workspace/projects/antonelli && ./auto-update.sh
```

## 网站预览

- **统计面板**: 总资讯数、今日新增、覆盖地区、活跃信源
- **四栏布局**: 中国、欧洲、美洲、亚洲
- **深色主题**: 现代化 UI 设计
- **响应式**: 支持移动端

## 备份位置

PDF 备份自动保存到:
```
~/Antonelli/YYYYMMDD/Antonelli-YYYYMMDD-HHMM.pdf
```

## 访问地址

- **生产环境**: https://rss.shaojiujidi.com
- **Vercel 预览**: https://antonelli-xxx.vercel.app

## 技术栈

- **后端**: Python 3.11 + SQLite
- **前端**: HTML + CSS (water.css)
- **部署**: Vercel
- **CI/CD**: GitHub Actions
- **数据源**: RSS feeds

## 项目状态

✅ **已完成并准备好部署**

下一步:
1. 创建 GitHub 仓库
2. 部署到 Vercel
3. 配置自定义域名
4. 享受自动更新!

---

Powered by PureCut © 2026
