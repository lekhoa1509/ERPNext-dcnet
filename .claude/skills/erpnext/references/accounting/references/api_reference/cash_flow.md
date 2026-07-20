# API Reference: cash_flow.py

**Language**: Python

**Source**: `report/cash_flow/cash_flow.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_cash_flow_accounts()

**Returns**: (none)



### get_account_type_based_data(company, account_type, period_list, accumulated_values, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| account_type | None | - | - |
| period_list | None | - | - |
| accumulated_values | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_account_type_based_gl_data(company, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### get_start_date(period, accumulated_values, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period | None | - | - |
| accumulated_values | None | - | - |
| company | None | - | - |

**Returns**: (none)



### add_total_row_account(out, data, label, period_list, currency, summary_data, filters, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| data | None | - | - |
| label | None | - | - |
| period_list | None | - | - |
| currency | None | - | - |
| summary_data | None | - | - |
| filters | None | - | - |
| consolidated | None | False | - |

**Returns**: (none)



### show_opening_and_closing_balance(out, period_list, currency, net_change_in_cash, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |
| period_list | None | - | - |
| currency | None | - | - |
| net_change_in_cash | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_opening_balance(company, period_list, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| period_list | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_net_income(company, period_list, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| period_list | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_opening_range_using_fiscal_year(company, period_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| period_list | None | - | - |

**Returns**: (none)



### get_report_summary(summary_data, currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| summary_data | None | - | - |
| currency | None | - | - |

**Returns**: (none)



### get_chart_data(columns, data, currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| data | None | - | - |
| currency | None | - | - |

**Returns**: (none)


