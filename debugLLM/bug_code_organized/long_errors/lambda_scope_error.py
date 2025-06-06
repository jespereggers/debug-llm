def create_lambda():
	funcs = []
	for i in range(5):
		funcs.append(lambda: print(i))
	return funcs

funcs = create_lambda()
for f in funcs:
	f()