# Encapsulation in Python — Complete Guide

## What is Encapsulation?

**Encapsulation** is the OOP concept of **bundling data (variables) and methods (functions) together inside a class**, and **restricting direct access** to some of that data from outside.

Think of it as a **capsule** (like a medicine capsule 💊) — the medicine inside is protected by the outer shell. You can only take it through the shell, not reach in and grab the powder directly.

```text
┌─────────────────────────────┐
│         CLASS (Capsule)      │
│  ┌───────────────────────┐   │
│  │  Private data (secret) │   │  ← Protected inside
│  │  __password            │   │
│  └───────────────────────┘   │
│  ┌───────────────────────┐   │
│  │  Public methods (door) │   │  ← Controlled access
│  │  login()               │   │
│  └───────────────────────┘   │
└─────────────────────────────┘
```

---

## ELI5 — Encapsulation for a 5th Grader 🧒

**Imagine your piggy bank 🐷.** You put money inside it. Can anyone just reach in and grab the coins? **No!** They need to either:
1. Use the **coin slot** to put money in (deposit)
2. Use the **plug at the bottom** to take money out (withdraw)

The piggy bank **hides** the money (data) and only gives you **controlled ways** to interact with it (methods). That's encapsulation!

**Another example — your school locker 🔒:**
- Your diary is inside the locker (private data)
- Only YOU have the key (private access)
- Your friends can see the locker from outside (public)
- If someone wants your notes, YOU decide whether to open it (controlled access)

**In Python terms:**
```python
class PiggyBank:
    def __init__(self):
        self.__money = 0          # 🔒 PRIVATE — hidden inside

    def deposit(self, amount):    # 🚪 Public door — controlled access
        self.__money += amount
        print(f"Deposited ₹{amount}")

    def check_balance(self):       # 🚪 Public door — read only
        print(f"Balance: ₹{self.__money}")

piggy = PiggyBank()
piggy.deposit(100)
piggy.check_balance()
# piggy.__money  ← ❌ ERROR! Can't touch the private money directly!
```

**One sentence:** *Encapsulation = hide the data, expose only safe doors (methods) to use it.* 🚪

---

## Why Do We Need Encapsulation?

| Problem without it | Solution with it |
|---|---|
| Anyone can change your password directly | Only `login()` method can validate it |
| Data can be set to invalid values (`balance = -500`) | Methods validate before changing |
| Code breaks when internal details change | Outside code only uses stable methods |
| Sensitive data (API keys, passwords) exposed | Private attributes hide them |

**Real-world example:** Your bank app shows your balance, but you can't directly change the balance in the bank's database. You go through `deposit()` / `withdraw()` methods — the bank controls the access!

---

## The 3 Access Levels in Python

Python uses **naming conventions** (not enforced keywords like Java) to signal access levels:

| Level | Syntax | Meaning | Access from outside |
|-------|--------|---------|---------------------|
| **Public** | `self.var` | Open to everyone | ✅ Yes |
| **Protected** | `self._var` | Internal use (convention) | ⚠️ Yes, but "don't" |
| **Private** | `self.__var` | Hidden (name mangling) | ❌ No |

---

## Where Encapsulation Was Implemented in This Repo 📂

### 1. [135_Normal_Class.py](135_Normal_Class.py) — No Encapsulation (Baseline)

```python
class Car:
    def __init__(self, o_name, o_make, o_model):
        self.name = o_name      # All PUBLIC
        self.make = o_make
        self.model = o_model
```

**What's wrong?** Everything is public. Anyone can change `car.name = "Hacked"` — no protection at all.

---

### 2. [136_WEcap.py](136_WEcap.py) — Hardcoded Credentials (Still No Protection)

```python
class VWOLoginPage:
    def __init__(self, email_arg, password_arg):
        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        if self.email == "student@example.com" and self.password == "demo123":
            print("Login is Allowed")
```

**What's wrong?** Credentials are hardcoded in the code AND stored as public attributes. Anyone can read `obj.password`.

---

### 3. [137_WEcap_Secure.py](137_WEcap_Secure.py) — Credentials in `.env` (Better, but still public)

