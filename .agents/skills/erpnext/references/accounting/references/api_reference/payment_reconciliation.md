# API Reference: payment_reconciliation.py

**Language**: Python

**Source**: `doctype/payment_reconciliation/payment_reconciliation.py`

---

## Classes

### PaymentReconciliation

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list(args)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |


##### get_count(args)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |


##### get_stats(args)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |


##### db_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_unreconciled_entries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_nonreconciled_payment_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_payment_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_jv_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_return_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_dr_or_cr_notes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_payment_entries(self, non_reconciled_payments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| non_reconciled_payments | None | - | - |


##### get_invoice_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_invoice_entries(self, non_reconciled_invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| non_reconciled_invoices | None | - | - |


##### get_difference_amount(self, payment_entry, invoice, allocated_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_entry | None | - | - |
| invoice | None | - | - |
| allocated_amount | None | - | - |


##### is_auto_process_enabled(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_difference_on_allocation_change(self, payment_entry, invoice, allocated_amount)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| payment_entry | None | - | - |
| invoice | None | - | - |
| allocated_amount | None | - | - |


##### allocate_entries(self, args)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### update_dimension_values_in_allocated_entries(self, res)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| res | None | - | - |


##### get_allocated_entry(self, pay, inv, allocated_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pay | None | - | - |
| inv | None | - | - |
| allocated_amount | None | - | - |


##### reconcile_allocations(self, skip_ref_details_update_for_pe = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| skip_ref_details_update_for_pe | None | False | - |


##### reconcile(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_payment_details(self, row, dr_or_cr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| dr_or_cr | None | - | - |


##### check_mandatory_to_fetch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invoice_exchange_map(self, invoices, payments)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoices | None | - | - |
| payments | None | - | - |


##### validate_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_dimensions_filter_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### build_qb_filter_conditions(self, get_invoices = False, get_return_invoices = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| get_invoices | None | False | - |
| get_return_invoices | None | False | - |


##### get_journal_filter_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### reconcile_dr_cr_note(dr_cr_notes, company, active_dimensions = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dr_cr_notes | None | - | - |
| company | None | - | - |
| active_dimensions | None | None | - |

**Returns**: (none)



### adjust_allocations_for_taxes(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_queries_for_dimension_filters(company: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | str | None | None | - |

**Returns**: (none)


