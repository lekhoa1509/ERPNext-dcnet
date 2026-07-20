# API Reference: deferred_revenue.py

**Language**: Python

**Source**: `deferred_revenue.py`

---

## Functions

### validate_service_stop_date(doc)

Validates service_stop_date for Purchase Invoice and Sales Invoice

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### build_conditions(process_type, account, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| process_type | None | - | - |
| account | None | - | - |
| company | None | - | - |

**Returns**: (none)



### convert_deferred_expense_to_expense(deferred_process, start_date = None, end_date = None, conditions = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| deferred_process | None | - | - |
| start_date | None | None | - |
| end_date | None | None | - |
| conditions | None | '' | - |

**Returns**: (none)



### convert_deferred_revenue_to_income(deferred_process, start_date = None, end_date = None, conditions = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| deferred_process | None | - | - |
| start_date | None | None | - |
| end_date | None | None | - |
| conditions | None | '' | - |

**Returns**: (none)



### get_booking_dates(doc, item, posting_date = None, prev_posting_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| item | None | - | - |
| posting_date | None | None | - |
| prev_posting_date | None | None | - |

**Returns**: (none)



### calculate_monthly_amount(doc, item, last_gl_entry, start_date, end_date, total_days, total_booking_days, account_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| item | None | - | - |
| last_gl_entry | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |
| total_days | None | - | - |
| total_booking_days | None | - | - |
| account_currency | None | - | - |

**Returns**: (none)



### calculate_amount(doc, item, last_gl_entry, total_days, total_booking_days, account_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| item | None | - | - |
| last_gl_entry | None | - | - |
| total_days | None | - | - |
| total_booking_days | None | - | - |
| account_currency | None | - | - |

**Returns**: (none)



### get_already_booked_amount(doc, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| item | None | - | - |

**Returns**: (none)



### book_deferred_income_or_expense(doc, deferred_process, posting_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| deferred_process | None | - | - |
| posting_date | None | None | - |

**Returns**: (none)



### process_deferred_accounting(posting_date = None)

Converts deferred income/expense into income/expense
Executed via background jobs on every month end

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | None | - |

**Returns**: (none)



### make_gl_entries(doc, credit_account, debit_account, against, amount, base_amount, posting_date, project, account_currency, cost_center, item, deferred_process = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| credit_account | None | - | - |
| debit_account | None | - | - |
| against | None | - | - |
| amount | None | - | - |
| base_amount | None | - | - |
| posting_date | None | - | - |
| project | None | - | - |
| account_currency | None | - | - |
| cost_center | None | - | - |
| item | None | - | - |
| deferred_process | None | None | - |

**Returns**: (none)



### send_mail(deferred_process)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| deferred_process | None | - | - |

**Returns**: (none)



### book_revenue_via_journal_entry(doc, credit_account, debit_account, amount, base_amount, posting_date, project, account_currency, cost_center, item, deferred_process = None, submit = 'No')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| credit_account | None | - | - |
| debit_account | None | - | - |
| amount | None | - | - |
| base_amount | None | - | - |
| posting_date | None | - | - |
| project | None | - | - |
| account_currency | None | - | - |
| cost_center | None | - | - |
| item | None | - | - |
| deferred_process | None | None | - |
| submit | None | 'No' | - |

**Returns**: (none)



### get_deferred_booking_accounts(doctype, voucher_detail_no, dr_or_cr)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| voucher_detail_no | None | - | - |
| dr_or_cr | None | - | - |

**Returns**: (none)



### _book_deferred_revenue_or_expense(item, via_journal_entry, submit_journal_entry, book_deferred_entries_based_on, prev_posting_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| via_journal_entry | None | - | - |
| submit_journal_entry | None | - | - |
| book_deferred_entries_based_on | None | - | - |
| prev_posting_date | None | None | - |

**Returns**: (none)


