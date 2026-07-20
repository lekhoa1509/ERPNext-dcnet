# API Reference: pos_profile.py

**Language**: Python

**Source**: `doctype/pos_profile/pos_profile.py`

---

## Classes

### POSProfile

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_accounting_dimensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_disabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_default_profile(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_all_link_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_groups(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_payment_methods(self)

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


##### set_defaults(self, include_current_pos = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| include_current_pos | None | True | - |




## Functions

### get_item_groups(pos_profile)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |

**Returns**: (none)



### get_permitted_nodes(group_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_type | None | - | - |

**Returns**: (none)



### get_child_nodes(group_type, root)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| group_type | None | - | - |
| root | None | - | - |

**Returns**: (none)



### pos_profile_query(doctype, txt, searchfield, start, page_len, filters)

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



### set_default_profile(pos_profile, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pos_profile | None | - | - |
| company | None | - | - |

**Returns**: (none)


