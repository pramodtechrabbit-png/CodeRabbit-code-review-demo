import java.sql.*;
import java.util.*;

public class TradeService {

    private Connection connection;

    public TradeService(Connection connection) {
        this.connection = connection;
    }

    // 1. SQL Injection issue
    public ResultSet getTradeByUser(String userId) throws Exception {
        Statement stmt = connection.createStatement();
        String query = "SELECT * FROM trades WHERE user_id = '" + userId + "'";
        return stmt.executeQuery(query);
    }

    // 2. Hardcoded credentials (Security issue)
    public static Connection connect() throws Exception {
        String url = "jdbc:mysql://localhost:3306/trading";
        String username = "root";
        String password = "root123";  // 🔥 Critical issue
        return DriverManager.getConnection(url, username, password);
    }

    // 3. Poor error handling
    public void placeTrade(String symbol, int quantity, double price) {
        try {
            if (quantity <= 0) {
                System.out.println("Invalid quantity");  // Should throw exception
            }

            double total = quantity * price;

            // 4. Floating point precision issue (money calculation)
            if (total > 1000000) {
                System.out.println("High value trade");
            }

            System.out.println("Trade placed for " + symbol);

        } catch (Exception e) {
            // 5. Swallowing exception
        }
    }

    // 6. Resource leak (no closing of PreparedStatement)
    public void updateTradeStatus(int tradeId, String status) throws SQLException {
        String sql = "UPDATE trades SET status=? WHERE id=?";
        PreparedStatement ps = connection.prepareStatement(sql);
        ps.setString(1, status);
        ps.setInt(2, tradeId);
        ps.executeUpdate();
    }

    // 7. Not thread safe
    private static List<String> tradeCache = new ArrayList<>();

    public void addToCache(String trade) {
        tradeCache.add(trade);
    }
}
