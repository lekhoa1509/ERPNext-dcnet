<!-- Source: erpnext_projects skill -->

# ERPNext Projects Module

## Description

The ERPNext Projects module provides comprehensive project management capabilities within ERPNext. It enables organizations to manage projects, track tasks with dependencies, log time via timesheets, calculate project costs and billing, and generate project reports.

**Source:** ERPNext v16 Codebase Analysis
**Files Analyzed:** 40
**Languages:** Python (90%), JavaScript (10%)
**Confidence Level:** High (direct codebase analysis)

---

## When to Use This Skill

Use this skill when you need to:

### Project Management
- Create and manage projects (internal or external)
- Set up project templates for repeatable project structures
- Track project progress and completion percentage
- Link projects to Sales Orders for billing
- Calculate project costing and gross margin

### Task Management
- Create tasks with dependencies (depends_on relationships)
- Set up parent-child task hierarchies (nested tasks)
- Track task status, priority, and expected dates
- Validate task dates against project dates
- Use template tasks for standardized workflows

### Time Tracking & Billing
- Log employee time via Timesheets
- Calculate billable vs. non-billable hours
- Set costing and billing rates per activity type
- Generate Sales Invoices from timesheets
- Track percentage billed for projects

### Reporting
- Daily Timesheet Summary reports
- Delayed Tasks Summary with chart visualization
- Project Summary reports
- Project-wise Stock Tracking
- Timesheet Billing Summary

---

## Key Concepts

### DocTypes Overview

| DocType | Purpose | Key Fields |
|---------|---------|------------|
| **Project** | Main project container | `project_name`, `status`, `expected_start_date`, `expected_end_date`, `percent_complete` |
| **Task** | Work items within projects | `subject`, `project`, `status`, `exp_start_date`, `exp_end_date`, `depends_on` |
| **Project Template** | Reusable project structure | `template_name`, tasks (child table) |
| **Timesheet** | Time logging document | `employee`, `time_logs` (child table), `total_hours`, `total_billable_amount` |
| **Activity Type** | Categories for time logs | `activity_type`, `billing_rate`, `costing_rate` |
| **Activity Cost** | Employee-specific rates | `employee`, `activity_type`, `billing_rate`, `costing_rate` |

### Project Status Flow

```
Open → Working → Pending Review → Overdue → Completed → Cancelled
```

### Task Hierarchy

Tasks support a **Nested Set** structure:
- **Group Tasks** (`is_group=1`): Container tasks with child tasks
- **Child Tasks**: Tasks with `parent_task` reference
- **Dependent Tasks**: Tasks with `depends_on` relationships

### Time Log Flow

```
Employee → Timesheet → Time Logs → Activity Type → Billing/Costing Rates
                ↓
        Project → total_billable_amount, total_costing_amount
                ↓
        Sales Invoice (optional)
```

---

## Quick Reference

### 1. Create a Project (From Codebase)

```python
import frappe

# Create a basic project
project = frappe.get_doc({
    'doctype': 'Project',
    'project_name': 'Website Redesign',
    'status': 'Open',
    'expected_start_date': frappe.utils.nowdate(),
    'company': 'My Company'
})
project.insert()
```

### 2. Create a Task with Dependencies (From Codebase)

```python
import frappe

# Create a parent task (group)
parent_task = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'Development Phase',
    'project': 'PROJ-0001',
    'is_group': 1,
    'exp_start_date': '2024-01-01',
    'exp_end_date': '2024-01-31'
})
parent_task.insert()

# Create a child task
child_task = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'Setup Database',
    'project': 'PROJ-0001',
    'parent_task': parent_task.name,
    'exp_start_date': '2024-01-01',
    'exp_end_date': '2024-01-05'
})
child_task.insert()

# Create a dependent task
dependent_task = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'Create API Endpoints',
    'project': 'PROJ-0001',
    'depends_on': [{'task': child_task.name}],
    'exp_start_date': '2024-01-06',
    'exp_end_date': '2024-01-10'
})
dependent_task.insert()
```

