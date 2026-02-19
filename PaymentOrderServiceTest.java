package com.demo.service;

import org.junit.jupiter.api.*;
import java.math.BigDecimal;
import java.util.List;
import java.util.concurrent.*;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for PaymentOrderService
 * Tests cover functionality, concurrency, edge cases, and security issues
 */
public class PaymentOrderServiceTest {

    private PaymentOrderService service;

    @BeforeEach
    void setUp() {
        service = new PaymentOrderService();
    }

    @AfterEach
    void tearDown() {
        service.shutdownExecutor();
    }

    @Nested
    @DisplayName("Add Order Tests")
    class AddOrderTests {
        @Test
        @DisplayName("Test add order with valid parameters")
        void testAddOrderSuccess() {
            boolean result = service.addOrder("order123", "user456");

            assertTrue(result);
            assertTrue(service.getOrders().contains("order123"));
        }

        @Test
        @DisplayName("Test add order with null orderId")
        void testAddOrderNullOrderId() {
            boolean result = service.addOrder(null, "user123");

            assertFalse(result);
            assertEquals(0, service.getOrders().size());
        }

        @Test
        @DisplayName("Test add order with null userId")
        void testAddOrderNullUserId() {
            boolean result = service.addOrder("order123", null);

            assertFalse(result);
            assertEquals(0, service.getOrders().size());
        }

