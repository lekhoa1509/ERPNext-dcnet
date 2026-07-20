# API Reference: bank_reconciliation_tool.py

**Language**: Python

**Source**: `doctype/bank_reconciliation_tool/bank_reconciliation_tool.py`

---

## Classes

### BankReconciliationTool

**Inherits from**: Document



## Functions

### get_bank_transactions(bank_account, from_date = None, to_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| from_date | None | None | - |
| to_date | None | None | - |

**Returns**: (none)



### get_account_balance(bank_account, till_date, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| till_date | None | - | - |
| company | None | - | - |

**Returns**: (none)



### update_bank_transaction(bank_transaction_name, reference_number, party_type = None, party = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transaction_name | None | - | - |
| reference_number | None | - | - |
| party_type | None | None | - |
| party | None | None | - |

**Returns**: (none)



### create_journal_entry_bts(bank_transaction_name, reference_number = None, reference_date = None, posting_date = None, entry_type = None, second_account = None, mode_of_payment = None, party_type = None, party = None, allow_edit = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transaction_name | None | - | - |
| reference_number | None | None | - |
| reference_date | None | None | - |
| posting_date | None | None | - |
| entry_type | None | None | - |
| second_account | None | None | - |
| mode_of_payment | None | None | - |
| party_type | None | None | - |
| party | None | None | - |
| allow_edit | None | None | - |

**Returns**: (none)



### create_payment_entry_bts(bank_transaction_name, reference_number = None, reference_date = None, party_type = None, party = None, posting_date = None, mode_of_payment = None, project = None, cost_center = None, allow_edit = None, company_bank_account = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transaction_name | None | - | - |
| reference_number | None | None | - |
| reference_date | None | None | - |
| party_type | None | None | - |
| party | None | None | - |
| posting_date | None | None | - |
| mode_of_payment | None | None | - |
| project | None | None | - |
| cost_center | None | None | - |
| allow_edit | None | None | - |
| company_bank_account | None | None | - |

**Returns**: (none)



### auto_reconcile_vouchers(bank_account, from_date = None, to_date = None, filter_by_reference_date = None, from_reference_date = None, to_reference_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| from_date | None | None | - |
| to_date | None | None | - |
| filter_by_reference_date | None | None | - |
| from_reference_date | None | None | - |
| to_reference_date | None | None | - |

**Returns**: (none)



### start_auto_reconcile(bank_transactions, from_date, to_date, filter_by_reference_date, from_reference_date, to_reference_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transactions | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| filter_by_reference_date | None | - | - |
| from_reference_date | None | - | - |
| to_reference_date | None | - | - |

**Returns**: (none)



### get_auto_reconcile_message(partially_reconciled, reconciled)

Returns alert message and indicator for auto reconciliation depending on result state.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| partially_reconciled | None | - | - |
| reconciled | None | - | - |

**Returns**: (none)



### reconcile_vouchers(bank_transaction_name, vouchers)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transaction_name | None | - | - |
| vouchers | None | - | - |

**Returns**: (none)



### get_linked_payments(bank_transaction_name, document_types = None, from_date = None, to_date = None, filter_by_reference_date = None, from_reference_date = None, to_reference_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_transaction_name | None | - | - |
| document_types | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| filter_by_reference_date | None | None | - |
| from_reference_date | None | None | - |
| to_reference_date | None | None | - |

**Returns**: (none)



### subtract_allocations(gl_account, vouchers)

Look up & subtract any existing Bank Transaction allocations

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_account | None | - | - |
| vouchers | None | - | - |

**Returns**: (none)



### get_allocated_amount(voucher_allocated_amounts, voucher, gl_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_allocated_amounts | None | - | - |
| voucher | None | - | - |
| gl_account | None | - | - |

**Returns**: (none)



### check_matching(bank_account, company, transaction, document_types = None, from_date = None, to_date = None, filter_by_reference_date = None, from_reference_date = None, to_reference_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| company | None | - | - |
| transaction | None | - | - |
| document_types | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| filter_by_reference_date | None | None | - |
| from_reference_date | None | None | - |
| to_reference_date | None | None | - |

**Returns**: (none)



### get_queries(bank_account, company, transaction, document_types = None, from_date = None, to_date = None, filter_by_reference_date = None, from_reference_date = None, to_reference_date = None, exact_match = None, common_filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| company | None | - | - |
| transaction | None | - | - |
| document_types | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| filter_by_reference_date | None | None | - |
| from_reference_date | None | None | - |
| to_reference_date | None | None | - |
| exact_match | None | None | - |
| common_filters | None | None | - |

**Returns**: (none)



### get_matching_queries(bank_account, company, transaction, document_types = None, exact_match = None, account_from_to = None, from_date = None, to_date = None, filter_by_reference_date = None, from_reference_date = None, to_reference_date = None, common_filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bank_account | None | - | - |
| company | None | - | - |
| transaction | None | - | - |
| document_types | None | None | - |
| exact_match | None | None | - |
| account_from_to | None | None | - |
| from_date | None | None | - |
| to_date | None | None | - |
| filter_by_reference_date | None | None | - |
| from_reference_date | None | None | - |
| to_reference_date | None | None | - |
| common_filters | None | None | - |

**Returns**: (none)



### get_bt_matching_query(exact_match, transaction)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exact_match | None | - | - |
| transaction | None | - | - |

**Returns**: (none)



### get_pe_matching_query(exact_match, account_from_to, transaction, from_date, to_date, filter_by_reference_date, from_reference_date, to_reference_date, common_filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exact_match | None | - | - |
| account_from_to | None | - | - |
| transaction | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| filter_by_reference_date | None | - | - |
| from_reference_date | None | - | - |
| to_reference_date | None | - | - |
| common_filters | None | - | - |

**Returns**: (none)



### get_je_matching_query(exact_match, transaction, from_date, to_date, filter_by_reference_date, from_reference_date, to_reference_date, common_filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exact_match | None | - | - |
| transaction | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| filter_by_reference_date | None | - | - |
| from_reference_date | None | - | - |
| to_reference_date | None | - | - |
| common_filters | None | - | - |

**Returns**: (none)



### get_si_matching_query(exact_match, currency, common_filters, transaction)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exact_match | None | - | - |
| currency | None | - | - |
| common_filters | None | - | - |
| transaction | None | - | - |

**Returns**: (none)



### get_pi_matching_query(exact_match, currency, common_filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| exact_match | None | - | - |
| currency | None | - | - |
| common_filters | None | - | - |

**Returns**: (none)


