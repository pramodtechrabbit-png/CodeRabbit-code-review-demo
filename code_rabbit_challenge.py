# code_rabbit_challenge.py
# Purpose: Trigger multiple defects for CodeRabbit review

def sum_odd_numbers(lst):
    # Sum all odd numbers in the list
    total = 0
    for i in range(len(lst)):
        if lst[i] % 2 = 1:  # Issue: wrong operator, should be '=='
            total += lst[i]
    return total

def factorial(n):
    # Calculate factorial recursively
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)  # Issue: no input validation, stack overflow possible

def find_duplicates(lst):
    # Find duplicates in a list
    duplicates = []
    for i in lst:
        if lst.count(i) > 1:
            duplicates.append(i)  # Issue: inefficient, duplicates repeated
    return duplicates

def string_stats(s):
    # Count letters, digits, and spaces
    letters = 0
    digits = 0
    spaces = 0
    for char in s:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            digits += 1
        else:
            spaces += 1  # Issue: counts punctuation as space
    return letters, digits, spaces

def unsafe_access(lst, index):
    return lst[index]  # Issue: no bounds check, may throw IndexError

# Test the functions
numbers = [1, 2, 3, 3, 4, 5, 5, 5]
print("Sum of odd numbers:", sum_odd_numbers(numbers))
print("Factorial of 5:", factorial(5))
print("Duplicates found:", find_duplicates(numbers))
print("String stats:", string_stats("Hello 123!"))
print("Unsafe access:", unsafe_access(numbers, 10))  # Will throw IndexError
