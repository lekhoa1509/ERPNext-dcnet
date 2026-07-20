# API Reference: system_health_report.py

**Language**: Python

**Source**: `desk/doctype/system_health_report/system_health_report.py`

---

## Classes

### SystemHealthReport

**Inherits from**: Document

#### Methods

##### db_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_background_jobs(self)

**Decorators**: `@health_check('Background Jobs')`, `@no_wait(get_redis_conn)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_scheduler(self)

**Decorators**: `@health_check('Scheduler')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_email_stats(self)

**Decorators**: `@health_check('Emails')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_errors(self)

**Decorators**: `@health_check('Errors')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_database_details(self)

**Decorators**: `@health_check('Database')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_cache_details(self)

**Decorators**: `@health_check('Cache')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_storage_details(self)

**Decorators**: `@health_check('Storage')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_user_stats(self)

**Decorators**: `@health_check('Users')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list(filters = None, page_length = 20)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |
| page_length | None | 20 | - |


##### get_count(filters = None)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |


##### get_stats()

**Decorators**: `@staticmethod`




## Functions

### no_wait(func)

Disable tenacity waiting on some function

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### health_check(step: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| step | str | - | - |

**Returns**: (none)



### get_job_status(job_id: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | str | None | None | - |

**Returns**: (none)



### get_directory_size()

**Returns**: (none)



### _get_directory_size()

**Returns**: (none)



### suppress_exception(func: Callable)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | Callable | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


