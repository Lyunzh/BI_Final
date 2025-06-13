package org.assignment.bi_backend.Controller;

import org.assignment.bi_backend.Entity.UserBehavior;
import org.assignment.bi_backend.Service.DailyKafkaConsumerService;
import org.assignment.bi_backend.Repository.UserBehaviorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.Duration;
import java.time.Instant;
import java.time.LocalDate;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class BehaviorController {
    @Autowired
    private DailyKafkaConsumerService kafkaService;

    @Autowired
    private UserBehaviorRepository behaviorRepo;

    @GetMapping("/api/triggerDay")
    public ResponseEntity<Map<String, Object>> triggerDay(
            @RequestParam int day,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate
    ) {
        // 记录开始时间
        Instant startInstant = Instant.now();
        LocalDate target = startDate.plusDays(day);

        // 执行消费与落库
        kafkaService.consumeForDate(target);
        List<UserBehavior> behaviors = behaviorRepo.findByEventTimeBetween(
                target.atStartOfDay(), target.plusDays(1).atStartOfDay()
        );

        // 记录结束时间，计算耗时
        Instant endInstant = Instant.now();
        long durationMs = Duration.between(startInstant, endInstant).toMillis();

        // 返回结果给前端
        Map<String, Object> result = new HashMap<>();
        result.put("status", "success");
        result.put("day", day);
        result.put("processedCount", behaviors.size());
        result.put("durationMs", durationMs);

        return ResponseEntity.ok(result);
    }
}
