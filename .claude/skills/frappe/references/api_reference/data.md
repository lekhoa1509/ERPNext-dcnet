# API Reference: data.py

**Language**: Python

**Source**: `utils/data.py`

---

## Classes

### Weekday

**Inherits from**: Enum



### _UserInfo

**Inherits from**: typing.TypedDict



### UnicodeWithAttrs

**Inherits from**: str

#### Methods

##### __init__(self, text)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| text | None | - | - |




## Functions

### get_start_of_week_index() → int

**Returns**: `int`



### is_invalid_date_string(date_string: str) → bool

Return True if the date string is invalid or None or empty.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_string | str | - | - |

**Returns**: `bool`



### getdate(string_date: DateTimeLikeObject | None = None, parse_day_first: bool = False) → datetime.date | None

Convert string date (yyyy-mm-dd) to datetime.date object.
If no input is provided, current date is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_date | DateTimeLikeObject | None | None | - |
| parse_day_first | bool | False | - |

**Returns**: `datetime.date | None`



### get_datetime(datetime_str: DateTimeLikeObject | None | tuple | list = None) → datetime.datetime | None

Return the below mentioned values based on the given `datetime_str`:

* If `datetime_str` is None, returns datetime object of current datetime
* If `datetime_str` is already a datetime object, returns the same
* If `datetime_str` is a timedelta object, returns the same
* If `datetime_str` is a list or tuple, returns a datetime object
* If `datetime_str` is a date object, returns a datetime object
* If `datetime_str` is a valid date string, returns a datetime object for the same
* If `datetime_str` is an invalid date string, returns None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime_str | DateTimeLikeObject | None | tuple | list | None | - |

**Returns**: `datetime.datetime | None`



### get_timedelta(time: str | datetime.timedelta | None = None) → datetime.timedelta | None

Return `datetime.timedelta` object from string value of a valid time format.

Return None if `time` is not a valid format.

Args:
        time (str | datetime.timedelta): A valid time representation. This string is parsed
        using `dateutil.parser.parse`. Examples of valid inputs are:
        '0:0:0', '17:21:00', '2012-01-19 17:21:00'. Checkout
        https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse

Return:
        datetime.timedelta: Timedelta object equivalent of the passed `time` string

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time | str | datetime.timedelta | None | None | - |

**Returns**: `datetime.timedelta | None`



### to_timedelta(time_str: str | datetime.time) → datetime.timedelta

Return a `datetime.timedelta` object from the given string or `datetime.time` object.
If the given argument is not a string or a `datetime.time` object, it is returned as is.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_str | str | datetime.time | - | - |

**Returns**: `datetime.timedelta`



### add_to_date(date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as_string: Literal[False] = False, as_datetime: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| years | None | 0 | - |
| months | None | 0 | - |
| weeks | None | 0 | - |
| days | None | 0 | - |
| hours | None | 0 | - |
| minutes | None | 0 | - |
| seconds | None | 0 | - |
| as_string | Literal[False] | False | - |
| as_datetime | Literal[False] | False | - |

**Returns**: `datetime.date`



### add_to_date(date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as_string: Literal[False] = False, as_datetime: Literal[True] = True) → datetime.datetime

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| years | None | 0 | - |
| months | None | 0 | - |
| weeks | None | 0 | - |
| days | None | 0 | - |
| hours | None | 0 | - |
| minutes | None | 0 | - |
| seconds | None | 0 | - |
| as_string | Literal[False] | False | - |
| as_datetime | Literal[True] | True | - |

**Returns**: `datetime.datetime`



### add_to_date(date, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as_string: Literal[True] = True, as_datetime: bool = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| years | None | 0 | - |
| months | None | 0 | - |
| weeks | None | 0 | - |
| days | None | 0 | - |
| hours | None | 0 | - |
| minutes | None | 0 | - |
| seconds | None | 0 | - |
| as_string | Literal[True] | True | - |
| as_datetime | bool | False | - |

**Returns**: `str`



### add_to_date(date: DateTimeLikeObject | None = None, years = 0, months = 0, weeks = 0, days = 0, hours = 0, minutes = 0, seconds = 0, as_string = False, as_datetime = False) → DateTimeLikeObject

Adds `days` to the given date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | None | None | - |
| years | None | 0 | - |
| months | None | 0 | - |
| weeks | None | 0 | - |
| days | None | 0 | - |
| hours | None | 0 | - |
| minutes | None | 0 | - |
| seconds | None | 0 | - |
| as_string | None | False | - |
| as_datetime | None | False | - |

**Returns**: `DateTimeLikeObject`



### add_days(date: DateTimeLikeObject, days: NumericType) → DateTimeLikeObject

Return a new date after adding the given number of `days` to the given `date`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | - | - |
| days | NumericType | - | - |

**Returns**: `DateTimeLikeObject`



### add_months(date: DateTimeLikeObject, months: NumericType) → DateTimeLikeObject

Return a new date after adding the given number of `months` to the given `date`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | - | - |
| months | NumericType | - | - |

