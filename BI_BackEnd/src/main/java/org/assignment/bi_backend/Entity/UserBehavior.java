package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "user_behavior")
public class UserBehavior {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long eventId;

    @Column(name = "user_id", nullable = false)
    private String userId;

    @Column(name = "news_id", nullable = false)
    private String newsId;

    @Enumerated(EnumType.STRING)
    @Column(name = "event_type", nullable = false)
    private EventType eventType;    // 枚举 IMPRESSION / CLICK

    @Column(name = "event_time", columnDefinition = "DATETIME(6)", nullable = false)
    private LocalDateTime eventTime;

    public UserBehavior() {}

    // Getters and Setters
    public Long getEventId() {
        return eventId;
    }
    public void setEventId(Long eventId) {
        this.eventId = eventId;
    }

    public String getUserId() {
        return userId;
    }
    public void setUserId(String userId) {
        this.userId = userId;
    }

    public String getNewsId() {
        return newsId;
    }
    public void setNewsId(String newsId) {
        this.newsId = newsId;
    }

    public EventType getEventType() {
        return eventType;
    }
    public void setEventType(EventType eventType) {
        this.eventType = eventType;
    }

    public LocalDateTime getEventTime() {
        return eventTime;
    }
    public void setEventTime(LocalDateTime eventTime) {
        this.eventTime = eventTime;
    }
}