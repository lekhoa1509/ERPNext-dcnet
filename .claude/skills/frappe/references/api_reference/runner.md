# API Reference: runner.py

**Language**: Python

**Source**: `testing/runner.py`

---

## Classes

### TestRunner

**Inherits from**: unittest.TextTestRunner

#### Methods

##### __init__(self, stream = None, descriptions = True, verbosity = 1, failfast = False, buffer = True, resultclass = None, warnings = 'module')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stream | None | None | - |
| descriptions | None | True | - |
| verbosity | None | 1 | - |
| failfast | None | False | - |
| buffer | None | True | - |
| resultclass | None | None | - |
| warnings | None | 'module' | - |


##### iterRun(self) → Iterator[tuple[str, str, unittest.TestSuite]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Iterator[tuple[str, str, unittest.TestSuite]]`


##### _has_tests(self, suite)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suite | None | - | - |


##### _prepare_category(self, category, suite, app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| category | None | - | - |
| suite | None | - | - |
| app | None | - | - |


##### _apply_debug_decorators(self, suite)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suite | None | - | - |


##### _profile(self)

**Decorators**: `@contextlib.contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _iterate_suite(suite)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| suite | None | - | - |



