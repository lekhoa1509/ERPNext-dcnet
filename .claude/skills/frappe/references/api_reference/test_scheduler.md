# API Reference: test_scheduler.py

**Language**: Python

**Source**: `tests/test_scheduler.py`

---

## Classes

### TestScheduler

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_enqueue_jobs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_queue_peeking(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_dormant(self, _mock)

**Decorators**: `@patch.object(frappe.utils.frappecloud, 'on_frappecloud', return_value=True)`, `@patch.dict(frappe.conf, {'developer_mode': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _mock | None | - | - |


##### test_once_a_day_for_dormant(self, _mocks)

**Decorators**: `@patch.object(frappe.utils.frappecloud, 'on_frappecloud', return_value=True)`, `@patch.dict(frappe.conf, {'developer_mode': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _mocks | None | - | - |


##### test_real_time_alignment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### test_timeout_10()

**Returns**: (none)



### test_method()

**Returns**: (none)



### get_test_job(method = 'frappe.tests.test_scheduler.test_timeout_10', frequency = 'All') → ScheduledJobType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | 'frappe.tests.test_scheduler.test_timeout_10' | - |
| frequency | None | 'All' | - |

**Returns**: `ScheduledJobType`


