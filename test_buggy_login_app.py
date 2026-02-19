"""
Comprehensive test suite for buggy_login_app.py
Tests cover main functionality, database operations, business logic,
edge cases, security issues, and error handling.
"""

import pytest
import os
import json
import hashlib
import time
import sqlite3
import tempfile
from unittest.mock import patch, mock_open, MagicMock, call
import buggy_login_app


class TestHashPassword:
    """Tests for hash_password function"""

    def test_hash_password_basic(self):
        """Test basic password hashing"""
        result = buggy_login_app.hash_password("password123")
        assert isinstance(result, str)
        assert len(result) == 32  # MD5 produces 32-char hex string

    def test_hash_password_consistency(self):
        """Test that same password produces same hash"""
        hash1 = buggy_login_app.hash_password("test123")
        hash2 = buggy_login_app.hash_password("test123")
        assert hash1 == hash2

    def test_hash_password_different_inputs(self):
        """Test that different passwords produce different hashes"""
        hash1 = buggy_login_app.hash_password("password1")
        hash2 = buggy_login_app.hash_password("password2")
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """Test hashing empty string"""
        result = buggy_login_app.hash_password("")
        expected = hashlib.md5(b"").hexdigest()
        assert result == expected

    def test_hash_password_unicode(self):
        """Test hashing unicode characters"""
        result = buggy_login_app.hash_password("пароль日本語")
        assert isinstance(result, str)
        assert len(result) == 32

    def test_hash_password_long_input(self):
        """Test hashing very long password"""
        long_password = "a" * 10000
        result = buggy_login_app.hash_password(long_password)
        assert len(result) == 32


