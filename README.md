# 🍷 Antonelli - 全球酒类行业情报系统

## 项目简介

Antonelli 是一个专注于全球酒类行业的 RSS 情报追踪系统，覆盖北美、南美、欧洲、中国、日本和亚太地区的生产商、分销商和推广渠道动态。

## 在线访问

**🌐 网站**: https://rss.shaojiujidi.com

## 覆盖地区

| 地区 | 信源数量 | 主要类型 |
|------|---------|---------|
| 北美 | 3 | Wine Enthusiast, The Spirits Business, Brewbound |
| 欧洲 | 3 | Decanter, The Drinks Business, Wine-Searcher |
| 日本 | 2 | Nomunication, Sake World |
| 亚太其他 | 1 | The Shout |

## 追踪关键词

- 并购 (Acquisition / Merger / 并购)
- 新品发布 (Launch / New Product / 新品)
- 分销合作 (Distribution / Partnership / 分销 / 合作)
- 投资扩张 (Investment / Expansion / 投资 / 扩张)
- 市场趋势 (Market / Trend)

## 本地使用方法

### 1. 抓取 RSS 数据

```bash
cd projects/antonelli
python3 fetch_rss.py
```

### 2. 生成报告

```bash
python3 generate_report.py
```

报告将保存在 `reports/` 目录下。

### 3. 查看报告

```bash
cat reports/antonelli_latest.md
```

## 自动化设置

建议添加 cron 任务实现自动抓取：

```bash
# 每天早上 8 点抓取
0 8 * * * cd /Users/streitenjavis/.openclaw/workspace/projects/antonelli && python3 fetch_rss.py

# 每天早上 9 点生成报告
0 9 * * * cd /Users/streitenjavis/.openclaw/workspace/projects/antonelli && python3 generate_report.py
```

## 文件结构

```
projects/antonelli/
├── config.json          # 配置文件 (RSS 源、关键词)
├── fetch_rss.py         # RSS 抓取脚本
├── generate_report.py   # 报告生成脚本
├── build_site.py        # 网站生成脚本
├── data.db              # SQLite 数据库
├── reports/             # 报告输出目录
├── web/                 # 网站输出目录
│   ├── index.html
│   └── ...
├── api/                 # Vercel API 函数
│   └── index.py
├── requirements.txt     # Python 依赖
├── vercel.json          # Vercel 配置
└── README.md            # 本文件
```

## 部署到 Vercel

### 1. 安装 Vercel CLI

```bash
npm i -g vercel
```

### 2. 登录 Vercel

```bash
vercel login
```

### 3. 部署

```bash
cd projects/antonelli
vercel --prod
```

### 4. 配置环境变量 (可选)

在 Vercel Dashboard 中设置：
- `UPDATE_TOKEN`: 用于触发更新的安全令牌

## 数据来源

所有数据来自公开的 RSS 源，包括行业媒体、贸易出版物和新闻网站。

## 技术栈

- **后端**: Python + SQLite
- **前端**: 静态 HTML (由 Python 生成)
- **部署**: Vercel
- **数据源**: RSS feeds

---

*Antonelli Intelligence System - 专注于全球酒类行业情报*
