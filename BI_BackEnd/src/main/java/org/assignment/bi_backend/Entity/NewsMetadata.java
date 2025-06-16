package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class NewsMetadata {
    @Id
    private String newsId;

    private String title;

    @Lob
    private String content;

    private String category;

    private String topic;

    private Integer titleLength;

    private Integer contentLength;

    private LocalDateTime newsCreateTime;

    // getters and setters
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
}
