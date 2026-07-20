# API Reference: plant_floor.py

**Language**: Python

**Source**: `doctype/plant_floor/plant_floor.py`

---

## Classes

### PlantFloor

**Inherits from**: Document

#### Methods

##### make_stock_entry(self, kwargs)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| kwargs | None | - | - |


##### get_item_details(self, kwargs) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| kwargs | None | - | - |

**Returns**: `list[dict]`




## Functions

### get_stock_summary(warehouse, start = 0, item_code = None, item_group = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| start | None | 0 | - |
| item_code | None | None | - |
| item_group | None | None | - |

**Returns**: (none)



### get_stock_details(warehouse, start = 0, item_code = None, item_group = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |
| start | None | 0 | - |
| item_code | None | None | - |
| item_group | None | None | - |

**Returns**: (none)


