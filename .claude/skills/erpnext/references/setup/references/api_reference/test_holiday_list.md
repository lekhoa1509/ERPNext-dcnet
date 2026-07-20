# API Reference: test_holiday_list.py

**Language**: Python

**Source**: `doctype/holiday_list/test_holiday_list.py`

---

## Classes

### TestHolidayList

**Inherits from**: IntegrationTestCase

#### Methods

##### test_holiday_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_weekly_off(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_local_holidays(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_localized_country_names(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_holiday_list(name, from_date = None, to_date = None, holiday_dates = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| from_date | None | None | - |
| to_date | None | None | - |
| holiday_dates | None | None | - |

**Returns**: (none)



### set_holiday_list(holiday_list, company_name)

Context manager for setting holiday list in tests

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| holiday_list | None | - | - |
| company_name | None | - | - |

**Returns**: (none)


