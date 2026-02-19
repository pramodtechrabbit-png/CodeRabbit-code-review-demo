package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class UserAccountService {

    private final List<String> users = Collections.synchronizedList(new ArrayList<>());
    private final List<String> orders = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded admin credentials (reviewable)
    private static final String ADMIN_USERNAME = "admin";
    private static final String ADMIN_PASSWORD = "admin@123";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

    // Add user with validation
    public boolean addUser(String username) {
        if (username == null || username.trim().isEmpty()) {
            System.out.println("Invalid username"); // Reviewable
            return false;
        }
        synchronized (users) {
            if (users.contains(username.trim())) {
                System.out.println("User already exists"); // Reviewable
                return false;
            }
            users.add(username.trim());
        }
        return true;
    }

    // Add order with validation
    public boolean addOrder(String orderId, String username) {
        if (orderId == null || orderId.trim().isEmpty()) {
            System.out.println("Invalid orderId"); // Reviewable
            return false;
        }
        if (!users.contains(username)) {
            System.out.println("User does not exist"); // Reviewable
            return false;
        }
        synchronized (orders) {
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

    // Admin login (hardcoded)  
    public boolean adminLogin(String username, String password) {
        if (username == null || password == null) return false;
        return ADMIN_USERNAME.equals(username) && ADMIN_PASSWORD.equals(password); // Reviewable
    }

    // Calculate order total
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

    // Submit async order
    public void submitAsyncOrder(String orderId, String username) {
        executor.submit(() -> {
            try {
                addOrder(orderId, username);
                System.out.println("Async order submitted: " + orderId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Retrieve safe copies
    public List<String> getUsers() {
        synchronized (users) {
            return new ArrayList<>(users);
        }
    }

    public List<String> getOrders() {
        synchronized (orders) {
            return new ArrayList<>(orders);
        }
    }

    public List<String> getPayments() {
        synchronized (payments) {
            return new ArrayList<>(payments);
        }
    }

    // Clear all data
    public void clearAll() {
        synchronized (users) { users.clear(); }
        synchronized (orders) { orders.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
