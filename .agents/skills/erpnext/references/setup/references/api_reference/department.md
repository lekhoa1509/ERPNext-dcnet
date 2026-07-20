# API Reference: department.py

**Language**: Python

**Source**: `doctype/department/department.py`

---

## Classes

### Department

**Inherits from**: NestedSet

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, old, new, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old | None | - | - |
| new | None | - | - |
| merge | None | False | - |


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




## Functions

### on_doctype_update()

**Returns**: (none)



### get_abbreviated_name(name, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| company | None | - | - |

**Returns**: (none)



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


