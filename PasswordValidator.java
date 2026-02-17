public class PasswordValidator {

    /**
     * Validate that a password meets defined strength and character rules.
     *
     * <p>The password must be at least 8 characters long, contain at least one
     * lowercase letter, one uppercase letter, one digit, and one special character
     * from the set {@code @$!%*?&}. Only letters, digits, and those special
     * characters are allowed.
     *
     * @param password the password to validate; may be {@code null} or blank (null or blank returns {@code false})
     * @return {@code true} if the password satisfies the length, character-class, and allowed-character constraints, {@code false} otherwise
     */
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