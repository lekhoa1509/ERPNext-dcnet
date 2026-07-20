# API Reference: gross_and_net_profit_report.py

**Language**: Python

**Source**: `report/gross_and_net_profit_report/gross_and_net_profit_report.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_revenue(data, period_list, include_in_gross = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| period_list | None | - | - |
| include_in_gross | None | 1 | - |

**Returns**: (none)



### remove_parent_with_no_child(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### adjust_account_totals(data, period_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| period_list | None | - | - |

**Returns**: (none)



### set_total(node, value, complete_list, totals)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| node | None | - | - |
| value | None | - | - |
| complete_list | None | - | - |
| totals | None | - | - |

**Returns**: (none)



### get_profit(gross_income, gross_expense, period_list, company, profit_type, currency = None, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gross_income | None | - | - |
| gross_expense | None | - | - |
| period_list | None | - | - |
| company | None | - | - |
| profit_type | None | - | - |
| currency | None | None | - |
| consolidated | None | False | - |

**Returns**: (none)



### get_net_profit(non_gross_income, gross_income, gross_expense, non_gross_expense, period_list, company, currency = None, consolidated = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| non_gross_income | None | - | - |
| gross_income | None | - | - |
| gross_expense | None | - | - |
| non_gross_expense | None | - | - |
| period_list | None | - | - |
| company | None | - | - |
| currency | None | None | - |
| consolidated | None | False | - |

**Returns**: (none)


