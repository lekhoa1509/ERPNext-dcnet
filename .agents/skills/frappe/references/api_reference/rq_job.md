# API Reference: rq_job.py

**Language**: Python

**Source**: `core/doctype/rq_job/rq_job.py`

---

## Classes

### RQJob

**Inherits from**: Document

#### Methods

##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### job(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list(filters = None, start = 0, page_length = 20, order_by = 'creation desc')

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |
| start | None | 0 | - |
| page_length | None | 20 | - |
| order_by | None | 'creation desc' | - |


##### get_matching_job_ids(filters) → list[str]

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: `list[str]`


##### delete(self)

**Decorators**: `@check_permissions`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### stop_job(self)

**Decorators**: `@check_permissions`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel(self)

**Decorators**: `@check_permissions`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_count(filters = None) → int

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | None | - |

**Returns**: `int`


##### get_stats()

**Decorators**: `@staticmethod`


##### db_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_permissions(method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |

**Returns**: (none)



### serialize_job(job: Job) → frappe._dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | Job | - | - |

**Returns**: `frappe._dict`



### for_current_site(job: Job) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | Job | - | - |

**Returns**: `bool`



### filter_current_site_jobs(job_ids: list[str]) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_ids | list[str] | - | - |

**Returns**: `list[str]`



### _eval_filters(filter, values: list[str]) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filter | None | - | - |
| values | list[str] | - | - |

**Returns**: `list[str]`



### fetch_job_ids(queue: Queue, status: str) → list[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| queue | Queue | - | - |
| status | str | - | - |

**Returns**: `list[str]`



### remove_failed_jobs()

**Returns**: (none)



### get_all_queued_jobs()

**Returns**: (none)



### stop_job(job_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_id | None | - | - |

**Returns**: (none)



### get_custom_queues()

**Returns**: (none)



### wrapper()

**Returns**: (none)


