# Lambda Expressions in Python

A complete beginner-to-advanced guide on lambda (anonymous) functions.

---

## 1. What is a Lambda Expression?

A **lambda** is a small, **anonymous** (nameless) function defined in a single line.

```python
lambda arguments: expression
```

| Part | Meaning |
|------|---------|
| `lambda` | Keyword — "I'm creating a quick function" |
| `arguments` | Input parameters (like normal function params) |
| `:` | Separator between arguments and expression |
| `expression` | Single expression — **automatically returned** (no `return` needed) |

### Example

```python
# Normal function
def add(a, b):
    return a + b

# Lambda equivalent
add_lambda = lambda a, b: a + b

print(add(5, 3))        # 8
print(add_lambda(5, 3))  # 8
```

---

## 2. Lambda vs Normal Function

| Aspect | Normal `def` | Lambda |
|--------|:---:|:------:|
| **Name** | Has a name | Anonymous (no name) |
| **Lines** | Multiple lines allowed | **Single expression only** |
| **Return** | Explicit `return` needed | Implicit return |
| **Statements** | ✅ Loops, if-else, try/except | ❌ Only expressions |
| **Reuse** | ✅ Call from anywhere | ❌ Defined where used |
| **Docstring** | ✅ Can have docstrings | ❌ Cannot |
| **Best for** | Complex logic, reusable code | Simple one-liner callbacks |

### Key Difference — Statements vs Expressions

```python
# ❌ Lambda CANNOT have statements (print, if-elif-else with blocks, loops)
# lambda x: print(x) or x * 2   ← SyntaxError

# ✅ Lambda CAN have conditional expression (ternary)
max_val = lambda a, b: a if a > b else b

# ✅ Equivalent normal function
def max_val(a, b):
    if a > b:
        return a
    else:
        return b
```

---

## 3. Lambda with Multiple Arguments

```python
# Two arguments
multiply = lambda a, b: a * b
print(multiply(5, 6))  # 30

# Three arguments
sum_three = lambda a, b, c: a + b + c
print(sum_three(5, 6, 7))  # 18

# Default arguments
power = lambda base, exp=2: base ** exp
print(power(5))     # 25 (5^2)
print(power(5, 3))  # 125 (5^3)

# Variable arguments (*args)
sum_all = lambda *args: sum(args)
print(sum_all(1, 2, 3, 4, 5))  # 15
```

---

## 4. Lambda with Conditional (Ternary)

```python
# if-else in lambda
check_even_odd = lambda num: "Even" if num % 2 == 0 else "Odd"
print(check_even_odd(5))  # Odd
print(check_even_odd(8))  # Even

# Nested ternary (use sparingly — can be hard to read)
grade = lambda score: "A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70 else "F"
print(grade(85))  # B
```

---

## 5. Where to Use Lambda — The Big 3

Lambda shines when passed as an argument to other functions.

### 5.1 `map()` — Transform Every Item

Applies a function to each item in an iterable.

```python
numbers = [1, 2, 3, 4, 5]

# Double each number
doubled = list(map(lambda x: x * 2, numbers))
print(doubled)  # [2, 4, 6, 8, 10]

# Convert to uppercase
names = ["alice", "bob", "charlie"]
upper_names = list(map(lambda n: n.upper(), names))
print(upper_names)  # ['ALICE', 'BOB', 'CHARLIE']
```

### 5.2 `filter()` — Keep Items That Match

Keeps only items where the condition is `True`.

```python
numbers = [1, 2, 3, 4, 5, 6]

# Keep only even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6]

# Keep only names with length > 3
names = ["hi", "hello", "hey", "greetings"]
long_names = list(filter(lambda n: len(n) > 3, names))
print(long_names)  # ['hello', 'greetings']
```

### 5.3 `sorted()` — Custom Sort Order

Sorts using a custom key function.

```python
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob",   "grade": 72},
    {"name": "Charlie", "grade": 95},
]

# Sort by grade (ascending)
sorted_by_grade = sorted(students, key=lambda s: s["grade"])
print(sorted_by_grade)
# [{'name': 'Bob', 'grade': 72}, {'name': 'Alice', 'grade': 85}, {'name': 'Charlie', 'grade': 95}]

# Sort by grade (descending)
sorted_desc = sorted(students, key=lambda s: s["grade"], reverse=True)

# Sort by name length
sorted_by_name_len = sorted(students, key=lambda s: len(s["name"]))
```

---

## 6. Lambda with Other Built-in Functions

### 6.1 `max()` / `min()` with Custom Key

```python
students = [("Alice", 85), ("Bob", 72), ("Charlie", 95)]

# Student with highest grade
top_student = max(students, key=lambda s: s[1])
print(top_student)  # ('Charlie', 95)

# Student with lowest grade
worst_student = min(students, key=lambda s: s[1])
print(worst_student)  # ('Bob', 72)
```

### 6.2 `any()` / `all()` with Lambda

