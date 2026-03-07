#!/bin/bash
# Antonelli 自动更新脚本 - 用于 OpenClaw Cron
# 每天早上7点和晚上6点运行

cd /Users/streitenjavis/.openclaw/workspace/projects/antonelli

# 日志
LOG_FILE="/Users/streitenjavis/.openclaw/logs/antonelli_cron.log"
mkdir -p "$(dirname "$LOG_FILE")"

echo "========== Antonelli 更新开始: $(date) ==========" >> "$LOG_FILE"

# 1. 抓取 RSS 数据
echo "[$(date +%H:%M:%S)] 抓取 RSS 数据..." >> "$LOG_FILE"
python3 fetch_rss.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "[$(date +%H:%M:%S)] ✅ RSS 抓取成功" >> "$LOG_FILE"
else
    echo "[$(date +%H:%M:%S)] ❌ RSS 抓取失败" >> "$LOG_FILE"
fi

# 2. 生成报告
echo "[$(date +%H:%M:%S)] 生成报告..." >> "$LOG_FILE"
python3 generate_report.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "[$(date +%H:%M:%S)] ✅ 报告生成成功" >> "$LOG_FILE"
else
    echo "[$(date +%H:%M:%S)] ❌ 报告生成失败" >> "$LOG_FILE"
fi

# 3. 生成网站
echo "[$(date +%H:%M:%S)] 生成网站..." >> "$LOG_FILE"
python3 build_site.py >> "$LOG_FILE" 2>&1
if [ $? -eq 0 ]; then
    echo "[$(date +%H:%M:%S)] ✅ 网站生成成功" >> "$LOG_FILE"
else
    echo "[$(date +%H:%M:%S)] ❌ 网站生成失败" >> "$LOG_FILE"
fi

echo "========== Antonelli 更新完成: $(date) ==========" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
