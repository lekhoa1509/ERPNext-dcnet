# API Reference: serial_no.py

**Language**: Python

**Source**: `doctype/serial_no/serial_no.py`

---

## Classes

### SerialNoCannotCreateDirectError

**Inherits from**: ValidationError



### SerialNoCannotCannotChangeError

**Inherits from**: ValidationError



### SerialNoWarehouseError

**Inherits from**: ValidationError



### SerialNo

**Inherits from**: StockController

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_maintenance_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_available_serial_nos(serial_no_series, qty) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no_series | None | - | - |
| qty | None | - | - |

**Returns**: `list[str]`



### get_new_serial_number(series)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| series | None | - | - |

**Returns**: (none)



### get_items_html(serial_nos, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### get_serial_nos(serial_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | None | - | - |

**Returns**: (none)



### get_serial_nos_from_sle_list(bundles)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bundles | None | - | - |

**Returns**: (none)



### clean_serial_no_string(serial_no: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_no | str | - | - |

**Returns**: `str`



### update_maintenance_status()

**Returns**: (none)



### auto_fetch_serial_number(qty: int, item_code: str, warehouse: str, posting_date: str | None = None, batch_nos: str | list[str] | None = None, for_doctype: str | None = None, exclude_sr_nos = None) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| qty | int | - | - |
| item_code | str | - | - |
| warehouse | str | - | - |
| posting_date | str | None | None | - |
| batch_nos | str | list[str] | None | None | - |
| for_doctype | str | None | None | - |
| exclude_sr_nos | None | None | - |

**Returns**: `list[str]`



### get_pos_reserved_serial_nos(filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### fetch_serial_numbers(filters, qty, do_not_include = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |
| qty | None | - | - |
| do_not_include | None | None | - |

**Returns**: (none)



### get_serial_nos_for_outward(kwargs)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| kwargs | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)


