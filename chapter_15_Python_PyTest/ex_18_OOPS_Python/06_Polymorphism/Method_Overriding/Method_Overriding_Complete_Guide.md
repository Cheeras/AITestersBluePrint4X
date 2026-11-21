# Method Overriding in Python — Complete Guide

## What is Method Overriding?

**Method overriding** happens when a **child class redefines a method** that already exists in its **parent class** with the **same name and same parameters**. The child's version **replaces** the parent's version for that child's objects.

**Real-world analogy — a child's voice 🗣️:**

- **Parent says:** `make_sound()` → "Generic sound"
- **Dog inherits** and **overrides**: `make_sound()` → "Woof!"
- **Cat inherits** and **overrides**: `make_sound()` → "Meow!"

Same method name, same signature — but **each child has its own version**!

```text
        ┌─────────────────────────────┐
        │         Animal (Parent)      │
        │  make_sound() → "Generic"    │
        └──────────────┬──────────────┘
                       │ inherits
           ┌───────────┴───────────┐
           │                       │
   ┌───────┴───────┐       ┌───────┴───────┐
   │  Dog (Child)   │       │  Cat (Child)  │
   │  make_sound()  │       │  make_sound() │
   │  → "Woof!" ✅  │       │  → "Meow!" ✅ │
   └───────────────┘       └───────────────┘
```

---

## ELI5 — Method Overriding for a 5th Grader 🧒

**Imagine your family has a tradition:** every Sunday, someone cooks dinner.

- **Grandma** cooks: `cook()` → "I make traditional biryani 🍛"
- **Mom** *overrides* it: `cook()` → "I make fusion biryani with paneer 🍛"
- **You** *override* it: `cook()` → "I order pizza 🍕"

Same job name (`cook()`), same job title — but **everyone does it their own way**. The kid (child class) gets to **replace** how the task works!

```python
class Grandma:                 # Parent
    def cook(self):
        print("Traditional biryani 🍛")

class Mom(Grandma):            # Child — overrides cook()
    def cook(self):
        print("Fusion biryani with paneer 🍛")

class Me(Mom):                 # Grandchild — overrides again!
    def cook(self):
        print("Order pizza 🍕")

print("Grandma:", Grandma().cook())   # Traditional biryani
print("Mom:    ", Mom().cook())       # Fusion biryani
print("Me:     ", Me().cook())        # Order pizza
```

**One sentence:** *Method overriding = the child gets the parent's method and replaces it with its own version.* 🔄

---

## Method Overriding vs Method Overloading — CRITICAL Difference ⚠️

These two sound similar but are **completely different**:

| Aspect | **Overloading** | **Overriding** |
|--------|-----------------|----------------|
| **What** | Same name, **different parameters** | Same name, **same parameters** |
| **Where** | **Same class** (multiple versions) | **Parent → Child** (across classes) |
| **Why** | Handle different argument counts | Replace parent behavior |
| **Inheritance needed?** | ❌ No | ✅ **Yes — required** |
| **Python support?** | ❌ Not natively (simulate with defaults) | ✅ **Yes — fully supported** |
| **Java comparison** | Compile-time | Runtime (dynamic dispatch) |

```python
# OVERLOADING (same class, different params)
class Math:
    def add(self, a, b, c=0):   # one flexible method
        return a + b + c

# OVERRIDING (parent → child, same signature)
class Animal:
    def sound(self):
        print("Generic sound")

class Dog(Animal):
    def sound(self):           # SAME name, SAME params = OVERRIDE
        print("Woof!")
```

---

## Simple Example — From Your Own Repo 🗂️

### [155_MOverride.py](155_MOverride.py) — Basic Overriding

```python
class BaseTest:
    def run(self):
        print("Running the Base Test")

class LoginTest(BaseTest):
    def run(self):                    # 🔄 OVERRIDES BaseTest.run()
        print("Running the Login Test")

t = BaseTest()
t.run()          # → "Running the Base Test"

t2 = LoginTest()
t2.run()         # → "Running the Login Test"  ← overridden!
```

**What happened?** `LoginTest` inherited `run()` from `BaseTest`, but then **replaced it** with its own version. When you call `t2.run()`, Python finds `LoginTest.run()` **first** (before looking up the parent) and uses it.

---

### [156_MOverride2.py](156_MOverride2.py) — Hierarchical Overriding

