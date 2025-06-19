#!/bin/bash

# === 配置项 ===
FLUME_HOME="/usr/local/flume"
PID_DIR="$FLUME_HOME/pids"

# 检查 PID 目录是否存在
if [ ! -d "$PID_DIR" ]; then
    echo "❌ PID 目录不存在：$PID_DIR"
    exit 1
fi

# 遍历所有 pid 文件
for pid_file in "$PID_DIR"/*.pid; do
    [ -e "$pid_file" ] || continue  # 如果没有文件则跳过

    agent_name=$(basename "$pid_file" .pid)
    pid=$(cat "$pid_file")

    if ps -p "$pid" > /dev/null 2>&1; then
        kill "$pid"
        echo "🛑 已停止 $agent_name (PID: $pid)"
    else
        echo "⚠️ 进程 $pid 不存在，可能已退出：$agent_name"
    fi

    rm -f "$pid_file"
done

echo "✅ 所有可用的 Flume agents 已尝试停止。"
