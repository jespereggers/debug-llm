count = 0

def increment():
    global count  # Unnecessary use of global variable
    count += 1

for i in range(100):
    increment()

print(count)
