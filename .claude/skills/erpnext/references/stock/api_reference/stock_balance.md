# API Reference: stock_balance.py

**Language**: Python

**Source**: `stock_balance.py`

---

## Functions

### repost(only_actual = False, allow_negative_stock = False, allow_zero_rate = False, only_bin = False)

Repost everything!

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| only_actual | None | False | - |
| allow_negative_stock | None | False | - |
| allow_zero_rate | None | False | - |
| only_bin | None | False | - |

**Returns**: (none)



### repost_stock(item_code, warehouse, allow_zero_rate = False, only_actual = False, only_bin = False, allow_negative_stock = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| allow_zero_rate | None | False | - |
| only_actual | None | False | - |
| only_bin | None | False | - |
| allow_negative_stock | None | False | - |

**Returns**: (none)



### repost_actual_qty(item_code, warehouse, allow_zero_rate = False, allow_negative_stock = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| allow_zero_rate | None | False | - |
| allow_negative_stock | None | False | - |

**Returns**: (none)



### get_balance_qty_from_sle(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_reserved_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_indented_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_ordered_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_planned_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### update_bin_qty(item_code, warehouse, qty_dict = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| qty_dict | None | None | - |

**Returns**: (none)



### set_stock_balance_as_per_serial_no(item_code = None, posting_date = None, posting_time = None, fiscal_year = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| posting_date | None | None | - |
| posting_time | None | None | - |
| fiscal_year | None | None | - |

**Returns**: (none)


