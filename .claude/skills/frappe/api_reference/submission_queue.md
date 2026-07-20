# API Reference: submission_queue.py

**Language**: Python

**Source**: `core/doctype/submission_queue/submission_queue.py`

---

## Classes

### SubmissionQueue

**Inherits from**: Document

#### Methods

##### created_at(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### enqueued_by(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### queued_doc(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_logs(days = 30)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 30 | - |


##### insert(self, to_be_queued_doc: Document, action: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| to_be_queued_doc | Document | - | - |
| action | str | - | - |


##### lock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unlock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_job_id(self, job_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job_id | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### background_submission(self, to_be_queued_doc: Document, action_for_queuing: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| to_be_queued_doc | Document | - | - |
| action_for_queuing | str | - | - |


##### notify(self, submission_status: str, action: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| submission_status | str | - | - |
| action | str | - | - |


##### unlock_doc(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### queue_submission(doc: Document, action: str, alert: bool = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | Document | - | - |
| action | str | - | - |
| alert | bool | True | - |

**Returns**: (none)



### get_latest_submissions(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### format_tb(traceback: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| traceback | str | None | None | - |

**Returns**: (none)


