# API Reference: pos_closing_entry.py

**Language**: Python

**Source**: `doctype/pos_closing_entry/pos_closing_entry.py`

---

## Classes

### POSClosingEntry

**Inherits from**: StatusUpdater

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_posting_date_and_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_invoice_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pos_opening_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_invoice_mode(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_pos_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pos_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_sales_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_sales_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### retry(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_opening_entry(self, for_cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| for_cancel | None | False | - |


##### update_sales_invoices_closing_entry(self, cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | False | - |


##### check_pce_is_cancellable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_cashiers(doctype, txt, searchfield, start, page_len, filters)

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



### get_invoices(start, end, pos_profile, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| end | None | - | - |
| pos_profile | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_payments(invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoices | None | - | - |

**Returns**: (none)



### get_taxes(invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoices | None | - | - |

**Returns**: (none)



### make_closing_entry_from_opening(opening_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| opening_entry | None | - | - |

**Returns**: (none)



### build_invoice_query(invoice_doctype, user, pos_profile, start, end)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_doctype | None | - | - |
| user | None | - | - |
| pos_profile | None | - | - |
| start | None | - | - |
| end | None | - | - |

**Returns**: (none)


