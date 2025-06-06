def outer_function():
	x = 10
	def inner_function():
		x += 1
	inner_function()
	return x