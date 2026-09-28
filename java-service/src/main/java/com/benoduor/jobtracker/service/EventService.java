package com.benoduor.jobtracker.service;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.repository.EventRepository;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.util.List;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class EventService {
    private final EventRepository eventRepository;

    public EventService(EventRepository eventRepository) {
        this.eventRepository = eventRepository;
    }

    public ApplicationEvent recordEvent(String applicationId, String eventType, String note) {
        ApplicationEvent event = new ApplicationEvent(applicationId, eventType, note);
        return eventRepository.save(event);
    }

    public List<ApplicationEvent> getEventsForApplication(String applicationId) {
        return eventRepository.findByApplicationId(applicationId);
    }

    public List<ApplicationEvent> getEventsByType(String eventType) {
        return eventRepository.findByEventType(eventType);
    }

    public long getTotalEventCount() {
        return eventRepository.count();
    }

    public long getEventCountByType(String eventType) {
        return eventRepository.countByEventType(eventType);
    }

    public Map<String, Object> getMetrics() {
        Map<String, Object> metrics = new HashMap<>();
        metrics.put("total_events", getTotalEventCount());
        metrics.put("applied_events", getEventCountByType("applied"));
        metrics.put("interview_events", getEventCountByType("interview"));
        metrics.put("offer_events", getEventCountByType("offer"));
        metrics.put("rejection_events", getEventCountByType("rejected"));
        return metrics;
    }

    public Map<String, Object> getApplicationTimeline(String applicationId) {
        List<ApplicationEvent> events = getEventsForApplication(applicationId);
        Map<String, Object> timeline = new HashMap<>();
        timeline.put("application_id", applicationId);
        timeline.put("event_count", events.size());
        timeline.put("events", events.stream()
            .map(e -> {
                Map<String, Object> evt = new HashMap<>();
                evt.put("id", e.getId());
                evt.put("type", e.getEventType());
                evt.put("note", e.getNote());
                evt.put("timestamp", e.getCreatedAt());
                return evt;
            })
            .collect(Collectors.toList()));
        return timeline;
    }
}
