# API Reference: profitability_analysis.py

**Language**: Python

**Source**: `report/profitability_analysis/profitability_analysis.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_accounts_data(based_on, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| based_on | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_data(accounts, filters, based_on)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| filters | None | - | - |
| based_on | None | - | - |

**Returns**: (none)



### calculate_values(accounts, gl_entries_by_account, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| gl_entries_by_account | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### accumulate_values_into_parents(accounts, accounts_by_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| accounts_by_name | None | - | - |

**Returns**: (none)



### prepare_data(accounts, filters, total_row, parent_children_map, based_on)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| filters | None | - | - |
| total_row | None | - | - |
| parent_children_map | None | - | - |
| based_on | None | - | - |

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### set_gl_entries_by_account(company, from_date, to_date, based_on, gl_entries_by_account, ignore_closing_entries = False)

Returns a dict like { "account": [gl entries], ... }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| from_date | None | - | - |
| to_date | None | - | - |
| based_on | None | - | - |
| gl_entries_by_account | None | - | - |
| ignore_closing_entries | None | False | - |

**Returns**: (none)


