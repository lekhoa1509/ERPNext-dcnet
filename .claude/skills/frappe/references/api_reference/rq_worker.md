# API Reference: rq_worker.py

**Language**: Python

**Source**: `core/doctype/rq_worker/rq_worker.py`

---

## Classes

### RQWorker

**Inherits from**: Document

#### Methods

##### load_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list(start = 0, page_length = 0)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | 0 | - |
| page_length | None | 0 | - |


##### get_count() → int

**Decorators**: `@staticmethod`

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


##### delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### serialize_worker(worker: Worker) → frappe._dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| worker | Worker | - | - |

**Returns**: `frappe._dict`



### compute_utilization(worker: Worker) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| worker | Worker | - | - |

**Returns**: `float`


