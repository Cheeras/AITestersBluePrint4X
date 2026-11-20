# Inheritance in Python — Complete Guide

## What is Inheritance?

Inheritance is a core OOP concept where a **child class** acquires the properties and methods of a **parent class**. It promotes **code reuse** — you write common logic once in the parent and share it across multiple children.

**Real-world analogy:** A child inherits traits (eyes, height) from parents. The child has those traits automatically without redefining them.

```text
Parent Class (Base)   ──>  Child Class (Derived)
   ↑                          ↑
  General                   Specific
```

---

## ELI5 — Inheritance for a 5th Grader 🧒

**Imagine this:** You look like your mom or dad, right? Maybe you have your dad's eyes or your mom's smile. You didn't *do* anything to get them — you just **inherited** them. You were born with them!

**Inheritance in Python is exactly the same!**

A **child class** (like you) automatically gets the things a **parent class** (like your parents) has — without writing them again.

```python
class Mom:                    # 👩 Parent
    def smile(self):
        print("😊 Smiling")

class Baby(Mom):              # 👶 Child — Baby IS-A Mom's child
    pass                      # Baby wrote NOTHING here!

baby = Baby()
baby.smile()                  # 😊 Works! Baby inherited it!
```

See? The baby didn't write the `smile` code — it got it from Mom for free. **That's inheritance!**

### The School Playground Story 🏫

Let's use a real scenario every 5th grader knows — **a school**:

```python
class Student:                    # 👨‍🏫 Parent — ALL students have this
    def __init__(self, name):
        self.name = name

    def eat_lunch(self):
        print(f"{self.name} is eating lunch 🍎")

    def go_home(self):
        print(f"{self.name} is going home 🚌")

# Now the special kids — they inherit everything from Student!
class ArtStudent(Student):        # 🎨 Child 1
    def paint(self):
        print(f"{self.name} is painting 🎨")

class MusicStudent(Student):      # 🎵 Child 2
    def play_guitar(self):
        print(f"{self.name} is playing guitar 🎸")

# Test it!
riya = ArtStudent("Riya")
riya.eat_lunch()    # ✅ From Student (inherited!)
riya.paint()        # ✅ Riya's own skill

arjun = MusicStudent("Arjun")
arjun.go_home()     # ✅ From Student (inherited!)
arjun.play_guitar() # ✅ Arjun's own skill
```

**Why is this awesome?** Riya and Arjun both eat lunch and go home — but we wrote that code **ONCE** in `Student`. No copying, no repeating! If the school changes lunch time, we change it in ONE place.

**Remember this one sentence:** *Inheritance = a child class gets the parent's superpowers for free, then adds its own.* 🦸

---

## Types of Inheritance in Python

Python supports **5 types** of inheritance:

| # | Type | Description | Files |
|---|------|-------------|-------|
| 1 | **Single** | One child inherits from one parent | `143_SI.py` |
| 2 | **Multiple** | One child inherits from multiple parents | `144_MI.py`, `145_MI_002.py` |
| 3 | **Multilevel** | Chain: Grandparent → Parent → Child | `146_ML.py` |
| 4 | **Hierarchical** | One parent, multiple children | `147_HI.py` |
| 5 | **Hybrid** | Mix of multiple + multilevel | `148_Hybrid.py` |

---

## 1. Single Inheritance

**One parent → One child**

```mermaid
classDiagram
    class BaseTest {
        +setup()
    }
    class LoginTest {
        +run()
    }
    BaseTest <|-- LoginTest
```

```python
class BaseTest:
    def setup(self):
        print("Launching browser")

class LoginTest(BaseTest):   # LoginTest IS-A BaseTest
    def run(self):
        self.setup()         # Inherited method
        print("Running login test")

t = LoginTest()
t.setup()  # From parent
t.run()    # From child
```

**Real-world use:** A base page class → specific page class (LoginPage, HomePage).

---

## 2. Multiple Inheritance

**Multiple parents → One child**

```mermaid
classDiagram
    class APIBase {
        +api_auth()
    }
    class DBBase {
        +db_connect()
    }
    class TestHybrid {
        +run()
    }
    APIBase <|-- TestHybrid
    DBBase <|-- TestHybrid
```

