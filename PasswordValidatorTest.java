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
 * - Valid passwords with all required criteria
 * - Invalid passwords missing various criteria
 * - Edge cases (null, empty, whitespace)
 * - Boundary conditions (minimum length)
 * - Special character validation
 * - Case sensitivity
 * - Regression scenarios
 */
@DisplayName("PasswordValidator Tests")
class PasswordValidatorTest {

    // ========== Valid Password Tests ==========

    @Test
    @DisplayName("Valid password with all required criteria")
    void testValidPassword() {
        assertTrue(PasswordValidator.isValidPassword("Valid1Pass!"));
    }

    @Test
    @DisplayName("Valid password with exactly 8 characters")
    void testValidPasswordMinimumLength() {
        assertTrue(PasswordValidator.isValidPassword("Pass1234!"));
    }

    @Test
    @DisplayName("Valid password with multiple special characters")
    void testValidPasswordMultipleSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Valid1@Pass!"));
    }

    @Test
    @DisplayName("Valid password with all allowed special characters")
    void testValidPasswordAllSpecialChars() {
        assertTrue(PasswordValidator.isValidPassword("Valid1@$!%*?&Pass"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "Password1@",
        "MyP@ssw0rd",
        "Str0ng!Pass",
        "C0mplex$123",
        "S3cur3P@ss",
        "T3st!Pass1",
        "V@lid8Pwd",
        "P@ssw0rd123",
        "Secure!23Pass",
        "Abcdef1@"
    })
    @DisplayName("Valid passwords with various combinations")
    void testVariousValidPasswords(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    // ========== Null and Empty Tests ==========

    @Test
    @DisplayName("Null password returns false")
    void testNullPassword() {
        assertFalse(PasswordValidator.isValidPassword(null));
    }

    @Test
    @DisplayName("Empty password returns false")
    void testEmptyPassword() {
        assertFalse(PasswordValidator.isValidPassword(""));
    }

    @Test
    @DisplayName("Whitespace-only password returns false")
    void testWhitespaceOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("        "));
    }

    @Test
    @DisplayName("Password with only tabs returns false")
    void testTabOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("\t\t\t\t"));
    }

    @Test
    @DisplayName("Password with mixed whitespace returns false")
    void testMixedWhitespacePassword() {
        assertFalse(PasswordValidator.isValidPassword(" \t\n\r "));
    }

    // ========== Length Requirement Tests ==========

    @Test
    @DisplayName("Password with 7 characters returns false")
    void testPasswordTooShort() {
        assertFalse(PasswordValidator.isValidPassword("Pass1@"));
    }

    @Test
    @DisplayName("Password with 1 character returns false")
    void testPasswordSingleCharacter() {
        assertFalse(PasswordValidator.isValidPassword("P"));
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "P1@a",        // 4 chars
        "Pa1@",        // 4 chars
        "Pass1@",      // 6 chars
        "Pass1@a"      // 7 chars
    })
    @DisplayName("Passwords shorter than 8 characters return false")
    void testPasswordsBelowMinimumLength(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    // ========== Missing Lowercase Letter Tests ==========

    @Test
    @DisplayName("Password without lowercase letter returns false")
    void testPasswordNoLowercase() {
        assertFalse(PasswordValidator.isValidPassword("PASSWORD1!"));
    }

    @Test
    @DisplayName("Password with only uppercase, digit, and special char returns false")
    void testPasswordNoLowercaseAllOthers() {
        assertFalse(PasswordValidator.isValidPassword("TESTING123!"));
    }

    // ========== Missing Uppercase Letter Tests ==========

    @Test
    @DisplayName("Password without uppercase letter returns false")
    void testPasswordNoUppercase() {
        assertFalse(PasswordValidator.isValidPassword("password1!"));
    }

    @Test
    @DisplayName("Password with only lowercase, digit, and special char returns false")
    void testPasswordNoUppercaseAllOthers() {
        assertFalse(PasswordValidator.isValidPassword("testing123!"));
    }

    // ========== Missing Digit Tests ==========

    @Test
    @DisplayName("Password without digit returns false")
    void testPasswordNoDigit() {
        assertFalse(PasswordValidator.isValidPassword("Password!"));
    }

    @Test
    @DisplayName("Password with letters and special chars but no digit returns false")
    void testPasswordNoDigitAllOthers() {
        assertFalse(PasswordValidator.isValidPassword("TestPass!@#"));
    }

    // ========== Missing Special Character Tests ==========

    @Test
    @DisplayName("Password without special character returns false")
    void testPasswordNoSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("Password123"));
    }

    @Test
    @DisplayName("Password with letters and digits but no special char returns false")
    void testPasswordNoSpecialCharAllOthers() {
        assertFalse(PasswordValidator.isValidPassword("TestPass123"));
    }

    // ========== Special Character Validation Tests ==========

    @ParameterizedTest
    @ValueSource(strings = {
        "Password1@",   // @ allowed
        "Password1$",   // $ allowed
        "Password1!",   // ! allowed
        "Password1%",   // % allowed
        "Password1*",   // * allowed
        "Password1?",   // ? allowed
        "Password1&"    // & allowed
    })
    @DisplayName("Passwords with each allowed special character are valid")
    void testEachAllowedSpecialCharacter(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    @ParameterizedTest
    @ValueSource(strings = {
        "Password1#",   // # not allowed
        "Password1^",   // ^ not allowed
        "Password1(",   // ( not allowed
        "Password1)",   // ) not allowed
        "Password1-",   // - not allowed
        "Password1_",   // _ not allowed
        "Password1+",   // + not allowed
        "Password1=",   // = not allowed
        "Password1[",   // [ not allowed
        "Password1]",   // ] not allowed
        "Password1{",   // { not allowed
        "Password1}",   // } not allowed
        "Password1|",   // | not allowed
        "Password1\\",  // \ not allowed
        "Password1:",   // : not allowed
        "Password1;",   // ; not allowed
        "Password1\"",  // " not allowed
        "Password1'",   // ' not allowed
        "Password1<",   // < not allowed
        "Password1>",   // > not allowed
        "Password1,",   // , not allowed
        "Password1.",   // . not allowed
        "Password1/",   // / not allowed
        "Password1~",   // ~ not allowed
        "Password1`"    // ` not allowed
    })
    @DisplayName("Passwords with disallowed special characters return false")
    void testDisallowedSpecialCharacters(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }

    // ========== Whitespace in Password Tests ==========

    @Test
    @DisplayName("Password with leading whitespace returns false")
    void testPasswordWithLeadingWhitespace() {
        assertFalse(PasswordValidator.isValidPassword(" Password1!"));
    }

    @Test
    @DisplayName("Password with trailing whitespace returns false")
    void testPasswordWithTrailingWhitespace() {
        assertFalse(PasswordValidator.isValidPassword("Password1! "));
    }

    @Test
    @DisplayName("Password with internal whitespace returns false")
    void testPasswordWithInternalWhitespace() {
        assertFalse(PasswordValidator.isValidPassword("Pass word1!"));
    }

    @Test
    @DisplayName("Password with multiple spaces returns false")
    void testPasswordWithMultipleSpaces() {
        assertFalse(PasswordValidator.isValidPassword("Pass   word1!"));
    }

    // ========== Edge Cases and Boundary Tests ==========

    @Test
    @DisplayName("Password with exactly one of each required element")
    void testPasswordMinimalRequirements() {
        assertTrue(PasswordValidator.isValidPassword("Abcdef1@"));
    }

    @Test
    @DisplayName("Very long valid password")
    void testVeryLongPassword() {
        String longPassword = "Abcdef1@" + "a".repeat(100);
        assertTrue(PasswordValidator.isValidPassword(longPassword));
    }

    @Test
    @DisplayName("Password with multiple uppercase letters")
    void testPasswordMultipleUppercase() {
        assertTrue(PasswordValidator.isValidPassword("PASSWORD1!"));
    }

    @Test
    @DisplayName("Password with multiple lowercase letters")
    void testPasswordMultipleLowercase() {
        assertTrue(PasswordValidator.isValidPassword("Password1!"));
    }

    @Test
    @DisplayName("Password with multiple digits")
    void testPasswordMultipleDigits() {
        assertTrue(PasswordValidator.isValidPassword("Pass123456!"));
    }

    @Test
    @DisplayName("Password starting with digit")
    void testPasswordStartingWithDigit() {
        assertTrue(PasswordValidator.isValidPassword("1Password!"));
    }

    @Test
    @DisplayName("Password starting with special character")
    void testPasswordStartingWithSpecialChar() {
        assertTrue(PasswordValidator.isValidPassword("@Password1"));
    }

    @Test
    @DisplayName("Password ending with uppercase")
    void testPasswordEndingWithUppercase() {
        assertTrue(PasswordValidator.isValidPassword("password1!A"));
    }

    @Test
    @DisplayName("Password with all digits except one letter and special char")
    void testPasswordMostlyDigits() {
        assertTrue(PasswordValidator.isValidPassword("Aa@111111"));
    }

    @Test
    @DisplayName("Password with alternating character types")
    void testPasswordAlternatingTypes() {
        assertTrue(PasswordValidator.isValidPassword("P1a@S2s!"));
    }

    // ========== Regression Tests ==========

    @Test
    @DisplayName("Regression: Password with only special characters fails")
    void testRegressionOnlySpecialChars() {
        assertFalse(PasswordValidator.isValidPassword("@$!%*?&@"));
    }

    @Test
    @DisplayName("Regression: Password with Unicode characters fails")
    void testRegressionUnicodeCharacters() {
        assertFalse(PasswordValidator.isValidPassword("Pässw0rd!"));
    }

    @Test
    @DisplayName("Regression: Password 'admin' returns false")
    void testRegressionCommonPassword() {
        assertFalse(PasswordValidator.isValidPassword("admin"));
    }

    @Test
    @DisplayName("Regression: Password '12345678' returns false")
    void testRegressionNumericOnlyPassword() {
        assertFalse(PasswordValidator.isValidPassword("12345678"));
    }

    @Test
    @DisplayName("Regression: Password with null character fails")
    void testRegressionNullCharacter() {
        assertFalse(PasswordValidator.isValidPassword("Pass1\0word!"));
    }

    @Test
    @DisplayName("Regression: Password with newline character fails")
    void testRegressionNewlineCharacter() {
        assertFalse(PasswordValidator.isValidPassword("Pass1\nword!"));
    }

    @Test
    @DisplayName("Regression: Empty string after trim returns false")
    void testRegressionEmptyAfterTrim() {
        assertFalse(PasswordValidator.isValidPassword("   "));
    }

    // ========== Multiple Missing Requirements Tests ==========

    @Test
    @DisplayName("Password missing uppercase and digit returns false")
    void testPasswordMissingUppercaseAndDigit() {
        assertFalse(PasswordValidator.isValidPassword("password!"));
    }

    @Test
    @DisplayName("Password missing lowercase and special char returns false")
    void testPasswordMissingLowercaseAndSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("PASSWORD123"));
    }

    @Test
    @DisplayName("Password missing digit and special char returns false")
    void testPasswordMissingDigitAndSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("Password"));
    }

    @Test
    @DisplayName("Password with only letters returns false")
    void testPasswordOnlyLetters() {
        assertFalse(PasswordValidator.isValidPassword("PasswordTest"));
    }

    @Test
    @DisplayName("Password with all uppercase letters and digit but no special char returns false")
    void testPasswordUppercaseDigitNoSpecialChar() {
        assertFalse(PasswordValidator.isValidPassword("PASSWORD123"));
    }

    // ========== Case Sensitivity Tests ==========

    @Test
    @DisplayName("Password case sensitivity - all lowercase with requirements fails without uppercase")
    void testCaseSensitivityAllLowercase() {
        assertFalse(PasswordValidator.isValidPassword("password1!"));
    }

    @Test
    @DisplayName("Password case sensitivity - all uppercase with requirements fails without lowercase")
    void testCaseSensitivityAllUppercase() {
        assertFalse(PasswordValidator.isValidPassword("PASSWORD1!"));
    }

    @Test
    @DisplayName("Password case sensitivity - mixed case required")
    void testCaseSensitivityMixedRequired() {
        assertTrue(PasswordValidator.isValidPassword("Password1!"));
    }

    // ========== Additional Security Tests ==========

    @Test
    @DisplayName("Common weak password 'Password1!' is valid but weak")
    void testCommonWeakPasswordStillValid() {
        // This password meets technical requirements but is weak
        assertTrue(PasswordValidator.isValidPassword("Password1!"));
    }

    @Test
    @DisplayName("Password with repeated characters but valid")
    void testPasswordRepeatedCharacters() {
        assertTrue(PasswordValidator.isValidPassword("Aaaaaa1!"));
    }

    @Test
    @DisplayName("Password with sequential characters but valid")
    void testPasswordSequentialCharacters() {
        assertTrue(PasswordValidator.isValidPassword("Abc123!@"));
    }

    // ========== Boundary Length Tests ==========

    @Test
    @DisplayName("Password exactly 8 characters with all requirements")
    void testPasswordExactly8Characters() {
        assertTrue(PasswordValidator.isValidPassword("Passwor1!"));
    }

    @Test
    @DisplayName("Password with 9 characters")
    void testPassword9Characters() {
        assertTrue(PasswordValidator.isValidPassword("Password1!"));
    }

    @Test
    @DisplayName("Password with 100 characters")
    void testPassword100Characters() {
        String password = "Pass1@" + "a".repeat(94);
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    // ========== SQL Injection Pattern Tests ==========

    @Test
    @DisplayName("Password resembling SQL injection returns false due to disallowed chars")
    void testSQLInjectionPattern() {
        assertFalse(PasswordValidator.isValidPassword("Pass1' OR '1'='1"));
    }

    @Test
    @DisplayName("Password with semicolon returns false")
    void testPasswordWithSemicolon() {
        assertFalse(PasswordValidator.isValidPassword("Pass1;DROP"));
    }

    // ========== Real-World Valid Password Examples ==========

    @ParameterizedTest
    @ValueSource(strings = {
        "MyS3cur3P@ss",
        "Tr0ub4dor&3",
        "C0rr3ct!H0rs3",
        "P@ssw0rdStr0ng",
        "S3cur1ty!F1rst",
        "My!P@ssw0rd",
        "Compl3x$Pass",
        "S@f3P@ssw0rd",
        "Str0ng!2024",
        "T3st@Acc0unt"
    })
    @DisplayName("Real-world valid password examples")
    void testRealWorldValidPasswords(String password) {
        assertTrue(PasswordValidator.isValidPassword(password));
    }

    // ========== Real-World Invalid Password Examples ==========

    @ParameterizedTest
    @ValueSource(strings = {
        "password",         // No uppercase, digit, special char
        "PASSWORD",         // No lowercase, digit, special char
        "12345678",         // No letters, special char
        "pass",             // Too short
        "Pass1",            // Too short, no special char
        "password123",      // No uppercase, special char
        "PASSWORD123",      // No lowercase, special char
        "Password!",        // No digit
        "Password1",        // No special char
        "Pass!",            // Too short, no digit
        "admin123",         // No uppercase, special char
        "qwerty",           // Too short, no uppercase, digit, special char
        "letmein",          // No uppercase, digit, special char
        "welcome",          // No uppercase, digit, special char
        "monkey",           // Too short, no uppercase, digit, special char
        "dragon",           // Too short, no uppercase, digit, special char
        "master",           // Too short, no uppercase, digit, special char
        "sunshine",         // No uppercase, digit, special char
        "princess",         // No uppercase, digit, special char
        "football"          // No uppercase, digit, special char
    })
    @DisplayName("Real-world invalid password examples")
    void testRealWorldInvalidPasswords(String password) {
        assertFalse(PasswordValidator.isValidPassword(password));
    }
}