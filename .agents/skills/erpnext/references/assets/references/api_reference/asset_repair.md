# API Reference: asset_repair.py

**Language**: Python

**Source**: `doctype/asset_repair/asset_repair.py`

---

## Classes

### AssetRepair

**Inherits from**: AccountsController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_purchase_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_purchase_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_purchase_invoice_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_expense_account(self, row)

Validate that the expense account exists in the purchase invoice for non-stock items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### validate_purchase_invoice_repair_cost(self, row)

Validate that repair cost doesn't exceed available amount.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### update_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_consumed_items_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_repair_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_total_repair_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_sabb(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_repair_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_asset_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_total_value_of_stock_consumed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### decrease_stock_quantity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_serial_no(self, stock_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| stock_item | None | - | - |


##### make_gl_entries(self, cancel = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| cancel | None | False | - |


##### get_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gl_entries_for_repair_cost(self, gl_entries, fixed_asset_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| fixed_asset_account | None | - | - |


##### get_gl_entries_for_consumed_items(self, gl_entries, fixed_asset_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| fixed_asset_account | None | - | - |


##### set_increase_in_asset_life(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_depreciation_note(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_asset_activity(self, subject = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| subject | None | None | - |




## Functions

### get_downtime(failure_date, completion_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| failure_date | None | - | - |
| completion_date | None | - | - |

**Returns**: (none)



### get_purchase_invoice(doctype, txt, searchfield, start, page_len, filters)

Get Purchase Invoices that have expense accounts for non-stock items.
Only returns invoices with at least one non-stock, non-fixed-asset item with an expense account.

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



### get_expense_accounts(doctype, txt, searchfield, start, page_len, filters)

Get expense accounts for non-stock (service) items from the purchase invoice.
Used as a query function for link fields.

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



### _get_expense_accounts_for_purchase_invoice(purchase_invoice: str) → list[str]

Get expense accounts for non-stock items from the purchase invoice.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_invoice | str | - | - |

**Returns**: `list[str]`



### get_unallocated_repair_cost(purchase_invoice: str, expense_account: str, exclude_asset_repair: str | None = None) → float

Calculate the unused repair cost for a purchase invoice and expense account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_invoice | str | - | - |
| expense_account | str | - | - |
| exclude_asset_repair | str | None | None | - |

**Returns**: `float`



### get_allocated_repair_cost(purchase_invoice: str, expense_account: str, exclude_asset_repair: str | None = None) → float

Get the total repair cost already allocated from submitted Asset Repairs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_invoice | str | - | - |
| expense_account | str | - | - |
| exclude_asset_repair | str | None | None | - |

**Returns**: `float`



### get_total_expense_amount(purchase_invoice: str, expense_account: str) → float

Get the total expense amount from GL entries for a purchase invoice and account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_invoice | str | - | - |
| expense_account | str | - | - |

**Returns**: `float`


