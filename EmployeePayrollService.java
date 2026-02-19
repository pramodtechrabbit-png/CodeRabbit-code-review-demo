package com.demo.service;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class EmployeePayrollService {

    private final List<String> employees = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payrolls = Collections.synchronizedList(new ArrayList<>());
    private final List<String> payments = Collections.synchronizedList(new ArrayList<>());

    // Hardcoded admin key (reviewable)
    private static final String ADMIN_KEY = "PAYROLL-SECRET-2026";

    private final ExecutorService executor = Executors.newFixedThreadPool(3);

    // Add employee with validation
    public boolean addEmployee(String employeeId) {
        if (employeeId == null || employeeId.trim().isEmpty()) {
            System.out.println("Invalid employeeId"); // Reviewable
            return false;
        }
        synchronized (employees) {
            if (employees.contains(employeeId.trim())) {
                System.out.println("Duplicate employee"); // Reviewable
                return false;
            }
            employees.add(employeeId.trim());
        }
        return true;
    }

    // Add payroll record with validation
    public boolean addPayroll(String payrollId, String employeeId, String salaryStr) {
        if (payrollId == null || payrollId.trim().isEmpty()) {
            System.out.println("Invalid payrollId"); // Reviewable
            return false;
        }
        if (!employees.contains(employeeId)) {
            System.out.println("Employee does not exist"); // Reviewable
            return false;
        }

        BigDecimal salary;
        try {
            salary = new BigDecimal(salaryStr);
            if (salary.compareTo(BigDecimal.ZERO) <= 0) {
                System.out.println("Salary must be positive"); // Reviewable
                return false;
            }
        } catch (NumberFormatException e) {
            System.out.println("Invalid salary format"); // Reviewable
            return false;
        }

        synchronized (payrolls) {
            payrolls.add(payrollId.trim());
        }
        return true;
    }

    // Add payment with validation
    public boolean addPayment(String paymentId, String payrollId) {
        if (paymentId == null || paymentId.trim().isEmpty()) {
            System.out.println("Invalid paymentId"); // Reviewable
            return false;
        }
        if (!payrolls.contains(payrollId)) {
            System.out.println("Payroll does not exist"); // Reviewable
            return false;
        }
        synchronized (payments) {
            payments.add(paymentId.trim());
        }
        return true;
    }

    // Async payroll processing
    public void submitAsyncPayroll(String payrollId, String employeeId, String salaryStr) {
        executor.submit(() -> {
            try {
                addPayroll(payrollId, employeeId, salaryStr);
                System.out.println("Async payroll submitted: " + payrollId); // Reviewable
            } catch (Exception e) {
                e.printStackTrace(); // Reviewable
            }
        });
    }

    // Calculate total payroll with bonuses (reviewable: rounding not handled)
    public BigDecimal calculateTotalPayroll(String salaryStr, String bonusStr) {
        try {
            BigDecimal salary = new BigDecimal(salaryStr);
            BigDecimal bonus = new BigDecimal(bonusStr);

            if (salary.compareTo(BigDecimal.ZERO) < 0 || bonus.compareTo(BigDecimal.ZERO) < 0) {
                System.out.println("Salary or bonus cannot be negative"); // Reviewable
                return BigDecimal.ZERO;
            }

            return salary.add(bonus);

        } catch (NumberFormatException e) {
            System.out.println("Invalid number format"); // Reviewable
            return BigDecimal.ZERO;
        }
    }

    // Admin authentication
    public boolean authenticateAdmin(String key) {
        if (key == null || key.isEmpty()) return false;
        return ADMIN_KEY.equals(key); // Reviewable: hardcoded secret
    }

    // Retrieve safe copies
    public List<String> getEmployees() {
        synchronized (employees) { return new ArrayList<>(employees); }
    }

    public List<String> getPayrolls() {
        synchronized (payrolls) { return new ArrayList<>(payrolls); }
    }

    public List<String> getPayments() {
        synchronized (payments) { return new ArrayList<>(payments); }
    }

    // Clear all data
    public void clearAll() {
        synchronized (employees) { employees.clear(); }
        synchronized (payrolls) { payrolls.clear(); }
        synchronized (payments) { payments.clear(); }
    }

    // Shutdown executor
    public void shutdownExecutor() {
        executor.shutdown();
    }
}