```python
numbers = [1, 2, 3, 4, 5]

# Is any number even?
has_even = any(map(lambda x: x % 2 == 0, numbers))
print(has_even)  # True

# Are all numbers positive?
all_positive = all(map(lambda x: x > 0, numbers))
print(all_positive)  # True

# Are all numbers less than 10?
all_small = all(map(lambda x: x < 10, numbers))
print(all_small)  # True
```

### 6.3 `reduce()` from functools

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Sum all numbers
total = reduce(lambda a, b: a + b, numbers)
print(total)  # 15

# Find the maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
print(maximum)  # 5
```

---

## 7. Lambda with `pandas` (Data Analysis)

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "salary": [50000, 60000, 70000]
})

# Apply 10% bonus
df["bonus"] = df["salary"].apply(lambda s: s * 0.10)

# Categorize salary
df["level"] = df["salary"].apply(
    lambda s: "Junior" if s < 55000 else "Mid" if s < 65000 else "Senior"
)
print(df)
```

---

## 8. Lambda with `tkinter` (GUI)

```python
import tkinter as tk

root = tk.Tk()
button = tk.Button(
    root,
    text="Click Me",
    command=lambda: print("Button clicked!")  # Inline callback
)
button.pack()
root.mainloop()
```

---

## 9. Best Practices ✅

### ✅ DO Use Lambda When

| Scenario | Example |
|----------|---------|
| Inside `map()` / `filter()` / `sorted()` | `map(lambda x: x * 2, numbers)` |
| Simple key function for sorting | `sorted(items, key=lambda i: i["id"])` |
| Quick inline transformation | `list(map(lambda s: s.strip().lower(), names))` |
| Throwaway callback | `button.config(command=lambda: save())` |
| Inside `any()` / `all()` checks | `all(map(lambda r: r.ok, responses))` |

### ❌ DON'T Use Lambda When

| Anti-pattern | Why | Fix |
|-------------|:---:|:---:|
| **Assigning to a variable** | Just use `def` | `def add(a, b): return a + b` |
| **More than one expression** | Lambda only supports one | Use a named function |
| **Complex logic (if-elif-else blocks)** | Impossible to read | Use a named function |
| **Same lambda repeated in code** | DRY violation | Extract to named function |
| **Needs a docstring** | Lambda can't have docs | Use `def` with docstring |

### ⚠️ The PEP 8 Rule

> **PEP 8** — The official Python style guide says:
> *"Always use a def statement instead of an assignment statement that binds a lambda expression directly to an identifier."*

```python
# ❌ BAD — assigning lambda to a variable (PEP 8 violation)
double = lambda x: x * 2

# ✅ GOOD — use def instead
def double(x):
    return x * 2
```

---

## 10. Common Pitfalls

### Pitfall 1: Late Binding Closure

```python
# ❌ BUG — all functions return 9
funcs = [lambda x: x ** i for i in range(5)]
print([f(3) for f in funcs])  # [81, 81, 81, 81, 81] — all use i=4!

# ✅ FIX — capture i at creation time
funcs = [lambda x, i=i: x ** i for i in range(5)]
print([f(3) for f in funcs])  # [1, 3, 9, 27, 81]
```

### Pitfall 2: Forgetting to Call

```python
# ❌ BUG — returns the lambda itself, not the result
add = lambda a, b: a + b
result = add  # ← forgot (5, 3)
print(result)  # <function <lambda> at 0x...>

# ✅ FIX — call it
result = add(5, 3)
print(result)  # 8
```

### Pitfall 3: Too Complex to Read

```python
# ❌ BAD — unreadable mess
process = lambda items: list(map(lambda x: (lambda y: y * 2)(x) if x > 0 else (lambda z: abs(z) * 3)(x), items))

# ✅ GOOD — named functions are readable
def transform(x):
    if x > 0:
        return x * 2
    return abs(x) * 3

process = [transform(x) for x in items]
```

---

## 11. Quick Reference Card

| Task | Lambda Expression |
|------|-------------------|
| Double a number | `lambda x: x * 2` |
| Add two numbers | `lambda a, b: a + b` |
| Check if even | `lambda x: x % 2 == 0` |
| Ternary (if-else) | `lambda x: "Even" if x % 2 == 0 else "Odd"` |
| Square a number | `lambda x: x ** 2` |
| String to uppercase | `lambda s: s.upper()` |
| Get dict value | `lambda d: d["key"]` |
| Get tuple element | `lambda t: t[1]` |
| Length of string | `lambda s: len(s)` |
| Strip and lowercase | `lambda s: s.strip().lower()` |
| Sum of list | `lambda *args: sum(args)` |
| Return True if > 0 | `lambda x: x > 0` |

---

## 12. Summary

> **Use lambda when you need a simple, one-expression function as an argument to another function. Use `def` for everything else.**

```python
# ✅ Good lambda uses
list(map(lambda x: x * 2, data))              # Transform
list(filter(lambda x: x > 0, data))           # Filter
sorted(data, key=lambda x: x["name"])         # Sort
any(map(lambda x: x > 0, data))               # Check
max(data, key=lambda x: x.score)              # Find max

# ❌ Bad lambda uses
double = lambda x: x * 2                      # Use def
complex_logic = lambda x: ...                 # Use def
repeated_lambda = ...                         # Extract to def
```