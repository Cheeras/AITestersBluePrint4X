# Python Constructors — Complete Guide for Beginners

---

## 1. What is a Constructor?

A **constructor** is a special method that **automatically runs** when you create an object from a class. Its job is to **initialize** (set up) the object's data.

In Python, the constructor is always named `__init__` (short for **init**ialize).

### Real-world analogy

Think of a constructor like the **setup process** when you buy a new phone:

- When you unbox a new phone, it already has some default settings
- You can also configure it with your preferences (name, language, etc.)
- This setup happens **automatically** when you first turn it on

Similarly, when you create an object (`MobilePhone()`), the constructor runs automatically to set it up.

---

## 2. Your Code Explained

```python
class MobilePhone:
    model = None

    def __init__(self):                    # ← This is the CONSTRUCTOR
        print("I will be called, when obj is created!")

    def talk(self):
        print("Normal F(n)")

iphone = MobilePhone()  # ← Creating object → Constructor runs automatically!
```

**Output:**

```
I will be called, when obj is created!
```

Notice: You **never called** `__init__` directly. It ran **automatically** the moment you wrote `MobilePhone()`.

---

## 3. How to Create a Constructor

### Syntax:

```python
class ClassName:
    def __init__(self):
        # Initialization code here
        pass
```

### Rules:

| Rule                        | Explanation                                      |
| --------------------------- | ------------------------------------------------ |
| Name must be `__init__`   | Double underscores on both sides (dunder method) |
| First parameter is `self` | Refers to the current object being created       |
| Runs automatically          | No need to call it manually                      |
| Can have parameters         | To accept values at the time of object creation  |

---

## 4. Types of Constructors

### A. Default (Non-parameterized) Constructor

Takes **only `self`** — no extra parameters.

```python
class MobilePhone:
    def __init__(self):
        print("Default Constructor: Object created!")
        self.brand = "Unknown"   # Default value

nokia = MobilePhone()   # Output: Default Constructor: Object created!
print(nokia.brand)      # Output: Unknown
```

### B. Parameterized Constructor

Takes `self` **plus additional parameters** to set custom values.

```python
class MobilePhone:
    def __init__(self, brand, model):    # ← Parameters besides self
        print("Parameterized Constructor called!")
        self.brand = brand               # Assign parameter to instance
        self.model = model

# Pass values when creating the object
iphone = MobilePhone("Apple", "iPhone 18 Pro Max")
#                      ↑         ↑
#                   brand       model

print(iphone.brand)   # Output: Apple
print(iphone.model)   # Output: iPhone 18 Pro Max
```

---

## 5. How to Call a Constructor

### ❌ Wrong way (don't do this):

```python
iphone.__init__()   # You NEVER call __init__ directly
```

### ✅ Right way (just create the object):

```python
iphone = MobilePhone()                # Calls default constructor
samsung = MobilePhone("Samsung", "S25 Ultra")  # Calls parameterized constructor
```

Python automatically calls `__init__` when you use `ClassName()`.

---

## 6. Parameterized Constructor — Deep Dive

### Example 1: One parameter

```python
class Student:
    def __init__(self, name):
        self.name = name
        print(f"Student {self.name} created!")

s1 = Student("Alice")   # Output: Student Alice created!
s2 = Student("Bob")     # Output: Student Bob created!
```

### Example 2: Multiple parameters

```python
class MobilePhone:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price
        print(f"{brand} {model} created — ₹{price}")

iphone = MobilePhone("Apple", "iPhone 18", 89999)
# Output: Apple iPhone 18 created — ₹89999

samsung = MobilePhone("Samsung", "S25 Ultra", 129999)
# Output: Samsung S25 Ultra created — ₹129999
```

### Example 3: With default parameter values

