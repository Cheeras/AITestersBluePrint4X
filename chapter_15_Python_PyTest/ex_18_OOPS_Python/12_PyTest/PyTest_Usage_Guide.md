# PyTest Usage Guide

## What is PyTest?

**PyTest** is a Python testing framework that makes it easy to write simple and scalable test cases. It is the most popular testing framework in the Python ecosystem.

### Why PyTest is Used in Automation

| Feature                           | Benefit                                                                                     |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| **Simple syntax**           | Write tests with plain `assert` — no need for `self.assertEqual()` or `assertTrue()` |
| **Auto-discovery**          | PyTest automatically finds test files and functions — no test suite configuration needed   |
| **Fixtures**                | Reusable setup/teardown code (e.g., browser launch, DB connection)                          |
| **Parametrization**         | Run the same test with multiple inputs using `@pytest.mark.parametrize`                   |
| **Plugins**                 | HTML reports, parallel execution, code coverage — all via plugins                          |
| **Assertion introspection** | Detailed failure messages — shows exactly what values were compared                        |
| **CI/CD friendly**          | Exit codes, JUnit XML output, and seamless integration with Jenkins, GitHub Actions, etc.   |

---

## Naming Conventions

PyTest uses **auto-discovery** — it finds tests by name. Follow these conventions:

### File Names

| Convention          | Example            | Discovered?                |
| ------------------- | ------------------ | -------------------------- |
| `test_<name>.py`  | `test_login.py`  | ✅ Yes                     |
| `<name>_test.py`  | `login_test.py`  | ✅ Yes                     |
| `test-<name>.py`  | `test-login.py`  | ❌ No (hyphen not allowed) |
| `check_<name>.py` | `check_login.py` | ❌ No                      |

### Function Names

| Convention       | Example                | Discovered? |
| ---------------- | ---------------------- | ----------- |
| `test_<name>`  | `test_login_valid()` | ✅ Yes      |
| `<name>_test`  | `login_valid_test()` | ❌ No       |
| `check_<name>` | `check_login()`      | ❌ No       |

### Class Names

| Convention     | Example       | Discovered? |
| -------------- | ------------- | ----------- |
| `Test<Name>` | `TestLogin` | ✅ Yes      |
| `<Name>Test` | `LoginTest` | ❌ No       |

> **Rule of thumb:** Always prefix with `test_` for files/functions and `Test` for classes.

---

## Basic Examples

### Example 1: Simple test file

**test_math.py**

```python
def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2

def test_fail():
    assert 1 == 2  # This will fail
```

Run it:

```powershell
pytest test_math.py -v
```

Output:

```
test_math.py::test_addition PASSED
test_math.py::test_subtraction PASSED
test_math.py::test_fail FAILED
```

### Example 2: Test with a class

**test_login.py**

```python
class TestLogin:
    def test_valid_login(self):
        username = "admin"
        password = "pass123"
        assert username == "admin" and password == "pass123"

    def test_invalid_login(self):
        username = "admin"
        password = "wrong"
        assert username != "admin" or password != "pass123"
```

### Example 3: Using fixtures (setup/teardown)

**test_browser.py**

```python
import pytest

@pytest.fixture
def browser():
    print("\n🚀 Launching browser...")
    driver = "Chrome Driver"  # In real code: WebDriver()
    yield driver              # Test runs here
    print("\n🛑 Closing browser...")
    driver = None

def test_title(browser):
    assert browser == "Chrome Driver"

def test_url(browser):
    assert browser is not None
```

### Example 4: Parametrized tests

**test_calculator.py**

```python
import pytest

@pytest.mark.parametrize("a, b, expected", [
    (1, 1, 2),
    (2, 3, 5),
    (10, -5, 5),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert a + b == expected
```

Run it:

```powershell
pytest test_calculator.py -v
```

Output:

```
test_calculator.py::test_add[1-1-2] PASSED
test_calculator.py::test_add[2-3-5] PASSED
test_calculator.py::test_add[10--5-5] PASSED
test_calculator.py::test_add[0-0-0] PASSED
```

### Example 5: Grouping tests with markers

**test_smoke.py**

```python
import pytest

@pytest.mark.smoke
def test_login():
    assert True

@pytest.mark.regression
def test_payment():
    assert True

@pytest.mark.smoke
def test_logout():
    assert True
```

Run only smoke tests:

```powershell
pytest test_smoke.py -m smoke -v
```

---

## Best Practices & Recommendations

### ✅ Do

| Practice                                      | Example                                                    |
| --------------------------------------------- | ---------------------------------------------------------- |
| **One assertion per test**              | One `assert` per function — easier to debug failures    |
| **Use descriptive test names**          | `test_login_with_valid_credentials()` not `test_1()`   |
| **Keep tests independent**              | Tests should not depend on each other's order              |
| **Use fixtures for setup**              | Put browser launch, DB connection in `@pytest.fixture`   |
| **Use parametrize for multiple inputs** | `@pytest.mark.parametrize` instead of copy-pasting tests |
| **Group with markers**                  | `@pytest.mark.smoke`, `@pytest.mark.regression`        |
| **Use `-v` for verbose output**       | `pytest -v` shows pass/fail per test                     |
| **Run a specific test**                 | `pytest test_file.py::test_name -v`                      |

### ❌ Avoid

| Anti-pattern                                  | Why                                                           |
| --------------------------------------------- | ------------------------------------------------------------- |
| **Test files without `test_` prefix** | PyTest won't discover them                                    |
| **Relying on test order**               | Tests may run in any order — each must be self-contained     |
| **Hardcoding credentials**              | Use `.env` files and `os.getenv()`                        |
| **Print statements for debugging**      | Use `pytest -s` to see prints, or better — use `logging` |
| **Ignoring test isolation**             | One test modifying global state can break another test        |

### Recommended Project Structure

```
project/
├── src/                    # Application code
│   └── calculator.py
├── tests/                  # Test files
│   ├── test_calculator.py
│   ├── test_login.py
│   └── conftest.py         # Shared fixtures (auto-loaded by pytest)
├── .venv/                  # Virtual environment
├── pytest.ini              # PyTest configuration
└── requirements.txt
```

### Sample `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
```

---

## Common Commands Reference

| Command                            | Description                                         |
| ---------------------------------- | --------------------------------------------------- |
| `pytest`                         | Discover and run all tests                          |
| `pytest -v`                      | Verbose output (shows each test name)               |
| `pytest -s`                      | Show print() output                                 |
| `pytest -k "login"`              | Run tests matching "login" in the name              |
| `pytest -m smoke`                | Run only tests marked `@pytest.mark.smoke`        |
| `pytest --html=report.html`      | Generate HTML report (requires `pytest-html`)     |
| `pytest -n 4`                    | Run 4 tests in parallel (requires `pytest-xdist`) |
| `pytest --cov=src`               | Measure code coverage (requires `pytest-cov`)     |
| `pytest test_file.py::test_func` | Run a single test function                          |
