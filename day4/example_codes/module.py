def greeting(name):
    print("Hello, " + name)

    
person1 = {
    "name": "John",
    "age": 36,
    "country": "Norway"
}

class Octopus:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def tell_me_about_the_octopus(self):
        print(f"This octopus is {self.color}.")
        print(f"{self.name} is the octopus's name.")
        