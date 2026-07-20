# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Classes

### InvalidWarehouseCompany

**Inherits from**: frappe.ValidationError



### PendingRepostingError

**Inherits from**: frappe.ValidationError



## Functions

### get_stock_value_from_bin(warehouse = None, item_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | None | - |
| item_code | None | None | - |

**Returns**: (none)



### get_stock_value_on(warehouses: list | str | None = None, posting_date: str | None = None, item_code: str | None = None, company: str | None = None) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouses | list | str | None | None | - |
| posting_date | str | None | None | - |
| item_code | str | None | None | - |
| company | str | None | None | - |

**Returns**: `float`



### get_stock_balance(item_code, warehouse, posting_date = None, posting_time = None, with_valuation_rate = False, with_serial_no = False, inventory_dimensions_dict = None)

Returns stock balance quantity at given warehouse on given posting date or current date.

If `with_valuation_rate` is True, will return tuple (qty, rate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| posting_date | None | None | - |
| posting_time | None | None | - |
| with_valuation_rate | None | False | - |
| with_serial_no | None | False | - |
| inventory_dimensions_dict | None | None | - |

**Returns**: (none)



### get_serial_nos_data(serial_nos)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |

**Returns**: (none)



### get_latest_stock_qty(item_code, warehouse = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | None | - |

**Returns**: (none)



### get_latest_stock_balance()

**Returns**: (none)



### get_bin(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_or_make_bin(item_code: str, warehouse: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |

**Returns**: `str`



### _create_bin(item_code, warehouse)

Create a bin and take care of concurrent inserts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_incoming_rate(args, raise_error_if_no_rate = True)

Get Incoming Rate based on valuation method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| raise_error_if_no_rate | None | True | - |

**Returns**: (none)



### get_avg_purchase_rate(serial_nos)

get average value of serial numbers

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |

**Returns**: (none)



### get_valuation_method(item_code, company = None)

get valuation method from item or default

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | None | - |

**Returns**: (none)



### get_fifo_rate(previous_stock_queue, qty)

get FIFO (average) Rate from Queue

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| previous_stock_queue | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### get_lifo_rate(previous_stock_queue, qty)

get LIFO (average) Rate from Queue

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| previous_stock_queue | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### _get_fifo_lifo_rate(previous_stock_queue, qty, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| previous_stock_queue | None | - | - |
| qty | None | - | - |
| method | None | - | - |

**Returns**: (none)



### get_valid_serial_nos(sr_nos, qty = 0, item_code = '')

split serial nos, validate and return list of valid serial nos

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sr_nos | None | - | - |
| qty | None | 0 | - |
| item_code | None | '' | - |

**Returns**: (none)



### validate_warehouse_company(warehouse, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| company | None | - | - |

**Returns**: (none)



### is_group_warehouse(warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |

**Returns**: (none)



### validate_disabled_warehouse(warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |

**Returns**: (none)



### update_included_uom_in_report(columns, result, include_uom, conversion_factors)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| result | None | - | - |
| include_uom | None | - | - |
| conversion_factors | None | - | - |

**Returns**: (none)



### add_additional_uom_columns(columns, result, include_uom, conversion_factors)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| columns | None | - | - |
| result | None | - | - |
| include_uom | None | - | - |
| conversion_factors | None | - | - |

**Returns**: (none)



### get_incoming_outgoing_rate_for_cancel(item_code, voucher_type, voucher_no, voucher_detail_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| voucher_type | None | - | - |
| voucher_no | None | - | - |
| voucher_detail_no | None | - | - |

**Returns**: (none)



### is_reposting_item_valuation_in_progress()

**Returns**: (none)



### check_pending_reposting(posting_date: str, company: str | None = None, throw_error: bool = True) → bool

Check if there are pending reposting job till the specified posting date.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | str | - | - |
| company | str | None | None | - |
| throw_error | bool | True | - |

**Returns**: `bool`



### scan_barcode(search_value: str, ctx: dict | str | None = None) → BarcodeScanResult

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| search_value | str | - | - |
| ctx | dict | str | None | None | - |

**Returns**: `BarcodeScanResult`



### _update_item_info(scan_result: dict[str, str | None], ctx: dict | None = None) → dict[str, str | None]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scan_result | dict[str, str | None] | - | - |
| ctx | dict | None | None | - |

**Returns**: `dict[str, str | None]`



### get_combine_datetime(posting_date, posting_time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| posting_date | None | - | - |
| posting_time | None | - | - |

**Returns**: (none)



### get_default_stock_uom() → str | None

**Returns**: `str | None`



### set_cache(data: BarcodeScanResult)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | BarcodeScanResult | - | - |

**Returns**: (none)



### get_cache() → BarcodeScanResult | None

**Returns**: `BarcodeScanResult | None`


