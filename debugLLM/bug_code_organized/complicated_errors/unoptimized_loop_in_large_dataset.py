def process_large_dataset(dataset):
    result = []
    for i in range(len(dataset)):
        for j in range(len(dataset)):  # Nested loop causing inefficiency
            if dataset[i] == dataset[j]:
                result.append(dataset[i])
    return result

large_dataset = [i for i in range(1000)]
print(process_large_dataset(large_dataset))  # Extremely inefficient for large datasets
