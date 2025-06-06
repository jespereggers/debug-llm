def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)  # Inefficient recursive calls

print(fibonacci(50))  # Stack overflow due to large recursion depth
