#!/usr/bin/env python3
"""
Antonelli - 生成静态网站 (新版)
支持：地区分组、新窗口打开、PDF备份
"""

import sqlite3
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data.db"
CONFIG_PATH = Path(__file__).parent / "config.json"
WEB_DIR = Path(__file__).parent / "web"
PDF_DIR = Path.home() / "Antonelli"  # PDF保存目录

def ensure_dirs():
    """确保目录存在"""
    WEB_DIR.mkdir(exist_ok=True)
    (WEB_DIR / "static").mkdir(exist_ok=True)

def extract_images_from_summary(summary):
    """从摘要中提取图片URL"""
    if not summary:
        return []
    # 匹配各种图片格式
    img_patterns = [
        r'<img[^>]+src=["\']([^"\']+)["\']',  # 标准img标签
        r'<img[^>]+src=([^\s>]+)',  # 无引号的src
    ]
    images = []
    for pattern in img_patterns:
        matches = re.findall(pattern, summary, re.IGNORECASE)
        images.extend(matches)
    # 去重并限制数量
    seen = set()
    unique = []
    for img in images[:3]:  # 最多3张
        if img not in seen:
            seen.add(img)
            unique.append(img)
    return unique

def process_images_for_html(images):
    """生成图片HTML，带懒加载和错误处理"""
    if not images:
        return ""
    html = '<div class="article-images">'
    for src in images:
        html += f'''<div class="img-container">
            <img src="{src}" alt="" class="content-img" loading="lazy" referrerpolicy="no-referrer"
                 onerror="this.style.display='none'; this.parentElement.classList.add('img-error');"
                 onload="this.parentElement.classList.add('img-loaded');">
            <div class="img-placeholder">📷</div>
        </div>'''
    html += '</div>'
    return html

def get_articles():
    """获取所有文章并按地区分组"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        SELECT title, link, summary, published, source, region, keywords_matched, fetched_at
        FROM articles
        ORDER BY fetched_at DESC
    ''')
    
    articles = c.fetchall()
    conn.close()
    
    # 按地区分组（不含中国）
    by_region = {
        '欧洲': [],
        '美洲': [],
        '亚洲': []
    }
    
    for article in articles:
        region = article[5]  # region 字段
        if region == '欧洲':
            by_region['欧洲'].append(article)
        elif region in ['北美', '南美']:
            by_region['美洲'].append(article)
        elif region in ['日本', '亚太其他', '中国']:
            by_region['亚洲'].append(article)
        else:
            # 其他归类到亚洲
            by_region['亚洲'].append(article)
    
    return by_region

def get_stats():
    """获取统计信息"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM articles')
    total = c.fetchone()[0]
    
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(*) FROM articles WHERE date(fetched_at) = ?', (today,))
    today_count = c.fetchone()[0]
    
    # 按四大地区统计
    c.execute('SELECT region, COUNT(*) FROM articles GROUP BY region')
    raw_regions = dict(c.fetchall())
    
    # 合并为三大地区（不含中国）
    by_region = {'欧洲': 0, '美洲': 0, '亚洲': 0}
    for region, count in raw_regions.items():
        if region == '欧洲':
            by_region['欧洲'] += count
        elif region in ['北美', '南美']:
            by_region['美洲'] += count
        else:
            # 中国、日本、亚太其他都归类到亚洲
            by_region['亚洲'] += count
    
    conn.close()
    return {
        'total': total,
        'today': today_count,
        'by_region': by_region
    }

def save_pdf_backup():
    """保存当前网页为PDF备份"""
    try:
        now = datetime.now()
        date_str = now.strftime('%Y%m%d')
        time_str = now.strftime('%H%M')
        
        # 创建日期文件夹
        date_folder = PDF_DIR / date_str
        date_folder.mkdir(parents=True, exist_ok=True)
        
        # PDF文件名: Antonelli-20260307-1400.pdf
        pdf_name = f"Antonelli-{date_str}-{time_str}.pdf"
        pdf_path = date_folder / pdf_name
        
        # 使用 Chrome headless 生成 PDF
        html_path = WEB_DIR / "index.html"
        
        cmd = [
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            '--headless',
            '--disable-gpu',
            '--print-to-pdf-no-header',
            f'--print-to-pdf={pdf_path}',
            f'file://{html_path}'
        ]
        
        subprocess.run(cmd, capture_output=True, timeout=30)
        
        if pdf_path.exists():
            print(f"✅ PDF备份已保存: {pdf_path}")
            return str(pdf_path)
    except Exception as e:
        print(f"⚠️ PDF备份失败: {e}")
    return None

