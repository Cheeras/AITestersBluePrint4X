# 2. Create a Laptop class with a default constructor 
# that sets brand = "Unknown"
class Laptop:
    def __init__(self):
        self.model = "Unknown"
        self.year = 0
        self.price = 0
        self.brand = "Unknown"

# Creating object for the laptop class - with no values passed inside
laptop1 = Laptop()
laptop2 = Laptop()

laptop1.brand = "HP"
laptop1.model = "Pavilion"
laptop1.year = 2022
laptop1.price = 35000



print(laptop1.brand,laptop1.model,laptop1.year,laptop1.price)
print(laptop2.brand,laptop2.model,laptop2.year,laptop2.price)