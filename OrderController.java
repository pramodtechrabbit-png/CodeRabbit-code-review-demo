package com.trading.app.controller;

import org.springframework.web.bind.annotation.*;
import java.util.*;
import java.sql.*;
import javax.sql.DataSource;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private DataSource dataSource;

    // 1️⃣ Field injection missing (NullPointer risk)
    public OrderController(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    // 2️⃣ No authentication / authorization
    @PostMapping("/place")
    public String placeOrder(@RequestParam String userId,
                             @RequestParam String symbol,
                             @RequestParam int quantity,
                             @RequestParam double price) throws Exception {

        // 3️⃣ No input validation
        double total = quantity * price;

        Connection conn = dataSource.getConnection();

        // 4️⃣ SQL Injection
        String sql = "INSERT INTO orders(user_id,symbol,quantity,price,total) VALUES('"
                + userId + "','" + symbol + "',"
                + quantity + "," + price + "," + total + ")";

        Statement stmt = conn.createStatement();
        stmt.executeUpdate(sql);

        // 5️⃣ No transaction handling

        // 6️⃣ Resource leak (connection not closed)

        return "Order Placed";
    }

    // 7️⃣ Exposing internal error
    @GetMapping("/{id}")
    public Map<String, Object> getOrder(@PathVariable int id) throws Exception {

        Connection conn = dataSource.getConnection();
        Statement stmt = conn.createStatement();

        ResultSet rs = stmt.executeQuery("SELECT * FROM orders WHERE id=" + id);

        if (!rs.next()) {
            throw new RuntimeException("Order not found in DB with ID: " + id);
        }

        Map<String, Object> response = new HashMap<>();
        response.put("id", rs.getInt("id"));
        response.put("userId", rs.getString("user_id"));
        response.put("symbol", rs.getString("symbol"));
        response.put("quantity", rs.getInt("quantity"));
        response.put("price", rs.getDouble("price"));

        return response;
    }

    // 8️⃣ Not thread safe shared state
    private static List<String> auditLog = new ArrayList<>();

    @PostMapping("/audit")
    public String audit(@RequestBody String message) {
        auditLog.add(message);
        return "Logged";
    }

    // 9️⃣ Hardcoded admin bypass
    @DeleteMapping("/delete/{id}")
    public String deleteOrder(@PathVariable int id,
                              @RequestParam String role) throws Exception {

        if (role.equals("admin123")) {  // 🚨 Hardcoded secret
            Connection conn = dataSource.getConnection();
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("DELETE FROM orders WHERE id=" + id);
            return "Deleted";
        }

        return "Not Authorized";
    }

    // 🔟 Floating point issue for money
    @GetMapping("/calculate")
    public double calculate(@RequestParam int quantity,
                            @RequestParam double price) {

        return quantity * price; // Should use BigDecimal
    }
}
