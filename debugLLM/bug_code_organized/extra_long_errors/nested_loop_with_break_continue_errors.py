def search_value(matrix, target):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == target:
                print(f"Found {target} at position ({i}, {j})")
                break  # Incorrect usage of break
        else:
            continue  # This will skip printing when target is not found in the row

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
search_value(matrix, 5)
