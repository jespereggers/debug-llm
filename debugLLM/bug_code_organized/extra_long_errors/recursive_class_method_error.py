class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def insert(self, new_value):
        if new_value < self.value:
            if self.left is None:
                self.left = Node(new_value)
            else:
                self.left.insert(new_value)
        else:
            if self.right is None:
                self.right = Node(new_value)
            else:
                self.right.insert(new_value)

    def display(self):
        if self.left:
            self.left.display()
        print(self.value)
        if self.right:
            self.right.display()

root = Node(10)
values = [5, 3, 7, 15, 12, 20]
for v in values:
    root.insert(v)

# This will cause a recursive loop because display() prints values in incorrect order
root.display()
