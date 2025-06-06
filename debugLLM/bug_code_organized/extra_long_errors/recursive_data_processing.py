def process_data(data):
    if isinstance(data, list):
        for item in data:
            process_data(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            print(f"Processing {key}: {value}")
            process_data(value)
    else:
        # Infinite recursion due to lack of base case for processing non-iterable data
        process_data(data)

data_structure = {
    'key1': [1, 2, 3],
    'key2': {
        'subkey1': 'value1',
        'subkey2': 'value2'
    },
    'key3': 'final_value'
}

process_data(data_structure)
