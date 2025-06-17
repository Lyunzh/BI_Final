#!/bin/bash

# === 配置项 ===
FLUME_HOME="/usr/local/flume"
FLUME_CONF_DIR="$FLUME_HOME/conf"
LOG_DIR="$FLUME_HOME/logs/agents"
AGENT_CONF_DIR="$FLUME_CONF_DIR/agents"
PID_DIR="$FLUME_HOME/pids"

# 创建目录（如不存在）
mkdir -p "$LOG_DIR"
mkdir -p "$PID_DIR"

# 遍历所有 flume-*.conf 文件
for conf_file in "$AGENT_CONF_DIR"/flume-*.conf; do
    # 提取日期部分
    base_name=$(basename "$conf_file")            # flume-2019-06-13.conf
    date_part=${base_name:6:10}                   # 2019-06-13
    date_nodash=${date_part//-/}                  # 20190613
    agent_name="agent_$date_nodash"

    # 日志路径
    out_log="$LOG_DIR/${agent_name}-out.log"
    err_log="$LOG_DIR/${agent_name}-err.log"

    # 启动 Flume agent（后台运行）
    nohup /usr/local/flume/bin/flume-ng agent \
        --conf "$FLUME_CONF_DIR" \
        --conf-file "$conf_file" \
        --name "$agent_name" \
        > "$out_log" 2> "$err_log" &

    echo $! > "$FLUME_HOME/pids/${agent_name}.pid"
    echo "✅ Started Flume agent '$agent_name' with config '$conf_file'"
done

# 暂停（等待用户回车）
read -p "所有 Flume agent 已启动。按 Enter 继续..."
