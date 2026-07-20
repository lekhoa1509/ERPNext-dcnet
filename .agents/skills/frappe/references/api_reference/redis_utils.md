# API Reference: redis_utils.py

**Language**: Python

**Source**: `commands/redis_utils.py`

---

## Functions

### create_rq_users(set_admin_password = False, use_rq_auth = False)

Create Redis Queue users and add to acl and app configs.

acl config file will be used by redis server while starting the server
and app config is used by app while connecting to redis server.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| set_admin_password | None | False | - |
| use_rq_auth | None | False | - |

**Returns**: (none)


