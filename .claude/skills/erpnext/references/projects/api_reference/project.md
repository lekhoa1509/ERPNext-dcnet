# API Reference: project.py

**Language**: Python

**Source**: `doctype/project/project.py`

---

## Classes

### Project

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_print(self, settings = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| settings | None | None | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### copy_from_template(self)

Copy tasks from template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### create_task_from_template(self, task_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task_details | None | - | - |


##### calculate_start_date(self, task_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task_details | None | - | - |


##### calculate_end_date(self, task_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| task_details | None | - | - |


##### update_if_holiday(self, date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| date | None | - | - |


##### dependency_mapping(self, template_tasks, project_tasks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template_tasks | None | - | - |
| project_tasks | None | - | - |


##### check_depends_on_value(self, template_task, project_task, project_tasks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template_task | None | - | - |
| project_task | None | - | - |
| project_tasks | None | - | - |


##### check_for_parent_tasks(self, template_task, project_task, project_tasks)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| template_task | None | - | - |
| project_task | None | - | - |
| project_tasks | None | - | - |


##### is_row_updated(self, row, existing_task_data, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| existing_task_data | None | - | - |
| fields | None | - | - |


##### update_project(self)

Called externally by Task

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_percent_complete(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_costing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### calculate_gross_margin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_purchase_costing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_sales_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_billed_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_billed_amount_from_parent(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_billed_amount_from_child(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_rename(self, old_name, new_name, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |
| merge | None | False | - |


##### send_welcome_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_timeline_data(doctype: str, name: str) → dict[int, int]

Return timeline for attendance

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `dict[int, int]`



### get_project_list(doctype, txt, filters, limit_start, limit_page_length = 20, order_by = 'creation')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| filters | None | - | - |
| limit_start | None | - | - |
| limit_page_length | None | 20 | - |
| order_by | None | 'creation' | - |

**Returns**: (none)



### get_list_context(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### get_users_for_project(doctype, txt, searchfield, start, page_len, filters)

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



### get_cost_center_name(project)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | None | - | - |

**Returns**: (none)



### hourly_reminder()

**Returns**: (none)



### project_status_update_reminder()

**Returns**: (none)



### daily_reminder()

**Returns**: (none)



### twice_daily_reminder()

**Returns**: (none)



### weekly_reminder()

**Returns**: (none)



### allow_to_make_project_update(project, time, frequency)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | None | - | - |
| time | None | - | - |
| frequency | None | - | - |

**Returns**: (none)



### create_duplicate_project(prev_doc, project_name)

Create duplicate project based on the old project

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| prev_doc | None | - | - |
| project_name | None | - | - |

**Returns**: (none)



### get_projects_for_collect_progress(frequency, fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frequency | None | - | - |
| fields | None | - | - |

**Returns**: (none)



### send_project_update_email_to_users(project)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | None | - | - |

**Returns**: (none)



### collect_project_status()

**Returns**: (none)



### send_project_status_email_to_users()

**Returns**: (none)



### update_project_sales_billing()

**Returns**: (none)



### create_kanban_board_if_not_exists(project)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | None | - | - |

**Returns**: (none)



### set_project_status(project, status)

set status for project and all related tasks

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | None | - | - |
| status | None | - | - |

**Returns**: (none)



### get_holiday_list(company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | None | - |

**Returns**: (none)



### get_users_email(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### calculate_total_purchase_cost(project: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | str | None | None | - |

**Returns**: (none)



### update_costing_and_billing(project: str | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| project | str | None | None | - |

**Returns**: (none)


