# API Reference: loader.py

**Language**: Python

**Source**: `testing/loader.py`

---

## Classes

### FrappeTestLoader

**Inherits from**: unittest.TestLoader

#### Methods

##### recursive_load_suites_in_pymodule(self, suite)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suite | None | - | - |


##### load_testsuites_in_pymodule(self, file_modules)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| file_modules | None | - | - |


##### load_pymodule_for_files(self, files: list)

files: list of tuple of (Path, str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| files | list | - | - |


##### get_files(self, apps: list) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| apps | list | - | - |

**Returns**: `list`


##### discover_tests(self, params: TestParameters) → unittest.TestSuite

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| params | TestParameters | - | - |

**Returns**: `unittest.TestSuite`



