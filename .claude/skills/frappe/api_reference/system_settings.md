# API Reference: system_settings.py

**Language**: Python

**Source**: `core/doctype/system_settings/system_settings.py`

---

## Classes

### SystemSettings

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_otp_sms_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_user_pass_login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_backup_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_file_extensions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### update_last_reset_password_date()

**Returns**: (none)



### load()

**Returns**: (none)



### get_system_settings(key: str)

Return the value associated with the given `key` from System Settings DocType.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |

**Returns**: (none)



### clear_system_settings_cache()

**Returns**: (none)



### sync_system_settings()

**Returns**: (none)


