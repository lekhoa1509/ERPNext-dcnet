# API Reference: notification_log.py

**Language**: Python

**Source**: `doctype/notification_log/notification_log.py`

---

## Classes

### NotificationLog

**Inherits from**: Document

#### Methods

##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_old_logs(days = 180)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| days | None | 180 | - |




## Functions

### get_permission_query_conditions(for_user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| for_user | None | - | - |

**Returns**: (none)



### get_title(doctype, docname, title_field = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| title_field | None | None | - |

**Returns**: (none)



### get_title_html(title)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | None | - | - |

**Returns**: (none)



### enqueue_create_notification(users: list[str] | str, doc: dict)

Send notification to users.

users: list of user emails or string of users with comma separated emails
doc: contents of `Notification` doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| users | list[str] | str | - | - |
| doc | dict | - | - |

**Returns**: (none)



### make_notification_logs(doc, users)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| users | None | - | - |

**Returns**: (none)



### _get_user_ids(user_emails)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user_emails | None | - | - |

**Returns**: (none)



### send_notification_email(doc: NotificationLog)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | NotificationLog | - | - |

**Returns**: (none)



### get_email_header(doc, language: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| language | str | None | None | - |

**Returns**: (none)



### format_email_header(header_map, language, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| header_map | None | - | - |
| language | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### get_notification_logs(limit: int = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| limit | int | 20 | - |

**Returns**: (none)



### mark_all_as_read()

**Returns**: (none)



### mark_as_read(docname: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docname | str | - | - |

**Returns**: (none)



### trigger_indicator_hide()

**Returns**: (none)



### set_notifications_as_unseen(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)


