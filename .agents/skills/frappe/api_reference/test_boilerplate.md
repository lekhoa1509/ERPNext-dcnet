# API Reference: test_boilerplate.py

**Language**: Python

**Source**: `tests/test_boilerplate.py`

---

## Classes

### TestBoilerPlate

**Inherits from**: unittest.TestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### create_app(self, hooks, no_git = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| hooks | None | - | - |
| no_git | None | False | - |


##### delete_test_app(cls, app_name)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| app_name | None | - | - |


##### get_user_input_stream(inputs)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| inputs | None | - | - |


##### test_simple_input_to_boilerplate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_invalid_inputs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_ci_yaml(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_app(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_app_without_git_init(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_paths(self, app_dir, app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| app_dir | None | - | - |
| app_name | None | - | - |


##### check_parsable_python_files(self, app_dir)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| app_dir | None | - | - |


##### test_new_patch_util(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



