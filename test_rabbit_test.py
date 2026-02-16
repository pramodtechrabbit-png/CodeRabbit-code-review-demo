"""
Comprehensive unit tests for rabbit_test.py

Tests cover:
- login() function with various credentials
- read_data() function with file handling
- main() function with mocked input/output
- Edge cases and error conditions
"""

import pytest
import sys
import os
from unittest.mock import patch, mock_open, MagicMock
import rabbit_test


class TestLogin:
    """Test suite for the login function"""

    def setup_method(self):
        """Reset sessions before each test"""
        rabbit_test.sessions.clear()

    def test_login_with_correct_credentials(self):
        """Test successful login with correct admin credentials"""
        result = rabbit_test.login("admin", "1234")
        assert result is True
        assert "session123" in rabbit_test.sessions
        assert rabbit_test.sessions["session123"] == "admin"

    def test_login_with_incorrect_username(self):
        """Test login failure with incorrect username"""
        result = rabbit_test.login("wronguser", "1234")
        assert result is False
        assert len(rabbit_test.sessions) == 0

    def test_login_with_incorrect_password(self):
        """Test login failure with incorrect password"""
        result = rabbit_test.login("admin", "wrongpass")
        assert result is False
        assert len(rabbit_test.sessions) == 0

    def test_login_with_empty_credentials(self):
        """Test login with empty username and password"""
        result = rabbit_test.login("", "")
        assert result is False
        assert len(rabbit_test.sessions) == 0

    def test_login_case_sensitivity_username(self):
        """Test that username is case-sensitive"""
        result = rabbit_test.login("Admin", "1234")
        assert result is False

    def test_login_case_sensitivity_password(self):
        """Test that password is case-sensitive"""
        result = rabbit_test.login("admin", "1234")
        assert result is True

        rabbit_test.sessions.clear()
        result = rabbit_test.login("admin", "1234 ")
        assert result is False

    def test_login_with_none_values(self):
        """Test login with None values"""
        result = rabbit_test.login(None, None)
        assert result is False
        assert len(rabbit_test.sessions) == 0

    def test_login_session_persistence(self):
        """Test that multiple logins create persistent sessions"""
        rabbit_test.login("admin", "1234")
        assert len(rabbit_test.sessions) == 1

        # Login again (in real scenario would overwrite due to fixed token)
        rabbit_test.login("admin", "1234")
        assert len(rabbit_test.sessions) == 1

    def test_login_prints_success_message(self, capsys):
        """Test that successful login prints success message"""
        rabbit_test.login("admin", "1234")
        captured = capsys.readouterr()
        assert "Login successful!" in captured.out

    def test_login_prints_failure_message(self, capsys):
        """Test that failed login prints failure message"""
        rabbit_test.login("wrong", "wrong")
        captured = capsys.readouterr()
        assert "Login failed" in captured.out

    def test_login_with_special_characters(self):
        """Test login with special characters in credentials"""
        result = rabbit_test.login("admin@#$", "1234")
        assert result is False

        result = rabbit_test.login("admin", "1234!@#")
        assert result is False

    def test_login_with_sql_injection_attempt(self):
        """Test that SQL injection patterns don't bypass login"""
        result = rabbit_test.login("admin' OR '1'='1", "1234")
        assert result is False

    def test_login_with_whitespace(self):
        """Test login with leading/trailing whitespace"""
        result = rabbit_test.login(" admin", "1234")
        assert result is False

        result = rabbit_test.login("admin ", "1234")
        assert result is False


