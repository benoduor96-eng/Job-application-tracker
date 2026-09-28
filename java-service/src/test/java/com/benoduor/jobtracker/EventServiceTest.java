package com.benoduor.jobtracker.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import com.benoduor.jobtracker.model.ApplicationEvent;
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
        service.record(new ApplicationEvent("created", 12L));
        service.record(new ApplicationEvent("updated", 12L));

        assertEquals(2, service.count());
    }

    @Test
    void rejectsMissingEventType() {
        assertThrows(
            IllegalArgumentException.class,
            () -> service.record(new ApplicationEvent("", 4L))
        );
    }

    @Test
    void rejectsNegativeApplicationId() {
        assertThrows(
            IllegalArgumentException.class,
            () -> service.record(new ApplicationEvent("created", -1L))
        );
    }

    @Test
    void exposesCountsByEventType() {
        service.record(new ApplicationEvent("created", 1L));
        service.record(new ApplicationEvent("created", 2L));
        service.record(new ApplicationEvent("updated", 1L));

        Map<String, Long> counts = service.countByType();

        assertEquals(2L, counts.get("created"));
        assertEquals(1L, counts.get("updated"));
    }

    @Test
    void returnsAnImmutableSnapshot() {
        service.record(new ApplicationEvent("created", 1L));

        Map<String, Long> counts = service.countByType();

        assertThrows(
            UnsupportedOperationException.class,
            () -> counts.put("deleted", 1L)
        );
    }
}
