package org.assignment.bi_backend.Entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Setter
@Getter
@Entity
@Table(name = "user_behavior")
public class UserBehavior {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "event_id")
    private Long eventId;

    @Column(name = "user_id", length = 255)
    private String userId;

    @Column(name = "news_id", length = 255)
    private String newsId;

    @Column(name = "event_time", columnDefinition = "DATETIME(6)")
    private LocalDateTime eventTime;

    @Column(name = "duration")
    private Integer duration;

}
