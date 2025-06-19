package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Setter
@Getter
@Entity
@Table(name = "news_metadata")
public class NewsMetadata {

    @Id
    @Column(name = "news_id", length = 255)
    private String newsId;

    @Column(name = "title", length = 500)
    private String title;

    @Lob
    @Column(name = "content")
    private String content;

    @Column(name = "category", length = 20)
    private String category;

    @Column(name = "topic", length = 50)
    private String topic;

    @Column(name = "title_length")
    private Integer titleLength;

    @Column(name = "content_length")
    private Integer contentLength;

    @Column(name = "create_time", columnDefinition = "DATETIME(6)")
    private LocalDateTime newsCreateTime;

}
