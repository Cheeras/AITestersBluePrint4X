# 2. Create a Laptop class with a default constructor 
# that sets brand = "Unknown"
class Laptop:
    def __init__(self,model,year,price,brand="Unknown"):
        self.model = model
        self.year = year
        self.price = price
        self.brand = brand

# Creating object for the laptop class
laptop1 = Laptop("Pevilion",2022,35000,"HP")
laptop2 = Laptop("Notebook",2025,65000)

print(laptop1.brand,laptop1.model,laptop1.year,laptop1.price)
print(laptop2.brand,laptop2.model,laptop2.year,laptop2.price)