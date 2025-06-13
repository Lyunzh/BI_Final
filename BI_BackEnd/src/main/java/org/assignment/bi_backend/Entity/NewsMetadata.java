package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "news_metadata")
public class NewsMetadata {
    @Id
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

    @Column(name = "create_time", columnDefinition = "DATETIME(6)", nullable = false)
    private LocalDateTime createTime;

    // Getters and Setters
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

    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime createTime) { this.createTime = createTime; }
}
