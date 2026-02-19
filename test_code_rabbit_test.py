"""
Comprehensive test suite for code_rabbit_test.py
Tests cover main functionality, edge cases, error handling, and boundary conditions.

Note: The source file code_rabbit_test.py executes test code at module level
which causes a ZeroDivisionError on line 42. This is intentional to demonstrate
the risky_division bug. The import will fail, so we import individual functions.
"""

import pytest
import sys

# Import the module and handle the ZeroDivisionError that occurs at module load
try:
    import code_rabbit_test
except ZeroDivisionError:
    # This is expected - the source file calls risky_division(10, 0) at module level
    # We need to import the module differently
    pass

# Import functions directly by reading the module
import importlib.util
spec = importlib.util.spec_from_file_location("code_rabbit_test_safe", "/home/jailuser/git/code_rabbit_test.py")
code_rabbit_test_module = importlib.util.module_from_spec(spec)

# Execute only the function definitions, not the test code at the bottom
import types
with open("/home/jailuser/git/code_rabbit_test.py", "r") as f:
    source = f.read()
    # Remove the test execution lines at the end
    lines = source.split("\n")
    func_lines = []
    for line in lines:
        if line.startswith("# Test the functions"):
            break
        func_lines.append(line)
    safe_source = "\n".join(func_lines)

# Execute the safe source to get the functions
exec(safe_source, code_rabbit_test_module.__dict__)
code_rabbit_test = code_rabbit_test_module


