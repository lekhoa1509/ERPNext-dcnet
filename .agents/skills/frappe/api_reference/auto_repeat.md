# API Reference: auto_repeat.py

**Language**: Python

**Source**: `automation/doctype/auto_repeat/auto_repeat.py`

---

## Classes

### AutoRepeat

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_insert(self)

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


##### set_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unlink_if_applicable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reference_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_submit_on_creation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_email_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_auto_repeat_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_auto_repeat_id(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_completed(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_auto_repeat_schedule(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_new_documents(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_new_document(self, assignee = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| assignee | None | None | - |


##### update_doc(self, new_doc, reference_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_doc | None | - | - |
| reference_doc | None | - | - |


##### set_auto_repeat_period(self, new_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_doc | None | - | - |


##### get_next_schedule_date(self, schedule_date, for_full_schedule = False)

Return the next schedule date for auto repeat after a recurring document has been created.
Add required offset to the schedule_date param and return the next schedule date.

:param schedule_date: The date when the last recurring document was created.
:param for_full_schedule: If True, return the immediate next schedule date, else the full schedule.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| schedule_date | None | - | - |
| for_full_schedule | None | False | - |


##### get_days(self, schedule_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| schedule_date | None | - | - |


##### get_offset_for_weekly_frequency(self, schedule_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| schedule_date | None | - | - |


##### get_auto_repeat_days(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_notification(self, new_doc)

Notify concerned people about recurring document generation

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_doc | None | - | - |


##### fetch_linked_contacts(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### disable_auto_repeat(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### notify_error_to_user(self, error_log)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| error_log | None | - | - |




## Functions

### get_next_date(dt, mcount, day = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| mcount | None | - | - |
| day | None | None | - |

**Returns**: (none)



### get_next_weekday(current_schedule_day, weekdays)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| current_schedule_day | None | - | - |
| weekdays | None | - | - |

**Returns**: (none)



### make_auto_repeat_entry()

**Returns**: (none)



### create_repeated_entries(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_auto_repeat_entries(date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| date | None | None | - |

**Returns**: (none)



### make_auto_repeat(doctype, docname, frequency = 'Daily', start_date = None, end_date = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| frequency | None | 'Daily' | - |
| start_date | None | None | - |
| end_date | None | None | - |

**Returns**: (none)



### get_auto_repeat_doctypes(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### update_reference(docname: str, reference: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |
| reference | str | - | - |

**Returns**: (none)



### generate_message_preview(name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | str | - | - |

**Returns**: (none)


