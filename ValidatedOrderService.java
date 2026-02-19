package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class ValidatedOrderService {

    // Thread-safe immutable list exposure
    private final List<String> orders = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded admin password (reviewable)
    private static final String ADMIN_PASSWORD = "admin123";

    // Add order with validation
    public boolean addOrder(String orderId) {
        if (orderId == null || orderId.trim().isEmpty()) {
            System.out.println("Invalid orderId"); // Reviewable: should use logging
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

    // Retrieve a copy of the orders list (safe)
    public List<String> getOrders() {
        synchronized (orders) {
            return new ArrayList<>(orders); // Safe copy
        }
    }

    // Admin login with validation
    public boolean adminLogin(String password) {
        if (password == null || password.isEmpty()) {
            return false;
        }
        return ADMIN_PASSWORD.equals(password); // Reviewable: hardcoded
    }

    // Calculate total amount using BigDecimal (validation included)
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
            System.out.println("Invalid number format"); // Reviewable: should use logger
            return BigDecimal.ZERO;
        }
    }

    // Clear all orders
    public void clearOrders() {
        synchronized (orders) {
            orders.clear();
        }
    }
}
