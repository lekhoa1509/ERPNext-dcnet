# API Reference: test_modules.py

**Language**: Python

**Source**: `tests/test_modules.py`

---

## Classes

### TestUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_module_json_no_export(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_module_json(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_customizations(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_customizations_with_module_filter(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sync_customizations(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reload_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_export_doc(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_boilerplate(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### write_file(path, content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| content | None | - | - |

**Returns**: (none)



### delete_file(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### delete_path(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### temp_doctype()

**Returns**: (none)



### note_customizations()

**Returns**: (none)


