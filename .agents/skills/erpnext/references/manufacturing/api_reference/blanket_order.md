# API Reference: blanket_order.py

**Language**: Python

**Source**: `doctype/blanket_order/blanket_order.py`

---

## Classes

### BlanketOrder

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_party_item_code(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_customer_items_ref(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_supplier_items_ref(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_ordered_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_order(source_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |

**Returns**: (none)



### validate_against_blanket_order(order_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| order_doc | None | - | - |

**Returns**: (none)



### update_doc(source_doc, target_doc, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_doc | None | - | - |
| target_doc | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)



### update_item(source, target, source_parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| source_parent | None | - | - |

**Returns**: (none)


