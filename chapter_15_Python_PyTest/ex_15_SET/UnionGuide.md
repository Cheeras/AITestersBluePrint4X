# Set Operations in Python — Union, Intersection, Difference & More

A complete guide to set operations with operators vs methods.

---

## 1. Quick Reference

| Operation | Operator | Method | In-Place Operator | In-Place Method |
|-----------|:--------:|:------:|:-----------------:|:---------------:|
| **Union** | `a \| b` | `a.union(b)` | `a \|= b` | `a.update(b)` |
| **Intersection** | `a & b` | `a.intersection(b)` | `a &= b` | `a.intersection_update(b)` |
| **Difference** | `a - b` | `a.difference(b)` | `a -= b` | `a.difference_update(b)` |
| **Symmetric Difference** | `a ^ b` | `a.symmetric_difference(b)` | `a ^= b` | `a.symmetric_difference_update(b)` |

---

## 2. Union — Combine Elements from Both Sets

### Operator: `|`
### Method: `union()`

Returns a new set with **all elements** from both sets (duplicates removed).

```python
a = {1, 2, 3}
b = {3, 4, 5}

# Operator
print(a | b)          # {1, 2, 3, 4, 5}

# Method
print(a.union(b))     # {1, 2, 3, 4, 5}

# In-place — modifies original set
a |= b                # a now becomes {1, 2, 3, 4, 5}
a.update(b)           # same as above
```

### Visual Diagram

```mermaid
graph LR
    subgraph "a = {1, 2, 3}"
        A1((1)) A2((2)) A3((3))
    end
    subgraph "b = {3, 4, 5}"
        B3((3)) B4((4)) B5((5))
    end
    subgraph "a | b = {1, 2, 3, 4, 5}"
        R1((1)) R2((2)) R3((3)) R4((4)) R5((5))
    end
    A1 --> R1
    A2 --> R2
    A3 --> R3
    B3 --> R3
    B4 --> R4
    B5 --> R5
```

---

## 3. Intersection — Elements Common to Both Sets

### Operator: `&`
### Method: `intersection()`

Returns a new set with **only the elements that appear in both** sets.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Operator
print(a & b)                   # {3, 4}

# Method
print(a.intersection(b))       # {3, 4}

# In-place — keeps only common elements
a &= b                         # a now becomes {3, 4}
a.intersection_update(b)       # same as above
```

### Visual Diagram

```mermaid
graph LR
    subgraph "a = {1, 2, 3, 4}"
        A1((1)) A2((2)) A3((3)) A4((4))
    end
    subgraph "b = {3, 4, 5, 6}"
        B3((3)) B4((4)) B5((5)) B6((6))
    end
    subgraph "a & b = {3, 4}"
        R3((3)) R4((4))
    end
    A3 --> R3
    A4 --> R4
    B3 --> R3
    B4 --> R4
```

---

## 4. Difference — Elements in First Set but Not in Second

### Operator: `-`
### Method: `difference()`

Returns a new set with elements from `a` that are **not** in `b`.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Operator
print(a - b)                   # {1, 2}

# Method
print(a.difference(b))         # {1, 2}

# Note: b - a is different!
print(b - a)                   # {5, 6}

# In-place — removes common elements from a
a -= b                         # a now becomes {1, 2}
a.difference_update(b)         # same as above
```

### Visual Diagram

```mermaid
graph LR
    subgraph "a = {1, 2, 3, 4}"
        A1((1)) A2((2)) A3((3)) A4((4))
    end
    subgraph "b = {3, 4, 5, 6}"
        B3((3)) B4((4)) B5((5)) B6((6))
    end
    subgraph "a - b = {1, 2}"
        R1((1)) R2((2))
    end
    A1 --> R1
    A2 --> R2
```

---

## 5. Symmetric Difference — Elements in Either, But Not Both

### Operator: `^`
### Method: `symmetric_difference()`

Returns a new set with elements that are in **either** set, **but not** in both (like XOR).

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Operator
print(a ^ b)                         # {1, 2, 5, 6}

# Method
print(a.symmetric_difference(b))     # {1, 2, 5, 6}

# Same result regardless of order
print(b ^ a)                         # {1, 2, 5, 6}