### 3. Create Project from Template (From Test Suite)

```python
import frappe

# Create template tasks
template_task = frappe.get_doc({
    'doctype': 'Task',
    'subject': 'Initial Setup',
    'is_template': 1,
    'begin': 0,      # Days from project start
    'duration': 5    # Task duration in days
})
template_task.insert()

# Create project template
template = frappe.get_doc({
    'doctype': 'Project Template',
    'template_name': 'Standard Implementation',
    'tasks': [{'task': template_task.name}]
})
template.insert()

# Create project from template
project = frappe.get_doc({
    'doctype': 'Project',
    'project_name': 'Client Implementation',
    'project_template': template.name,
    'expected_start_date': frappe.utils.nowdate()
})
project.insert()
# Tasks are automatically created from template with calculated dates
```

### 4. Log Time with Timesheet (From Test Suite)

```python
import frappe
from frappe.utils import now_datetime, add_to_date

# Create a timesheet with time logs
timesheet = frappe.get_doc({
    'doctype': 'Timesheet',
    'employee': 'HR-EMP-00001',
    'time_logs': [{
        'activity_type': 'Development',
        'from_time': now_datetime(),
        'to_time': add_to_date(now_datetime(), hours=4),
        'hours': 4,
        'project': 'PROJ-0001',
        'is_billable': 1,
        'billing_hours': 4,
        'billing_rate': 100,
        'costing_rate': 50
    }]
})
timesheet.insert()
timesheet.submit()

# Project automatically updates costing/billing amounts
project = frappe.get_doc('Project', 'PROJ-0001')
print(f"Billable: {project.total_billable_amount}")
print(f"Costing: {project.total_costing_amount}")
```

### 5. Set Activity Cost per Employee

```python
import frappe

# Set custom rates for specific employee-activity combinations
activity_cost = frappe.get_doc({
    'doctype': 'Activity Cost',
    'employee': 'HR-EMP-00001',
    'activity_type': 'Consulting',
    'billing_rate': 150,
    'costing_rate': 75
})
activity_cost.insert()
# Note: Validates uniqueness - one entry per employee-activity pair
```

### 6. Query Tasks for a Project

```python
import frappe

# Get all tasks for a project with dependencies
tasks = frappe.get_all('Task',
    filters={'project': 'PROJ-0001'},
    fields=['name', 'subject', 'status', 'exp_end_date',
            'depends_on_tasks', 'parent_task', 'progress'],
    order_by='creation asc'
)

for task in tasks:
    print(f"{task.subject}: {task.status} - {task.progress}%")
```

### 7. Generate Sales Invoice from Timesheet

```python
import frappe

# Enable timesheet fetching in Sales Invoice
# Projects Settings > Fetch timesheet in Sales Invoice = 1

# Then create Sales Invoice linked to project
sales_invoice = frappe.get_doc({
    'doctype': 'Sales Invoice',
    'customer': 'Customer Name',
    'project': 'PROJ-0001',
    # Timesheets auto-populated based on project
})
```

---

## API Reference

### Project Class Methods

| Method | Description |
|--------|-------------|
| `validate()` | Validates project data |
| `copy_from_template()` | Creates tasks from project template |
| `update_project()` | Called by Task to update project stats |
| `update_percent_complete()` | Recalculates completion percentage |
| `update_costing()` | Updates costing from timesheets |
| `calculate_gross_margin()` | Calculates margin based on billing vs costing |
| `update_purchase_costing()` | Updates costs from Purchase Orders |

### Task Class Methods

| Method | Description |
|--------|-------------|
| `validate_dates()` | Ensures dates are valid |
| `validate_depends_on_tasks()` | Checks for circular dependencies |
| `validate_parent_is_group()` | Ensures parent task is a group |
| `update_depends_on()` | Updates dependent tasks list |
| `update_nsm_model()` | Maintains nested set structure |
| `on_update()` | Triggers project update |

