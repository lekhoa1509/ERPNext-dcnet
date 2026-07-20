# API Reference: trial_balance.py

**Language**: Python

**Source**: `report/trial_balance/trial_balance.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### validate_filters(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_data(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_opening_balances(filters, ignore_is_opening, exchange_rate = None, ignore_reporting_currency = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| ignore_is_opening | None | - | - |
| exchange_rate | None | None | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### get_rootwise_opening_balances(filters, report_type, ignore_is_opening, exchange_rate = None, ignore_reporting_currency = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| report_type | None | - | - |
| ignore_is_opening | None | - | - |
| exchange_rate | None | None | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### get_opening_balance(doctype, filters, report_type, accounting_dimensions, period_closing_voucher = None, start_date = None, ignore_is_opening = 0, ignore_reporting_currency = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| filters | None | - | - |
| report_type | None | - | - |
| accounting_dimensions | None | - | - |
| period_closing_voucher | None | None | - |
| start_date | None | None | - |
| ignore_is_opening | None | 0 | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### calculate_values(accounts, gl_entries_by_account, opening_balances, show_net_values, ignore_is_opening = 0, exchange_rate = None, ignore_reporting_currency = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| gl_entries_by_account | None | - | - |
| opening_balances | None | - | - |
| show_net_values | None | - | - |
| ignore_is_opening | None | 0 | - |
| exchange_rate | None | None | - |
| ignore_reporting_currency | None | True | - |

**Returns**: (none)



### calculate_total_row(accounts, company_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| company_currency | None | - | - |

**Returns**: (none)



### accumulate_values_into_parents(accounts, accounts_by_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| accounts_by_name | None | - | - |

**Returns**: (none)



### prepare_data(accounts, filters, parent_children_map, company_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| filters | None | - | - |
| parent_children_map | None | - | - |
| company_currency | None | - | - |

**Returns**: (none)



### get_columns()

**Returns**: (none)



### prepare_opening_closing(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)



### hide_group_accounts(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)


