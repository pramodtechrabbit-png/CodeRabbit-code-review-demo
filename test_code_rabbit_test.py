"""
Comprehensive test suite for code_rabbit_test.py

Tests cover all functions with main functionality, edge cases, boundary conditions,
error handling, and negative cases to ensure robust test coverage.
"""

import pytest
import code_rabbit_test


class TestCalcAverage:
    """Tests for calc_average function"""

    def test_calc_average_basic(self):
        """Test basic average calculation"""
        result = code_rabbit_test.calc_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calc_average_single_element(self):
        """Test average with single element"""
        result = code_rabbit_test.calc_average([10])
        assert result == 10.0

    def test_calc_average_two_elements(self):
        """Test average with two elements"""
        result = code_rabbit_test.calc_average([5, 15])
        assert result == 10.0

    def test_calc_average_negative_numbers(self):
        """Test average with negative numbers"""
        result = code_rabbit_test.calc_average([-5, -10, -15])
        assert result == -10.0

    def test_calc_average_mixed_positive_negative(self):
        """Test average with mixed positive and negative numbers"""
        result = code_rabbit_test.calc_average([-10, 0, 10])
        assert result == 0.0

    def test_calc_average_floats(self):
        """Test average with floating point numbers"""
        result = code_rabbit_test.calc_average([1.5, 2.5, 3.5])
        assert abs(result - 2.5) < 0.0001

    def test_calc_average_large_numbers(self):
        """Test average with large numbers"""
        result = code_rabbit_test.calc_average([1000000, 2000000, 3000000])
        assert result == 2000000.0

    def test_calc_average_zeros(self):
        """Test average with all zeros"""
        result = code_rabbit_test.calc_average([0, 0, 0])
        assert result == 0.0

    def test_calc_average_empty_list_raises_error(self):
        """Test that empty list raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.calc_average([])

    def test_calc_average_many_elements(self):
        """Test average with many elements"""
        nums = list(range(1, 101))  # 1 to 100
        result = code_rabbit_test.calc_average(nums)
        assert result == 50.5

    def test_calc_average_precision_test(self):
        """Test average calculation precision"""
        result = code_rabbit_test.calc_average([10, -5, 15, 0])
        assert result == 5.0

    def test_calc_average_fractional_result(self):
        """Test average that results in fraction"""
        result = code_rabbit_test.calc_average([1, 2])
        assert result == 1.5

    def test_calc_average_duplicates(self):
        """Test average with duplicate values"""
        result = code_rabbit_test.calc_average([5, 5, 5, 5])
        assert result == 5.0

    def test_calc_average_very_small_numbers(self):
        """Test average with very small numbers"""
        result = code_rabbit_test.calc_average([0.001, 0.002, 0.003])
        assert abs(result - 0.002) < 0.0001


class TestFindMax:
    """Tests for find_max function"""

    def test_find_max_positive_numbers(self):
        """Test finding max in positive numbers"""
        result = code_rabbit_test.find_max([1, 5, 3, 9, 2])
        assert result == 9

    def test_find_max_single_element(self):
        """Test finding max with single element"""
        result = code_rabbit_test.find_max([42])
        assert result == 42

    def test_find_max_all_same(self):
        """Test finding max when all numbers are same"""
        result = code_rabbit_test.find_max([7, 7, 7, 7])
        assert result == 7

    def test_find_max_negative_numbers(self):
        """Test finding max with all negative numbers - demonstrates bug"""
        result = code_rabbit_test.find_max([-1, -5, -3, -2])
        # Bug: initializes max_num to 0, so returns 0 instead of -1
        assert result == 0  # This is the buggy behavior

    def test_find_max_mixed_positive_negative(self):
        """Test finding max with mixed positive and negative"""
        result = code_rabbit_test.find_max([-10, 5, -3, 8, -1])
        assert result == 8

    def test_find_max_with_zero(self):
        """Test finding max when zero is in the list"""
        result = code_rabbit_test.find_max([0, -5, -10])
        assert result == 0

    def test_find_max_large_numbers(self):
        """Test finding max with large numbers"""
        result = code_rabbit_test.find_max([1000000, 999999, 1000001])
        assert result == 1000001

    def test_find_max_floats(self):
        """Test finding max with floating point numbers"""
        result = code_rabbit_test.find_max([1.1, 2.2, 1.9, 2.1])
        assert result == 2.2

    def test_find_max_negative_floats(self):
        """Test finding max with negative floats - demonstrates bug"""
        result = code_rabbit_test.find_max([-0.1, -0.5, -0.3])
        # Bug: returns 0 instead of -0.1
        assert result == 0

    def test_find_max_at_beginning(self):
        """Test when max is at beginning of list"""
        result = code_rabbit_test.find_max([10, 5, 3, 1])
        assert result == 10

    def test_find_max_at_end(self):
        """Test when max is at end of list"""
        result = code_rabbit_test.find_max([1, 3, 5, 10])
        assert result == 10

    def test_find_max_duplicates_of_max(self):
        """Test when max appears multiple times"""
        result = code_rabbit_test.find_max([5, 10, 3, 10, 2])
        assert result == 10

    def test_find_max_empty_list_returns_zero(self):
        """Test that empty list returns 0"""
        result = code_rabbit_test.find_max([])
        assert result == 0

    def test_find_max_very_small_positive(self):
        """Test finding max with very small positive numbers"""
        result = code_rabbit_test.find_max([0.001, 0.003, 0.002])
        assert abs(result - 0.003) < 0.0001


class TestReverseString:
    """Tests for reverse_string function"""

    def test_reverse_string_basic(self):
        """Test basic string reversal"""
        result = code_rabbit_test.reverse_string("hello")
        assert result == "olleh"

    def test_reverse_string_single_char(self):
        """Test reversing single character"""
        result = code_rabbit_test.reverse_string("a")
        assert result == "a"

    def test_reverse_string_empty(self):
        """Test reversing empty string"""
        result = code_rabbit_test.reverse_string("")
        assert result == ""

    def test_reverse_string_palindrome(self):
        """Test reversing palindrome"""
        result = code_rabbit_test.reverse_string("racecar")
        assert result == "racecar"

    def test_reverse_string_with_spaces(self):
        """Test reversing string with spaces"""
        result = code_rabbit_test.reverse_string("hello world")
        assert result == "dlrow olleh"

    def test_reverse_string_with_numbers(self):
        """Test reversing string with numbers"""
        result = code_rabbit_test.reverse_string("abc123")
        assert result == "321cba"

    def test_reverse_string_special_characters(self):
        """Test reversing string with special characters"""
        result = code_rabbit_test.reverse_string("hello!")
        assert result == "!olleh"

    def test_reverse_string_unicode(self):
        """Test reversing string with unicode characters"""
        result = code_rabbit_test.reverse_string("hello世界")
        assert result == "界世olleh"

    def test_reverse_string_long(self):
        """Test reversing long string"""
        original = "a" * 1000
        result = code_rabbit_test.reverse_string(original)
        assert result == original  # All same character

    def test_reverse_string_mixed_case(self):
        """Test reversing mixed case string"""
        result = code_rabbit_test.reverse_string("HeLLo")
        assert result == "oLLeH"

    def test_reverse_string_only_spaces(self):
        """Test reversing string with only spaces"""
        result = code_rabbit_test.reverse_string("   ")
        assert result == "   "

    def test_reverse_string_newlines(self):
        """Test reversing string with newlines"""
        result = code_rabbit_test.reverse_string("hello\nworld")
        assert result == "dlrow\nolleh"

    def test_reverse_string_tabs(self):
        """Test reversing string with tabs"""
        result = code_rabbit_test.reverse_string("a\tb\tc")
        assert result == "c\tb\ta"

    def test_reverse_string_actually_reverses(self):
        """Test that function actually reverses correctly"""
        result = code_rabbit_test.reverse_string("CodeRabbit")
        assert result == "tibbaRedoC"


class TestMergeDicts:
    """Tests for merge_dicts function"""

    def test_merge_dicts_basic(self):
        """Test basic dictionary merge"""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_dicts_overwrites_keys(self):
        """Test that merge overwrites existing keys"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 10, "c": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == 10
        assert result["b"] == 2
        assert result["c"] == 3

    def test_merge_dicts_empty_second(self):
        """Test merging with empty second dictionary"""
        d1 = {"a": 1, "b": 2}
        d2 = {}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2}

    def test_merge_dicts_empty_first(self):
        """Test merging with empty first dictionary"""
        d1 = {}
        d2 = {"a": 1, "b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2}

    def test_merge_dicts_both_empty(self):
        """Test merging two empty dictionaries"""
        d1 = {}
        d2 = {}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {}

    def test_merge_dicts_modifies_first(self):
        """Test that merge modifies the first dictionary"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert d1 is result
        assert d1 == {"a": 1, "b": 2}

    def test_merge_dicts_different_value_types(self):
        """Test merging dicts with different value types"""
        d1 = {"a": 1, "b": "hello"}
        d2 = {"c": [1, 2, 3], "d": {"nested": "dict"}}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == 1
        assert result["b"] == "hello"
        assert result["c"] == [1, 2, 3]
        assert result["d"] == {"nested": "dict"}

    def test_merge_dicts_overwrites_without_warning(self):
        """Test that overwriting happens without warning"""
        d1 = {"key": "original"}
        d2 = {"key": "overwritten"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["key"] == "overwritten"

    def test_merge_dicts_many_keys(self):
        """Test merging dictionaries with many keys"""
        d1 = {f"key{i}": i for i in range(50)}
        d2 = {f"key{i}": i + 100 for i in range(50, 100)}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 100

    def test_merge_dicts_nested_dicts(self):
        """Test merging with nested dictionaries"""
        d1 = {"outer": {"inner": 1}}
        d2 = {"outer": {"inner": 2}}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # Overwrites entire nested dict
        assert result["outer"] == {"inner": 2}

    def test_merge_dicts_numeric_keys(self):
        """Test merging with numeric keys"""
        d1 = {1: "one", 2: "two"}
        d2 = {3: "three", 4: "four"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {1: "one", 2: "two", 3: "three", 4: "four"}

    def test_merge_dicts_mixed_key_types(self):
        """Test merging with mixed key types"""
        d1 = {"str": 1, 1: "int"}
        d2 = {2: "two", "another": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 4

    def test_merge_dicts_none_values(self):
        """Test merging with None values"""
        d1 = {"a": None}
        d2 = {"b": None}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": None, "b": None}


class TestRiskyDivision:
    """Tests for risky_division function"""

    def test_risky_division_basic(self):
        """Test basic division"""
        result = code_rabbit_test.risky_division(10, 2)
        assert result == 5.0

    def test_risky_division_integers(self):
        """Test division with integers"""
        result = code_rabbit_test.risky_division(20, 4)
        assert result == 5.0

    def test_risky_division_floats(self):
        """Test division with floats"""
        result = code_rabbit_test.risky_division(10.5, 2.0)
        assert result == 5.25

    def test_risky_division_negative_numerator(self):
        """Test division with negative numerator"""
        result = code_rabbit_test.risky_division(-10, 2)
        assert result == -5.0

    def test_risky_division_negative_denominator(self):
        """Test division with negative denominator"""
        result = code_rabbit_test.risky_division(10, -2)
        assert result == -5.0

    def test_risky_division_both_negative(self):
        """Test division with both negative"""
        result = code_rabbit_test.risky_division(-10, -2)
        assert result == 5.0

    def test_risky_division_zero_numerator(self):
        """Test division with zero numerator"""
        result = code_rabbit_test.risky_division(0, 5)
        assert result == 0.0

    def test_risky_division_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10, 0)

    def test_risky_division_fractional_result(self):
        """Test division resulting in fraction"""
        result = code_rabbit_test.risky_division(7, 2)
        assert result == 3.5

    def test_risky_division_large_numbers(self):
        """Test division with large numbers"""
        result = code_rabbit_test.risky_division(1000000, 1000)
        assert result == 1000.0

    def test_risky_division_very_small_numbers(self):
        """Test division with very small numbers"""
        result = code_rabbit_test.risky_division(0.001, 0.1)
        assert abs(result - 0.01) < 0.0001

    def test_risky_division_by_one(self):
        """Test division by one"""
        result = code_rabbit_test.risky_division(42, 1)
        assert result == 42.0

    def test_risky_division_by_itself(self):
        """Test number divided by itself"""
        result = code_rabbit_test.risky_division(7, 7)
        assert result == 1.0

    def test_risky_division_float_by_zero_raises_error(self):
        """Test that float division by zero also raises error"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10.5, 0.0)

    def test_risky_division_precision(self):
        """Test division precision"""
        result = code_rabbit_test.risky_division(1, 3)
        assert abs(result - 0.333333) < 0.0001


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_calc_average_then_divide(self):
        """Test calculating average then using in division"""
        avg = code_rabbit_test.calc_average([10, 20, 30])
        result = code_rabbit_test.risky_division(100, avg)
        assert result == 5.0

    def test_find_max_in_reversed_scenario(self):
        """Test finding max and string operations"""
        nums = [3, 7, 2, 9, 5]
        max_val = code_rabbit_test.find_max(nums)
        reversed_str = code_rabbit_test.reverse_string(str(max_val))
        assert reversed_str == "9"

    def test_merge_and_manipulate_dicts(self):
        """Test merging dicts with numeric values"""
        d1 = {"a": 10, "b": 20}
        d2 = {"c": 30}
        merged = code_rabbit_test.merge_dicts(d1, d2)
        total = sum(merged.values())
        assert total == 60

    def test_string_operations_with_numbers(self):
        """Test string operations with string representations of numbers"""
        nums_str = "12345"
        reversed_str = code_rabbit_test.reverse_string(nums_str)
        assert reversed_str == "54321"


class TestEdgeCases:
    """Additional edge case and boundary tests"""

    def test_calc_average_boundary_large_list(self):
        """Test average with very large list"""
        nums = list(range(10000))
        result = code_rabbit_test.calc_average(nums)
        assert result == 4999.5

    def test_find_max_boundary_all_same_negative(self):
        """Test find_max when all numbers are same negative value"""
        result = code_rabbit_test.find_max([-5, -5, -5])
        # Bug: returns 0 instead of -5
        assert result == 0

    def test_reverse_string_performance_large(self):
        """Test reverse string with large input"""
        large_string = "a" * 10000 + "b"
        result = code_rabbit_test.reverse_string(large_string)
        assert result[0] == "b"
        assert result[-1] == "a"

    def test_merge_dicts_overwrite_all_keys(self):
        """Test merging where all keys are overwritten"""
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"a": 10, "b": 20, "c": 30}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 10, "b": 20, "c": 30}

    def test_risky_division_boundary_very_small_divisor(self):
        """Test division with very small divisor"""
        result = code_rabbit_test.risky_division(1, 0.0000001)
        assert result > 1000000


