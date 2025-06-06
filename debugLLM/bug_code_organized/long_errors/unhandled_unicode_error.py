def write_to_file(text):
	with open('test.txt', 'w', encoding='ascii') as f:
		f.write(text)

write_to_file('Hello 😊')