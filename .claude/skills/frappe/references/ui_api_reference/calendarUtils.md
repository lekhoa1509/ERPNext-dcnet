# API Reference: calendarUtils.js

**Language**: JavaScript

**Source**: `src/components/Calendar/calendarUtils.js`

---

## Functions

### getCalendarDates(month, year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| month | None | - | - |
| year | None | - | - |

**Returns**: (none)



### getCurrentMonthDates(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### getBeforeDates(firstDay, leftPadding)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| firstDay | None | - | - |
| leftPadding | None | - | - |

**Returns**: (none)



### getNextMonthDates(currentAndPreviousMonthDates)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| currentAndPreviousMonthDates | None | - | - |

**Returns**: (none)



### getDatesAfter(date, startIndex, counter, stepper = 1, getNextMonthDates = false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| startIndex | None | - | - |
| counter | None | - | - |
| stepper | None | 1 | - |
| getNextMonthDates | None | false | - |

**Returns**: (none)



### isLeapYear(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### groupBy(obj, fn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| obj | None | - | - |
| fn | None | - | - |

**Returns**: (none)



### calculateMinutes(time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time | None | - | - |

**Returns**: (none)



### convertMinutesToHours(minutes)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| minutes | None | - | - |

**Returns**: (none)



### parseDate(date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |

**Returns**: (none)



### parseDateEventPopupFormat(date, showDay = true, showMonth = true, weekDay = 'short')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| showDay | None | true | - |
| showMonth | None | true | - |
| weekDay | None | 'short' | - |

**Returns**: (none)



### parseDateWithComma(date, showDay = false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| showDay | None | false | - |

**Returns**: (none)



### parseDateWithDay(date, fullDay = false)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| fullDay | None | false | - |

**Returns**: (none)



### calculateDiff(from, to)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| from | None | - | - |
| to | None | - | - |

**Returns**: (none)



### handleSeconds(time)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time | None | - | - |

**Returns**: (none)



### findOverlappingEventsCount(events)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| events | None | - | - |

**Returns**: (none)



### formattedDuration(fromTime, toTime, timeFormat)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fromTime | None | - | - |
| toTime | None | - | - |
| timeFormat | None | - | - |

**Returns**: (none)



### formatTime(time, format)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| time | None | - | - |
| format | None | - | - |

**Returns**: (none)



### getWeekendDays(config)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| config | None | - | - |

**Returns**: (none)



### isWeekend(date, config)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | - | - |
| config | None | - | - |

**Returns**: (none)



### formatMonthYear(month, year)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| month | None | - | - |
| year | None | - | - |

**Returns**: (none)



### getWeekMonthParts(weekDates)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| weekDates | None | - | - |

**Returns**: (none)