### Timesheet Class Methods

| Method | Description |
|--------|-------------|
| `validate()` | Validates timesheet data |
| `calculate_hours()` | Computes total hours |
| `calculate_total_amounts()` | Computes billing/costing totals |
| `validate_overlap()` | Checks for time log overlaps |
| `update_task_and_project()` | Updates linked task/project |
| `on_submit()` | Finalizes timesheet calculations |

### Error Classes

| Class | Raised When |
|-------|------------|
| `CircularReferenceError` | Task depends on itself (directly or indirectly) |
| `ParentIsGroupError` | Parent task is not a group task |
| `OverlapError` | Timesheet time logs overlap |
| `OverWorkLoggedError` | More time logged than available |
| `DuplicationError` | Duplicate Activity Cost entry |

---

## Configuration

### Projects Settings

Located at: **Setup > Settings > Projects Settings**

| Setting | Purpose |
|---------|---------|
| `ignore_workstation_time_overlap` | Allow overlapping timesheets |
| `fetch_timesheet_in_sales_invoice` | Auto-fetch timesheets when creating SI |

### DocType JSON Configuration

Key configuration files in `doctype/*/` folders:

| File | DocType | Settings Count |
|------|---------|---------------|
| `project.json` | Project | 24 |
| `task.json` | Task | 23 |
| `timesheet.json` | Timesheet | 21 |
| `activity_cost.json` | Activity Cost | 20 |
| `project_template.json` | Project Template | 20 |

---

## Reports

### Daily Timesheet Summary

**Path:** `report/daily_timesheet_summary/`

```python
from erpnext.projects.report.daily_timesheet_summary import daily_timesheet_summary

# Execute report
columns, data = daily_timesheet_summary.execute(filters={
    'from_date': '2024-01-01',
    'to_date': '2024-01-31'
})
```

### Delayed Tasks Summary

**Path:** `report/delayed_tasks_summary/`

Features:
- Lists tasks past their expected end date
- Includes chart visualization
- Filterable by project, status

```python
from erpnext.projects.report.delayed_tasks_summary import delayed_tasks_summary

columns, data = delayed_tasks_summary.execute(filters={
    'project': 'PROJ-0001'
})
```

### Project Summary

**Path:** `report/project_summary/`

Aggregates project statistics:
- Task counts by status
- Total hours logged
- Billing vs costing amounts

### Project-wise Stock Tracking

**Path:** `report/project_wise_stock_tracking/`

Tracks inventory movements linked to projects:
- Purchased items cost
- Issued items cost
- Delivered items cost

### Timesheet Billing Summary

**Path:** `report/timesheet_billing_summary/`

Summarizes timesheet billing:
- Groupable by employee, project, or activity
- Shows billable hours vs actual hours

---

## Design Patterns

### Observer Pattern (3 instances)

Used for event-driven updates:
- Task update triggers Project update
- Timesheet submit triggers Project costing update
- Activity Cost validates uniqueness

### Factory Pattern (1 instance)

Used in Project Template:
- `copy_from_template()` creates Task documents from template definition

### Nested Set Model

Task hierarchy uses Frappe's NestedSet:
- Efficient tree traversal
- Parent-child relationships
- `lft` and `rgt` fields for ordering

---

## Working with This Skill

### For Beginners

1. **Start with Projects**: Create a simple project first
2. **Add Tasks**: Create basic tasks without dependencies
3. **Log Time**: Create timesheets to track work
4. **View Reports**: Use built-in reports to see progress

### For Intermediate Users

1. **Use Templates**: Set up project templates for common workflows
2. **Task Dependencies**: Create dependency chains between tasks
3. **Activity Costs**: Configure employee-specific billing rates
4. **Sales Integration**: Link projects to Sales Orders

### For Advanced Users

1. **Custom Validation**: Extend Task/Project classes for custom rules
2. **Reporting Customization**: Modify report scripts for custom metrics
3. **Integration**: Connect to external project management tools
4. **Automation**: Use Server Scripts for automated project workflows

