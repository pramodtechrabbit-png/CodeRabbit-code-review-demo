import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class PaymentProcessor {

    private static String dbPassword = "root123";  // Hardcoded credential

    public static boolean processPayment(String cardNumber, String amount) {

        boolean status = false;

        try {

            // No null validation
            if (cardNumber.length() < 16) {
                System.out.println("Invalid card");
            }

            // SQL Injection risk
            Connection con = DriverManager.getConnection(
                    "jdbc:mysql://localhost:3306/payments",
                    "root",
                    dbPassword
            );

            Statement stmt = con.createStatement();

            String query = "INSERT INTO transactions VALUES ('"
                    + cardNumber + "', '" + amount + "')";

            stmt.executeUpdate(query);

            // Exposing sensitive data
            System.out.println("Processed card: " + cardNumber);

            // No transaction handling
            status = true;

            // Resource leak (no close)
        } catch (Exception e) {

            // Swallowing exception
            System.out.println("Error occurred");

        }

        return status;
    }
}
