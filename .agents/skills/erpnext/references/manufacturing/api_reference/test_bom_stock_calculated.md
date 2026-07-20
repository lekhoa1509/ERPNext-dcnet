# API Reference: test_bom_stock_calculated.py

**Language**: Python

**Source**: `report/bom_stock_calculated/test_bom_stock_calculated.py`

---

## Classes

### TestBOMStockCalculated

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_stock_calculated(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_items()

**Returns**: (none)



### create_boms(fg_item, rm_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fg_item | None | - | - |
| rm_items | None | - | - |

**Returns**: (none)



### get_expected_data(bom, qty_to_make)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom | None | - | - |
| qty_to_make | None | - | - |

**Returns**: (none)



### update_bom_items(bom, uom, conversion_factor)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom | None | - | - |
| uom | None | - | - |
| conversion_factor | None | - | - |

**Returns**: (none)


