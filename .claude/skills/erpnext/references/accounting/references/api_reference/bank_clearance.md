# API Reference: bank_clearance.py

**Language**: Python

**Source**: `doctype/bank_clearance/bank_clearance.py`

---

## Classes

### BankClearance

**Inherits from**: Document

#### Methods

##### get_payment_entries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_clearance_date(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_payment_entries_for_bank_clearance(from_date, to_date, account, bank_account, include_reconciled_entries, include_pos_transactions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |
| account | None | - | - |
| bank_account | None | - | - |
| include_reconciled_entries | None | - | - |
| include_pos_transactions | None | - | - |

**Returns**: (none)



### validate_entry(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


