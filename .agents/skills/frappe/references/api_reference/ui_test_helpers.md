# API Reference: ui_test_helpers.py

**Language**: Python

**Source**: `tests/ui_test_helpers.py`

---

## Functions

### create_if_not_exists(doc)

Create records if they dont exist.
Will check for uniqueness by checking if a record exists with these field value pairs

:param doc: dict of field value pairs. can be a list of dict for multiple records.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### create_todo_records()

**Returns**: (none)



### prepare_webform_test()

**Returns**: (none)



### create_doctype_for_attachment()

**Returns**: (none)



### create_datetime_test_doctype()

**Returns**: (none)



### create_datetime_test_record()

**Returns**: (none)



### setup_workflow()

**Returns**: (none)



### create_contact_phone_nos_records()

**Returns**: (none)



### create_doctype(name, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| fields | None | - | - |

**Returns**: (none)



### create_child_doctype(name, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| fields | None | - | - |

**Returns**: (none)



### create_contact_records()

**Returns**: (none)



### create_multiple_todo_records()

**Returns**: (none)



### insert_contact(first_name, phone_number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| first_name | None | - | - |
| phone_number | None | - | - |

**Returns**: (none)



### create_form_tour()

**Returns**: (none)



### create_data_for_discussions()

**Returns**: (none)



### create_web_page(title, route, single_thread)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | None | - | - |
| route | None | - | - |
| single_thread | None | - | - |

**Returns**: (none)



### create_topic_and_reply(web_page)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| web_page | None | - | - |

**Returns**: (none)



### update_webform_to_multistep()

**Returns**: (none)



### update_child_table(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### insert_doctype_with_child_table_record(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### insert_translations()

**Returns**: (none)



### create_test_user(username = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| username | None | None | - |

**Returns**: (none)



### setup_tree_doctype()

**Returns**: (none)



### setup_image_doctype()

**Returns**: (none)



### setup_inbox()

**Returns**: (none)



### setup_default_view(view, force_reroute = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| view | None | - | - |
| force_reroute | None | None | - |

**Returns**: (none)



### create_kanban()

**Returns**: (none)



### create_todo(description)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| description | None | - | - |

**Returns**: (none)



### create_todo_with_attachment_limit(description)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| description | None | - | - |

**Returns**: (none)



### create_admin_kanban()

**Returns**: (none)



### add_remove_role(action, user, role)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| action | None | - | - |
| user | None | - | - |
| role | None | - | - |

**Returns**: (none)



### publish_realtime(event = None, message = None, room = None, user = None, doctype = None, docname = None, task_id = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | None | - |
| message | None | None | - |
| room | None | None | - |
| user | None | None | - |
| doctype | None | None | - |
| docname | None | None | - |
| task_id | None | None | - |

**Returns**: (none)



### publish_progress(duration = 3, title = None, doctype = None, docname = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| duration | None | 3 | - |
| title | None | None | - |
| doctype | None | None | - |
| docname | None | None | - |

**Returns**: (none)



### slow_task(duration, title, doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| duration | None | - | - |
| title | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### empty_my_workspaces()

**Returns**: (none)



### insert_child(doc, data, barcode, check, rating, duration, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| data | None | - | - |
| barcode | None | - | - |
| check | None | - | - |
| rating | None | - | - |
| duration | None | - | - |
| date | None | - | - |

**Returns**: (none)


