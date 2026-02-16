import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for PasswordValidator class.
 *
 * Tests cover:
 * - Valid password scenarios
 * - Invalid password scenarios (missing requirements)
 * - Edge cases (null, empty, whitespace)
 * - Boundary conditions (length limits)
 * - Special character validation
 * - Regression scenarios
 */
public class PasswordValidatorTest {

    // Valid Password Tests

    @Test
    @DisplayName("Should accept valid password with all requirements")
    public void testValidPasswordWithAllRequirements() {
        assertTrue(PasswordValidator.isValidPassword("Abcdef1@"));
    }

    @Test
    @DisplayName("Should accept valid password with minimum length")
    public void testValidPasswordMinimumLength() {
        assertTrue(PasswordValidator.isValidPassword("Abc123!@"));
    }

    @Test
    @DisplayName("Should accept valid password with multiple special characters")
    public void testValidPasswordMultipleSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Test123!@#$%"));
    }

    @Test
    @DisplayName("Should accept valid password with all allowed special characters")
    public void testValidPasswordAllSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Pass123@$!%*?&"));
    }

    @Test
    @DisplayName("Should accept valid password longer than minimum")
    public void testValidPasswordLongerThanMinimum() {
        assertTrue(PasswordValidator.isValidPassword("MySecurePassword123!"));
    }

    @Test
    @DisplayName("Should accept valid password with multiple uppercase letters")
    public void testValidPasswordMultipleUppercase() {
        assertTrue(PasswordValidator.isValidPassword("ABCD123efg!"));
    }

    @Test
    @DisplayName("Should accept valid password with multiple lowercase letters")
    public void testValidPasswordMultipleLowercase() {
        assertTrue(PasswordValidator.isValidPassword("ABCabc123!"));
    }

    @Test
    @DisplayName("Should accept valid password with multiple digits")
    public void testValidPasswordMultipleDigits() {
        assertTrue(PasswordValidator.isValidPassword("Test123456!"));
    }

    // Null and Empty Tests

    @Test
    @DisplayName("Should reject null password")
    public void testNullPassword() {
        assertFalse(PasswordValidator.isValidPassword(null));
    }

    @Test
    @DisplayName("Should reject empty password")
    public void testEmptyPassword() {
        assertFalse(PasswordValidator.isValidPassword(""));
    }

    @Test
    @DisplayName("Should reject whitespace-only password")
    public void testWhitespaceOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("   "));
    }

    @Test
    @DisplayName("Should reject tab-only password")
    public void testTabOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("\t\t\t"));
    }

    @Test
    @DisplayName("Should reject newline-only password")
    public void testNewlineOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("\n\n"));
    }

    @Test
    @DisplayName("Should reject mixed whitespace password")
    public void testMixedWhitespacePassword() {
        assertFalse(PasswordValidator.isValidPassword(" \t\n "));
    }

    // Length Requirement Tests

    @Test
    @DisplayName("Should reject password with 7 characters (one below minimum)")
    public void testPasswordTooShort() {
        assertFalse(PasswordValidator.isValidPassword("Abc12!@"));
    }

    @Test
    @DisplayName("Should reject password with 6 characters")
    public void testPasswordSixChars() {
        assertFalse(PasswordValidator.isValidPassword("Ab12!@"));
    }

    @Test
    @DisplayName("Should reject password with 5 characters")
    public void testPasswordFiveChars() {
        assertFalse(PasswordValidator.isValidPassword("Ab12!"));
    }

    @Test
    @DisplayName("Should reject single character password")
    public void testPasswordSingleChar() {
        assertFalse(PasswordValidator.isValidPassword("A"));
    }

    // Missing Uppercase Tests

    @Test
    @DisplayName("Should reject password without uppercase letter")
    public void testPasswordWithoutUppercase() {
        assertFalse(PasswordValidator.isValidPassword("abcdef1@"));
    }

    @Test
    @DisplayName("Should reject long password without uppercase")
    public void testLongPasswordWithoutUppercase() {
        assertFalse(PasswordValidator.isValidPassword("thisisaverylongpassword123!"));
    }

    // Missing Lowercase Tests

    @Test
    @DisplayName("Should reject password without lowercase letter")
    public void testPasswordWithoutLowercase() {
        assertFalse(PasswordValidator.isValidPassword("ABCDEF1@"));
    }

    @Test
    @DisplayName("Should reject long password without lowercase")
    public void testLongPasswordWithoutLowercase() {
        assertFalse(PasswordValidator.isValidPassword("THISISAVERYLONGPASSWORD123!"));
    }

    // Missing Digit Tests

    @Test
    @DisplayName("Should reject password without digit")
    public void testPasswordWithoutDigit() {
        assertFalse(PasswordValidator.isValidPassword("Abcdefgh!"));
    }

    @Test
    @DisplayName("Should reject long password without digit")
    public void testLongPasswordWithoutDigit() {
        assertFalse(PasswordValidator.isValidPassword("ThisIsALongPassword!@#$"));
    }

    // Missing Special Character Tests

    @Test
    @DisplayName("Should reject password without special character")
    public void testPasswordWithoutSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef123"));
    }

    @Test
    @DisplayName("Should reject long password without special character")
    public void testLongPasswordWithoutSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("ThisIsALongPassword123"));
    }

    // Invalid Special Character Tests

    @Test
    @DisplayName("Should reject password with hashtag (not in allowed set)")
    public void testPasswordWithHashtag() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1#"));
    }

    @Test
    @DisplayName("Should reject password with plus sign (not in allowed set)")
    public void testPasswordWithPlusSign() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1+"));
    }

    @Test
    @DisplayName("Should reject password with equals sign (not in allowed set)")
    public void testPasswordWithEqualsSign() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1="));
    }

    @Test
    @DisplayName("Should reject password with caret (not in allowed set)")
    public void testPasswordWithCaret() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1^"));
    }

    @Test
    @DisplayName("Should reject password with tilde (not in allowed set)")
    public void testPasswordWithTilde() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1~"));
    }

    @Test
    @DisplayName("Should reject password with underscore (not in allowed set)")
    public void testPasswordWithUnderscore() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1_"));
    }

    @Test
    @DisplayName("Should reject password with hyphen (not in allowed set)")
    public void testPasswordWithHyphen() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1-"));
    }

    @Test
    @DisplayName("Should reject password with pipe (not in allowed set)")
    public void testPasswordWithPipe() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1|"));
    }

    @Test
    @DisplayName("Should reject password with backslash (not in allowed set)")
    public void testPasswordWithBackslash() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1\\"));
    }

    @Test
    @DisplayName("Should reject password with square brackets (not in allowed set)")
    public void testPasswordWithSquareBrackets() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1[]"));
    }

    @Test
    @DisplayName("Should reject password with curly braces (not in allowed set)")
    public void testPasswordWithCurlyBraces() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1{}"));
    }

    @Test
    @DisplayName("Should reject password with parentheses (not in allowed set)")
    public void testPasswordWithParentheses() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1()"));
    }

    // Whitespace Within Password Tests

    @Test
    @DisplayName("Should reject password with spaces in middle")
    public void testPasswordWithSpacesInMiddle() {
        assertFalse(PasswordValidator.isValidPassword("Abc def1@"));
    }

    @Test
    @DisplayName("Should reject password with leading space")
    public void testPasswordWithLeadingSpace() {
        assertFalse(PasswordValidator.isValidPassword(" Abcdef1@"));
    }

    @Test
    @DisplayName("Should reject password with trailing space")
    public void testPasswordWithTrailingSpace() {
        assertFalse(PasswordValidator.isValidPassword("Abcdef1@ "));
    }

    @Test
    @DisplayName("Should reject password with tab character")
    public void testPasswordWithTabCharacter() {
        assertFalse(PasswordValidator.isValidPassword("Abc\tdef1@"));
    }

    // Combined Missing Requirements Tests

    @Test
    @DisplayName("Should reject password missing uppercase and digit")
    public void testPasswordMissingUppercaseAndDigit() {
        assertFalse(PasswordValidator.isValidPassword("abcdefgh!"));
    }

    @Test
    @DisplayName("Should reject password missing uppercase and special char")
    public void testPasswordMissingUppercaseAndSpecial() {
        assertFalse(PasswordValidator.isValidPassword("abcdef123"));
    }

    @Test
    @DisplayName("Should reject password missing lowercase and digit")
    public void testPasswordMissingLowercaseAndDigit() {
        assertFalse(PasswordValidator.isValidPassword("ABCDEFGH!"));
    }

    @Test
    @DisplayName("Should reject password with only letters")
    public void testPasswordOnlyLetters() {
        assertFalse(PasswordValidator.isValidPassword("AbCdEfGh"));
    }

    @Test
    @DisplayName("Should reject password with only digits and special chars")
    public void testPasswordOnlyDigitsAndSpecial() {
        assertFalse(PasswordValidator.isValidPassword("12345678!@"));
    }

    // Boundary and Edge Case Tests

    @Test
    @DisplayName("Should accept password with exactly 8 characters")
    public void testPasswordExactlyEightChars() {
        assertTrue(PasswordValidator.isValidPassword("Abcd123!"));
    }

    @Test
    @DisplayName("Should accept password with 9 characters")
    public void testPasswordNineChars() {
        assertTrue(PasswordValidator.isValidPassword("Abcd123!@"));
    }

    @Test
    @DisplayName("Should accept very long valid password")
    public void testVeryLongValidPassword() {
        assertTrue(PasswordValidator.isValidPassword("ThisIsAVeryLongSecurePassword123!@#$%"));
    }

    @Test
    @DisplayName("Should accept password with 100 characters")
    public void testPasswordHundredChars() {
        // Create a 100-char valid password
        StringBuilder sb = new StringBuilder("Abc123!");
        for (int i = 0; i < 93; i++) {
            sb.append("a");
        }
        assertTrue(PasswordValidator.isValidPassword(sb.toString()));
    }

    // Parameterized Tests for Valid Passwords

    @ParameterizedTest
    @ValueSource(strings = {
        "Password1!",
        "MyP@ssw0rd",
        "Test123$",
        "Valid&Pass1",
        "Str0ng*Pass",
        "Secure?123A",
        "Complex%Pass1",
        "Good@Pass123",
        "UPPER123lower!",
        "MixedCase123@"
    })
    @DisplayName("Should accept various valid password formats")
    public void testVariousValidPasswords(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    // Parameterized Tests for Invalid Passwords

    @ParameterizedTest
    @ValueSource(strings = {
        "short1!",       // Too short
        "nocaps123!",    // No uppercase
        "NOLOWER123!",   // No lowercase
        "NoDigits!@#",   // No digits
        "NoSpecial123",  // No special char
        "abc",           // Too short, no uppercase, no digit, no special
        "12345678",      // No letters, no special
        "!@#$%^&*",      // No letters, no digits
        "Abcdefgh",      // No digit, no special
        "ABCDEFGH"       // No lowercase, no digit, no special
    })
    @DisplayName("Should reject various invalid password formats")
    public void testVariousInvalidPasswords(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    // Special Character Coverage Tests

    @Test
    @DisplayName("Should accept password with @ symbol")
    public void testPasswordWithAtSymbol() {
        assertTrue(PasswordValidator.isValidPassword("Test123@abc"));
    }

    @Test
    @DisplayName("Should accept password with $ symbol")
    public void testPasswordWithDollarSymbol() {
        assertTrue(PasswordValidator.isValidPassword("Test123$abc"));
    }

    @Test
    @DisplayName("Should accept password with ! symbol")
    public void testPasswordWithExclamation() {
        assertTrue(PasswordValidator.isValidPassword("Test123!abc"));
    }

    @Test
    @DisplayName("Should accept password with % symbol")
    public void testPasswordWithPercent() {
        assertTrue(PasswordValidator.isValidPassword("Test123%abc"));
    }

    @Test
    @DisplayName("Should accept password with * symbol")
    public void testPasswordWithAsterisk() {
        assertTrue(PasswordValidator.isValidPassword("Test123*abc"));
    }

    @Test
    @DisplayName("Should accept password with ? symbol")
    public void testPasswordWithQuestionMark() {
        assertTrue(PasswordValidator.isValidPassword("Test123?abc"));
    }

    @Test
    @DisplayName("Should accept password with & symbol")
    public void testPasswordWithAmpersand() {
        assertTrue(PasswordValidator.isValidPassword("Test123&abc"));
    }

    // Regression Tests

    @Test
    @DisplayName("Regression: Password that looks valid but has disallowed special char")
    public void testRegressionDisallowedSpecialChar() {
        // Has all requirements but uses # instead of allowed special chars
        assertFalse(PasswordValidator.isValidPassword("Password123#"));
    }

    @Test
    @DisplayName("Regression: Password with leading/trailing spaces after trim should fail")
    public void testRegressionPasswordWithWhitespacePadding() {
        // Even though trim() is called, spaces within password make it invalid
        assertFalse(PasswordValidator.isValidPassword("  Abcdef1@  "));
    }

    @Test
    @DisplayName("Regression: Minimum length counted correctly with special chars")
    public void testRegressionMinimumLengthWithSpecialChars() {
        // Exactly 8 chars with all requirements
        assertTrue(PasswordValidator.isValidPassword("Aa1@bcde"));
        // 7 chars should fail
        assertFalse(PasswordValidator.isValidPassword("Aa1@bcd"));
    }

    @Test
    @DisplayName("Regression: Multiple special characters don't bypass other requirements")
    public void testRegressionMultipleSpecialCharsDontBypass() {
        // Has special chars but missing uppercase
        assertFalse(PasswordValidator.isValidPassword("abc123!@#$%"));
        // Has special chars but missing lowercase
        assertFalse(PasswordValidator.isValidPassword("ABC123!@#$%"));
        // Has special chars but missing digits
        assertFalse(PasswordValidator.isValidPassword("Abcdef!@#$%"));
    }

    @Test
    @DisplayName("Regression: Single character from each category at exact minimum")
    public void testRegressionSingleCharEachCategory() {
        assertTrue(PasswordValidator.isValidPassword("Aa1@aaaa"));
    }

    @Test
    @DisplayName("Regression: Unicode characters are rejected")
    public void testRegressionUnicodeCharacters() {
        assertFalse(PasswordValidator.isValidPassword("Pass123\u00A1"));  // ¡
        assertFalse(PasswordValidator.isValidPassword("Pass123\u00BF"));  // ¿
        assertFalse(PasswordValidator.isValidPassword("Test123\u00E9"));  // é
    }

    @Test
    @DisplayName("Regression: Emoji characters are rejected")
    public void testRegressionEmojiCharacters() {
        assertFalse(PasswordValidator.isValidPassword("Password123😀"));
    }

    @Test
    @DisplayName("Regression: All requirements met but too short by one char")
    public void testRegressionAllRequirementsButTooShort() {
        assertFalse(PasswordValidator.isValidPassword("Aa1@bcd"));  // 7 chars
    }

    @Test
    @DisplayName("Regression: Case sensitivity for letters")
    public void testRegressionCaseSensitivity() {
        assertTrue(PasswordValidator.isValidPassword("ABCdef12!"));
        assertFalse(PasswordValidator.isValidPassword("abcdefg1!"));  // No uppercase
        assertFalse(PasswordValidator.isValidPassword("ABCDEFG1!"));  // No lowercase
    }

    @Test
    @DisplayName("Regression: Zero is a valid digit")
    public void testRegressionZeroIsValidDigit() {
        assertTrue(PasswordValidator.isValidPassword("Test000@abc"));
    }

    @Test
    @DisplayName("Regression: Digits at different positions")
    public void testRegressionDigitsAtDifferentPositions() {
        assertTrue(PasswordValidator.isValidPassword("1Testab@"));  // Beginning
        assertTrue(PasswordValidator.isValidPassword("Test1ab@"));  // Middle
        assertTrue(PasswordValidator.isValidPassword("Testab@1"));  // End
    }

    @Test
    @DisplayName("Negative test: SQL injection patterns")
    public void testNegativeSQLInjectionPatterns() {
        assertFalse(PasswordValidator.isValidPassword("'; DROP TABLE users; --"));
        assertFalse(PasswordValidator.isValidPassword("' OR '1'='1"));
    }

    @Test
    @DisplayName("Negative test: Common weak passwords")
    public void testNegativeCommonWeakPasswords() {
        assertFalse(PasswordValidator.isValidPassword("password"));
        assertFalse(PasswordValidator.isValidPassword("12345678"));
        assertFalse(PasswordValidator.isValidPassword("qwerty"));
    }

    @Test
    @DisplayName("Negative test: Dictionary words without complexity")
    public void testNegativeDictionaryWords() {
        assertFalse(PasswordValidator.isValidPassword("dictionary"));
        assertFalse(PasswordValidator.isValidPassword("SUMMER"));
        assertFalse(PasswordValidator.isValidPassword("Winter"));
    }

    @Test
    @DisplayName("Boundary test: Password starting with each allowed special char")
    public void testBoundaryPasswordStartingWithSpecialChar() {
        assertTrue(PasswordValidator.isValidPassword("@Test123"));
        assertTrue(PasswordValidator.isValidPassword("$Test123"));
        assertTrue(PasswordValidator.isValidPassword("!Test123"));
        assertTrue(PasswordValidator.isValidPassword("%Test123"));
        assertTrue(PasswordValidator.isValidPassword("*Test123"));
        assertTrue(PasswordValidator.isValidPassword("?Test123"));
        assertTrue(PasswordValidator.isValidPassword("&Test123"));
    }

    @Test
    @DisplayName("Boundary test: Password ending with each allowed special char")
    public void testBoundaryPasswordEndingWithSpecialChar() {
        assertTrue(PasswordValidator.isValidPassword("Test123@"));
        assertTrue(PasswordValidator.isValidPassword("Test123$"));
        assertTrue(PasswordValidator.isValidPassword("Test123!"));
        assertTrue(PasswordValidator.isValidPassword("Test123%"));
        assertTrue(PasswordValidator.isValidPassword("Test123*"));
        assertTrue(PasswordValidator.isValidPassword("Test123?"));
        assertTrue(PasswordValidator.isValidPassword("Test123&"));
    }

    @Test
    @DisplayName("Additional test: Password with all digits 0-9")
    public void testPasswordWithAllDigits() {
        assertTrue(PasswordValidator.isValidPassword("Test0123456789!"));
    }

    @Test
    @DisplayName("Additional test: Password with alternating case")
    public void testPasswordWithAlternatingCase() {
        assertTrue(PasswordValidator.isValidPassword("TeSt123!@#"));
    }
}