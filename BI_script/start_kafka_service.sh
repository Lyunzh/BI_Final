#!/bin/bash

# Kafka 安装目录
KAFKA_DIR=/usr/local/kafka

# 配置文件
ZOOKEEPER_CONFIG=$KAFKA_DIR/config/zookeeper.properties
KAFKA_CONFIG=$KAFKA_DIR/config/server.properties

# 启动 Zookeeper 的 screen 会话
screen -dmS zookeeper $KAFKA_DIR/bin/zookeeper-server-start.sh $ZOOKEEPER_CONFIG
echo "✅ Zookeeper 启动完毕，screen 会话名：zookeeper"

# 等待几秒以确保 Zookeeper 启动稳定
sleep 5

# 启动 Kafka 的 screen 会话
screen -dmS kafka $KAFKA_DIR/bin/kafka-server-start.sh $KAFKA_CONFIG
echo "✅ Kafka 启动完毕，screen 会话名：kafka"

# 提示
echo "✅ 所有服务已启动，使用以下命令查看运行情况："
echo "  screen -ls"
echo "  screen -r zookeeper  # 进入 Zookeeper 会话，Ctrl+C 关闭服务"
echo "  screen -r kafka      # 进入 Kafka 会话，Ctrl+C 关闭服务"
echo "✅ 通过以下命令杀死会话"
echo "  screen -S kafka -X quit"
echo "  screen -S zookeeper -X quit"
