# API Reference: test_stock_reservation_entry.py

**Language**: Python

**Source**: `doctype/stock_reservation_entry/test_stock_reservation_entry.py`

---

## Classes

### TestStockReservationEntry

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_validate_stock_reservation_settings(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_get_available_qty_to_reserve(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_update_status(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_update_reserved_qty_in_voucher(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_cant_consume_reserved_stock(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_stock_reservation_against_sales_order(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 0, 'pick_serial_and_batch_based_on': 'FIFO', 'auto_create_serial_and_batch_bundle_for_outward': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_auto_reserve_serial_and_batch(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 1, 'pick_serial_and_batch_based_on': 'FIFO'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_stock_reservation_from_pick_list(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 1, 'pick_serial_and_batch_based_on': 'FIFO'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_stock_reservation_from_purchase_receipt(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 1, 'pick_serial_and_batch_based_on': 'FIFO', 'auto_reserve_stock_for_sales_order_on_purchase': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_consider_reserved_stock_while_cancelling_an_inward_transaction(self) → None

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 1, 'pick_serial_and_batch_based_on': 'FIFO'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`




## Functions

### create_items() → dict

**Returns**: `dict`



### create_material_receipt(items: dict, warehouse: str = '_Test Warehouse - _TC', qty: float = 100) → StockEntry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | dict | - | - |
| warehouse | str | '_Test Warehouse - _TC' | - |
| qty | float | 100 | - |

**Returns**: `StockEntry`



### cancel_all_stock_reservation_entries() → None

**Returns**: `None`



### make_stock_reservation_entry()

**Returns**: (none)


