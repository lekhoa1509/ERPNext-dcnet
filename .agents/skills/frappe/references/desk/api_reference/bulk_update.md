# API Reference: bulk_update.py

**Language**: Python

**Source**: `doctype/bulk_update/bulk_update.py`

---

## Classes

### BulkUpdate

**Inherits from**: Document

#### Methods

##### bulk_update(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### submit_cancel_or_update_docs(doctype, docnames, action = 'submit', data = None, task_id = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docnames | None | - | - |
| action | None | 'submit' | - |
| data | None | None | - |
| task_id | None | None | - |

**Returns**: (none)



### _bulk_action(doctype, docnames, action, data, task_id = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docnames | None | - | - |
| action | None | - | - |
| data | None | - | - |
| task_id | None | None | - |

**Returns**: (none)


