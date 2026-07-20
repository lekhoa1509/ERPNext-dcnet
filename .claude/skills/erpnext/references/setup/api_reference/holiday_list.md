# API Reference: holiday_list.py

**Language**: Python

**Source**: `doctype/holiday_list/holiday_list.py`

---

## Classes

### OverlapError

**Inherits from**: frappe.ValidationError



### HolidayList

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_weekly_off_dates(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_supported_countries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_local_holidays(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sort_holidays(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_holidays(self) → list[date]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[date]`


##### validate_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_weekly_off_date_list(self, start_date, end_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| start_date | None | - | - |
| end_date | None | - | - |


##### clear_table(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_events(start, end, filters = None)

Returns events for Gantt / Calendar view rendering.

:param start: Start date-time.
:param end: End date-time.
:param filters: Filters (JSON).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| end | None | - | - |
| filters | None | None | - |

**Returns**: (none)



### is_holiday(holiday_list, date = None)

Returns true if the given date is a holiday in the given holiday list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| holiday_list | None | - | - |
| date | None | None | - |

**Returns**: (none)



### is_half_holiday(holiday_list, date = None)

Returns true if the given date is a half holiday in the given holiday list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| holiday_list | None | - | - |
| date | None | None | - |

**Returns**: (none)



### local_country_name(country_code: str) → str

Return the localized country name for the given country code.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| country_code | str | - | - |

**Returns**: `str`