```python
class TestSuite:
    def info(self):
        print("Test suite information")

class BaseTest(TestSuite):
    def setup(self):
        print("Base setup")

    def run(self):
        print("Base Test execution")

class LoginTest(BaseTest):
    def run(self):                    # 🔄 Overrides BaseTest.run()
        print("Login Test execution")

class APITest(BaseTest):
    def run(self):                    # 🔄 Overrides BaseTest.run()
        print("API Test execution")

t1 = LoginTest()
t2 = APITest()
t3 = BaseTest()

t1.run()   # → "Login Test execution"
t2.run()   # → "API Test execution"
t3.run()   # → "Base Test execution"
```

**This is the POWER of overriding:** One method name `run()` — but **3 different behaviors** depending on which object calls it! This is **polymorphism** in action. 🎯

---

## What Exactly is Being Overridden?

### 1. Override Instance Methods (most common)

```python
class Payment:
    def process(self):
        print("Processing payment (generic)")

class CreditCard(Payment):
    def process(self):               # Override
        print("Processing via Credit Card 💳")

class UPI(Payment):
    def process(self):               # Override
        print("Processing via UPI 📱")
```

### 2. Override `__init__` (constructor) — VERY Common!

```python
class BaseTest:
    def __init__(self, browser):
        self.browser = browser
        print(f"BaseTest initialized with {browser}")

class LoginTest(BaseTest):
    def __init__(self, browser, username):   # 🔄 Overrides __init__
        super().__init__(browser)            # ✅ Call parent constructor!
        self.username = username
        print(f"LoginTest for {username}")

t = LoginTest("Chrome", "admin@test.com")
# BaseTest initialized with Chrome
# LoginTest for admin@test.com
```

> ⚠️ **Key note:** When overriding `__init__`, ALWAYS call `super().__init__(...)` if the parent sets up important state!

### 3. Override Built-in Magic Methods (dunder methods)

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):                # 🔄 Override built-in str()
        return f"₹{self.amount}"

    def __add__(self, other):         # 🔄 Override + operator!
        return Money(self.amount + other.amount)

m1 = Money(100)
m2 = Money(250)
print(m1)            # → ₹100  (custom __str__)
print(m1 + m2)       # → ₹350  (custom __add__)
```

---

## The Magic of `super()` — Calling the Parent's Version

Sometimes you want the child's version **AND** the parent's logic too. Use `super()`:

```python
class BaseTest:
    def setup(self):
        print("1. Launching browser")

    def run(self):
        self.setup()
        print("2. Running base test")

class LoginTest(BaseTest):
    def run(self):                      # Override
        super().run()                   # 🔄 Parent logic FIRST
        print("3. Running login-specific steps")
        print("4. Verifying login page")

t = LoginTest()
t.run()
# 1. Launching browser
# 2. Running base test
# 3. Running login-specific steps
# 4. Verifying login page
```

**Why is this huge for QA?** The base framework handles browser setup (parent), while each test adds its own logic (child) — without repeating the setup code!

---

## Real-World Examples 🌍

### 1. Test Automation Framework (THE classic QA example 🎯)

```python
class BaseTest:
    def __init__(self, browser):
        self.browser = browser

    def setup(self):
        print(f"Launching {self.browser} browser")

    def teardown(self):
        print(f"Closing {self.browser} browser")

    def run(self):
        self.setup()
        print("Running generic test steps")
        self.teardown()

class LoginTest(BaseTest):
    def run(self):                          # 🔄 Override
        self.setup()
        print("Entering username & password")
        print("Clicking login button")
        print("Verifying dashboard")
        self.teardown()

class PaymentTest(BaseTest):
    def run(self):                          # 🔄 Override
        self.setup()
        print("Adding item to cart")
        print("Processing payment")
        print("Verifying order confirmation")
        self.teardown()

LoginTest("Chrome").run()
PaymentTest("Firefox").run()
```

**Real-world reason:** One `BaseTest` provides `setup()`/`teardown()` for everyone, and each test **overrides** only `run()` with its unique steps. No repetition!

---

### 2. Animal Sounds (Polymorphism classic 🐾)

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print(f"{self.name} makes a sound")

class Dog(Animal):
    def make_sound(self):          # 🔄 Override
        print(f"{self.name} barks: Woof!")

class Cat(Animal):
    def make_sound(self):          # 🔄 Override
        print(f"{self.name} meows: Meow!")

class Duck(Animal):
    def make_sound(self):          # 🔄 Override
        print(f"{self.name} quacks: Quack!")

# Polymorphism: same call, different behavior!
for animal in [Dog("Rex"), Cat("Kitty"), Duck("Donald")]:
    animal.make_sound()
# Rex barks: Woof!
# Kitty meows: Meow!
# Donald quacks: Quack!
```