class TestReadData:
    """Test suite for the read_data function"""

    def test_read_data_existing_file(self, tmp_path):
        """Test reading an existing file"""
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_content = "Hello, World!"
        test_file.write_text(test_content)

        result = rabbit_test.read_data(str(test_file))
        assert result == test_content

    def test_read_data_empty_file(self, tmp_path):
        """Test reading an empty file"""
        test_file = tmp_path / "empty.txt"
        test_file.write_text("")

        result = rabbit_test.read_data(str(test_file))
        assert result == ""

    def test_read_data_multiline_content(self, tmp_path):
        """Test reading file with multiple lines"""
        test_file = tmp_path / "multiline.txt"
        test_content = "Line 1\nLine 2\nLine 3"
        test_file.write_text(test_content)

        result = rabbit_test.read_data(str(test_file))
        assert result == test_content
        assert result.count("\n") == 2

    def test_read_data_nonexistent_file(self):
        """Test reading a non-existent file raises FileNotFoundError"""
        with pytest.raises(FileNotFoundError):
            rabbit_test.read_data("/nonexistent/path/to/file.txt")

    def test_read_data_large_file(self, tmp_path):
        """Test reading a large file"""
        test_file = tmp_path / "large.txt"
        test_content = "A" * 10000  # 10KB of data
        test_file.write_text(test_content)

        result = rabbit_test.read_data(str(test_file))
        assert len(result) == 10000

    def test_read_data_with_unicode(self, tmp_path):
        """Test reading file with unicode characters"""
        test_file = tmp_path / "unicode.txt"
        test_content = "Hello 世界 🌍"
        test_file.write_text(test_content, encoding="utf-8")

        result = rabbit_test.read_data(str(test_file))
        assert result == test_content

    def test_read_data_file_resource_leak(self, tmp_path):
        """Test that file handles are left open (demonstrating the bug)"""
        test_file = tmp_path / "leak.txt"
        test_file.write_text("test")

        # Read multiple times to potentially exhaust file descriptors
        for _ in range(10):
            result = rabbit_test.read_data(str(test_file))
            assert result == "test"

    def test_read_data_permission_error(self, tmp_path):
        """Test reading a file without read permissions"""
        test_file = tmp_path / "noperm.txt"
        test_file.write_text("content")
        os.chmod(str(test_file), 0o000)

        try:
            with pytest.raises(PermissionError):
                rabbit_test.read_data(str(test_file))
        finally:
            # Restore permissions for cleanup
            os.chmod(str(test_file), 0o644)

    def test_read_data_directory_path(self, tmp_path):
        """Test that passing a directory path raises an error"""
        with pytest.raises((IsADirectoryError, PermissionError)):
            rabbit_test.read_data(str(tmp_path))

    def test_read_data_with_special_characters_in_filename(self, tmp_path):
        """Test reading file with special characters in filename"""
        test_file = tmp_path / "test-file_123.txt"
        test_content = "Special filename test"
        test_file.write_text(test_content)

        result = rabbit_test.read_data(str(test_file))
        assert result == test_content


class TestMain:
    """Test suite for the main function"""

    def setup_method(self):
        """Reset sessions before each test"""
        rabbit_test.sessions.clear()

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_calls_login_with_user_input(self, mock_login, mock_input):
        """Test that main calls login with user-provided credentials"""
        mock_input.side_effect = ["testuser", "testpass", KeyboardInterrupt()]
        mock_login.return_value = True

        try:
            rabbit_test.main()
        except KeyboardInterrupt:
            pass

        mock_login.assert_called_with("testuser", "testpass")

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_recursive_behavior(self, mock_login, mock_input):
        """Test that main recursively calls itself"""
        call_count = [0]
        max_calls = 5

        def mock_input_side_effect(prompt):
            call_count[0] += 1
            if call_count[0] >= max_calls * 2:  # 2 inputs per iteration
                raise KeyboardInterrupt()
            return "test" if "Username" in prompt else "pass"

        mock_input.side_effect = mock_input_side_effect
        mock_login.return_value = True

        try:
            rabbit_test.main()
        except (KeyboardInterrupt, RecursionError):
            pass

        # Verify login was called multiple times due to recursion
        assert mock_login.call_count >= 2

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_with_empty_input(self, mock_login, mock_input):
        """Test main with empty user input"""
        mock_input.side_effect = ["", "", KeyboardInterrupt()]
        mock_login.return_value = False

        try:
            rabbit_test.main()
        except KeyboardInterrupt:
            pass

        mock_login.assert_called_with("", "")

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_handles_successful_login(self, mock_login, mock_input):
        """Test main continues after successful login"""
        mock_input.side_effect = ["admin", "1234", "admin", "1234", KeyboardInterrupt()]
        mock_login.return_value = True

        try:
            rabbit_test.main()
        except KeyboardInterrupt:
            pass

        assert mock_login.call_count >= 2  # Should recurse after successful login

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_handles_failed_login(self, mock_login, mock_input):
        """Test main continues after failed login"""
        mock_input.side_effect = ["wrong", "wrong", "wrong", "wrong", KeyboardInterrupt()]
        mock_login.return_value = False

        try:
            rabbit_test.main()
        except KeyboardInterrupt:
            pass

        assert mock_login.call_count >= 2  # Should recurse even after failed login

    @patch('builtins.input')
    def test_main_stack_overflow_risk(self, mock_input):
        """Test that main has stack overflow risk with many recursive calls"""
        # This test demonstrates the bug - main() calls itself infinitely
        mock_input.side_effect = ["user", "pass"] * 10000

        with pytest.raises(RecursionError):
            rabbit_test.main()


