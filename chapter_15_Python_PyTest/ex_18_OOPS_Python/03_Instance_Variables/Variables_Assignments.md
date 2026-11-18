# Instance, Local & Global Variables — Practice Assignments

---

## Quick Refresher

| Variable Type            | Where Declared                | How to Access              | Lifetime                 |
| ------------------------ | ----------------------------- | -------------------------- | ------------------------ |
| **Global**         | Outside any class/function    | Directly by name (`g`)   | Entire program           |
| **Class/Instance** | Inside class, outside methods | `self.var_name`          | As long as object exists |
| **Local**          | Inside a method/function      | Directly by name (`var`) | Only inside that method  |

---

## Assignment 1: Employee Salary Calculator (Real-world HR scenario)

Create a class `Employee` with:

- A **global variable** `company_name = "TechCorp"`
- An **instance variable** `salary` set via constructor
- A **local variable** `bonus` inside a method that calculates total pay

```python
# Global variable
company_name = "TechCorp"

class Employee:
    def __init__(self, name, salary):
        self.name = name          # Instance variable
        self.salary = salary      # Instance variable

    def calculate_total_pay(self):
        bonus = 5000              # Local variable
        total = self.salary + bonus  # Local variable
        print(f"{self.name} at {company_name}")
        print(f"Base: ₹{self.salary}, Bonus: ₹{bonus}, Total: ₹{total}")

# Test
e1 = Employee("Alice", 50000)
e2 = Employee("Bob", 60000)
e1.calculate_total_pay()
e2.calculate_total_pay()
```

**Expected Output:**

```
Alice at TechCorp
Base: ₹50000, Bonus: ₹5000, Total: ₹55000
Bob at TechCorp
Base: ₹60000, Bonus: ₹5000, Total: ₹65000
```

---

## Assignment 2: Shopping Cart (Real-world E-commerce)

Create a class `ShoppingCart` with:

- A **global variable** `tax_rate = 0.18` (18% GST)
- An **instance variable** `items` (list of item prices)
- A **local variable** `subtotal` inside a method

```python
# Global variable
tax_rate = 0.18

class ShoppingCart:
    def __init__(self, customer_name):
        self.customer_name = customer_name  # Instance variable
        self.items = []                      # Instance variable

    def add_item(self, price):
        self.items.append(price)

    def calculate_bill(self):
        subtotal = sum(self.items)           # Local variable
        tax = subtotal * tax_rate            # Local variable
        total = subtotal + tax               # Local variable
        print(f"Customer: {self.customer_name}")
        print(f"Items: {self.items}")
        print(f"Subtotal: ₹{subtotal}")
        print(f"Tax ({tax_rate*100}%): ₹{tax}")
        print(f"Total: ₹{total}")

# Test
cart = ShoppingCart("John")
cart.add_item(500)
cart.add_item(1200)
cart.add_item(300)
cart.calculate_bill()
```

---

## Assignment 3: Bank Account (Real-world Banking)

Create a class `BankAccount` with:

- A **global variable** `bank_name = "National Bank"`
- An **instance variable** `balance` that starts with a deposit
- A **local variable** `transaction_fee` inside the withdraw method

```python
# Global variable
bank_name = "National Bank"

class BankAccount:
    def __init__(self, account_holder, initial_deposit):
        self.account_holder = account_holder  # Instance variable
        self.balance = initial_deposit         # Instance variable

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited ₹{amount}. New balance: ₹{self.balance}")

    def withdraw(self, amount):
        transaction_fee = 10                   # Local variable
        total_deduction = amount + transaction_fee  # Local variable
        if self.balance >= total_deduction:
            self.balance -= total_deduction
            print(f"Withdrew ₹{amount} (fee: ₹{transaction_fee})")
            print(f"Remaining balance: ₹{self.balance}")
        else:
            print("Insufficient balance!")

    def display(self):
        print(f"{bank_name} — Account Holder: {self.account_holder}")
        print(f"Balance: ₹{self.balance}")

# Test
acc = BankAccount("Priya", 10000)
acc.display()
acc.deposit(5000)
acc.withdraw(2000)
acc.display()
```

---

## Assignment 4: Student Grade Tracker (Real-world Education)

Create a class `Student` with:

