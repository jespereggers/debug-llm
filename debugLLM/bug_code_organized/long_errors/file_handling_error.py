def read_file(filename):
	f = open(filename, "r")
	content = f.read()
	f.close()
	return content