class TestCalcAverage:
    """Tests for calc_average function"""

    def test_calc_average_positive_numbers(self):
        """Test average of positive numbers"""
        result = code_rabbit_test.calc_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calc_average_negative_numbers(self):
        """Test average with negative numbers"""
        result = code_rabbit_test.calc_average([-5, -10, -15])
        assert result == -10.0

    def test_calc_average_mixed_numbers(self):
        """Test average with mixed positive and negative numbers"""
        result = code_rabbit_test.calc_average([-10, 10, -5, 5])
        assert result == 0.0

    def test_calc_average_single_element(self):
        """Test average with single element"""
        result = code_rabbit_test.calc_average([42])
        assert result == 42.0

    def test_calc_average_zeros(self):
        """Test average with zeros"""
        result = code_rabbit_test.calc_average([0, 0, 0])
        assert result == 0.0

    def test_calc_average_floats(self):
        """Test average with floating point numbers"""
        result = code_rabbit_test.calc_average([1.5, 2.5, 3.5])
        assert abs(result - 2.5) < 0.001

    def test_calc_average_empty_list_raises_error(self):
        """Test that empty list causes division by zero"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.calc_average([])

    def test_calc_average_large_numbers(self):
        """Test average with large numbers"""
        result = code_rabbit_test.calc_average([1000000, 2000000, 3000000])
        assert result == 2000000.0

    def test_calc_average_many_elements(self):
        """Test average with many elements"""
        nums = list(range(1, 101))
        result = code_rabbit_test.calc_average(nums)
        assert result == 50.5

    def test_calc_average_fractional_result(self):
        """Test average resulting in fraction"""
        result = code_rabbit_test.calc_average([1, 2])
        assert result == 1.5


class TestFindMax:
    """Tests for find_max function"""

    def test_find_max_positive_numbers(self):
        """Test finding max in positive numbers"""
        result = code_rabbit_test.find_max([1, 5, 3, 9, 2])
        assert result == 9

    def test_find_max_negative_numbers(self):
        """Test finding max in all negative numbers (bug: returns 0)"""
        result = code_rabbit_test.find_max([-5, -10, -3, -20])
        # Bug: function returns 0 instead of -3
        assert result == 0  # Documents the bug

    def test_find_max_mixed_numbers(self):
        """Test finding max in mixed positive and negative numbers"""
        result = code_rabbit_test.find_max([-5, 10, -15, 3])
        assert result == 10

    def test_find_max_single_element(self):
        """Test finding max with single element"""
        result = code_rabbit_test.find_max([42])
        assert result == 42

    def test_find_max_all_zeros(self):
        """Test finding max in list of zeros"""
        result = code_rabbit_test.find_max([0, 0, 0])
        assert result == 0

    def test_find_max_with_zero(self):
        """Test finding max when zero is not the max"""
        result = code_rabbit_test.find_max([0, 5, 2, 8])
        assert result == 8

    def test_find_max_duplicates(self):
        """Test finding max with duplicate max values"""
        result = code_rabbit_test.find_max([5, 10, 3, 10, 2])
        assert result == 10

    def test_find_max_first_element_is_max(self):
        """Test when first element is maximum"""
        result = code_rabbit_test.find_max([100, 50, 25, 10])
        assert result == 100

    def test_find_max_last_element_is_max(self):
        """Test when last element is maximum"""
        result = code_rabbit_test.find_max([10, 25, 50, 100])
        assert result == 100

    def test_find_max_negative_with_zero(self):
        """Test finding max when list has zero and negative numbers (bug)"""
        result = code_rabbit_test.find_max([-5, 0, -10])
        # Function correctly returns 0 in this case
        assert result == 0

    def test_find_max_large_numbers(self):
        """Test finding max with large numbers"""
        result = code_rabbit_test.find_max([1000000, 5000000, 2000000])
        assert result == 5000000

    def test_find_max_floats(self):
        """Test finding max with floating point numbers"""
        result = code_rabbit_test.find_max([1.5, 3.7, 2.1, 3.8, 1.9])
        assert abs(result - 3.8) < 0.001


class TestReverseString:
    """Tests for reverse_string function"""

    def test_reverse_string_basic(self):
        """Test reversing a simple string"""
        result = code_rabbit_test.reverse_string("hello")
        assert result == "olleh"

    def test_reverse_string_palindrome(self):
        """Test reversing a palindrome"""
        result = code_rabbit_test.reverse_string("racecar")
        assert result == "racecar"

    def test_reverse_string_empty(self):
        """Test reversing empty string"""
        result = code_rabbit_test.reverse_string("")
        assert result == ""

    def test_reverse_string_single_char(self):
        """Test reversing single character"""
        result = code_rabbit_test.reverse_string("a")
        assert result == "a"

    def test_reverse_string_with_spaces(self):
        """Test reversing string with spaces"""
        result = code_rabbit_test.reverse_string("hello world")
        assert result == "dlrow olleh"

    def test_reverse_string_numbers(self):
        """Test reversing string of numbers"""
        result = code_rabbit_test.reverse_string("12345")
        assert result == "54321"

    def test_reverse_string_special_chars(self):
        """Test reversing string with special characters"""
        result = code_rabbit_test.reverse_string("a!b@c#")
        assert result == "#c@b!a"

    def test_reverse_string_unicode(self):
        """Test reversing string with unicode characters"""
        result = code_rabbit_test.reverse_string("日本語")
        assert result == "語本日"

    def test_reverse_string_mixed_case(self):
        """Test reversing mixed case string"""
        result = code_rabbit_test.reverse_string("HeLLo")
        assert result == "oLLeH"

    def test_reverse_string_long(self):
        """Test reversing long string"""
        long_str = "a" * 1000
        result = code_rabbit_test.reverse_string(long_str)
        assert result == long_str
        assert len(result) == 1000

    def test_reverse_string_coderabbit(self):
        """Test the example from the source"""
        result = code_rabbit_test.reverse_string("CodeRabbit")
        assert result == "tibbaRedoC"


class TestMergeDicts:
    """Tests for merge_dicts function"""

    def test_merge_dicts_basic(self):
        """Test basic dict merging"""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_dicts_overwrites_keys(self):
        """Test that merge overwrites keys (documents the bug)"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 99, "c": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # Bug: d2 overwrites d1 without warning
        assert result["a"] == 99
        assert result["b"] == 2
        assert result["c"] == 3

    def test_merge_dicts_empty_second(self):
        """Test merging with empty second dict"""
        d1 = {"a": 1, "b": 2}
        d2 = {}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2}

    def test_merge_dicts_empty_first(self):
        """Test merging with empty first dict"""
        d1 = {}
        d2 = {"a": 1, "b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2}

    def test_merge_dicts_both_empty(self):
        """Test merging two empty dicts"""
        d1 = {}
        d2 = {}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {}

    def test_merge_dicts_modifies_first_dict(self):
        """Test that merge modifies the first dict in place"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # The function returns d1, which is modified
        assert result is d1
        assert d1 == {"a": 1, "b": 2}

    def test_merge_dicts_complex_values(self):
        """Test merging dicts with complex values"""
        d1 = {"a": [1, 2, 3], "b": "text"}
        d2 = {"c": {"nested": "dict"}}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == [1, 2, 3]
        assert result["b"] == "text"
        assert result["c"] == {"nested": "dict"}

    def test_merge_dicts_numeric_keys(self):
        """Test merging dicts with numeric keys"""
        d1 = {1: "one", 2: "two"}
        d2 = {3: "three", 4: "four"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 4

    def test_merge_dicts_overwrite_different_types(self):
        """Test overwriting value with different type"""
        d1 = {"a": 1}
        d2 = {"a": "string"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == "string"

    def test_merge_dicts_example_from_source(self):
        """Test the example from the source"""
        d1 = {"a": 1}
        d2 = {"a": 2, "b": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # d2 overwrites d1's "a" value
        assert result == {"a": 2, "b": 3}


class TestRiskyDivision:
    """Tests for risky_division function"""

    def test_risky_division_basic(self):
        """Test basic division"""
        result = code_rabbit_test.risky_division(10, 2)
        assert result == 5.0

    def test_risky_division_negative_dividend(self):
        """Test division with negative dividend"""
        result = code_rabbit_test.risky_division(-10, 2)
        assert result == -5.0

    def test_risky_division_negative_divisor(self):
        """Test division with negative divisor"""
        result = code_rabbit_test.risky_division(10, -2)
        assert result == -5.0

    def test_risky_division_both_negative(self):
        """Test division with both negative"""
        result = code_rabbit_test.risky_division(-10, -2)
        assert result == 5.0

    def test_risky_division_zero_dividend(self):
        """Test division with zero dividend"""
        result = code_rabbit_test.risky_division(0, 5)
        assert result == 0.0

    def test_risky_division_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError (bug: no check)"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10, 0)

    def test_risky_division_floats(self):
        """Test division with floating point numbers"""
        result = code_rabbit_test.risky_division(7.5, 2.5)
        assert abs(result - 3.0) < 0.001

    def test_risky_division_large_numbers(self):
        """Test division with large numbers"""
        result = code_rabbit_test.risky_division(1000000, 1000)
        assert result == 1000.0

    def test_risky_division_fractional_result(self):
        """Test division resulting in fraction"""
        result = code_rabbit_test.risky_division(10, 3)
        assert abs(result - 3.333333) < 0.001

    def test_risky_division_one_by_one(self):
        """Test division of 1 by 1"""
        result = code_rabbit_test.risky_division(1, 1)
        assert result == 1.0

    def test_risky_division_result_less_than_one(self):
        """Test division resulting in value less than 1"""
        result = code_rabbit_test.risky_division(1, 2)
        assert result == 0.5


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_calc_average_and_find_max_same_list(self):
        """Test calculating average and finding max on same list"""
        nums = [5, 10, 15, 20]
        avg = code_rabbit_test.calc_average(nums)
        max_val = code_rabbit_test.find_max(nums)
        assert avg == 12.5
        assert max_val == 20

    def test_reverse_string_twice_returns_original(self):
        """Test that reversing twice returns original"""
        original = "hello"
        reversed_once = code_rabbit_test.reverse_string(original)
        reversed_twice = code_rabbit_test.reverse_string(reversed_once)
        assert reversed_twice == original

    def test_merge_multiple_dicts_sequentially(self):
        """Test merging multiple dicts in sequence"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        d3 = {"c": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        result = code_rabbit_test.merge_dicts(result, d3)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_division_and_average_workflow(self):
        """Test using division results in average calculation"""
        result1 = code_rabbit_test.risky_division(10, 2)
        result2 = code_rabbit_test.risky_division(20, 4)
        avg = code_rabbit_test.calc_average([result1, result2])
        assert avg == 5.0


class TestEdgeCasesAndBoundaries:
    """Edge cases and boundary condition tests"""

    def test_calc_average_very_large_list(self):
        """Test average with very large list"""
        nums = list(range(1, 10001))
        result = code_rabbit_test.calc_average(nums)
        assert result == 5000.5

    def test_find_max_all_same_values(self):
        """Test finding max when all values are the same"""
        result = code_rabbit_test.find_max([5, 5, 5, 5])
        assert result == 5

    def test_reverse_string_very_long(self):
        """Test reversing very long string"""
        long_str = "abc" * 1000
        result = code_rabbit_test.reverse_string(long_str)
        assert result == "cba" * 1000

    def test_merge_dicts_many_keys(self):
        """Test merging dicts with many keys"""
        d1 = {f"key{i}": i for i in range(50)}
        d2 = {f"key{i}": i + 100 for i in range(50, 100)}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 100

    def test_risky_division_very_small_divisor(self):
        """Test division with very small divisor"""
        result = code_rabbit_test.risky_division(1, 0.0001)
        assert result == 10000.0

    def test_calc_average_precision_with_floats(self):
        """Test precision issues with floating point average"""
        nums = [0.1, 0.2, 0.3]
        result = code_rabbit_test.calc_average(nums)
        assert abs(result - 0.2) < 0.001


class TestRegressionAndSecurityIssues:
    """Regression tests and tests documenting issues"""

    def test_calc_average_manual_loop_inefficiency(self):
        """Document that function uses manual loop instead of sum()"""
        # This test just documents the inefficiency mentioned in comments
        nums = [1, 2, 3, 4, 5]
        result = code_rabbit_test.calc_average(nums)
        expected = sum(nums) / len(nums)
        assert result == expected

    def test_find_max_initialization_bug(self):
        """Document bug: max_num initialized to 0 instead of first element"""
        # When all numbers are negative, function returns 0 (incorrect)
        negative_nums = [-1, -2, -3, -4]
        result = code_rabbit_test.find_max(negative_nums)
        # Bug: returns 0 instead of -1
        assert result == 0  # Documents the bug

    def test_reverse_string_inefficient_concatenation(self):
        """Document that function uses inefficient string concatenation"""
        # This test documents the inefficiency mentioned in comments
        s = "test"
        result = code_rabbit_test.reverse_string(s)
        expected = s[::-1]
        assert result == expected

    def test_merge_dicts_overwrites_without_warning(self):
        """Document that merge overwrites without warning"""
        d1 = {"important": "data"}
        d2 = {"important": "overwritten"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # Bug: original value is lost without warning
        assert result["important"] == "overwritten"

    def test_risky_division_no_zero_check(self):
        """Document that function has no zero-division check"""
        # This is the main bug in risky_division
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10, 0)

    def test_calc_average_empty_list_crash(self):
        """Regression test: ensure empty list handling is documented"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.calc_average([])

    def test_merge_dicts_maintains_reference(self):
        """Test that merged dict maintains reference to original"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        original_id = id(d1)
        result = code_rabbit_test.merge_dicts(d1, d2)
        # Result is the same object as d1
        assert id(result) == original_id