"""
Comprehensive test suite for code_rabbit_test.py

Tests cover:
- calc_average() function with various inputs
- find_max() function with edge cases
- reverse_string() function
- merge_dicts() function
- risky_division() function with error cases
- All edge cases and boundary conditions
"""

import pytest
import sys

# Import functions directly by executing only the function definitions
# This avoids the module-level code that causes ZeroDivisionError
with open('/home/jailuser/git/code_rabbit_test.py', 'r') as f:
    source = f.read()
    # Extract only the function definitions (before the test code)
    func_code = source.split('# Test the functions')[0]

# Create a module object to hold the functions
import types
code_rabbit_test = types.ModuleType('code_rabbit_test')
exec(func_code, code_rabbit_test.__dict__)
sys.modules['code_rabbit_test'] = code_rabbit_test


class TestCalcAverage:
    """Test suite for calc_average function"""

    def test_calc_average_basic(self):
        """Test calculating average of positive numbers"""
        result = code_rabbit_test.calc_average([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_calc_average_single_element(self):
        """Test average of single element"""
        result = code_rabbit_test.calc_average([42])
        assert result == 42.0

    def test_calc_average_with_negatives(self):
        """Test average with negative numbers"""
        result = code_rabbit_test.calc_average([-5, -10, -15])
        assert result == -10.0

    def test_calc_average_mixed_positive_negative(self):
        """Test average with mixed positive and negative"""
        result = code_rabbit_test.calc_average([10, -5, 15, 0])
        assert result == 5.0

    def test_calc_average_with_zero(self):
        """Test average including zero"""
        result = code_rabbit_test.calc_average([0, 0, 0])
        assert result == 0.0

    def test_calc_average_empty_list_raises_error(self):
        """Test that empty list raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.calc_average([])

    def test_calc_average_floats(self):
        """Test average with floating point numbers"""
        result = code_rabbit_test.calc_average([1.5, 2.5, 3.5])
        assert abs(result - 2.5) < 0.001

    def test_calc_average_large_numbers(self):
        """Test average with large numbers"""
        result = code_rabbit_test.calc_average([1000000, 2000000, 3000000])
        assert result == 2000000.0

    def test_calc_average_many_elements(self):
        """Test average with many elements"""
        nums = list(range(1, 101))  # 1 to 100
        result = code_rabbit_test.calc_average(nums)
        assert abs(result - 50.5) < 0.001

    def test_calc_average_precision(self):
        """Test average calculation precision"""
        result = code_rabbit_test.calc_average([1, 2, 3])
        assert result == 2.0
        assert isinstance(result, float)

    def test_calc_average_inefficient_loop(self):
        """Document inefficient manual loop implementation"""
        # The function uses manual indexing instead of sum()
        nums = [1, 2, 3, 4, 5]
        result = code_rabbit_test.calc_average(nums)
        # Verify it still works despite inefficiency
        assert result == sum(nums) / len(nums)

    def test_calc_average_all_same_value(self):
        """Test average when all values are the same"""
        result = code_rabbit_test.calc_average([7, 7, 7, 7, 7])
        assert result == 7.0

    def test_calc_average_two_elements(self):
        """Test average of two elements"""
        result = code_rabbit_test.calc_average([10, 20])
        assert result == 15.0


class TestFindMax:
    """Test suite for find_max function"""

    def test_find_max_basic(self):
        """Test finding max in positive numbers"""
        result = code_rabbit_test.find_max([1, 5, 3, 9, 2])
        assert result == 9

    def test_find_max_single_element(self):
        """Test max of single element"""
        result = code_rabbit_test.find_max([42])
        assert result == 42

    def test_find_max_all_negative_fails(self):
        """Test that find_max fails with all negative numbers (bug)"""
        result = code_rabbit_test.find_max([-5, -10, -3, -20])
        # Bug: max_num initialized to 0, so returns 0 instead of -3
        assert result == 0  # This is the bug!

    def test_find_max_with_zero(self):
        """Test max when zero is in the list"""
        result = code_rabbit_test.find_max([0, 5, 3, 1])
        assert result == 5

    def test_find_max_all_zeros(self):
        """Test max when all values are zero"""
        result = code_rabbit_test.find_max([0, 0, 0])
        assert result == 0

    def test_find_max_at_beginning(self):
        """Test when max is at the beginning"""
        result = code_rabbit_test.find_max([100, 5, 10, 20])
        assert result == 100

    def test_find_max_at_end(self):
        """Test when max is at the end"""
        result = code_rabbit_test.find_max([1, 2, 3, 100])
        assert result == 100

    def test_find_max_duplicate_maxes(self):
        """Test when max value appears multiple times"""
        result = code_rabbit_test.find_max([10, 20, 30, 30, 20])
        assert result == 30

    def test_find_max_large_numbers(self):
        """Test with large numbers"""
        result = code_rabbit_test.find_max([1000000, 999999, 500000])
        assert result == 1000000

    def test_find_max_floats(self):
        """Test with floating point numbers"""
        result = code_rabbit_test.find_max([1.5, 2.7, 2.6, 1.9])
        assert result == 2.7

    def test_find_max_mixed_positive_negative(self):
        """Test with mixed positive and negative"""
        result = code_rabbit_test.find_max([10, -5, 15, 0, -20])
        assert result == 15

    def test_find_max_negative_close_to_zero(self):
        """Test with negative numbers close to zero (exposes bug)"""
        result = code_rabbit_test.find_max([-0.1, -0.5, -0.3])
        # Bug: returns 0 instead of -0.1
        assert result == 0

    def test_find_max_one_positive_rest_negative(self):
        """Test with one positive and rest negative"""
        result = code_rabbit_test.find_max([-10, 5, -20, -30])
        assert result == 5

    def test_find_max_empty_list(self):
        """Test find_max with empty list"""
        result = code_rabbit_test.find_max([])
        assert result == 0  # Returns initial value


class TestReverseString:
    """Test suite for reverse_string function"""

    def test_reverse_string_basic(self):
        """Test reversing a basic string"""
        result = code_rabbit_test.reverse_string("hello")
        assert result == "olleh"

    def test_reverse_string_empty(self):
        """Test reversing empty string"""
        result = code_rabbit_test.reverse_string("")
        assert result == ""

    def test_reverse_string_single_char(self):
        """Test reversing single character"""
        result = code_rabbit_test.reverse_string("a")
        assert result == "a"

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
        result = code_rabbit_test.reverse_string("a!b@c#")
        assert result == "#c@b!a"

    def test_reverse_string_unicode(self):
        """Test reversing string with unicode characters"""
        result = code_rabbit_test.reverse_string("Hello世界")
        assert result == "界世olleH"

    def test_reverse_string_long(self):
        """Test reversing long string"""
        long_str = "a" * 1000
        result = code_rabbit_test.reverse_string(long_str)
        assert result == long_str  # All same character

    def test_reverse_string_punctuation(self):
        """Test reversing string with punctuation"""
        result = code_rabbit_test.reverse_string("Hello, World!")
        assert result == "!dlroW ,olleH"

    def test_reverse_string_newlines(self):
        """Test reversing string with newlines"""
        result = code_rabbit_test.reverse_string("line1\nline2")
        assert result == "2enil\n1enil"

    def test_reverse_string_tabs(self):
        """Test reversing string with tabs"""
        result = code_rabbit_test.reverse_string("a\tb\tc")
        assert result == "c\tb\ta"

    def test_reverse_string_inefficient_implementation(self):
        """Document inefficient string concatenation"""
        # The function uses += which is inefficient
        # Should use slicing: s[::-1]
        result = code_rabbit_test.reverse_string("CodeRabbit")
        assert result == "tibbaRedoC"

    def test_reverse_string_case_sensitivity(self):
        """Test that reverse preserves case"""
        result = code_rabbit_test.reverse_string("AbCdEf")
        assert result == "fEdCbA"


class TestMergeDicts:
    """Test suite for merge_dicts function"""

    def test_merge_dicts_basic(self):
        """Test basic dictionary merge"""
        d1 = {"a": 1, "b": 2}
        d2 = {"c": 3, "d": 4}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 1, "b": 2, "c": 3, "d": 4}

    def test_merge_dicts_overwrites_existing_keys(self):
        """Test that merge overwrites existing keys (bug/feature)"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 99, "c": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == 99  # Overwrites without warning

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
        """Test that function modifies first dict in place"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        result = code_rabbit_test.merge_dicts(d1, d2)
        # d1 is modified in place
        assert d1 is result
        assert d1 == {"a": 1, "b": 2}

    def test_merge_dicts_with_different_value_types(self):
        """Test merging dicts with different value types"""
        d1 = {"a": 1, "b": "string"}
        d2 = {"c": [1, 2, 3], "d": None}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == 1
        assert result["b"] == "string"
        assert result["c"] == [1, 2, 3]
        assert result["d"] is None

    def test_merge_dicts_nested_dicts(self):
        """Test merging dicts with nested structures"""
        d1 = {"a": {"x": 1}}
        d2 = {"b": {"y": 2}}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": {"x": 1}, "b": {"y": 2}}

    def test_merge_dicts_overwrite_different_types(self):
        """Test overwriting value with different type"""
        d1 = {"a": 1}
        d2 = {"a": "string"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == "string"

    def test_merge_dicts_many_keys(self):
        """Test merging dicts with many keys"""
        d1 = {f"key{i}": i for i in range(50)}
        d2 = {f"key{i}": i + 100 for i in range(50, 100)}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 100

    def test_merge_dicts_special_keys(self):
        """Test merging dicts with special key names"""
        d1 = {"": 1, " ": 2}
        d2 = {"key with spaces": 3, "key-with-dashes": 4}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert "" in result
        assert " " in result
        assert "key with spaces" in result

    def test_merge_dicts_numeric_keys(self):
        """Test merging dicts with numeric keys"""
        d1 = {1: "a", 2: "b"}
        d2 = {3: "c", 4: "d"}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result[1] == "a"
        assert result[4] == "d"

    def test_merge_dicts_complete_overwrite(self):
        """Test when all keys are overwritten"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 10, "b": 20}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result == {"a": 10, "b": 20}


class TestRiskyDivision:
    """Test suite for risky_division function"""

    def test_risky_division_basic(self):
        """Test basic division"""
        result = code_rabbit_test.risky_division(10, 2)
        assert result == 5.0

    def test_risky_division_by_zero_raises_error(self):
        """Test that division by zero raises ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10, 0)

    def test_risky_division_negative_numbers(self):
        """Test division with negative numbers"""
        result = code_rabbit_test.risky_division(-10, 2)
        assert result == -5.0

    def test_risky_division_both_negative(self):
        """Test division with both negative"""
        result = code_rabbit_test.risky_division(-10, -2)
        assert result == 5.0

    def test_risky_division_zero_numerator(self):
        """Test division with zero numerator"""
        result = code_rabbit_test.risky_division(0, 5)
        assert result == 0.0

    def test_risky_division_float_result(self):
        """Test division resulting in float"""
        result = code_rabbit_test.risky_division(7, 2)
        assert result == 3.5

    def test_risky_division_large_numbers(self):
        """Test division with large numbers"""
        result = code_rabbit_test.risky_division(1000000, 1000)
        assert result == 1000.0

    def test_risky_division_very_small_divisor(self):
        """Test division by very small number"""
        result = code_rabbit_test.risky_division(1, 0.0001)
        assert result == 10000.0

    def test_risky_division_precision(self):
        """Test division precision"""
        result = code_rabbit_test.risky_division(1, 3)
        assert abs(result - 0.333333) < 0.00001

    def test_risky_division_identity(self):
        """Test division by 1"""
        result = code_rabbit_test.risky_division(42, 1)
        assert result == 42.0

    def test_risky_division_self(self):
        """Test dividing number by itself"""
        result = code_rabbit_test.risky_division(42, 42)
        assert result == 1.0

    def test_risky_division_floats(self):
        """Test division with float inputs"""
        result = code_rabbit_test.risky_division(10.5, 2.5)
        assert result == 4.2

    def test_risky_division_no_error_handling(self):
        """Document that function has no error handling"""
        # Function will raise exception instead of handling gracefully
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(5, 0)

    def test_risky_division_negative_by_positive(self):
        """Test negative divided by positive"""
        result = code_rabbit_test.risky_division(-15, 3)
        assert result == -5.0

    def test_risky_division_positive_by_negative(self):
        """Test positive divided by negative"""
        result = code_rabbit_test.risky_division(15, -3)
        assert result == -5.0


class TestIntegrationScenarios:
    """Integration tests combining multiple functions"""

    def test_calculate_average_then_find_max(self):
        """Test calculating average and finding max from same data"""
        nums = [10, -5, 15, 0]
        avg = code_rabbit_test.calc_average(nums)
        max_val = code_rabbit_test.find_max(nums)
        assert avg == 5.0
        assert max_val == 15

    def test_reverse_multiple_strings(self):
        """Test reversing multiple strings"""
        strings = ["CodeRabbit", "Testing", "Python"]
        results = [code_rabbit_test.reverse_string(s) for s in strings]
        assert results[0] == "tibbaRedoC"
        assert results[1] == "gnitseT"
        assert results[2] == "nohtyP"

    def test_merge_multiple_dicts_sequential(self):
        """Test merging multiple dicts sequentially"""
        d1 = {"a": 1}
        d2 = {"b": 2}
        d3 = {"c": 3}
        result = code_rabbit_test.merge_dicts(d1, d2)
        result = code_rabbit_test.merge_dicts(result, d3)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_division_on_average_result(self):
        """Test using division on calculated average"""
        nums = [10, 20, 30]
        avg = code_rabbit_test.calc_average(nums)
        result = code_rabbit_test.risky_division(avg, 2)
        assert result == 10.0

    def test_all_functions_with_edge_cases(self):
        """Test all functions with various edge cases"""
        # Average with single element
        avg = code_rabbit_test.calc_average([42])
        assert avg == 42.0

        # Max with single element
        max_val = code_rabbit_test.find_max([42])
        assert max_val == 42

        # Reverse single char
        rev = code_rabbit_test.reverse_string("a")
        assert rev == "a"

        # Merge empty dicts
        merged = code_rabbit_test.merge_dicts({}, {})
        assert merged == {}

        # Divide by 1
        div = code_rabbit_test.risky_division(42, 1)
        assert div == 42.0


class TestEdgeCasesAndBoundaries:
    """Additional edge cases and boundary condition tests"""

    def test_calc_average_very_large_list(self):
        """Test average with very large list"""
        nums = list(range(10000))
        result = code_rabbit_test.calc_average(nums)
        expected = sum(nums) / len(nums)
        assert abs(result - expected) < 0.001

    def test_find_max_all_equal(self):
        """Test find_max when all elements are equal"""
        result = code_rabbit_test.find_max([5, 5, 5, 5])
        assert result == 5

    def test_reverse_string_very_long(self):
        """Test reversing very long string"""
        long_str = "x" * 10000
        result = code_rabbit_test.reverse_string(long_str)
        assert len(result) == 10000
        assert result == long_str

    def test_merge_dicts_large_scale(self):
        """Test merging large dictionaries"""
        d1 = {i: i for i in range(1000)}
        d2 = {i + 1000: i for i in range(1000)}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert len(result) == 2000

    def test_risky_division_infinity(self):
        """Test division resulting in infinity"""
        result = code_rabbit_test.risky_division(1e308, 1e-308)
        assert result == float('inf')

    def test_calc_average_floating_point_precision(self):
        """Test floating point precision issues"""
        nums = [0.1, 0.2, 0.3]
        result = code_rabbit_test.calc_average(nums)
        assert abs(result - 0.2) < 0.0001

    def test_find_max_extreme_values(self):
        """Test find_max with extreme values"""
        result = code_rabbit_test.find_max([1e10, 1e9, 1e11])
        assert result == 1e11

    def test_reverse_string_only_spaces(self):
        """Test reversing string with only spaces"""
        result = code_rabbit_test.reverse_string("     ")
        assert result == "     "

    def test_merge_dicts_with_none_values(self):
        """Test merging dicts containing None values"""
        d1 = {"a": None, "b": 2}
        d2 = {"c": None, "d": 4}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] is None
        assert result["c"] is None

    def test_risky_division_negative_zero(self):
        """Test division with negative zero"""
        result = code_rabbit_test.risky_division(-0.0, 1)
        assert result == 0.0


class TestDocumentedIssues:
    """Tests documenting known issues in the code"""

    def test_calc_average_inefficient_loop_issue(self):
        """Document: Uses inefficient manual loop instead of sum()"""
        # Should use: return sum(nums) / len(nums)
        nums = [1, 2, 3, 4, 5]
        result = code_rabbit_test.calc_average(nums)
        assert result == 3.0  # Works but inefficient

    def test_calc_average_no_empty_check_issue(self):
        """Document: No check for empty list causes ZeroDivisionError"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.calc_average([])

    def test_find_max_negative_numbers_issue(self):
        """Document: Fails with all negative numbers due to max_num=0 init"""
        result = code_rabbit_test.find_max([-1, -2, -3])
        assert result == 0  # Bug: should be -1

    def test_reverse_string_inefficient_concatenation_issue(self):
        """Document: Uses inefficient string concatenation instead of slicing"""
        # Should use: return s[::-1]
        result = code_rabbit_test.reverse_string("test")
        assert result == "tset"  # Works but inefficient

    def test_merge_dicts_overwrites_without_warning_issue(self):
        """Document: Overwrites existing keys without warning"""
        d1 = {"a": 1, "b": 2}
        d2 = {"a": 999}
        result = code_rabbit_test.merge_dicts(d1, d2)
        assert result["a"] == 999  # Original value lost

    def test_risky_division_no_error_handling_issue(self):
        """Document: No error handling for division by zero"""
        with pytest.raises(ZeroDivisionError):
            code_rabbit_test.risky_division(10, 0)


class TestRegressionScenarios:
    """Regression tests for real-world scenarios"""

    def test_calc_average_with_duplicates(self):
        """Regression: Average calculation with duplicate values"""
        nums = [5, 5, 5, 10, 10, 10]
        result = code_rabbit_test.calc_average(nums)
        assert result == 7.5

    def test_find_max_unsorted_list(self):
        """Regression: Find max in completely unsorted list"""
        nums = [3, 7, 2, 9, 1, 5, 8, 4, 6]
        result = code_rabbit_test.find_max(nums)
        assert result == 9

    def test_reverse_string_with_emoji(self):
        """Regression: Reverse string containing emoji"""
        result = code_rabbit_test.reverse_string("Hello🚀World")
        assert "dlroW" in result
        assert "🚀" in result

    def test_merge_dicts_preserves_order(self):
        """Regression: Verify merge preserves insertion order (Python 3.7+)"""
        d1 = {"a": 1, "b": 2, "c": 3}
        d2 = {"d": 4, "e": 5}
        result = code_rabbit_test.merge_dicts(d1, d2)
        keys = list(result.keys())
        assert keys == ["a", "b", "c", "d", "e"]

    def test_risky_division_commutative_property(self):
        """Regression: Division is not commutative"""
        result1 = code_rabbit_test.risky_division(10, 2)
        result2 = code_rabbit_test.risky_division(2, 10)
        assert result1 != result2
        assert result1 == 5.0
        assert result2 == 0.2

    def test_consecutive_operations(self):
        """Regression: Test consecutive operations on same data"""
        nums = [5, 10, 15, 20, 25]

        # Calculate average
        avg = code_rabbit_test.calc_average(nums)
        assert avg == 15.0

        # Find max
        max_val = code_rabbit_test.find_max(nums)
        assert max_val == 25

        # Verify original list unchanged
        assert nums == [5, 10, 15, 20, 25]

    def test_dict_merge_state_mutation(self):
        """Regression: Verify that first dict is mutated"""
        d1_original = {"a": 1, "b": 2}
        d1 = d1_original.copy()
        d2 = {"c": 3}

        result = code_rabbit_test.merge_dicts(d1, d2)

        # d1 is modified in place
        assert d1 is result
        assert d1 != d1_original
        assert "c" in d1