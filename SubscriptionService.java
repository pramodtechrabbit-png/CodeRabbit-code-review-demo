package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class SubscriptionService {

    private final List<String> users = Collections.synchronizedList(new ArrayList<>());
    private final List<String> subscriptions = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key (reviewable)
    private static final String API_KEY = "SUBSCRIPTION-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(2);

    // Add user with validation
    public boolean addUser(String userId) {
        if (userId == null || userId.trim().isEmpty()) {
            System.out.println("Invalid userId"); // Reviewable
            return false;
        }
        synchronized (users) {
            if (users.contains(userId.trim())) {
                System.out.println("Duplicate user"); // Reviewable
                return false;
            }
            users.add(userId.trim());
        }
        return true;
    }

    // Add subscription with validation
    public boolean addSubscription(String subscriptionId, String userId) {
        if (subscriptionId == null || subscriptionId.trim().isEmpty()) {
            System.out.println("Invalid subscriptionId"); // Reviewable
            return false;
        }
        if (!users.contains(userId)) {
            System.out.println("User does not exist"); // Reviewable
            return false;
        }
        synchronized (subscriptions) {
            subscriptions.add(subscriptionId.trim());
        }
        return true;
    }

    // Add payment with validation
    public boolean addPayment(String paymentId, String subscriptionId) {
        if (paymentId == null || paymentId.trim().isEmpty()) {
            System.out.println("Invalid paymentId"); // Reviewable
            return false;
        }
        if (!subscriptions.contains(subscriptionId)) {
            System.out.println("Subscription does not exist"); // Reviewable
            return false;
        }
        synchronized (payments) {
            payments.add(paymentId.trim());
        }
        return true;
    }

    // Async subscription creation
    public void submitAsyncSubscription(String subscriptionId, String userId) {
        executor.submit(() -> {
            try {
                addSubscription(subscriptionId, userId);
                System.out.println("Async subscription submitted: " + subscriptionId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Calculate subscription cost safely
    public BigDecimal calculateTotal(String priceStr, String monthsStr) {
        try {
            BigDecimal price = new BigDecimal(priceStr);
            BigDecimal months = new BigDecimal(monthsStr);

            if (price.compareTo(BigDecimal.ZERO) < 0 || months.compareTo(BigDecimal.ZERO) < 0) {
                System.out.println("Price or months cannot be negative"); // Reviewable
                return BigDecimal.ZERO;
            }

            return price.multiply(months);

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Admin authentication
    public boolean authenticateAdmin(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) return false;
        return API_KEY.equals(apiKey); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getUsers() {
        synchronized (users) { return new ArrayList<>(users); }
    }

    public List<String> getSubscriptions() {
        synchronized (subscriptions) { return new ArrayList<>(subscriptions); }
    }

    public List<String> getPayments() {
        synchronized (payments) { return new ArrayList<>(payments); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (users) { users.clear(); }
        synchronized (subscriptions) { subscriptions.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
