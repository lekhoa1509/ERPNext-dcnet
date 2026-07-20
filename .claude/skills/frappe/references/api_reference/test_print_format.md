# API Reference: test_print_format.py

**Language**: Python

**Source**: `printing/doctype/print_format/test_print_format.py`

---

## Classes

### TestPrintFormat

**Inherits from**: IntegrationTestCase

#### Methods

##### test_print_user(self, style = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| style | None | None | - |


##### test_print_user_standard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_print_user_modern(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_print_user_classic(self)

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



