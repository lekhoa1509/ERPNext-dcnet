# API Reference: document_follow.py

**Language**: Python

**Source**: `form/document_follow.py`

---

## Functions

### update_follow(doctype: str, doc_name: str, following: bool)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| doc_name | str | - | - |
| following | bool | - | - |

**Returns**: (none)



### follow_document(doctype, doc_name, user)

param:
Doctype name
doc name
user email

condition:
avoided for some doctype
follow only if track changes are set to 1

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |
| user | None | - | - |

**Returns**: (none)



### unfollow_document(doctype, doc_name, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_message(doc_name, doctype, frequency, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc_name | None | - | - |
| doctype | None | - | - |
| frequency | None | - | - |
| user | None | - | - |

**Returns**: (none)



### send_email_alert(receiver, docinfo, timeline)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| receiver | None | - | - |
| docinfo | None | - | - |
| timeline | None | - | - |

**Returns**: (none)



### send_document_follow_mails(frequency)

param:
frequency for sanding mails

task:
set receiver according to frequency
group document list according to user
get changes, activity, comments on doctype
call method to send mail

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |

**Returns**: (none)



### get_user_list(frequency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |

**Returns**: (none)



### get_message_for_user(frequency, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_document_followed_by_user(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_version(doctype, doc_name, frequency, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |
| frequency | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_comments(doctype, doc_name, frequency, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |
| frequency | None | - | - |
| user | None | - | - |

**Returns**: (none)



### is_document_followed(doctype, doc_name, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_follow_users(doctype, doc_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| doc_name | None | - | - |

**Returns**: (none)



### get_row_changed(row_changed, time, doctype, doc_name, v)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row_changed | None | - | - |
| time | None | - | - |
| doctype | None | - | - |
| doc_name | None | - | - |
| v | None | - | - |

**Returns**: (none)



### get_added_row(added, time, doctype, doc_name, v)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| added | None | - | - |
| time | None | - | - |
| doctype | None | - | - |
| doc_name | None | - | - |
| v | None | - | - |

**Returns**: (none)



### get_field_changed(changed, time, doctype, doc_name, v)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| changed | None | - | - |
| time | None | - | - |
| doctype | None | - | - |
| doc_name | None | - | - |
| v | None | - | - |

**Returns**: (none)



### send_hourly_updates()

**Returns**: (none)



### send_daily_updates()

**Returns**: (none)



### send_weekly_updates()

**Returns**: (none)



### _get_filters(frequency, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |
| user | None | - | - |

**Returns**: (none)


