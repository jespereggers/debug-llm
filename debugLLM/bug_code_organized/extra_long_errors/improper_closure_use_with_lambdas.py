def generate_functions():
    functions = []
    for i in range(5):
        functions.append(lambda: print(i))  # Incorrect closure, all will print the same value
    return functions

funcs = generate_functions()
for func in funcs:
    func()
