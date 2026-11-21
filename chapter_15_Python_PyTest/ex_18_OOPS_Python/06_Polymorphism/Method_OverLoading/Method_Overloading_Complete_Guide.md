# Method Overloading in Python — Complete Guide

## What is Method Overloading?

**Method overloading** is when a class has **multiple methods with the same name** but **different parameters** (different count or types). The idea is: *one method name, many behaviors* — the correct method is chosen based on the arguments passed.

**Real-world analogy — a person named "call" 📞:**

Think of ordering food at a restaurant:

- `order("Pizza")` — one item
- `order("Pizza", "Coke")` — two items
- `order("Pizza", "Coke", 2)` — two items, quantity 2

Same method name `order()`, but behaves differently based on what you pass! That's overloading.

```text
        ┌─────────────────────────────┐
        │        Person Class          │
        │                             │
        │  order(pizza)               │  ← Same name,
        │  order(pizza, coke)         │    different
        │  order(pizza, coke, qty)    │    parameters
        └─────────────────────────────┘
```

---

## Simple Example

### In Java/C++ (true overloading):

```java
class MathClass {
    int add(int a, int b) {           // 2 parameters
        return a + b;
    }
    int add(int a, int b, int c) {    // 3 parameters — same name!
        return a + b + c;
    }
}

MathClass m = new MathClass();
m.add(10, 20);        // → 30  (picks 2-param version)
m.add(10, 20, 30);    // → 60  (picks 3-param version)
```

The compiler **automatically picks** the right method by counting arguments.

### In Python (attempt — ❌ does NOT work like Java):

```python
class MathClass:
    def add(self, a, b):              # First definition
        return a + b

    def add(self, a, b, c):           # Second definition — OVERRIDES!
        return a - b - c

m = MathClass()
print(m.add(10, 20))     # ❌ TypeError: add() missing 1 required positional argument: 'c'
print(m.add(10, 20, 30)) # → -40  (only the SECOND method exists!)
```

📄 This is exactly what [150_MLoading.py](150_MLoading.py) shows — the first `add` is **completely erased**.

> ⚠️ **Why?** In Python, a class body is executed top-to-bottom. The second `add` **rebinds the name** `add` to the new function. The first one is gone forever.

---

## Is Python Supports Method Overloading? 🤔

### Short answer: **NO true overloading** — but Python gives you ways to simulate it!

| Feature                         | Java         | Python                                                        |
| ------------------------------- | ------------ | ------------------------------------------------------------- |
| Multiple methods, same name     | ✅ All kept  | ❌ Only last one survives                                     |
| Compiler picks by signature     | ✅ Automatic | ❌ Not possible                                               |
| Default parameters              | ⚠️ Limited | ✅ ✅ **Yes — primary technique**                      |
| `*args` / `**kwargs`        | ❌           | ✅ ✅ **Yes — flexible approach**                      |
| **Then how do we do it?** | Built-in     | **Simulated via defaults, `*args`, or type checking** |

---

## The 4 Ways Python Simulates Method Overloading

### Method 1: Default Parameters (Most Common ✅)

```python
class MathClass:
    def add(self, a, b, c=0):     # c is OPTIONAL
        return a + b + c

m = MathClass()
print(m.add(10, 20))       # → 30   (c defaults to 0)
print(m.add(10, 20, 30))   # → 60   (c = 30)
print(m.add(3.14, 5.67))   # → 8.81 (floats work too!)
```

📄 See [152_REAL_MLoading.py](152_REAL_MLoading.py) — this is the pattern it demonstrates.

When you call `add(10, 20)`, Python fills `c` with its default. It's like having "two methods" — one that takes 2 args, one that takes 3.

---

### Method 2: `*args` — Any Number of Arguments

```python
class MathClass:
    def add(self, *args):         # *args = tuple of all arguments
        total = 0
        for num in args:
            total += num
        return total

m = MathClass()
print(m.add(10, 20))                 # → 30
print(m.add(10, 20, 30, 40))         # → 100
print(m.add(1, 2, 3, 4, 5, 6, 7))    # → 28 — ANY count works!
```

**Real-world use:** A `sum()` utility that handles any number of numbers — like Python's built-in `sum()`.

---

### Method 3: Type Checking with `isinstance()` (Different Types)

```python
class Calculator:
    def calculate(self, a, b=None):
        if b is None:                       # One argument — square it!
            return a * a
        elif isinstance(a, str) or isinstance(b, str):  # Strings — concat!
            return str(a) + str(b)
        else:                               # Two numbers — multiply!
            return a * b

calc = Calculator()
print(calc.calculate(5))        # → 25          (square)
print(calc.calculate(5, 3))     # → 15          (multiply)
print(calc.calculate("Hello", " World"))  # → "Hello World" (concat)
```

**Real-world use:** `print()` itself does this — it accepts any number of any type of arguments!

---

### Method 4: `None` Check — Optional Behaviors

```python
class Browser:
    def make_http_request(self, url, auth=None):    # auth is optional
        if auth:
            print(f"Making request to {url} with auth: {auth}")
        else:
            print(f"Making request to {url} without auth")

b = Browser()
b.make_http_request("google.com")          # → without auth
b.make_http_request("google.com", "admin") # → with auth
```

📄 See [153_IQ.py](153_IQ.py) — this is the exact real-world example (HTTP request with optional auth)!

