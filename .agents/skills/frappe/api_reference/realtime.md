# API Reference: realtime.py

**Language**: Python

**Source**: `realtime.py`

---

## Functions

### publish_progress(percent, title = None, doctype = None, docname = None, description = None, task_id = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| percent | None | - | - |
| title | None | None | - |
| doctype | None | None | - |
| docname | None | None | - |
| description | None | None | - |
| task_id | None | None | - |

**Returns**: (none)



### publish_realtime(event: str | None = None, message: dict | None = None, room: str | None = None, user: str | None = None, doctype: str | None = None, docname: str | None = None, task_id: str | None = None, after_commit: bool = False)

Publish real-time updates

:param event: Event name, like `task_progress` etc. that will be handled by the client (default is `task_progress` if within task or `global`)
:param message: JSON message object. For async must contain `task_id`
:param room: Room in which to publish update (default entire site)
:param user: Transmit to user
:param doctype: Transmit to doctype, docname
:param docname: Transmit to doctype, docname
:param after_commit: (default False) will emit after current transaction is committed

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | str | None | None | - |
| message | dict | None | None | - |
| room | str | None | None | - |
| user | str | None | None | - |
| doctype | str | None | None | - |
| docname | str | None | None | - |
| task_id | str | None | None | - |
| after_commit | bool | False | - |

**Returns**: (none)



### flush_realtime_log()

**Returns**: (none)



### clear_realtime_log()

**Returns**: (none)



### emit_via_redis(event, message, room)

Publish real-time updates via redis

:param event: Event name, like `task_progress` etc.
:param message: JSON message object. For async must contain `task_id`
:param room: name of the room

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |
| message | None | - | - |
| room | None | - | - |

**Returns**: (none)



### has_permission(doctype: str, name: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `bool`



### get_user_info()

**Returns**: (none)



### get_doctype_room(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_doc_room(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### get_user_room(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### get_site_room()

**Returns**: (none)



### get_task_progress_room(task_id)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| task_id | None | - | - |

**Returns**: (none)



### get_website_room()

**Returns**: (none)


