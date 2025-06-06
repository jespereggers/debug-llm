def get_element_at_index(lst, index):
    return lst[index]  # No check for index out of bounds

my_list = [1, 2, 3, 4]
print(get_element_at_index(my_list, 5))  # Raises IndexError
