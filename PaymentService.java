package com.demo.service;

import java.util.ArrayList;
import java.util.List;

public class PaymentService {

    private static List<String> payments = new ArrayList<>();

    // 1️⃣ Adds payment without validation
    public void addPayment(String paymentId) {
        payments.add(paymentId); // No null or empty check
    }

    // 2️⃣ Returns internal mutable list
    public List<String> getPayments() {
        return payments;
    }

    // 3️⃣ Hardcoded API key (security flaw)
    private static final String API_KEY = "12345-SECRET-KEY";

    public boolean authenticate(String apiKey) {
        return API_KEY.equals(apiKey);
    }

    // 4️⃣ Floating point for money calculation
    public double calculateAmount(double price, int quantity) {
        return price * quantity; // Should use BigDecimal
    }

    // 5️⃣ Divide by zero risk
    public int calculateDiscount(int price, int divisor) {
        try {
            return price / divisor;
        } catch (Exception e) {
            return 0; // Poor error handling
        }
    }

    // 6️⃣ Thread safety issue
    public void clearPayments() {
        payments.clear(); // Static mutable list is not thread safe
    }

    // 7️⃣ Logging using System.out
    public void printPayments() {
        for (String p : payments) {
            System.out.println("Payment: " + p);
        }
    }

    // 8️⃣ Adds duplicate payment
    public void addDuplicatePayment(String paymentId) {
        payments.add(paymentId);
        payments.add(paymentId); // Adds duplicate without check
    }
}
