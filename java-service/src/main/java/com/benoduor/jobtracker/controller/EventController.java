package com.benoduor.jobtracker.controller;

import com.benoduor.jobtracker.model.ApplicationEvent;
import com.benoduor.jobtracker.service.EventService;
import com.benoduor.jobtracker.service.EventAnalyticsService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/events")
@CrossOrigin(origins = "*")
public class EventController {
    private final EventService eventService;
    private final EventAnalyticsService analyticsService;

    public EventController(EventService eventService, EventAnalyticsService analyticsService) {
        this.eventService = eventService;
        this.analyticsService = analyticsService;
    }

    @PostMapping
    public ResponseEntity<Map<String, Object>> recordEvent(@RequestBody Map<String, String> payload) {
        String applicationId = payload.get("application_id");
        String eventType = payload.get("event_type");
        String note = payload.get("note");

        if (applicationId == null || eventType == null) {
            return ResponseEntity.badRequest().body(
                Map.of("error", "application_id and event_type are required")
            );
        }

        ApplicationEvent event = eventService.recordEvent(applicationId, eventType, note);
        Map<String, Object> response = new HashMap<>();
        response.put("id", event.getId());
        response.put("application_id", event.getApplicationId());
        response.put("event_type", event.getEventType());
        response.put("note", event.getNote());
        response.put("created_at", event.getCreatedAt());
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of(
            "status", "ok",
            "service", "job-tracker-events"
        ));
    }

    @GetMapping("/metrics")
    public ResponseEntity<Map<String, Object>> getMetrics() {
        return ResponseEntity.ok(eventService.getMetrics());
    }

    @GetMapping("/analytics")
    public ResponseEntity<Map<String, Object>> analytics() {
        return ResponseEntity.ok(analyticsService.summary());
    }

    @GetMapping("/analytics/recent")
    public ResponseEntity<Map<String, Object>> recentAnalytics(
        @RequestParam(defaultValue = "30") int days
    ) {
        return ResponseEntity.ok(analyticsService.recentSummary(days));
    }

    @GetMapping("/analytics/application/{applicationId}")
    public ResponseEntity<Map<String, Object>> applicationHealth(
        @PathVariable String applicationId
    ) {
        return ResponseEntity.ok(analyticsService.applicationHealth(applicationId));
    }

    @GetMapping("/analytics/stalled")
    public ResponseEntity<List<Map<String, Object>>> stalledApplications(
        @RequestParam(defaultValue = "7") int days
    ) {
        return ResponseEntity.ok(analyticsService.stalledApplications(days));
    }

    @GetMapping("/application/{applicationId}")
    public ResponseEntity<Map<String, Object>> getApplicationTimeline(@PathVariable String applicationId) {
        return ResponseEntity.ok(eventService.getApplicationTimeline(applicationId));
    }

    @GetMapping("/application/{applicationId}/events")
    public ResponseEntity<List<ApplicationEvent>> getApplicationEvents(@PathVariable String applicationId) {
        return ResponseEntity.ok(eventService.getEventsForApplication(applicationId));
    }

    @GetMapping("/type/{eventType}")
    public ResponseEntity<List<ApplicationEvent>> getEventsByType(@PathVariable String eventType) {
        return ResponseEntity.ok(eventService.getEventsByType(eventType));
    }
}
