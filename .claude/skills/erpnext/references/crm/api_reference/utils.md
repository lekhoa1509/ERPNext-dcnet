# API Reference: utils.py

**Language**: Python

**Source**: `utils.py`

---

## Classes

### CRMNote

**Inherits from**: Document

#### Methods

##### add_note(self, note)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| note | None | - | - |


##### edit_note(self, note, row_id)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| note | None | - | - |
| row_id | None | - | - |


##### delete_note(self, row_id)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_id | None | - | - |




## Functions

### update_lead_phone_numbers(contact, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| contact | None | - | - |
| method | None | - | - |

**Returns**: (none)



### copy_comments(doctype, docname, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### link_communications(doctype, docname, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_linked_communication_list(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### link_communications_with_prospect(communication, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | None | - | - |
| method | None | - | - |

**Returns**: (none)



### update_modified_timestamp(communication, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| communication | None | - | - |
| method | None | - | - |

**Returns**: (none)



### get_linked_prospect(reference_doctype, reference_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | None | - | - |
| reference_name | None | - | - |

**Returns**: (none)



### link_events_with_prospect(event, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| event | None | - | - |
| method | None | - | - |

**Returns**: (none)



### link_open_tasks(ref_doctype, ref_docname, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### link_open_events(ref_doctype, ref_docname, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_open_activities(ref_doctype, ref_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |

**Returns**: (none)



### get_closed_todos(ref_doctype, ref_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |

**Returns**: (none)



### get_open_todos(ref_doctype, ref_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |

**Returns**: (none)



### get_open_events(ref_doctype, ref_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |

**Returns**: (none)



### get_closed_events(ref_doctype, ref_docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |

**Returns**: (none)



### get_filtered_todos(ref_doctype, ref_docname, status: str | tuple[str, str])

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |
| status | str | tuple[str, str] | - | - |

**Returns**: (none)



### get_filtered_events(ref_doctype, ref_docname, open: bool)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doctype | None | - | - |
| ref_docname | None | - | - |
| open | bool | - | - |

**Returns**: (none)



### open_leads_opportunities_based_on_todays_event()

**Returns**: (none)


