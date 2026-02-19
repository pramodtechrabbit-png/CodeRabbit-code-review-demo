import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Comprehensive test suite for PasswordValidator
 * Tests cover validation rules, edge cases, and boundary conditions
 */
public class PasswordValidatorTest {

    @Nested
    @DisplayName("Valid Password Tests")
    class ValidPasswordTests {
        @Test
        @DisplayName("Test valid password with all requirements")
        void testValidPasswordAllRequirements() {
            assertTrue(PasswordValidator.isValidPassword("Test123!"));
        }

        @Test
        @DisplayName("Test valid password with minimum length")
        void testValidPasswordMinimumLength() {
            assertTrue(PasswordValidator.isValidPassword("Abcd123!"));
        }

        @Test
        @DisplayName("Test valid password with all allowed special characters")
        void testValidPasswordAllSpecialChars() {
            assertTrue(PasswordValidator.isValidPassword("Test1@$!"));
            assertTrue(PasswordValidator.isValidPassword("Test2%*?"));
            assertTrue(PasswordValidator.isValidPassword("Test3&ab"));
        }

        @Test
        @DisplayName("Test valid password with multiple uppercase letters")
        void testValidPasswordMultipleUppercase() {
            assertTrue(PasswordValidator.isValidPassword("TEST123!abc"));
        }

        @Test
        @DisplayName("Test valid password with multiple lowercase letters")
        void testValidPasswordMultipleLowercase() {
            assertTrue(PasswordValidator.isValidPassword("Testtest1!"));
        }

        @Test
        @DisplayName("Test valid password with multiple digits")
        void testValidPasswordMultipleDigits() {
            assertTrue(PasswordValidator.isValidPassword("Test123456!"));
        }

        @Test
        @DisplayName("Test valid password with multiple special characters")
        void testValidPasswordMultipleSpecial() {
            assertTrue(PasswordValidator.isValidPassword("Test1@!$%"));
        }

        @Test
        @DisplayName("Test valid password with long length")
        void testValidPasswordLongLength() {
            assertTrue(PasswordValidator.isValidPassword("TestPassword123!ExtendedVersion"));
        }

        @Test
        @DisplayName("Test valid password at exact 8 characters")
        void testValidPasswordExactEightChars() {
            assertTrue(PasswordValidator.isValidPassword("Pass123!"));
        }
    }

    @Nested
    @DisplayName("Invalid Password - Null and Empty Tests")
    class NullAndEmptyTests {
        @Test
        @DisplayName("Test null password returns false")
        void testNullPassword() {
            assertFalse(PasswordValidator.isValidPassword(null));
        }

        @Test
        @DisplayName("Test empty string password returns false")
        void testEmptyPassword() {
            assertFalse(PasswordValidator.isValidPassword(""));
        }

        @Test
        @DisplayName("Test whitespace-only password returns false")
        void testWhitespaceOnlyPassword() {
            assertFalse(PasswordValidator.isValidPassword("        "));
        }

        @Test
        @DisplayName("Test password with leading/trailing whitespace that's valid when trimmed")
        void testPasswordWithWhitespace() {
            // Password gets trimmed, but still needs to meet requirements
            assertFalse(PasswordValidator.isValidPassword("  Test123!  "));
        }
    }

    @Nested
    @DisplayName("Invalid Password - Length Tests")
    class LengthTests {
        @Test
        @DisplayName("Test password with 7 characters fails")
        void testPasswordTooShort() {
            assertFalse(PasswordValidator.isValidPassword("Test12!"));
        }

        @Test
        @DisplayName("Test password with 6 characters fails")
        void testPasswordSixChars() {
            assertFalse(PasswordValidator.isValidPassword("Tes12!"));
        }

        @Test
        @DisplayName("Test password with 1 character fails")
        void testPasswordOneChar() {
            assertFalse(PasswordValidator.isValidPassword("A"));
        }

        @Test
        @DisplayName("Test password with 0 characters after trim fails")
        void testPasswordEmptyAfterTrim() {
            assertFalse(PasswordValidator.isValidPassword("   "));
        }
    }