class TestLog:
    """Tests for log function"""

    @patch("builtins.open", new_callable=mock_open)
    @patch("time.ctime", return_value="Wed Jan 1 00:00:00 2025")
    def test_log_writes_message(self, mock_ctime, mock_file):
        """Test that log writes formatted message"""
        buggy_login_app.log("Test message")
        mock_file.assert_called_once_with("app.log", "a")
        handle = mock_file()
        handle.write.assert_called_once_with("Wed Jan 1 00:00:00 2025 - Test message\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_log_empty_message(self, mock_file):
        """Test logging empty message"""
        buggy_login_app.log("")
        handle = mock_file()
        assert handle.write.called

    @patch("builtins.open", new_callable=mock_open)
    def test_log_unicode_message(self, mock_file):
        """Test logging unicode characters"""
        buggy_login_app.log("User 日本語 performed action")
        assert mock_file.called


class TestDatabaseFunctions:
    """Tests for database operations"""

    def setup_method(self):
        """Create a temporary database for each test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db_path = self.temp_db.name
        self.temp_db.close()

    def teardown_method(self):
        """Clean up temporary database"""
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    @patch("sqlite3.connect")
    def test_init_db_creates_table(self, mock_connect):
        """Test that init_db creates users table"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        buggy_login_app.init_db()

        mock_cursor.execute.assert_called_once()
        assert "CREATE TABLE" in mock_cursor.execute.call_args[0][0]
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_add_user_db_inserts_user(self, mock_connect):
        """Test adding user to database"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        buggy_login_app.add_user_db("testuser", "testpass")

        mock_cursor.execute.assert_called_once()
        assert "INSERT INTO users" in mock_cursor.execute.call_args[0][0]
        assert mock_cursor.execute.call_args[0][1] == ("testuser", "testpass")
        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_get_user_db_retrieves_user(self, mock_connect):
        """Test retrieving user from database"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, "testuser", "testpass")

        result = buggy_login_app.get_user_db("testuser")

        mock_cursor.execute.assert_called_once()
        assert "SELECT" in mock_cursor.execute.call_args[0][0]
        assert result == (1, "testuser", "testpass")
        mock_conn.close.assert_called_once()

    @patch("sqlite3.connect")
    def test_get_user_db_nonexistent_user(self, mock_connect):
        """Test retrieving nonexistent user"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        result = buggy_login_app.get_user_db("nonexistent")

        assert result is None

    def test_init_db_real_database(self):
        """Test init_db with real database"""
        with patch("sqlite3.connect", return_value=sqlite3.connect(self.temp_db_path)):
            buggy_login_app.init_db()

        # Verify table was created
        conn = sqlite3.connect(self.temp_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        conn.close()
        assert result is not None


class TestAuthenticate:
    """Tests for authenticate function"""

    @patch("builtins.print")
    def test_authenticate_superuser(self, mock_print):
        """Test authenticating hardcoded superuser"""
        result = buggy_login_app.authenticate("superuser", "superpass")
        assert result is True

    @patch("buggy_login_app.get_user_db")
    def test_authenticate_valid_user(self, mock_get_user):
        """Test authenticating valid database user"""
        mock_get_user.return_value = (1, "testuser", "testpass")
        result = buggy_login_app.authenticate("testuser", "testpass")
        assert result is True

    @patch("buggy_login_app.get_user_db")
    def test_authenticate_wrong_password(self, mock_get_user):
        """Test authenticating with wrong password"""
        mock_get_user.return_value = (1, "testuser", "correctpass")
        result = buggy_login_app.authenticate("testuser", "wrongpass")
        assert result is False

    @patch("buggy_login_app.get_user_db")
    def test_authenticate_nonexistent_user(self, mock_get_user):
        """Test authenticating nonexistent user"""
        mock_get_user.return_value = None
        result = buggy_login_app.authenticate("nonexistent", "password")
        assert result is False

    @patch("buggy_login_app.get_user_db")
    def test_authenticate_empty_credentials(self, mock_get_user):
        """Test authenticating with empty credentials"""
        mock_get_user.return_value = None
        result = buggy_login_app.authenticate("", "")
        assert result is False

    @patch("buggy_login_app.get_user_db")
    def test_authenticate_plaintext_password_comparison(self, mock_get_user):
        """Test that password comparison is plaintext (security issue)"""
        mock_get_user.return_value = (1, "user", "password123")
        # Passwords are compared in plaintext, not hashed
        result = buggy_login_app.authenticate("user", "password123")
        assert result is True


class TestCreateSession:
    """Tests for create_session function"""

    def setup_method(self):
        """Reset SESSIONS before each test"""
        buggy_login_app.SESSIONS.clear()

    @patch("random.randint", return_value=5555)
    def test_create_session_basic(self, mock_random):
        """Test creating a session"""
        before_time = time.time()
        token = buggy_login_app.create_session("testuser")
        after_time = time.time()

        assert token == "5555"
        assert "5555" in buggy_login_app.SESSIONS
        session = buggy_login_app.SESSIONS["5555"]
        assert session["username"] == "testuser"
        assert before_time <= session["time"] <= after_time

    @patch("random.randint")
    def test_create_session_multiple_users(self, mock_random):
        """Test creating multiple sessions"""
        mock_random.side_effect = [1111, 2222, 3333]

        token1 = buggy_login_app.create_session("user1")
        token2 = buggy_login_app.create_session("user2")
        token3 = buggy_login_app.create_session("user3")

        assert len(buggy_login_app.SESSIONS) == 3
        assert token1 == "1111"
        assert token2 == "2222"
        assert token3 == "3333"

    @patch("random.randint", return_value=5000)
    def test_create_session_collision(self, mock_random):
        """Test session token collision"""
        token1 = buggy_login_app.create_session("user1")
        token2 = buggy_login_app.create_session("user2")

        # Second session overwrites first
        assert buggy_login_app.SESSIONS["5000"]["username"] == "user2"

    @patch("random.randint", return_value=9999)
    def test_create_session_empty_username(self, mock_random):
        """Test creating session with empty username"""
        token = buggy_login_app.create_session("")
        assert buggy_login_app.SESSIONS["9999"]["username"] == ""


class TestFileHandling:
    """Tests for read_config and write_config functions"""

    @patch("builtins.open", mock_open(read_data='{"key": "value"}'))
    def test_read_config_basic(self):
        """Test reading basic config file"""
        result = buggy_login_app.read_config("config.json")
        assert result == {"key": "value"}

    @patch("builtins.open", mock_open(read_data='{"nested": {"key": "value"}}'))
    def test_read_config_nested(self):
        """Test reading nested config"""
        result = buggy_login_app.read_config("config.json")
        assert result["nested"]["key"] == "value"

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_config_file_not_found(self, mock_file):
        """Test reading non-existent file"""
        with pytest.raises(FileNotFoundError):
            buggy_login_app.read_config("nonexistent.json")

    @patch("builtins.open", mock_open(read_data='invalid json'))
    def test_read_config_invalid_json(self):
        """Test reading invalid JSON"""
        with pytest.raises(json.JSONDecodeError):
            buggy_login_app.read_config("invalid.json")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_write_config_basic(self, mock_json_dump, mock_file):
        """Test writing basic config"""
        data = {"key": "value"}
        buggy_login_app.write_config("config.json", data)
        mock_file.assert_called_once_with("config.json", "w")
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_write_config_closes_file(self, mock_json_dump, mock_file):
        """Test that write_config closes the file"""
        buggy_login_app.write_config("config.json", {"key": "value"})
        handle = mock_file()
        handle.close.assert_called_once()

    @patch("builtins.open", side_effect=PermissionError)
    def test_write_config_permission_error(self, mock_file):
        """Test writing config with permission error"""
        with pytest.raises(PermissionError):
            buggy_login_app.write_config("config.json", {"key": "value"})


class TestLogin:
    """Tests for login function"""

    def setup_method(self):
        """Reset state before each test"""
        buggy_login_app.SESSIONS.clear()

    @patch("buggy_login_app.authenticate", return_value=True)
    @patch("random.randint", return_value=7777)
    @patch("builtins.print")
    def test_login_success(self, mock_print, mock_random, mock_auth):
        """Test successful login"""
        buggy_login_app.login("testuser", "testpass")
        mock_print.assert_called_with("Login successful! Session: 7777")
        assert "7777" in buggy_login_app.SESSIONS

    @patch("buggy_login_app.authenticate", return_value=False)
    @patch("builtins.print")
    def test_login_failure(self, mock_print, mock_auth):
        """Test failed login"""
        buggy_login_app.login("testuser", "wrongpass")
        mock_print.assert_called_with("Login failed!")
        assert len(buggy_login_app.SESSIONS) == 0

    @patch("buggy_login_app.authenticate", return_value=True)
    @patch("random.randint", return_value=8888)
    @patch("builtins.print")
    def test_login_creates_session(self, mock_print, mock_random, mock_auth):
        """Test that login creates session"""
        buggy_login_app.login("user", "pass")
        assert "8888" in buggy_login_app.SESSIONS
        assert buggy_login_app.SESSIONS["8888"]["username"] == "user"


class TestAddUser:
    """Tests for add_user function"""

    def setup_method(self):
        """Reset USERS before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "guest", "password": "guest"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_basic(self, mock_file):
        """Test adding a new user"""
        initial_count = len(buggy_login_app.USERS)
        buggy_login_app.add_user("newuser", "newpass")
        assert len(buggy_login_app.USERS) == initial_count + 1
        assert buggy_login_app.USERS[-1]["username"] == "newuser"
        assert buggy_login_app.USERS[-1]["password"] == "newpass"

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_logs_password(self, mock_file):
        """Test that add_user logs password"""
        buggy_login_app.add_user("user", "secret123")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secret123" in str(call) for call in write_calls)

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_duplicate_username(self, mock_file):
        """Test adding duplicate username"""
        buggy_login_app.add_user("admin", "newpass")
        # Should succeed since there's no duplicate check
        assert len([u for u in buggy_login_app.USERS if u["username"] == "admin"]) >= 2

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_empty_username(self, mock_file):
        """Test adding user with empty username"""
        buggy_login_app.add_user("", "password")
        assert buggy_login_app.USERS[-1]["username"] == ""


class TestResetPassword:
    """Tests for reset_password function"""

    def setup_method(self):
        """Reset USERS before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "guest", "password": "guest"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_success(self, mock_file):
        """Test successful password reset"""
        result = buggy_login_app.reset_password("admin", "newpass")
        assert result is True
        admin_user = next(u for u in buggy_login_app.USERS if u["username"] == "admin")
        assert admin_user["password"] == "newpass"

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_nonexistent_user(self, mock_file):
        """Test password reset for nonexistent user"""
        result = buggy_login_app.reset_password("nonexistent", "newpass")
        assert result is False

    @patch("builtins.open", new_callable=mock_open)
    def test_reset_password_logs_new_password(self, mock_file):
        """Test that reset_password logs the new password"""
        buggy_login_app.reset_password("admin", "newsecret")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("newsecret" in str(call) for call in write_calls)


class TestBusinessLogic:
    """Tests for business logic functions"""

    def test_calculate_total_basic(self):
        """Test calculating total for items"""
        items = [
            {"price": 10.0, "quantity": 2},
            {"price": 5.0, "quantity": 3}
        ]
        result = buggy_login_app.calculate_total(items)
        assert result == 35.0

    def test_calculate_total_empty_list(self):
        """Test calculating total for empty list"""
        result = buggy_login_app.calculate_total([])
        assert result == 0

    def test_calculate_total_single_item(self):
        """Test calculating total for single item"""
        items = [{"price": 100.0, "quantity": 1}]
        result = buggy_login_app.calculate_total(items)
        assert result == 100.0

    def test_calculate_total_zero_quantity(self):
        """Test calculating total with zero quantity"""
        items = [{"price": 10.0, "quantity": 0}]
        result = buggy_login_app.calculate_total(items)
        assert result == 0

    def test_calculate_total_fractional_prices(self):
        """Test calculating total with fractional prices"""
        items = [{"price": 9.99, "quantity": 3}]
        result = buggy_login_app.calculate_total(items)
        assert abs(result - 29.97) < 0.01

    def test_apply_discount_basic(self):
        """Test applying discount"""
        result = buggy_login_app.apply_discount(100.0, 10)
        assert result == 90.0

    def test_apply_discount_zero(self):
        """Test applying zero discount"""
        result = buggy_login_app.apply_discount(100.0, 0)
        assert result == 100.0

    def test_apply_discount_hundred_percent(self):
        """Test applying 100% discount"""
        result = buggy_login_app.apply_discount(100.0, 100)
        assert result == 0.0

    def test_apply_discount_fractional(self):
        """Test applying fractional discount"""
        result = buggy_login_app.apply_discount(100.0, 12.5)
        assert result == 87.5

    def test_apply_discount_negative_total(self):
        """Test applying discount to negative total"""
        result = buggy_login_app.apply_discount(-100.0, 10)
        assert result == -90.0

    def test_generate_invoice_basic(self):
        """Test generating invoice"""
        items = [{"price": 10.0, "quantity": 2}]
        invoice = buggy_login_app.generate_invoice("ORDER-001", items)

        assert invoice["order_id"] == "ORDER-001"
        assert invoice["items"] == items
        assert invoice["total"] == 20.0
        assert "date" in invoice

    def test_generate_invoice_empty_items(self):
        """Test generating invoice with empty items"""
        invoice = buggy_login_app.generate_invoice("ORDER-002", [])
        assert invoice["total"] == 0

    def test_generate_invoice_multiple_items(self):
        """Test generating invoice with multiple items"""
        items = [
            {"price": 10.0, "quantity": 2},
            {"price": 5.0, "quantity": 3},
            {"price": 20.0, "quantity": 1}
        ]
        invoice = buggy_login_app.generate_invoice("ORDER-003", items)
        assert invoice["total"] == 55.0


class TestAdminOperations:
    """Tests for admin operations"""

    def setup_method(self):
        """Reset USERS before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "guest", "password": "guest"},
            {"username": "test", "password": "test123"}
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_user_success(self, mock_file):
        """Test deleting a user"""
        initial_count = len(buggy_login_app.USERS)
        buggy_login_app.delete_user("guest")
        assert len(buggy_login_app.USERS) == initial_count - 1
        assert not any(u["username"] == "guest" for u in buggy_login_app.USERS)

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_user_nonexistent(self, mock_file):
        """Test deleting nonexistent user"""
        initial_count = len(buggy_login_app.USERS)
        buggy_login_app.delete_user("nonexistent")
        assert len(buggy_login_app.USERS) == initial_count

    @patch("builtins.open", new_callable=mock_open)
    def test_delete_user_removes_all_matches(self, mock_file):
        """Test deleting removes all users with same name"""
        buggy_login_app.USERS.append({"username": "admin", "password": "other"})
        buggy_login_app.delete_user("admin")
        assert not any(u["username"] == "admin" for u in buggy_login_app.USERS)

    def test_list_users_returns_all_users(self):
        """Test listing all users"""
        result = buggy_login_app.list_users()
        assert len(result) == 3
        assert result == buggy_login_app.USERS

    def test_list_users_empty(self):
        """Test listing users when list is empty"""
        buggy_login_app.USERS.clear()
        result = buggy_login_app.list_users()
        assert result == []