```python
from dotenv import load_dotenv
import os

class VWOLoginPage:
    def __init__(self, email_arg, password_arg):
        self.email = email_arg
        self.password = password_arg

    def login_confirm(self):
        load_dotenv()
        if self.email == os.getenv("USERNAME") and self.password == os.getenv("PASSWORD"):
            print("Allowed, Login success")
```

**Improvement:** Credentials moved to `.env` file (not in code). **Still weak:** `self.password` is public — anyone can print `obj.password` (the last line does exactly that!).

---

### 4. [138_Ecap_Better.py](138_Ecap_Better.py) — Introducing All 3 Levels

```python
class Car:
    def __init__(self):
        self.public_shankar = "shankar"      # PUBLIC
        self._protected_baby = "demo123"     # PROTECTED (single _)
        self.__private_baby = "demo123"      # PRIVATE (double __)
```

**This is the turning point!** Now you can see all three access levels declared side by side.

---

### 5. [139_AccessModifiers_Detailed.py](139_AccessModifiers_Detailed.py) — Full Walkthrough

This file demonstrates:
- Public — accessible & modifiable from outside
- Protected — accessible but discouraged
- Private — `AttributeError` when accessed directly
- **Name mangling**: `__pin` becomes `_BankAccountPrivate__pin`
- Inheritance behavior — child can't see parent's private
- Real-world `VWOLoginPage` with all three levels

```python
class VWOLoginPage:
    _BASE_URL = "https://app.vwo.com"        # Protected constant

    def __init__(self, email, password):
        self.email = email                    # Public
        self.__password = password            # PRIVATE — hidden!
        self._login_attempts = 0             # Protected

    def login(self):
        self._login_attempts += 1
        if self.__password == "secret@123":   # Used INSIDE only
            return True
```

---

### 6. [140_Ecap.py](140_Ecap.py) — Real-World Bank (Best Example 🏆)

```python
class Bank:
    def __init__(self, account_number, balance):
        self.balance = balance                # PUBLIC — safe to show
        self.__acccount_number = account_number  # PRIVATE — hidden!

    def check_balance(self):
        print(self.balance)

    def deposit(self, amount):
        self.balance = self.balance + amount

    def show_me_account_number(self, is_auth):   # 🔐 CONTROLLED ACCESS!
        if is_auth == True:
            print(self.__acccount_number)        # Only if authorized
        else:
            print("Not Allowed")

icici = Bank(987654321, 100)
icici.deposit(1000)
icici.check_balance()
icici.show_me_account_number(True)   # ✅ Authorized → shows number
icici.show_me_account_number(False)  # ❌ Not authorized → "Not Allowed"
```

**Why this is the BEST encapsulation example:**
- ✅ `balance` is public — safe to show anyone
- ✅ `__account_number` is private — hidden from the world
- ✅ `show_me_account_number(is_auth)` is the **controlled door** — even if someone calls it, they need authorization!
- ✅ This mirrors real banking: you can't just read someone's account number without permission

---

### 7. [141_REAL.py](141_REAL.py) — Family-Themed Example

```python
class Home:
    def __init__(self):
        self.public_var = "father"        # Public — everyone knows
        self._protected_var = "brother"   # Protected — family only
        self.__private_var = "baby"       # Private — hidden

        def mom(self):
            print(self.__private_var)     # Mom can see the baby
            self.__wife()                 # Mom can call private method

        def __wife(self):                 # Private method
            print("Private wife")

object_ref = Home()
# object_ref.__wife()      ← ❌ AttributeError (commented out)
# object_ref.__private_var ← ❌ AttributeError
```

**The family analogy:** The "baby" (private) is only known inside the home. Outsiders can't see it.

---

### 8. [142_PPP.py](142_PPP.py) — Test Framework Example

