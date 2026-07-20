# API Reference: redis_queue.py

**Language**: Python

**Source**: `utils/redis_queue.py`

---

## Classes

### RedisQueue

**Inherits from**: (none)

#### Methods

##### __init__(self, conn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| conn | None | - | - |


##### add_user(self, username, password = None)

Create or update the user.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| username | None | - | - |
| password | None | None | - |


##### get_connection(cls, username = None, password = None)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| username | None | None | - |
| password | None | None | - |


##### new(cls, username = 'default', password = None)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| username | None | 'default' | - |
| password | None | None | - |


##### set_admin_password(cls, cur_password = None, new_password = None, reset_passwords = False)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| cur_password | None | None | - |
| new_password | None | None | - |
| reset_passwords | None | False | - |


##### get_new_user_settings(cls, username, password)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| username | None | - | - |
| password | None | - | - |


##### get_acl_key_rules(cls, include_key_prefix = False)

FIXME: Find better way

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| include_key_prefix | None | False | - |


##### get_acl_command_rules(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### gen_acl_list(cls, set_admin_password = False)

Generate list of ACL users needed for this branch.

This list contains default ACL user and the bench ACL user(used by all sites incase of ACL is enabled).

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| set_admin_password | None | False | - |



