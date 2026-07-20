# API Reference: sessions.py

**Language**: Python

**Source**: `sessions.py`

---

## Classes

### Session

**Inherits from**: (none)

#### Methods

##### __init__(self, user: str, resume: bool = False, full_name: str | None = None, user_type: str | None = None, session_end: str | None = None, audit_user: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |
| resume | bool | False | - |
| full_name | str | None | None | - |
| user_type | str | None | None | - |
| session_end | str | None | None | - |
| audit_user | str | None | None | - |


##### validate_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start(self, session_end: str | None = None, audit_user: str | None = None)

start a new session

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| session_end | str | None | None | - |
| audit_user | str | None | None | - |


##### insert_session_record(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### resume(self)

non-login request: load a session

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_session_record(self)

get session record, or return the standard Guest Record

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_session_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_session_data_from_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_session_data_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _delete_session(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### start_as_guest(self)

all guests share the same 'Guest' session

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update(self, force = False)

extend session expiry

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| force | None | False | - |


##### set_impersonated(self, original_user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| original_user | None | - | - |




## Functions

### clear()

**Returns**: (none)



### clear_sessions(user = None, keep_current = False, force = False)

Clear other sessions of the current user. Called at login / logout

:param user: user name (default: current user)
:param keep_current: keep current session (default: false)
:param force: triggered by the user (default false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |
| keep_current | None | False | - |
| force | None | False | - |

**Returns**: (none)



### get_sessions_to_clear(user = None, keep_current = False, force = False)

Return sessions of the current user. Called at login / logout.

:param user: user name (default: current user)
:param keep_current: keep current session (default: false)
:param force: ignore simultaneous sessions count, log the user out of all except current (default: false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |
| keep_current | None | False | - |
| force | None | False | - |

**Returns**: (none)



### delete_session(sid = None, user = None, reason = 'Session Expired')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sid | None | None | - |
| user | None | None | - |
| reason | None | 'Session Expired' | - |

**Returns**: (none)



### clear_all_sessions(reason = None)

This effectively logs out all users

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reason | None | None | - |

**Returns**: (none)



### get_expired_sessions()

Return list of expired sessions.

**Returns**: (none)



### clear_expired_sessions()

This function is meant to be called from scheduler

**Returns**: (none)



### get()

get session boot info

**Returns**: (none)



### get_boot_assets_json()

**Returns**: (none)



### get_csrf_token()

**Returns**: (none)



### generate_csrf_token()

**Returns**: (none)



### get_expiry_period_for_query()

**Returns**: (none)



### get_expiry_in_seconds(expiry = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| expiry | None | None | - |

**Returns**: (none)



### get_expired_threshold()

Get cutoff time before which all sessions are considered expired.

**Returns**: (none)



### get_expiry_period()

**Returns**: (none)


