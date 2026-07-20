# API Reference: stock_reservation_entry.py

**Language**: Python

**Source**: `doctype/stock_reservation_entry/stock_reservation_entry.py`

---

## Classes

### StockReservationEntry

**Inherits from**: Document

#### Methods

##### validate(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### before_submit(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### on_submit(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### on_update_after_submit(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### on_cancel(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### before_cancel(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_reserved_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_unreserved_qty_in_sre(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_serial_batch_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_from_voucher_reservation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_amended_doc(self) → None

Raises an exception if document is amended.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_mandatory(self) → None

Raises an exception if mandatory fields are not set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_group_warehouse(self) → None

Raises an exception if `Warehouse` is a Group Warehouse.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_uom_is_integer(self) → None

Validates `Reserved Qty` with Stock UOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### set_reservation_based_on(self) → None

Sets `Reservation Based On` based on `Has Serial No` and `Has Batch No`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_reservation_based_on_qty(self) → None

Validates `Reserved Qty` when `Reservation Based On` is `Qty`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### auto_reserve_serial_and_batch(self, based_on: str | None = None) → None

Auto pick Serial and Batch Nos to reserve when `Reservation Based On` is `Serial and Batch`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| based_on | str | None | None | - |

**Returns**: `None`


##### validate_reservation_based_on_serial_and_batch(self) → None

Validates `Reserved Qty`, `Serial and Batch Nos` when `Reservation Based On` is `Serial and Batch`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### update_reserved_qty_in_voucher(self, reserved_qty_field: str = 'stock_reserved_qty', update_modified: bool = True) → None

Updates total reserved qty in the voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reserved_qty_field | str | 'stock_reserved_qty' | - |
| update_modified | bool | True | - |

**Returns**: `None`


##### update_reserved_qty_in_pick_list(self, reserved_qty_field: str = 'stock_reserved_qty', update_modified: bool = True) → None

Updates total reserved qty in the Pick List.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| reserved_qty_field | str | 'stock_reserved_qty' | - |
| update_modified | bool | True | - |

**Returns**: `None`


##### update_reserved_stock_in_bin(self) → None

Updates `Reserved Stock` in Bin.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### update_status(self, status: str | None = None, update_modified: bool = True) → None

Updates status based on Voucher Qty, Reserved Qty and Delivered Qty.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | str | None | None | - |
| update_modified | bool | True | - |

**Returns**: `None`


##### can_be_updated(self) → None

Raises an exception if `Stock Reservation Entry` is not allowed to be updated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### validate_with_allowed_qty(self, qty_to_be_reserved: float) → None

Validates `Reserved Qty` with `Max Reserved Qty`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| qty_to_be_reserved | float | - | - |

**Returns**: `None`


##### consume_serial_batch_for_material_transfer(self, row_wise_serial_batch)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_wise_serial_batch | None | - | - |




### StockReservation

**Inherits from**: (none)

#### Methods

##### __init__(self, doc, items = None, kwargs = None, notify = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| items | None | None | - |
| kwargs | None | None | - |
| notify | None | True | - |


##### initialize_fields(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### cancel_stock_reservation_entries(self, names = None) → None

Cancels Stock Reservation Entries for the Voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| names | None | None | - |

**Returns**: `None`


##### make_stock_reservation_entries(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_serial_batch(self, sre, serial_batch_bundles)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| sre | None | - | - |
| serial_batch_bundles | None | - | - |


##### throw_stock_not_exists_error(self, idx, item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| idx | None | - | - |
| item_code | None | - | - |
| warehouse | None | - | - |


##### get_available_qty_to_reserve(self, item_code, warehouse, ignore_sre = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| warehouse | None | - | - |
| ignore_sre | None | None | - |


##### transfer_reservation_entries_to(self, docnames, from_doctype, to_doctype, against_fg_item = None, qty_change = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docnames | None | - | - |
| from_doctype | None | - | - |
| to_doctype | None | - | - |
| against_fg_item | None | None | - |
| qty_change | None | None | - |


##### update_delivered_qty(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### make_stock_reservation_entry(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_reserved_entries(self, doctype, docnames, against_fg_item = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docnames | None | - | - |
| against_fg_item | None | None | - |


##### get_items_to_reserve(self, docnames, from_doctype, to_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docnames | None | - | - |
| from_doctype | None | - | - |
| to_doctype | None | - | - |




## Functions

### validate_stock_reservation_settings(voucher: object) → None

Raises an exception if `Stock Reservation` is not enabled or `Voucher Type` is not allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher | object | - | - |

**Returns**: `None`



### get_available_qty_to_reserve(item_code: str, warehouse: str, batch_no: str | None = None, ignore_sre = None) → float

Returns `Available Qty to Reserve (Actual Qty - Reserved Qty)` for Item, Warehouse and Batch combination.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| batch_no | str | None | None | - |
| ignore_sre | None | None | - |

**Returns**: `float`



### get_available_serial_nos_to_reserve(item_code: str, warehouse: str, has_batch_no: bool = False, ignore_sre = None) → list[tuple]