---

## Available Reference Files

### API Reference (`references/api_reference/`)

| File | Description | Confidence |
|------|-------------|------------|
| `project.md` | Project DocType API with all methods | Medium |
| `task.md` | Task DocType API with NestedSet methods | Medium |
| `timesheet.md` | Timesheet DocType API with validation | Medium |
| `timesheet_detail.md` | Time log entry API | Medium |
| `project_template.md` | Template API with dependency validation | Medium |
| `activity_cost.md` | Activity cost management API | Medium |
| `activity_type.md` | Activity type configuration | Medium |

### Reports (`references/api_reference/`)

| File | Description |
|------|-------------|
| `daily_timesheet_summary.md` | Daily time log report |
| `delayed_tasks_summary.md` | Overdue tasks report |
| `project_summary.md` | Project statistics report |
| `project_wise_stock_tracking.md` | Inventory tracking per project |
| `timesheet_billing_summary.md` | Billing aggregation report |

### Test Examples (`references/test_examples/`)

Real-world usage patterns extracted from test suite:
- Project creation with templates
- Task dependency management
- Timesheet billing scenarios
- Report generation examples

### Configuration (`references/config_patterns/`)

DocType JSON configurations for all Projects module doctypes.

---

## Common Patterns

### Link Project to Sales Order

```python
# In Sales Order, set project field
sales_order.project = project.name
sales_order.save()

# Project automatically tracks:
# - total_sales_amount
# - gross_margin
```

### Calculate Project Completion

```python
# Completion is calculated based on:
# 1. Task-based: % of completed tasks
# 2. Time-based: If no tasks, manual completion tracking

project = frappe.get_doc('Project', 'PROJ-0001')
project.update_percent_complete()
print(f"Completion: {project.percent_complete}%")
```

### Reschedule Dependent Tasks

```python
# When a task's end date changes, dependent tasks can be rescheduled
task = frappe.get_doc('Task', 'TASK-0001')
task.exp_end_date = '2024-01-15'
task.save()
# Dependent tasks validate against this new date
```

---

## Integration Points

### With ERPNext Modules

| Module | Integration |
|--------|------------|
| **HR** | Employee linked to Timesheets |
| **Selling** | Sales Orders linked to Projects |
| **Buying** | Purchase Orders track project costs |
| **Accounting** | Project-wise P&L reporting |
| **Stock** | Stock movements linked to projects |

### Webhooks & Events

```python
# In hooks.py
doc_events = {
    "Task": {
        "on_update": "myapp.task_handler.on_task_update"
    },
    "Project": {
        "after_insert": "myapp.project_handler.setup_project"
    }
}
```

---

## Troubleshooting

### Circular Reference Error

**Cause:** Task A depends on Task B, which depends on Task A

**Solution:** Review and break the dependency cycle

```python
# Check task dependencies
task = frappe.get_doc('Task', 'TASK-0001')
print(task.depends_on)  # List of dependent tasks
```

### Overlap Error in Timesheets

**Cause:** Two time logs overlap for the same employee

**Solution:** Adjust time log start/end times, or enable overlap setting

```python
# In Projects Settings
frappe.db.set_value('Projects Settings', None,
    'ignore_workstation_time_overlap', 1)
```

### Project Not Updating Costs

**Cause:** Timesheet not submitted, or project link missing

**Solution:** Ensure timesheet is submitted with valid project link

```python
timesheet = frappe.get_doc('Timesheet', 'TS-0001')
for log in timesheet.time_logs:
    print(f"Project: {log.project}")  # Must have project
timesheet.submit()  # Must be submitted
```

---

**Source:** ERPNext v16 Codebase Analysis
**Analysis Depth:** Full (API, Tests, Configuration, Documentation)
**Last Updated:** Based on codebase snapshot
**Generated by:** Skill Seeker | Codebase Analyzer
