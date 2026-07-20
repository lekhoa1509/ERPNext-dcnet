# API Reference: test_rq_job.py

**Language**: Python

**Source**: `core/doctype/rq_job/test_rq_job.py`

---

## Classes

### TestRQJob

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### check_status(self, job: Job, status, wait = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job | Job | - | - |
| status | None | - | - |
| wait | None | True | - |


##### test_serialization(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_configurable_ttl(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_func_obj_serialization(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_list_filtering(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_queue_burst_consumption(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multi_queue_burst_consumption_worker_pool(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_job_id_manual_dedup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_auto_job_dedup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_enqueue_after_commit(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_memory_usage(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_failed_jobs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### wait_for_completion(job: Job)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job | Job | - | - |

**Returns**: (none)



### test_func(fail = False, sleep = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fail | None | False | - |
| sleep | None | 0 | - |

**Returns**: (none)


