# How To: Dashboard Chart

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test dashboard chart

## Prerequisites

**Required Modules:**
- `datetime`
- `unittest.mock`
- `dateutil.relativedelta`
- `frappe`
- `frappe.core.doctype.doctype.test_doctype`
- `frappe.desk.doctype.dashboard_chart.dashboard_chart`
- `frappe.tests`
- `frappe.utils`
- `frappe.utils.dateutils`


## Step-by-Step Guide

### Step 1: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Dashboard Chart', chart_type='Count', document_type='DocType', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='{}', timeseries=1).insert()
```

### Step 2: Assign cur_date = value

```python
cur_date = datetime.now() - relativedelta(years=1)
```

### Step 3: Assign result = get(...)

```python
result = get(chart_name='Test Dashboard Chart', refresh=1)
```

### Step 4: Call frappe.delete_doc()

```python
frappe.delete_doc('Dashboard Chart', 'Test Dashboard Chart')
```

### Step 5: Assign month = get_last_day(...)

```python
month = get_last_day(cur_date)
```

### Step 6: Assign month = formatdate(...)

```python
month = formatdate(month.strftime('%Y-%m-%d'))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(result.get('labels')[idx], get_period(month))
```


## Complete Example

```python
# Workflow
if frappe.db.exists('Dashboard Chart', 'Test Dashboard Chart'):
    frappe.delete_doc('Dashboard Chart', 'Test Dashboard Chart')
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Dashboard Chart', chart_type='Count', document_type='DocType', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='{}', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Dashboard Chart', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
```

## Next Steps


---

*Source: test_dashboard_chart.py:59 | Complexity: Intermediate | Last updated: 2026-02-04*