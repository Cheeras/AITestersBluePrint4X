# Lambda Expressions in Test Automation

Real-world use cases of lambda in **Playwright**, **Selenium**, and **API testing** frameworks.

---

## 1. 🎭 Playwright — UI Testing

### 1.1 Sort Test Data by Custom Criteria

```python
test_data = [
    {"name": "Login",    "priority": 1, "duration_ms": 1200},
    {"name": "Logout",   "priority": 3, "duration_ms": 400},
    {"name": "Signup",   "priority": 2, "duration_ms": 900},
]

# Sort tests by priority (ascending)
sorted_tests = sorted(test_data, key=lambda t: t["priority"])

# Sort by duration (descending) — run slowest tests first
sorted_by_duration = sorted(test_data, key=lambda t: t["duration_ms"], reverse=True)
```

### 1.2 Filter Test Results

```python
test_results = [
    {"name": "TC-01", "status": "passed", "browser": "chrome"},
    {"name": "TC-02", "status": "failed", "browser": "firefox"},
    {"name": "TC-03", "status": "passed", "browser": "edge"},
    {"name": "TC-04", "status": "failed", "browser": "chrome"},
]

# Get only failed tests
failed_tests = list(filter(lambda t: t["status"] == "failed", test_results))

# Get Chrome tests only
chrome_tests = list(filter(lambda t: t["browser"] == "chrome", test_results))
```

### 1.3 Transform Browser Configs

```python
browsers = [
    {"name": "chrome",  "width": 1920, "height": 1080},
    {"name": "firefox", "width": 1366, "height": 768},
    {"name": "edge",    "width": 1440, "height": 900},
]

# Generate viewport strings for reporting
viewport_labels = list(
    map(lambda b: f"{b['name']}: {b['width']}x{b['height']}", browsers)
)
print(viewport_labels)
# ['chrome: 1920x1080', 'firefox: 1366x768', 'edge: 1440x900']
```

### 1.4 Dynamic Assertions with `expect`

```python
from playwright.sync_api import expect

# Check if any element in a list matches a condition
elements = page.locator(".product-price").all()
prices = [float(e.text_content().replace("$", "")) for e in elements]

# Assert all prices are > 0
assert all(map(lambda p: p > 0, prices)), "All prices must be positive"

# Assert at least one item is on sale (< $10)
assert any(map(lambda p: p < 10, prices)), "At least one item should be on sale"
```

### 1.5 Generate Unique Test IDs

```python
test_cases = ["Login", "Logout", "Signup", "Payment"]
# Create test IDs: TC-LOGIN, TC-LOGOUT, TC-SIGNUP, TC-PAYMENT
test_ids = list(map(lambda tc: f"TC-{tc.upper()}", test_cases))
print(test_ids)
```

---

## 2. 🌐 Selenium — UI Testing

### 2.1 Clean Up Web Elements

```python
from selenium.webdriver.common.by import By

# Remove empty or whitespace-only texts from a list
elements = driver.find_elements(By.CSS_SELECTOR, ".product-name")
product_names = list(
    filter(lambda n: n.strip(), map(lambda e: e.text, elements))
)
```

### 2.2 Validate Multiple Fields

```python
form_fields = [
    {"locator": (By.ID, "username"), "expected": "user@example.com"},
    {"locator": (By.ID, "email"),    "expected": "user@example.com"},
    {"locator": (By.ID, "phone"),    "expected": "+1-555-0100"},
]

# Check all fields match expected values
all_match = all(
    map(lambda f: driver.find_element(*f["locator"]).get_attribute("value") == f["expected"],
        form_fields)
)
assert all_match, "Form fields do not match expected values"
```

### 2.3 Dynamic Wait Conditions

```python
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Wait until any of several elements appears
locators = [
    (By.ID, "success-message"),
    (By.ID, "error-message"),
    (By.CLASS_NAME, "notification"),
]

# Using lambda with EC.any_of (Python 3.10+)
wait = WebDriverWait(driver, 10)
element = wait.until(
    lambda d: next((d.find_element(*loc) for loc in locators if d.find_elements(*loc)), None)
)
```

### 2.4 Extract Data from Tables

```python
rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

# Parse each row into a dict
parsed_data = list(map(lambda row: {
    "id":   row.find_elements(By.TAG_NAME, "td")[0].text,
    "name": row.find_elements(By.TAG_NAME, "td")[1].text,
    "status": row.find_elements(By.TAG_NAME, "td")[2].text,
}, rows))
```

---

## 3. 🔌 API Testing (Requests / pytest)

### 3.1 Validate Response Status Codes

```python
import requests

endpoints = [
    ("GET",    "https://api.github.com/users/octocat"),
    ("GET",    "https://api.github.com/repos/octocat/hello-world"),
    ("GET",    "https://api.github.com/rate_limit"),
]

# Check all endpoints return 200
responses = list(map(lambda ep: requests.request(ep[0], ep[1]), endpoints))
assert all(map(lambda r: r.status_code == 200, responses)), "All endpoints must return 200"
```

### 3.2 Filter API Response Data

```python
response = requests.get("https://api.github.com/search/repositories?q=python+testing")
data = response.json()

# Get only repos with > 100 stars
popular_repos = list(
    filter(lambda r: r["stargazers_count"] > 100, data["items"])
)

# Extract just the names and URLs
repo_summary = list(
    map(lambda r: {"name": r["name"], "url": r["html_url"]}, popular_repos)
)
```

