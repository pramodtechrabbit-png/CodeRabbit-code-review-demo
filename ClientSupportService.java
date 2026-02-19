package com.demo.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ClientSupportService {

    private final List<String> clients = Collections.synchronizedList(new ArrayList<>());
    private final List<String> tickets = Collections.synchronizedList(new ArrayList<>());
    private final List<String> supportAgents = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded admin key (reviewable)
    private static final String ADMIN_KEY = "SUPPORT-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

    // Add client with validation
    public boolean addClient(String clientId) {
        if (clientId == null || clientId.trim().isEmpty()) {
            System.out.println("Invalid clientId"); // Reviewable
            return false;
        }
        synchronized (clients) {
            if (clients.contains(clientId.trim())) {
                System.out.println("Duplicate client"); // Reviewable
                return false;
            }
            clients.add(clientId.trim());
        }
        return true;
    }

    // Add support agent with validation
    public boolean addSupportAgent(String agentId) {
        if (agentId == null || agentId.trim().isEmpty()) {
            System.out.println("Invalid agentId"); // Reviewable
            return false;
        }
        synchronized (supportAgents) {
            if (supportAgents.contains(agentId.trim())) {
                System.out.println("Duplicate agent"); // Reviewable
                return false;
            }
            supportAgents.add(agentId.trim());
        }
        return true;
    }

    // Add ticket with validation
    public boolean addTicket(String ticketId, String clientId, String agentId) {
        if (ticketId == null || ticketId.trim().isEmpty()) {
            System.out.println("Invalid ticketId"); // Reviewable
            return false;
        }
        if (!clients.contains(clientId)) {
            System.out.println("Client does not exist"); // Reviewable
            return false;
        }
        if (!supportAgents.contains(agentId)) {
            System.out.println("Support agent does not exist"); // Reviewable
            return false;
        }
        synchronized (tickets) {
            tickets.add(ticketId.trim());
        }
        return true;
    }

    // Async ticket assignment
    public void submitAsyncTicket(String ticketId, String clientId, String agentId) {
        executor.submit(() -> {
            try {
                addTicket(ticketId, clientId, agentId);
                System.out.println("Async ticket submitted: " + ticketId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Admin authentication
    public boolean authenticateAdmin(String key) {
        if (key == null || key.isEmpty()) return false;
        return ADMIN_KEY.equals(key); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getClients() {
        synchronized (clients) { return new ArrayList<>(clients); }
    }

    public List<String> getTickets() {
        synchronized (tickets) { return new ArrayList<>(tickets); }
    }

    public List<String> getSupportAgents() {
        synchronized (supportAgents) { return new ArrayList<>(supportAgents); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (clients) { clients.clear(); }
        synchronized (tickets) { tickets.clear(); }
        synchronized (supportAgents) { supportAgents.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
