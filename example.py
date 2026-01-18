# Example Python file for testing pycole


def calculate_sum(numbers):
    """Calculate the sum of a list of numbers."""
    total = 0
    for num in numbers:
        total += num
    return total


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0
    return calculate_sum(numbers) / len(numbers)


# Main execution
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    print(f"Sum: {calculate_sum(data)}")
    print(f"Average: {calculate_average(data)}")
