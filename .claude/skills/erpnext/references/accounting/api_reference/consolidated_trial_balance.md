# API Reference: consolidated_trial_balance.py

**Language**: Python

**Source**: `report/consolidated_trial_balance/consolidated_trial_balance.py`

---

## Functions

### execute(filters: dict | None = None)

Return columns and data for the report.

This is the main entry point for the report. It accepts the filters as a
dictionary and should return columns and data. It is called by the framework
every time the report is refreshed or a filter is updated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: (none)



### validate_filters(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### validate_companies(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### sort_companies(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_data(filters) → list[list]

Return data for the report.

The report data is a list of rows, with each row being a list of cell values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[list]`



### get_company_wise_tb_data(filters, reporting_currency, ignore_reporting_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| reporting_currency | None | - | - |
| ignore_reporting_currency | None | - | - |

**Returns**: (none)



### prepare_companywise_tb_data(accounts, filters, parent_children_map, reporting_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| accounts | None | - | - |
| filters | None | - | - |
| parent_children_map | None | - | - |
| reporting_currency | None | - | - |

**Returns**: (none)



### calculate_total_row(data, reporting_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| reporting_currency | None | - | - |

**Returns**: (none)



### calculate_foreign_currency_translation_reserve(total_row, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| total_row | None | - | - |
| data | None | - | - |

**Returns**: (none)



### get_fctr_root_row_index(data)

Returns: index, root_type, parent_account

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### consolidate_trial_balance_data(data, tb_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| tb_data | None | - | - |

**Returns**: (none)



### get_reporting_currency(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### consolidate_gle_data(data, entry, tb_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| entry | None | - | - |
| tb_data | None | - | - |

**Returns**: (none)



### update_to_presentation_currency(data, from_currency, to_currency, date, ignore_reporting_currency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| from_currency | None | - | - |
| to_currency | None | - | - |
| date | None | - | - |
| ignore_reporting_currency | None | - | - |

**Returns**: (none)



### get_columns()

**Returns**: (none)


