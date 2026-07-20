# API Reference: doctype_layout.py

**Language**: Python

**Source**: `custom/doctype/doctype_layout/doctype_layout.py`

---

## Classes

### DocTypeLayout

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sync_fields(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_fields(self, added_fields: list[str], doctype_fields: list['DocField']) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| added_fields | list[str] | - | - |
| doctype_fields | list['DocField'] | - | - |

**Returns**: `list[dict]`


##### remove_fields(self, removed_fields: list[str]) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| removed_fields | list[str] | - | - |

**Returns**: `list[dict]`