---

### 3. Shape Area Calculator (Math/Design 📐)

```python
class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):                    # 🔄 Override
        return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):                    # 🔄 Override
        return self.w * self.h

shapes = [Circle(5), Rectangle(4, 6)]
for s in shapes:
    print(f"Area: {s.area()}")
# Area: 78.5
# Area: 24
```

---

### 4. Employee Salary (HR System 💰)

```python
class Employee:
    def __init__(self, name, base):
        self.name = name
        self.base = base

    def salary(self):
        return self.base

class Developer(Employee):
    def salary(self):                  # 🔄 Override — adds bonus
        return self.base + 10000

class Manager(Employee):
    def salary(self):                  # 🔄 Override — adds higher bonus
        return self.base + 25000

dev = Developer("Alice", 60000)
mgr = Manager("Bob", 60000)
print(dev.salary())    # → 70000
print(mgr.salary())    # → 85000
```

---

## __init__ Overriding — The `super().__init__()` Pattern (Must Know!)

```python
class Animal:
    def __init__(self, name):       # Parent constructor
        self.name = name
        print(f"Animal created: {name}")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)      # 🔑 MUST call parent's __init__
        self.breed = breed
        print(f"Dog breed: {breed}")

d = Dog("Rex", "German Shepherd")
# Animal created: Rex
# Dog breed: German Shepherd
print(d.name)    # → Rex (set by parent)
print(d.breed)   # → German Shepherd (set by child)
```

---

## Method Resolution Order (MRO) — Which Version Gets Called?

When you call a method on an object, Python searches in this order:

```text
1. Child class itself          ← found? use it (OVERRIDE!)
2. Parent class
3. Grandparent class
4. ...up the chain
```

```python
class GrandParent:
    def greet(self):
        print("Hello from GrandParent")

class Parent(GrandParent):
    def greet(self):           # Overrides GrandParent
        print("Hello from Parent")

class Child(Parent):
    pass                       # No override — uses Parent's version

Child().greet()   # → "Hello from Parent"  (nearest override wins)

print(Child.__mro__)
# (<class 'Child'>, <class 'Parent'>, <class 'GrandParent'>, <class 'object'>)
```

---

## Overriding vs Overloading — One Final Comparison

```python
# ─── OVERLOADING (Python style: default params) ───
class Math:
    def greet(self, name="World"):      # Same class, flexible params
        return f"Hello, {name}!"

m = Math()
m.greet()               # Hello, World!
m.greet("Shankar")      # Hello, Shankar!

# ─── OVERRIDING (parent → child, same signature) ───
class Greeter:
    def greet(self):
        return "Hello, World!"

class HindiGreeter(Greeter):
    def greet(self):                    # Same name, same params
        return "Namaste, Duniya!"

HindiGreeter().greet()   # → "Namaste, Duniya!"
```

---

## Quick Reference Cheat-Sheet

```text
OVERRIDING:
  ✅ Child redefines parent's method (same name + same params)
  ✅ Works fully in Python (unlike overloading!)
  ✅ Uses inheritance — REQUIRED
  ✅ super().method() calls the parent's version
  ✅ Polymorphism: same call, different result per object

WHEN TO OVERRIDE:
  • Customize setup/teardown per test (QA)
  • Different behaviors per subclass (Animal, Shape)
  • Extend __init__ with child-specific attributes
  • Customize magic methods (__str__, __add__)

DON'T FORGET:
  • super().__init__(...) when overriding constructor
  • MRO: nearest class in the chain wins
  • Overriding ≠ Overloading (see table above)
```

## Key Takeaways

1. **Method overriding** = child redefines a parent method with the **same name & parameters** — child's version wins
2. **Python FULLY supports overriding** (unlike overloading which needs simulation)
3. **`super()`** lets the child call the parent's version — essential for `__init__` and for extending behavior
4. **Polymorphism** is the payoff — one method name, many behaviors (your [156_MOverride2.py](156_MOverride2.py) shows `run()` doing 3 different things!)
5. **MRO** decides which version runs — child first, then up the chain
6. **Real-world:** Test frameworks (override `run()`), payment systems, shape calculators, HR salary logic — everywhere you need "same interface, different implementation"
7. **Memorize this pair:** *Overloading = same class, different params. Overriding = different classes, same params.* 🎯