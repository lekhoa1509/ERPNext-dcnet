# API Reference: repost_accounting_ledger.py

**Language**: Python

**Source**: `doctype/repost_accounting_ledger/repost_accounting_ledger.py`

---

## Classes

### RepostAccountingLedger

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_deferred_accounting(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_for_closed_fiscal_year(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_vouchers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_existing_ledger_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_preview_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_preview(self)

**Decorators**: `@frappe.whitelist()`

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

### start_repost(account_repost_doc = str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_repost_doc | None | str | - |

**Returns**: `None`



### get_allowed_types_from_settings(child_doc: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_doc | bool | False | - |

**Returns**: (none)



### get_child_docs(doc: list) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | list | - | - |

**Returns**: `list`



### validate_docs_for_deferred_accounting(sales_docs, purchase_docs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_docs | None | - | - |
| purchase_docs | None | - | - |

**Returns**: (none)



### validate_docs_for_voucher_types(doc_voucher_types)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_voucher_types | None | - | - |

**Returns**: (none)



### get_repost_allowed_types(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)