# In-place
a ^= b                               # a now becomes {1, 2, 5, 6}
a.symmetric_difference_update(b)     # same as above
```

### Visual Diagram

```mermaid
graph LR
    subgraph "a = {1, 2, 3, 4}"
        A1((1)) A2((2)) A3((3)) A4((4))
    end
    subgraph "b = {3, 4, 5, 6}"
        B3((3)) B4((4)) B5((5)) B6((6))
    end
    subgraph "a ^ b = {1, 2, 5, 6}"
        R1((1)) R2((2)) R5((5)) R6((6))
    end
    A1 --> R1
    A2 --> R2
    B5 --> R5
    B6 --> R6
```

---

## 6. 🎯 The Key Difference: Operators vs Methods

Both produce the **same result** when both operands are sets:

```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b)          # {1, 2, 3, 4, 5}
print(a.union(b))     # {1, 2, 3, 4, 5}

print(a & b)          # {3}
print(a.intersection(b))  # {3}
```

### 🔑 But Methods Accept ANY Iterable

```python
a = {1, 2, 3}

# ✅ Methods work with lists, tuples, ranges, etc.
print(a.union([4, 5, 6]))              # {1, 2, 3, 4, 5, 6}  ← list
print(a.intersection((2, 3, 4)))       # {2, 3}               ← tuple
print(a.difference(range(1, 3)))       # {3}                  ← range
print(a.symmetric_difference("34"))    # {1, 2, '3', '4'}     ← string

# ❌ Operators require BOTH sides to be sets
# print(a | [4, 5, 6])   # TypeError: unsupported operand type(s) for |: 'set' and 'list'
# print(a & (2, 3, 4))   # TypeError: unsupported operand type(s) for &: 'set' and 'tuple'
# print(a - range(1, 3)) # TypeError: unsupported operand type(s) for -: 'set' and 'range'
```

### Methods Can Chain Multiple Sets

```python
a = {1, 2}

# Method — multiple arguments
print(a.union({3, 4}, {5, 6}, {7, 8}))              # {1, 2, 3, 4, 5, 6, 7, 8}
print(a.intersection({1, 2, 3}, {1, 2, 4}))         # {1, 2}
print(a.difference({1}, {2}))                        # set()

# Operator — needs separate calls
print(a | {3, 4} | {5, 6} | {7, 8})                 # Same result, verbose
```

---

## 7. In-Place Operations (Modify Original Set)

| Operator | Method | What it does |
|:--------:|:------:|-------------|
| `a \|= b` | `a.update(b)` | Adds all items from `b` into `a` |
| `a &= b` | `a.intersection_update(b)` | Keeps only items found in both |
| `a -= b` | `a.difference_update(b)` | Removes items found in `b` |
| `a ^= b` | `a.symmetric_difference_update(b)` | Keeps items not in both |

```python
a = {1, 2, 3}
b = {3, 4, 5}

# Non-in-place — creates a new set, a is unchanged
c = a | b
print(a)  # {1, 2, 3}  ← unchanged

# In-place — modifies a directly
a |= b
print(a)  # {1, 2, 3, 4, 5}  ← changed!
```

---

## 8. Comparison Table

| Aspect | Operator (`\|`, `&`, `-`, `^`) | Method (`union()`, `intersection()`, etc.) |
|--------|:------------------------------:|:------------------------------------------:|
| **Both args must be set** | ✅ Yes | ❌ No — any iterable works |
| **Syntax** | Short and clean | Verbose but flexible |
| **Multiple sets** | Needs chaining `a \| b \| c` | Accepts multiple args `.union(b, c)` |
| **In-place version** | `a \|= b` | `a.update(b)` |
| **Readability** | ⭐ Excellent for set-to-set | ⭐ Better for mixed types |

---

## 9. Best Practices ✅

### ✅ Use Operators When

```python
# Both are sets — operator is cleaner
active_users = {"alice", "bob", "charlie"}
admin_users = {"bob", "dave"}

all_users = active_users | admin_users      # ✅ Clean
common = active_users & admin_users          # ✅ Clean
```

### ✅ Use Methods When

```python
# Second arg is a list/tuple — method is required
active_users = {"alice", "bob", "charlie"}
new_signups = ["dave", "eve"]                # ← list, not set

all_users = active_users.union(new_signups)  # ✅ Works
# all_users = active_users | new_signups     # ❌ TypeError!

