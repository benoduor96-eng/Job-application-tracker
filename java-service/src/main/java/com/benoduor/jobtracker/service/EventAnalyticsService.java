package com.benoduor.jobtracker.service;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.repository.EventRepository;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * Event analytics independent from the persistence-facing EventService.
 *
 * The calculations are deterministic and operate on stored events, making
 * them suitable for reporting endpoints and scheduled aggregation later.
 */
@Service
public class EventAnalyticsService {
    private static final Set<String> TERMINAL_EVENTS =
        Set.of("offer", "rejected", "withdrawn");

    private final EventRepository repository;

    public EventAnalyticsService(EventRepository repository) {
        this.repository = repository;
    }

    public Map<String, Object> summary() {
        List<ApplicationEvent> events = repository.findAll();
        return summarize(events);
    }

    public Map<String, Object> recentSummary(int days) {
        int boundedDays = Math.max(1, Math.min(days, 3650));
        LocalDateTime since = LocalDateTime.now().minusDays(boundedDays);
        List<ApplicationEvent> events = repository.findByCreatedAtAfter(since);
        Map<String, Object> result = summarize(events);
        result.put("period_days", boundedDays);
        result.put("since", since);
        return result;
    }

    public Map<String, Object> applicationHealth(String applicationId) {
        List<ApplicationEvent> events = repository.findByApplicationId(applicationId)
            .stream()
            .sorted(Comparator.comparing(ApplicationEvent::getCreatedAt))
            .toList();

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("application_id", applicationId);
        result.put("event_count", events.size());
        result.put("first_event", events.isEmpty() ? null : events.get(0).getCreatedAt());
        result.put("last_event", events.isEmpty() ? null :
            events.get(events.size() - 1).getCreatedAt());
        result.put("duration_hours", durationHours(events));
        result.put("terminal", isTerminal(events));
        result.put("event_types", distinctTypes(events));
        result.put("transitions", transitions(events));
        return result;
    }

    public List<Map<String, Object>> stalledApplications(int minimumDays) {
        int days = Math.max(1, Math.min(minimumDays, 3650));
        LocalDateTime cutoff = LocalDateTime.now().minusDays(days);
        Map<String, List<ApplicationEvent>> byApplication =
            repository.findAll().stream()
                .filter(event -> event.getCreatedAt() != null)
                .collect(Collectors.groupingBy(
                    ApplicationEvent::getApplicationId,
                    LinkedHashMap::new,
                    Collectors.toList()
                ));

        List<Map<String, Object>> stalled = new ArrayList<>();
        for (Map.Entry<String, List<ApplicationEvent>> entry : byApplication.entrySet()) {
            List<ApplicationEvent> events = entry.getValue().stream()
                .sorted(Comparator.comparing(ApplicationEvent::getCreatedAt))
                .toList();
            if (events.isEmpty()) {
                continue;
            }
            ApplicationEvent last = events.get(events.size() - 1);
            if (last.getCreatedAt().isBefore(cutoff) && !isTerminal(events)) {
                Map<String, Object> item = new LinkedHashMap<>();
                item.put("application_id", entry.getKey());
                item.put("last_event", last.getCreatedAt());
                item.put("last_event_type", last.getEventType());
                item.put(
                    "days_since_activity",
                    Duration.between(last.getCreatedAt(), LocalDateTime.now()).toDays()
                );
                item.put("event_count", events.size());
                stalled.add(item);
            }
        }

        stalled.sort((left, right) ->
            Long.compare(
                ((Number) right.get("days_since_activity")).longValue(),
                ((Number) left.get("days_since_activity")).longValue()
            )
        );
        return stalled;
    }

    private Map<String, Object> summarize(List<ApplicationEvent> events) {
        Map<String, Long> byType = events.stream()
            .filter(Objects::nonNull)
            .collect(Collectors.groupingBy(
                ApplicationEvent::getEventType,
                LinkedHashMap::new,
                Collectors.counting()
            ));

        long applications = events.stream()
            .map(ApplicationEvent::getApplicationId)
            .filter(Objects::nonNull)
            .distinct()
            .count();

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("application_count", applications);
        result.put("event_count", events.size());
        result.put("event_types", byType);
        result.put("conversion", conversionMetrics(byType));
        return result;
    }

    private Map<String, Double> conversionMetrics(Map<String, Long> counts) {
        double applied = counts.getOrDefault("applied", 0L);
        double screening = counts.getOrDefault("screening", 0L);
        double interview = counts.getOrDefault("interview", 0L);
        double offer = counts.getOrDefault("offer", 0L);

        Map<String, Double> result = new LinkedHashMap<>();
        result.put("screening_from_applied", rate(screening, applied));
        result.put("interview_from_applied", rate(interview, applied));
        result.put("offer_from_applied", rate(offer, applied));
        result.put("offer_from_interview", rate(offer, interview));
        return result;
    }

    private double rate(double numerator, double denominator) {
        if (denominator <= 0) {
            return 0.0;
        }
        return Math.round((numerator / denominator) * 10000.0) / 100.0;
    }

    private long durationHours(List<ApplicationEvent> events) {
        if (events.size() < 2) {
            return 0;
        }
        return Duration.between(
            events.get(0).getCreatedAt(),
            events.get(events.size() - 1).getCreatedAt()
        ).toHours();
    }

    private boolean isTerminal(List<ApplicationEvent> events) {
        if (events.isEmpty()) {
            return false;
        }
        String type = events.get(events.size() - 1).getEventType();
        return TERMINAL_EVENTS.contains(type);
    }

    private List<String> distinctTypes(List<ApplicationEvent> events) {
        return events.stream()
            .map(ApplicationEvent::getEventType)
            .filter(Objects::nonNull)
            .distinct()
            .toList();
    }

    private List<Map<String, String>> transitions(List<ApplicationEvent> events) {
        List<Map<String, String>> result = new ArrayList<>();
        String previous = null;
        for (ApplicationEvent event : events) {
            if (event.getEventType() == null) {
                continue;
            }
            if (previous != null && !previous.equals(event.getEventType())) {
                result.add(Map.of(
                    "from", previous,
                    "to", event.getEventType()
                ));
            }
            previous = event.getEventType();
        }
        return result;
    }
}
