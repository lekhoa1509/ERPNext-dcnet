# API Reference: financial_ratios.py

**Language**: Python

**Source**: `report/financial_ratios/financial_ratios.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### setup_filters(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_columns(period_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| period_list | None | - | - |

**Returns**: (none)



### get_ratios_data(filters, period_list, years)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| period_list | None | - | - |
| years | None | - | - |

**Returns**: (none)



### get_gl_data(filters, period_list, years)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| period_list | None | - | - |
| years | None | - | - |

**Returns**: (none)



### add_liquidity_ratios(data, years, current_asset, current_liability, quick_asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| years | None | - | - |
| current_asset | None | - | - |
| current_liability | None | - | - |
| quick_asset | None | - | - |

**Returns**: (none)



### add_solvency_ratios(data, years, total_asset, total_liability, net_sales, cogs, total_income, total_expense)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| years | None | - | - |
| total_asset | None | - | - |
| total_liability | None | - | - |
| net_sales | None | - | - |
| cogs | None | - | - |
| total_income | None | - | - |
| total_expense | None | - | - |

**Returns**: (none)



### add_turnover_ratios(data, years, period_list, filters, total_asset, net_sales, cogs, direct_expense)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| years | None | - | - |
| period_list | None | - | - |
| filters | None | - | - |
| total_asset | None | - | - |
| net_sales | None | - | - |
| cogs | None | - | - |
| direct_expense | None | - | - |

**Returns**: (none)



### update_balances(ratio_dict, total_dict, account_type, year, root_type_data, root_type, net_dict = None, total_net = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ratio_dict | None | - | - |
| total_dict | None | - | - |
| account_type | None | - | - |
| year | None | - | - |
| root_type_data | None | - | - |
| root_type | None | - | - |
| net_dict | None | None | - |
| total_net | None | 0 | - |

**Returns**: (none)



### avg_ratio_balance(account_type, period_list, precision, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_type | None | - | - |
| period_list | None | - | - |
| precision | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### calculate_ratio(value, denominator, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| denominator | None | - | - |
| precision | None | - | - |

**Returns**: (none)


