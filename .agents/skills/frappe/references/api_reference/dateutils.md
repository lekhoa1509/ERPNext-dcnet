# API Reference: dateutils.py

**Language**: Python

**Source**: `utils/dateutils.py`

---

## Functions

### user_to_str(date, date_format = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| date_format | None | None | - |

**Returns**: (none)



### parse_date(date)

tries to parse given date to system's format i.e. yyyy-mm-dd. returns a string

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### get_user_date_format()

**Returns**: (none)



### datetime_in_user_format(date_time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_time | None | - | - |

**Returns**: (none)



### get_dates_from_timegrain(from_date, to_date, timegrain = 'Daily')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_date | None | - | - |
| to_date | None | - | - |
| timegrain | None | 'Daily' | - |

**Returns**: (none)



### get_from_date_from_timespan(to_date, timespan)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| to_date | None | - | - |
| timespan | None | - | - |

**Returns**: (none)



### get_period(date, interval = 'Monthly')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| interval | None | 'Monthly' | - |

**Returns**: (none)



### get_period_beginning(date, timegrain, as_str = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| timegrain | None | - | - |
| as_str | None | True | - |

**Returns**: (none)



### get_period_ending(date, timegrain)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| timegrain | None | - | - |

**Returns**: (none)