    @Nested
    @DisplayName("Invalid Password - Missing Character Types")
    class MissingCharacterTypeTests {
        @Test
        @DisplayName("Test password missing uppercase letter")
        void testPasswordMissingUppercase() {
            assertFalse(PasswordValidator.isValidPassword("test123!"));
        }

        @Test
        @DisplayName("Test password missing lowercase letter")
        void testPasswordMissingLowercase() {
            assertFalse(PasswordValidator.isValidPassword("TEST123!"));
        }

        @Test
        @DisplayName("Test password missing digit")
        void testPasswordMissingDigit() {
            assertFalse(PasswordValidator.isValidPassword("TestPass!"));
        }

        @Test
        @DisplayName("Test password missing special character")
        void testPasswordMissingSpecialChar() {
            assertFalse(PasswordValidator.isValidPassword("Test1234"));
        }

        @Test
        @DisplayName("Test password with only uppercase and lowercase")
        void testPasswordOnlyLetters() {
            assertFalse(PasswordValidator.isValidPassword("TestPassword"));
        }

        @Test
        @DisplayName("Test password with only letters and digits")
        void testPasswordNoSpecialChar() {
            assertFalse(PasswordValidator.isValidPassword("Test1234"));
        }

        @Test
        @DisplayName("Test password with only uppercase and digits")
        void testPasswordNoLowercaseNoSpecial() {
            assertFalse(PasswordValidator.isValidPassword("TEST1234"));
        }
    }

    @Nested
    @DisplayName("Invalid Password - Invalid Special Characters")
    class InvalidSpecialCharacterTests {
        @Test
        @DisplayName("Test password with hash symbol (not in allowed set)")
        void testPasswordWithHashSymbol() {
            assertFalse(PasswordValidator.isValidPassword("Test123#"));
        }

        @Test
        @DisplayName("Test password with comma (not in allowed set)")
        void testPasswordWithComma() {
            assertFalse(PasswordValidator.isValidPassword("Test123,"));
        }

        @Test
        @DisplayName("Test password with period (not in allowed set)")
        void testPasswordWithPeriod() {
            assertFalse(PasswordValidator.isValidPassword("Test123."));
        }

        @Test
        @DisplayName("Test password with underscore (not in allowed set)")
        void testPasswordWithUnderscore() {
            assertFalse(PasswordValidator.isValidPassword("Test123_"));
        }

        @Test
        @DisplayName("Test password with dash (not in allowed set)")
        void testPasswordWithDash() {
            assertFalse(PasswordValidator.isValidPassword("Test123-"));
        }

        @Test
        @DisplayName("Test password with plus (not in allowed set)")
        void testPasswordWithPlus() {
            assertFalse(PasswordValidator.isValidPassword("Test123+"));
        }

        @Test
        @DisplayName("Test password with equals (not in allowed set)")
        void testPasswordWithEquals() {
            assertFalse(PasswordValidator.isValidPassword("Test123="));
        }

        @Test
        @DisplayName("Test password with parentheses (not in allowed set)")
        void testPasswordWithParentheses() {
            assertFalse(PasswordValidator.isValidPassword("Test123()"));
        }

        @Test
        @DisplayName("Test password with brackets (not in allowed set)")
        void testPasswordWithBrackets() {
            assertFalse(PasswordValidator.isValidPassword("Test123[]"));
        }

        @Test
        @DisplayName("Test password with braces (not in allowed set)")
        void testPasswordWithBraces() {
            assertFalse(PasswordValidator.isValidPassword("Test123{}"));
        }

        @Test
        @DisplayName("Test password with pipe (not in allowed set)")
        void testPasswordWithPipe() {
            assertFalse(PasswordValidator.isValidPassword("Test123|"));
        }

        @Test
        @DisplayName("Test password with backslash (not in allowed set)")
        void testPasswordWithBackslash() {
            assertFalse(PasswordValidator.isValidPassword("Test123\\"));
        }

        @Test
        @DisplayName("Test password with forward slash (not in allowed set)")
        void testPasswordWithForwardSlash() {
            assertFalse(PasswordValidator.isValidPassword("Test123/"));
        }

