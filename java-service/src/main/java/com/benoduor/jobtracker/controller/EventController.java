package com.benoduor.jobtracker.controller;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.service.EventService;
import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/events")
public class EventController {

    private final EventService service;

    public EventController(EventService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> record(
            @RequestBody ApplicationEvent event) {
        long total = service.record(event);
        return ResponseEntity.ok(Map.of(
                "accepted", true,
                "eventCount", total,
                "eventType", event.eventType()
        ));
    }

    @GetMapping("/stats")
    public Map<String, Object> stats() {
        return Map.of(
                "eventCount", service.count(),
                "byType", service.countByType()
        );
    }

    @GetMapping("/health")
    public Map<String, String> health() {
        return Map.of(
                "status", "ok",
                "service", "job-tracker-events"
        );
    }
}