Returns Available Serial Nos to Reserve (Available Serial Nos - Reserved Serial Nos)` for Item, Warehouse and Batch combination.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| has_batch_no | bool | False | - |
| ignore_sre | None | None | - |

**Returns**: `list[tuple]`



### get_sre_reserved_qty_for_item_and_warehouse(item_code: str, warehouse: str | None = None) → float

Returns current `Reserved Qty` for Item and Warehouse combination.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | None | None | - |

**Returns**: `float`



### get_sre_reserved_qty_for_items_and_warehouses(item_code_list: list, warehouse_list: list | None = None) → dict

Returns a dict like {("item_code", "warehouse"): "reserved_qty", ... }.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code_list | list | - | - |
| warehouse_list | list | None | None | - |

**Returns**: `dict`



### get_sre_reserved_qty_details_for_voucher(voucher_type: str, voucher_no: str) → dict

Returns a dict like {"voucher_detail_no": "reserved_qty", ... }.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | - | - |
| voucher_no | str | - | - |

**Returns**: `dict`



### get_sre_reserved_warehouses_for_voucher(voucher_type: str, voucher_no: str, voucher_detail_no: str | None = None) → list

Returns a list of warehouses where the stock is reserved for the provided voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | - | - |
| voucher_no | str | - | - |
| voucher_detail_no | str | None | None | - |

**Returns**: `list`



### get_sre_reserved_qty_for_voucher_detail_no(item_code: str, voucher_type: str, voucher_no: str, voucher_detail_no: str, ignore_sre = None, warehouse = None, from_voucher_detail_no = None) → float

Returns `Reserved Qty` against the Voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| voucher_type | str | - | - |
| voucher_no | str | - | - |
| voucher_detail_no | str | - | - |
| ignore_sre | None | None | - |
| warehouse | None | None | - |
| from_voucher_detail_no | None | None | - |

**Returns**: `float`



### get_sre_reserved_serial_nos_details(item_code: str, warehouse: str, serial_nos: list | None = None) → dict

Returns a dict of `Serial No` reserved in Stock Reservation Entry. The dict is like {serial_no: sre_name, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| serial_nos | list | None | None | - |

**Returns**: `dict`



### get_sre_reserved_batch_nos_details(item_code: str, warehouse: str, batch_nos: list | None = None) → dict

Returns a dict of `Batch Qty` reserved in Stock Reservation Entry. The dict is like {batch_no: qty, ...}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |
| warehouse | str | - | - |
| batch_nos | list | None | None | - |

**Returns**: `dict`



### get_sre_details_for_voucher(voucher_type: str, voucher_no: str) → list[dict]

Returns a list of SREs for the provided voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | - | - |
| voucher_no | str | - | - |

**Returns**: `list[dict]`



### get_serial_batch_entries_for_voucher(sre_name: str) → list[dict]

Returns a list of `Serial and Batch Entries` for the provided voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sre_name | str | - | - |

**Returns**: `list[dict]`



### get_ssb_bundle_for_voucher(sre: dict) → object

Returns a new `Serial and Batch Bundle` against the provided SRE.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sre | dict | - | - |

**Returns**: `object`



### has_reserved_stock(voucher_type: str, voucher_no: str, voucher_detail_no: str | None = None) → bool

Returns True if there is any Stock Reservation Entry for the given voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | - | - |
| voucher_no | str | - | - |
| voucher_detail_no | str | None | None | - |

**Returns**: `bool`



### create_stock_reservation_entries_for_so_items(sales_order: object, items_details: list[dict] | None = None, from_voucher_type: Literal['Pick List', 'Purchase Receipt'] = None, notify = True) → None

Creates Stock Reservation Entries for Sales Order Items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sales_order | object | - | - |
| items_details | list[dict] | None | None | - |
| from_voucher_type | Literal['Pick List', 'Purchase Receipt'] | None | - |
| notify | None | True | - |

**Returns**: `None`



### cancel_stock_reservation_entries(voucher_type: str | None = None, voucher_no: str | None = None, voucher_detail_no: str | None = None, from_voucher_type: Literal['Pick List', 'Purchase Receipt'] = None, from_voucher_no: str | None = None, from_voucher_detail_no: str | None = None, sre_list: list | None = None, notify: bool = True) → None

Cancel Stock Reservation Entries.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | None | None | - |
| voucher_no | str | None | None | - |
| voucher_detail_no | str | None | None | - |
| from_voucher_type | Literal['Pick List', 'Purchase Receipt'] | None | - |
| from_voucher_no | str | None | None | - |
| from_voucher_detail_no | str | None | None | - |
| sre_list | list | None | None | - |
| notify | bool | True | - |

**Returns**: `None`



### get_stock_reservation_entries_for_voucher(voucher_type: str, voucher_no: str, voucher_detail_no: str | None = None, fields: list[str] | None = None, ignore_status: bool = False) → list[dict]

Returns list of Stock Reservation Entries against a Voucher.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| voucher_type | str | - | - |
| voucher_no | str | - | - |
| voucher_detail_no | str | None | None | - |
| fields | list[str] | None | None | - |
| ignore_status | bool | False | - |

**Returns**: `list[dict]`



### update_serial_batch_delivered_qty(row, name, is_cancelled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| name | None | - | - |
| is_cancelled | None | False | - |

**Returns**: (none)