class TestHeavyComputation:
    """Tests for heavy_computation function"""

    def test_heavy_computation_returns_int(self):
        """Test that heavy_computation returns integer"""
        result = buggy_login_app.heavy_computation()
        assert isinstance(result, int)

    def test_heavy_computation_correct_result(self):
        """Test that heavy_computation returns correct sum"""
        # Sum of 0 to 9999999 = n * (n-1) / 2 where n = 10000000
        expected = sum(range(10000000))
        result = buggy_login_app.heavy_computation()
        assert result == expected

    def test_heavy_computation_positive(self):
        """Test that heavy_computation returns positive number"""
        result = buggy_login_app.heavy_computation()
        assert result > 0


class TestIntegration:
    """Integration tests combining multiple functions"""

    def setup_method(self):
        """Reset state before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "guest", "password": "guest"}
        ])
        buggy_login_app.SESSIONS.clear()

    @patch("builtins.open", new_callable=mock_open)
    @patch("buggy_login_app.authenticate")
    @patch("random.randint", return_value=9999)
    @patch("builtins.print")
    def test_add_user_and_login(self, mock_print, mock_random, mock_auth, mock_file):
        """Test adding user and logging in"""
        buggy_login_app.add_user("newuser", "newpass")

        # Mock authenticate to check USERS list
        def auth_side_effect(username, password):
            for user in buggy_login_app.USERS:
                if user["username"] == username and user["password"] == password:
                    return True
            return False

        mock_auth.side_effect = auth_side_effect

        buggy_login_app.login("newuser", "newpass")
        assert "9999" in buggy_login_app.SESSIONS

    @patch("builtins.open", new_callable=mock_open)
    @patch("buggy_login_app.authenticate")
    @patch("builtins.print")
    def test_reset_password_and_login(self, mock_print, mock_auth, mock_file):
        """Test resetting password and logging in"""
        buggy_login_app.reset_password("admin", "newpass123")

        # Mock authenticate
        def auth_side_effect(username, password):
            for user in buggy_login_app.USERS:
                if user["username"] == username and user["password"] == password:
                    return True
            return False

        mock_auth.side_effect = auth_side_effect

        result1 = buggy_login_app.authenticate("admin", "admin123")
        result2 = buggy_login_app.authenticate("admin", "newpass123")

        assert result2 is True

    def test_invoice_with_discount_workflow(self):
        """Test complete invoice workflow with discount"""
        items = [
            {"price": 100.0, "quantity": 2},
            {"price": 50.0, "quantity": 1}
        ]

        # Calculate total
        total = buggy_login_app.calculate_total(items)
        assert total == 250.0

        # Apply discount
        discounted = buggy_login_app.apply_discount(total, 20)
        assert discounted == 200.0

        # Generate invoice
        invoice = buggy_login_app.generate_invoice("ORDER-100", items)
        assert invoice["total"] == 250.0  # Invoice uses original total

    @patch("builtins.open", new_callable=mock_open)
    def test_add_list_delete_workflow(self, mock_file):
        """Test add, list, delete workflow"""
        initial_count = len(buggy_login_app.list_users())

        buggy_login_app.add_user("tempuser", "temppass")
        assert len(buggy_login_app.list_users()) == initial_count + 1

        buggy_login_app.delete_user("tempuser")
        assert len(buggy_login_app.list_users()) == initial_count


class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def setup_method(self):
        """Reset state before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"}
        ])
        buggy_login_app.SESSIONS.clear()

    @patch("buggy_login_app.authenticate", return_value=True)
    @patch("random.randint", return_value=1000)
    @patch("builtins.print")
    def test_login_with_very_long_username(self, mock_print, mock_random, mock_auth):
        """Test login with very long username"""
        long_username = "u" * 10000
        buggy_login_app.login(long_username, "pass")
        assert "1000" in buggy_login_app.SESSIONS

    def test_calculate_total_with_negative_prices(self):
        """Test calculate_total with negative prices"""
        items = [{"price": -10.0, "quantity": 2}]
        result = buggy_login_app.calculate_total(items)
        assert result == -20.0

    def test_calculate_total_with_large_numbers(self):
        """Test calculate_total with large numbers"""
        items = [{"price": 1000000.0, "quantity": 1000}]
        result = buggy_login_app.calculate_total(items)
        assert result == 1000000000.0

    def test_apply_discount_over_100_percent(self):
        """Test applying discount over 100%"""
        result = buggy_login_app.apply_discount(100.0, 150)
        assert result == -50.0

    def test_apply_discount_negative_discount(self):
        """Test applying negative discount (increases price)"""
        result = buggy_login_app.apply_discount(100.0, -10)
        assert result == 110.0

    def test_generate_invoice_with_unicode_order_id(self):
        """Test generating invoice with unicode order ID"""
        items = [{"price": 10.0, "quantity": 1}]
        invoice = buggy_login_app.generate_invoice("订单-123", items)
        assert invoice["order_id"] == "订单-123"

    @patch("builtins.open", new_callable=mock_open)
    def test_add_user_with_dict_like_values(self, mock_file):
        """Test adding user with special characters"""
        buggy_login_app.add_user("user{}", "pass[]")
        assert buggy_login_app.USERS[-1]["username"] == "user{}"

    def test_list_users_returns_reference(self):
        """Test that list_users returns actual list reference"""
        users = buggy_login_app.list_users()
        users.append({"username": "hacker", "password": "hack"})
        # This modifies the actual USERS list (potential security issue)
        assert len(buggy_login_app.USERS) == 2