- A **global variable** `school = "Greenwood High"`
- An **instance variable** `marks` (dictionary of subject: score)
- A **local variable** `total` and `average` inside the grade method

```python
# Global variable
school = "Greenwood High"

class Student:
    def __init__(self, name):
        self.name = name          # Instance variable
        self.marks = {}           # Instance variable

    def add_mark(self, subject, score):
        self.marks[subject] = score

    def calculate_grade(self):
        total = sum(self.marks.values())           # Local variable
        average = total / len(self.marks)          # Local variable
        grade = "A" if average >= 90 else "B" if average >= 75 else "C"  # Local

        print(f"{school} — Student: {self.name}")
        print(f"Marks: {self.marks}")
        print(f"Total: {total}, Average: {average:.1f}, Grade: {grade}")

# Test
s = Student("Rahul")
s.add_mark("Math", 95)
s.add_mark("Science", 88)
s.add_mark("English", 92)
s.calculate_grade()
```

---

## Assignment 5: Fix the Bug (Test your understanding)

This code has **3 bugs** related to variable scope. Find and fix them:

```python
discount = 0.10  # Global: 10% discount

class Order:
    def __init__(self, item, price):
        self.item = item
        self.price = price

    def apply_discount(self):
        discounted_price = self.price * (1 - discount)  # Local
        print(f"Item: {self.item}")
        print(f"Original: ₹{self.price}")
        print(f"Discounted: ₹{discounted_price}")

    def print_receipt(self):
        tax = self.price * 0.08
        final = self.price + tax
        print(f"Item: {self.item}")
        print(f"Tax: ₹{tax}")
        print(f"Final: ₹{final}")
        print(f"Discounted price was: ₹{discounted_price}")  # ❌ Bug 1

order = Order("Laptop", 50000)
order.apply_discount()
order.print_receipt()
print(f"Item name: {item}")  # ❌ Bug 2
print(f"Price: {price}")     # ❌ Bug 3
```

**Bugs to fix:**

1. `discounted_price` is local to `apply_discount()` — can't access it in `print_receipt()`
2. `item` is an instance variable — must use `order.item` or `self.item`
3. `price` is an instance variable — must use `order.price` or `self.price`

---

## Assignment 6: Real-world Test Automation Example

Create a class `APITest` that simulates API testing:

```python
# Global variable — test environment URL
base_url = "https://api.example.com"

class APITest:
    total_tests = 0  # Class variable to count all tests

    def __init__(self, test_name, endpoint):
        self.test_name = test_name      # Instance variable
        self.endpoint = endpoint        # Instance variable
        self.status = None              # Instance variable
        APITest.total_tests += 1

    def execute(self):
        response_code = 200             # Local variable (simulated)
        response_time_ms = 150          # Local variable (simulated)
        self.status = "PASS" if response_code == 200 else "FAIL"

        print(f"Test: {self.test_name}")
        print(f"URL: {base_url}{self.endpoint}")
        print(f"Response: {response_code} ({response_time_ms}ms)")
        print(f"Status: {self.status}")
        print(f"Total tests run: {APITest.total_tests}")
        print("-" * 30)

# Test
t1 = APITest("Get Users", "/users")
t2 = APITest("Create User", "/users/create")
t1.execute()
t2.execute()
```

---

## Summary Table — When to Use What

| Scenario                        | Use                                        | Example                                          |
| ------------------------------- | ------------------------------------------ | ------------------------------------------------ |
| Value shared across ALL objects | **Global variable**                  | `tax_rate`, `company_name`, `base_url`     |
| Value unique to EACH object     | **Instance variable** (`self.xxx`) | `self.name`, `self.salary`, `self.balance` |
| Temporary value inside a method | **Local variable**                   | `bonus`, `subtotal`, `total`, `average`  |

---

## Practice on Your Own

Try creating these:

1. **Library System** — Global: `library_name`, Instance: `book_title`, `is_borrowed`, Local: `due_date` in a method
2. **Cab Booking** — Global: `base_fare_per_km`, Instance: `passenger_name`, `distance`, Local: `total_fare` in a method
3. **Restaurant Bill** — Global: `service_tax`, Instance: `table_no`, `items_ordered`, Local: `bill_total` in a method
