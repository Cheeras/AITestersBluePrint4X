# Abstraction in Python — Complete Guide

## What is Abstraction?

**Abstraction** is the OOP concept of **hiding the complex implementation details** and **showing only the essential features** to the user.

Think of it like driving a car 🚗:
- You press the **accelerator** → car moves (that's all you need to know!)
- You DON'T need to know about fuel injection, pistons, gears, or engine ECM — those details are **hidden**

```text
┌─────────────────────────────────────────────┐
│              USER (Driver)                   │
│   sees ONLY: steering, brake, accelerator    │
└──────────────────┬──────────────────────────┘
                   │ abstraction (hiding)
┌──────────────────▼──────────────────────────┐
│          INTERNAL DETAILS (Hidden)           │
│   Engine, GearBox, Pistons, Fuel Lines...    │
└─────────────────────────────────────────────┘
```

---

## ELI5 — Abstraction for a 5th Grader 🧒

**Imagine a TV remote 📺:**
- It has buttons: POWER, VOLUME, CHANNEL
- You press them and things happen — easy!
- Do you know what's INSIDE the remote? The circuit board? The infrared LED? **No!**
- But you don't NEED to — the remote **hides the complicated stuff** and shows you only the simple buttons.

**In Python terms:**

```python
class TVRemote:
    def press_power(self):
        # Inside: complex code to send IR signals
        print("TV turning ON...")     # User only sees this!

    def volume_up(self):
        # Inside: complex signal logic
        print("Volume 🔊 up!")

remote = TVRemote()
remote.press_power()    # Simple! User doesn't see the internals
```

**One sentence:** *Abstraction = hide the complicated details, show only what the user needs.* 🎛️

---

## How Python Does Abstraction — `ABC` and `abstractmethod` 🔑

Python implements abstraction using the built-in `abc` module:

```python
from abc import ABC, abstractmethod   # ← THE key line!
```

| Imported item | What it does |
|---------------|--------------|
| `ABC` | **Abstract Base Class** — a blueprint class you CANNOT create objects from |
| `abstractmethod` | A **decorator** that marks a method as "children MUST implement this" |

### The Three Rules of Python Abstraction:

1. **Rule 1:** An `ABC` class **cannot be instantiated** → `Animal()` gives `TypeError`
2. **Rule 2:** A method marked `@abstractmethod` has **no implementation** (just `pass`)
3. **Rule 3:** Every child class **MUST implement** all abstract methods — or the child ALSO can't be instantiated

```python
from abc import ABC, abstractmethod

class Animal(ABC):                 # Rule 1: blueprint only
    @abstractmethod
    def sound(self):               # Rule 2: no code, just a rule
        pass

# ❌ Rule 1 in action:
# a = Animal()  → TypeError: Can't instantiate abstract class Animal

class Dog(Animal):                 # Rule 3: MUST implement sound()
    def sound(self):               # ✅ Implemented!
        print("Bark!")

dog = Dog("PP")
dog.sound()   # → Bark!
```

📄 This is exactly [157_Abs.py](157_Abs.py)!

---

## Simple Example — The Loan Contract 💰

```python
from abc import ABC, abstractmethod

class Father(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def loan(self):                # 📋 Contract: every child MUST give loan
        pass

class Shankar(Father):             # ✅ Implements the contract
    def loan(self):
        print(f"{self.name} is giving the 50K loan")

sc = Shankar("Shankar Cheerala")
sc.loan()   # → Shankar Cheerala is giving the 50K loan
```

📄 This is exactly [158_Abs_Part1.py](158_Abs_Part1.py)!

**Why a contract?** The `Father` says: *"Anyone who is my child MUST handle loans."* Every child class is **forced** to implement `loan()` — no escaping!

---

## ⭐ Key Insight — ABC Classes CAN Have Normal Methods Too!

Many beginners think abstract classes = ONLY abstract methods. **Wrong!** An ABC can have:
- ✅ Abstract methods (children MUST implement)
- ✅ Normal methods (children inherit automatically — shared logic!)
- ✅ `__init__` constructors (children inherit initialization!)

```python
from abc import ABC, abstractmethod

class BrowserManager(ABC):
    @abstractmethod
    def start(self):               # 📋 MUST implement (each browser differs)
        pass

    def stop(self):                # ✅ Normal method — SHARED logic
        print("Stop command, common")   # Same for ALL browsers

class ChromeBrowser(BrowserManager):
    def start(self):               # ✅ Required implementation
        # t = ChromeDriver()  ← real driver code here
        print("We are starting the chrome")

tc = ChromeBrowser()
tc.start()   # → We are starting the chrome  (child's own)
tc.stop()    # → Stop command, common       (inherited from ABC!)
```

📄 This is exactly [159_REAL_Example.py](159_REAL_Example.py)!

---

## 📖 Key Idea #2 — Abstract classes can inherit from multiple abstract classes!

```python
from abc import ABC, abstractmethod

class GearBox(ABC):
    @abstractmethod
    def setGear(self):             # Contract 1
        pass

class Engine(ABC):
    @abstractmethod
    def start(self):               # Contract 2
        pass

    @abstractmethod
    def stop(self):                # Contract 3
        pass

class Car(Engine, GearBox):        # 📋 Must implement ALL 3!
    def start(self):
        print("starting")

    def stop(self):
        print("Stop")

    def setGear(self):
        print("Gearbox is ready")

    def drive(self):               # ✅ New method using all contracts
        self.start()
        self.setGear()
        self.stop()

tesla = Car()
tesla.drive()
# → starting
# → Gearbox is ready
# → Stop
```

📄 This is exactly [160_Hide_Abs.py](160_Hide_Abs.py)!

**The insight:** `Car` inherits from **TWO abstract contracts** (`Engine` + `GearBox`) and must satisfy BOTH. This is abstraction + multiple inheritance working together!

---

## 📖 Key Idea #3 — An abstract class can inherit from another abstract class (staying abstract!)

```python
from abc import ABC, abstractmethod

class ExcelReader(ABC):
    @abstractmethod
    def readFromExcel(self):       # Contract 1
        pass

class Browser(ExcelReader):        # Still abstract! Doesn't implement readFromExcel
    @abstractmethod
    def startBrowser(self):        # Adds MORE contracts
        pass

    @abstractmethod
    def stopBrowser(self):
        pass

# ❌ Browser() → TypeError: Can't instantiate abstract class Browser
# A FINAL concrete class must implement ALL 3 methods!
```

📄 This is exactly [161.py](161.py)!

**The chain of contracts:** `ExcelReader` says "implement `readFromExcel`" → `Browser` adds "AND `startBrowser` AND `stopBrowser`" → the final child must do **all three**!

```text
ExcelReader (1 contract)  →  Browser (3 contracts)  →  ???? (must do all 3)
```

---

## 🎭 Abstraction vs Encapsulation — Don't Confuse Them!

These are the two MOST confused concepts. Here's the difference:

| Aspect | **Abstraction** | **Encapsulation** |
|--------|-----------------|-------------------|
| **What** | Hiding **implementation details** | Hiding **data** and controlling access |
| **Focus** | WHAT the object does (interface) | HOW the data is protected (security) |
| **Tools** | `ABC`, `abstractmethod` | `_protected`, `__private`, getters/setters |
| **Question it answers** | "What can this object DO?" | "What can outsiders SEE/CHANGE?" |
| **Analogy** | TV remote (simple buttons, hidden circuits) | Piggy bank (money locked inside) |

```python
# ENCAPSULATION (file 140): hiding DATA
class Bank:
    def __init__(self, acct_no, balance):
        self.__acct_no = acct_no            # 🔒 Private data
    def show_me_account_number(self, is_auth):   # Controlled door
        ...

# ABSTRACTION (file 157): hiding IMPLEMENTATION
class Animal(ABC):
    @abstractmethod
    def sound(self): pass                    # 📋 Contract — no code
class Dog(Animal):
    def sound(self): print("Bark!")          # Details hidden from user
```

**Simple rule:**
- **Encapsulation** → "You can't touch my private data directly" 🔒
- **Abstraction** → "You don't need to know HOW it works, just WHAT it does" 🎛️

---

## Real-World Examples 🌍

### 1. Test Automation — Page Object Model (THE QA classic 🎯)

```python
from abc import ABC, abstractmethod

class BasePage(ABC):                       # Blueprint for ALL pages
    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def load(self):                        # Every page MUST load
        pass

    @abstractmethod
    def verify_page(self):                 # Every page MUST verify itself
        pass

class LoginPage(BasePage):
    def load(self):                        # ✅ Implemented
        print("Navigating to /login...")

    def verify_page(self):                 # ✅ Implemented
        print("Verifying username field, password field, login button...")

class HomePage(BasePage):
    def load(self):                        # ✅ Implemented
        print("Navigating to /home...")

    def verify_page(self):                 # ✅ Implemented
        print("Verifying dashboard widgets...")

# 🎯 One interface, many implementations!
login = LoginPage("chromedriver")
login.load()           # → Navigating to /login...
login.verify_page()    # → Verifying login elements...

home = HomePage("chromedriver")
home.load()            # → Navigating to /home...
home.verify_page()     # → Verifying dashboard widgets...
```

**Why QA teams LOVE this:** New developers CANNOT forget to implement `load()` and `verify_page()` — the `ABC` contract FORCES them! No more pages missing verification methods! 🔒

---

### 2. Payment Gateways (E-Commerce 💳)

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def authenticate(self):          # Every gateway MUST authenticate
        pass

    @abstractmethod
    def charge(self, amount):        # Every gateway MUST charge
        pass

    @abstractmethod
    def refund(self, amount):        # Every gateway MUST refund
        pass

class Razorpay(PaymentGateway):
    def authenticate(self):
        print("Razorpay: API key verified")
    def charge(self, amount):
        print(f"Razorpay: Charged ₹{amount}")
    def refund(self, amount):
        print(f"Razorpay: Refunded ₹{amount}")

class PayPal(PaymentGateway):
    def authenticate(self):
        print("PayPal: OAuth token verified")
    def charge(self, amount):
        print(f"PayPal: Charged ₹{amount}")
    def refund(self, amount):
        print(f"PayPal: Refunded ₹{amount}")
```

**The beauty:** Your e-commerce code only talks to `PaymentGateway` — swap Razorpay ↔ PayPal with ZERO changes to the rest of the app! That's **design-by-contract**! 🏗️

---

### 3. Vehicle System (Real-world Car 🚗)

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start_engine(self): pass        # All vehicles start somehow

    @abstractmethod
    def drive(self): pass               # All vehicles move somehow

class PetrolCar(Vehicle):
    def start_engine(self):
        print("Igniting petrol engine with spark plug ⚡")
    def drive(self):
        print("Petrol car driving 🚗")

class ElectricCar(Vehicle):
    def start_engine(self):
        print("Powering electric motor from battery 🔋")
    def drive(self):
        print("Electric car driving silently 🚗💨")
```

**The user just calls `start_engine()` — they don't care if it's petrol or electric (hidden details!)**

---

## When to Use Abstraction? (Decision Guide)

| Situation | Use abstraction? |
|-----------|-----------------|
| Multiple classes share a behavior but implement it DIFFERENTLY | ✅ Yes — make it abstract |
| You want to FORCE children to implement methods | ✅ Yes — contract |
| All children share the SAME implementation | ❌ No — just a normal parent (inheritance) |
| You need to hide internal complexity from users | ✅ Yes — abstract or normal class hides details |
| Only ONE class will ever exist | ❌ No — abstraction adds no value |

---

## Quick Reference Cheat-Sheet

```text
IMPORTS:
  from abc import ABC, abstractmethod

RULES:
  ✅ ABC class = blueprint, CANNOT instantiate directly
  ✅ @abstractmethod = "children MUST implement this"
  ✅ Child MUST implement ALL abstract methods or stay abstract
  ✅ ABC can also have normal methods (shared logic) + __init__

ERROR YOU'LL SEE:
  TypeError: Can't instantiate abstract class X with abstract method Y
  → Means: Y wasn't implemented in child X. Fix by implementing it!

REMEMBER:
  Encapsulation = hide DATA (private variables)     🔒
  Abstraction   = hide IMPLEMENTATION (methods)     🎛️
```

## Key Takeaways

1. **Abstraction** = hiding complex details, showing only essential features (like driving a car)
2. **`from abc import ABC, abstractmethod`** → Python's abstraction toolkit (built-in module)
3. **`ABC`** = a class you can't create objects from — it's a blueprint/contract
4. **`@abstractmethod`** = a "MUST IMPLEMENT" stamp forcing children to write the method
5. **Big superpower:** Abstract classes can ALSO have normal methods + `__init__` — shared logic AND contracts together ([159](159_REAL_Example.py))
6. **Multi-contract:** A class can inherit from multiple abstract classes, implementing all their contracts ([160](160_Hide_Abs.py))
7. **Abstract chains:** An abstract class can inherit another abstract class, adding more contracts ([161](161.py))
8. **Your repo progression:** [157_Abs.py](157_Abs.py) (Animal contract) → [158_Abs_Part1.py](158_Abs_Part1.py) (Loan contract) → [159_REAL_Example.py](159_REAL_Example.py) (Browser + shared method) → [160_Hide_Abs.py](160_Hide_Abs.py) (Car, multi-contract) → [161.py](161.py) (abstract chain)
9. **Abstraction ≠ Encapsulation:** hiding *implementation* vs hiding *data*