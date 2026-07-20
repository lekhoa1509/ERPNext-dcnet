# API Reference: load.py

**Language**: Python

**Source**: `form/load.py`

---

## Functions

### getdoc(doctype, name)

Loads a doclist for a given document. This method is called directly from the client.
Requires "doctype", "name" as form variables.
Will also call the "onload" method on the document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### getdoctype(doctype, with_parent = False)

load doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| with_parent | None | False | - |

**Returns**: (none)



### get_meta_bundle(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### get_docinfo(doc = None, doctype = None, name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | None | - |
| doctype | None | None | - |
| name | None | None | - |

**Returns**: (none)



### add_comments(doc, docinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| docinfo | None | - | - |

**Returns**: (none)



### get_milestones(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_attachments(dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### get_versions(doc: 'Document') → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `list[dict]`



### get_communications(doctype, name, start = 0, limit = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| start | None | 0 | - |
| limit | None | 20 | - |

**Returns**: (none)



### get_comments(doctype: str, name: str, comment_type: str | list[str] = 'Comment') → list[frappe._dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| comment_type | str | list[str] | 'Comment' | - |

**Returns**: `list[frappe._dict]`



### _get_communications(doctype, name, start = 0, limit = 20)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| start | None | 0 | - |
| limit | None | 20 | - |

**Returns**: (none)



### get_communication_data(doctype, name, start = 0, limit = 20, after = None, fields = None, group_by = None, as_dict = True)

Return list of communications for a given document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| start | None | 0 | - |
| limit | None | 20 | - |
| after | None | None | - |
| fields | None | None | - |
| group_by | None | None | - |
| as_dict | None | True | - |

**Returns**: (none)



### get_assignments(dt, dn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dt | None | - | - |
| dn | None | - | - |

**Returns**: (none)



### run_onload(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_view_logs(doc: 'Document') → list[dict]

get and return the latest view logs if available

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |

**Returns**: `list[dict]`



### get_tags(doctype: str, name: str) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `str`



### get_document_email(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_additional_timeline_content(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### set_link_titles(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_title_values_for_link_and_dynamic_link_fields(doc, link_fields = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| link_fields | None | None | - |

**Returns**: (none)



### get_title_values_for_table_and_multiselect_fields(doc, table_fields = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| table_fields | None | None | - |

**Returns**: (none)



### send_link_titles(link_titles)

Append link titles dict in `frappe.local.response`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| link_titles | None | - | - |

**Returns**: (none)



### update_user_info(docinfo, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docinfo | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### get_user_info_for_viewers(users)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| users | None | - | - |

**Returns**: (none)


