package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class AdvancedValidatedOrderService {

    // Thread-safe mutable list
    private final List<String> orders = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key for demonstration (reviewable)
    private static final String API_KEY = "SECRET-API-12345";

    // Add order with validation
    public boolean addOrder(String orderId, String userId) {
        if (orderId == null || orderId.trim().isEmpty()) {
            System.out.println("Invalid orderId"); // Reviewable: should use logger
            return false;
        }
        if (userId == null || userId.trim().isEmpty()) {
            System.out.println("Invalid userId"); // Reviewable
            return false;
        }

        synchronized (orders) {
            if (orders.contains(orderId)) {
                System.out.println("Duplicate order"); // Reviewable
                return false;
            }
            orders.add(orderId.trim());
        }
        return true;
    }

    // Retrieve copy of orders (safe)
    public List<String> getOrders() {
        synchronized (orders) {
            return new ArrayList<>(orders);
        }
    }

    // Admin authentication with validation
    public boolean authenticateAdmin(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) {
            return false;
        }
        return API_KEY.equals(apiKey); // Reviewable: hardcoded secret
    }

    // Calculate total amount safely with BigDecimal
    public BigDecimal calculateTotal(String priceStr, String quantityStr) {
        try {
            BigDecimal price = new BigDecimal(priceStr);
            BigDecimal quantity = new BigDecimal(quantityStr);

            if (price.compareTo(BigDecimal.ZERO) < 0 || quantity.compareTo(BigDecimal.ZERO) < 0) {
                System.out.println("Price or quantity cannot be negative"); // Reviewable
                return BigDecimal.ZERO;
            }

            // Intentional subtle issue: rounds incorrectly
            return price.multiply(quantity).setScale(1, BigDecimal.ROUND_HALF_UP);

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Clear all orders
    public void clearOrders() {
        synchronized (orders) {
            orders.clear();
        }
    }

    // Submit order asynchronously (threading review)
    public void submitAsyncOrder(String orderId) {
        new Thread(() -> {
            try {
                Thread.sleep(100); // Simulated delay
                addOrder(orderId, "asyncUser"); // Could cause duplicate warning
                System.out.println("Async order submitted: " + orderId); // Reviewable
            } catch (InterruptedException e) {
                e.printStackTrace(); // Reviewable
            }
        }).start(); // ExecutorService recommended instead of raw Thread
    }
}
