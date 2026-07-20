# API Reference: stock_ageing.py

**Language**: Python

**Source**: `report/stock_ageing/stock_ageing.py`

---

## Classes

### FIFOSlots

Returns FIFO computed slots of inwarded stock as per date.

**Inherits from**: (none)

#### Methods

##### __init__(self, filters: dict | None = None, sle: list | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | dict | None | None | - |
| sle | list | None | None | - |


##### generate(self) → dict

Returns dict of the foll.g structure:
Key = Item A / (Item A, Warehouse A)
Key: {
        'details' -> Dict: ** item details **,
        'fifo_queue' -> List: ** list of lists containing entries/slots for existing stock,
                consumed/updated and maintained via FIFO. **
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`


##### uppercase_serial_nos(self, serial_nos)

Convert serial nos to uppercase for uniformity.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| serial_nos | None | - | - |


##### __init_key_stores(self, row: dict) → tuple

Initialise keys and FIFO Queue.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | dict | - | - |

**Returns**: `tuple`


##### __compute_incoming_stock(self, row: dict, fifo_queue: list, transfer_key: tuple, serial_nos: list)

Update FIFO Queue on inward stock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | dict | - | - |
| fifo_queue | list | - | - |
| transfer_key | tuple | - | - |
| serial_nos | list | - | - |


##### __compute_outgoing_stock(self, row: dict, fifo_queue: list, transfer_key: tuple, serial_nos: list)

Update FIFO Queue on outward stock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | dict | - | - |
| fifo_queue | list | - | - |
| transfer_key | tuple | - | - |
| serial_nos | list | - | - |


##### __adjust_incoming_transfer_qty(self, transfer_data: dict, fifo_queue: list, row: dict)

Add previously removed stock back to FIFO Queue.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| transfer_data | dict | - | - |
| fifo_queue | list | - | - |
| row | dict | - | - |


##### __update_balances(self, row: dict, key: tuple | str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | dict | - | - |
| key | tuple | str | - | - |


##### __aggregate_details_by_item(self, wh_wise_data: dict) → dict

Aggregate Item-Wh wise data into single Item entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| wh_wise_data | dict | - | - |

**Returns**: `dict`


##### __get_stock_ledger_entries(self) → Iterator[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `Iterator[dict]`


##### __get_bundle_wise_serial_nos(self) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict`


##### __get_item_query(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### __get_warehouse_conditions(self, sle, sle_query) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sle | None | - | - |
| sle_query | None | - | - |

**Returns**: `str`




## Functions

### execute(filters: Filters = None) → tuple

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | None | - |

**Returns**: `tuple`



### format_report_data(filters: Filters, item_details: dict, to_date: str) → list[dict]

Returns ordered, formatted data with ranges.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |
| item_details | dict | - | - |
| to_date | str | - | - |

**Returns**: `list[dict]`



### check_and_replace_valuations_if_moving_average(range_values, item_valuation_method, valuation_rate, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| range_values | None | - | - |
| item_valuation_method | None | - | - |
| valuation_rate | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_average_age(fifo_queue: list, to_date: str) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fifo_queue | list | - | - |
| to_date | str | - | - |

**Returns**: `float`



### get_range_age(filters: Filters, fifo_queue: list, to_date: str, item_dict: dict) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |
| fifo_queue | list | - | - |
| to_date | str | - | - |
| item_dict | dict | - | - |

**Returns**: `list`



### get_columns(filters: Filters) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |

**Returns**: `list[dict]`



### get_chart_data(data: list, filters: Filters) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | list | - | - |
| filters | Filters | - | - |

**Returns**: `dict`



### setup_ageing_columns(filters: Filters, range_columns: list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | Filters | - | - |
| range_columns | list | - | - |

**Returns**: (none)



### add_column(range_columns: list, label: str, fieldname: str, fieldtype: str = 'Float', width: int = 140)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| range_columns | list | - | - |
| label | str | - | - |
| fieldname | str | - | - |
| fieldtype | str | 'Float' | - |
| width | int | 140 | - |

**Returns**: (none)



### add_to_fifo_queue(slot)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| slot | None | - | - |

**Returns**: (none)


