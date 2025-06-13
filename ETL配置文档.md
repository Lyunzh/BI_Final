## Flume + Kafka 配置文档

- **MySQL**

  1. 创建数据库 bi_database，字符集 utf8mb4，排序规则 utf8mb4_unicode_ci
  2. 按照数据库设计文档建表

- **SpringBoot**

  1. IDEA 创建 SpringBoot3.5.0 项目（java17）
  2. 添加依赖项（pom.xml）
  3. application.properties 中数据库连接字符串修改一下
  4. application.properties 中 news.file.path 改成你自己的 news.tsv 的路径（需要去掉最后两列，我把处理好的也附在文件中了）

- **ZooKeeper**

  1. 下载 [zookeeper](https://archive.apache.org/dist/zookeeper/zookeeper-3.6.4/apache-zookeeper-3.6.4-bin.tar.gz) 并解压到 D:\apache-zookeeper-3.6.4-bin（自定义目录）

  2. 新建 D:\apache-zookeeper-3.6.4-bin\data 文件夹

  3. D:\apache-zookeeper-3.6.4-bin\conf 中 zoo_sample.cfg文件改名为 zoo.cfg，进行如下修改：

     ```shell
     dataDir=/tmp/zookeeper
     改为：dataDir=D:\\apache-zookeeper-3.6.4-bin\\data
     ```

  4. 新建系统变量 ZOOKEEPER_HOME（D:\apache-zookeeper-3.6.4-bin），环境变量 Path 中添加 %ZOOKEEPER_HOME%\bin

  5. 使用管理员权限启动 cmd，运行 `zkServer`

  6. 使用管理员权限启动另一个 cmd，运行 `zkCli`

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

  4. 启动 zookeeper 后，使用管理员权限启动 cmd，cd D:\kafka_2.12-3.5.1，运行以下命令启动服务：

     ```shell
     .\bin\windows\kafka-server-start.bat .\config\server.properties
     ```

  5. 使用管理员权限启动另一个 cmd，cd D:\kafka_2.12-3.5.1\bin\windows：

     > ***注意：kafka删除主题可能会有bug，尽量避免***
     
     ```shell
     创建主题：
     kafka-topics.bat --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 10 --topic impression_logs
     查询主题：
     kafka-topics.bat --bootstrap-server localhost:9092 --list
     ```
  
- **Flume**

  1. 下载 [flume](https://www.apache.org/dyn/closer.lua/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz) 并解压到 D:\apache-flume-1.11.0-bin（自定义目录）

  2. 新建系统变量 FLUME_HOME（D:\apache-flume-1.11.0-bin），环境变量 Path 中添加 %FLUME_HOME%\bin 和 %FLUME_HOME%\conf

  3. 复制 D:\apache-flume-1.9.0-bin\conf 目录中带有 `.template` 的三个文件，复制后去掉 `.template` 后缀

  5. 新建 D:\\apache-flume-1.11.0-bin\\data\\log_stream 文件夹

  6. 新建 D:\apache-flume-1.9.0-bin\conf\flume-impression.conf：

     ```
     # Agent Name
     agent1.sources  = spoolSrc
     agent1.channels = memChannel
     agent1.sinks    = kafkaSink
     
     # 1) Source: Monitor Dir
     agent1.sources.spoolSrc.type = spooldir
     agent1.sources.spoolSrc.spoolDir = D:\\apache-flume-1.11.0-bin\\data\\log_stream
     agent1.sources.spoolSrc.fileHeader = true
     agent1.sources.spoolSrc.recursiveDirectorySearch = false
     
     # 2) Channel: Memory
     agent1.channels.memChannel.type = memory
     agent1.channels.memChannel.capacity = 10000
     agent1.channels.memChannel.transactionCapacity = 1000
     
     # 3) Sink: Send to Kafka
     agent1.sinks.kafkaSink.type = org.apache.flume.sink.kafka.KafkaSink
     agent1.sinks.kafkaSink.topic = impression_logs
     agent1.sinks.kafkaSink.brokerList = localhost:9092
     agent1.sinks.kafkaSink.requiredAcks = 1
     agent1.sinks.kafkaSink.batchSize = 20
     
     # 4) bind Source, Channel, Sink
     agent1.sources.spoolSrc.channels = memChannel
     agent1.sinks.kafkaSink.channel = memChannel
     ```

  7. 把 impression_log_sorted.csv 复制到 D:\\apache-flume-1.11.0-bin\\data\\log_stream

  7. cd D:\apache-flume-1.11.0-bin：

     ```shell
     bin\flume-ng.cmd agent --conf conf --conf-file conf\flume-impression.conf --name agent1
     ```

  9. 在另一个终端 cd D:\kafka_2.12-3.5.1\bin\windows，即可看到消息

     ```shell
     kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic impression_logs --from-beginning
     ```

  9. 运行 SpringBoot 项目

  10. 在 Postman 或 apifox 或使用 curl 访问 http://localhost:8082/api/triggerDay?day=0&startDate=2019-06-13，这里 `day=0` 对应 `2019-06-13`；接口会从 Kafka earliest 开始拉取，只保存这一天（00:00:00–23:59:59）的记录。
      再下一天，需要把 day 改成 1、2、... 最大为 21，对应 `2019-07-04`
  
  11. 检查数据库，看是否有`2019-06-13` 等日期的曝光条目和那些新闻的元数据。



TODO：

- Kafka 中数据在存入数据库后要消费掉，下次不再重读
- 提高落库性能