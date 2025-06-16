#!/bin/bash

CSV_PATH="./impression_log.csv"
BASE_DIR="/usr/local/flume/data/log_stream"
SCRIPT_PATH="./log_simulator.py"

# 调用 Python 脚本
python3 "$SCRIPT_PATH" --csv "$CSV_PATH" --base-dir "$BASE_DIR"

# 暂停脚本（按回车继续）
read -p "✅ 日志生成完毕。按 Enter 键继续..."
