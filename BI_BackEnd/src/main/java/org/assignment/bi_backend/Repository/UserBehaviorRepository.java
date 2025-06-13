package org.assignment.bi_backend.Repository;

import org.assignment.bi_backend.Entity.UserBehavior;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface UserBehaviorRepository extends JpaRepository<UserBehavior, Long> {
    List<UserBehavior> findByEventTimeBetween(LocalDateTime start, LocalDateTime end);
}
