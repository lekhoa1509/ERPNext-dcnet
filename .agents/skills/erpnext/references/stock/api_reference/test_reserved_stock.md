# API Reference: test_reserved_stock.py

**Language**: Python

**Source**: `report/reserved_stock/test_reserved_stock.py`

---

## Classes

### TestReservedStock

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

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


##### test_reserved_stock_report(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0, 'enable_stock_reservation': 1, 'auto_reserve_serial_and_batch': 1, 'pick_serial_and_batch_based_on': 'FIFO'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



