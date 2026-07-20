# API Reference: prepared_report_analytics.py

**Language**: Python

**Source**: `core/report/prepared_report_analytics/prepared_report_analytics.py`

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



### get_columns(filters) → list[dict]

Return columns for the report.

One field definition per column, just like a DocType field definition.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[dict]`



### get_data(filters) → list[list]

Return data for the report.

The report data is a list of rows, with each row being a list of cell values.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[list]`


