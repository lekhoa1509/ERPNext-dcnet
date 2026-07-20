# API Reference: opening_invoice_creation_tool.py

**Language**: Python

**Source**: `doctype/opening_invoice_creation_tool/opening_invoice_creation_tool.py`

---

## Classes

### OpeningInvoiceCreationTool

**Inherits from**: Document

#### Methods

##### onload(self)

Load the Opening Invoice summary

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_opening_invoice_summary(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### validate_mandatory_invoice_fields(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_party(self, party_type, party)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| party_type | None | - | - |
| party | None | - | - |


##### get_invoice_dict(self, row = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | None | - |


##### make_invoices(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### start_import(invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoices | None | - | - |

**Returns**: (none)



### publish(index, total, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| index | None | - | - |
| total | None | - | - |
| doctype | None | - | - |

**Returns**: (none)



### get_temporary_opening_account(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### prepare_invoice_summary(doctype, invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| invoices | None | - | - |

**Returns**: (none)



### get_item_dict()

**Returns**: (none)