**Returns**: `DateTimeLikeObject`



### add_years(date: DateTimeLikeObject, years: NumericType) → DateTimeLikeObject

Return a new date after adding the given number of `years` to the given `date`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | - | - |
| years | NumericType | - | - |

**Returns**: `DateTimeLikeObject`



### date_diff(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → int

Return the difference between given two dates in days.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `int`



### days_diff(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → int

Return the difference between given two dates in days.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `int`



### month_diff(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → int

Return the difference between given two dates in months.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `int`



### time_diff(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → datetime.timedelta

Return the difference between given two dates as `datetime.timedelta` object.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `datetime.timedelta`



### time_diff_in_seconds(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → float

Return the difference between given two dates in seconds.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `float`



### time_diff_in_hours(string_ed_date: DateTimeLikeObject, string_st_date: DateTimeLikeObject) → float

Return the difference between given two dates in hours.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_ed_date | DateTimeLikeObject | - | - |
| string_st_date | DateTimeLikeObject | - | - |

**Returns**: `float`



### now_datetime() → datetime.datetime

Return the current datetime in system timezone.

**Returns**: `datetime.datetime`



### get_timestamp(date: DateTimeLikeObject | None = None) → float

Return the Unix timestamp (seconds since Epoch) for the given `date`.
If `date` is None, the current timestamp is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | None | None | - |

**Returns**: `float`



### get_eta(from_time: DateTimeLikeObject, percent_complete) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from_time | DateTimeLikeObject | - | - |
| percent_complete | None | - | - |

**Returns**: `str`



### get_system_timezone() → str

Return the system timezone.

**Returns**: `str`



### convert_utc_to_timezone(utc_timestamp: datetime.datetime, time_zone: str) → datetime.datetime

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| utc_timestamp | datetime.datetime | - | - |
| time_zone | str | - | - |

**Returns**: `datetime.datetime`



### get_datetime_in_timezone(time_zone: str) → datetime.datetime

Return the current datetime in the given timezone (e.g. 'Asia/Kolkata').

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_zone | str | - | - |

**Returns**: `datetime.datetime`



### convert_utc_to_system_timezone(utc_timestamp: datetime.datetime) → datetime.datetime

Return the given UTC `datetime` timestamp in system timezone.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| utc_timestamp | datetime.datetime | - | - |

**Returns**: `datetime.datetime`



### now() → str

Return current datetime as `yyyy-mm-dd hh:mm:ss`.

**Returns**: `str`



### nowdate() → str

Return current date as `yyyy-mm-dd`.

**Returns**: `str`



### today() → str

Return today's date in `yyyy-mm-dd` format.

**Returns**: `str`



### get_abbr(string: str, max_len: int = 2) → str

Return the abbreviation of the given string.

Examples:

* "John Doe" => "JD"
* "Jenny Jane Doe" => "JJ" (default, `max_len` = 2)
* "Jenny Jane Doe" => "JJD" (`max_len` = 3)

Return "?" if the given string is empty.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | str | - | - |
| max_len | int | 2 | - |

**Returns**: `str`



### nowtime() → str

Return current time (system timezone) in `hh:mm:ss` format.

**Returns**: `str`