```python
class APIBase:
    def api_auth(self):
        print("Authenticating via API")

class DBBase:
    def db_connect(self):
        print("Connecting to database")

class TestHybrid(APIBase, DBBase):  # Inherits from BOTH
    def run(self):
        self.api_auth()
        self.db_connect()
        print("Running test")

tc = TestHybrid()
tc.run()
```

**⚠️ Diamond Problem & MRO:** If both parents have a method with the same name, Python uses **MRO (Method Resolution Order)** — left-to-right, depth-first.

```python
class Father1:
    def money(self):
        print("Father1's money")

class Father2:
    def money(self):
        print("Father2's money")

class Child(Father2, Father1):  # Father2 checked FIRST
    pass

c = Child()
c.money()  # Output: Father2's money (leftmost parent wins)
print(Child.__mro__)  # See the resolution order
```

**Real-world use:** A test class that needs both API authentication AND database connection.

---

## 3. Multilevel Inheritance

**Grandparent → Parent → Child (chain)**

```mermaid
classDiagram
    class TestSuite {
        +info()
    }
    class BaseTest {
        +setup()
    }
    class UITest {
        +run()
    }
    TestSuite <|-- BaseTest
    BaseTest <|-- UITest
```

```python
class TestSuite:          # Grandparent
    def info(self):
        print("Test Suite v2.0")

class BaseTest(TestSuite):  # Parent
    def setup(self):
        print("Setting up browser")

class UITest(BaseTest):     # Child
    def run(self):
        self.info()    # From grandparent
        self.setup()   # From parent
        print("Running UI test")

test = UITest()
test.run()
```

**Real-world use:** Framework hierarchy — `TestSuite` → `BaseTest` → `LoginTest` / `SignupTest`.

---

## 4. Hierarchical Inheritance

**One parent → Multiple children**

```mermaid
classDiagram
    class BaseTest {
        +setup()
    }
    class LoginTest {
        +run()
    }
    class SignupTest {
        +run()
    }
    BaseTest <|-- LoginTest
    BaseTest <|-- SignupTest
```

```python
class BaseTest:
    def setup(self):
        print("Setup from BaseTest")

class LoginTest(BaseTest):
    def run(self):
        print("Running Login Test")

class SignupTest(BaseTest):
    def run(self):
        print("Running Signup Test")

LoginTest().setup()   # Shared from BaseTest
LoginTest().run()
SignupTest().setup()  # Shared from BaseTest
SignupTest().run()
```

**Real-world use:** A single `BaseTest` class providing `setup()`/`teardown()` to ALL test classes.

---

## 5. Hybrid Inheritance

**Mix of multiple + multilevel**

```mermaid
classDiagram
    class Base {
        +base_method()
    }
    class A {
        +a_method()
    }
    class B {
        +b_method()
    }
    class C {
        +c_method()
    }
    Base <|-- A
    Base <|-- B
    A <|-- C
    B <|-- C
```

```python
class Base:
    def base_method(self):
        print("Base Method")

class A(Base):       # Single: A inherits Base
    def a_method(self):
        print("A Method")

class B(Base):       # Single: B inherits Base
    def b_method(self):
        print("B Method")

class C(A, B):       # Multiple: C inherits A AND B
    def c_method(self):
        print("C method")

obj = C()
obj.base_method()  # From Base (via A or B)
obj.a_method()     # From A
obj.b_method()     # From B
obj.c_method()     # Own
```

**Real-world use:** Complex framework where a test needs capabilities from multiple branches of the hierarchy.

---

## Real-World Example — Test Automation Framework

```python
class BaseTest:
    def __init__(self, browser):
        self.browser = browser

    def setup(self):
        print(f"Launching {self.browser}")

class LoginTest(BaseTest):    # Single Inheritance
    def run_test(self):
        self.setup()
        print("Running login test...")

class SignupTest(BaseTest):   # Hierarchical Inheritance
    def run_test(self):
        self.setup()
        print("Running signup test...")

t = LoginTest("Chrome")
t.run_test()

t1 = SignupTest("Firefox")
t1.run_test()
```

