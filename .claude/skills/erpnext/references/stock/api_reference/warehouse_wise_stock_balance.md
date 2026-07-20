# API Reference: warehouse_wise_stock_balance.py

**Language**: Python

**Source**: `report/warehouse_wise_stock_balance/warehouse_wise_stock_balance.py`

---

## Classes

### StockBalanceFilter

**Inherits from**: TypedDict



## Functions

### execute(filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: (none)



### get_warehouse_wise_balance(filters: StockBalanceFilter) → list[SLEntry]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | StockBalanceFilter | - | - |

**Returns**: `list[SLEntry]`



### get_warehouses(report_filters: StockBalanceFilter)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| report_filters | StockBalanceFilter | - | - |

**Returns**: (none)



### get_data(filters: StockBalanceFilter)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | StockBalanceFilter | - | - |

**Returns**: (none)



### update_indent(warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouses | None | - | - |

**Returns**: (none)



### set_balance_in_parent(warehouses)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouses | None | - | - |

**Returns**: (none)



### get_columns(filters: StockBalanceFilter) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | StockBalanceFilter | - | - |

**Returns**: `list[dict]`



### add_indent(warehouse, indent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| indent | None | - | - |

**Returns**: (none)



### update_balance(warehouse, balance)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| balance | None | - | - |

**Returns**: (none)


