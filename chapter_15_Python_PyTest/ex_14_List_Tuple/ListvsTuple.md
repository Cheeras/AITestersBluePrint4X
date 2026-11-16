# List vs Tuple in Python

## 🧠 Layman Analogy

Think of **List** as a **whiteboard** 🏷️ and **Tuple** as an **engraved stone tablet** 🪨.

| Feature | **List** (Whiteboard) | **Tuple** (Stone Tablet) |
|---------|-----------------------|--------------------------|
| **Can change?** | ✅ Yes — erase, rewrite, add, remove | ❌ No — once written, permanent |
| **Flexible** | ✅ Can grow or shrink | ❌ Fixed size forever |
| **Speed** | ⏱️ Slightly slower (because changeable) | ⚡ Faster (Python optimizes it) |
| **Syntax** | Square brackets `[]` | Parentheses `()` |

---

## 📊 Quick Comparison Table

| Feature | List | Tuple |
|---------|:----:|:-----:|
| **Syntax** | `[1, 2, 3]` | `(1, 2, 3)` |
| **Mutable?** | ✅ Yes | ❌ No |
| **Ordered?** | ✅ Yes | ✅ Yes |
| **Indexed?** | ✅ Yes | ✅ Yes |
| **Allow duplicates?** | ✅ Yes | ✅ Yes |
| **Heterogeneous?** | ✅ Yes | ✅ Yes |
| **Hashable (can be dict key)?** | ❌ No | ✅ Yes |
| **Performance** | Slower | Faster |
| **Built-in methods** | Many (`append`, `remove`, `sort`, etc.) | Few (`count`, `index`) |

---

## 🔧 Code Examples

### 1. Creating List vs Tuple

```python
# List — square brackets
fruits_list = ["apple", "banana", "orange"]

# Tuple — parentheses
fruits_tuple = ("apple", "banana", "orange")

print(type(fruits_list))   # <class 'list'>
print(type(fruits_tuple))  # <class 'tuple'>
```

### 2. Accessing elements (same for both)

```python
my_list = ["a", "b", "c"]
my_tuple = ("a", "b", "c")

print(my_list[0])    # a
print(my_tuple[1])   # b
print(my_list[-1])   # c (negative indexing)
print(my_tuple[0:2]) # ('a', 'b') (slicing)
```

### 3. Mutable vs Immutable

```python
# LIST — can change
fruits = ["apple", "banana"]
fruits.append("orange")   # ✅ Add new item
fruits[0] = "mango"       # ✅ Replace item
fruits.remove("banana")   # ✅ Remove item
print(fruits)             # ['mango', 'orange']

# TUPLE — cannot change
days = ("Mon", "Tue", "Wed")
days[0] = "Sun"           # ❌ TypeError: 'tuple' object does not support item assignment
days.append("Thu")        # ❌ AttributeError: 'tuple' object has no attribute 'append'
```

### 4. Tuple Packing and Unpacking

```python
# Packing
coordinates = (10, 20, 30)

# Unpacking
x, y, z = coordinates
print(x, y, z)  # 10 20 30

# Swap variables (elegant with tuples)
a, b = 5, 10
a, b = b, a
print(a, b)  # 10 5
```

### 5. List to Tuple and Vice Versa

```python
# Tuple → List (when you need to modify)
api_urls = ("https://api.github.com", "https://api.twitter.com")
api_list = list(api_urls)
api_list.append("https://api.new.com")
print(api_list)

# List → Tuple (when you want to protect data)
browsers = ["chrome", "firefox", "edge"]
browsers_tuple = tuple(browsers)
# browsers_tuple[0] = "safari"  ❌ Now protected!
```

---

## ✅ When to Use Tuple — Real-World Examples

### 1. API URLs / Configuration (Should never change)

```python
# 🔒 Fixed endpoints — protected from accidental modification
API_URLs = (
    "https://api.github.com",
    "https://api.twitter.com",
    "https://api.facebook.com"
)
```

### 2. Days of Week / Months / Fixed Constants

```python
# 🔒 These never change — perfect for tuple
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
```

### 3. Function Returning Multiple Values

```python
def get_min_max(numbers):
    return min(numbers), max(numbers)  # Returns a tuple

result = get_min_max([3, 7, 1, 9, 4])
print(result)       # (1, 9)
minimum, maximum = result  # Tuple unpacking
print(minimum)      # 1
```

### 4. Dictionary Keys (List cannot be used)

```python
# ✅ Tuple works as dictionary key
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London"
}
print(locations[(40.7128, -74.0060)])  # New York

# ❌ List cannot be used as dictionary key
# locations[[1, 2, 3]] = "invalid"  # TypeError: unhashable type: 'list'
```

### 5. Database Records (Read-only data)