### get_first_day(dt, d_years = 0, d_months = 0, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| d_years | None | 0 | - |
| d_months | None | 0 | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_first_day(dt, d_years = 0, d_months = 0, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| d_years | None | 0 | - |
| d_months | None | 0 | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_first_day(dt, d_years: int = 0, d_months: int = 0, as_str: bool = False) → str | datetime.date

Return the first day of the month for the date specified by date object.

Also, add `d_years` and `d_months` if specified.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| d_years | int | 0 | - |
| d_months | int | 0 | - |
| as_str | bool | False | - |

**Returns**: `str | datetime.date`



### get_quarter_start(dt: DateTimeLikeObject | None = None, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_quarter_start(dt: DateTimeLikeObject | None = None, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_quarter_start(dt: DateTimeLikeObject | None = None, as_str: bool = False) → str | datetime.date

Return the start date of the quarter for the given datetime like object (`dt`).

If `dt` is None, the current quarter start date is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | bool | False | - |

**Returns**: `str | datetime.date`



### get_first_day_of_week(dt: DateTimeLikeObject, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_first_day_of_week(dt: DateTimeLikeObject, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_first_day_of_week(dt: DateTimeLikeObject, as_str = False) → datetime.date | str

Return the first day of the week (as per System Settings or Sunday by default) for the given datetime like object (`dt`).

If `as_str` is True, the first day of the week is returned as a string in `yyyy-mm-dd` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | None | False | - |

**Returns**: `datetime.date | str`



### get_week_start_offset_days(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### get_normalized_weekday_index(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### get_year_start(dt: DateTimeLikeObject, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_year_start(dt: DateTimeLikeObject, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_year_start(dt: DateTimeLikeObject, as_str = False) → str | datetime.date

Return the start date of the year for the given date (`dt`).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | None | False | - |

**Returns**: `str | datetime.date`



### get_last_day_of_week(dt: DateTimeLikeObject, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_last_day_of_week(dt: DateTimeLikeObject, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_last_day_of_week(dt: DateTimeLikeObject, as_str = False) → datetime.date | str

Return the last day of the week (first day is taken from System Settings or Sunday by default) for the given datetime like object (`dt`).

If `as_str` is True, the last day of the week is returned as a string in `yyyy-mm-dd` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | - | - |
| as_str | None | False | - |

**Returns**: `datetime.date | str`



### get_last_day(dt)

Return last day of the month using:

`get_first_day(dt, 0, 1) + datetime.timedelta(-1)`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### is_last_day_of_the_month(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### get_quarter_ending(dt: DateTimeLikeObject | None = None, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_quarter_ending(dt: DateTimeLikeObject | None = None, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_quarter_ending(date: DateTimeLikeObject | None = None, as_str = False) → str | datetime.date

Return the end date of the quarter for the given datetime like object (`date`).

If `date` is None, the current quarter end date is returned.
If `as_str` is True, the end date of the quarter is returned as a string in `yyyy-mm-dd` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | None | None | - |
| as_str | None | False | - |

**Returns**: `str | datetime.date`



### get_year_ending(dt: DateTimeLikeObject | None = None, as_str: Literal[False] = False) → datetime.date

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[False] | False | - |

**Returns**: `datetime.date`



### get_year_ending(dt: DateTimeLikeObject | None = None, as_str: Literal[True] = False) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | DateTimeLikeObject | None | None | - |
| as_str | Literal[True] | False | - |

**Returns**: `str`



### get_year_ending(date: DateTimeLikeObject | None = None, as_str = False) → datetime.date | str

Return the end date of the year for the given datetime like object (`date`).

If `date` is None, the current year end date is returned.
If `as_str` is True, the end date of the year is returned as a string in `yyyy-mm-dd` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | None | None | - |
| as_str | None | False | - |

**Returns**: `datetime.date | str`



### get_time(time_str: str | datetime.datetime | datetime.time | datetime.timedelta) → datetime.time

Return a `datetime.time` object for the given `time_str`.

If the given argument is already a `datetime.time` object, it is returned as is.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_str | str | datetime.datetime | datetime.time | datetime.timedelta | - | - |

**Returns**: `datetime.time`



### get_datetime_str(datetime_obj: DateTimeLikeObject) → str

Return the given datetime like object (datetime.date, datetime.datetime, string) as a string in `yyyy-mm-dd hh:mm:ss` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime_obj | DateTimeLikeObject | - | - |

**Returns**: `str`



### get_date_str(date_obj: DateTimeLikeObject) → str

Return the given datetime like object (datetime.date, datetime.datetime, string) as a string in `yyyy-mm-dd` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_obj | DateTimeLikeObject | - | - |

**Returns**: `str`



### get_time_str(timedelta_obj: datetime.timedelta | str) → str

Return the given timedelta object as a string in `hh:mm:ss` format.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| timedelta_obj | datetime.timedelta | str | - | - |

**Returns**: `str`



### get_user_date_format() → str

Get the current user date format. The result will be cached.

**Returns**: `str`



### get_user_time_format() → str

Get the current user time format. The result will be cached.

**Returns**: `str`



### format_date(string_date = None, format_string: str | None = None, parse_day_first: bool = False) → str

Convert the given string date to :data:`user_date_format`.

User format specified in defaults

Examples:

* dd-mm-yyyy
* mm-dd-yyyy
* dd/mm/yyyy

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string_date | None | None | - |
| format_string | str | None | None | - |
| parse_day_first | bool | False | - |

**Returns**: `str`



### format_time(time_string = None, format_string: str | None = None) → str

Convert the given string time to :data:`user_time_format`.

User format specified in defaults

Examples:

* HH:mm:ss
* HH:mm

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_string | None | None | - |
| format_string | str | None | None | - |

**Returns**: `str`



### format_datetime(datetime_string: DateTimeLikeObject, format_string: str | None = None) → str

Convert the given string time to :data:`user_datetime_format`
User format specified in defaults

Examples:

* dd-mm-yyyy HH:mm:ss
* mm-dd-yyyy HH:mm

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime_string | DateTimeLikeObject | - | - |
| format_string | str | None | None | - |

**Returns**: `str`



### format_duration(seconds: float | int, hide_days: bool = False) → str

Convert the given duration value in seconds to duration format.

example:
convert 12885 to '3h 34m 45s' where 12885 = seconds in float
        -12885 to '-3h 34m 45s'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| seconds | float | int | - | - |
| hide_days | bool | False | - |

**Returns**: `str`



### duration_to_seconds(duration)

Convert the given duration formatted value to duration value in seconds.

example: convert '3h 34m 45s' to 12885 (value in seconds)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| duration | None | - | - |

**Returns**: (none)



### validate_duration_format(duration)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| duration | None | - | - |

**Returns**: (none)



### get_weekdays() → list[str]

Return a list of weekday names.

Return value: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

**Returns**: `list[str]`



### get_weekday(datetime: DateTimeLikeObject | None = None) → str

Return the weekday name (e.g. 'Sunday') for the given datetime like object (datetime.date, datetime.datetime, string).

If `datetime` argument is not provided, the current weekday name is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime | DateTimeLikeObject | None | None | - |

**Returns**: `str`



### get_month(datetime: DateTimeLikeObject | None = None) → str

Return the month name (e.g. 'January') for the given datetime like object (datetime.date, datetime.datetime, string).

If `datetime` argument is not provided, the current month name is returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| datetime | DateTimeLikeObject | None | None | - |

**Returns**: `str`



### get_timespan_date_range(timespan: TimespanOptions) → tuple[datetime.datetime, datetime.datetime] | None

Return the date range (start_date, end_date) tuple for the given timespan.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| timespan | TimespanOptions | - | - |

**Returns**: `tuple[datetime.datetime, datetime.datetime] | None`



### global_date_format(date: DateTimeLikeObject, format = 'long') → str

Return localized date in the form of 'January 1, 2012'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | DateTimeLikeObject | - | - |
| format | None | 'long' | - |

**Returns**: `str`



### has_common(l1: typing.Hashable, l2: typing.Hashable) → bool

Return truthy value if there are common elements in lists l1 and l2.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| l1 | typing.Hashable | - | - |
| l2 | typing.Hashable | - | - |

**Returns**: `bool`



### cast_fieldtype(fieldtype, value, show_warning = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldtype | None | - | - |
| value | None | - | - |
| show_warning | None | True | - |

**Returns**: (none)



### cast(fieldtype, value = None)

Cast the value to the Python native object of the Frappe fieldtype provided.
If value is None, the first/lowest value of the `fieldtype` will be returned.
If value can't be cast as fieldtype due to an invalid input, None will be returned.

Mapping of Python types => Frappe types:
        * str => ("Data", "Text", "Small Text", "Long Text", "Text Editor", "Select", "Link", "Dynamic Link")
        * float => ("Currency", "Float", "Percent")
        * int => ("Int", "Check")
        * datetime.datetime => ("Datetime",)
        * datetime.date => ("Date",)
        * datetime.time => ("Time",)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fieldtype | None | - | - |
| value | None | None | - |

**Returns**: (none)



### flt(s: NumericType | str, precision: Literal[0]) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | - | - |
| precision | Literal[0] | - | - |

**Returns**: `int`



### flt(s: NumericType | str, precision: int | None = None) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | - | - |
| precision | int | None | None | - |

**Returns**: `float`



### flt(s: None) → Literal[0.0]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |

**Returns**: `Literal[0.0]`



### flt(s: NumericType | str | None, precision: int | None = None, rounding_method: str | None = None) → float

Convert to float (ignoring commas in string).

:param s: Number in string or other numeric format.
:param precision: optional argument to specify precision for rounding.
:returns: Converted number in python float type.

Return 0 if input can not be converted to float.

Examples:

>>> flt("43.5", precision=0)
44
>>> flt("42.5", precision=0)
42
>>> flt("10,500.5666", precision=2)
10500.57
>>> flt("a")
0.0
>>> flt(None)
0.0

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | None | - | - |
| precision | int | None | None | - |
| rounding_method | str | None | None | - |

**Returns**: `float`



### cint(s: NumericType | str | None, default: int = 0) → int

Convert to integer.

:param s: Number in string or other numeric format.
:returns: Converted number in python integer type.

Return default if input cannot be converted to integer.

Examples:
>>> cint("100")
100
>>> cint("a")
0
>>> cint(None)
0

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | None | - | - |
| default | int | 0 | - |

**Returns**: `int`



### floor(s: NumericType | str) → int

Return a number representing the largest integer less than or equal to the specified number.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | - | - |

**Returns**: `int`



### ceil(s: NumericType | str) → int

Return the smallest integer greater than or equal to the given number.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | NumericType | str | - | - |

**Returns**: `int`



### cstr(s, encoding = 'utf-8') → str

Convert the given argument to string.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |
| encoding | None | 'utf-8' | - |

**Returns**: `str`



### sbool(x: str | Any) → bool | str | Any

Convert str object to Boolean if possible.

Example:
        "true" becomes True
        "1" becomes True
        "{}" remains "{}"

Args:
        x (str): String to be converted to Bool

Return Boolean or x.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| x | str | Any | - | - |

**Returns**: `bool | str | Any`



### rounded(num, precision = 0, rounding_method = None)

Round according to method set in system setting, defaults to banker's rounding

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| num | None | - | - |
| precision | None | 0 | - |
| rounding_method | None | None | - |

**Returns**: (none)



### _bankers_rounding_legacy(num, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| num | None | - | - |
| precision | None | - | - |

**Returns**: (none)



### _round_away_from_zero(num, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| num | None | - | - |
| precision | None | - | - |

**Returns**: (none)



### _bankers_rounding(num, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| num | None | - | - |
| precision | None | - | - |

**Returns**: (none)



### remainder(numerator: NumericType, denominator: NumericType, precision: int = 2) → NumericType

Return the remainder of the division of `numerator` by `denominator`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| numerator | NumericType | - | - |
| denominator | NumericType | - | - |
| precision | int | 2 | - |

**Returns**: `NumericType`



### safe_div(numerator: NumericType, denominator: NumericType, precision: int = 2) → float

SafeMath division that returns zero when divided by zero.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| numerator | NumericType | - | - |
| denominator | NumericType | - | - |
| precision | int | 2 | - |

**Returns**: `float`



### round_based_on_smallest_currency_fraction(value, currency, precision = 2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| currency | None | - | - |
| precision | None | 2 | - |

**Returns**: (none)



### encode(obj, encoding = 'utf-8')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| encoding | None | 'utf-8' | - |

**Returns**: (none)



### parse_val(v)

Convert to simple datatypes from SQL query results.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| v | None | - | - |

**Returns**: (none)



### fmt_money(amount: str | float | int | None, precision: int | None = None, currency: str | None = None, format: str | None = None) → str

Convert to string with commas for thousands, millions etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| amount | str | float | int | None | - | - |
| precision | int | None | None | - |
| currency | str | None | None | - |
| format | str | None | None | - |

**Returns**: `str`



### __getattr__(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### money_in_words(number: str | float | int, main_currency: str | None = None, fraction_currency: str | None = None)

Return string in words with currency and fraction currency.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| number | str | float | int | - | - |
| main_currency | str | None | None | - |
| fraction_currency | str | None | None | - |

**Returns**: (none)



### in_words(integer: int, in_million = True) → str

Return string in words for the given integer.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| integer | int | - | - |
| in_million | None | True | - |

**Returns**: `str`



### is_html(text: str) → bool

Return True if the given `text` contains any HTML tags.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | str | - | - |

**Returns**: `bool`



### is_image(filepath: str) → bool

Return True if the given `filepath` points to an image file.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filepath | str | - | - |

**Returns**: `bool`



### get_thumbnail_base64_for_image(src: str) → dict[str, str] | None

Return the base64 encoded string for the thumbnail of the given image source path.

Example return value:

{
        "base64": "data:image/ext;base64,...",
        "width": 50,
        "height": 50
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| src | str | - | - |

**Returns**: `dict[str, str] | None`



### image_to_base64(image: 'PILImageFile', extn: str) → bytes

Return the base64 encoded string for the given PIL `ImageFile`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| image | 'PILImageFile' | - | - |
| extn | str | - | - |

**Returns**: `bytes`



### pdf_to_base64(filename: str) → bytes | None

Return the base64 encoded string for the given PDF file.

Return None if the file is not found or is not a PDF file.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filename | str | - | - |

**Returns**: `bytes | None`



### strip_html(text: str) → str

Remove anything enclosed in and including <>.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | str | - | - |

**Returns**: `str`



### escape_html(text: str) → str

Return the given text with HTML special characters escaped.

e.g. '<h1>Hello</h1>' -> '&lt;h1&gt;Hello&lt;/h1&gt;'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | str | - | - |

**Returns**: `str`



### pretty_date(iso_datetime: datetime.datetime | str, mini = False) → str

Return a localized string representation of the delta to the current system time.

For example, "1 hour ago", "2 days ago", "in 5 seconds", etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| iso_datetime | datetime.datetime | str | - | - |
| mini | None | False | - |

**Returns**: `str`



### comma_or(some_list: list | tuple, add_quotes = True) → str

Return the given list or tuple as a comma separated string with the last item joined by 'or'.
e.g. ['a', 'b', 'c'] -> 'a, b or c'

If `add_quotes` is True, each item in the list will be wrapped in single quotes.
e.g. ['a', 'b', 'c'] -> "'a', 'b' or 'c'"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| some_list | list | tuple | - | - |
| add_quotes | None | True | - |

**Returns**: `str`



### comma_and(some_list: list | tuple, add_quotes = True) → str

Return the given list or tuple as a comma separated string with the last item joined by 'and'.
e.g. ['a', 'b', 'c'] -> 'a, b and c'

If `add_quotes` is True, each item in the list will be wrapped in single quotes.
e.g. ['a', 'b', 'c'] -> "'a', 'b' and 'c'"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| some_list | list | tuple | - | - |
| add_quotes | None | True | - |

**Returns**: `str`



### comma_sep(some_list: list | tuple, pattern: str, add_quotes = True) → str

Return the given list or tuple as a comma separated string, with the last item joined by the given string format pattern.

If `add_quotes` is True, each item in the list will be wrapped in single quotes.

e.g. if `some_list` is ['a', 'b', 'c'] and `pattern` is '{0} or {1}', the output will be 'a, b or c'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| some_list | list | tuple | - | - |
| pattern | str | - | - |
| add_quotes | None | True | - |

**Returns**: `str`



### new_line_sep(some_list: list | tuple) → str

Return the given list or tuple as a new line separated string.

       e.g. ['', 'Paid', 'Unpaid'] -> '
Paid
Unpaid'
       

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| some_list | list | tuple | - | - |

**Returns**: `str`



### filter_strip_join(some_list: list[str], sep: str) → list[str]

given a list, filter None values, strip spaces and join

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| some_list | list[str] | - | - |
| sep | str | - | - |

**Returns**: `list[str]`



### get_url(uri: str | None = None, full_address: bool = False, allow_header_override: bool = True) → str

Get app url from request.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| uri | str | None | None | - |
| full_address | bool | False | - |
| allow_header_override | bool | True | - |

**Returns**: `str`



### get_host_name_from_request() → str

Return the hostname (`request.host`) from the request headers.

**Returns**: `str`



### url_contains_port(url: str) → bool

Return True if the given url contains a port number.

e.g. 'http://localhost:8000' -> True, 'http://localhost' -> False.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: `bool`



### get_host_name() → str

Return the hostname of the current site.

e.g. If site is 'https://cloud.frappe.io', returns 'cloud.frappe.io'.

**Returns**: `str`



### get_link_to_form(doctype: str, name: str | None = None, label: str | None = None) → str

Return the HTML link to the given document's form view.

e.g. get_link_to_form("Sales Invoice", "INV-0001", "Link Label") returns:
    '<a href="https://frappe.io/desk/sales-invoice/INV-0001">Link Label</a>'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | None | None | - |
| label | str | None | None | - |

**Returns**: `str`



### get_link_to_report(name: str, label: str | None = None, report_type: str | None = None, doctype: str | None = None, filters: dict | None = None) → str

Return the HTML link to the given report.

e.g. get_link_to_report("Revenue Report", "Link Label") returns:
        '<a href="https://frappe.io/desk/query-report/Revenue%20Report">Link Label</a>'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |
| label | str | None | None | - |
| report_type | str | None | None | - |
| doctype | str | None | None | - |
| filters | dict | None | None | - |

**Returns**: `str`



### get_absolute_url(doctype: str, name: str) → str

Return the absolute route for the form view of the given document in the desk.

e.g. when doctype="Sales Invoice" and name="INV-00001", returns '/desk/sales-invoice/INV-00001'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `str`



### get_url_to_form(doctype: str, name: str | None = None) → str

Return the absolute URL for the form view of the given document in the desk.

e.g. when doctype="Sales Invoice" and your site URL is "https://frappe.io",
         returns 'https://frappe.io/desk/sales-invoice/INV-00001'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | None | None | - |

**Returns**: `str`



### get_url_to_list(doctype: str) → str

Return the absolute URL for the list view of the given document in the desk.

e.g. when doctype="Sales Invoice" and your site URL is "https://frappe.io",
         returns 'https://frappe.io/desk/sales-invoice'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `str`



### get_url_to_report(name, report_type: str | None = None, doctype: str | None = None) → str

Return the absolute URL for the report in the desk.

e.g. when name="Sales Register" and your site URL is "https://frappe.io",
         returns 'https://frappe.io/desk/query-report/Sales%20Register'

You can optionally pass `report_type` and `doctype` to get the URL for a Report Builder report.

get_url_to_report("Revenue", "Report Builder", "Sales Invoice") -> 'https://frappe.io/desk/sales-invoice/view/report/Revenue'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| report_type | str | None | None | - |
| doctype | str | None | None | - |

**Returns**: `str`



### get_url_to_report_with_filters(name, filters, report_type = None, doctype = None)

Return the absolute URL for the report in the desk with filters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| filters | None | - | - |
| report_type | None | None | - |
| doctype | None | None | - |

**Returns**: (none)



### get_filtered_list_url(doctype: str, docnames: list[str] | None = None) → str

Get a filtered list view URL for a doctype with specific document names.

:param doctype: The doctype name
:param docnames: List of document names to filter

:return: URL to the filtered list view

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| docnames | list[str] | None | None | - |

**Returns**: `str`



### get_filtered_list_link(doctype: str, docnames: list[str] | None = None, label: str | None = None) → str

Get an HTML link to a filtered list view for a doctype with specific document names.

:param doctype: The doctype name
:param docnames: List of document names to filter
:param label: Optional label for the link. If not provided, uses doctype

:return: HTML link to the filtered list view

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| docnames | list[str] | None | None | - |
| label | str | None | None | - |

**Returns**: `str`



### sql_like(value: str, pattern: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | str | - | - |
| pattern | str | - | - |

**Returns**: `bool`



### filter_operator_is(value: str | None, pattern: str) → bool

Operator `is` can have two values: 'set' or 'not set'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | str | None | - | - |
| pattern | str | - | - |

**Returns**: `bool`



### filter_operator_timespan(value: str, pattern: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | str | - | - |
| pattern | str | - | - |

**Returns**: `bool`



### evaluate_filters(doc: 'Mapping', filters: FilterSignature)

Return True if doc matches filters.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Mapping' | - | - |
| filters | FilterSignature | - | - |

**Returns**: (none)



### compare(val1: Any, condition: str, val2: Any, fieldtype: str | None = None) → bool

Compare two values using the specified operator with optional fieldtype casting.

Args:
        val1: The left operand value to compare
        condition: The comparison operator (e.g., "=", ">", "is", "in", "like")
        val2: The right operand value to compare against
        fieldtype: Optional fieldtype for casting val1 (and val2 for most operators)

Returns:
        bool: True if the comparison evaluates to True, False otherwise

Note:
- For "is" operator: No casting is performed to preserve None values
- For "in"/"not in" operators: Only val1 is cast (if not None), val2 remains unchanged
- For "Timespan" operator: No casting is performed
- For other operators: Both val1 and val2 are cast to the specified fieldtype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| val1 | Any | - | - |
| condition | str | - | - |
| val2 | Any | - | - |
| fieldtype | str | None | None | - |

**Returns**: `bool`



### get_filter(doctype: str, filters: FilterSignature, filters_config = None) → 'frappe._dict'

Return a `_dict` like:

{
        "doctype": ...
        "fieldname": ...
        "operator": ...
        "value": ...
        "fieldtype": ...
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| filters | FilterSignature | - | - |
| filters_config | None | None | - |

**Returns**: `'frappe._dict'`



### make_filter_tuple(doctype, key, value)

return a filter tuple like [doctype, key, operator, value]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| key | None | - | - |
| value | None | - | - |

**Returns**: (none)



### make_filter_dict(filters)

convert this [[doctype, key, operator, value], ..]
to this { key: (operator, value), .. }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | None | - | - |

**Returns**: (none)



### sanitize_column(column_name: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| column_name | str | - | - |

**Returns**: `str`



### _sanitize_column(column_name: str, db_type: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| column_name | str | - | - |
| db_type | str | - | - |

**Returns**: `str`



### scrub_urls(html: str) → str

Expand relative urls in the given `html`.

e.g. If HTML is '<a href="/files/abc.jpeg">View Image</a>' and site URL is 'https://frappe.io',
        returns '<a href="https://frappe.io/files/abc.jpeg">View Image</a>'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | str | - | - |

**Returns**: `str`



### expand_relative_urls(html: str) → str

Expand relative urls in the given `html`.

e.g. If HTML is '<a href="/files/abc.jpeg">View Image</a>' and site URL is 'https://frappe.io',
        returns '<a href="https://frappe.io/files/abc.jpeg">View Image</a>'.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | str | - | - |

**Returns**: `str`



### quoted(url: str) → str

Return the given `url` quoted.

e.g. 'https://frappe.io/files/my Image file.jpeg' -> 'https://frappe.io/files/my%20Image%20file.jpeg'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |

**Returns**: `str`



### quote_urls(html: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | str | - | - |

**Returns**: `str`



### unique(seq: typing.Sequence['T']) → list['T']

use this instead of list(set()) to preserve order of the original list.
Thanks to Stackoverflow: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| seq | typing.Sequence['T'] | - | - |

**Returns**: `list['T']`



### strip(val: str, chars: str | None = None) → str

Strip the given characters from the given string.

e.g. strip(',hello,bye,', ',') -> 'hello,bye'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| val | str | - | - |
| chars | str | None | None | - |

**Returns**: `str`



### get_string_between(start: str, string: str, end: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | str | - | - |
| string | str | - | - |
| end | str | - | - |

**Returns**: `str`



### to_markdown(html: str) → str

Convert the given HTML to markdown and returns it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | str | - | - |

**Returns**: `str`



### md_to_html(markdown_text: str) → 'UnicodeWithAttrs' | None

Convert the given markdown text to HTML and returns it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| markdown_text | str | - | - |

**Returns**: `'UnicodeWithAttrs' | None`



### markdown(markdown_text: str) → 'UnicodeWithAttrs' | None

Convert the given markdown text to HTML and returns it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| markdown_text | str | - | - |

**Returns**: `'UnicodeWithAttrs' | None`



### is_subset(list_a: list, list_b: list) → bool

Return whether list_a is a subset of list_b.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| list_a | list | - | - |
| list_b | list | - | - |

**Returns**: `bool`



### generate_hash() → str

Generates a random hash using best available randomness source and returns it.

You can optionally provide the `length` of the hash to be generated. Default is 56.

**Returns**: `str`



### sha256_hash(input: str | bytes) → str

Return hash of the string using sha256 algorithm.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| input | str | bytes | - | - |

**Returns**: `str`



### dict_with_keys(dict, keys)

Return a new dict with a subset of keys.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dict | None | - | - |
| keys | None | - | - |

**Returns**: (none)



### guess_date_format(date_string: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_string | str | - | - |

**Returns**: `str`



### validate_json_string(string: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | str | - | - |

**Returns**: `None`



### parse_json(val: str)

Parses json if string else return

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| val | str | - | - |

**Returns**: (none)



### orjson_dumps(obj, default = None, option = None, decode = True)

A wrapper around `orjson.dumps`, with some default options set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| default | None | None | - |
| option | None | None | - |
| decode | None | True | - |

**Returns**: (none)



### get_user_info_for_avatar(user_id: str) → _UserInfo

Return user info for the given `user_id` suitable for use in an avatar.

e.g. {
        "email": "faris@frappe.io",
        "image": "/assets/frappe/images/ui/avatar.png",
        "name": "Faris Ansari"
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_id | str | - | - |

**Returns**: `_UserInfo`



### validate_python_code(string: str, fieldname: str | None = None, is_expression: bool = True) → None

Validate python code fields by using compile_command to ensure that expression is valid python.

args:
        fieldname: name of field being validated.
        is_expression: true for validating simple single line python expression, else validated as script.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | str | - | - |
| fieldname | str | None | None | - |
| is_expression | bool | True | - |

**Returns**: `None`



### format_timedelta(o: datetime.timedelta | str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| o | datetime.timedelta | str | - | - |

**Returns**: `str`



### parse_timedelta(s: str) → datetime.timedelta

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | str | - | - |

**Returns**: `datetime.timedelta`



### get_job_name(key: str, doctype: str | None = None, doc_name: str | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| doctype | str | None | None | - |
| doc_name | str | None | None | - |

**Returns**: `str`



### get_imaginary_pixel_response()

**Returns**: (none)



### is_site_link(link: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| link | str | - | - |

**Returns**: `bool`



### bold(text: str | int | float) → str

Return `text` wrapped in `<strong>` tags.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | str | int | float | - | - |

**Returns**: `str`



### safe_encode(param, encoding = 'utf-8')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| param | None | - | - |
| encoding | None | 'utf-8' | - |

**Returns**: (none)



### safe_decode(param, encoding = 'utf-8', fallback_map: dict | None = None)

Method to safely decode data into a string

:param param: The data to be decoded
:param encoding: The encoding to decode into
:param fallback_map: A fallback map to reference in case of a LookupError
:return:

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| param | None | - | - |
| encoding | None | 'utf-8' | - |
| fallback_map | dict | None | None | - |

**Returns**: (none)



### as_unicode(text, encoding: str = 'utf-8') → str

Convert to unicode if required.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | None | - | - |
| encoding | str | 'utf-8' | - |

**Returns**: `str`



### mock(type, size = 1, locale = 'en')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| type | None | - | - |
| size | None | 1 | - |
| locale | None | 'en' | - |

**Returns**: (none)



### recursive_defaultdict()

**Returns**: (none)



### _get_rss_memory_usage()

**Returns**: (none)



### add_trackers_to_url(url: str, source: str, campaign: str | None = None, medium: str | None = None, content: str | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |
| source | str | - | - |
| campaign | str | None | None | - |
| medium | str | None | None | - |
| content | str | None | None | - |

**Returns**: `str`



### parse_and_map_trackers_from_url(url: str, create: bool = False) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | str | - | - |
| create | bool | False | - |

**Returns**: `dict`



### map_trackers(url_trackers: dict, create: bool = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url_trackers | dict | - | - |
| create | bool | False | - |

**Returns**: (none)



### attach_expanded_links(doctype: str, docs: list, fields_to_expand: list)

Expands specified link or dynamic link fields in a list of documents by replacing
their linked values (names) with full document records.

This function takes a list of documents and a list of link fieldnames that should be
expanded. For each specified field, it retrieves all referenced linked records from
the corresponding doctypes and replaces the link value in each document with the
full linked record (as a dict).

Args:
        doctype (str): The parent doctype of the provided documents.
        docs (list[dict]): A list of document dictionaries whose link fields are to be expanded.
        fields_to_expand (list[str]): A list of fieldnames corresponding to link or dynamic
                link fields that should be expanded.

Returns:
        None: The function modifies the `docs` list in place.

Example:
        >>> docs = [{"customer": "CUST-001"}, {"customer": "CUST-002"}]
        >>> attach_expanded_links("Sales Invoice", docs, ["customer"])
        >>> docs[0]["customer"]
        {
                "name": "CUST-001",
                "customer_name": "John Doe",
                "customer_group": "Retail",
                ...
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| docs | list | - | - |
| fields_to_expand | list | - | - |

**Returns**: (none)



### fraction_in_words() → str

**Returns**: `str`



### _get_base64()

**Returns**: (none)



### is_set()

**Returns**: (none)



### _raise_exception()

**Returns**: (none)



### _expand_relative_urls(match)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | None | - | - |

**Returns**: (none)



### _quote_url(match)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| match | None | - | - |

**Returns**: (none)



### _get_date_format(date_str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date_str | None | - | - |

**Returns**: (none)



### _get_time_format(time_str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time_str | None | - | - |

**Returns**: (none)



### get_utm_values()

**Returns**: (none)


