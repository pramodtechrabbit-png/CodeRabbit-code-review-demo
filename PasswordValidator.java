public class PasswordValidator {

    public static boolean isValidPassword(String password) {

        if (password == null || password.trim().isEmpty()) {
            return false;
        }

        // Minimum 8 characters,
        // At least one uppercase letter,
        // One lowercase letter,
        // One digit,
        // One special character
        String passwordRegex = 
            "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$";

        return password.matches(passwordRegex);
    }
}
