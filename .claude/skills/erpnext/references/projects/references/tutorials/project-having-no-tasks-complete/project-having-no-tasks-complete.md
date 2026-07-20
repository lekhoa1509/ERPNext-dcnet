# How To: Project Having No Tasks Complete

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test project having no tasks complete

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

### Step 1: Assign project_name = 'Test Project - No Tasks Completion'

```python
project_name = 'Test Project - No Tasks Completion'
```

### Step 2: Call frappe.db.sql()

```python
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
```

### Step 3: Call frappe.delete_doc()

```python
frappe.delete_doc('Project', project_name)
```

### Step 4: Assign project = frappe.get_doc.insert(...)

```python
project = frappe.get_doc({'doctype': 'Project', 'project_name': project_name, 'status': 'Open', 'expected_start_date': nowdate(), 'company': '_Test Company'}).insert()
```

### Step 5: Assign tasks = frappe.get_all(...)

```python
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name', 'parent_task'], dict(project=project.name), order_by='creation asc')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(project.status, 'Open')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(tasks), 0)
```

### Step 8: Assign project.status = 'Completed'

```python
project.status = 'Completed'
```

### Step 9: Call project.save()

```python
project.save()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(project.status, 'Completed')
```


## Complete Example

```python
# Workflow
project_name = 'Test Project - No Tasks Completion'
frappe.db.sql(' delete from tabTask where project = %s ', project_name)
frappe.delete_doc('Project', project_name)
project = frappe.get_doc({'doctype': 'Project', 'project_name': project_name, 'status': 'Open', 'expected_start_date': nowdate(), 'company': '_Test Company'}).insert()
tasks = frappe.get_all('Task', ['subject', 'exp_end_date', 'depends_on_tasks', 'name', 'parent_task'], dict(project=project.name), order_by='creation asc')
self.assertEqual(project.status, 'Open')
self.assertEqual(len(tasks), 0)
project.status = 'Completed'
project.save()
self.assertEqual(project.status, 'Completed')
```

## Next Steps


---

*Source: test_project.py:226 | Complexity: Advanced | Last updated: 2026-02-04*