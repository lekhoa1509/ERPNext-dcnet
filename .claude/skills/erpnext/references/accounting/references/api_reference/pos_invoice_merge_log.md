# API Reference: pos_invoice_merge_log.py

**Language**: Python

**Source**: `doctype/pos_invoice_merge_log/pos_invoice_merge_log.py`

---

## Classes

### POSInvoiceMergeLog

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_pos_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pos_invoice_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### process_merging_into_sales_invoice(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### process_merging_into_credit_notes(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### distinguish_return_pos_invoices(self, data, sales_invoice_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |
| sales_invoice_doc | None | None | - |


##### merge_pos_invoice_into(self, invoice, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice | None | - | - |
| data | None | - | - |


##### get_new_sales_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_pos_invoices(self, invoice_docs, sales_invoice = '', credit_notes = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| invoice_docs | None | - | - |
| sales_invoice | None | '' | - |
| credit_notes | None | None | - |


##### serial_and_batch_bundle_reference_for_pos_invoice(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delink_serial_and_batch_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_serial_and_batch_bundles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_linked_invoices(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_all_unconsolidated_invoices()

**Returns**: (none)



### get_invoice_customer_map(pos_invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_invoices | None | - | - |

**Returns**: (none)



### split_invoices_by_accounting_dimension(pos_invoices)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_invoices | None | - | - |

**Returns**: (none)



### consolidate_pos_invoices(pos_invoices = None, closing_entry = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_invoices | None | None | - |
| closing_entry | None | None | - |

**Returns**: (none)



### unconsolidate_pos_invoices(closing_entry)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| closing_entry | None | - | - |

**Returns**: (none)



### split_invoices(invoices)

Splits invoices into multiple groups
Use-case:
If a serial no is sold and later it is returned
then split the invoices such that the selling entry is merged first and then the return entry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoices | None | - | - |

**Returns**: (none)



### create_merge_logs(invoice_by_customer, closing_entry = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| invoice_by_customer | None | - | - |
| closing_entry | None | None | - |

**Returns**: (none)



### cancel_merge_logs(merge_logs, closing_entry = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| merge_logs | None | - | - |
| closing_entry | None | None | - |

**Returns**: (none)



### enqueue_job(job)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | None | - | - |

**Returns**: (none)



### check_scheduler_status()

**Returns**: (none)



### get_error_message(message) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | None | - | - |

**Returns**: `str`


