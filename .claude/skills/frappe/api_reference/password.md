# API Reference: password.py

**Language**: Python

**Source**: `utils/password.py`

---

## Functions

### get_decrypted_password(doctype, name, fieldname = 'password', raise_exception = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| fieldname | None | 'password' | - |
| raise_exception | None | True | - |

**Returns**: (none)



### set_encrypted_password(doctype, name, pwd, fieldname = 'password')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| pwd | None | - | - |
| fieldname | None | 'password' | - |

**Returns**: (none)



### remove_encrypted_password(doctype, name, fieldname = 'password')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| fieldname | None | 'password' | - |

**Returns**: (none)



### check_password(user, pwd, doctype = 'User', fieldname = 'password', delete_tracker_cache = True)

Checks if user and password are correct, else raises frappe.AuthenticationError

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| pwd | None | - | - |
| doctype | None | 'User' | - |
| fieldname | None | 'password' | - |
| delete_tracker_cache | None | True | - |

**Returns**: (none)



### delete_login_failed_cache(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### update_password(user, pwd, doctype = 'User', fieldname = 'password', logout_all_sessions = False)

Update the password for the User

:param user: username
:param pwd: new password
:param doctype: doctype name (for encryption)
:param fieldname: fieldname (in given doctype) (for encryption)
:param logout_all_session: delete all other session

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| pwd | None | - | - |
| doctype | None | 'User' | - |
| fieldname | None | 'password' | - |
| logout_all_sessions | None | False | - |

**Returns**: (none)



### delete_all_passwords_for(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### rename_password(doctype, old_name, new_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |

**Returns**: (none)



### rename_password_field(doctype, old_fieldname, new_fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| old_fieldname | None | - | - |
| new_fieldname | None | - | - |

**Returns**: (none)



### create_auth_table()

**Returns**: (none)



### encrypt(txt, encryption_key = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| txt | None | - | - |
| encryption_key | None | None | - |

**Returns**: (none)



### decrypt(txt, encryption_key = None, key: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| txt | None | - | - |
| encryption_key | None | None | - |
| key | str | None | None | - |

**Returns**: (none)



### get_encryption_key()

**Returns**: (none)



### get_password_reset_limit()

**Returns**: (none)


