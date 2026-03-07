#!/usr/bin/env python3
"""
Antonelli - 生成每日情报报告
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

DB_PATH = Path(__file__).parent / "data.db"
CONFIG_PATH = Path(__file__).parent / "config.json"
OUTPUT_DIR = Path(__file__).parent / "reports"

def get_recent_articles(hours=24):
    """获取最近的文章"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    since = (datetime.now() - timedelta(hours=hours)).isoformat()
    
    c.execute('''
        SELECT title, link, summary, published, source, region, keywords_matched
        FROM articles
        WHERE fetched_at > ?
        ORDER BY fetched_at DESC
    ''', (since,))
    
    articles = c.fetchall()
    conn.close()
    return articles

def generate_markdown(articles):
    """生成 Markdown 报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    md = f"""# 🍷 Antonelli 酒类情报日报

**日期**: {today}  
**来源**: 全球 {len(set(a[5] for a in articles))} 个地区 · {len(set(a[4] for a in articles))} 个信源

---

## 📊 今日概览

- **新增资讯**: {len(articles)} 条
- **重点关键词**: 并购、新品发布、市场扩张、分销合作

---

"""
    
    # 按地区分组
    by_region = {}
    for a in articles:
        region = a[5]
        if region not in by_region:
            by_region[region] = []
        by_region[region].append(a)
    
    # 生成各地区内容
    for region, items in by_region.items():
        md += f"\n## 🌍 {region}\n\n"
        for title, link, summary, published, source, _, keywords in items[:10]:  # 每地区最多10条
            md += f"### [{title}]({link})\n\n"
            md += f"- **来源**: {source}\n"
            if keywords:
                md += f"- **关键词**: {keywords}\n"
            md += f"- **摘要**: {summary[:200]}...\n\n"
    
    if not articles:
        md += "\n*今日暂无新资讯*\n"
    
    md += f"""
---

*报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}*  
*Antonelli Intelligence System*
"""
    return md

def main():
    print(f"📄 Antonelli 报告生成 - {datetime.now().strftime('%Y-%m-%d')}")
    
    articles = get_recent_articles(hours=24)
    print(f"  获取到 {len(articles)} 条资讯")
    
    markdown = generate_markdown(articles)
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    report_path = OUTPUT_DIR / f"antonelli_report_{today}.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    print(f"  ✅ 报告已保存: {report_path}")
    
    # 同时保存最新版本
    latest_path = OUTPUT_DIR / "antonelli_latest.md"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    return report_path

if __name__ == "__main__":
    main()
