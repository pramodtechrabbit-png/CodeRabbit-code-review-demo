# code_rabbit_test.py
# Purpose: Test CodeRabbit review with multiple defects

def calc_average(nums):
    # Returns average of list
    total = 0
    for i in range(len(nums)):
        total += nums[i]   # Issue: manual loop, inefficient
    avg = total / len(nums)   # Issue: no empty list check
    return avg

def find_max(nums):
    # Find maximum number
    max_num = 0   # Issue: fails if all numbers are negative
    for n in nums:
        if n > max_num:
            max_num = n
    return max_num

def reverse_string(s):
    # Reverse string manually
    rev = ""
    for i in range(len(s)-1, -1, -1):
        rev += s[i]  # Issue: inefficient, should use slicing
    return rev

def merge_dicts(d1, d2):
    # Merge two dicts
    for key in d2:
        d1[key] = d2[key]   # Issue: overwrites without warning
    return d1

def risky_division(a, b):
    return a / b   # Issue: no zero-division check

# Test the functions
if __name__ == "__main__":
    nums = [10, -5, 15, 0]
    print("Average:", calc_average(nums))
    print("Max:", find_max(nums))
    print("Reversed:", reverse_string("CodeRabbit"))
    print("Merged dict:", merge_dicts({"a": 1}, {"a": 2, "b": 3}))
    print("Division result:", risky_division(10, 0))  # Will throw exception