### 3.3 Parametrize Test Data

```python
import pytest

# Generate test data dynamically
test_inputs = [1, 2, 3, 4, 5]
expected_outputs = list(map(lambda x: x * 2, test_inputs))

@pytest.mark.parametrize("input_val,expected", list(zip(test_inputs, expected_outputs)))
def test_double(input_val, expected):
    assert input_val * 2 == expected
```

### 3.4 Assert Response Schema

```python
response = requests.get("https://api.example.com/users/1")
user = response.json()

required_fields = ["id", "name", "email", "created_at"]

# Check all required fields exist
assert all(map(lambda f: f in user, required_fields)), "Missing required fields"

# Check no field is None
assert all(map(lambda f: user[f] is not None, required_fields)), "Required fields cannot be null"
```

### 3.5 Transform API Payloads

```python
# Convert list of user IDs to API request payload
user_ids = [101, 102, 103]
payloads = list(map(lambda uid: {"user_id": uid, "action": "activate"}, user_ids))

# Send batch requests
responses = list(map(lambda p: requests.post("https://api.example.com/users/action", json=p), payloads))
```

---

## 4. 🧪 pytest — Test Framework Utilities

### 4.1 Dynamic Test IDs for Parametrization

```python
import pytest

test_data = [
    ("chrome",  "standard_user", "secret_sauce"),
    ("firefox", "problem_user",  "secret_sauce"),
    ("edge",    "locked_out_user", "secret_sauce"),
]

# Generate readable test IDs: chrome-standard_user, firefox-problem_user, etc.
test_ids = list(map(lambda d: f"{d[0]}-{d[1]}", test_data))

@pytest.mark.parametrize("browser,username,password", test_data, ids=test_ids)
def test_login(browser, username, password):
    # Test logic here
    pass
```

### 4.2 Filter Test Fixtures

```python
# configs.py
browser_configs = [
    {"name": "chrome",  "headless": True,  "viewport": {"width": 1920, "height": 1080}},
    {"name": "firefox", "headless": False, "viewport": {"width": 1366, "height": 768}},
    {"name": "edge",    "headless": True,  "viewport": {"width": 1440, "height": 900}},
]

# Get only headless configs
headless_configs = list(filter(lambda c: c["headless"], browser_configs))

# Get configs with width > 1400
wide_configs = list(filter(lambda c: c["viewport"]["width"] > 1400, browser_configs))
```

### 4.3 Custom pytest Hooks

```python
# conftest.py
def pytest_collection_modifyitems(config, items):
    """Run slower tests last."""
    items.sort(key=lambda item: item.get_closest_marker("slow") is not None)
```

---

## 5. 📊 Best Practices for Lambda in Automation

### ✅ DO

| Practice | Example |
|----------|---------|
| **Use with `map()`, `filter()`, `sorted()`** | `sorted(tests, key=lambda t: t["priority"])` |
| **Keep it simple — one expression** | `lambda x: x.strip().lower()` |
| **Use for throwaway logic** | Inline inside `pytest.mark.parametrize` |
| **Combine with `all()` / `any()`** | `all(map(lambda r: r.status_code == 200, responses))` |
| **Use for data transformation** | Converting API responses, formatting test data |

### ❌ DON'T

| Anti-pattern | Why | Fix |
|-------------|:---:|:---:|
| **Assign lambda to a variable** | Just use `def` | `def double(x): return x * 2` |
| **Complex multi-step logic** | Unreadable | Use a named function |
| **Side effects inside lambda** | Lambda should return, not `print()` | Use `def` |
| **Same lambda repeated** | DRY violation | Extract to a named function |
| **Nested lambdas** | Impossible to debug | Break into smaller functions |

### 🏆 The Golden Rule for Automation

```python
# ✅ GOOD — simple, readable, one expression
sorted_tests = sorted(all_tests, key=lambda t: t["priority"])

# ✅ GOOD — inline transformation
test_ids = list(map(lambda tc: f"TC-{tc.upper()}", test_cases))

# ✅ GOOD — quick filter
failed = list(filter(lambda r: r["status"] == "failed", results))

# ❌ BAD — too complex for lambda
process = lambda x: x * 2 if x > 0 else (x + 10 if x == 0 else abs(x) * 3)

# ✅ FIX — use a named function
def process(x):
    if x > 0:
        return x * 2
    elif x == 0:
        return x + 10
    else:
        return abs(x) * 3
```

---

## 6. 🚀 Quick Reference Card

| Use Case | Lambda Expression |
|----------|------------------|
| Sort tests by priority | `sorted(tests, key=lambda t: t["priority"])` |
| Filter failed tests | `filter(lambda r: r["status"] == "failed", results)` |
| Transform test names | `map(lambda tc: tc.upper(), test_cases)` |
| Validate all responses | `all(map(lambda r: r.ok, responses))` |
| Check any element matches | `any(map(lambda p: p < 10, prices))` |
| Generate test IDs | `map(lambda d: f"{d[0]}-{d[1]}", data)` |
| Extract field from list | `map(lambda u: u["name"], users)` |
| Custom sort key | `sorted(items, key=lambda i: i["duration"])` |