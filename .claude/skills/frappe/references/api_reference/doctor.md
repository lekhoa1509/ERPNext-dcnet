# API Reference: doctor.py

**Language**: Python

**Source**: `utils/doctor.py`

---

## Functions

### get_workers()

**Returns**: (none)



### purge_pending_jobs(event = None, site = None, queue = None)

Purge tasks of the event event type. Passing 'all' will not purge all
events but of the all event type, ie. the ones that are enqueued every five
mintues and would any leave daily, hourly and weekly tasks

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | None | - |
| site | None | None | - |
| queue | None | None | - |

**Returns**: (none)



### get_jobs_by_queue(site = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | None | - |

**Returns**: (none)



### get_pending_jobs(site = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | None | - |

**Returns**: (none)



### any_job_pending(site: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | str | - | - |

**Returns**: `bool`



### check_number_of_workers()

**Returns**: (none)



### get_running_tasks()

**Returns**: (none)



### doctor(site = None)

Prints diagnostic information for the scheduler

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | None | - |

**Returns**: (none)



### pending_jobs(site = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | None | None | - |

**Returns**: (none)


