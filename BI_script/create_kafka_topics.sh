#!/bin/bash

KAFKA_BIN="/usr/local/kafka/bin"  # 修改为你 Kafka 的 bin 路径
TOPIC_PREFIX="impression_"
START_DATE="2019-06-13"
DAYS=22
PARTITIONS=10
REPLICATION=1

for ((i = 0; i < DAYS; i++)); do
    date=$(date -d "$START_DATE +$i day" +"%Y%m%d")
    topic="${TOPIC_PREFIX}${date}"
    echo "Creating topic '$topic'..."
    "/usr/local/kafka/bin/kafka-topics.sh" \
        --create \
        --bootstrap-server localhost:9092 \
        --replication-factor $REPLICATION \
        --partitions $PARTITIONS \
        --topic "$topic"
done