```text
make_http_request("google.com")            → without auth
make_http_request("google.com", "admin")   → with auth
       Same method name — 2 behaviors!
```

---

## Real-World Examples 🌍

### 1. Employee Salary Calculation (HR System)

```python
class Employee:
    def calculate_salary(self, base, bonus=0, tax=0.10):
        gross = base + bonus
        net = gross - (gross * tax)
        return net

emp = Employee()
print(emp.calculate_salary(50000))                  # Simplest: only base
print(emp.calculate_salary(50000, bonus=10000))     # With bonus
print(emp.calculate_salary(50000, 10000, 0.20))     # Full breakdown
```

**One method, many salary scenarios** — HR doesn't need 3 different methods!

---

### 2. Payment Processing (E-Commerce)

```python
class Payment:
    def process(self, amount, currency="INR", method="card"):
        if method == "card":
            print(f"Processing ₹{amount} {currency} via Card 💳")
        elif method == "upi":
            print(f"Processing ₹{amount} {currency} via UPI 📱")
        else:
            print(f"Processing ₹{amount} {currency} via {method}")

p = Payment()
p.process(1000)                          # Default card payment
p.process(2000, "USD")                   # Different currency
p.process(500, "INR", "upi")             # Different method
```

---

### 3. Test Automation — Web Element Actions (QA)

```python
class WebElement:
    def click(self, timeout=10, retry=False):
        if retry:
            print(f"Clicking with retry, timeout {timeout}s")
        else:
            print(f"Clicking once, timeout {timeout}s")

    def send_keys(self, text, clear_before=True, press_enter=False):
        if clear_before:
            print(f"Clearing field...")
        print(f"Typing: {text}")
        if press_enter:
            print("Pressing Enter ⏎")

element = WebElement()
element.click()                         # Default behavior
element.click(30, retry=True)           # Retry on flaky element
element.send_keys("admin@test.com")     # Basic
element.send_keys("admin@test.com", press_enter=True)  # Submit!
```

**Why QA loves this:** One method handles normal + edge-case behavior — no need to write 4 different `click` methods.

---

### 4. Sending Messages (Notification System)

```python
class Notification:
    def send(self, message, recipient=None, channel="email"):
        if recipient is None:                    # Broadcast to all
            print(f"[{channel}] Broadcasting: {message}")
        elif channel == "sms":
            print(f"[SMS] {recipient}: {message}")
        elif channel == "whatsapp":
            print(f"[WhatsApp] {recipient}: {message}")
        else:
            print(f"[Email] {recipient}: {message}")

n = Notification()
n.send("Server down!")                        # Broadcast
n.send("Deploy complete", "team@company.com")  # Email
n.send("OTP 1234", "+919876543210", "sms")     # SMS
```

---

## 🧪 The "Pitfall" Example — Why Order Matters

```python
class MathClass:
    def add(self, a, b):          # ❌ Will be OVERWRITTEN
        return a + b

    def add(self, a, b, c=10):    # ✅ This is the ONLY one that survives
        return a + b + c

m = MathClass()
print(m.add(10, 20))        # → 40  (c = default 10, NOT 2-arg method!)
print(m.add(10, 20, 30))    # → 60
```

📄 This is exactly your [151_MLoading_Default_Param.py](151_MLoading_Default_Param.py) and [152_REAL_MLoading.py](152_REAL_MLoading.py). The first `add` is never called — **only the last definition exists**.

---

## Python vs Java — Comparison Table

| Aspect                             | Java                   | Python                                |
| ---------------------------------- | ---------------------- | ------------------------------------- |
| Same name, multiple versions       | ✅ Keeps all           | ❌ Last one wins                      |
| Overloading technique              | Write multiple methods | Default params / `*args`            |
| `add(10, 20)` with both versions | Picks 2-param version  | TypeError (if last needs 3)           |
| Compiled or runtime decision       | **Compile-time** | **Runtime** (just one function) |
| Cleanest way to do "overload"      | Native                 | `def add(a, b, c=0)`                |

---

## Quick Reference Cheat-Sheet

```text
Need to support:                    Technique                Example
─────────────────────────────────  ──────────────────────  ───────────────────
2 or 3 arguments                   Default parameter       def add(a, b, c=0)
Any number of arguments            *args                   def add(*args)
Different data types               isinstance() check      def process(a, b=None)
Optional behavior flag             None check              def req(url, auth=None)

REMEMBER:
  ❌ Duplicate method names = last one wins (no true overloading)
  ✅ Default parameters = the Pythonic "overloading"
  ✅ *args = unlimited flexibility
```

---

## Key Takeaways

1. **True method overloading is NOT supported in Python** — only the last method with a given name survives (see [150_MLoading.py](150_MLoading.py))
2. **Default parameters** are the #1 Python way to get overloading behavior — `def add(self, a, b, c=0)`
3. **`*args` / `**kwargs`** give unlimited flexibility — any number of arguments
4. **`isinstance()` + `None` checks** let one method handle different types/behaviors
5. **Same goal, different approach:** Java overloading = many methods; Python overloading = one flexible method
6. Your repo files show the full journey: [150_MLoading.py](150_MLoading.py) (broken attempt) → [151_MLoading_Default_Param.py](151_MLoading_Default_Param.py) & [152_REAL_MLoading.py](152_REAL_MLoading.py) (default params ✅) → [153_IQ.py](153_IQ.py) (real-world optional auth ✅)
