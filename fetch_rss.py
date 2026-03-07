#!/usr/bin/env python3
"""
Antonelli - 全球酒类行业 RSS 抓取工具
"""

import json
import feedparser
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import sys

DB_PATH = Path(__file__).parent / "data.db"
CONFIG_PATH = Path(__file__).parent / "config.json"

def init_db():
    """初始化数据库"""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            link TEXT,
            summary TEXT,
            published TEXT,
            source TEXT,
            region TEXT,
            fetched_at TEXT,
            keywords_matched TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_keywords():
    """获取关键词列表"""
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    return config.get("keywords", [])

def check_keywords(text, keywords):
    """检查文本中是否包含关键词"""
    if not text:
        return []
    text_lower = text.lower()
    matched = []
    for kw in keywords:
        if kw.lower() in text_lower:
            matched.append(kw)
    return matched

def fetch_feed(name, url, region, keywords):
    """抓取单个 RSS 源"""
    articles = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # 最近20条
            title = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", ""))
            
            # 检查关键词
            content = f"{title} {summary}"
            matched = check_keywords(content, keywords)
            
            article = {
                "id": hashlib.md5(f"{title}{url}".encode()).hexdigest(),
                "title": title,
                "link": entry.get("link", ""),
                "summary": summary[:500],
                "published": entry.get("published", datetime.now().isoformat()),
                "source": name,
                "region": region,
                "fetched_at": datetime.now().isoformat(),
                "keywords_matched": ",".join(matched)
            }
            articles.append(article)
    except Exception as e:
        print(f"  ⚠️ {name}: {e}")
    return articles

def save_articles(articles):
    """保存文章到数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    added = 0
    for a in articles:
        try:
            c.execute('''
                INSERT OR IGNORE INTO articles 
                (id, title, link, summary, published, source, region, fetched_at, keywords_matched)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (a["id"], a["title"], a["link"], a["summary"], 
                  a["published"], a["source"], a["region"], a["fetched_at"], a["keywords_matched"]))
            if c.rowcount > 0:
                added += 1
        except Exception as e:
            print(f"  保存失败: {e}")
    conn.commit()
    conn.close()
    return added

def main():
    print(f"🍷 Antonelli RSS 抓取 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    
    init_db()
    
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    
    keywords = get_keywords()
    total_added = 0
    
    for region_key, region_data in config["regions"].items():
        region_name = region_data["name"]
        sources = region_data.get("sources", [])
        
        if not sources:
            continue
            
        print(f"\n📍 {region_name}")
        
        for source in sources:
            name = source["name"]
            url = source["url"]
            print(f"  → {name}")
            
            articles = fetch_feed(name, url, region_name, keywords)
            added = save_articles(articles)
            total_added += added
            print(f"     新增 {added} 条")
    
    print(f"\n✅ 完成! 共新增 {total_added} 条资讯")

if __name__ == "__main__":
    main()
