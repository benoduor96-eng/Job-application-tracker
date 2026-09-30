package com.benoduor.jobtracker.service;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.repository.EventRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.mockito.Mockito;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

class EventAnalyticsServiceTest {
    private EventRepository repository;
    private EventAnalyticsService service;

    @BeforeEach
    void setUp() {
        repository = Mockito.mock(EventRepository.class);
        service = new EventAnalyticsService(repository);
    }

    @Test
    void summaryCountsApplicationsAndEvents() {
        when(repository.findAll()).thenReturn(List.of(
            event("1", "applied"),
            event("1", "interview"),
            event("2", "applied"),
            event("2", "offer")
        ));

        Map<String, Object> result = service.summary();

        assertEquals(2L, result.get("application_count"));
        assertEquals(4, result.get("event_count"));
        Map<?, ?> types = (Map<?, ?>) result.get("event_types");
        assertEquals(2L, types.get("applied"));
        assertEquals(1L, types.get("offer"));
    }

    @Test
    void conversionMetricsReturnPercentages() {
        when(repository.findAll()).thenReturn(List.of(
            event("1", "applied"),
            event("2", "applied"),
            event("3", "applied"),
            event("1", "interview"),
            event("2", "interview"),
            event("1", "offer")
        ));

        Map<String, Object> result = service.summary();
        Map<?, ?> conversion = (Map<?, ?>) result.get("conversion");

        assertEquals(66.67, conversion.get("interview_from_applied"));
        assertEquals(33.33, conversion.get("offer_from_applied"));
        assertEquals(50.0, conversion.get("offer_from_interview"));
    }

    @Test
    void applicationHealthBuildsTransitions() {
        when(repository.findByApplicationId("1")).thenReturn(List.of(
            event("1", "applied"),
            event("1", "screening"),
            event("1", "interview")
        ));

        Map<String, Object> result = service.applicationHealth("1");

        assertEquals("1", result.get("application_id"));
        assertEquals(3, result.get("event_count"));
        assertFalse(result.get("terminal").equals(Boolean.TRUE));
        assertEquals(
            List.of("applied", "screening", "interview"),
            result.get("event_types")
        );
        List<?> transitions = (List<?>) result.get("transitions");
        assertEquals(2, transitions.size());
    }

    @Test
    void terminalApplicationIsDetected() {
        when(repository.findByApplicationId("1")).thenReturn(List.of(
            event("1", "applied"),
            event("1", "rejected")
        ));

        Map<String, Object> result = service.applicationHealth("1");

        assertEquals(Boolean.TRUE, result.get("terminal"));
    }

    @Test
    void stalledApplicationsExcludeTerminalApplications() {
        LocalDateTime old = LocalDateTime.now().minusDays(20);
        when(repository.findAll()).thenReturn(List.of(
            eventAt("1", "applied", old),
            eventAt("2", "applied", old),
            eventAt("2", "rejected", old.plusHours(1))
        ));

        List<Map<String, Object>> result = service.stalledApplications(7);

        assertEquals(1, result.size());
        assertEquals("1", result.get(0).get("application_id"));
        assertTrue(((Number) result.get(0).get("days_since_activity")).longValue() >= 19);
    }

    @Test
    void recentSummaryBoundsRequestedDays() {
        when(repository.findByCreatedAtAfter(Mockito.any(LocalDateTime.class)))
            .thenReturn(List.of(event("1", "applied")));

        Map<String, Object> result = service.recentSummary(10000);

        assertEquals(3650, result.get("period_days"));
        assertEquals(1, result.get("event_count"));
    }

    private ApplicationEvent event(String applicationId, String type) {
        return eventAt(applicationId, type, LocalDateTime.now().minusHours(1));
    }

    private ApplicationEvent eventAt(
        String applicationId,
        String type,
        LocalDateTime timestamp
    ) {
        ApplicationEvent event = new ApplicationEvent(applicationId, type, "test");
        event.setCreatedAt(timestamp);
        return event;
    }
}
