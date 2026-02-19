# review_example.py
# Python code for CodeRabbit review

def process_numbers(numbers):
    """
    Returns the square root of each number in the list.
    Issues intentionally included for review.
    """
    result = []
    for num in numbers:
        sqrt = num ** 0.5   # Issue: no negative number check
        result.append(sqrt)
    return result

# Test the function
nums = [4, 16, -9, 25]  # Includes a negative number intentionally
print("Processed numbers:", process_numbers(nums))

# Another function with issues
def merge_dicts(dict1, dict2):
    """
    Merges two dictionaries. May overwrite values without warning.
    """
    for key in dict2:
        dict1[key] = dict2[key]   # Issue: overwrites existing keys silently
    return dict1

dict_a = {"a": 1, "b": 2}
dict_b = {"b": 3, "c": 4}
print("Merged dict:", merge_dicts(dict_a, dict_b))
