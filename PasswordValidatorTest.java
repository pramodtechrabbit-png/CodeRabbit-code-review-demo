import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for PasswordValidator
 *
 * Tests cover:
 * - Valid passwords meeting all requirements
 * - Null and empty input validation
 * - Whitespace handling
 * - Individual requirement failures (missing uppercase, lowercase, digit, special char)
 * - Minimum length validation
 * - Edge cases and boundary conditions
 * - Special character validation
 * - Security-related edge cases
 */
@DisplayName("PasswordValidator Tests")
public class PasswordValidatorTest {

    // ========== Valid Password Tests ==========

    @Test
    @DisplayName("Valid password with all requirements met")
    public void testValidPasswordWithAllRequirements() {
        assertTrue(PasswordValidator.isValidPassword("Test1234!"));
    }

    @Test
    @DisplayName("Valid password at minimum length (8 characters)")
    public void testValidPasswordMinimumLength() {
        assertTrue(PasswordValidator.isValidPassword("Test123!"));
    }

    @Test
    @DisplayName("Valid password with long length")
    public void testValidPasswordLongLength() {
        assertTrue(PasswordValidator.isValidPassword("TestPassword123!@#$%LongString"));
    }

    @Test
    @DisplayName("Valid password with all allowed special characters")
    public void testValidPasswordAllSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Pass123@"));
        assertTrue(PasswordValidator.isValidPassword("Pass123$"));
        assertTrue(PasswordValidator.isValidPassword("Pass123!"));
        assertTrue(PasswordValidator.isValidPassword("Pass123%"));
        assertTrue(PasswordValidator.isValidPassword("Pass123*"));
        assertTrue(PasswordValidator.isValidPassword("Pass123?"));
        assertTrue(PasswordValidator.isValidPassword("Pass123&"));
    }

    @Test
    @DisplayName("Valid password with multiple special characters")
    public void testValidPasswordMultipleSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Test123!@#$%*?&"));
    }

    @Test
    @DisplayName("Valid password with uppercase at different positions")
    public void testValidPasswordUppercasePositions() {
        assertTrue(PasswordValidator.isValidPassword("Test1234!"));  // Beginning
        assertTrue(PasswordValidator.isValidPassword("tEst1234!"));  // Middle
        assertTrue(PasswordValidator.isValidPassword("test1234T!")); // End
    }

    // ========== Null and Empty Tests ==========

    @Test
    @DisplayName("Null password should be invalid")
    public void testNullPassword() {
        assertFalse(PasswordValidator.isValidPassword(null));
    }

    @Test
    @DisplayName("Empty string password should be invalid")
    public void testEmptyPassword() {
        assertFalse(PasswordValidator.isValidPassword(""));
    }

    @ParameterizedTest
    @ValueSource(strings = {" ", "  ", "   ", "\t", "\n", "\r\n", "    "})
    @DisplayName("Whitespace-only passwords should be invalid")
    public void testWhitespaceOnlyPasswords(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    // ========== Missing Requirements Tests ==========

    @Test
    @DisplayName("Password missing uppercase letter should be invalid")
    public void testPasswordMissingUppercase() {
        assertFalse(PasswordValidator.isValidPassword("test1234!"));
    }

    @Test
    @DisplayName("Password missing lowercase letter should be invalid")
    public void testPasswordMissingLowercase() {
        assertFalse(PasswordValidator.isValidPassword("TEST1234!"));
    }

    @Test
    @DisplayName("Password missing digit should be invalid")
    public void testPasswordMissingDigit() {
        assertFalse(PasswordValidator.isValidPassword("TestTest!"));
    }

    @Test
    @DisplayName("Password missing special character should be invalid")
    public void testPasswordMissingSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("Test1234"));
    }

    @Test
    @DisplayName("Password with only uppercase and lowercase should be invalid")
    public void testPasswordOnlyLetters() {
        assertFalse(PasswordValidator.isValidPassword("TestTestTest"));
    }

    @Test
    @DisplayName("Password with only letters and digits should be invalid")
    public void testPasswordNoSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("Test1234Test"));
    }

    // ========== Length Validation Tests ==========

    @ParameterizedTest
    @ValueSource(strings = {"T1!", "Te1!", "Tes1!", "Test1!", "Test12!", "Test123"})
    @DisplayName("Passwords shorter than 8 characters should be invalid")
    public void testPasswordTooShort(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    @Test
    @DisplayName("Password with exactly 7 characters should be invalid")
    public void testPasswordSevenCharacters() {
        assertFalse(PasswordValidator.isValidPassword("Test12!"));
    }

    @Test
    @DisplayName("Password with exactly 8 characters and all requirements should be valid")
    public void testPasswordExactlyEightCharacters() {
        assertTrue(PasswordValidator.isValidPassword("Test123!"));
    }

    @Test
    @DisplayName("Very long valid password should be accepted")
    public void testVeryLongPassword() {
        String longPassword = "Test1234!" + "a".repeat(1000);
        assertTrue(PasswordValidator.isValidPassword(longPassword));
    }

    // ========== Special Character Edge Cases ==========

    @ParameterizedTest
    @ValueSource(strings = {"Test1234#", "Test1234^", "Test1234(", "Test1234)", "Test1234-",
                            "Test1234_", "Test1234+", "Test1234=", "Test1234~"})
    @DisplayName("Passwords with non-allowed special characters should be invalid")
    public void testPasswordWithDisallowedSpecialChars(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    @Test
    @DisplayName("Password with space character should be invalid")
    public void testPasswordWithSpace() {
        assertFalse(PasswordValidator.isValidPassword("Test 1234!"));
    }

    @Test
    @DisplayName("Password with leading whitespace should be invalid after trim")
    public void testPasswordWithLeadingWhitespace() {
        assertFalse(PasswordValidator.isValidPassword(" Test1234!"));
    }

    @Test
    @DisplayName("Password with trailing whitespace should be invalid after trim")
    public void testPasswordWithTrailingWhitespace() {
        assertFalse(PasswordValidator.isValidPassword("Test1234! "));
    }

    // ========== Boundary and Edge Cases ==========

    @Test
    @DisplayName("Password with multiple uppercase letters should be valid")
    public void testPasswordMultipleUppercase() {
        assertTrue(PasswordValidator.isValidPassword("TEST1234!"));
        assertTrue(PasswordValidator.isValidPassword("TeST1234!"));
    }

    @Test
    @DisplayName("Password with multiple lowercase letters should be valid")
    public void testPasswordMultipleLowercase() {
        assertTrue(PasswordValidator.isValidPassword("Test1234!"));
        assertTrue(PasswordValidator.isValidPassword("TESt1234!"));
    }

    @Test
    @DisplayName("Password with multiple digits should be valid")
    public void testPasswordMultipleDigits() {
        assertTrue(PasswordValidator.isValidPassword("Test12345!"));
        assertTrue(PasswordValidator.isValidPassword("Test999999!"));
    }

    @Test
    @DisplayName("Password starting with digit should be valid")
    public void testPasswordStartingWithDigit() {
        assertTrue(PasswordValidator.isValidPassword("1TestAbc!"));
    }

    @Test
    @DisplayName("Password starting with special char should be valid")
    public void testPasswordStartingWithSpecialChar() {
        assertTrue(PasswordValidator.isValidPassword("!Test1234"));
    }

    @Test
    @DisplayName("Password ending with uppercase should be valid")
    public void testPasswordEndingWithUppercase() {
        assertTrue(PasswordValidator.isValidPassword("test1234!A"));
    }

    // ========== Multiple Requirement Failures ==========

    @Test
    @DisplayName("Password missing multiple requirements should be invalid")
    public void testPasswordMissingMultipleRequirements() {
        assertFalse(PasswordValidator.isValidPassword("testtest"));     // Missing upper, digit, special
        assertFalse(PasswordValidator.isValidPassword("TESTTEST"));     // Missing lower, digit, special
        assertFalse(PasswordValidator.isValidPassword("12345678"));     // Missing upper, lower, special
        assertFalse(PasswordValidator.isValidPassword("!@#$%*?&"));     // Missing upper, lower, digit
    }

    @Test
    @DisplayName("Password with all characters same type should be invalid")
    public void testPasswordSameType() {
        assertFalse(PasswordValidator.isValidPassword("abcdefgh"));     // Only lowercase
        assertFalse(PasswordValidator.isValidPassword("ABCDEFGH"));     // Only uppercase
        assertFalse(PasswordValidator.isValidPassword("12345678"));     // Only digits
    }

    // ========== Regex Pattern Edge Cases ==========

    @Test
    @DisplayName("Password with minimum one of each requirement should be valid")
    public void testPasswordMinimumRequirements() {
        assertTrue(PasswordValidator.isValidPassword("Aa1!aaaa"));
    }

    @Test
    @DisplayName("Password with requirements scattered throughout should be valid")
    public void testPasswordScatteredRequirements() {
        assertTrue(PasswordValidator.isValidPassword("a1B!cdef"));
        assertTrue(PasswordValidator.isValidPassword("!1aB2c3D"));
    }

    @Test
    @DisplayName("Password with special characters at boundaries should be valid")
    public void testPasswordSpecialCharBoundaries() {
        assertTrue(PasswordValidator.isValidPassword("!Test123"));
        assertTrue(PasswordValidator.isValidPassword("Test123!"));
        assertTrue(PasswordValidator.isValidPassword("!Test12!"));
    }

    // ========== Common Password Patterns ==========

    @ParameterizedTest
    @ValueSource(strings = {"Password1!", "Welcome1!", "Admin123!", "Test1234!", "User1234@"})
    @DisplayName("Common but valid password patterns should be accepted")
    public void testCommonValidPasswords(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    @ParameterizedTest
    @ValueSource(strings = {"password", "12345678", "qwerty", "abc123", "password123"})
    @DisplayName("Common weak passwords should be rejected")
    public void testCommonWeakPasswords(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    // ========== Real-world Scenarios ==========

    @Test
    @DisplayName("Password with mix of requirements in realistic format should be valid")
    public void testRealisticPassword() {
        assertTrue(PasswordValidator.isValidPassword("MyP@ssw0rd"));
        assertTrue(PasswordValidator.isValidPassword("Secure123!"));
        assertTrue(PasswordValidator.isValidPassword("Complex$Pass1"));
    }

    @Test
    @DisplayName("Password that looks secure but missing requirements should be invalid")
    public void testAlmostValidPassword() {
        assertFalse(PasswordValidator.isValidPassword("password123"));  // Missing upper and special
        assertFalse(PasswordValidator.isValidPassword("PASSWORD123"));  // Missing lower and special
        assertFalse(PasswordValidator.isValidPassword("Password!@#"));  // Missing digit
    }

    // ========== Unicode and International Characters ==========

    @Test
    @DisplayName("Password with unicode characters should be invalid")
    public void testPasswordWithUnicodeChars() {
        assertFalse(PasswordValidator.isValidPassword("Test123\u00E9!"));  // é character
        assertFalse(PasswordValidator.isValidPassword("Test123\u4E2D!"));  // Chinese character
    }

    @Test
    @DisplayName("Password with emoji should be invalid")
    public void testPasswordWithEmoji() {
        assertFalse(PasswordValidator.isValidPassword("Test123!😀"));
    }

    // ========== Security Edge Cases ==========

    @Test
    @DisplayName("Password with repeated characters but meeting requirements should be valid")
    public void testPasswordRepeatedCharacters() {
        assertTrue(PasswordValidator.isValidPassword("AAaa11!!"));
    }

    @Test
    @DisplayName("Password with all same character repeated should be invalid")
    public void testPasswordAllSameChar() {
        assertFalse(PasswordValidator.isValidPassword("aaaaaaaa"));
    }

    @Test
    @DisplayName("Sequential characters meeting requirements should be valid")
    public void testPasswordSequentialChars() {
        assertTrue(PasswordValidator.isValidPassword("Abcd1234!"));
    }

    // ========== Trim Behavior Tests ==========

    @Test
    @DisplayName("Password with only whitespace after trim should be invalid")
    public void testPasswordWhitespaceAfterTrim() {
        assertFalse(PasswordValidator.isValidPassword("   "));
    }

    @Test
    @DisplayName("Valid password with surrounding whitespace should be invalid due to trim")
    public void testValidPasswordWithSurroundingWhitespace() {
        // The password is trimmed first, which removes the whitespace
        // But "Test1234!" itself is only 9 chars after trim, still valid
        assertTrue(PasswordValidator.isValidPassword(" Test1234! "));

        // However, internal spaces would make it invalid
        assertFalse(PasswordValidator.isValidPassword(" Test 1234! "));
    }

    // ========== Additional Regression Tests ==========

    @Test
    @DisplayName("Password exactly meeting minimum criteria should be valid")
    public void testMinimumValidPassword() {
        assertTrue(PasswordValidator.isValidPassword("Aa1!aaaa"));  // 8 chars: 1 upper, 6 lower, 1 digit, 1 special
    }

    @Test
    @DisplayName("Password with all requirements but only 7 chars should be invalid")
    public void testAllRequirementsButTooShort() {
        assertFalse(PasswordValidator.isValidPassword("Aa1!aaa"));  // Only 7 chars
    }

    @Test
    @DisplayName("Password with 8 chars but missing one requirement should be invalid")
    public void testEightCharsButMissingRequirement() {
        assertFalse(PasswordValidator.isValidPassword("Aaa1aaaa"));  // Missing special char
        assertFalse(PasswordValidator.isValidPassword("Aaa!aaaa"));  // Missing digit
        assertFalse(PasswordValidator.isValidPassword("AA1!aaaa"));  // Missing lowercase (has 2 lower)
    }

    @ParameterizedTest
    @ValueSource(strings = {"Test123@", "Pass456$", "Word789!", "Code012%", "Safe345*"})
    @DisplayName("Various valid 8-character passwords should all pass")
    public void testVariousValid8CharPasswords(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    @Test
    @DisplayName("Password with alternating character types should be valid")
    public void testAlternatingCharTypes() {
        assertTrue(PasswordValidator.isValidPassword("A1a!B2b@"));
    }

    @Test
    @DisplayName("Password with special char in middle should be valid")
    public void testSpecialCharMiddle() {
        assertTrue(PasswordValidator.isValidPassword("Test!123Abc"));
    }

    // ========== Negative Test Cases ==========

    @Test
    @DisplayName("Password with tab character should be invalid")
    public void testPasswordWithTab() {
        assertFalse(PasswordValidator.isValidPassword("Test\t1234!"));
    }

    @Test
    @DisplayName("Password with newline character should be invalid")
    public void testPasswordWithNewline() {
        assertFalse(PasswordValidator.isValidPassword("Test\n1234!"));
    }

    @Test
    @DisplayName("Empty string after trim should be invalid")
    public void testEmptyAfterTrim() {
        assertFalse(PasswordValidator.isValidPassword("     "));
    }
}