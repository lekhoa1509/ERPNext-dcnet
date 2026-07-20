# API Reference: clear_long_pending_stale_logs.py

**Language**: Python

**Source**: `patches/v14_0/clear_long_pending_stale_logs.py`

---

## Functions

### execute()

Due to large size of log tables on old sites some table cleanups never finished during daily log clean up. This patch discards such data by using "big delete" code.

ref: https://github.com/frappe/frappe/issues/16971

**Returns**: (none)



### is_log_cleanup_stuck(doctype: str, retention: int) → bool

Check if doctype has data significantly older than configured cleanup period

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| retention | int | - | - |

**Returns**: `bool`



### get_current_setting(fieldname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldname | None | - | - |

**Returns**: (none)