class TestSecurityIssues:
    """Tests documenting security issues in the code"""

    @patch("builtins.open", new_callable=mock_open)
    def test_password_stored_in_plaintext_memory(self, mock_file):
        """Document passwords stored in plaintext in memory"""
        buggy_login_app.add_user("user", "mysecretpassword")
        user = next(u for u in buggy_login_app.USERS if u["username"] == "user")
        assert user["password"] == "mysecretpassword"

    @patch("builtins.open", new_callable=mock_open)
    def test_passwords_logged_to_file(self, mock_file):
        """Document passwords logged to file"""
        buggy_login_app.add_user("user", "secret123")
        handle = mock_file()
        write_calls = [str(call) for call in handle.write.call_args_list]
        assert any("secret123" in str(call) for call in write_calls)

    def test_weak_md5_hashing(self):
        """Document use of weak MD5 hashing"""
        result = buggy_login_app.hash_password("password")
        assert result == hashlib.md5(b"password").hexdigest()

    def test_hardcoded_superuser_credentials(self):
        """Document hardcoded superuser credentials"""
        result = buggy_login_app.authenticate("superuser", "superpass")
        assert result is True

    @patch("random.randint", return_value=5000)
    def test_weak_session_tokens(self, mock_random):
        """Document weak 4-digit session tokens"""
        token = buggy_login_app.create_session("user")
        assert token == "5000"
        assert len(token) == 4

    @patch("buggy_login_app.get_user_db")
    def test_plaintext_password_in_database(self, mock_get_user):
        """Document plaintext passwords in database"""
        mock_get_user.return_value = (1, "user", "plaintext_password")
        result = buggy_login_app.authenticate("user", "plaintext_password")
        assert result is True

    def test_file_handle_not_closed_in_read_config(self):
        """Document file handle leak in read_config"""
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            result = buggy_login_app.read_config("config.json")
            assert result == {"key": "value"}

    @patch("sqlite3.connect")
    def test_sql_injection_vulnerability(self, mock_connect):
        """Document potential SQL injection in get_user_db"""
        # The function uses parameterized queries, which is good
        # but this test documents that we should verify this
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        buggy_login_app.get_user_db("admin' OR '1'='1")

        # Verify parameterized query is used (safe)
        call_args = mock_cursor.execute.call_args[0]
        assert "?" in call_args[0]  # Parameterized query


