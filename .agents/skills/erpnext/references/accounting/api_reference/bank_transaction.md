# API Reference: bank_transaction.py

**Language**: Python

**Source**: `doctype/bank_transaction/bank_transaction.py`

---

## Classes

### BankTransaction

**Inherits from**: Document

#### Methods

##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_currency(self)

Bank Transaction should be on the same currency as the Bank Account.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_references(self)

Make sure the same voucher is not allocated twice within the same Bank Transaction

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_allocated_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_old_payment_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_payment_entries(self, vouchers)

Add the vouchers with zero allocation. Save() will perform the allocations and clearance

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| vouchers | None | - | - |


##### allocate_payment_entries(self)

Refactored from bank reconciliation tool.
Non-zero allocations must be amended/cleared manually
Get the bank transaction amount (b) and remove as we allocate
For each payment_entry if allocated_amount == 0:
- get the amount already allocated against all transactions (t), need latest date
- get the voucher amount (from gl) (v)
- allocate (a = v - t)
    - a = 0: should already be cleared, so clear & remove payment_entry
    - 0 < a <= u: allocate a & clear
    - 0 < a, a > u: allocate u
    - 0 > a: Error: already over-allocated
- clear means: set the latest transaction date as clearance date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_payment_entries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_payment_entry(self, payment_entry)

Clear payment entry and clearance

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_entry | None | - | - |


##### delink_payment_entry(self, payment_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_entry | None | - | - |


##### clear_linked_payment_entry(self, payment_entry, clearance_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_entry | None | - | - |
| clearance_date | None | None | - |


##### update_linked_bank_transaction(self, bank_transaction_name, allocated_amount = None)

For when a second bank transaction has fixed another, e.g. refund

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bank_transaction_name | None | - | - |
| allocated_amount | None | None | - |


##### auto_set_party(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_included_fee(self)

The included_fee is only handled for withdrawals. An included_fee for a deposit, is not credited to the account and is
therefore outside of the deposit value and can be larger than the deposit itself.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### handle_excluded_fee(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_doctypes_for_bank_reconciliation()

Get Bank Reconciliation doctypes from all the apps

**Returns**: (none)



### get_clearance_details(transaction, payment_entry, bt_allocations, gl_entries, gl_bank_account)

There should only be one bank gl entry for a voucher, except for JE.
For JE, there can be multiple bank gl entries for the same account.
In this case, the allocable_amount will be the sum of amounts of all gl entries of the account.
There will be no gl entry for a Bank Transaction so return the unallocated amount.
Should only clear the voucher if all bank gl entries are allocated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transaction | None | - | - |
| payment_entry | None | - | - |
| bt_allocations | None | - | - |
| gl_entries | None | - | - |
| gl_bank_account | None | - | - |

**Returns**: (none)



### get_related_bank_gl_entries(docs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |

**Returns**: (none)



### get_total_allocated_amount(docs)

Gets the sum of allocations for a voucher on each bank GL account
along with the latest bank transaction date
NOTE: query may also include just saved vouchers/payments but with zero allocated_amount

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |

**Returns**: (none)



### get_reconciled_bank_transactions(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### remove_from_bank_transaction(doctype, docname)

Remove a (cancelled) voucher from all Bank Transactions.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)


