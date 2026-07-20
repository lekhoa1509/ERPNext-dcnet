# API Reference: task.py

**Language**: Python

**Source**: `doctype/task/task.py`

---

## Classes

### CircularReferenceError

**Inherits from**: frappe.ValidationError



### ParentIsGroupError

**Inherits from**: frappe.ValidationError



### Task

**Inherits from**: NestedSet

#### Methods

##### get_customer_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_default_end_date_if_missing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_expected_end_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_project_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_progress(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dependencies_for_template_task(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_template_task(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_depends_on_tasks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_completed_on(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_is_group(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_depends_on(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_nsm_model(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### unassign_todo(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_time_and_costing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_project(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_recursion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reschedule_dependent_tasks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_webform_permission(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### populate_depends_on(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_delete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### check_if_child_exists(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_project(doctype, txt, searchfield, start, page_len, filters)

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



### set_multiple_status(names, status)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| names | None | - | - |
| status | None | - | - |

**Returns**: (none)



### set_tasks_as_overdue()

**Returns**: (none)



### make_timesheet(source_name, target_doc = None, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| target_doc | None | None | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### get_children(doctype, parent, task = None, project = None, is_root = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| parent | None | - | - |
| task | None | None | - |
| project | None | None | - |
| is_root | None | False | - |

**Returns**: (none)



### add_node()

**Returns**: (none)



### add_multiple_tasks(data, parent)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| parent | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### set_missing_values(source, target)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |

**Returns**: (none)


