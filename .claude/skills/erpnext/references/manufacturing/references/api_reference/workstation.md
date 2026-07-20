# API Reference: workstation.py

**Language**: Python

**Source**: `doctype/workstation/workstation.py`

---

## Classes

### WorkstationHolidayError

**Inherits from**: frappe.ValidationError



### NotInWorkingHoursError

**Inherits from**: frappe.ValidationError



### OverlapError

**Inherits from**: frappe.ValidationError



### Workstation

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_operating_component(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### disabled_workstation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_total_working_hours(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_working_hours(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### set_hour_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_data_based_on_workstation_type(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### publish_workstation_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_overlap_for_operation_timings(self)

Check if there is no overlap in setting Workstation Operating Hours

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_bom_operation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_workstation_holiday(self, schedule_date, skip_holiday_list_check = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| schedule_date | None | - | - |
| skip_holiday_list_check | None | False | - |


##### start_job(self, job_card, from_time, employee)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job_card | None | - | - |
| from_time | None | - | - |
| employee | None | - | - |


##### complete_job(self, job_card, qty, to_time)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| job_card | None | - | - |
| qty | None | - | - |
| to_time | None | - | - |




## Functions

### get_job_cards(workstation, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workstation | None | - | - |
| job_card | None | None | - |

**Returns**: (none)



### get_status_color(status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| status | None | - | - |

**Returns**: (none)



### get_raw_materials(job_card)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_card | None | - | - |

**Returns**: (none)



### get_time_logs(job_cards)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_cards | None | - | - |

**Returns**: (none)



### get_default_holiday_list(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### check_if_within_operating_hours(workstation, operation, from_datetime, to_datetime)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workstation | None | - | - |
| operation | None | - | - |
| from_datetime | None | - | - |
| to_datetime | None | - | - |

**Returns**: (none)



### is_within_operating_hours(workstation, operation, from_datetime, to_datetime)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workstation | None | - | - |
| operation | None | - | - |
| from_datetime | None | - | - |
| to_datetime | None | - | - |

**Returns**: (none)



### check_workstation_for_holiday(workstation, from_datetime, to_datetime)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workstation | None | - | - |
| from_datetime | None | - | - |
| to_datetime | None | - | - |

**Returns**: (none)



### get_workstations()

**Returns**: (none)



### get_color_map()

**Returns**: (none)



### update_job_card(job_card, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_card | None | - | - |
| method | None | - | - |

**Returns**: (none)



### validate_job_card(job_card, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| job_card | None | - | - |
| status | None | - | - |

**Returns**: (none)


