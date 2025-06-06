def infinite_loop():
	x = 0
	while True:
		x += 1
		if x == 100:
			continue  # Continue instead of break causes infinite loop