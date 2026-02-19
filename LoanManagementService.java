package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class LoanManagementService {

    private final List<String> users = Collections.synchronizedList(new ArrayList<>());
    private final List<String> loans = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key for admin access (reviewable)
    private static final String ADMIN_API_KEY = "LOAN-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

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

    // Add loan with validation
    public boolean addLoan(String loanId, String userId, String amountStr) {
        if (loanId == null || loanId.trim().isEmpty()) {
            System.out.println("Invalid loanId"); // Reviewable
            return false;
        }
        if (!users.contains(userId)) {
            System.out.println("User does not exist"); // Reviewable
            return false;
        }

        BigDecimal amount;
        try {
            amount = new BigDecimal(amountStr);
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                System.out.println("Amount must be positive"); // Reviewable
                return false;
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount format"); // Reviewable
            return false;
        }

        synchronized (loans) {
            loans.add(loanId.trim());
        }
        return true;
    }

    // Add payment with validation
    public boolean addPayment(String paymentId, String loanId) {
        if (paymentId == null || paymentId.trim().isEmpty()) {
            System.out.println("Invalid paymentId"); // Reviewable
            return false;
        }
        if (!loans.contains(loanId)) {
            System.out.println("Loan does not exist"); // Reviewable
            return false;
        }
        synchronized (payments) {
            payments.add(paymentId.trim());
        }
        return true;
    }

    // Async loan submission
    public void submitAsyncLoan(String loanId, String userId, String amountStr) {
        executor.submit(() -> {
            try {
                addLoan(loanId, userId, amountStr);
                System.out.println("Async loan submitted: " + loanId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Calculate total loan amount
    public BigDecimal calculateTotalLoan(String amountStr, String interestRateStr, String monthsStr) {
        try {
            BigDecimal principal = new BigDecimal(amountStr);
            BigDecimal rate = new BigDecimal(interestRateStr);
            BigDecimal months = new BigDecimal(monthsStr);

            if (principal.compareTo(BigDecimal.ZERO) <= 0 ||
                rate.compareTo(BigDecimal.ZERO) < 0 ||
                months.compareTo(BigDecimal.ZERO) <= 0) {
                System.out.println("Invalid principal, rate, or months"); // Reviewable
                return BigDecimal.ZERO;
            }

            // Simple interest calculation (reviewable: rounding not handled)
            return principal.add(principal.multiply(rate).multiply(months).divide(new BigDecimal("100")));

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Admin authentication
    public boolean authenticateAdmin(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) return false;
        return ADMIN_API_KEY.equals(apiKey); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getUsers() {
        synchronized (users) { return new ArrayList<>(users); }
    }

    public List<String> getLoans() {
        synchronized (loans) { return new ArrayList<>(loans); }
    }

    public List<String> getPayments() {
        synchronized (payments) { return new ArrayList<>(payments); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (users) { users.clear(); }
        synchronized (loans) { loans.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
