# API Reference: warehouse.py

**Language**: Python

**Source**: `doctype/warehouse/warehouse.py`

---

## Classes

### Warehouse

**Inherits from**: NestedSet

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_nsm_model(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### warn_about_multiple_warehouse_account(self)

If Warehouse value is split across multiple accounts, warn.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_sle_exists(self, non_cancelled_only = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| non_cancelled_only | None | False | - |


##### check_if_child_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### convert_to_group_or_ledger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### convert_to_ledger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### convert_to_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unlink_from_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_children(doctype, parent = None, company = None, is_root = False, include_disabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | None | - |
| company | None | None | - |
| is_root | None | False | - |
| include_disabled | None | False | - |

**Returns**: (none)



### add_node()

**Returns**: (none)



### convert_to_group_or_ledger(docname = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | None | None | - |

**Returns**: (none)



### get_child_warehouses(warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |

**Returns**: (none)



### get_warehouses_based_on_account(account, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| company | None | None | - |

**Returns**: (none)



### apply_warehouse_filter(query, sle, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | None | - | - |
| sle | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_warehouses_for_reorder(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_accounts_where_value_is_booked(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)


