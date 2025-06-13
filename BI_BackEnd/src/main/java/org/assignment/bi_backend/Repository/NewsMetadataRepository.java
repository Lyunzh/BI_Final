package org.assignment.bi_backend.Repository;

import org.assignment.bi_backend.Entity.NewsMetadata;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NewsMetadataRepository extends JpaRepository<NewsMetadata, String> {
}