def generate_html():
    """生成 HTML 页面"""
    articles_by_region = get_articles()
    stats = get_stats()
    now = datetime.now()
    
    # 地区颜色映射
    region_colors = {
        '中国': '#e74c3c',
        '欧洲': '#3498db',
        '美洲': '#2ecc71',
        '亚洲': '#f39c12'
    }
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Antonelli | 全球酒类行业情报</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css">
    <style>
        :root {{
            --background-body: #0d1117;
            --background: #161b22;
            --background-alt: #21262d;
            --text-main: #c9d1d9;
            --text-bright: #f0f6fc;
            --text-muted: #8b949e;
            --links: #58a6ff;
            --focus: #388bfd;
            --border: #30363d;
            --code: #f78166;
            --button-hover: #388bfd;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        .header {{
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 3em;
            margin: 0;
            background: linear-gradient(135deg, #f78166 0%, #ff6b6b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header p {{
            color: var(--text-muted);
            margin-top: 10px;
            font-size: 1.1em;
        }}
        .update-time {{
            text-align: center;
            color: var(--text-muted);
            margin-bottom: 30px;
            font-size: 0.9em;
        }}
        .update-time a {{
            color: var(--links);
            text-decoration: none;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 40px;
        }}
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        .stat-card {{
            background: var(--background);
            padding: 25px 20px;
            border-radius: 12px;
            text-align: center;
            border: 1px solid var(--border);
            transition: transform 0.2s, border-color 0.2s;
        }}
        .stat-card:hover {{
            transform: translateY(-2px);
            border-color: var(--links);
        }}
        .stat-card h3 {{
            margin: 0;
            font-size: 2.5em;
            color: #f78166;
        }}
        .stat-card p {{
            margin: 10px 0 0;
            color: var(--text-muted);
            font-size: 0.95em;
        }}
        
        /* 四栏布局 */
        .regions-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-top: 40px;
        }}
        @media (max-width: 1200px) {{
            .regions-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        @media (max-width: 768px) {{
            .regions-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .region-column {{
            background: var(--background);
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        .region-header {{
            padding: 20px;
            font-size: 1.3em;
            font-weight: bold;
            color: white;
            text-align: center;
        }}
        .region-header.中国 {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }}
        .region-header.欧洲 {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }}
        .region-header.美洲 {{ background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%); }}
        .region-header.亚洲 {{ background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); }}
        
        .region-content {{
            padding: 15px;
            max-height: 800px;
            overflow-y: auto;
        }}
        
        .article {{
            background: var(--background-alt);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 8px;
            border: 1px solid var(--border);
            transition: border-color 0.2s;
        }}
        .article:hover {{
            border-color: var(--links);
        }}
        .article h4 {{
            margin: 0 0 8px;
            font-size: 0.95em;
            line-height: 1.4;
        }}
        .article h4 a {{
            color: var(--text-bright);
            text-decoration: none;
        }}
        .article h4 a:hover {{
            color: var(--links);
        }}
        .article-meta {{
            color: var(--text-muted);
            font-size: 0.8em;
            margin-bottom: 8px;
        }}
        .article-summary {{
            color: var(--text-main);
            font-size: 0.85em;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        /* ===== 图片容器和自适应样式 ===== */
        .article-images {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }}
        
        .img-container {{
            position: relative;
            flex: 1 1 calc(50% - 4px);
            min-width: 120px;
            max-width: 100%;
            border-radius: 8px;
            overflow: hidden;
            background: var(--background);
            min-height: 100px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .img-container.img-loaded {{
            background: transparent;
            min-height: auto;
        }}
        
        .img-container.img-error {{
            background: var(--background-alt);
            min-height: 60px;
        }}
        
        .content-img {{
            width: 100%;
            height: auto;
            max-height: 200px;
            object-fit: cover;
            object-position: center;
            border-radius: 8px;
            display: block;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .img-container.img-loaded .content-img {{
            opacity: 1;
        }}
        
        .img-container.img-error .content-img {{
            display: none;
        }}
        
        .img-placeholder {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.5em;
            opacity: 0.4;
            transition: opacity 0.3s ease;
        }}
        
        .img-container.img-loaded .img-placeholder {{
            opacity: 0;
            pointer-events: none;
        }}
        
        .img-container.img-error .img-placeholder {{
            opacity: 0.2;
            font-size: 1.2em;
        }}
        
        @media (max-width: 768px) {{
            .img-container {{
                flex: 1 1 100%;
                min-height: 80px;
            }}
            .content-img {{
                max-height: 180px;
            }}
        }}
        
        @media (max-width: 480px) {{
            .content-img {{
                max-height: 150px;
            }}
            .img-container {{
                min-height: 60px;
            }}
        }}
        
        .keywords {{
            margin-top: 10px;
        }}
        .keyword {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            margin-right: 4px;
            margin-bottom: 4px;
            background: var(--background);
            color: var(--text-muted);
            border: 1px solid var(--border);
        }}
        .footer {{
            text-align: center;
            padding: 40px 0;
            border-top: 1px solid var(--border);
            margin-top: 60px;
            color: var(--text-muted);
        }}
        .footer a {{
            color: var(--links);
        }}
        
        /* 滚动条样式 */
        .region-content::-webkit-scrollbar {{
            width: 6px;
        }}
        .region-content::-webkit-scrollbar-track {{
            background: var(--background);
        }}
        .region-content::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 3px;
        }}
        .region-content::-webkit-scrollbar-thumb:hover {{
            background: var(--text-muted);
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🍷 Antonelli</h1>
        <p>全球酒类行业情报追踪系统 · Powered by PureCut</p>
    </div>
    
    <div class="update-time">
        最后更新: {now.strftime('%Y-%m-%d %H:%M')} | 
        <a href="https://purecut.com" target="_blank">PureCut</a>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <h3>{stats['total']}</h3>
            <p>总资讯数</p>
        </div>
        <div class="stat-card">
            <h3>{stats['today']}</h3>
            <p>今日新增</p>
        </div>
        <div class="stat-card">
            <h3>3</h3>
            <p>覆盖地区</p>
        </div>
        <div class="stat-card">
            <h3>9</h3>
            <p>活跃信源</p>
        </div>
    </div>
    
    <div class="regions-grid">
'''
    
    # 生成三大地区栏目（不含中国）
    for region_name in ['欧洲', '美洲', '亚洲']:
        articles = articles_by_region.get(region_name, [])
        count = len(articles)
        
        html += f'''
        <div class="region-column">
            <div class="region-header {region_name}">
                {region_name} ({count})
            </div>
            <div class="region-content">
'''
        
        # 显示该地区的文章 (最多显示20条)
        for article in articles[:20]:
            title, link, summary, published, source, region, keywords, fetched_at = article
            
            # 清理摘要 (保留图片用于提取)
            clean_summary = re.sub(r'<[^>]+>', '', summary)[:150] if summary else ''
            
            # 提取图片
            images = extract_images_from_summary(summary) if summary else []
            images_html = process_images_for_html(images)
            
            # 关键词
            keywords_html = ''
            if keywords:
                kw_list = [k.strip() for k in keywords.split(',') if k.strip()][:3]  # 最多3个
                keywords_html = '<div class="keywords">' + ''.join([f'<span class="keyword">{k}</span>' for k in kw_list]) + '</div>'
            
            html += f'''
                <div class="article">
                    <h4><a href="{link}" target="_blank" rel="noopener noreferrer">{title}</a></h4>
                    <div class="article-meta">📰 {source} · {fetched_at[:10]}</div>
                    {images_html}
                    <div class="article-summary">{clean_summary}...</div>
                    {keywords_html}
                </div>
'''
        
        if not articles:
            html += '<div style="text-align: center; padding: 40px 20px; color: var(--text-muted);">今日暂无新资讯，显示历史数据</div>'
        
        html += '''
            </div>
        </div>
'''
    
    html += f'''
    </div>
    
    <div class="footer">
        <p>Antonelli Intelligence System © 2026 · Powered by <a href="https://purecut.com" target="_blank">PureCut</a></p>
        <p style="font-size: 0.9em; margin-top: 10px;">
            数据来源: Wine Enthusiast, The Spirits Business, Decanter, The Drinks Business, Wine-Searcher, Nomunication, Sake World, The Shout
        </p>
    </div>
</body>
</html>
'''
    
    # 写入文件
    with open(WEB_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 网站已生成: {WEB_DIR}/index.html")
    return WEB_DIR / "index.html"

def main():
    ensure_dirs()
    
    # 先保存当前版本的PDF备份
    current_html = WEB_DIR / "index.html"
    if current_html.exists():
        print("📄 保存当前版本PDF备份...")
        save_pdf_backup()
    
    # 生成新网站
    generate_html()
    print("✅ 完成!")

if __name__ == "__main__":
    main()
