# API Reference: test_submission_queue.py

**Language**: Python

**Source**: `core/doctype/submission_queue/test_submission_queue.py`

---

## Classes

### TestSubmissionQueue

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### check_status(self, job: 'Job', status, wait = True)

**Decorators**: `@timeout(seconds=20)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job | 'Job' | - | - |
| status | None | - | - |
| wait | None | True | - |


##### test_queue_operation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



