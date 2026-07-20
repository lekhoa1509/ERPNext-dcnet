# API Reference: auth.py

**Language**: Python

**Source**: `auth.py`

---

## Classes

### HTTPRequest

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### domain(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_request_ip(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_cookies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_session(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_csrf_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_lang(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_allowed_referrer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### LoginManager

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### post_login(self, session_end: str | None = None, audit_user: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| session_end | str | None | None | - |
| audit_user | str | None | None | - |


##### get_user_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_boot_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_user_info(self, resume = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| resume | None | False | - |


##### clear_preferred_language(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_session(self, resume: bool = False, session_end: str | None = None, audit_user: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| resume | bool | False | - |
| session_end | str | None | None | - |
| audit_user | str | None | None | - |


##### clear_active_sessions(self)

Clear other sessions of the current user if `deny_multiple_sessions` is not set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### authenticate(self, user: str | None = None, pwd: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | None | None | - |
| pwd | str | None | None | - |


##### force_user_to_reset_password(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_password(self, user, pwd)

check password

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | - | - |
| pwd | None | - | - |


##### fail(self, message, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| message | None | - | - |
| user | None | None | - |


##### run_trigger(self, event = 'on_login')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| event | None | 'on_login' | - |


##### validate_hour(self)

check if user is logging in during restricted hours

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login_as_guest(self)

login as guest

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login_as(self, user: str, session_end: str | None = None, audit_user: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |
| session_end | str | None | None | - |
| audit_user | str | None | None | - |


##### impersonate(self, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | - | - |


##### logout(self, arg = '', user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| arg | None | '' | - |
| user | None | None | - |


##### clear_cookies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### CookieManager

**Inherits from**: (none)

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### init_cookies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_cookie(self, key, value, expires = None, secure = False, httponly = False, samesite = 'Lax', max_age = None, deduplicate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |
| expires | None | None | - |
| secure | None | False | - |
| httponly | None | False | - |
| samesite | None | 'Lax' | - |
| max_age | None | None | - |
| deduplicate | None | False | - |


##### delete_cookie(self, to_delete)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| to_delete | None | - | - |


##### flush_cookies(self, response: Response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | Response | - | - |




### LoginAttemptTracker

Track login attemts of a user.

Lock the account for s number of seconds if there have been n consecutive unsuccessful attempts to log in.

**Inherits from**: (none)

#### Methods

##### __init__(self, key: str, max_consecutive_login_attempts: int = 3, lock_interval: int = 5 * 60)

Initialize the tracker.

:param user_name: Name of the loggedin user
:param max_consecutive_login_attempts: Maximum allowed consecutive failed login attempts
:param lock_interval: Locking interval incase of maximum failed attempts

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |
| max_consecutive_login_attempts | int | 3 | - |
| lock_interval | int | 5 * 60 | - |


##### login_failed_count(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login_failed_count(self, count)

**Decorators**: `@login_failed_count.setter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | None | - | - |


##### login_failed_count(self)

**Decorators**: `@login_failed_count.deleter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login_failed_time(self)

First failed login attempt time within lock interval.

For every user we track only First failed login attempt time within lock interval of time.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### login_failed_time(self, timestamp)

**Decorators**: `@login_failed_time.setter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| timestamp | None | - | - |


##### login_failed_time(self)

**Decorators**: `@login_failed_time.deleter`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_failure_attempt(self)

Log user failure attempts into the system.

Increase the failure count if new failure is with in current lock interval time period, if not reset the login failure count.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_success_attempt(self)

Reset login failures.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_user_allowed(self) → bool

Is user allowed to login

User is not allowed to login if login failures are greater than threshold within in lock interval from first login failure.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`




## Functions

### get_logged_user()

**Returns**: (none)



### clear_cookies()

**Returns**: (none)



### validate_ip_address(user)

Method to check if the user has IP restrictions enabled, and if so is the IP address they are
connecting from allowlisted.

Certain methods called from our socketio backend need direct access, and so the IP is not
checked for those

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_login_attempt_tracker(key: str, raise_locked_exception: bool = True)

Get login attempt tracker instance.

:param user_name: Name of the loggedin user
:param raise_locked_exception: If set, raises an exception incase of user not allowed to login

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| raise_locked_exception | bool | True | - |

**Returns**: (none)



### validate_auth()

Authenticate and sets user for the request.

**Returns**: (none)



### validate_oauth(authorization_header)

Authenticate request using OAuth and set session user

Args:
        authorization_header (list of str): The 'Authorization' header containing the prefix and token

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| authorization_header | None | - | - |

**Returns**: (none)



### validate_auth_via_api_keys(authorization_header)

Authenticate request using API keys and set session user

Args:
        authorization_header (list of str): The 'Authorization' header containing the prefix and token

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| authorization_header | None | - | - |

**Returns**: (none)



### validate_api_key_secret(api_key, api_secret, frappe_authorization_source = None)

frappe_authorization_source to provide api key and secret for a doctype apart from User

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| api_key | None | - | - |
| api_secret | None | - | - |
| frappe_authorization_source | None | None | - |

**Returns**: (none)



### validate_auth_via_hooks()

**Returns**: (none)



### check_request_ip()

**Returns**: (none)


