# API Reference: scheduler.py

**Language**: Python

**Source**: `utils/scheduler.py`

---

## Functions

### cprint()

Prints only if called from STDOUT

**Returns**: (none)



### start_scheduler() → NoReturn

Run enqueue_events_for_all_sites based on scheduler tick.
Specify scheduler_tick_interval in seconds in common_site_config.json

**Returns**: `NoReturn`



### _get_scheduler_lock_file() → True

**Returns**: `True`



### is_schduler_process_running() → bool

Checks if any other process is holding the lock.

Note: FLOCK is held by process until it exits, this function just checks if process is
running or not. We can't determine if process is stuck somehwere.

**Returns**: `bool`



### sleep_duration(tick)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tick | None | - | - |

**Returns**: (none)



### enqueue_events_for_all_sites() → None

Loop through sites and enqueue events that are not already queued

**Returns**: `None`



### enqueue_events_for_site(site: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | str | - | - |

**Returns**: `None`



### enqueue_events() → list[str] | None

**Returns**: `list[str] | None`



### is_scheduler_inactive(verbose = True) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| verbose | None | True | - |

**Returns**: `bool`



### is_scheduler_disabled(verbose = True) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| verbose | None | True | - |

**Returns**: `bool`



### toggle_scheduler(enable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable | None | - | - |

**Returns**: (none)



### enable_scheduler()

**Returns**: (none)



### disable_scheduler()

**Returns**: (none)



### schedule_jobs_based_on_activity(check_time = None)

Return True for active sites as defined by `Activity Log`.
Also return True for inactive sites once every 24 hours based on `Scheduled Job Log`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| check_time | None | None | - |

**Returns**: (none)



### is_dormant(check_time = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| check_time | None | None | - |

**Returns**: (none)



### _get_last_creation_timestamp(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### activate_scheduler()

**Returns**: (none)



### get_scheduler_status()

**Returns**: (none)



### get_scheduler_tick() → int

**Returns**: `int`



### log_exc()

**Returns**: (none)


