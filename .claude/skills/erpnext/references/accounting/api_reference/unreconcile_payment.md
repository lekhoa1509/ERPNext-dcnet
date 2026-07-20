# API Reference: unreconcile_payment.py

**Language**: Python

**Source**: `doctype/unreconcile_payment/unreconcile_payment.py`

---

## Classes

### UnreconcilePayment

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_allocations_from_payment(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_references(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### doc_has_references(doctype: str | None = None, docname: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | None | None | - |
| docname | str | None | None | - |

**Returns**: (none)



### get_linked_payments_for_doc(company: str | None = None, doctype: str | None = None, docname: str | None = None) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | None | None | - |
| doctype | str | None | None | - |
| docname | str | None | None | - |

**Returns**: `list`



### get_linked_advances(company, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### create_unreconcile_doc_for_selection(selections = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| selections | None | None | - |

**Returns**: (none)


