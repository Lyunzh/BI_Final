## Flume + Kafka 配置文档

> 可以把 BI_script 复制到 ~ 目录下，cd BI_script 后运行相关脚本，权限不够就加个 sudo
>
> ```shell
> 先 cd 到 /mnt/ 中存放 BI_script 的目录，然后：
> sudo cp -r /mnt/e/BI_script ~/BI_script
> ** impression_log.csv要自己放进去
> 
> 如果运行时提示：sudo: unable to execute ./create_kafka_topics.sh: No such file or directory 这种，是CRLF问题，这样解决：
> ~/BI_script$ sudo apt install dos2unix
> ~/BI_script$ sudo dos2unix *.sh
> ```

- **Kafka**

  1. 下载 kafka

     ```shell
     ~$ wget https://downloads.apache.org/kafka/3.7.2/kafka_2.13-3.7.2.tgz
     ~$ tar xvf kafka_2.13-3.5.1.tgz
     ~$ sudo mv kafka_2.13-3.5.1 /usr/local/kafka
     ```

  2. 运行脚本启动 kafka 服务（用的 screen）

     ```shell
     ~/BI_script$ sudo chmod +x start_kafka_service.sh
     ~/BI_script$ sudo ./start_kafka_service.sh
     ```

  5. 运行脚本批量创建 topic**（只需运行一次）**

     > ***注意：kafka删除主题可能会有bug，尽量避免***
     
     ```shell
     ~/BI_script$ sudo chmod +x create_kafka_topics.sh
     ~/BI_script$ sudo ./create_kafka_topics.sh
     ```

- **Flume**

  1. 下载 flume

     ```shell
     ~$ wget https://downloads.apache.org/flume/1.11.0/apache-flume-1.11.0-bin.tar.gz
     ~$ tar -zxvf apache-flume-1.11.0-bin.tar.gz
     ~$ sudo mv apache-flume-1.11.0-bin /usr/local/flume
     ```

  2. 运行命令修改 flume 配置

     ```shell
     ~$ sudo nano /etc/profile
     在最后增加：
     FLUME_HOME=/usr/local/flume
     PATH=$FLUME_HOME/bin:$PATH
     export FLUME_HOME PATH
     保存并退出（Ctrl+O 回车 Ctrl+X），然后：
     ~$ source /etc/profile
     
     ~$ cd /usr/local/flume
     /usr/local/flume$ mkdir data
     /usr/local/flume$ mkdir data/log_stream
     
     /usr/local/flume$ cd conf
     /usr/local/flume/conf$ mkdir agents
     /usr/local/flume/conf$ sudo cp flume-env.sh.template flume-env.sh
     /usr/local/flume/conf$ sudo cp flume-conf.properties.template flume-conf.properties
     
     /usr/local/flume/conf$ sudo nano flume-env.sh 
     修改成你自己的jdk1.8路径：
     export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
     保存并退出（Ctrl+O 回车 Ctrl+X）
     ```

  3. 运行脚本批量配置 flume agent**（只需运行一次）**

     ```shell
     ~/BI_script$ sudo chmod +x setup_flume_agent.sh
     ~/BI_script$ sudo ./setup_flume_agent.sh
     ```

  4. 运行脚本流式读取 impression_log.csv 并发送到 log_stream 中：**（只需运行一次）**
     
     ```shell
     ~/BI_script$ sudo chmod +x start_log_simulator.sh
     ~/BI_script$ sudo ./start_log_simulator.sh
     ```
     
  5. 运行脚本批量开启 agent 向 kafka 中 sink（记得修改 param 中的参数）**（只需运行一次）**
  
     ```shell
     ~/BI_script$ sudo chmod +x start_flume_agents.sh
     ~/BI_script$ sudo ./start_flume_agents.sh
     
     如需停止，可以在确认log_stream中文件后缀变成.COMPLETED后，运行以下命令：
     ~/BI_script$ sudo chmod +x stop_flume_agents.sh
     ~/BI_script$ sudo ./stop_flume_agents.sh
     ```
  
  9. 运行 SpringBoot 项目
  
  10. 在 Postman 或 apifox 或使用 curl 访问 http://localhost:8082/api/triggerDay?day=0&startDate=2019-06-13，这里 `day=0` 对应 `2019-06-13`；接口会从 Kafka earliest 开始拉取，只保存这一天（00:00:00–23:59:59）的记录。
      再下一天，需要把 day 改成 1、2、... 最大为 21，对应 `2019-07-04`

  11. 检查数据库，看是否有`2019-06-13` 等日期的曝光条目和那些新闻的元数据。
  
- **MySQL**
  1. 创建数据库 bi_database，字符集 utf8mb4，排序规则 utf8mb4_unicode_ci
  2. 按照数据库设计文档建表
- **SpringBoot**
  1. IDEA 创建 SpringBoot3.5.0 项目（java17）
  2. 添加依赖项（pom.xml）
  3. application.properties 中数据库连接字符串修改一下
  4. application.properties 中 news.file.path 改成你自己的 news.tsv 的路径（已附在文件中）

---

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

