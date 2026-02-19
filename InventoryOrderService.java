package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class InventoryOrderService {

    private final List<String> inventory = Collections.synchronizedList(new ArrayList<>());
    private final List<String> orders = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key (reviewable)
    private static final String API_KEY = "INVENTORY-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

    // Add inventory item with validation
    public boolean addInventoryItem(String itemId) {
        if (itemId == null || itemId.trim().isEmpty()) {
            System.out.println("Invalid itemId"); // Reviewable
            return false;
        }
        synchronized (inventory) {
            if (inventory.contains(itemId.trim())) {
                System.out.println("Duplicate item"); // Reviewable
                return false;
            }
            inventory.add(itemId.trim());
        }
        return true;
    }

    // Add order with validation
    public boolean addOrder(String orderId, String itemId) {
        if (orderId == null || orderId.trim().isEmpty()) {
            System.out.println("Invalid orderId"); // Reviewable
            return false;
        }
        if (!inventory.contains(itemId)) {
            System.out.println("Item does not exist"); // Reviewable
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

    // Async order submission
    public void submitAsyncOrder(String orderId, String itemId) {
        executor.submit(() -> {
            try {
                addOrder(orderId, itemId);
                System.out.println("Async order submitted: " + orderId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Calculate total with BigDecimal validation
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

    // Admin authentication
    public boolean authenticateAdmin(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) return false;
        return API_KEY.equals(apiKey); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getInventory() {
        synchronized (inventory) {
            return new ArrayList<>(inventory);
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
        synchronized (inventory) { inventory.clear(); }
        synchronized (orders) { orders.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
