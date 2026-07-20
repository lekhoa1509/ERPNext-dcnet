# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Functions

### update_last_purchase_rate(doc, is_submit) → None

updates last_purchase_rate in item table for each item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| is_submit | None | - | - |

**Returns**: `None`



### validate_for_items(doc) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: `None`



### set_stock_levels(row) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: `None`



### validate_item_and_get_basic_data(row) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: `dict`



### validate_stock_item_warehouse(row, item) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |
| item | None | - | - |

**Returns**: `None`



### check_on_hold_or_closed_status(doctype, docname) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: `None`



### get_linked_material_requests(items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |

**Returns**: (none)


