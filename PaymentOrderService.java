package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class PaymentOrderService {

    private final List<String> orders = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key (reviewable)
    private static final String API_KEY = "API-SECRET-98765";

    private final ExecutorService executor = Executors.newFixedThreadPool(3); // ExecutorService

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

    // Add payment with validation
    public boolean addPayment(String paymentId, String orderId) {
        if (paymentId == null || paymentId.trim().isEmpty()) {
            System.out.println("Invalid paymentId"); // Reviewable
            return false;
        }
        if (!orders.contains(orderId)) {
            System.out.println("Order does not exist"); // Reviewable
            return false;
        }

        synchronized (payments) {
            payments.add(paymentId.trim());
        }
        return true;
    }

    // Retrieve safe copy of orders
    public List<String> getOrders() {
        synchronized (orders) {
            return new ArrayList<>(orders);
        }
    }

    // Retrieve safe copy of payments
    public List<String> getPayments() {
        synchronized (payments) {
            return new ArrayList<>(payments);
        }
    }

    // Admin authentication
    public boolean authenticate(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) {
            return false;
        }
        return API_KEY.equals(apiKey); // Reviewable: hardcoded
    }

    // Calculate total safely
    public BigDecimal calculateTotal(String priceStr, String quantityStr) {
        try {
            BigDecimal price = new BigDecimal(priceStr);
            BigDecimal quantity = new BigDecimal(quantityStr);

            if (price.compareTo(BigDecimal.ZERO) < 0 || quantity.compareTo(BigDecimal.ZERO) < 0) {
                System.out.println("Price or quantity cannot be negative"); // Reviewable
                return BigDecimal.ZERO;
            }

            return price.multiply(quantity);

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Submit order asynchronously
    public void submitAsyncOrder(String orderId, String userId) {
        executor.submit(() -> {
            try {
                addOrder(orderId, userId);
                System.out.println("Async order submitted: " + orderId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Shutdown executor (good practice, reviewable if missing in future)
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
