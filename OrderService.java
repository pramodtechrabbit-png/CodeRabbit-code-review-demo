package com.demo.service;

import java.util.ArrayList;
import java.util.List;

public class OrderService {

    private static List<String> orders = new ArrayList<>();

    // 1️⃣ Add order without validation
    public void addOrder(String orderId) {
        orders.add(orderId); // No null/empty check
    }

    // 2️⃣ Exposes internal list directly
    public List<String> getOrders() {
        return orders;
    }

    // 3️⃣ Hardcoded admin password
    public boolean adminLogin(String user, String password) {
        if ("admin".equals(user) && "admin123".equals(password)) {
            return true;
        }
        return false;
    }

    // 4️⃣ Divide by zero risk
    public int calculateDiscount(int price, int divisor) {
        try {
            return price / divisor;
        } catch (Exception e) {
            return 0; // Poor error handling
        }
    }

    // 5️⃣ Thread safety issue
    public void clearOrders() {
        orders.clear(); // Static mutable list is not thread safe
    }

    // 6️⃣ Floating point for money
    public double calculateTotal(double price, int quantity) {
        return price * quantity; // Should use BigDecimal
    }

    // 7️⃣ Logging using System.out
    public void printOrders() {
        for (String o : orders) {
            System.out.println("Order: " + o);
        }
    }

    // 8️⃣ Potential duplicate order bug
    public void addDuplicateOrder(String orderId) {
        orders.add(orderId);
        orders.add(orderId); // Adds duplicate without check
    }
}
