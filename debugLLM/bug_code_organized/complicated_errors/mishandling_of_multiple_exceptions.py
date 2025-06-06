def divide_and_parse(value1, value2):
    try:
        result = int(value1) / int(value2)
    except (ValueError, ZeroDivisionError) as e:  # Catching multiple exceptions but treating them the same
        print(f"Error: {e}")
    return result

divide_and_parse("10", "0")  # ZeroDivisionError not clearly distinguished
divide_and_parse("abc", "10")  # ValueError treated the same way
