package com.trading.engine;

import java.util.*;
import java.util.concurrent.*;
import org.apache.kafka.clients.consumer.*;
import java.time.Duration;

public class TradeProcessor {

    private static final Object lock1 = new Object();
    private static final Object lock2 = new Object();

    private static List<String> tradeCache = new ArrayList<>();
    private KafkaConsumer<String, String> consumer;

    public TradeProcessor(KafkaConsumer<String, String> consumer) {
        this.consumer = consumer;
    }

    // 1️⃣ Deadlock Risk
    public void processTrade(String tradeId) {
        synchronized (lock1) {
            synchronized (lock2) {
                System.out.println("Processing trade: " + tradeId);
            }
        }
    }

    public void reverseProcess(String tradeId) {
        synchronized (lock2) {
            synchronized (lock1) {  // Opposite lock order → Deadlock
                System.out.println("Reversing trade: " + tradeId);
            }
        }
    }

    // 2️⃣ Memory Leak (Unbounded List)
    public void cacheTrade(String trade) {
        tradeCache.add(trade);
    }

    // 3️⃣ Not Thread Safe
    public void clearCache() {
        tradeCache.clear();
    }

    // 4️⃣ Kafka Offset Commit Problem
    public void startConsumer() {
        consumer.subscribe(Arrays.asList("trades-topic"));

        while (true) {  // 5️⃣ Infinite loop without shutdown handling
            ConsumerRecords<String, String> records =
                    consumer.poll(Duration.ofMillis(100));

            for (ConsumerRecord<String, String> record : records) {

                // 6️⃣ No validation
                String value = record.value();

                // 7️⃣ Possible NullPointerException
                if (value.contains("BUY")) {
                    cacheTrade(value);
                }

                // 8️⃣ Commit before processing success
                consumer.commitSync();
            }
        }
    }

    // 9️⃣ Floating point for money
    public double calculatePnL(double buyPrice, double sellPrice, int quantity) {
        return (sellPrice - buyPrice) * quantity;
    }

    // 🔟 Blocking call inside async executor
    public void asyncProcess() {
        ExecutorService executor = Executors.newFixedThreadPool(5);

        executor.submit(() -> {
            try {
                Thread.sleep(10000); // Blocking call
                System.out.println("Async task done");
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });

        // 1️⃣1️⃣ Executor never shutdown → Thread leak
    }

    // 1️⃣2️⃣ No error handling for Kafka consumer
}
