# API Reference: incorrect_serial_and_batch_bundle.py

**Language**: Python

**Source**: `report/incorrect_serial_and_batch_bundle/incorrect_serial_and_batch_bundle.py`

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



### get_unlinked_serial_batch_bundles(filters) → list[list]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[list]`



### get_linked_cancelled_sabb(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### fix_sabb_entries(selected_rows)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| selected_rows | None | - | - |

**Returns**: (none)


