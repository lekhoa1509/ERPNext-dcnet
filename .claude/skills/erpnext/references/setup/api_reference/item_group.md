# API Reference: item_group.py

**Language**: Python

**Source**: `doctype/item_group/item_group.py`

---

## Classes

### ItemGroup

**Inherits from**: NestedSet

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_item_tax(self)

Check whether Tax Rate is not entered twice for same Tax Type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_child_item_groups_key(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_group_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_child_item_groups(item_group_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_group_name | None | - | - |

**Returns**: (none)



### get_item_group_defaults(item, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| company | None | - | - |

**Returns**: (none)