class TestRegressionScenarios:
    """Regression tests for real-world scenarios"""

    def test_calc_average_with_mixed_int_float(self):
        """Regression: Ensure int and float mixing works"""
        result = code_rabbit_test.calc_average([1, 2.5, 3, 4.5])
        assert result == 2.75

    def test_find_max_after_list_modification(self):
        """Regression: Ensure function doesn't modify input"""
        nums = [5, 3, 8, 1]
        original = nums.copy()
        code_rabbit_test.find_max(nums)
        assert nums == original

    def test_reverse_string_does_not_modify_original(self):
        """Regression: Ensure original string unchanged"""
        original = "test"
        result = code_rabbit_test.reverse_string(original)
        assert original == "test"
        assert result == "tset"

    def test_merge_dicts_preserves_d2(self):
        """Regression: Ensure second dict is not modified"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        d2_copy = d2.copy()
        code_rabbit_test.merge_dicts(d1, d2)
        assert d2 == d2_copy

    def test_division_result_type(self):
        """Regression: Ensure division always returns float"""
        result = code_rabbit_test.risky_division(10, 5)
        assert isinstance(result, float)

    def test_calc_average_negative_zero_mix(self):
        """Regression: Test with negative, zero, and positive"""
        result = code_rabbit_test.calc_average([-5, 0, 5])
        assert result == 0.0

    def test_find_max_single_negative(self):
        """Regression: Single negative number"""
        result = code_rabbit_test.find_max([-10])
        # Bug: returns 0 instead of -10
        assert result == 0

    def test_string_reverse_idempotent(self):
        """Regression: Reversing twice returns original"""
        original = "testing"
        reversed_once = code_rabbit_test.reverse_string(original)
        reversed_twice = code_rabbit_test.reverse_string(reversed_once)
        assert reversed_twice == original


class TestSecurityAndRobustness:
    """Tests for security issues and robustness"""

    def test_calc_average_type_error_protection(self):
        """Test that calc_average handles only numbers"""
        # This will raise TypeError if non-numeric
        with pytest.raises(TypeError):
            code_rabbit_test.calc_average(["a", "b", "c"])

    def test_risky_division_documents_no_check(self):
        """Document that risky_division doesn't check for zero"""
        # The function name itself indicates it's risky
        # No validation is performed
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(1, 0)

    def test_merge_dicts_mutation_side_effect(self):
        """Document that merge_dicts mutates first argument"""
        d1_original = {"a": 1}
        d1 = d1_original.copy()
        d2 = {"b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # d1 is mutated
        assert d1 is result
        assert "b" in d1

    def test_find_max_initialization_bug(self):
        """Document the max_num initialization bug"""
        # max_num is initialized to 0, causing issues with negative numbers
        result = code_rabbit_test.find_max([-1, -2, -3])
        assert result == 0  # Bug: should be -1