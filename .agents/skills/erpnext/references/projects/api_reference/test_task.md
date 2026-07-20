# API Reference: test_task.py

**Language**: Python

**Source**: `doctype/task/test_task.py`

---

## Classes

### TestTask

**Inherits from**: ERPNextTestSuite

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_task_total_costing_and_billing_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_circular_reference(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reschedule_dependent_task(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_close_assignment(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_overdue(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parent_task_must_be_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_expected_end_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_task(subject, start = None, end = None, depends_on = None, project = None, parent_task = None, is_group = 0, is_template = 0, begin = 0, duration = 0, save = True, priority = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| subject | None | - | - |
| start | None | None | - |
| end | None | None | - |
| depends_on | None | None | - |
| project | None | None | - |
| parent_task | None | None | - |
| is_group | None | 0 | - |
| is_template | None | 0 | - |
| begin | None | 0 | - |
| duration | None | 0 | - |
| save | None | True | - |
| priority | None | None | - |

**Returns**: (none)



### assign()

**Returns**: (none)



### get_owner_and_status()

**Returns**: (none)


