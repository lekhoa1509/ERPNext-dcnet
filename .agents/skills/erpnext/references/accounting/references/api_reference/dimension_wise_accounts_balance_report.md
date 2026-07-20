# API Reference: dimension_wise_accounts_balance_report.py

**Language**: Python

**Source**: `report/dimension_wise_accounts_balance_report/dimension_wise_accounts_balance_report.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_data(filters, dimension_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| dimension_list | None | - | - |

**Returns**: (none)



### set_gl_entries_by_account(dimension_list, filters, account, gl_entries_by_account)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_list | None | - | - |
| filters | None | - | - |
| account | None | - | - |
| gl_entries_by_account | None | - | - |

**Returns**: (none)



### format_gl_entries(gl_entries_by_account, accounts_by_name, dimension_list, dimension_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| gl_entries_by_account | None | - | - |
| accounts_by_name | None | - | - |
| dimension_list | None | - | - |
| dimension_type | None | - | - |

**Returns**: (none)



### prepare_data(accounts, filters, company_currency, dimension_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| filters | None | - | - |
| company_currency | None | - | - |
| dimension_list | None | - | - |

**Returns**: (none)



### accumulate_values_into_parents(accounts, accounts_by_name, dimension_list)

accumulate children's values in parent accounts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| accounts_by_name | None | - | - |
| dimension_list | None | - | - |

**Returns**: (none)



### get_condition(dimension)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension | None | - | - |

**Returns**: (none)



### get_dimensions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_columns(dimension_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_list | None | - | - |

**Returns**: (none)


