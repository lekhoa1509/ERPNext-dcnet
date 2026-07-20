# API Reference: process_period_closing_voucher.py

**Language**: Python

**Source**: `doctype/process_period_closing_voucher/process_period_closing_voucher.py`

---

## Classes

### ProcessPeriodClosingVoucher

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


##### populate_processing_tables(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_dates(self, start, end)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start | None | - | - |
| end | None | - | - |


##### generate_pcv_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_opening_balances_dates(self)

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

### start_pcv_processing(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### pause_pcv_processing(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### cancel_pcv_processing(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### resume_pcv_processing(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### update_default_dimensions(dimension_fields, gl_entry, dimension_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_fields | None | - | - |
| gl_entry | None | - | - |
| dimension_values | None | - | - |

**Returns**: (none)



### get_gle_for_pl_account(pcv, acc, balances, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pcv | None | - | - |
| acc | None | - | - |
| balances | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### get_gle_for_closing_account(pcv, dimension_balance, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pcv | None | - | - |
| dimension_balance | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### schedule_next_date(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### make_dict_json_compliant(dimension_wise_balance) → dict

convert tuple -> str
JSON doesn't support dictionary with tuple keys

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_wise_balance | None | - | - |

**Returns**: `dict`



### get_consolidated_gles(balances, report_type) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| balances | None | - | - |
| report_type | None | - | - |

**Returns**: `list`



### get_gl_entries(docname)

Calculate total closing balance of all P&L accounts across PCV start and end date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### calculate_balance_sheet_balance(docname)

Calculate total closing balance of all P&L accounts across PCV start and end date.
If it is first PCV, opening entries are also considered

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### get_p_l_closing_entries(pl_gles, pcv)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pl_gles | None | - | - |
| pcv | None | - | - |

**Returns**: (none)



### get_bs_closing_entries(dimension_wise_balance, pcv)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_wise_balance | None | - | - |
| pcv | None | - | - |

**Returns**: (none)



### get_closing_account_closing_entry(closing_account_gle, pcv)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| closing_account_gle | None | - | - |
| pcv | None | - | - |

**Returns**: (none)



### summarize_and_post_ledger_entries(docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | - | - |

**Returns**: (none)



### get_closing_entry(pcv, account, balances, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pcv | None | - | - |
| account | None | - | - |
| balances | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### get_dimensions()

**Returns**: (none)



### get_dimension_key(res)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| res | None | - | - |

**Returns**: (none)



### build_dimension_wise_balance_dict(gl_entries)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries | None | - | - |

**Returns**: (none)



### process_individual_date(docname: str, date, report_type, parentfield)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |
| date | None | - | - |
| report_type | None | - | - |
| parentfield | None | - | - |

**Returns**: (none)


