# API Reference: google_calendar.py

**Language**: Python

**Source**: `integrations/doctype/google_calendar/google_calendar.py`

---

## Classes

### RecurrenceParameters

**Inherits from**: TypedDict



### GoogleCalendar

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_access_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### authorize_access(g_calendar: str, reauthorize: bool = False)

If no Authorization code get it from Google and then request for Refresh Token.
Google Calendar Name is set to flags to set_value after Authorization Code is obtained.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_calendar | str | - | - |
| reauthorize | bool | False | - |

**Returns**: (none)



### get_authentication_url(client_id = None, redirect_uri = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| client_id | None | None | - |
| redirect_uri | None | None | - |

**Returns**: (none)



### google_callback(code = None)

Authorization code is sent to callback as per the API configuration

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | None | None | - |

**Returns**: (none)



### sync(g_calendar: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_calendar | str | None | None | - |

**Returns**: (none)



### get_google_calendar_object(g_calendar)

Return an object of Google Calendar along with Google Calendar doc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_calendar | None | - | - |

**Returns**: (none)



### check_google_calendar(account: GoogleCalendar, google_calendar)

Checks if Google Calendar is present with the specified name.
If not, creates one.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | GoogleCalendar | - | - |
| google_calendar | None | - | - |

**Returns**: (none)



### sync_events_from_google_calendar(g_calendar, method = None)

Sync Events from Google Calendar in Framework Calendar.

Google Calendar returns nextSyncToken when all the events in Google Calendar are fetched.
nextSyncToken is returned at the very last page
https://developers.google.com/calendar/v3/sync

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| g_calendar | None | - | - |
| method | None | None | - |

**Returns**: (none)



### insert_event_to_calendar(account, event, recurrence = None)

Inserts event in Frappe Calendar during Sync

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| event | None | - | - |
| recurrence | None | None | - |

**Returns**: (none)



### update_participants_in_event(calendar_event: 'Event', google_event: dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| calendar_event | 'Event' | - | - |
| google_event | dict | - | - |

**Returns**: (none)



### update_event_in_calendar(account, event, recurrence = None)

Updates Event in Frappe Calendar if any existing Google Calendar Event is updated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |
| event | None | - | - |
| recurrence | None | None | - |

**Returns**: (none)



### insert_event_in_google_calendar(doc, method = None)

Insert Events in Google Calendar if sync_with_google_calendar is checked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### update_event_in_google_calendar(doc, method = None)

Updates Events in Google Calendar if any existing event is modified in Frappe Calendar

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### delete_event_from_google_calendar(doc, method = None)

Delete Events from Google Calendar if Frappe Event is deleted.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### parse_google_calendar_date(dt)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |

**Returns**: (none)



### google_calendar_to_repeat_on()

recurrence is in the form ['RRULE:FREQ=WEEKLY;BYDAY=MO,TU,TH']
has the frequency and then the days on which the event recurs

Both have been mapped in a dict for easier mapping.

**Returns**: (none)



### format_date_according_to_google_calendar(all_day, starts_on, ends_on = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| all_day | None | - | - |
| starts_on | None | - | - |
| ends_on | None | None | - |

**Returns**: (none)



### parse_google_calendar_recurrence_rule(repeat_day_week_number, repeat_day_name)

Return (repeat_on) exact date for combination eg 4TH viz. 4th thursday of a month.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| repeat_day_week_number | None | - | - |
| repeat_day_name | None | - | - |

**Returns**: (none)



### repeat_on_to_google_calendar_recurrence_rule(doc)

Return event (repeat_on) in Google Calendar format ie RRULE:FREQ=WEEKLY;BYDAY=MO,TU,TH.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_week_number(dt: date)

Return the week number of the month for the specified date.

https://stackoverflow.com/questions/3806473/python-week-number-of-the-month/16804556

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | date | - | - |

**Returns**: (none)



### get_recurrence_parameters(recurrence: str) → RecurrenceParameters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| recurrence | str | - | - |

**Returns**: `RecurrenceParameters`



### get_conference_data(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_attendees(doc)

Return a list of dicts with attendee emails, if available in event_participants table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)