# Multiple sets at once
a = {1, 2}
result = a.union({3, 4}, {5, 6}, {7, 8})    # ✅ Multiple args
```

### ✅ Use In-Place When Modifying Original

```python
# Instead of creating a new variable
all_items = all_items | new_items     # Creates new set, reassigns

# Use in-place — modifies directly
all_items |= new_items                # ✅ More efficient
all_items.update(new_items)           # ✅ Same thing
```

---

## 10. Real-World Examples

### 10.1 Merge User Permissions

```python
# Users with different permission levels
basic_permissions = {"read", "write"}
admin_permissions = {"read", "write", "delete", "manage_users"}

# Give admin all basic permissions
full_permissions = basic_permissions | admin_permissions
print(full_permissions)  # {'read', 'write', 'delete', 'manage_users'}
```

### 10.2 Find Common Test Failures

```python
chrome_failures = {"TC-01", "TC-03", "TC-05"}
firefox_failures = {"TC-03", "TC-05", "TC-07"}
edge_failures = {"TC-03", "TC-05", "TC-09"}

# Tests that fail in ALL browsers
critical_failures = chrome_failures & firefox_failures & edge_failures
print(critical_failures)  # {'TC-03', 'TC-05'}
```

### 10.3 Find Tests That Passed (Difference)

```python
all_tests = {"TC-01", "TC-02", "TC-03", "TC-04", "TC-05"}
failed_tests = {"TC-02", "TC-04"}

passed_tests = all_tests - failed_tests
print(passed_tests)  # {'TC-01', 'TC-03', 'TC-05'}
```

### 10.4 Find Tests That Ran in Only One Browser

```python
chrome_tests = {"TC-01", "TC-02", "TC-03", "TC-04"}
firefox_tests = {"TC-03", "TC-04", "TC-05", "TC-06"}

# Tests exclusive to each browser
only_chrome = chrome_tests - firefox_tests     # {'TC-01', 'TC-02'}
only_firefox = firefox_tests - chrome_tests    # {'TC-05', 'TC-06'}

# Tests that ran in only one browser (not both)
exclusive_tests = chrome_tests ^ firefox_tests  # {'TC-01', 'TC-02', 'TC-05', 'TC-06'}
```

### 10.5 Add New Tags to Existing Set

```python
# Using in-place union
existing_tags = {"smoke", "regression", "critical"}
new_tags = ["ui", "performance"]  # ← list from external source

existing_tags.update(new_tags)  # ✅ In-place, works with list
print(existing_tags)  # {'smoke', 'regression', 'critical', 'ui', 'performance'}

# Same thing with operator (but must convert to set first)
existing_tags |= set(new_tags)
```

---

## 11. Quick Reference Card

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Create new sets
a | b              # {1, 2, 3, 4, 5, 6}  — Union
a & b              # {3, 4}               — Intersection
a - b              # {1, 2}               — Difference (in a, not b)
b - a              # {5, 6}               — Difference (in b, not a)
a ^ b              # {1, 2, 5, 6}         — Symmetric Difference

# Methods (accept any iterable)
a.union(b)                    # {1, 2, 3, 4, 5, 6}
a.intersection(b)             # {3, 4}
a.difference(b)               # {1, 2}
a.symmetric_difference(b)     # {1, 2, 5, 6}

# In-place (modify original)
a |= b          # a.update(b)
a &= b          # a.intersection_update(b)
a -= b          # a.difference_update(b)
a ^= b          # a.symmetric_difference_update(b)

# Check relationships
a.isdisjoint(b)               # True if no common elements
a.issubset(b)                 # True if a ⊆ b
a.issuperset(b)               # True if a ⊇ b
```

---

## 12. Summary

> **Use operators (`|`, `&`, `-`, `^`) when both sides are sets — shorter and cleaner.**
> **Use methods (`union()`, `intersection()`, etc.) when working with lists, tuples, or other iterables.**
> **Use in-place versions (`|=`, `&=`) when you want to modify the original set instead of creating a new one.**

| Scenario | Recommendation |
|----------|:--------------:|
| Both are sets | `a \| b` ✅ |
| Second arg is a list/tuple | `a.union(b)` ✅ |
| Need to modify original | `a \|= b` ✅ |
| Multiple sets at once | `a.union(b, c, d)` ✅ |
| Readable code review | Either — both are standard |