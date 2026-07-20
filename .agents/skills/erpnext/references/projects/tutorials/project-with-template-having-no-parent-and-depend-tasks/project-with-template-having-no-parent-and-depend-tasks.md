# How To: Project With Template Having No Parent And Depend Tasks

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project with template having no parent and depend tasks

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.utils`
- `erpnext.projects.doctype.project_template.test_project_template`
- `erpnext.projects.doctype.task.test_task`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.tests.utils`
- `erpnext.projects.doctype.timesheet.test_timesheet`
- `erpnext.setup.doctype.employee.test_employee`


## Step-by-Step Guide

### Step 1: Assign project_name = 'Test Project with Template - No Parent and Dependend Tasks'

```python
project_name = 'Test Project with Template - No Parent and Dependend Tasks'
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
```

### Step 3: Call frappe.delete_doc()

```python
frappe.delete_doc('Project', project_name)
```

### Step 4: Assign task1 = task_exists(...)

```python
task1 = task_exists('Test Template Task with No Parent and Dependency')
```

### Step 5: Assign template = make_project_template(...)

```python
template = make_project_template('Test Project Template - No Parent and Dependend Tasks', [task1])
```

### Step 6: Assign project = get_project(...)

```python
project = get_project(project_name, template)
```

### Step 7: Assign tasks = frappe.get_all(...)

```python
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'priority'], dict(project=project.name), order_by='creation asc')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(tasks[0].priority, 'High')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(tasks[0].subject, 'Test Template Task with No Parent and Dependency')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 5, 3))
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(tasks), 1)
```

### Step 12: Assign task1 = create_task(...)

```python
task1 = create_task(subject='Test Template Task with No Parent and Dependency', is_template=1, begin=5, duration=3, priority='High')
```


## Complete Example

```python
# Workflow
project_name = 'Test Project with Template - No Parent and Dependend Tasks'
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
task1 = task_exists('Test Template Task with No Parent and Dependency')
if not task1:
    task1 = create_task(subject='Test Template Task with No Parent and Dependency', is_template=1, begin=5, duration=3, priority='High')
template = make_project_template('Test Project Template - No Parent and Dependend Tasks', [task1])
project = get_project(project_name, template)
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'priority'], dict(project=project.name), order_by='creation asc')
self.assertEqual(tasks[0].priority, 'High')
self.assertEqual(tasks[0].subject, 'Test Template Task with No Parent and Dependency')
self.assertEqual(getdate(tasks[0].exp_end_date), calculate_end_date(project, 5, 3))
self.assertEqual(len(tasks), 1)
```

## Next Steps


---

*Source: test_project.py:42 | Complexity: Advanced | Last updated: 2026-02-04*