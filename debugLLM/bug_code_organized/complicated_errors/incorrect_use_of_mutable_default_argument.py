def append_to_list(value, my_list=[]):
    my_list.append(value)  # Mutable default argument
    return my_list

print(append_to_list(1))  # [1]
print(append_to_list(2))  # [1, 2] - Unexpected behavior
print(append_to_list(3))  # [1, 2, 3] - List is shared across calls
