# API Reference: putaway_rule.py

**Language**: Python

**Source**: `doctype/putaway_rule/putaway_rule.py`

---

## Classes

### PutawayRule

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_rule(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_priority(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse_and_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_capacity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_stock_capacity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_available_putaway_capacity(rule)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rule | None | - | - |

**Returns**: (none)



### apply_putaway_rule(doctype, items, company, sync = None, purpose = None)

Applies Putaway Rule on line items.

items: List of Purchase Receipt/Stock Entry Items
company: Company in the Purchase Receipt/Stock Entry
doctype: Doctype to apply rule on
purpose: Purpose of Stock Entry
sync (optional): Sync with client side only for client side calls

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| items | None | - | - |
| company | None | - | - |
| sync | None | None | - |
| purpose | None | None | - |

**Returns**: (none)



### _items_changed(old, new, doctype: str) → bool

Check if any items changed by application of putaway rules.

If not, changing item table can have side effects since `name` items also changes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| old | None | - | - |
| new | None | - | - |
| doctype | str | - | - |

**Returns**: `bool`



### get_ordered_putaway_rules(item_code, company, source_warehouse = None)

Returns an ordered list of putaway rules to apply on an item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |
| source_warehouse | None | None | - |

**Returns**: (none)



### add_row(item, to_allocate, warehouse, updated_table, rule = None, serial_nos = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| to_allocate | None | - | - |
| warehouse | None | - | - |
| updated_table | None | - | - |
| rule | None | None | - |
| serial_nos | None | None | - |

**Returns**: (none)



### show_unassigned_items_message(items_not_accomodated)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items_not_accomodated | None | - | - |

**Returns**: (none)



### get_serial_nos_to_allocate(serial_nos, to_allocate)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |
| to_allocate | None | - | - |

**Returns**: (none)