        @Test
        @DisplayName("Test password with semicolon (not in allowed set)")
        void testPasswordWithSemicolon() {
            assertFalse(PasswordValidator.isValidPassword("Test123;"));
        }

        @Test
        @DisplayName("Test password with colon (not in allowed set)")
        void testPasswordWithColon() {
            assertFalse(PasswordValidator.isValidPassword("Test123:"));
        }

        @Test
        @DisplayName("Test password with single quote (not in allowed set)")
        void testPasswordWithSingleQuote() {
            assertFalse(PasswordValidator.isValidPassword("Test123'"));
        }

        @Test
        @DisplayName("Test password with double quote (not in allowed set)")
        void testPasswordWithDoubleQuote() {
            assertFalse(PasswordValidator.isValidPassword("Test123\""));
        }

        @Test
        @DisplayName("Test password with less than (not in allowed set)")
        void testPasswordWithLessThan() {
            assertFalse(PasswordValidator.isValidPassword("Test123<"));
        }

        @Test
        @DisplayName("Test password with greater than (not in allowed set)")
        void testPasswordWithGreaterThan() {
            assertFalse(PasswordValidator.isValidPassword("Test123>"));
        }

        @Test
        @DisplayName("Test password with tilde (not in allowed set)")
        void testPasswordWithTilde() {
            assertFalse(PasswordValidator.isValidPassword("Test123~"));
        }

        @Test
        @DisplayName("Test password with backtick (not in allowed set)")
        void testPasswordWithBacktick() {
            assertFalse(PasswordValidator.isValidPassword("Test123`"));
        }
    }

    @Nested
    @DisplayName("Boundary and Edge Cases")
    class BoundaryAndEdgeCaseTests {
        @Test
        @DisplayName("Test password with exactly one of each required type")
        void testPasswordMinimalRequirements() {
            assertTrue(PasswordValidator.isValidPassword("Aa1!bcde"));
        }

        @Test
        @DisplayName("Test password with spaces (not allowed)")
        void testPasswordWithSpaces() {
            assertFalse(PasswordValidator.isValidPassword("Test 123!"));
        }

        @Test
        @DisplayName("Test password with tab character (not allowed)")
        void testPasswordWithTab() {
            assertFalse(PasswordValidator.isValidPassword("Test\t123!"));
        }

        @Test
        @DisplayName("Test password with newline (not allowed)")
        void testPasswordWithNewline() {
            assertFalse(PasswordValidator.isValidPassword("Test\n123!"));
        }

        @Test
        @DisplayName("Test very long valid password")
        void testVeryLongPassword() {
            String longPassword = "Aa1!" + "a".repeat(1000);
            assertTrue(PasswordValidator.isValidPassword(longPassword));
        }

        @Test
        @DisplayName("Test password with all allowed special chars")
        void testPasswordWithAllAllowedSpecialChars() {
            assertTrue(PasswordValidator.isValidPassword("Test1@$!%*?&"));
        }

        @Test
        @DisplayName("Test password with repeated characters")
        void testPasswordWithRepeatedChars() {
            assertTrue(PasswordValidator.isValidPassword("Aaaa1111!!!!"));
        }

        @Test
        @DisplayName("Test password with unicode characters (not allowed)")
        void testPasswordWithUnicode() {
            assertFalse(PasswordValidator.isValidPassword("Test123!ñ"));
        }

        @Test
        @DisplayName("Test password with emoji (not allowed)")
        void testPasswordWithEmoji() {
            assertFalse(PasswordValidator.isValidPassword("Test123!😀"));
        }

        @Test
        @DisplayName("Test password with control characters (not allowed)")
        void testPasswordWithControlChars() {
            assertFalse(PasswordValidator.isValidPassword("Test123!\u0000"));
        }
    }

    @Nested
    @DisplayName("Regression Tests")
    class RegressionTests {
        @Test
        @DisplayName("Test common weak passwords are rejected")
        void testCommonWeakPasswords() {
            assertFalse(PasswordValidator.isValidPassword("password"));
            assertFalse(PasswordValidator.isValidPassword("12345678"));
            assertFalse(PasswordValidator.isValidPassword("Password"));
        }

