# API Reference: user_settings.py

**Language**: Python

**Source**: `model/utils/user_settings.py`

---

## Functions

### get_user_settings(doctype, for_update = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| for_update | None | False | - |

**Returns**: (none)



### update_user_settings(doctype, user_settings, for_update = False)

update user settings in cache

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user_settings | None | - | - |
| for_update | None | False | - |

**Returns**: (none)



### sync_user_settings()

Sync from cache to database (called asynchronously via the browser)

**Returns**: (none)



### save(doctype, user_settings)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| user_settings | None | - | - |

**Returns**: (none)



### get(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### update_user_settings_data(user_setting, fieldname, old, new, condition_fieldname = None, condition_values = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_setting | None | - | - |
| fieldname | None | - | - |
| old | None | - | - |
| new | None | - | - |
| condition_fieldname | None | None | - |
| condition_values | None | None | - |

**Returns**: (none)