        @Test
        @DisplayName("Test add order with empty orderId")
        void testAddOrderEmptyOrderId() {
            boolean result = service.addOrder("", "user123");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add order with whitespace-only orderId")
        void testAddOrderWhitespaceOrderId() {
            boolean result = service.addOrder("   ", "user123");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add order with empty userId")
        void testAddOrderEmptyUserId() {
            boolean result = service.addOrder("order123", "");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add order with whitespace-only userId")
        void testAddOrderWhitespaceUserId() {
            boolean result = service.addOrder("order123", "   ");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add duplicate order fails")
        void testAddDuplicateOrder() {
            service.addOrder("order123", "user456");
            boolean result = service.addOrder("order123", "user789");

            assertFalse(result);
            assertEquals(1, service.getOrders().size());
        }

        @Test
        @DisplayName("Test add order trims whitespace from orderId")
        void testAddOrderTrimsOrderId() {
            boolean result = service.addOrder("  order123  ", "user456");

            assertTrue(result);
            assertTrue(service.getOrders().contains("order123"));
            assertFalse(service.getOrders().contains("  order123  "));
        }

        @Test
        @DisplayName("Test add multiple orders")
        void testAddMultipleOrders() {
            service.addOrder("order1", "user1");
            service.addOrder("order2", "user2");
            service.addOrder("order3", "user3");

            assertEquals(3, service.getOrders().size());
        }

        @Test
        @DisplayName("Test add order with special characters")
        void testAddOrderWithSpecialCharacters() {
            boolean result = service.addOrder("order@#$%", "user!@#");

            assertTrue(result);
        }

        @Test
        @DisplayName("Test add order with very long IDs")
        void testAddOrderWithLongIds() {
            String longOrderId = "order" + "x".repeat(1000);
            String longUserId = "user" + "y".repeat(1000);

            boolean result = service.addOrder(longOrderId, longUserId);

            assertTrue(result);
        }

        @Test
        @DisplayName("Test add order with unicode characters")
        void testAddOrderWithUnicode() {
            boolean result = service.addOrder("订单123", "用户456");

            assertTrue(result);
        }
    }

    @Nested
    @DisplayName("Add Payment Tests")
    class AddPaymentTests {
        @Test
        @DisplayName("Test add payment with valid order")
        void testAddPaymentSuccess() {
            service.addOrder("order123", "user456");
            boolean result = service.addPayment("payment789", "order123");

            assertTrue(result);
            assertTrue(service.getPayments().contains("payment789"));
        }

        @Test
        @DisplayName("Test add payment with null paymentId")
        void testAddPaymentNullPaymentId() {
            service.addOrder("order123", "user456");
            boolean result = service.addPayment(null, "order123");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add payment with empty paymentId")
        void testAddPaymentEmptyPaymentId() {
            service.addOrder("order123", "user456");
            boolean result = service.addPayment("", "order123");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add payment with whitespace paymentId")
        void testAddPaymentWhitespacePaymentId() {
            service.addOrder("order123", "user456");
            boolean result = service.addPayment("   ", "order123");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add payment for non-existent order")
        void testAddPaymentNonExistentOrder() {
            boolean result = service.addPayment("payment789", "order999");

            assertFalse(result);
            assertEquals(0, service.getPayments().size());
        }

        @Test
        @DisplayName("Test add payment trims paymentId")
        void testAddPaymentTrimsPaymentId() {
            service.addOrder("order123", "user456");
            service.addPayment("  payment789  ", "order123");

            assertTrue(service.getPayments().contains("payment789"));
        }

        @Test
        @DisplayName("Test add multiple payments for same order")
        void testAddMultiplePayments() {
            service.addOrder("order123", "user456");
            service.addPayment("payment1", "order123");
            service.addPayment("payment2", "order123");

            assertEquals(2, service.getPayments().size());
        }

        @Test
        @DisplayName("Test add duplicate payments allowed")
        void testAddDuplicatePayments() {
            service.addOrder("order123", "user456");
            service.addPayment("payment789", "order123");
            service.addPayment("payment789", "order123");

            // Duplicate payments are allowed
            assertEquals(2, service.getPayments().size());
        }

        @Test
        @DisplayName("Test add payment with null orderId")
        void testAddPaymentNullOrderId() {
            service.addOrder("order123", "user456");
            boolean result = service.addPayment("payment789", null);

            assertFalse(result);
        }

        @Test
        @DisplayName("Test add payment before order exists")
        void testAddPaymentBeforeOrder() {
            boolean result = service.addPayment("payment789", "order123");

            assertFalse(result);
        }
    }

    @Nested
    @DisplayName("Get Orders and Payments Tests")
    class GetOrdersAndPaymentsTests {
        @Test
        @DisplayName("Test get orders returns copy")
        void testGetOrdersReturnsCopy() {
            service.addOrder("order123", "user456");
            List<String> orders1 = service.getOrders();
            List<String> orders2 = service.getOrders();

            assertNotSame(orders1, orders2);
        }

        @Test
        @DisplayName("Test get orders returns immutable copy")
        void testGetOrdersReturnsSafeCopy() {
            service.addOrder("order123", "user456");
            List<String> orders = service.getOrders();

            // Modifying returned list doesn't affect internal state
            orders.add("malicious");
            assertEquals(1, service.getOrders().size());
        }

        @Test
        @DisplayName("Test get payments returns copy")
        void testGetPaymentsReturnsCopy() {
            service.addOrder("order123", "user456");
            service.addPayment("payment789", "order123");

            List<String> payments1 = service.getPayments();
            List<String> payments2 = service.getPayments();

            assertNotSame(payments1, payments2);
        }

        @Test
        @DisplayName("Test get payments returns safe copy")
        void testGetPaymentsReturnsSafeCopy() {
            service.addOrder("order123", "user456");
            service.addPayment("payment789", "order123");

            List<String> payments = service.getPayments();
            payments.add("malicious");

            assertEquals(1, service.getPayments().size());
        }

        @Test
        @DisplayName("Test get empty orders")
        void testGetEmptyOrders() {
            List<String> orders = service.getOrders();

            assertNotNull(orders);
            assertEquals(0, orders.size());
        }

        @Test
        @DisplayName("Test get empty payments")
        void testGetEmptyPayments() {
            List<String> payments = service.getPayments();

            assertNotNull(payments);
            assertEquals(0, payments.size());
        }
    }

    @Nested
    @DisplayName("Authentication Tests")
    class AuthenticationTests {
        @Test
        @DisplayName("Test authenticate with correct API key")
        void testAuthenticateSuccess() {
            boolean result = service.authenticate("API-SECRET-98765");

            assertTrue(result);
        }

        @Test
        @DisplayName("Test authenticate with incorrect API key")
        void testAuthenticateIncorrectKey() {
            boolean result = service.authenticate("wrong-key");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test authenticate with null API key")
        void testAuthenticateNullKey() {
            boolean result = service.authenticate(null);

            assertFalse(result);
        }

        @Test
        @DisplayName("Test authenticate with empty API key")
        void testAuthenticateEmptyKey() {
            boolean result = service.authenticate("");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test authenticate is case-sensitive")
        void testAuthenticateCaseSensitive() {
            boolean result = service.authenticate("api-secret-98765");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test authenticate with whitespace in key")
        void testAuthenticateWithWhitespace() {
            boolean result = service.authenticate("API-SECRET-98765 ");

            assertFalse(result);
        }

        @Test
        @DisplayName("Test hardcoded API key vulnerability")
        void testHardcodedApiKeyVulnerability() {
            // Documents security issue: hardcoded API key
            assertTrue(service.authenticate("API-SECRET-98765"));
        }
    }

    @Nested
    @DisplayName("Calculate Total Tests")
    class CalculateTotalTests {
        @Test
        @DisplayName("Test calculate total with valid parameters")
        void testCalculateTotalSuccess() {
            BigDecimal result = service.calculateTotal("100.50", "2");

            assertEquals(new BigDecimal("201.00"), result);
        }

        @Test
        @DisplayName("Test calculate total with decimals")
        void testCalculateTotalWithDecimals() {
            BigDecimal result = service.calculateTotal("10.99", "3");

            assertEquals(new BigDecimal("32.97"), result);
        }

        @Test
        @DisplayName("Test calculate total with negative price returns zero")
        void testCalculateTotalNegativePrice() {
            BigDecimal result = service.calculateTotal("-10", "5");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with negative quantity returns zero")
        void testCalculateTotalNegativeQuantity() {
            BigDecimal result = service.calculateTotal("10", "-5");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with both negative returns zero")
        void testCalculateTotalBothNegative() {
            BigDecimal result = service.calculateTotal("-10", "-5");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with zero price")
        void testCalculateTotalZeroPrice() {
            BigDecimal result = service.calculateTotal("0", "5");

            assertEquals(new BigDecimal("0"), result);
        }

        @Test
        @DisplayName("Test calculate total with zero quantity")
        void testCalculateTotalZeroQuantity() {
            BigDecimal result = service.calculateTotal("10", "0");

            assertEquals(new BigDecimal("0"), result);
        }

        @Test
        @DisplayName("Test calculate total with invalid price format")
        void testCalculateTotalInvalidPrice() {
            BigDecimal result = service.calculateTotal("invalid", "5");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with invalid quantity format")
        void testCalculateTotalInvalidQuantity() {
            BigDecimal result = service.calculateTotal("10", "invalid");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with null price")
        void testCalculateTotalNullPrice() {
            BigDecimal result = service.calculateTotal(null, "5");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with null quantity")
        void testCalculateTotalNullQuantity() {
            BigDecimal result = service.calculateTotal("10", null);

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with empty strings")
        void testCalculateTotalEmptyStrings() {
            BigDecimal result = service.calculateTotal("", "");

            assertEquals(BigDecimal.ZERO, result);
        }

        @Test
        @DisplayName("Test calculate total with very large numbers")
        void testCalculateTotalLargeNumbers() {
            BigDecimal result = service.calculateTotal("999999999.99", "999999999");

            assertTrue(result.compareTo(BigDecimal.ZERO) > 0);
        }

        @Test
        @DisplayName("Test calculate total with many decimal places")
        void testCalculateTotalManyDecimals() {
            BigDecimal result = service.calculateTotal("10.123456789", "2");

            assertNotNull(result);
            assertTrue(result.compareTo(BigDecimal.ZERO) > 0);
        }

        @Test
        @DisplayName("Test calculate total precision")
        void testCalculateTotalPrecision() {
            BigDecimal result = service.calculateTotal("0.1", "3");

            assertEquals(new BigDecimal("0.3"), result);
        }
    }

    @Nested
    @DisplayName("Async Order Tests")
    class AsyncOrderTests {
        @Test
        @DisplayName("Test submit async order")
        void testSubmitAsyncOrder() throws InterruptedException {
            service.submitAsyncOrder("asyncOrder1", "user123");

            // Wait for async operation to complete
            Thread.sleep(100);

            assertTrue(service.getOrders().contains("asyncOrder1"));
        }

        @Test
        @DisplayName("Test submit multiple async orders")
        void testSubmitMultipleAsyncOrders() throws InterruptedException {
            service.submitAsyncOrder("async1", "user1");
            service.submitAsyncOrder("async2", "user2");
            service.submitAsyncOrder("async3", "user3");

            // Wait for async operations
            Thread.sleep(200);

            assertTrue(service.getOrders().size() >= 3);
        }

        @Test
        @DisplayName("Test async order with invalid parameters")
        void testAsyncOrderInvalidParameters() throws InterruptedException {
            service.submitAsyncOrder(null, "user123");

            Thread.sleep(100);

            assertEquals(0, service.getOrders().size());
        }

        @Test
        @DisplayName("Test shutdown executor")
        void testShutdownExecutor() {
            assertDoesNotThrow(() -> service.shutdownExecutor());
        }

        @Test
        @DisplayName("Test multiple shutdown calls")
        void testMultipleShutdownCalls() {
            service.shutdownExecutor();
            assertDoesNotThrow(() -> service.shutdownExecutor());
        }
    }

    @Nested
    @DisplayName("Concurrency Tests")
    class ConcurrencyTests {
        @Test
        @DisplayName("Test concurrent order additions")
        void testConcurrentOrderAdditions() throws InterruptedException {
            int threadCount = 10;
            CountDownLatch latch = new CountDownLatch(threadCount);

            for (int i = 0; i < threadCount; i++) {
                final int index = i;
                new Thread(() -> {
                    service.addOrder("order" + index, "user" + index);
                    latch.countDown();
                }).start();
            }

            latch.await(5, TimeUnit.SECONDS);

            assertEquals(threadCount, service.getOrders().size());
        }

        @Test
        @DisplayName("Test concurrent payment additions")
        void testConcurrentPaymentAdditions() throws InterruptedException {
            service.addOrder("order123", "user456");

            int threadCount = 10;
            CountDownLatch latch = new CountDownLatch(threadCount);

            for (int i = 0; i < threadCount; i++) {
                final int index = i;
                new Thread(() -> {
                    service.addPayment("payment" + index, "order123");
                    latch.countDown();
                }).start();
            }

            latch.await(5, TimeUnit.SECONDS);

            assertEquals(threadCount, service.getPayments().size());
        }

        @Test
        @DisplayName("Test concurrent duplicate order attempts")
        void testConcurrentDuplicateOrders() throws InterruptedException {
            int threadCount = 10;
            CountDownLatch latch = new CountDownLatch(threadCount);

            for (int i = 0; i < threadCount; i++) {
                new Thread(() -> {
                    service.addOrder("sameOrder", "user123");
                    latch.countDown();
                }).start();
            }

            latch.await(5, TimeUnit.SECONDS);

            // Only one should succeed
            assertEquals(1, service.getOrders().size());
        }
    }

    @Nested
    @DisplayName("Integration Tests")
    class IntegrationTests {
        @Test
        @DisplayName("Test complete order and payment flow")
        void testCompleteFlow() {
            // Authenticate
            assertTrue(service.authenticate("API-SECRET-98765"));

            // Add order
            assertTrue(service.addOrder("order123", "user456"));

            // Calculate total
            BigDecimal total = service.calculateTotal("100", "2");
            assertEquals(new BigDecimal("200"), total);

            // Add payment
            assertTrue(service.addPayment("payment789", "order123"));

            // Verify state
            assertEquals(1, service.getOrders().size());
            assertEquals(1, service.getPayments().size());
        }

        @Test
        @DisplayName("Test order without payment")
        void testOrderWithoutPayment() {
            service.addOrder("order123", "user456");

            assertEquals(1, service.getOrders().size());
            assertEquals(0, service.getPayments().size());
        }

        @Test
        @DisplayName("Test multiple orders with multiple payments")
        void testMultipleOrdersAndPayments() {
            service.addOrder("order1", "user1");
            service.addOrder("order2", "user2");

            service.addPayment("payment1", "order1");
            service.addPayment("payment2", "order1");
            service.addPayment("payment3", "order2");

            assertEquals(2, service.getOrders().size());
            assertEquals(3, service.getPayments().size());
        }
    }

    @Nested
    @DisplayName("Edge Cases and Regression Tests")
    class EdgeCasesTests {
        @Test
        @DisplayName("Test order ID with leading/trailing whitespace")
        void testOrderIdWhitespace() {
            service.addOrder("  order123  ", "user456");

            // Should be trimmed
            assertTrue(service.getOrders().contains("order123"));
        }

        @Test
        @DisplayName("Test payment for trimmed order ID")
        void testPaymentForTrimmedOrderId() {
            service.addOrder("  order123  ", "user456");
            boolean result = service.addPayment("payment789", "order123");

            assertTrue(result);
        }

        @Test
        @DisplayName("Test calculate total with scientific notation")
        void testCalculateTotalScientificNotation() {
            BigDecimal result = service.calculateTotal("1.5E2", "2");

            assertTrue(result.compareTo(BigDecimal.ZERO) > 0);
        }

        @Test
        @DisplayName("Test very long order and user IDs")
        void testVeryLongIds() {
            String longId = "x".repeat(10000);
            boolean result = service.addOrder(longId, longId);

            assertTrue(result);
        }

        @Test
        @DisplayName("Test payment ID same as order ID")
        void testPaymentIdSameAsOrderId() {
            service.addOrder("id123", "user456");
            boolean result = service.addPayment("id123", "id123");

            assertTrue(result);
        }
    }
}