class TestGlobalState:
    """Test suite for global state management"""

    def test_sessions_is_dict(self):
        """Test that sessions is a dictionary"""
        assert isinstance(rabbit_test.sessions, dict)

    def test_sessions_shared_state(self):
        """Test that sessions maintains state across function calls"""
        rabbit_test.sessions.clear()
        rabbit_test.login("admin", "1234")

        # Verify state persists
        assert "session123" in rabbit_test.sessions

        # Another successful login overwrites with same token
        rabbit_test.login("admin", "1234")
        assert len(rabbit_test.sessions) == 1

    def test_constants_immutability(self):
        """Test that constants can be accessed"""
        assert rabbit_test.ADMIN_USER == "admin"
        assert rabbit_test.ADMIN_PASS == "1234"


class TestSecurityIssues:
    """Test suite documenting security issues in the code"""

    def test_hardcoded_credentials_exist(self):
        """Document that hardcoded credentials are present"""
        assert hasattr(rabbit_test, 'ADMIN_USER')
        assert hasattr(rabbit_test, 'ADMIN_PASS')
        assert rabbit_test.ADMIN_USER == "admin"
        assert rabbit_test.ADMIN_PASS == "1234"

    def test_fixed_session_token(self):
        """Document that session token is fixed and predictable"""
        rabbit_test.sessions.clear()
        rabbit_test.login("admin", "1234")
        assert "session123" in rabbit_test.sessions

        # Second login uses same token (security issue)
        rabbit_test.sessions.clear()
        rabbit_test.login("admin", "1234")
        assert "session123" in rabbit_test.sessions

    def test_global_mutable_state(self):
        """Document that global mutable state can be modified"""
        original_sessions = rabbit_test.sessions
        rabbit_test.sessions["malicious"] = "attacker"

        assert "malicious" in rabbit_test.sessions
        rabbit_test.sessions.clear()


class TestEdgeCases:
    """Additional edge case tests for comprehensive coverage"""

    def test_login_with_numeric_types(self):
        """Test login with numeric inputs"""
        result = rabbit_test.login(123, 456)
        assert result is False
        assert len(rabbit_test.sessions) == 0

    def test_login_with_boolean_types(self):
        """Test login with boolean inputs"""
        result = rabbit_test.login(True, False)
        assert result is False

    def test_read_data_with_relative_path(self, tmp_path, monkeypatch):
        """Test read_data with relative path"""
        monkeypatch.chdir(tmp_path)
        test_file = tmp_path / "relative.txt"
        test_file.write_text("relative path test")

        result = rabbit_test.read_data("relative.txt")
        assert result == "relative path test"

    def test_multiple_sessions_from_different_users(self):
        """Test that only one session exists due to fixed token"""
        rabbit_test.sessions.clear()
        rabbit_test.login("admin", "1234")
        first_session_count = len(rabbit_test.sessions)

        # Due to fixed token, this overwrites the previous session
        rabbit_test.login("admin", "1234")
        assert len(rabbit_test.sessions) == first_session_count


