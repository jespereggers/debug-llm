def process_data(data):
    try:
        for item in data:
            try:
                result = 10 / item
                print(f"Processed {item}: {result}")
            except ZeroDivisionError:
                print("Division by zero encountered")
            finally:
                print("Finally block executed in inner loop")
    except Exception as e:
        print(f"An error occurred in outer loop: {e}")

data = [1, 0, 'a', 5]
process_data(data)
