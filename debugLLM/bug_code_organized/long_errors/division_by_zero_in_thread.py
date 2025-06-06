import threading

def worker(shared_data):
	shared_data.append(10 / 0)

threads = []
shared_data = []
for _ in range(3):
	thread = threading.Thread(target=worker, args=(shared_data,))
	threads.append(thread)
	thread.start()

for thread in threads:
	thread.join()