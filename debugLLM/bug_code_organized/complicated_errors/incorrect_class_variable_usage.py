class Counter:
    count = 0  # Class variable shared by all instances

    def __init__(self):
        Counter.count += 1

    def get_count(self):
        return Counter.count

counter1 = Counter()
counter2 = Counter()
counter3 = Counter()

print(counter1.get_count())  # Returns 3 for all instances, not expected behavior
print(counter2.get_count())
print(counter3.get_count())
