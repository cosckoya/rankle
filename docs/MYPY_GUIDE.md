# Mypy Quick Start Guide for Rankle

**Updated:** January 20, 2026

---

## 🎯 Why Mypy?

Mypy catches bugs **before you run your code**. It's like having a second pair of eyes that checks every line for type errors.

### **Real-World Example:**

```python
# This bug only shows up at runtime (customer impact!)
def get_user_name(user: dict[str, Any]) -> str:
    return user["name"].upper()  # ❌ Crashes if name is None!

# Mypy catches it during development:
# error: Item "None" of "str | None" has no attribute "upper"
```

---

## 🚀 Quick Wins (0 Code Changes Required!)

### **1. Run Mypy:**

```bash
# Install mypy (in venv or with pipx)
pip install mypy

# Run on entire project
mypy rankle/

# Run on specific module
mypy rankle/core/scanner.py

# Run with verbose output
mypy rankle/ --show-error-context
```

### **2. What Mypy Catches Immediately:**

✅ **None-related crashes:**

```python
x: str | None = get_value()
print(x.upper())  # ❌ Mypy error: might be None
```

✅ **Type mismatches:**

```python
def process(count: int) -> None: pass
process("5")  # ❌ Mypy error: expected int, got str
```

✅ **Return type issues:**

```python
def get_score() -> int:
    return None  # ❌ Mypy error: expected int, got None
```

✅ **Dictionary key typos:**

```python
config = {"timeout": 30}
x = config["timout"]  # ❌ Would crash at runtime
# (With TypedDict, mypy catches this!)
```

---

## 📊 Current Mypy Configuration

Your `pyproject.toml` has **3 phases** of strictness:

### **Phase 1: ENABLED NOW ✅**

These are already active and catching bugs:

- `warn_return_any = true` - Catches functions returning `Any`
- `warn_unreachable = true` - Finds dead code
- `warn_no_return = true` - Functions missing return statements
- `strict_equality = true` - Prevents `== None` bugs
- `no_implicit_optional = true` - Requires explicit `| None`

**Action:** Run `mypy rankle/` now to see if there are any issues

### **Phase 2: GRADUAL ADOPTION 🎯**

Enable these per-module when ready:

```toml
[[tool.mypy.overrides]]
module = "rankle.core.scanner"
disallow_untyped_defs = true  # All functions must have type hints
```

**Action:** Start with `rankle.utils.confidence` (newest, cleanest code)

### **Phase 3: STRICT MODE 🚀**

Future goal - maximum type safety:

```toml
[tool.mypy]
strict = true  # All strict options enabled
```

**Action:** Long-term goal after Phase 2 is complete

---

## 🔧 Common Mypy Patterns for Rankle

### **Pattern 1: Optional Returns**

```python
# ❌ WRONG - Mypy complains
def find_user(id: int) -> User:
    user = db.get(id)
    return user  # ❌ Could be None!

# ✅ CORRECT - Explicit None handling
def find_user(id: int) -> User | None:
    user = db.get(id)
    return user  # ✅ Caller knows to check for None
```

### **Pattern 2: Type Narrowing**

```python
# ✅ Mypy understands if statements
def process(value: str | None) -> str:
    if value is None:
        return "default"
    # Mypy knows value is str here
    return value.upper()  # ✅ No error
```

### **Pattern 3: Type Guards**

```python
from typing import TypeGuard

def is_valid_config(data: dict[str, Any]) -> TypeGuard[dict[str, str]]:
    return all(isinstance(v, str) for v in data.values())

def process(config: dict[str, Any]) -> None:
    if is_valid_config(config):
        # Mypy knows config is dict[str, str] here
        x: str = config["key"]  # ✅ Safe
```

### **Pattern 4: Lazy Initialization (Rankle Pattern)**

```python
# Your current pattern - Mypy validates this!
class Scanner:
    def __init__(self):
        self._analyzer: Analyzer | None = None

    @property
    def analyzer(self) -> Analyzer:  # ✅ Not Analyzer | None
        if self._analyzer is None:
            self._analyzer = Analyzer()
        return self._analyzer  # ✅ Mypy verifies never None
```

---

## 🐛 How to Fix Common Mypy Errors

### **Error: "Incompatible return value type"**

```python
# Mypy says: error: Incompatible return value type (got "str | None", expected "str")
def get_name() -> str:
    return config.get("name")  # ❌ .get() returns str | None

# Fix 1: Change return type
def get_name() -> str | None:
    return config.get("name")  # ✅

# Fix 2: Provide default
def get_name() -> str:
    return config.get("name", "Unknown")  # ✅

# Fix 3: Assert non-None
def get_name() -> str:
    name = config.get("name")
    assert name is not None, "Name must be configured"
    return name  # ✅ Mypy knows it's not None
```

