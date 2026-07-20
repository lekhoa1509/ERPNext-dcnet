# API Reference: audit_trail.py

**Language**: Python

**Source**: `core/doctype/audit_trail/audit_trail.py`

---

## Classes

### AuditTrail

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### compare_document(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_amended_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_diff_grid(self, i, diff)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| i | None | - | - |
| diff | None | - | - |


##### get_rows_added_removed_grid(self, i, diff, key, changed_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| i | None | - | - |
| diff | None | - | - |
| key | None | - | - |
| changed_dict | None | - | - |


##### get_rows_updated_grid(self, i, diff)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| i | None | - | - |
| diff | None | - | - |




## Functions

### get_field_label(fieldname, doctype, child_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |
| doctype | None | - | - |
| child_field | None | None | - |

**Returns**: (none)



### filter_fields_for_gridview(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)


