class Shape:
    def __init__(self, color):
        self.color = color

    def draw(self):
        raise NotImplementedError("Subclasses must implement this method.")

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def draw(self):
        return f"Drawing a circle with radius {self.radius} and color {self.color}"

class Square(Shape):
    def __init__(self, color, side_length):
        # Forgot to call the superclass constructor
        self.side_length = side_length

    def draw(self):
        return f"Drawing a square with side length {self.side_length} and color {self.color}"

shapes = [Circle('red', 5), Square('blue', 4)]
for shape in shapes:
    print(shape.draw())
