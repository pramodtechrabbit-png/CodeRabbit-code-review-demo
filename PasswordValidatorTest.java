# Example Python function for CodeRabbit review
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers)
    return average

# Test the function
nums = [10, 20, 30, 40]
print("Average:", calculate_average(nums))
