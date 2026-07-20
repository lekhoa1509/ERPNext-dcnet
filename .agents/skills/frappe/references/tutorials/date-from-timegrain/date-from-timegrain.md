# How To: Date From Timegrain

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test date from timegrain

## Prerequisites

**Required Modules:**
- `io`
- `json`
- `os`
- `sys`
- `datetime`
- `decimal`
- `enum`
- `io`
- `mimetypes`
- `unittest.mock`
- `hypothesis`
- `hypothesis`
- `PIL`
- `frappe`
- `frappe.installer`
- `frappe.model.document`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.utils`
- `frappe.utils.change_log`
- `frappe.utils.data`
- `frappe.utils.dateutils`
- `frappe.utils.diff`
- `frappe.utils.identicon`
- `frappe.utils.image`
- `frappe.utils.make_random`
- `frappe.utils.response`
- `frappe.utils.synchronization`
- `frappe.utils.typing_validations`
- `decimal`
- `decimal`
- `frappe.utils.html_utils`
- `frappe.utils.html_utils`
- `frappe`
- `frappe.utils.xlsxutils`
- `frappe.boot`
- `frappe.desk.form.load`
- `frappe.utils.lazy_loader`
- `unittest.mock`
- `frappe.core.doctype.doctype.doctype`


## Step-by-Step Guide

### Step 1: Assign start_date = getdate(...)

```python
start_date = getdate('2021-01-01')
```

### Step 2: Assign daily = get_dates_from_timegrain(...)

```python
daily = get_dates_from_timegrain(start_date, add_to_date(start_date, days=6), 'Daily')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(len(daily), 7)
```

### Step 4: Assign start = get_first_day_of_week(...)

```python
start = get_first_day_of_week(start_date)
```

### Step 5: Assign end = add_to_date(...)

```python
end = add_to_date(add_to_date(start, weeks=52), days=-1)
```

### Step 6: Assign weekly = get_dates_from_timegrain(...)

```python
weekly = get_dates_from_timegrain(start, end, 'Weekly')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(weekly), 52)
```

### Step 8: Assign quarterly = get_dates_from_timegrain(...)

```python
quarterly = get_dates_from_timegrain(start_date, add_to_date(start_date, months=5), 'Quarterly')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(quarterly), 2)
```

### Step 10: Assign yearly = get_dates_from_timegrain(...)

```python
yearly = get_dates_from_timegrain(start_date, add_to_date(start_date, years=2), 'Yearly')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(yearly), 3)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(d, add_to_date(start_date, days=idx))
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(d, add_to_date(start, days=7 * idx - 1))
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(d, add_to_date(start_date, months=idx * 3, days=-1))
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(d, add_to_date(start_date, years=idx, days=-1))
```


## Complete Example

```python
# Workflow
start_date = getdate('2021-01-01')
daily = get_dates_from_timegrain(start_date, add_to_date(start_date, days=6), 'Daily')
self.assertEqual(len(daily), 7)
for idx, d in enumerate(daily):
    self.assertEqual(d, add_to_date(start_date, days=idx))
start = get_first_day_of_week(start_date)
end = add_to_date(add_to_date(start, weeks=52), days=-1)
weekly = get_dates_from_timegrain(start, end, 'Weekly')
self.assertEqual(len(weekly), 52)
for idx, d in enumerate(weekly, start=1):
    self.assertEqual(d, add_to_date(start, days=7 * idx - 1))
quarterly = get_dates_from_timegrain(start_date, add_to_date(start_date, months=5), 'Quarterly')
self.assertEqual(len(quarterly), 2)
for idx, d in enumerate(quarterly, start=1):
    self.assertEqual(d, add_to_date(start_date, months=idx * 3, days=-1))
yearly = get_dates_from_timegrain(start_date, add_to_date(start_date, years=2), 'Yearly')
self.assertEqual(len(yearly), 3)
for idx, d in enumerate(yearly, start=1):
    self.assertEqual(d, add_to_date(start_date, years=idx, days=-1))
```

## Next Steps


---

*Source: test_utils.py:921 | Complexity: Advanced | Last updated: 2026-02-04*