from http.server import BaseHTTPRequestHandler
import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data.db"

def get_articles(limit=50, region=None):
    """获取文章"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    if region:
        c.execute('''
            SELECT title, link, summary, published, source, region, keywords_matched, fetched_at
            FROM articles
            WHERE region = ?
            ORDER BY fetched_at DESC
            LIMIT ?
        ''', (region, limit))
    else:
        c.execute('''
            SELECT title, link, summary, published, source, region, keywords_matched, fetched_at
            FROM articles
            ORDER BY fetched_at DESC
            LIMIT ?
        ''', (limit,))
    
    articles = []
    for row in c.fetchall():
        articles.append({
            'title': row[0],
            'link': row[1],
            'summary': row[2],
            'published': row[3],
            'source': row[4],
            'region': row[5],
            'keywords': row[6],
            'fetched_at': row[7]
        })
    
    conn.close()
    return articles

def get_stats():
    """获取统计"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM articles')
    total = c.fetchone()[0]
    
    today = datetime.now().strftime('%Y-%m-%d')
    c.execute('SELECT COUNT(*) FROM articles WHERE date(fetched_at) = ?', (today,))
    today_count = c.fetchone()[0]
    
    c.execute('SELECT region, COUNT(*) FROM articles GROUP BY region')
    by_region = dict(c.fetchall())
    
    conn.close()
    
    return {
        'total': total,
        'today': today_count,
        'by_region': by_region
    }

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        path = self.path
        
        if path == '/api/stats':
            data = get_stats()
        elif path == '/api/articles':
            data = get_articles(50)
        elif path.startswith('/api/articles/'):
            region = path.split('/')[-1]
            data = get_articles(50, region)
        else:
            data = {'error': 'Not found'}
        
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # 这里可以添加更新触发逻辑
        data = {'message': 'Update triggered'}
        self.wfile.write(json.dumps(data).encode())
