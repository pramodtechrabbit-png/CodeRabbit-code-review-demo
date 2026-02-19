# code_rabbit_validation_test.py
# Python code with validations and intentional issues for CodeRabbit review
# Description: Added multiple functions with input validations, type checks,
# and error handling. Includes intentional issues for AI code review:
# - Returning error values instead of exceptions
# - Mixed styles of validation
# - Type mismatches in test cases
# - Overwriting dict keys with warnings
# - Inefficient or unsafe practices

from typing import List, Dict

def safe_divide(a: float, b: float) -> float:
    """Divide a by b with validation."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        print("Error: Inputs must be numbers")
        return 0
    if b == 0:
        print("Error: Division by zero")
        return 0
    return a / b

def validate_list(nums: List[int]) -> bool:
    """Check if the list contains only integers and is not empty."""
    if not nums:
        return False
    for n in nums:
        if not isinstance(n, int):
            return False
    return True

def find_average(nums: List[int]) -> float:
    """Calculate average with validation."""
    if not validate_list(nums):
        print("Error: Invalid list")
        return -1
    return sum(nums) / len(nums)

def find_max_min(nums: List[int]) -> Dict[str, int]:
    """Return max and min of the list with validation."""
    if not validate_list(nums):
        raise ValueError("Invalid list")
    return {"max": max(nums), "min": min(nums)}

def reverse_string(s: str) -> str:
    """Reverse a string with type validation."""
    if not isinstance(s, str):
        return ""
    return s[::-1]

def merge_dicts(d1: Dict, d2: Dict) -> Dict:
    """Merge two dictionaries with validation."""
    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise TypeError("Both inputs must be dictionaries")
    merged = d1.copy()
    for key in d2:
        if key in merged:
            print(f"Warning: Overwriting key {key}")
        merged[key] = d2[key]
    return merged

# Test functions with intentional issues
nums = [10, 20, 30, "40"]  # Intentional type error
print("Average:", find_average(nums))
print("Max & Min:", find_max_min([5, 8, -2, 0]))
print("Safe Divide:", safe_divide(10, 0))
print("Reversed string:", reverse_string(12345))  # Invalid type
print("Merged dict:", merge_dicts({"a": 1}, {"a": 2, "b": 3}))
