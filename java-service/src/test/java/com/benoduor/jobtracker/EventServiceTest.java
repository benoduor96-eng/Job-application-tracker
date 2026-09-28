package com.benoduor.jobtracker;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.service.EventService;
import java.util.Map;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class EventServiceTest {
    private EventService service;

    @BeforeEach
    void setUp() {
        service = new EventService();
    }

    @Test
    void startsWithNoEvents() {
        assertEquals(0, service.count());
    }

    @Test
    void recordsEventsAndIncrementsCount() {
        service.record(new ApplicationEvent("12", "created", "first"));
        service.record(new ApplicationEvent("12", "updated", "changed"));
        assertEquals(2, service.count());
    }

    @Test
    void rejectsMissingEventType() {
        assertThrows(IllegalArgumentException.class,
            () -> service.record(new ApplicationEvent("4", "", "missing type")));
    }

    @Test
    void rejectsMissingApplicationId() {
        assertThrows(IllegalArgumentException.class,
            () -> service.record(new ApplicationEvent("", "created", "missing id")));
    }

    @Test
    void exposesCountsByEventType() {
        service.record(new ApplicationEvent("1", "created", "one"));
        service.record(new ApplicationEvent("2", "created", "two"));
        service.record(new ApplicationEvent("1", "updated", "three"));
        Map<String, Long> counts = service.countByType();
        assertEquals(2L, counts.get("created"));
        assertEquals(1L, counts.get("updated"));
    }

    @Test
    void returnsAnImmutableSnapshot() {
        service.record(new ApplicationEvent("1", "created", "one"));
        Map<String, Long> counts = service.countByType();
        assertThrows(UnsupportedOperationException.class,
            () -> counts.put("deleted", 1L));
    }
}
