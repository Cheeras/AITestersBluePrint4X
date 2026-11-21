# Abstraction

# Hide the details and show what is required

# Car - With key __private, tyres -> public,

# car -> multiple - Engine, GearBox

# car -> driver -> Engine, gearbox

from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def sound(self):
        pass

class Dog(Animal):
    def sound(self):
        print("Bark!")

dog = Dog("PP")
dog.sound()