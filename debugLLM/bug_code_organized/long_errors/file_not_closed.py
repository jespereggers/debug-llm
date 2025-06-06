def read_data(file_path):
	f = open(file_path, 'r')
	data = f.read()
	if not data:
		print('File is empty')
	# File is never closed
	return data