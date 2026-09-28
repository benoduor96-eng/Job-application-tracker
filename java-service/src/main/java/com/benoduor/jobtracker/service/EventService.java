package com.benoduor.jobtracker.service;
import com.benoduor.jobtracker.model.ApplicationEvent; import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Service;
@Service public class EventService { private final AtomicLong events=new AtomicLong(); public long record(ApplicationEvent e){ return events.incrementAndGet(); } public long count(){ return events.get(); } }