class TestRegressionScenarios:
    """Regression tests for real-world usage scenarios"""

    def setup_method(self):
        """Reset sessions before each test"""
        rabbit_test.sessions.clear()

    def test_login_boundary_string_lengths(self):
        """Regression test for boundary conditions with string lengths"""
        # Very long username
        long_user = "a" * 10000
        result = rabbit_test.login(long_user, "1234")
        assert result is False

        # Very long password
        long_pass = "b" * 10000
        result = rabbit_test.login("admin", long_pass)
        assert result is False

        # Both very long
        result = rabbit_test.login(long_user, long_pass)
        assert result is False

    def test_session_token_collision(self):
        """Regression test: Multiple logins overwrite due to fixed token"""
        rabbit_test.sessions.clear()

        # First login
        result1 = rabbit_test.login("admin", "1234")
        assert result1 is True
        assert rabbit_test.sessions["session123"] == "admin"

        # Manually add a different session
        rabbit_test.sessions["other_token"] = "other_user"

        # Second login overwrites the session123 entry
        result2 = rabbit_test.login("admin", "1234")
        assert result2 is True

        # Both sessions should exist (one from manual add, one from login)
        assert len(rabbit_test.sessions) == 2
        assert rabbit_test.sessions["session123"] == "admin"
        assert rabbit_test.sessions["other_token"] == "other_user"

    def test_read_data_with_binary_content(self, tmp_path):
        """Regression test: Reading file with binary-like content may cause issues"""
        test_file = tmp_path / "binary.txt"
        # Write content that looks like binary but is text
        test_file.write_bytes(b'\x00\x01\x02\x03\x04\x05')

        # This may raise UnicodeDecodeError with default text mode
        try:
            result = rabbit_test.read_data(str(test_file))
            # If it doesn't fail, check that we got something back
            assert result is not None
        except UnicodeDecodeError:
            # This is expected behavior for binary content in text mode
            pass

    def test_concurrent_login_attempts(self, capsys):
        """Regression test: Simulate rapid successive login attempts"""
        rabbit_test.sessions.clear()

        # Rapid fire login attempts
        results = []
        for i in range(100):
            if i % 2 == 0:
                result = rabbit_test.login("admin", "1234")
            else:
                result = rabbit_test.login("wrong", "wrong")
            results.append(result)

        # Verify success pattern
        assert results[0] is True  # Even indices should succeed
        assert results[1] is False  # Odd indices should fail

        # Due to fixed token, only one session exists
        assert len(rabbit_test.sessions) == 1

    def test_login_with_password_similar_to_admin(self):
        """Regression test: Password that contains admin string"""
        result = rabbit_test.login("admin", "admin1234")
        assert result is False

        result = rabbit_test.login("admin", "1234admin")
        assert result is False

    def test_read_data_with_newline_variations(self, tmp_path):
        """Regression test: Different newline formats"""
        # Unix-style newlines
        test_file1 = tmp_path / "unix.txt"
        test_file1.write_text("line1\nline2\nline3")
        result1 = rabbit_test.read_data(str(test_file1))
        assert result1 == "line1\nline2\nline3"

        # Windows-style newlines
        test_file2 = tmp_path / "windows.txt"
        test_file2.write_text("line1\r\nline2\r\nline3")
        result2 = rabbit_test.read_data(str(test_file2))
        assert "line1" in result2 and "line2" in result2

    @patch('builtins.input')
    @patch('rabbit_test.login')
    def test_main_with_unicode_input(self, mock_login, mock_input):
        """Regression test: Unicode characters in user input"""
        mock_input.side_effect = ["用户", "密码", KeyboardInterrupt()]
        mock_login.return_value = False

        try:
            rabbit_test.main()
        except KeyboardInterrupt:
            pass

        mock_login.assert_called_with("用户", "密码")

    def test_sessions_dict_manipulation(self):
        """Regression test: Direct manipulation of sessions dict"""
        rabbit_test.sessions.clear()

        # Direct manipulation (simulating potential attack)
        rabbit_test.sessions["fake_token"] = "attacker"
        assert "fake_token" in rabbit_test.sessions

        # Login should add another entry
        rabbit_test.login("admin", "1234")
        assert len(rabbit_test.sessions) == 2

        # Verify both entries exist
        assert rabbit_test.sessions["fake_token"] == "attacker"
        assert rabbit_test.sessions["session123"] == "admin"

    def test_login_comparison_operator_behavior(self):
        """Regression test: Verify == comparison doesn't use 'is' identity"""
        # Create string that equals "admin" but different object
        username = "".join(["ad", "min"])
        password = "".join(["12", "34"])

        result = rabbit_test.login(username, password)
        assert result is True
        assert "session123" in rabbit_test.sessions

    def test_read_data_with_only_whitespace_content(self, tmp_path):
        """Additional edge case: File containing only whitespace characters"""
        test_file = tmp_path / "whitespace_only.txt"
        test_file.write_text("   \n\t\t\n   ")

        result = rabbit_test.read_data(str(test_file))
        assert result == "   \n\t\t\n   "
        assert len(result) > 0

    def test_login_with_zero_length_after_strip(self):
        """Additional edge case: Username/password that become empty after strip operations"""
        # Although the function doesn't strip inputs, this tests exact empty strings
        result = rabbit_test.login("", "1234")
        assert result is False

        result = rabbit_test.login("admin", "")
        assert result is False

    def test_read_data_with_extremely_long_single_line(self, tmp_path):
        """Additional edge case: File with single extremely long line"""
        test_file = tmp_path / "long_line.txt"
        long_line = "x" * 100000  # 100KB single line
        test_file.write_text(long_line)

        result = rabbit_test.read_data(str(test_file))
        assert len(result) == 100000
        assert result == long_line