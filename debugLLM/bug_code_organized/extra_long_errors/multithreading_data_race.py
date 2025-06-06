import threading

shared_data = 0

def increment_data():
    global shared_data
    for _ in range(1000):
        shared_data += 1  # No synchronization, leading to race conditions

threads = []
for _ in range(10):
    t = threading.Thread(target=increment_data)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final value of shared_data: {shared_data}")
