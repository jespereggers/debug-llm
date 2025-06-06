def outer_function():
	def middle_function():
		def inner_function():
			return 1 / 0
		return inner_function()
	return middle_function()

outer_function()