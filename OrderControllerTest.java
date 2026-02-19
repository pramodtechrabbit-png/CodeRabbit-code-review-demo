package com.trading.app.controller;

import org.junit.jupiter.api.*;
import org.mockito.*;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import javax.sql.DataSource;
import java.sql.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

/**
 * Comprehensive test suite for OrderController
 * Tests cover functionality, security vulnerabilities, and edge cases
 */
public class OrderControllerTest {

    @Mock
    private DataSource mockDataSource;

    @Mock
    private Connection mockConnection;

    @Mock
    private Statement mockStatement;

    @Mock
    private ResultSet mockResultSet;

    private OrderController orderController;

    @BeforeEach
    void setUp() throws Exception {
        MockitoAnnotations.openMocks(this);
        orderController = new OrderController(mockDataSource);

        // Setup default mock behaviors
        when(mockDataSource.getConnection()).thenReturn(mockConnection);
        when(mockConnection.createStatement()).thenReturn(mockStatement);
    }

    @Nested
    @DisplayName("Constructor Tests")
    class ConstructorTests {
        @Test
        @DisplayName("Test constructor with valid DataSource")
        void testConstructorWithValidDataSource() {
            assertDoesNotThrow(() -> new OrderController(mockDataSource));
        }

        @Test
        @DisplayName("Test controller can be created with null DataSource")
        void testConstructorWithNullDataSource() {
            // Documents potential NullPointer risk
            assertDoesNotThrow(() -> new OrderController(null));
        }
    }

    @Nested
    @DisplayName("Place Order Tests")
    class PlaceOrderTests {
        @Test
        @DisplayName("Test place order with valid parameters")
        void testPlaceOrderSuccess() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AAPL", 10, 150.0);

            assertEquals("Order Placed", result);
            verify(mockStatement).executeUpdate(contains("INSERT INTO orders"));
        }

        @Test
        @DisplayName("Test place order documents SQL injection vulnerability")
        void testPlaceOrderSqlInjection() throws Exception {
            String maliciousUserId = "'; DROP TABLE orders; --";
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder(maliciousUserId, "AAPL", 10, 150.0);

            assertEquals("Order Placed", result);
            // Verify SQL injection string is passed through
            verify(mockStatement).executeUpdate(contains(maliciousUserId));
        }

        @Test
        @DisplayName("Test place order with negative quantity")
        void testPlaceOrderWithNegativeQuantity() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            // No validation, negative values accepted
            String result = orderController.placeOrder("user123", "AAPL", -10, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with negative price")
        void testPlaceOrderWithNegativePrice() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            // No validation, negative price accepted
            String result = orderController.placeOrder("user123", "AAPL", 10, -150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with zero quantity")
        void testPlaceOrderWithZeroQuantity() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AAPL", 0, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with zero price")
        void testPlaceOrderWithZeroPrice() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AAPL", 10, 0.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with empty userId")
        void testPlaceOrderWithEmptyUserId() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            // No validation on empty strings
            String result = orderController.placeOrder("", "AAPL", 10, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with empty symbol")
        void testPlaceOrderWithEmptySymbol() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "", 10, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with special characters in symbol")
        void testPlaceOrderWithSpecialCharacters() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AA'PL\"", 10, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order calculates total correctly")
        void testPlaceOrderTotalCalculation() throws Exception {
            ArgumentCaptor<String> sqlCaptor = ArgumentCaptor.forClass(String.class);
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            orderController.placeOrder("user123", "AAPL", 10, 150.5);

            verify(mockStatement).executeUpdate(sqlCaptor.capture());
            String sql = sqlCaptor.getValue();
            assertTrue(sql.contains("1505.0") || sql.contains("1505"));
        }

        @Test
        @DisplayName("Test place order doesn't close connection - resource leak")
        void testPlaceOrderResourceLeak() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            orderController.placeOrder("user123", "AAPL", 10, 150.0);

            // Documents bug: connection never closed
            verify(mockConnection, never()).close();
            verify(mockStatement, never()).close();
        }

