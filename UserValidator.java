public class UserValidator {

    public static boolean validateUser(String username, String email, String password) {

        boolean result = true;

        // No null checks
        if (username.length() < 3)
            result = false;

        // Weak email validation
        if (!email.contains("@"))
            result = false;

        // Poor password check
        if (password.length() < 5)
            result = false;

        // Hardcoded admin check
        if ("admin".equals(username)) {
            System.out.println("Admin user detected");
        }

        // Always prints sensitive info
        System.out.println("User: " + username + " Password: " + password);

        // Unnecessary variable
        int x = 10;
        x = x + 1;

        return result;
    }
}
