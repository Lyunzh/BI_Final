package org.assignment.bi_backend.Service;

import org.assignment.bi_backend.Entity.EventType;
import org.assignment.bi_backend.Entity.NewsMetadata;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;
import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;

import java.sql.Timestamp;
import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;

@Service
public class DailyKafkaConsumerService {
    private static final String TOPIC_PREFIX = "impression_";
    private static final DateTimeFormatter CSV_DATE_FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final int BATCH_SIZE = 2000;
    private static final String INSERT_SQL =
            "INSERT INTO news_behavior_wide(" +
                    "news_id, title, content, category, topic, title_length, content_length, news_create_time, user_id, event_type, event_time) " +
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?)";

    @Autowired
    private JdbcTemplate jdbc;

    @Autowired
    private NewsMetadataLoader loader;

    public void consumeForDate(LocalDate date) {
        String topic = TOPIC_PREFIX + date.toString().replace("-", "");
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "impression-wide-consumer");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, "5000");
        props.put(ConsumerConfig.FETCH_MIN_BYTES_CONFIG, "1048576");
        props.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, "200");

        // 使用 OpenCSV 解析器处理引号及字段分隔
        CSVParser parser = new CSVParserBuilder()
                .withSeparator(',')
                .withQuoteChar('"')
                .build();

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(topic));
            List<Object[]> batchArgs = new ArrayList<>(BATCH_SIZE);

            while (true) {
                ConsumerRecords<String, String> recs = consumer.poll(Duration.ofSeconds(1));
                if (recs.isEmpty()) break;

                for (ConsumerRecord<String, String> rec : recs) {
                    String[] f;
                    try {
                        f = parser.parseLine(rec.value());
                    } catch (Exception e) {
                        // 解析失败，跳过
                        continue;
                    }
                    if (f.length < 3 || "start_time".equalsIgnoreCase(f[2])) continue; // 跳过表头

                    String userId = f[0].trim();
                    String newsId = f[1].trim();
                    LocalDateTime eventTime = LocalDateTime.parse(f[2].trim(), CSV_DATE_FMT);

                    NewsMetadata md = loader.get(newsId);
                    if (md == null) continue;

                    Object[] params = new Object[] {
                            newsId,
                            md.getTitle(),
                            md.getContent(),
                            md.getCategory(),
                            md.getTopic(),
                            md.getTitleLength(),
                            md.getContentLength(),
                            Timestamp.valueOf(md.getNewsCreateTime() != null ? md.getNewsCreateTime() : eventTime),
                            userId,
                            EventType.valueOf("IMPRESSION").name(),
                            Timestamp.valueOf(eventTime)
                    };

                    batchArgs.add(params);
                    if (batchArgs.size() >= BATCH_SIZE) {
                        saveBatch(batchArgs);
                        batchArgs.clear();
                        consumer.commitAsync();
                    }
                }
            }

            if (!batchArgs.isEmpty()) {
                saveBatch(batchArgs);
                consumer.commitAsync();
            }
        }
    }

    private void saveBatch(List<Object[]> argsList) {
        jdbc.batchUpdate(INSERT_SQL, argsList);
    }
}