class TestRegressionAndBoundary:
    """Additional regression and boundary tests for enhanced coverage"""

    def setup_method(self):
        """Reset state before each test"""
        buggy_login_app.USERS.clear()
        buggy_login_app.USERS.extend([
            {"username": "admin", "password": "admin123"},
            {"username": "guest", "password": "guest"}
        ])
        buggy_login_app.SESSIONS.clear()

    def test_calculate_total_precision_accumulation(self):
        """Test precision issues with many small fractional items"""
        items = [{"price": 0.01, "quantity": 1} for _ in range(1000)]
        result = buggy_login_app.calculate_total(items)
        # Should be 10.0 but may have floating point errors
        assert abs(result - 10.0) < 0.01

    def test_apply_discount_cascading(self):
        """Test applying multiple discounts in sequence"""
        total = 1000.0
        total = buggy_login_app.apply_discount(total, 10)  # 900
        total = buggy_login_app.apply_discount(total, 10)  # 810
        total = buggy_login_app.apply_discount(total, 10)  # 729
        assert abs(total - 729.0) < 0.01

    def test_invoice_generation_with_complex_items(self):
        """Test invoice with various item types"""
        items = [
            {"price": 99.99, "quantity": 3},
            {"price": 0.01, "quantity": 100},
            {"price": 1000.00, "quantity": 1},
            {"price": 15.50, "quantity": 7}
        ]
        invoice = buggy_login_app.generate_invoice("ORDER-COMPLEX-001", items)

        expected_total = (99.99 * 3) + (0.01 * 100) + (1000.00 * 1) + (15.50 * 7)
        assert abs(invoice["total"] - expected_total) < 0.01
        assert invoice["order_id"] == "ORDER-COMPLEX-001"
        assert len(invoice["items"]) == 4

    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print")
    def test_user_lifecycle_complete_workflow(self, mock_print, mock_file):
        """Complete user lifecycle: add, modify, use, delete"""
        # Add user
        buggy_login_app.add_user("lifecycle_user", "initial_pass")
        assert any(u["username"] == "lifecycle_user" for u in buggy_login_app.USERS)

        # Reset password
        buggy_login_app.reset_password("lifecycle_user", "changed_pass")
        user = next(u for u in buggy_login_app.USERS if u["username"] == "lifecycle_user")
        assert user["password"] == "changed_pass"

        # Delete user
        buggy_login_app.delete_user("lifecycle_user")
        assert not any(u["username"] == "lifecycle_user" for u in buggy_login_app.USERS)

    @patch("buggy_login_app.authenticate", return_value=True)
    @patch("random.randint")
    @patch("builtins.print")
    def test_session_management_stress(self, mock_print, mock_random, mock_auth):
        """Stress test session management with many sessions"""
        mock_random.side_effect = range(1000, 1100)

        # Create 100 sessions
        for i in range(100):
            buggy_login_app.login(f"user{i}", "password")

        assert len(buggy_login_app.SESSIONS) == 100

        # Verify each session has correct structure
        for token_str in [str(i) for i in range(1000, 1100)]:
            if token_str in buggy_login_app.SESSIONS:
                session = buggy_login_app.SESSIONS[token_str]
                assert "username" in session
                assert "time" in session

    def test_business_logic_edge_case_zero_items(self):
        """Test business logic with zero-value items"""
        items = [
            {"price": 0, "quantity": 0},
            {"price": 0, "quantity": 100},
            {"price": 100, "quantity": 0}
        ]
        total = buggy_login_app.calculate_total(items)
        assert total == 0

        invoice = buggy_login_app.generate_invoice("ORDER-ZERO", items)
        assert invoice["total"] == 0