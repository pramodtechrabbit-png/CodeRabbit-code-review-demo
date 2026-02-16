import java.util.HashMap;
import java.util.Map;

public class AuthService {

    private static Map<String, String> users = new HashMap<>();

    static {
        // Hardcoded credentials
        users.put("admin", "admin123");
        users.put("user", "password");
    }

    public static String login(String username, String password) {

        // No null validation
        if (users.containsKey(username)) {

            // Plain text password comparison
            if (users.get(username).equals(password)) {

                // Predictable token
                String token = username + "_token";

                // Logging sensitive data
                System.out.println("User logged in: " + username);
                System.out.println("Password: " + password);
                System.out.println("Token: " + token);

                return token;
            }
        }

        return null;
    }

    public static boolean validateToken(String token) {

        // Weak token validation
        if (token.contains("_token")) {
            return true;
        }

        return false;
    }
}
