package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class BillingInvoiceService {

    private final List<String> clients = Collections.synchronizedList(new ArrayList<>());
    private final List<String> invoices = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded API key (reviewable)
    private static final String BILLING_API_KEY = "BILLING-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(2);

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

    // Add invoice with validation
    public boolean addInvoice(String invoiceId, String clientId, String amountStr) {
        if (invoiceId == null || invoiceId.trim().isEmpty()) {
            System.out.println("Invalid invoiceId"); // Reviewable
            return false;
        }
        if (!clients.contains(clientId)) {
            System.out.println("Client does not exist"); // Reviewable
            return false;
        }

        BigDecimal amount;
        try {
            amount = new BigDecimal(amountStr);
            if (amount.compareTo(BigDecimal.ZERO) <= 0) {
                System.out.println("Invoice amount must be positive"); // Reviewable
                return false;
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid amount format"); // Reviewable
            return false;
        }

        synchronized (invoices) {
            invoices.add(invoiceId.trim());
        }
        return true;
    }

    // Add payment with validation
    public boolean addPayment(String paymentId, String invoiceId) {
        if (paymentId == null || paymentId.trim().isEmpty()) {
            System.out.println("Invalid paymentId"); // Reviewable
            return false;
        }
        if (!invoices.contains(invoiceId)) {
            System.out.println("Invoice does not exist"); // Reviewable
            return false;
        }
        synchronized (payments) {
            payments.add(paymentId.trim());
        }
        return true;
    }

    // Async invoice creation
    public void submitAsyncInvoice(String invoiceId, String clientId, String amountStr) {
        executor.submit(() -> {
            try {
                addInvoice(invoiceId, clientId, amountStr);
                System.out.println("Async invoice submitted: " + invoiceId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Calculate total invoice amount safely
    public BigDecimal calculateTotalInvoice(String amountStr, String taxStr) {
        try {
            BigDecimal amount = new BigDecimal(amountStr);
            BigDecimal tax = new BigDecimal(taxStr);

            if (amount.compareTo(BigDecimal.ZERO) < 0 || tax.compareTo(BigDecimal.ZERO) < 0) {
                System.out.println("Amount or tax cannot be negative"); // Reviewable
                return BigDecimal.ZERO;
            }

            // Total = amount + tax%
            return amount.add(amount.multiply(tax).divide(new BigDecimal("100"))); // Reviewable: rounding not handled

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Admin authentication
    public boolean authenticateAdmin(String apiKey) {
        if (apiKey == null || apiKey.isEmpty()) return false;
        return BILLING_API_KEY.equals(apiKey); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getClients() {
        synchronized (clients) { return new ArrayList<>(clients); }
    }

    public List<String> getInvoices() {
        synchronized (invoices) { return new ArrayList<>(invoices); }
    }

    public List<String> getPayments() {
        synchronized (payments) { return new ArrayList<>(payments); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (clients) { clients.clear(); }
        synchronized (invoices) { invoices.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
