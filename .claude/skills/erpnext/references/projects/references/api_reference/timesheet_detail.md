# API Reference: timesheet_detail.py

**Language**: Python

**Source**: `doctype/timesheet_detail/timesheet_detail.py`

---

## Classes

### TimesheetDetail

**Inherits from**: Document

#### Methods

##### set_to_time(self)

Set to_time based on from_time and hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_project(self)

Set project based on task.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_hours(self)

Calculate hours based on from_time and to_time.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_billing_hours(self)

Update billing hours based on hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_cost(self, employee: str)

Update costing and billing rates based on activity type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| employee | str | - | - |


##### validate_dates(self)

Validate that to_time is not before from_time.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_project(self, parent_project: str)

Validate that project is same as Timesheet's parent project.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent_project | str | - | - |


##### validate_task_project(self)

Validate that the the task belongs to the project specified in the timesheet detail.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_billing_hours(self)

Warn if billing hours are more than actual hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



