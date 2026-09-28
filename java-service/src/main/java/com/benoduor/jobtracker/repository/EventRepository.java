package com.benoduor.jobtracker.repository;

import com.benoduor.jobtracker.model.ApplicationEvent;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface EventRepository extends JpaRepository<ApplicationEvent, Long> {
    List<ApplicationEvent> findByApplicationId(String applicationId);
    List<ApplicationEvent> findByEventType(String eventType);
    List<ApplicationEvent> findByCreatedAtAfter(LocalDateTime date);
    long countByEventType(String eventType);
}
