# API Reference: test_password_strength.py

**Language**: Python

**Source**: `tests/test_password_strength.py`

---

## Classes

### TestPasswordStrength

**Inherits from**: TestCase

#### Methods

##### test_long_password(self)

**Decorators**: `@retry(retry=retry_if_exception_type(AssertionError), stop=stop_after_attempt(3), wait=wait_fixed(0.5), reraise=True)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



