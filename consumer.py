from kafka import KafkaConsumer
import pymysql
from datetime import datetime

import logging
import time
# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def ingest_impression(date_str: str,
                      kafka_bootstrap_servers: str = 'localhost:9092',
                      mysql_config: dict = None,
                      batch_size: int = 10000):
    """
    从 Kafka 读取指定日期的 impression 主题数据，批量写入 MySQL user_behavior，
    并更新 news_metadata 中每条新闻的最早出现时间(create_time)。

    :param date_str: 'YYYY-MM-DD'，如 '2019-06-13'
    :param kafka_bootstrap_servers: Kafka 集群地址
    :param mysql_config: MySQL 连接配置，示例：
        {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'your_user',
            'password': 'your_pw',
            'db': 'your_db',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.Cursor
        }
    :param batch_size: 批量插入时每次提交的记录数
    """
    if mysql_config is None:
        raise ValueError("必须提供 mysql_config")

    start_time = time.time()
    logger.info(f"开始处理日期 {date_str} 的数据导入")
    logger.info(f"Kafka 服务器: {kafka_bootstrap_servers}")
    logger.info(f"MySQL 配置: { {k:v for k,v in mysql_config.items() if k != 'password'} }")

    # 1. 主题名
    topic = f"impression_{date_str.replace('-', '')}"
    logger.info(f"订阅 Kafka 主题: {topic}")

    # 2. 初始化 KafkaConsumer
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_bootstrap_servers,
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            consumer_timeout_ms=5000,
        )
        logger.info("Kafka 消费者初始化成功")
    except Exception as e:
        logger.error(f"初始化 Kafka 消费者失败: {str(e)}")
        raise

    # 3. 连接 MySQL
    try:
        conn = pymysql.connect(**mysql_config)
        cursor = conn.cursor()
        logger.info("MySQL 连接成功")
        
        # 测试查询确保表存在
        cursor.execute("SELECT 1 FROM user_behavior LIMIT 1")
        cursor.execute("SELECT 1 FROM news_metadata LIMIT 1")
        logger.info("MySQL 表验证通过")
    except Exception as e:
        logger.error(f"MySQL 连接或表验证失败: {str(e)}")
        raise

    # 4. 批量插入 SQL
    insert_sql = """
        INSERT INTO user_behavior_0613_0614
            (user_id, news_id, event_time, duration)
        VALUES (%s, %s, %s, %s)
    """

    # 用于追踪每个 news_id 的最早时间
    news_min_times = {}
    total_records = 0
    batch_count = 0

    batch = []
    try:
        logger.info("开始从 Kafka 消费数据...")
        for msg in consumer:
            # msg.value 示例: b'U125771,N92627,2019-06-13 05:18:48,82'
            line = msg.value.decode('utf-8').strip()
            if not line:
                continue

            user_id, news_id, ts_str, dur_str = line.split(',', 3)
            ts_str = ts_str.replace('"', '')
            if not ts_str[0].isdigit():
                logger.warning(f"忽略非时间数据: {ts_str}")
                continue
            event_time = datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S')
            duration = int(dur_str)

            # 添加到 batch
            batch.append((user_id, news_id, event_time, duration))

            # 更新最早时间
            if news_id not in news_min_times or event_time < news_min_times[news_id]:
                news_min_times[news_id] = event_time

            # 若达到批量阈值，写入一次
            if len(batch) >= batch_size:
                cursor.executemany(insert_sql, batch)
                conn.commit()
                batch_count += 1
                logger.info(f"已提交第 {batch_count} 批次，共 {len(batch)} 条记录")
                batch.clear()

        # 写入最后不足 batch_size 的部分
        if batch:
            cursor.executemany(insert_sql, batch)
            conn.commit()
            batch_count += 1
            logger.info(f"提交最后批次 (第 {batch_count} 批)，共 {len(batch)} 条记录")
            batch.clear()

        logger.info(f"共处理 {total_records} 条记录，发现 {len(news_min_times)} 个不同的新闻ID")

        # 5. 更新 news_metadata 表
        update_sql = """
            UPDATE news_metadata
            SET create_time = %s
            WHERE news_id = %s
              AND (create_time IS NULL OR create_time > %s)
        """
        updates = []
        update_count = 0
        update_batch_count = 0
        logger.info("开始更新 news_metadata 表...")

        for news_id, min_time in news_min_times.items():
            updates.append((min_time, news_id, min_time))
            update_count += 1

            # 分批提交更新
            if len(updates) >= batch_size:
                cursor.executemany(update_sql, updates)
                conn.commit()
                update_batch_count += 1
                logger.info(f"已提交第 {update_batch_count} 批更新，共 {len(updates)} 条更新")
                updates.clear()

        if updates:
            cursor.executemany(update_sql, updates)
            conn.commit()
            update_batch_count += 1
            logger.info(f"提交最后更新批次 (第 {update_batch_count} 批)，共 {len(updates)} 条更新")
            updates.clear()

    finally:
        cursor.close()
        conn.close()
        consumer.close()

        elapsed_time = time.time() - start_time
        logger.info(f"处理完成! 总耗时: {elapsed_time:.2f} 秒")
        logger.info(f"平均处理速度: {total_records/max(1, elapsed_time):.2f} 条/秒")


if __name__ == '__main__':
    ingest_impression(
        date_str='2019-06-14',
        kafka_bootstrap_servers='localhost:9092',
        mysql_config={
            'host': '172.22.96.1',
            'port': 3306,
            'user': 'root',
            'password': 'HCYmysql.1024',
            'db': 'bi_database',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.Cursor
        },
        batch_size=10000
    )
