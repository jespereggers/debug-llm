def buggy_function():
	lst = []
	lst.append(1)
	lst.append(2)
	return lst.append(3).reverse()