---

## Real-Time Use Cases of Inheritance 🎮

### 1. Test Automation (QA Framework) 🎯

This is exactly what your [149_REAL.py](149_REAL.py) does — the standard pattern used by QA engineers worldwide:

```python
class BaseTest:                          # 👨‍🏫 Parent — every test needs this
    def __init__(self, browser):
        self.browser = browser
    def setup(self):
        print(f"Launching {self.browser}")

class LoginTest(BaseTest):               # Child 1
    def run_test(self):
        self.setup()                     # Inherited!
        print("Running login test...")

class SignupTest(BaseTest):              # Child 2
    def run_test(self):
        self.setup()                     # Inherited!
        print("Running signup test...")

t = LoginTest("Chrome")    # ✅ Browser launch comes from BaseTest
t.run_test()
```

**Real-world reason:** In a QA company, you have 100 test classes. ALL of them need to launch a browser. Without inheritance, you'd copy the browser code 100 times! With inheritance, it's written once in `BaseTest`.

### 2. Video Games 🎮

```python
class Enemy:                    # Parent — all enemies share this
    def __init__(self, hp):
        self.hp = hp
    def take_damage(self, dmg):
        self.hp -= dmg
        print(f"Enemy HP: {self.hp}")

class Zombie(Enemy):            # Child 1
    def bite(self):
        print("🧟 Zombie bites!")

class Ghost(Enemy):             # Child 2
    def float(self):
        print("👻 Ghost floats through walls!")
```

All enemies take damage the same way — written once!

### 3. Online Shopping (Amazon-style) 🛒

```python
class Product:                  # Parent
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def show_price(self):
        print(f"{self.name}: ₹{self.price}")

class Electronics(Product):     # Child 1
    def warranty(self):
        print(f"{self.name} has 1-year warranty")

class Clothing(Product):        # Child 2
    def size(self):
        print(f"{self.name} comes in S/M/L")
```

### 4. Animals in a Zoo 🦁

```python
class Animal:                   # Parent
    def eat(self):
        print("Eating food 🍖")
    def sleep(self):
        print("Sleeping 😴")

class Dog(Animal):              # Child
    def bark(self):
        print("Woof! 🐶")

class Cat(Animal):              # Child
    def meow(self):
        print("Meow! 🐱")
```

### 5. Payment Systems 💳

```python
class Payment:                  # Parent — all payments share this
    def __init__(self, amount):
        self.amount = amount
    def process(self):
        print(f"Processing ₹{self.amount}...")

class CreditCard(Payment):      # Child 1
    def process(self):
        super().process()
        print("  via Credit Card 💳")

class UPI(Payment):             # Child 2
    def process(self):
        super().process()
        print("  via UPI 📱")
```

### 6. Employee Management (HR System) 🏢

```python
class Employee:                 # Parent
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    def work(self):
        print(f"{self.name} is working")

class Developer(Employee):      # Child 1
    def code(self):
        print(f"{self.name} is writing code 💻")

class Manager(Employee):        # Child 2
    def review(self):
        print(f"{self.name} is reviewing the team 📋")
```

---

## Quick Reference

```text
Inheritance Type    Syntax                          Use Case
─────────────────  ──────────────────────────────  ─────────────────────────
Single              class Child(Parent):            One specific test type
Multiple            class Child(P1, P2):            Combining API + DB
Multilevel          class C(B): class B(A):         Framework hierarchy
Hierarchical        class C1(P): class C2(P):       Shared base for all tests
Hybrid              class C(A, B): class A(P):      Complex framework needs
```

## Key Takeaways

1. **`super()`** — Call the parent's `__init__` from the child: `super().__init__()`
2. **`isinstance(obj, Class)`** — Check if an object is an instance of a class
3. **`issubclass(Child, Parent)`** — Check inheritance relationship
4. **`ClassName.__mro__`** — See the Method Resolution Order (which class's method runs first)
5. **Python follows MRO (C3 linearization)** — Left-to-right, depth-first, then parent