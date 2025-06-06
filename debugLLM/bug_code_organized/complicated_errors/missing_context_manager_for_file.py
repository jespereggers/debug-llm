def read_file(file_path):
    file = open(file_path, "r")  # Missing context manager (with open...)
    try:
        content = file.read()
    finally:
        file.close()  # Error-prone: What if there's an exception during file read?

print(read_file("example.txt"))
