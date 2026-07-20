# API Reference: test_prepared_report.py

**Language**: Python

**Source**: `core/doctype/prepared_report/test_prepared_report.py`

---

## Classes

### TestPreparedReport

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### wait_for_status(self, report, status)

**Decorators**: `@timeout(seconds=20)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report | None | - | - |
| status | None | - | - |


##### create_prepared_report(self, report = None, commit = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| report | None | None | - |
| commit | None | True | - |


##### test_queueing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_prepared_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_start_status_and_kill_jobs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### test_report()

**Returns**: (none)


