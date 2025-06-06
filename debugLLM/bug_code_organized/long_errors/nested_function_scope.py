def outer_function(x):
	def inner_function(y):
		return x + y
	return inner_function(5)

outer_function(10)