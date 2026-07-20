# API Reference: notification_settings.py

**Language**: Python

**Source**: `doctype/notification_settings/notification_settings.py`

---

## Classes

### NotificationSettings

**Inherits from**: Document

#### Methods

##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### is_notifications_enabled(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### is_email_notifications_enabled(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### is_email_notifications_enabled_for_type(user, notification_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| notification_type | None | - | - |

**Returns**: (none)



### create_notification_settings(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### toggle_notifications(user: str, enable: bool = False, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |
| enable | bool | False | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### get_subscribed_documents()

**Returns**: (none)



### get_permission_query_conditions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_permission(doc, ptype = 'read', user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| ptype | None | 'read' | - |
| user | None | None | - |

**Returns**: (none)



### set_seen_value(value, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| value | None | - | - |
| user | None | - | - |

**Returns**: (none)


