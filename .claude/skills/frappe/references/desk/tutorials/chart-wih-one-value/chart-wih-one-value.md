# How To: Chart Wih One Value

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test chart wih one value

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

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('Error Log')
```

### Step 2: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='Error Log', creation='2018-06-01 00:00:00').insert()
```

### Step 3: Call frappe.get_doc.insert()

```python
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart 2', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
```

### Step 4: Assign cur_date = value

```python
cur_date = datetime.now() - relativedelta(years=1)
```

### Step 5: Assign result = get(...)

```python
result = get(chart_name='Test Empty Dashboard Chart 2', refresh=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(result.get('datasets')[0].get('values')[2], 0)
```

### Step 7: Call frappe.delete_doc()

```python
frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart 2')
```

### Step 8: Assign month = get_last_day(...)

```python
month = get_last_day(cur_date)
```

### Step 9: Assign month = formatdate(...)

```python
month = formatdate(month.strftime('%Y-%m-%d'))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(result.get('labels')[idx], get_period(month))
```


## Complete Example

```python
# Workflow
if frappe.db.exists('Dashboard Chart', 'Test Empty Dashboard Chart 2'):
    frappe.delete_doc('Dashboard Chart', 'Test Empty Dashboard Chart 2')
frappe.db.delete('Error Log')
frappe.get_doc(doctype='Error Log', creation='2018-06-01 00:00:00').insert()
frappe.get_doc(doctype='Dashboard Chart', chart_name='Test Empty Dashboard Chart 2', chart_type='Count', document_type='Error Log', based_on='creation', timespan='Last Year', time_interval='Monthly', filters_json='[]', timeseries=1).insert()
cur_date = datetime.now() - relativedelta(years=1)
result = get(chart_name='Test Empty Dashboard Chart 2', refresh=1)
for idx in range(13):
    month = get_last_day(cur_date)
    month = formatdate(month.strftime('%Y-%m-%d'))
    self.assertEqual(result.get('labels')[idx], get_period(month))
    cur_date += relativedelta(months=1)
self.assertEqual(result.get('datasets')[0].get('values')[2], 0)
```

## Next Steps


---

*Source: test_dashboard_chart.py:113 | Complexity: Advanced | Last updated: 2026-02-04*