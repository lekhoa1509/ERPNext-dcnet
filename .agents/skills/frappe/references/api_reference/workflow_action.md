# API Reference: workflow_action.py

**Language**: Python

**Source**: `workflow/doctype/workflow_action/workflow_action.py`

---

## Classes

### WorkflowAction

**Inherits from**: Document



## Functions

### on_doctype_update()

**Returns**: (none)



### get_permission_query_conditions(user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |

**Returns**: (none)



### has_permission(doc, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | - | - |

**Returns**: (none)



### process_workflow_actions(doc, state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| state | None | - | - |

**Returns**: (none)



### apply_action(action, doctype, docname, current_state, user = None, last_modified = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| action | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| current_state | None | - | - |
| user | None | None | - |
| last_modified | None | None | - |

**Returns**: (none)



### confirm_action(doctype, docname, user, action)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |
| user | None | - | - |
| action | None | - | - |

**Returns**: (none)



### return_success_page(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### return_action_confirmation_page(doc, action, action_link, alert_doc_change = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| action | None | - | - |
| action_link | None | - | - |
| alert_doc_change | None | False | - |

**Returns**: (none)



### return_link_expired_page(doc, doc_workflow_state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| doc_workflow_state | None | - | - |

**Returns**: (none)



### update_completed_workflow_actions(doc, user = None, workflow = None, workflow_state = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| user | None | None | - |
| workflow | None | None | - |
| workflow_state | None | None | - |

**Returns**: (none)



### get_allowed_roles(user, workflow, workflow_state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | - | - |
| workflow | None | - | - |
| workflow_state | None | - | - |

**Returns**: (none)



### get_workflow_action_by_role(doc, allowed_roles)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| allowed_roles | None | - | - |

**Returns**: (none)



### update_completed_workflow_actions_using_role(user = None, workflow_action = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |
| workflow_action | None | None | - |

**Returns**: (none)



### get_next_possible_transitions(workflow_name, state, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workflow_name | None | - | - |
| state | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### get_users_next_action_data(transitions, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| transitions | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### create_workflow_actions_for_roles(roles, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| roles | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### send_workflow_action_email(doc, transitions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| transitions | None | - | - |

**Returns**: (none)



### deduplicate_actions(action_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| action_list | None | - | - |

**Returns**: (none)



### get_workflow_action_url(action, doc, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| action | None | - | - |
| doc | None | - | - |
| user | None | - | - |

**Returns**: (none)



### get_confirm_workflow_action_url(doc, action, user)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| action | None | - | - |
| user | None | - | - |

**Returns**: (none)



### is_workflow_action_already_created(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### clear_workflow_actions(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_doc_workflow_state(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_common_email_args(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_email_template_from_workflow(doc)

Return next_action_email_template for workflow state (if available) based on doc current workflow state.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_state_optional_field_value(workflow_name, state)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| workflow_name | None | - | - |
| state | None | - | - |

**Returns**: (none)



### user_has_permission(user: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | - | - |

**Returns**: `bool`


