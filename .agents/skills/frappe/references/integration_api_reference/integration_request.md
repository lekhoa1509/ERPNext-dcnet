# API Reference: integration_request.py

**Language**: Python

**Source**: `doctype/integration_request/integration_request.py`

---

## Classes

### IntegrationRequest

**Inherits from**: Document

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_logs(days = 30)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 30 | - |


##### update_status(self, params, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| params | None | - | - |
| status | None | - | - |


##### handle_success(self, response)

update the output field with the response along with the relevant status

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | - | - |


##### handle_failure(self, response)

update the error field with the response along with the relevant status

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | - | - |



