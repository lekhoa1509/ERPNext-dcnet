# API Reference: invalid_ledger_entries.py

**Language**: Python

**Source**: `report/invalid_ledger_entries/invalid_ledger_entries.py`

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



### get_columns() → list[dict]

Return columns for the report.

One field definition per column, just like a DocType field definition.

**Returns**: `list[dict]`



### get_data(filters) → list[list]

Return data for the report.

The report data is a list of rows, with each row being a list of cell values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[list]`



### identify_cancelled_vouchers(active_vouchers: list[dict] | list | None = None) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| active_vouchers | list[dict] | list | None | None | - |

**Returns**: `list[dict]`



### validate_filters(filters: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: (none)



### build_query_filters(filters: dict | None = None) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: `list`



### get_active_vouchers_for_period(filters: dict | None = None) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: `list[dict]`


