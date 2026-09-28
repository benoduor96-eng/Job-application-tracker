package com.benoduor.jobtracker.service;

import com.benoduor.jobtracker.model.ApplicationEvent;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;

@Service
public class EventService {

    private final AtomicLong events = new AtomicLong();
    private final Map<String, Long> countsByType = new HashMap<>();

    public synchronized long record(ApplicationEvent event) {
        validate(event);
        events.incrementAndGet();
        countsByType.merge(event.type(), 1L, Long::sum);
        return events.get();
    }

    public long count() {
        return events.get();
    }

    public synchronized Map<String, Long> countByType() {
        return Collections.unmodifiableMap(new HashMap<>(countsByType));
    }

    private void validate(ApplicationEvent event) {
        if (event == null || event.type() == null || event.type().isBlank()) {
            throw new IllegalArgumentException("Event type is required");
        }
        if (event.applicationId() == null || event.applicationId() < 0) {
            throw new IllegalArgumentException("Application id must be zero or greater");
        }
    }
}
