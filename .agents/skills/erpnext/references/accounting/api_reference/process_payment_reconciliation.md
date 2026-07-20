# API Reference: process_payment_reconciliation.py

**Language**: Python

**Source**: `doctype/process_payment_reconciliation/process_payment_reconciliation.py`

---

## Classes

### ProcessPaymentReconciliation

**Inherits from**: Document

#### Methods

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


##### validate_receivable_payable_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_bank_cash_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

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




## Functions

### get_reconciled_count(docname: str | None = None) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | None | None | - |

**Returns**: `float`



### get_pr_instance(doc: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |

**Returns**: (none)



### is_job_running(job_name: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_name | str | - | - |

**Returns**: `bool`



### pause_job_for_doc(docname: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | None | None | - |

**Returns**: (none)



### trigger_job_for_doc(docname: str | None = None)

Trigger background job

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | None | None | - |

**Returns**: (none)



### trigger_reconciliation_for_queued_docs()

Will be called from Cron Job
Fetch queued docs and start reconciliation process for each one

**Returns**: (none)



### reconcile_based_on_filters(doc: None | str = None) → None

Identify current state of document and execute next tasks in background

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | str | None | - |

**Returns**: `None`



### get_next_allocation(log: str) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| log | str | - | - |

**Returns**: `list`



### fetch_and_allocate(doc: str) → None

Fetch Invoices and Payments based on filters applied. FIFO ordering is used for allocation.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |

**Returns**: `None`



### reconcile(doc: None | str = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | str | None | - |

**Returns**: `None`



### is_any_doc_running(for_filter: str | dict | None = None) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| for_filter | str | dict | None | None | - |

**Returns**: `str | None`



### get_filters_as_tuple(fields, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fields | None | - | - |
| doc | None | - | - |

**Returns**: (none)


