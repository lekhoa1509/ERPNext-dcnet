# API Reference: discovery.py

**Language**: Python

**Source**: `testing/discovery.py`

---

## Classes

### TestRunnerError

Custom exception for test runner errors

**Inherits from**: Exception



## Functions

### discover_all_tests(apps: list[str], runner) → 'TestRunner'

Discover all tests for the specified app(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| apps | list[str] | - | - |
| runner | None | - | - |

**Returns**: `'TestRunner'`



### discover_doctype_tests(doctypes: list[str], runner, app: str, force: bool = False) → 'TestRunner'

Discover tests for the specified doctype(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list[str] | - | - |
| runner | None | - | - |
| app | str | - | - |
| force | bool | False | - |

**Returns**: `'TestRunner'`



### discover_module_tests(modules: list[str], runner, app: str) → 'TestRunner'

Discover tests for the specified test module

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| modules | list[str] | - | - |
| runner | None | - | - |
| app | str | - | - |

**Returns**: `'TestRunner'`



### _add_module_tests(runner, app: str, module: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| runner | None | - | - |
| app | str | - | - |
| module | str | - | - |

**Returns**: (none)


