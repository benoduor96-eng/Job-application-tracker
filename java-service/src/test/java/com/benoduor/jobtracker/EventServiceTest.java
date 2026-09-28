package com.benoduor.jobtracker;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.repository.EventRepository;
import com.benoduor.jobtracker.service.EventService;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

class EventServiceTest {
    private EventRepository repository;
    private EventService service;

    @BeforeEach
    void setUp() {
        repository = mock(EventRepository.class);
        service = new EventService(repository);
    }

    @Test
    void recordsAndPersistsAnEvent() {
        ApplicationEvent saved = new ApplicationEvent("12", "created", "first");
        when(repository.save(any(ApplicationEvent.class))).thenReturn(saved);

        ApplicationEvent result = service.recordEvent("12", "created", "first");

        assertSame(saved, result);
        ArgumentCaptor<ApplicationEvent> captor = ArgumentCaptor.forClass(ApplicationEvent.class);
        verify(repository).save(captor.capture());
        assertEquals("12", captor.getValue().getApplicationId());
        assertEquals("created", captor.getValue().getEventType());
        assertEquals("first", captor.getValue().getNote());
    }

    @Test
    void returnsEventsForAnApplication() {
        List<ApplicationEvent> events = List.of(
            new ApplicationEvent("12", "created", "first"),
            new ApplicationEvent("12", "updated", "changed")
        );
        when(repository.findByApplicationId("12")).thenReturn(events);

        assertSame(events, service.getEventsForApplication("12"));
        verify(repository).findByApplicationId("12");
    }

    @Test
    void returnsMetricsByEventType() {
        when(repository.count()).thenReturn(5L);
        when(repository.countByEventType("applied")).thenReturn(3L);
        when(repository.countByEventType("interview")).thenReturn(2L);
        when(repository.countByEventType("offer")).thenReturn(1L);
        when(repository.countByEventType("rejected")).thenReturn(1L);

        Map<String, Object> metrics = service.getMetrics();

        assertEquals(5L, metrics.get("total_events"));
        assertEquals(3L, metrics.get("applied_events"));
        assertEquals(2L, metrics.get("interview_events"));
        assertEquals(1L, metrics.get("offer_events"));
        assertEquals(1L, metrics.get("rejection_events"));
    }

    @Test
    void buildsApplicationTimeline() {
        ApplicationEvent event = new ApplicationEvent("12", "applied", "submitted");
        when(repository.findByApplicationId("12")).thenReturn(List.of(event));

        Map<String, Object> timeline = service.getApplicationTimeline("12");

        assertEquals("12", timeline.get("application_id"));
        assertEquals(1, timeline.get("event_count"));
        assertNotNull(timeline.get("events"));
        verify(repository).findByApplicationId("12");
    }
}
