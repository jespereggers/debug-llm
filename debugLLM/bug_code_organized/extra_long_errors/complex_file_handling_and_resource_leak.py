import os

def process_files(file_list):
    for file_name in file_list:
        try:
            f = open(file_name, 'r')
            data = f.read()
            if len(data) > 0:
                process_data(data)
        except FileNotFoundError:
            print(f"File {file_name} not found")
        except Exception as e:
            print(f"An error occurred: {e}")
            continue
        # File is not properly closed in case of an exception
        os.remove(file_name)  # Removing files even if they were not processed correctly

def process_data(data):
    for line in data.splitlines():
        print(line.upper())

process_files(['nonexistent1.txt', 'nonexistent2.txt'])
