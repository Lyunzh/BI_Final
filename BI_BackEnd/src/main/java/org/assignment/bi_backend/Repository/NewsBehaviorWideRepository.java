package org.assignment.bi_backend.Repository;

import org.assignment.bi_backend.Entity.NewsBehaviorWide;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NewsBehaviorWideRepository extends JpaRepository<NewsBehaviorWide, Long> {
}
