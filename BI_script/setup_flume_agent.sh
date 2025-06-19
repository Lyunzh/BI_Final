#!/bin/bash

# === 配置项 ===
BASE_DIR="/usr/local/flume/data/log_stream"
FLUME_CONF_DIR="/usr/local/flume/conf/agents"
START_DATE="2019-06-13"
DAYS=22

# === 主循环 ===
for ((i = 0; i < DAYS; i++)); do
    # 生成日期、路径、agent名、topic
    date_str=$(date -d "$START_DATE +$i day" +"%Y-%m-%d")
    date_compact=$(date -d "$START_DATE +$i day" +"%Y%m%d")
    folder="$BASE_DIR/$date_str"
    agent_name="agent_$date_compact"
    conf_file="$FLUME_CONF_DIR/flume-$date_str.conf"
    topic="impression_$date_compact"

    # 创建 spool 目录
    mkdir -p "$folder"

    # 生成配置文件内容
    cat > "$conf_file" <<EOF
# Flume config for date $date_str
$agent_name.sources = spoolSrc
$agent_name.sinks = kafkaSink
$agent_name.channels = memChannel

# Source
$agent_name.sources.spoolSrc.type = spooldir
$agent_name.sources.spoolSrc.spoolDir = $folder
$agent_name.sources.spoolSrc.fileHeader = true

# Channel
$agent_name.channels.memChannel.type = memory
$agent_name.channels.memChannel.capacity = 10000
$agent_name.channels.memChannel.transactionCapacity = 1000

# Sink
$agent_name.sinks.kafkaSink.type = org.apache.flume.sink.kafka.KafkaSink
$agent_name.sinks.kafkaSink.topic = $topic
$agent_name.sinks.kafkaSink.brokerList = localhost:9092

# Bindings
$agent_name.sources.spoolSrc.channels = memChannel
$agent_name.sinks.kafkaSink.channel = memChannel
EOF

    echo "✅ Created Flume config: $conf_file"
done