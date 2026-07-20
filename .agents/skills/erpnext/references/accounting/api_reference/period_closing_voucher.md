# API Reference: period_closing_voucher.py

**Language**: Python

**Source**: `doctype/period_closing_voucher/period_closing_voucher.py`

---

## Classes

### PeriodClosingVoucher

**Inherits from**: AccountsController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_start_and_end_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_previous_year_closed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### block_if_future_closing_voucher_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_future_closing_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_closing_account_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_closing_account_currency(self)

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


##### cancel_process_pcv_docs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_pcv_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gle_for_pl_account(self, acc, balances, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| acc | None | - | - |
| balances | None | - | - |
| dimensions | None | - | - |


##### get_gle_for_closing_account(self, dimension_balance, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| dimension_balance | None | - | - |
| dimensions | None | - | - |


##### update_default_dimensions(self, gl_entry, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entry | None | - | - |
| dimensions | None | - | - |


##### get_account_balances_based_on_dimensions(self, report_type)

Get balance for dimension-wise pl accounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_type | None | - | - |


##### get_accounting_dimension_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gl_entries_for_current_period(self, report_type, only_opening_entries = False, as_iterator = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report_type | None | - | - |
| only_opening_entries | None | False | - |
| as_iterator | None | False | - |


##### set_account_balance_dict(self, gle, acc_bal_dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gle | None | - | - |
| acc_bal_dict | None | - | - |


##### get_key(self, gle)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gle | None | - | - |


##### get_account_closing_balances(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_closing_entries_for_pl_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_closing_entries_for_balance_sheet_accounts(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_closing_entry(self, account, balances, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account | None | - | - |
| balances | None | - | - |
| dimensions | None | - | - |


##### get_closing_entries_for_closing_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_first_period_closing_voucher(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel_gl_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gle_count_against_current_pcv(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### process_gl_and_closing_entries(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### process_cancellation(voucher_type, voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | None | - | - |
| voucher_no | None | - | - |

**Returns**: (none)



### delete_closing_entries(voucher_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_no | None | - | - |

**Returns**: (none)



### get_period_start_end_date(fiscal_year, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_previous_closed_period_in_current_year(fiscal_year, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fiscal_year | None | - | - |
| company | None | - | - |

**Returns**: (none)


