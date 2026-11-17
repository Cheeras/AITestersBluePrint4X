# 1. Create a Car class with a constructor that 
# takes brand, color, and year
class Car:

    def __init__(self,brand,color,year,model=None):
        self.brand = brand
        self.color = color
        self.year = year
        self.model = model

#Creating the car class object
car1 = Car("maruti","White",2025,"S-Cross")
car2 = Car("BMW","Blue",2024,"B8")

print(car1.brand,car1.color,car1.year,car1.model)
print(car2.brand,car2.color,car2.year,car2.model)
    
