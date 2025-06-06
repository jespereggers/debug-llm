class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement abstract method")

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

    def speak(self):
        return "Woof!"

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)

    def speak(self):
        return "Meow!"

class Bird(Animal):  # Bird doesn't override the speak method, causing an error
    def __init__(self, name):
        super().__init__(name)

animals = [Dog("Fido"), Cat("Whiskers"), Bird("Tweety")]

for animal in animals:
    print(animal.speak())  # Raises NotImplementedError for Bird