        @Test
        @DisplayName("Test password with all digits except required chars")
        void testPasswordMostlyDigits() {
            assertTrue(PasswordValidator.isValidPassword("Test1234567890!"));
        }

        @Test
        @DisplayName("Test password starting with special character")
        void testPasswordStartsWithSpecial() {
            assertTrue(PasswordValidator.isValidPassword("!Test123"));
        }

        @Test
        @DisplayName("Test password ending with digit")
        void testPasswordEndsWithDigit() {
            assertTrue(PasswordValidator.isValidPassword("Test!abc1"));
        }

        @Test
        @DisplayName("Test password with uppercase at different positions")
        void testPasswordUppercasePositions() {
            assertTrue(PasswordValidator.isValidPassword("test123!A"));
            assertTrue(PasswordValidator.isValidPassword("tEst123!"));
            assertTrue(PasswordValidator.isValidPassword("Aest123!"));
        }

        @Test
        @DisplayName("Test password that looks valid but has invalid special char")
        void testPasswordAlmostValid() {
            assertFalse(PasswordValidator.isValidPassword("Test123#")); // # not allowed
            assertFalse(PasswordValidator.isValidPassword("Test123_")); // _ not allowed
        }

        @Test
        @DisplayName("Test password with multiple valid special chars")
        void testPasswordMultipleValidSpecialChars() {
            assertTrue(PasswordValidator.isValidPassword("Test1@!$%*"));
        }

        @Test
        @DisplayName("Test passwords at length boundaries")
        void testPasswordLengthBoundaries() {
            assertFalse(PasswordValidator.isValidPassword("Test12!"));  // 7 chars
            assertTrue(PasswordValidator.isValidPassword("Test123!"));  // 8 chars
            assertTrue(PasswordValidator.isValidPassword("Test1234!")); // 9 chars
        }

        @Test
        @DisplayName("Test case sensitivity of validation")
        void testCaseSensitivity() {
            assertFalse(PasswordValidator.isValidPassword("test123!"));  // no uppercase
            assertFalse(PasswordValidator.isValidPassword("TEST123!"));  // no lowercase
            assertTrue(PasswordValidator.isValidPassword("Test123!"));   // both
        }

        @Test
        @DisplayName("Test password with only question mark as special char")
        void testPasswordWithOnlyQuestionMark() {
            assertTrue(PasswordValidator.isValidPassword("Test123?"));
        }

        @Test
        @DisplayName("Test password with only ampersand as special char")
        void testPasswordWithOnlyAmpersand() {
            assertTrue(PasswordValidator.isValidPassword("Test123&"));
        }

        @Test
        @DisplayName("Test password with mixed case throughout")
        void testPasswordMixedCase() {
            assertTrue(PasswordValidator.isValidPassword("TeSt123!"));
            assertTrue(PasswordValidator.isValidPassword("tEsT123!"));
        }

        @Test
        @DisplayName("Test that trim is applied before validation")
        void testTrimBehavior() {
            // Whitespace is trimmed, but password still needs valid chars
            assertFalse(PasswordValidator.isValidPassword(" Test123! "));
        }
    }

    @Nested
    @DisplayName("Special Characters Validation")
    class SpecialCharactersValidation {
        @Test
        @DisplayName("Validate @ symbol works")
        void testAtSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123@"));
        }

        @Test
        @DisplayName("Validate $ symbol works")
        void testDollarSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123$"));
        }

        @Test
        @DisplayName("Validate ! symbol works")
        void testExclamationSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123!"));
        }

        @Test
        @DisplayName("Validate % symbol works")
        void testPercentSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123%"));
        }

        @Test
        @DisplayName("Validate * symbol works")
        void testAsteriskSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123*"));
        }

        @Test
        @DisplayName("Validate ? symbol works")
        void testQuestionSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123?"));
        }

        @Test
        @DisplayName("Validate & symbol works")
        void testAmpersandSymbol() {
            assertTrue(PasswordValidator.isValidPassword("Test123&"));
        }
    }
}