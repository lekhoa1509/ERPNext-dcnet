# API Reference: test_stock_balance.py

**Language**: Python

**Source**: `report/stock_balance/test_stock_balance.py`

---

## Classes

### TestStockBalance

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### assertPartialDictEq(self, expected: dict[str, Any], actual: dict[str, Any])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expected | dict[str, Any] | - | - |
| actual | dict[str, Any] | - | - |


##### generate_stock_ledger(self, item_code: str, movements)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | str | - | - |
| movements | None | - | - |


##### assertInvariants(self, rows)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows | None | - | - |


##### test_basic_stock_balance(self)

Check very basic functionality and item info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_converted_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_child_warehouse_balances(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_show_item_attr(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### stock_balance(filters)

Get rows from stock balance report

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)


