package org.assignment.bi_backend.Service;

import org.assignment.bi_backend.Entity.EventType;
import org.assignment.bi_backend.Entity.NewsMetadata;
import org.assignment.bi_backend.Entity.UserBehavior;
import org.assignment.bi_backend.Repository.UserBehaviorRepository;
import org.assignment.bi_backend.Repository.NewsMetadataRepository;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.TopicPartition;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class DailyKafkaConsumerService {
    @Autowired
    private UserBehaviorRepository behaviorRepo;

    @Autowired
    private NewsMetadataRepository metadataRepo;

    @Autowired
    private NewsMetadataLoader loader;

    private static final String TOPIC = "impression_logs";
    private static final DateTimeFormatter DT_FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public void consumeForDate(LocalDate date) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "impression-trigger-consumer");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer");
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        List<TopicPartition> parts;
        try (KafkaConsumer<String,String> consumer = new KafkaConsumer<>(props)) {
            parts = consumer.partitionsFor(TOPIC)
                            .stream()
                            .map(p -> new TopicPartition(TOPIC, p.partition()))
                            .collect(Collectors.toList());
            consumer.assign(parts);
            consumer.seekToBeginning(parts);

            LocalDateTime start = date.atStartOfDay();
            LocalDateTime end = start.plusDays(1);

            // Preload existing metadata IDs to avoid N+1 queries
            Set<String> allIds = new HashSet<>();
            List<ConsumerRecord<String, String>> allRecs = new ArrayList<>();
            ConsumerRecords<String, String> recs;
            do {
                recs = consumer.poll(Duration.ofSeconds(1));
                for (ConsumerRecord<String, String> rec : recs) {
                    String[] f = rec.value().split(",");
                    if ("user_id".equalsIgnoreCase(f[0])) {
                        continue;
                    }
                    LocalDateTime ts = LocalDateTime.parse(f[2], DT_FMT);
                    if (!ts.isBefore(start) && !ts.isAfter(end)) {
                        allRecs.add(rec);
                        allIds.add(f[1]);
                    }
                }
            } while (!recs.isEmpty());

            // Batch load existing metadata
            Set<String> existingMeta = metadataRepo.findAllById(allIds)
                    .stream().map(NewsMetadata::getNewsId).collect(Collectors.toSet());

            // Prepare batches
            List<UserBehavior> behaviorBatch = new ArrayList<>();
            List<NewsMetadata> metaBatch = new ArrayList<>();

            for (ConsumerRecord<String, String> rec : allRecs) {
                String[] f = rec.value().split(",");
                if ("user_id".equalsIgnoreCase(f[0])) {
                    continue;
                }
                LocalDateTime ts = LocalDateTime.parse(f[2], DT_FMT);
                String userId = f[0], newsId = f[1];

                // Behavior dedupe and batch
                UserBehavior ub = new UserBehavior();
                ub.setUserId(userId);
                ub.setNewsId(newsId);
                ub.setEventType(EventType.IMPRESSION);
                ub.setEventTime(ts);
                behaviorBatch.add(ub);

                // Metadata batch
                if (!existingMeta.contains(newsId)) {
                    NewsMetadata m = loader.get(newsId);
                    if (m != null) {
                        m.setCreateTime(ts);
                        metaBatch.add(m);
                        existingMeta.add(newsId);
                    }
                }
            }

            // Save in batches
            if (!metaBatch.isEmpty()) {
                metadataRepo.saveAll(metaBatch);
            }
            if (!behaviorBatch.isEmpty()) {
                behaviorRepo.saveAll(behaviorBatch);
            }

        }
    }
}