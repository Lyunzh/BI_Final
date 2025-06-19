package org.assignment.bi_backend.Service;

import org.apache.kafka.clients.consumer.*;
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
    private static final int BATCH_SIZE = 5000;
    private static final String INSERT_SQL_UB =
            "INSERT INTO user_behavior(user_id, news_id, event_time, duration) VALUES (?,?,?,?)";

    @Autowired
    private JdbcTemplate jdbc;

    public void consumeForDate(LocalDate date) {
        String topic = TOPIC_PREFIX + date.toString().replace("-", "");

        System.out.println("tpc:" + topic);

        Properties props = getProperties();

        // 使用 OpenCSV 解析器处理引号及字段分隔
        CSVParser parser = new CSVParserBuilder()
                .withSeparator(',')
                .withQuoteChar('"')
                .build();

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(topic));
            List<Object[]> batchArgs = new ArrayList<>(BATCH_SIZE);

            while (true) {
                ConsumerRecords<String, String> recs = consumer.poll(Duration.ofSeconds(10));
                System.out.println("Polled recs length: " + recs.count()); // debug
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
                    int duration = Integer.parseInt(f[3].trim());

                    Object[] params = new Object[] {
                            userId,
                            newsId,
                            Timestamp.valueOf(eventTime),
                            duration
                    };

                    System.out.println(Arrays.toString(params)); // debug

                    batchArgs.add(params);
                    if (batchArgs.size() >= BATCH_SIZE) {
                        // saveBatch(batchArgs);
                        batchArgs.clear();
                        // consumer.commitAsync(); // debug
                    }
                }
            }

            if (!batchArgs.isEmpty()) {
                System.out.println("while(true) exit."); // debug
                // saveBatch(batchArgs);
                // consumer.commitAsync(); // debug
            }
        }

        final String UPDATE_NM_TIME =
                "UPDATE news_metadata m " +
                        "JOIN ( " +
                        "    SELECT news_id, MIN(event_time) AS first_time " +
                        "    FROM user_behavior " +
                        "    GROUP BY news_id " +
                        ") ub ON m.news_id = ub.news_id " +
                        "SET m.create_time = ub.first_time " +
                        "WHERE m.create_time IS NULL";
        jdbc.update(UPDATE_NM_TIME);
    }

    private static Properties getProperties() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "172.22.105.28:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "impression-log-consumer-1");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        props.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, "1000");
        props.put(ConsumerConfig.MAX_PARTITION_FETCH_BYTES_CONFIG, "1048576");
        props.put(ConsumerConfig.FETCH_MAX_WAIT_MS_CONFIG, "30000");
        return props;
    }

    private void saveBatch(List<Object[]> argsList) {
        jdbc.batchUpdate(INSERT_SQL_UB, argsList);
    }
}