```python
class TestExample:
    def __init__(self):
        self.driver = "Chrome"            # PUBLIC
        self._config = "STAG"             # PROTECTED
        self.__api__key = "ABC12345"      # PRIVATE (note: __api__key)

    def show(self):
        print(f"Driver: {self.driver}")
        print(f"Config: {self._config}")
        print(f"API key: {self.__api__key}")

    def __private_method1(self):          # PRIVATE methods
        pass
    def __private_method2(self):
        pass

    def work(self):                       # Public method calls private ones
        self.__private_method1()
        self.__private_method2()

obj_ref = TestExample()
obj_ref.show()
obj_ref.work()
print(obj_ref.driver)      # ✅ Public — works
print(obj_ref._config)     # ⚠️ Protected — works but don't
# print(obj_ref.__api__key)  ← ❌ AttributeError (commented out)
```

**QA relevance:** In test frameworks, the API key is private — tests use it through methods, never directly.

---

## 🔑 The Key Techniques of Encapsulation

### 1. Name Mangling (How Python "hides" private)

When you write `self.__password`, Python internally renames it to `self._ClassName__password`:

```python
class Bank:
    def __init__(self):
        self.__pin = "1234"   # becomes _Bank__pin

b = Bank()
# print(b.__pin)              # ❌ AttributeError
print(b._Bank__pin)           # ⚠️ Works via mangled name (don't do this!)
```

### 2. Getter & Setter Methods (Controlled Access)

The professional way to expose private data:

```python
class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number
        self.__balance = balance

    # GETTER — read with validation
    def get_balance(self):
        return self.__balance

    # SETTER — write with validation
    def set_balance(self, amount):
        if amount < 0:
            print("❌ Balance can't be negative!")
        else:
            self.__balance = amount

acc = BankAccount("123456", 1000)
print(acc.get_balance())     # ✅ 1000
acc.set_balance(-500)        # ❌ "Balance can't be negative!"
acc.set_balance(2000)         # ✅ Works
```

### 3. The `@property` Decorator (Pythonic Getter/Setter)

The modern, clean way:

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):                    # Getter — read like an attribute
        return self.__balance

    @balance.setter
    def balance(self, amount):            # Setter — with validation
        if amount < 0:
            raise ValueError("Balance can't be negative!")
        self.__balance = amount

acc = BankAccount(1000)
print(acc.balance)      # ✅ 1000 (reads like public!)
acc.balance = 2500      # ✅ Validated set
# acc.balance = -100    # ❌ ValueError raised
```

---

## Encapsulation vs Inheritance — How They Work Together

| Concept | What it does | Example |
|---------|--------------|---------|
| **Encapsulation** | Hides data, controls access | `__password` hidden, `login()` validates |
| **Inheritance** | Reuses code across classes | `LoginTest(BaseTest)` gets `setup()` |

**Together in a real framework:**
```python
class BaseTest:                          # Encapsulation: hides browser setup
    def __init__(self, browser):
        self.__browser = browser         # Private

    def setup(self):                     # Public door
        print(f"Launching {self.__browser}")

class LoginTest(BaseTest):               # Inheritance: reuses BaseTest
    def run(self):
        self.setup()                     # Uses the public door
```

---

## Quick Reference

```text
Access Level    Syntax       Outside Access    Child Access    Use For
─────────────   ──────────   ───────────────   ─────────────   ─────────────
Public          self.var     ✅ Yes            ✅ Yes          Safe data
Protected       self._var    ⚠️ Yes (don't)   ✅ Yes          Internal helpers
Private         self.__var   ❌ No             ❌ No           Secrets, sensitive

Key techniques:
  Getter/Setter  →  get_balance() / set_balance()
  @property      →  Clean Pythonic access with validation
  Name mangling  →  __var becomes _ClassName__var
```

## Key Takeaways

1. **Encapsulation = data hiding + controlled access** — like a piggy bank 🐷
2. **Public** (`var`) — open to all
3. **Protected** (`_var`) — internal use, convention only
4. **Private** (`__var`) — hidden via name mangling
5. **Getters/Setters** — the professional way to expose private data safely
6. **`@property`** — the Pythonic way to do getters/setters
7. **Real-world use:** Bank accounts, login systems, API keys, test frameworks — anywhere you must protect sensitive data
8. **Your repo progression:** `135` (no protection) → `136-137` (creds, still public) → `138-139` (all 3 levels) → `140` (best: bank with auth-gated access) → `141-142` (family & test framework)
