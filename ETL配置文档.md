## Flume + Kafka 配置文档

- **MySQL**

  1. 创建数据库 bi_database，字符集 utf8mb4，排序规则 utf8mb4_unicode_ci
  2. 按照数据库设计文档建表

- **SpringBoot**

  1. IDEA 创建 SpringBoot3.5.0 项目（java17）
  2. 添加依赖项（pom.xml）
  3. application.properties 中数据库连接字符串修改一下
  4. application.properties 中 news.file.path 改成你自己的 news.tsv 的路径（已附在文件中）

- **ZooKeeper**

  1. 下载 [zookeeper](https://archive.apache.org/dist/zookeeper/zookeeper-3.6.4/apache-zookeeper-3.6.4-bin.tar.gz) 并解压到 D:\apache-zookeeper-3.6.4-bin（自定义目录）

  2. 新建 D:\apache-zookeeper-3.6.4-bin\data 文件夹

  3. D:\apache-zookeeper-3.6.4-bin\conf 中 zoo_sample.cfg文件改名为 zoo.cfg，进行如下修改：

     ```shell
     dataDir=/tmp/zookeeper
     改为：dataDir=D:\\apache-zookeeper-3.6.4-bin\\data
     ```

  4. 新建系统变量 ZOOKEEPER_HOME（D:\apache-zookeeper-3.6.4-bin），环境变量 Path 中添加 %ZOOKEEPER_HOME%\bin

  5. 运行 zkServer_start.ps1 和 zkCli_start.ps1

- **Kafka**

  1. 下载 [kafka](https://pan.baidu.com/s/1Av4ZwQPUaAntwVxz79Ne9w?pwd=yyds) 并解压到 D:\kafka_2.12-3.5.1（自定义目录）

  2. 新建 D:\kafka_2.12-3.5.1\logs 文件夹

  3. 修改 D:\kafka_2.12-3.5.1\config\server.properties

     ```shell
     log.dirs=/tmp/kafka-logs
     改为：log.dirs=D:\\kafka_2.12-3.5.1\\logs
     
     #listeners=PLAINTEXT://localhost:9092
     改为：listeners=PLAINTEXT://localhost:9092
     ```

  4. **！！启动 zookeeper 后，运行 kafka_server_start.ps1，记得修改路径**

  5. 运行 create_kafka_topics.ps1 脚本批量创建 topic（记得修改 param 中的参数）
  
     > ***注意：kafka删除主题可能会有bug，尽量避免***
     
     ```shell
     .\create_kafka_topics.ps1
     
     如需查询主题：
     kafka-topics.bat --bootstrap-server localhost:9092 --list
     ```
  
- **Flume**

  1. 下载 [flume](https://www.apache.org/dyn/closer.lua/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz) 并解压到 D:\apache-flume-1.11.0-bin（自定义目录）

  2. 新建系统变量 FLUME_HOME（D:\apache-flume-1.11.0-bin），环境变量 Path 中添加 %FLUME_HOME%\bin 和 %FLUME_HOME%\conf

  3. 复制 D:\apache-flume-1.9.0-bin\conf 目录中带有 `.template` 的三个文件，复制后去掉 `.template` 后缀，**新建agents文件夹，准备存放配置文件**

  5. 新建 D:\\apache-flume-1.11.0-bin\\data\\log_stream 文件夹

  6. 运行 setup_log_simulator.ps1 脚本（记得修改 param 中的参数）创建文件夹

     ```powershell
     .\setup_log_simulator.ps1
     ```
     
  6. 运行 log_simulator_start.ps1 流式读取 impression_log.csv 并发送到 log_stream 中：
  
     ```powershell
     .\log_simulator_start.ps1
     ```
  
  7. 运行 flume_agent_start.ps1 脚本批量开启 agent（记得修改 param 中的参数）
  
     ```shell
     .\flume_agent_start.ps1
     ```
  
  9. 运行 SpringBoot 项目
  
  10. 在 Postman 或 apifox 或使用 curl 访问 http://localhost:8082/api/triggerDay?day=0&startDate=2019-06-13，这里 `day=0` 对应 `2019-06-13`；接口会从 Kafka earliest 开始拉取，只保存这一天（00:00:00–23:59:59）的记录。
      再下一天，需要把 day 改成 1、2、... 最大为 21，对应 `2019-07-04`
  
  11. 检查数据库，看是否有`2019-06-13` 等日期的曝光条目和那些新闻的元数据。



TODO：

- √ Kafka 中数据在存入数据库后要消费掉，下次不再重读

- 提高落库性能 ↓ 

- 首先，我在flume里面建立22个文件夹，分别代表06-13到07-04的log_stream，对应建立22个agent，向kafka中对应的topic进行sink；其次，要有一个程序，流式地读取整个impression_log.csv文件，根据每条记录的日期，送到相应的log_stream里面；

- 然后，在写入数据库时，根据已有的逻辑，点击NextDay后，去找当天的kafka topic，然后把user_behavior和news_metadata存入数据库。此外，为了提高性能，我们把user_behavior和news_metadata这两个表进行了pre_aggregation，当前的表为：

  ```sql
  CREATE TABLE news_behavior_wide (
    -- 事件标识
    event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    
    -- 新闻元数据
    news_id VARCHAR(255) NOT NULL,
    title VARCHAR(500) NOT NULL,
    content LONGTEXT,
    category VARCHAR(20) NOT NULL,
    topic VARCHAR(50) NOT NULL,
    title_length SMALLINT UNSIGNED NOT NULL,
    content_length MEDIUMINT UNSIGNED NOT NULL,
    news_create_time DATETIME(6) NOT NULL,
    
    -- 用户行为数据
    user_id VARCHAR(255) NOT NULL,
    event_type ENUM('IMPRESSION','CLICK') NOT NULL,
    event_time DATETIME(6) NOT NULL,
    
    -- 主键和索引
    PRIMARY KEY (event_id, event_time), -- 复合主键用于分区
    INDEX idx_news_time (news_id, event_time),
    INDEX idx_user_time (user_id, event_time),
    INDEX idx_category_time (category, event_time),
    INDEX idx_event_type (event_type),
    INDEX idx_news_create (news_create_time),
    INDEX idx_title_length (title_length)
  ) ENGINE=InnoDB
  PARTITION BY RANGE (TO_DAYS(event_time)) (
    PARTITION p202306 VALUES LESS THAN (TO_DAYS('2023-07-01')),
    PARTITION p202307 VALUES LESS THAN (TO_DAYS('2023-08-01'))
  );
  ```

  因此，对应的代码要进行修改。