```python
class MobilePhone:
    def __init__(self, brand="Unknown", model="Unknown", price=0):
        self.brand = brand
        self.model = model
        self.price = price

p1 = MobilePhone()                          # All defaults
p2 = MobilePhone("Apple")                   # Only brand
p3 = MobilePhone("Samsung", "S25")          # Brand + model
p4 = MobilePhone("OnePlus", "12", 69999)    # All values
```

---

## 7. Compare: Without Constructor vs With Constructor

### ❌ Without constructor (tedious way)

```python
class MobilePhone:
    brand = None
    model = None
    price = None

iphone = MobilePhone()
iphone.brand = "Apple"        # Setting each attribute manually
iphone.model = "iPhone 18"    # ← Lots of repetitive code
iphone.price = 89999          # ← Easy to forget something
```

### ✅ With constructor (clean way)

```python
class MobilePhone:
    def __init__(self, brand, model, price):
        self.brand = brand
        self.model = model
        self.price = price

iphone = MobilePhone("Apple", "iPhone 18", 89999)  # One line!
```

---

## 8. `self` in the Constructor

Remember `self` from the previous guide? In the constructor, `self` refers to the **object being created**.

```python
class MobilePhone:
    def __init__(self, brand):
        # self = the new object (e.g., iphone)
        # brand = "Apple" (the value passed)
        self.brand = brand   # Means: iphone.brand = "Apple"

iphone = MobilePhone("Apple")
# Python internally does:
# 1. Creates a new empty object
# 2. Calls __init__(iphone, "Apple")
# 3. Inside: iphone.brand = "Apple"
```

---

## 9. Complete Working Example

```python
class MobilePhone:
    # Constructor — runs automatically when object is created
    def __init__(self, brand, model, price):
        print(f"📱 Creating a new {brand} phone...")
        self.brand = brand
        self.model = model
        self.price = price
        print(f"✅ {brand} {model} created! Price: ₹{price}\n")

    # Regular method
    def display_info(self):
        print(f"Brand: {self.brand}")
        print(f"Model: {self.model}")
        print(f"Price: ₹{self.price}")
        print("-" * 20)

# Create objects — constructor runs automatically each time
iphone = MobilePhone("Apple", "iPhone 18 Pro Max", 129999)
samsung = MobilePhone("Samsung", "S25 Ultra", 109999)
oneplus = MobilePhone("OnePlus", "12", 69999)

# Call methods on the objects
iphone.display_info()
samsung.display_info()
oneplus.display_info()
```

**Output:**

```
📱 Creating a new Apple phone...
✅ Apple iPhone 18 Pro Max created! Price: ₹129999

📱 Creating a new Samsung phone...
✅ Samsung S25 Ultra created! Price: ₹109999

📱 Creating a new OnePlus phone...
✅ OnePlus 12 created! Price: ₹69999

Brand: Apple
Model: iPhone 18 Pro Max
Price: ₹129999
--------------------
Brand: Samsung
Model: S25 Ultra
Price: ₹109999
--------------------
Brand: OnePlus
Model: 12
Price: ₹69999
--------------------
```

---

## 10. Quick Summary

| Concept                             | What it means                                        |
| ----------------------------------- | ---------------------------------------------------- |
| **Constructor**               | A special method that runs when you create an object |
| **Method name**               | Always `__init__`                                  |
| **Purpose**                   | To initialize the object's data (attributes)         |
| **Called?**                   | Automatically — never call it manually              |
| **Default constructor**       | Takes only `self`, no extra parameters             |
| **Parameterized constructor** | Takes `self` + extra parameters for custom values  |
| **`self` in constructor**   | Refers to the new object being created               |

### One-line memory trick:

> **Constructor = "Setup that runs automatically when an object is born"**

---

## 11. Practice Yourself

Try creating these:

```python
# 1. Create a Car class with a constructor that takes brand, color, and year
# 2. Create a Laptop class with a default constructor that sets brand = "Unknown"
# 3. Create a Book class where the constructor prints "Book added!" every time
```
