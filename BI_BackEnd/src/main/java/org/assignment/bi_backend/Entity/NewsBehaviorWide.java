package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "news_behavior_wide")
public class NewsBehaviorWide {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long eventId;

    @Column(name = "news_id", length = 255)
    private String newsId;

    @Column(nullable = false, length = 500)
    private String title;

    @Lob
    private String content;

    @Column(nullable = false, length = 20)
    private String category;

    @Column(nullable = false, length = 50)
    private String topic;

    @Column(name = "title_length", nullable = false)
    private Integer titleLength;

    @Column(name = "content_length", nullable = false)
    private Integer contentLength;

    @Column(name = "news_create_time", columnDefinition = "DATETIME(6)")
    private LocalDateTime newsCreateTime;

    @Column(name = "user_id", length = 255)
    private String userId;

    @Enumerated(EnumType.STRING)
    private EventType eventType;

    @Column(name = "event_time", columnDefinition = "DATETIME(6)")
    private LocalDateTime eventTime;

    // getters and setters
    public Long getEventId() {
        return eventId;
    }
    public void setEventId(Long eventId) {
        this.eventId = eventId;
    }

    public String getNewsId() { return newsId; }
    public void setNewsId(String newsId) { this.newsId = newsId; }

    public String getTitle() { return title; }
    public void setTitle(String title) { this.title = title; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }

    public String getTopic() { return topic; }
    public void setTopic(String topic) { this.topic = topic; }

    public Integer getTitleLength() { return titleLength; }
    public void setTitleLength(Integer titleLength) { this.titleLength = titleLength; }

    public Integer getContentLength() { return contentLength; }
    public void setContentLength(Integer contentLength) { this.contentLength = contentLength; }

    public LocalDateTime getNewsCreateTime() { return newsCreateTime; }
    public void setNewsCreateTime(LocalDateTime newsCreateTime) { this.newsCreateTime = newsCreateTime; }

    public String getUserId() {
        return userId;
    }
    public void setUserId(String userId) {
        this.userId = userId;
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
