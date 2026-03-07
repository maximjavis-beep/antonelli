# Antonelli 部署包

## 快速部署

### 方法 1: Vercel CLI (需要登录)

```bash
cd antonelli
npx vercel login
npx vercel --prod
```

### 方法 2: Vercel Dashboard (推荐)

1. 访问 https://vercel.com/new
2. 选择 "Upload" 选项
3. 上传整个 `antonelli` 文件夹
4. 部署完成后，在 Settings > Domains 添加 `rss.shaojiujidi.com`

### 方法 3: GitHub + Vercel 自动部署

1. 在 GitHub 创建仓库并推送代码
2. 在 Vercel 导入 GitHub 仓库
3. 配置环境变量:
   - `VERCEL_TOKEN`: 你的 Vercel Token

## 项目文件

- `web/index.html` - 主页面
- `web/data.db` - 数据库 (包含 150 条资讯)
- `api/index.py` - API 接口
- `vercel.json` - Vercel 配置

## 网站预览

网站已生成在 `web/index.html`，可以直接在浏览器打开预览。

## 更新数据

如需更新数据，运行:
```bash
python3 fetch_rss.py
python3 build_site.py
```

然后重新部署。
