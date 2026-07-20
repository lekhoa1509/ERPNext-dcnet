# API Reference: sales_order_analysis.py

**Language**: Python

**Source**: `report/sales_order_analysis/sales_order_analysis.py`

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



### get_conditions(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### get_data(conditions, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| conditions | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_so_elapsed_time(data)

query SO's elapsed time till latest delivery note

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### prepare_data(data, so_elapsed_time, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| so_elapsed_time | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### prepare_chart_data(pending, completed)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pending | None | - | - |
| completed | None | - | - |

**Returns**: (none)



### get_columns(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)