```python
# Each row from DB is typically returned as a tuple
employees = (
    (101, "Alice", "QA Engineer"),
    (102, "Bob", "SDET"),
    (103, "Charlie", "DevOps")
)
for emp_id, name, role in employees:
    print(f"{emp_id}: {name} — {role}")
```

### 6. HTTP Status Codes

```python
# 🔒 Fixed set of related constants
HTTP_SUCCESS = (200, 201, 204)
HTTP_REDIRECT = (301, 302, 307)
HTTP_CLIENT_ERROR = (400, 401, 403, 404)
HTTP_SERVER_ERROR = (500, 502, 503)
```

---

## ✅ When to Use List — Real-World Examples

### 1. Test Case IDs (Growing collection)

```python
# 📝 New test cases keep getting added
test_case_ids = ["TC-001", "TC-002", "TC-003"]
test_case_ids.append("TC-004")  # ✅ Add new test case
test_case_ids.append("TC-005")
print(test_case_ids)  # ['TC-001', 'TC-002', 'TC-003', 'TC-004', 'TC-005']
```

### 2. Shopping Cart / Dynamic Collections

```python
# 🛒 Items come and go
cart = []
cart.append("Laptop")
cart.append("Mouse")
cart.append("Keyboard")
cart.remove("Mouse")           # Removed from cart
cart[0] = "Gaming Laptop"      # Changed mind
print(cart)  # ['Gaming Laptop', 'Keyboard']
```

### 3. Browser Tabs (User opens/closes tabs)

```python
# 🌐 User keeps opening and closing tabs
browser_tabs = ["login", "dashboard"]
browser_tabs.append("settings")   # Open new tab
browser_tabs.append("profile")
browser_tabs.remove("login")      # Close tab
print(browser_tabs)  # ['dashboard', 'settings', 'profile']
```

### 4. Student Marks (Need sorting & modification)

```python
# 📊 Marks need to be updated and sorted
marks = [85, 92, 78, 95]
marks.append(88)         # New mark added
marks.sort()             # Sort ascending
marks[0] = 80            # Correct a wrong entry
print(marks)  # [80, 85, 88, 92, 95]
```

### 5. Queue of Tasks / To-Do List

```python
# ✅ Tasks change constantly
todo_list = ["Write tests", "Review PR", "Fix bug #42"]
todo_list.append("Deploy to staging")
completed = todo_list.pop(0)   # Remove first task
print(f"Completed: {completed}")  # Write tests
print(f"Remaining: {todo_list}")
```

---

## 🚀 Performance Difference

Tuples are **faster** than lists because they are immutable — Python can optimize memory allocation.

```python
import timeit

# List creation
list_time = timeit.timeit('[1, 2, 3, 4, 5]', number=10_000_000)
print(f"List:  {list_time:.4f} sec")

# Tuple creation
tuple_time = timeit.timeit('(1, 2, 3, 4, 5)', number=10_000_000)
print(f"Tuple: {tuple_time:.4f} sec")
```

**Typical output:**
```
List:  0.85 sec
Tuple: 0.12 sec   ← ~7x faster!
```

---

## 📝 Summary — One-Liner Rule

> **Use `tuple` when the data is fixed and should be protected. Use `list` when the data needs to grow, shrink, or change.**

| Scenario | Use | Why |
|----------|:---:|-----|
| API endpoints | ✅ **Tuple** | Fixed — never changes |
| Days of week | ✅ **Tuple** | Fixed set |
| DB query results | ✅ **Tuple** | Read-only data |
| Function returns | ✅ **Tuple** | Multiple values, immutable |
| Dict keys | ✅ **Tuple** | List can't be keys |
| Shopping cart | ✅ **List** | Items added/removed |
| Test case IDs | ✅ **List** | Collection grows |
| User data | ✅ **List** | Gets updated frequently |
| Sorting needed | ✅ **List** | Tuple has no `.sort()` |

---

## 🧪 Quick Quiz

```python
# Guess which works and which doesn't:
data1 = [1, 2, 3]
data2 = (1, 2, 3)

data1.append(4)      # ✅ or ❌ ?
data2.append(4)      # ✅ or ❌ ?
data1[0] = 99        # ✅ or ❌ ?
data2[0] = 99        # ✅ or ❌ ?

my_dict = {data1: "list"}   # ✅ or ❌ ?
my_dict = {data2: "tuple"}  # ✅ or ❌ ?
```

**Answers:**
- `data1.append(4)` → ✅ List is mutable
- `data2.append(4)` → ❌ Tuple has no `append`
- `data1[0] = 99` → ✅ List supports item assignment
- `data2[0] = 99` → ❌ Tuple is immutable
- `{data1: "list"}` → ❌ List is unhashable
- `{data2: "tuple"}` → ✅ Tuple is hashable