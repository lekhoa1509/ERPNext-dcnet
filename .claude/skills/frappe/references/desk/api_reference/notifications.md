# API Reference: notifications.py

**Language**: Python

**Source**: `notifications.py`

---

## Functions

### get_notifications()

**Returns**: (none)



### get_notifications_for_doctypes(config, notification_count)

Notifications for DocTypes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| config | None | - | - |
| notification_count | None | - | - |

**Returns**: (none)



### get_notifications_for_targets(config, notification_percent)

Notifications for doc targets

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| config | None | - | - |
| notification_percent | None | - | - |

**Returns**: (none)



### clear_notifications(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### clear_notification_config(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### delete_notification_count_for(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### clear_doctype_notifications(doc, method = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | None | - |

**Returns**: (none)



### get_notification_info()

**Returns**: (none)



### get_notification_config()

**Returns**: (none)



### get_filters_for(doctype)

get open filters for doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_open_count(doctype: str, name: str, items = None)

Get count for internal and external links for given transactions

:param doctype: Reference DocType
:param name: Reference Name
:param items: Optional list of transactions (json/dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| items | None | None | - |

**Returns**: (none)



### _get_linked_document_counts(doctype: str, name: str, items = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| items | None | None | - |

**Returns**: (none)



### get_internal_links(doc, link, link_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| link | None | - | - |
| link_doctype | None | - | - |

**Returns**: (none)



### get_external_links(doctype, name, links)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| links | None | - | - |

**Returns**: (none)



### get_doc_count(doctype, filters) → int | Literal['?']

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| filters | None | - | - |

**Returns**: `int | Literal['?']`



### get_dynamic_link_filters(doctype, links, fieldname)

- Updating filters based on dynamic_links specified in the dashboard data.
- Eg: "dynamic_links": {"fieldname": ["dynamic_fieldvalue", "dynamic_fieldname"]},

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| links | None | - | - |
| fieldname | None | - | - |

**Returns**: (none)



### notify_mentions(ref_doctype, ref_name, content)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_name | None | - | - |
| content | None | - | - |

**Returns**: (none)



### extract_mentions(txt)

Find all instances of @mentions in the html.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| txt | None | - | - |

**Returns**: (none)



### _get()

**Returns**: (none)