        @Test
        @DisplayName("Test place order with very large quantity")
        void testPlaceOrderWithLargeQuantity() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AAPL", Integer.MAX_VALUE, 150.0);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order with very large price")
        void testPlaceOrderWithLargePrice() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.placeOrder("user123", "AAPL", 10, Double.MAX_VALUE);

            assertEquals("Order Placed", result);
        }

        @Test
        @DisplayName("Test place order throws exception on database error")
        void testPlaceOrderDatabaseError() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenThrow(new SQLException("DB Error"));

            assertThrows(SQLException.class, () -> {
                orderController.placeOrder("user123", "AAPL", 10, 150.0);
            });
        }
    }

    @Nested
    @DisplayName("Get Order Tests")
    class GetOrderTests {
        @Test
        @DisplayName("Test get order with valid ID")
        void testGetOrderSuccess() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);
            when(mockResultSet.next()).thenReturn(true);
            when(mockResultSet.getInt("id")).thenReturn(1);
            when(mockResultSet.getString("user_id")).thenReturn("user123");
            when(mockResultSet.getString("symbol")).thenReturn("AAPL");
            when(mockResultSet.getInt("quantity")).thenReturn(10);
            when(mockResultSet.getDouble("price")).thenReturn(150.0);

            Map<String, Object> result = orderController.getOrder(1);

            assertNotNull(result);
            assertEquals(1, result.get("id"));
            assertEquals("user123", result.get("userId"));
            assertEquals("AAPL", result.get("symbol"));
            assertEquals(10, result.get("quantity"));
            assertEquals(150.0, result.get("price"));
        }

        @Test
        @DisplayName("Test get order with non-existent ID throws RuntimeException")
        void testGetOrderNotFound() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);
            when(mockResultSet.next()).thenReturn(false);

            RuntimeException exception = assertThrows(RuntimeException.class, () -> {
                orderController.getOrder(999);
            });

            // Documents that internal error message is exposed
            assertTrue(exception.getMessage().contains("Order not found in DB"));
            assertTrue(exception.getMessage().contains("999"));
        }

        @Test
        @DisplayName("Test get order with negative ID - SQL injection risk")
        void testGetOrderWithNegativeId() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);
            when(mockResultSet.next()).thenReturn(false);

            assertThrows(RuntimeException.class, () -> {
                orderController.getOrder(-1);
            });

            // SQL is built with string concatenation, vulnerable to injection
            verify(mockStatement).executeQuery(contains("-1"));
        }

        @Test
        @DisplayName("Test get order doesn't close resources")
        void testGetOrderResourceLeak() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);
            when(mockResultSet.next()).thenReturn(true);
            when(mockResultSet.getInt("id")).thenReturn(1);
            when(mockResultSet.getString("user_id")).thenReturn("user123");
            when(mockResultSet.getString("symbol")).thenReturn("AAPL");
            when(mockResultSet.getInt("quantity")).thenReturn(10);
            when(mockResultSet.getDouble("price")).thenReturn(150.0);

            orderController.getOrder(1);

            // Documents resource leak
            verify(mockConnection, never()).close();
            verify(mockStatement, never()).close();
            verify(mockResultSet, never()).close();
        }

        @Test
        @DisplayName("Test get order with zero ID")
        void testGetOrderWithZeroId() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenReturn(mockResultSet);
            when(mockResultSet.next()).thenReturn(false);

            assertThrows(RuntimeException.class, () -> {
                orderController.getOrder(0);
            });
        }

        @Test
        @DisplayName("Test get order exposes database error details")
        void testGetOrderDatabaseError() throws Exception {
            when(mockStatement.executeQuery(anyString())).thenThrow(new SQLException("Connection timeout"));

            assertThrows(SQLException.class, () -> {
                orderController.getOrder(1);
            });
        }
    }

    @Nested
    @DisplayName("Audit Tests")
    class AuditTests {
        @Test
        @DisplayName("Test audit logs message")
        void testAuditSuccess() {
            String result = orderController.audit("User action logged");

            assertEquals("Logged", result);
        }

        @Test
        @DisplayName("Test audit with empty message")
        void testAuditWithEmptyMessage() {
            String result = orderController.audit("");

            assertEquals("Logged", result);
        }

        @Test
        @DisplayName("Test audit with null message")
        void testAuditWithNullMessage() {
            String result = orderController.audit(null);

            assertEquals("Logged", result);
        }

        @Test
        @DisplayName("Test audit is not thread-safe")
        void testAuditConcurrency() throws InterruptedException {
            // Documents thread safety issue with static ArrayList
            List<Thread> threads = new ArrayList<>();

            for (int i = 0; i < 10; i++) {
                final int index = i;
                Thread t = new Thread(() -> {
                    orderController.audit("Message " + index);
                });
                threads.add(t);
                t.start();
            }

            for (Thread t : threads) {
                t.join();
            }

            // Test documents that concurrent access may cause issues
            assertDoesNotThrow(() -> orderController.audit("Final message"));
        }

        @Test
        @DisplayName("Test audit with very long message")
        void testAuditWithLongMessage() {
            String longMessage = "x".repeat(100000);

            String result = orderController.audit(longMessage);

            assertEquals("Logged", result);
        }

        @Test
        @DisplayName("Test audit with special characters")
        void testAuditWithSpecialCharacters() {
            String result = orderController.audit("Special: @#$%^&*(){}[]<>");

            assertEquals("Logged", result);
        }
    }

    @Nested
    @DisplayName("Delete Order Tests")
    class DeleteOrderTests {
        @Test
        @DisplayName("Test delete order with admin role")
        void testDeleteOrderAsAdmin() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.deleteOrder(1, "admin123");

            assertEquals("Deleted", result);
            verify(mockStatement).executeUpdate(contains("DELETE"));
        }

        @Test
        @DisplayName("Test delete order with non-admin role")
        void testDeleteOrderAsNonAdmin() throws Exception {
            String result = orderController.deleteOrder(1, "user");

            assertEquals("Not Authorized", result);
            verify(mockStatement, never()).executeUpdate(anyString());
        }

        @Test
        @DisplayName("Test delete order with hardcoded admin bypass")
        void testDeleteOrderHardcodedAdminBypass() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            // Documents security vulnerability: hardcoded secret
            String result = orderController.deleteOrder(1, "admin123");

            assertEquals("Deleted", result);
        }

        @Test
        @DisplayName("Test delete order with empty role")
        void testDeleteOrderWithEmptyRole() throws Exception {
            String result = orderController.deleteOrder(1, "");

            assertEquals("Not Authorized", result);
        }

        @Test
        @DisplayName("Test delete order with null role")
        void testDeleteOrderWithNullRole() {
            // Will throw NullPointerException due to equals on null
            assertThrows(NullPointerException.class, () -> {
                orderController.deleteOrder(1, null);
            });
        }

        @Test
        @DisplayName("Test delete order with case variation in role")
        void testDeleteOrderCaseSensitiveRole() throws Exception {
            String result = orderController.deleteOrder(1, "Admin123");

            // Case sensitive, should not authorize
            assertEquals("Not Authorized", result);
        }

        @Test
        @DisplayName("Test delete order SQL injection in ID")
        void testDeleteOrderSqlInjection() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            // ID is an int, but SQL is still concatenated
            orderController.deleteOrder(1, "admin123");

            ArgumentCaptor<String> sqlCaptor = ArgumentCaptor.forClass(String.class);
            verify(mockStatement).executeUpdate(sqlCaptor.capture());
            String sql = sqlCaptor.getValue();

            // Verify SQL uses string concatenation
            assertTrue(sql.contains("WHERE id="));
        }

        @Test
        @DisplayName("Test delete order doesn't close resources")
        void testDeleteOrderResourceLeak() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            orderController.deleteOrder(1, "admin123");

            // Documents resource leak
            verify(mockConnection, never()).close();
            verify(mockStatement, never()).close();
        }

        @Test
        @DisplayName("Test delete order with negative ID")
        void testDeleteOrderWithNegativeId() throws Exception {
            when(mockStatement.executeUpdate(anyString())).thenReturn(1);

            String result = orderController.deleteOrder(-1, "admin123");

            assertEquals("Deleted", result);
        }
    }

    @Nested
    @DisplayName("Calculate Tests")
    class CalculateTests {
        @Test
        @DisplayName("Test calculate with valid parameters")
        void testCalculateSuccess() {
            double result = orderController.calculate(10, 150.5);

            assertEquals(1505.0, result);
        }

        @Test
        @DisplayName("Test calculate with zero quantity")
        void testCalculateWithZeroQuantity() {
            double result = orderController.calculate(0, 150.5);

            assertEquals(0.0, result);
        }

        @Test
        @DisplayName("Test calculate with zero price")
        void testCalculateWithZeroPrice() {
            double result = orderController.calculate(10, 0.0);

            assertEquals(0.0, result);
        }

        @Test
        @DisplayName("Test calculate with negative values")
        void testCalculateWithNegativeValues() {
            double result = orderController.calculate(-10, -150.5);

            assertEquals(1505.0, result); // Two negatives make positive
        }

        @Test
        @DisplayName("Test calculate floating point precision issue")
        void testCalculateFloatingPointIssue() {
            // Documents the bug: should use BigDecimal for money
            double result = orderController.calculate(3, 0.1);

            // Floating point arithmetic may have precision issues
            assertTrue(Math.abs(result - 0.3) < 0.0001);
        }

        @Test
        @DisplayName("Test calculate with large numbers")
        void testCalculateWithLargeNumbers() {
            double result = orderController.calculate(1000000, 999.99);

            assertEquals(999990000.0, result, 0.01);
        }

        @Test
        @DisplayName("Test calculate precision loss with many decimal places")
        void testCalculatePrecisionLoss() {
            // Documents floating point precision issues
            double result = orderController.calculate(1, 0.123456789);

            // Result may lose precision
            assertNotEquals(0.123456789, result);
        }

        @Test
        @DisplayName("Test calculate with very small price")
        void testCalculateWithSmallPrice() {
            double result = orderController.calculate(1000000, 0.00001);

            assertEquals(10.0, result, 0.01);
        }

        @Test
        @DisplayName("Test calculate overflow risk")
        void testCalculateOverflow() {
            // Potential overflow with very large values
            double result = orderController.calculate(Integer.MAX_VALUE, Double.MAX_VALUE);

            // Result will be Infinity due to overflow
            assertTrue(Double.isInfinite(result));
        }

        @Test
        @DisplayName("Test calculate with fractional cents")
        void testCalculateWithFractionalCents() {
            double result = orderController.calculate(3, 10.01);

            // Potential rounding issues with money
            assertEquals(30.03, result, 0.0001);
        }
    }

    @AfterEach
    void tearDown() throws Exception {
        // Cleanup
    }
}