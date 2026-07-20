# API Reference: event.py

**Language**: Python

**Source**: `desk/doctype/event/event.py`

---

## Classes

### Event

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### sync_communication(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_communication(self, participant: 'EventParticipants')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| participant | 'EventParticipants' | - | - |


##### update_communication(self, participant: 'EventParticipants', communication: 'Communication')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| participant | 'EventParticipants' | - | - |
| communication | 'Communication' | - | - |


##### add_participant(self, doctype, docname)

Add a single participant to event participants

Args:
        doctype (string): Reference Doctype
        docname (string): Reference Docname

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |


##### add_participants(self, participants)

Add participant entry

Args:
        participants ([Array]): Array of a dict with doctype and docname

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| participants | None | - | - |


##### set_participants_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_event_from_user_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### update_attending_status(event_name, attendee, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event_name | None | - | - |
| attendee | None | - | - |
| status | None | - | - |

**Returns**: (none)



### delete_communication(event, reference_doctype, reference_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |
| reference_doctype | None | - | - |
| reference_docname | None | - | - |

**Returns**: (none)



### get_permission_query_conditions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_permission(doc, ptype = None, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | None | - |
| user | None | None | - |

**Returns**: (none)



### send_event_digest()

**Returns**: (none)



### get_events(start: date, end: date, user: str | None = None, for_reminder: bool = False, filters = None) → list[frappe._dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | date | - | - |
| end | date | - | - |
| user | str | None | None | - |
| for_reminder | bool | False | - |
| filters | None | None | - |

**Returns**: `list[frappe._dict]`



### delete_events(ref_type, ref_name, delete_event = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_type | None | - | - |
| ref_name | None | - | - |
| delete_event | None | False | - |

**Returns**: (none)



### set_status_of_events()

**Returns**: (none)



### resolve_event(e: EventLikeDict, target_date: 'date', repeat_till: 'date')

Record the event if it falls within the date range and is not excluded by the weekday.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | EventLikeDict | - | - |
| target_date | 'date' | - | - |
| repeat_till | 'date' | - | - |

**Returns**: (none)


