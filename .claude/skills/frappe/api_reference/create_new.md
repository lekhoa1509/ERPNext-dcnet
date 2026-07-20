# API Reference: create_new.py

**Language**: Python

**Source**: `model/create_new.py`

---

## Functions

### get_new_doc(doctype, parent_doc = None, parentfield = None, as_dict = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent_doc | None | None | - |
| parentfield | None | None | - |
| as_dict | None | False | - |

**Returns**: (none)



### make_new_doc(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### set_user_and_static_default_values(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_user_default_value(df, defaults, doctype_user_permissions, allowed_records, default_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| defaults | None | - | - |
| doctype_user_permissions | None | - | - |
| allowed_records | None | - | - |
| default_doc | None | - | - |

**Returns**: (none)



### get_static_default_value(df, doctype_user_permissions, allowed_records)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doctype_user_permissions | None | - | - |
| allowed_records | None | - | - |

**Returns**: (none)



### validate_value_via_user_permissions(df, doctype_user_permissions, allowed_records, user_default = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doctype_user_permissions | None | - | - |
| allowed_records | None | - | - |
| user_default | None | None | - |

**Returns**: (none)



### set_dynamic_default_values(doc, parent_doc, parentfield)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| parent_doc | None | - | - |
| parentfield | None | - | - |

**Returns**: (none)



### user_permissions_exist(df, doctype_user_permissions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doctype_user_permissions | None | - | - |

**Returns**: (none)



### get_default_based_on_another_field(df, user_permissions, parent_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| user_permissions | None | - | - |
| parent_doc | None | - | - |

**Returns**: (none)


