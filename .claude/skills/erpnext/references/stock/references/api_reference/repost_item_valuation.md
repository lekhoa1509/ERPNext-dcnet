# API Reference: repost_item_valuation.py

**Language**: Python

**Source**: `doctype/repost_item_valuation/repost_item_valuation.py`

---

## Classes

### RepostItemValuation

**Inherits from**: Document

#### Methods

##### clear_old_logs(days = None)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | None | - |


##### on_discard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### repost_now(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_repost_only_accounting_ledgers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_recreate_stock_ledgers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_period_closing_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_recreate_stock_ledgers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_closing_stock_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_max_period_closing_date(company)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |


##### validate_accounts_freeze(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_field_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_company(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_status(self, status = None, write = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | None | - |
| write | None | True | - |


##### clear_attachment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

During tests reposts are executed immediately.

Exceptions:
        1. "Repost Item Valuation" document has self.flags.dont_run_in_test
        2. global flag frappe.flags.dont_execute_stock_reposts is set

        These flags are useful for asserting real time behaviour like quantity updates.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_pending_repost_against_cancelled_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### restart_reposting(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### skipped_similar_reposts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### deduplicate_similar_repost(self)

Deduplicate similar reposts based on item-warehouse-posting combination.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### recreate_stock_ledger_entries(self)

Recreate Stock Ledger Entries for the transaction.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### bulk_restart_reposting(names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### repost(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### remove_attached_file(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### repost_sl_entries(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### repost_gl_entries(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### _get_directly_dependent_vouchers(doc)

Get stock vouchers that are directly affected by reposting
i.e. any one item-warehouse is present in the stock transaction

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### notify_error_to_stock_managers(doc, traceback)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| traceback | None | - | - |

**Returns**: (none)



### get_recipients()

**Returns**: (none)



### run_parallel_reposting()

**Returns**: (none)



### repost_entries()

**Returns**: (none)



### execute_reposting_entry(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_repost_item_valuation_entries()

**Returns**: (none)



### in_configured_timeslot(repost_settings = None, current_time = None)

Check if current time is in configured timeslot for reposting.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| repost_settings | None | None | - |
| current_time | None | None | - |

**Returns**: (none)



### execute_repost_item_valuation()

Execute repost item valuation via scheduler.

**Returns**: (none)



### make_reposting_for_accounting_ledgers(transactions, company, repost_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transactions | None | - | - |
| company | None | - | - |
| repost_doc | None | - | - |

**Returns**: (none)


