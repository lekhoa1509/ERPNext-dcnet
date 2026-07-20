# API Reference: budget_variance_report.py

**Language**: Python

**Source**: `report/budget_variance_report/budget_variance_report.py`

---

## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_budget_records(filters, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### build_budget_map(budget_records, filters)

Builds a nested dictionary structure aggregating budget and actual amounts.

Structure: {dimension_name: {account_name: {fiscal_year: {month_name: {"budget": amount, "actual": amount}}}}}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| budget_records | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_actual_transactions(dimension_name, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension_name | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_budget_distributions(budget)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| budget | None | - | - |

**Returns**: (none)



### get_months_in_range(start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start_date | None | - | - |
| end_date | None | - | - |

**Returns**: (none)



### build_report_data(budget_map, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| budget_map | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_periods(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_months_between(from_date, to_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_fiscal_years(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_budget_dimensions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### build_comparison_chart_data(filters, columns, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| columns | None | - | - |
| data | None | - | - |

**Returns**: (none)


