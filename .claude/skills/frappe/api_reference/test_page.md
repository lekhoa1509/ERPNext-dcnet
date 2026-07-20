# API Reference: test_page.py

**Language**: Python

**Source**: `core/doctype/page/test_page.py`

---

## Classes

### TestPage

**Inherits from**: IntegrationTestCase

#### Methods

##### test_naming(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_trashing(self)

**Decorators**: `@unittest.skipUnless(os.access(frappe.get_app_path('frappe'), os.W_OK), 'Only run if frappe app paths is writable')`, `@patch.dict(frappe.conf, {'developer_mode': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