### **Error: "Item None has no attribute"**

```python
# Mypy says: error: Item "None" of "str | None" has no attribute "upper"
value: str | None = get_value()
print(value.upper())  # ❌

# Fix 1: Check for None
if value is not None:
    print(value.upper())  # ✅

# Fix 2: Use walrus + check
if (value := get_value()) is not None:
    print(value.upper())  # ✅

# Fix 3: Provide fallback
print((value or "default").upper())  # ✅
```

### **Error: "Missing return statement"**

```python
# Mypy says: error: Missing return statement
def calculate(x: int) -> int:
    if x > 0:
        return x * 2
    # ❌ Missing return for x <= 0

# Fix:
def calculate(x: int) -> int:
    if x > 0:
        return x * 2
    return 0  # ✅
```

---

## 🎓 Mypy Integration Workflow

### **Development Workflow:**

```bash
# 1. Write code with type hints
vim rankle/core/scanner.py

# 2. Run mypy before commit
mypy rankle/core/scanner.py

# 3. Fix issues
vim rankle/core/scanner.py

# 4. Verify clean
mypy rankle/core/scanner.py
# Success: no issues found in 1 source file

# 5. Commit
git add rankle/core/scanner.py
git commit -m "feat: Add new scanner feature (mypy clean)"
```

### **Pre-commit Hook:**

Add to `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pre-commit/mirrors-mypy
  rev: v1.8.0
  hooks:
    - id: mypy
      additional_dependencies: [types-requests]
      args: [--config-file=pyproject.toml]
```

### **CI/CD Integration:**

Add to GitHub Actions:

```yaml
- name: Type check with mypy
  run: |
    pip install mypy types-requests
    mypy rankle/ --config-file pyproject.toml
```

---

## 📈 Gradual Adoption Roadmap

### **Week 1: Baseline**

- ✅ Run `mypy rankle/` to see current state
- ✅ Fix any critical errors
- ✅ Add mypy to pre-commit hooks

### **Week 2-3: Core Modules**

```bash
# Enable strict checking on core modules
mypy rankle/core/ --disallow-untyped-defs
# Fix issues, then add to pyproject.toml
```

### **Week 4-5: Utils**

```bash
# Enable strict checking on utils
mypy rankle/utils/ --disallow-untyped-defs
```

### **Week 6-8: Detectors & Modules**

```bash
# Enable strict checking on remaining modules
mypy rankle/detectors/ --disallow-untyped-defs
mypy rankle/modules/ --disallow-untyped-defs
```

### **Week 9+: Strict Mode**

```toml
[tool.mypy]
strict = true  # 🚀 Maximum safety!
```

---

## 🔥 Quick Command Reference

```bash
# Basic check
mypy rankle/

# Check specific file
mypy rankle/core/scanner.py

# Show detailed errors
mypy rankle/ --show-error-context --pretty

# Generate coverage report
mypy rankle/ --html-report mypy-report/

# Check with stricter rules (test before enabling)
mypy rankle/core/ --disallow-untyped-defs

# Ignore specific line
x = something  # type: ignore[error-code]

# Show configuration
mypy --show-config

# Install type stubs for third-party libs
pip install types-requests types-beautifulsoup4
```

---

## 💡 Pro Tips

1. **Start small:** Enable strictness one module at a time
2. **Use `reveal_type()`:** Debug mypy's inference

   ```python
   from typing import reveal_type
   x = get_value()
   reveal_type(x)  # Mypy will print the inferred type
   ```

3. **Check CI logs:** Mypy output is more useful than runtime errors
4. **Use `cast()` sparingly:** Only when you know better than mypy
5. **Read error codes:** `mypy --show-error-codes` helps understand issues

---

## 📚 Resources

- **Mypy Docs:** <https://mypy.readthedocs.io/>
- **Mypy Cheat Sheet:** <https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>
- **Type Hints PEP:** <https://peps.python.org/pep-0484/>
- **Gradual Typing:** <https://mypy.readthedocs.io/en/stable/existing_code.html>

---

## ✅ Next Steps

1. **Install mypy:** `pip install mypy` (in venv)
2. **Run first check:** `mypy rankle/`
3. **Fix critical issues:** Start with core modules
4. **Add to CI:** Prevent regressions
5. **Enable strict mode:** Gradually per module

**Your type hints are already excellent! Mypy will catch the few remaining edge cases.** 🎯
