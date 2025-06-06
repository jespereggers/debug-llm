def divide_numbers(numbers, divisor):
    results = []
    for number in numbers:
        try:
            result = number / divisor
            results.append(result)
        except ZeroDivisionError:
            results.append(None)
    return results

numbers = [10, 20, 30]
divisor = 0  # Division by zero, exception handled but leads to issues
print(divide_numbers(numbers, divisor))
