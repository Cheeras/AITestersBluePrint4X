"""
============================================================
PUBLIC vs PROTECTED vs PRIVATE - Detailed Explanation
============================================================

Python Naming Convention:
    public      = self.var         (no underscore)
    protected   = self._var        (single underscore)
    private     = self.__var       (double underscore -> name mangling)

There are NO real "private" in Python - it's all conventions + name mangling.
"""

print("=" * 60)
print("1. PUBLIC - No underscore")
print("=" * 60)


class CarPublic:
    def __init__(self, name, model):
        self.name = name  # PUBLIC - accessible from anywhere
        self.model = model

    def display(self):
        print(f"  Inside class: {self.name}, {self.model}")


car = CarPublic("Suzuki", "2025")
car.display()
print(f"  Outside class (direct access): {car.name}, {car.model}")
car.name = "Honda"  # Can be modified from outside
print(f"  After modification outside: {car.name}")

print()
print("=" * 60)
print("2. PROTECTED - Single underscore _")
print("=" * 60)
print("  Convention: 'internal use' - accessible but 'please don't touch'")
print()


class BankAccountProtected:
    def __init__(self, holder, balance):
        self.holder = holder
        self._branch_code = "BR-007"  # PROTECTED - internal use only

    def show_details(self):
        print(f"  Holder: {self.holder}, Branch: {self._branch_code}")


acc = BankAccountProtected("Shankar", 5000)
acc.show_details()
# Still accessible (Python doesn't enforce), but convention says DON'T
print(f"  Accessed outside (not recommended): {acc._branch_code}")

print()
print("=" * 60)
print("3. PRIVATE - Double underscore __ (Name Mangling)")
print("=" * 60)
print("  Python renames __var to _ClassName__var internally")
print()


class BankAccountPrivate:
    def __init__(self, holder, balance):
        self.holder = holder
        self.__pin = "1234"  # PRIVATE - becomes _BankAccountPrivate__pin

    def show_pin(self):
        print(f"  PIN (inside class): {self.__pin}")

    def validate_pin(self, input_pin):
        return self.__pin == input_pin


account = BankAccountPrivate("Shankar", 5000)
account.show_pin()

# This will FAIL - __pin is name-mangled
try:
    print(account.__pin)
except AttributeError as e:
    print(f"  [FAIL] Direct access failed: {e}")

# But you CAN still access it via the mangled name (not recommended)
print(f"  [WARN] Mangled name access: {account._BankAccountPrivate__pin}")

print()
print("=" * 60)
print("4. REAL-WORLD EXAMPLE - VWOLoginPage with All Three")
print("=" * 60)


class VWOLoginPage:
    # Class-level protected (convention)
    _BASE_URL = "https://app.vwo.com"

    def __init__(self, email, password):
        # PUBLIC - anyone can read/write
        self.email = email

        # PRIVATE - should not be accessed outside
        self.__password = password

        # PROTECTED - for internal/subclass use
        self._login_attempts = 0

    # PUBLIC method - anyone can call
    def login(self):
        self._login_attempts += 1
        if self.__password == "secret@123":
            print(f"  [OK] Login success for {self.email}")
            return True
        else:
            print(f"  [FAIL] Login failed for {self.email}")
            return False

    # PROTECTED method - for internal/subclass use
    def _reset_attempts(self):
        self._login_attempts = 0
        print(f"  [RESET] Attempts reset to {self._login_attempts}")

    # PUBLIC getter for private data (controlled access)
    def get_login_attempts(self):
        return self._login_attempts


user = VWOLoginPage("shankar@test.com", "secret@123")
user.login()
user.login()
print(f"  Login attempts (via getter): {user.get_login_attempts()}")

# PUBLIC - fine
print(f"  Email (public): {user.email}")

# PROTECTED - accessible but not recommended
print(f"  Base URL (protected): {user._BASE_URL}")

# PRIVATE - will fail
try:
    print(user.__password)
except AttributeError as e:
    print(f"  [FAIL] Cannot access private password: {e}")

print()
print("=" * 60)
print("5. INHERITANCE - How Protected & Private Behave")
print("=" * 60)


class Parent:
    def __init__(self):
        self.public = "I am public"
        self._protected = "I am protected"
        self.__private = "I am private"

    def show(self):
        print(f"    public={self.public}, _protected={self._protected}", end="")
        print(f", __private={self.__private}")


class Child(Parent):
    def access(self):
        print(f"    [OK] public (child): {self.public}")
        print(f"    [OK] _protected (child): {self._protected}")
        # __private is name-mangled to _Parent__private, so child can't see it
        try:
            print(f"    __private (child): {self.__private}")
        except AttributeError as e:
            print(f"    [FAIL] Cannot access __private from child: {e}")


obj = Child()
obj.show()
obj.access()

print()
print("=" * 60)
print("QUICK SUMMARY")
print("=" * 60)
print("  Syntax      | Convention          | Access from Outside | Access from Child")
print("  ------------+---------------------+---------------------+------------------")
print("  self.var    | PUBLIC              | Yes                 | Yes")
print("  self._var   | PROTECTED (internal)| Yes (don't)         | Yes")
print("  self.__var  | PRIVATE (mangled)   | No                  | No")
print("=" * 60)