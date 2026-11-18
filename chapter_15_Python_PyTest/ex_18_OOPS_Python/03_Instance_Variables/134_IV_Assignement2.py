## Assignment 2: Shopping Cart (Real-world E-commerce)
"""
Create a class `ShoppingCart` with:

- A **global variable** `tax_rate = 0.18` (18% GST)
- An **instance variable** `items` (list of item prices)
- A **local variable** `subtotal` inside a method
"""

tax_rate = 0.18

class ShoppingCart:
    def __init__(self,customerName):
        self.customerName = customerName
        self.items = []

    def add_item(self,price):
        self.items.append(price)

    def calculate_bill(self):
        subTotal = sum(self.items)
        tax = subTotal * tax_rate
        total = subTotal + tax
        print(f"Customer: {self.customerName}")
        print(f"Items: {self.items}")
        print(f"Subtotal: ₹{subTotal}")
        print(f"Tax ({tax_rate*100}%): ₹{tax}")
        print(f"Total: ₹{total}")

# Test
cart = ShoppingCart("John")
cart.add_item(500)
cart.add_item(1200)
cart.add_item(300)
cart.calculate_bill()