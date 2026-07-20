# API Reference: scheduled_job_type.py

**Language**: Python

**Source**: `core/doctype/scheduled_job_type/scheduled_job_type.py`

---

## Classes

### ScheduledJobType

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enqueue(self, force = False) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| force | None | False | - |

**Returns**: `bool`


##### is_event_due(self, current_time = None)

Return true if event is due based on time lapsed since last execution

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| current_time | None | None | - |


##### is_job_in_queue(self) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### rq_job_id(self)

Unique ID created to deduplicate jobs with single RQ call.

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### next_execution(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_next_execution(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### execute(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### log_status(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### update_scheduler_log(self, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| status | None | - | - |


##### get_queue_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### execute_event(doc: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |

**Returns**: (none)



### skip_next_execution(doc: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | str | - | - |

**Returns**: (none)



### run_scheduled_job(scheduled_job_type: str, job_type: str | None = None)

This is a wrapper function that runs a hooks.scheduler_events method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scheduled_job_type | str | - | - |
| job_type | str | None | None | - |

**Returns**: (none)



### sync_jobs(hooks: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hooks | dict | None | None | - |

**Returns**: (none)



### insert_events(scheduler_events: dict) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scheduler_events | dict | - | - |

**Returns**: `list`



### insert_cron_jobs(events: dict) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | dict | - | - |

**Returns**: `list`



### insert_event_jobs(events: list, event_type: str) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | list | - | - |
| event_type | str | - | - |

**Returns**: `list`



### insert_single_event(frequency: str, event: str, cron_format: str | None = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | str | - | - |
| event | str | - | - |
| cron_format | str | None | '' | - |

**Returns**: (none)



### clear_events(scheduler_events: dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| scheduler_events | dict | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### event_exists(event) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |

**Returns**: `bool`


