# How To: Weekly Off

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test weekly off

## Prerequisites

**Required Modules:**
- `contextlib`
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.setup.doctype.holiday_list.holiday_list`


## Step-by-Step Guide

### Step 1: Assign holiday_list = frappe.new_doc(...)

```python
holiday_list = frappe.new_doc('Holiday List')
```

### Step 2: Assign holiday_list.from_date = '2023-01-01'

```python
holiday_list.from_date = '2023-01-01'
```

### Step 3: Assign holiday_list.to_date = '2023-02-28'

```python
holiday_list.to_date = '2023-02-28'
```

### Step 4: Assign holiday_list.weekly_off = 'Sunday'

```python
holiday_list.weekly_off = 'Sunday'
```

### Step 5: Call holiday_list.get_weekly_off_dates()

```python
holiday_list.get_weekly_off_dates()
```

### Step 6: Assign holidays = value

```python
holidays = [holiday.holiday_date for holiday in holiday_list.holidays]
```

### Step 7: Call self.assertNotIn()

```python
self.assertNotIn(date(2022, 12, 25), holidays)
```

### Step 8: Call self.assertIn()

```python
self.assertIn(date(2023, 1, 1), holidays)
```

### Step 9: Call self.assertIn()

```python
self.assertIn(date(2023, 1, 8), holidays)
```

### Step 10: Call self.assertIn()

```python
self.assertIn(date(2023, 1, 15), holidays)
```

### Step 11: Call self.assertIn()

```python
self.assertIn(date(2023, 1, 22), holidays)
```

### Step 12: Call self.assertIn()

```python
self.assertIn(date(2023, 1, 29), holidays)
```

### Step 13: Call self.assertIn()

```python
self.assertIn(date(2023, 2, 5), holidays)
```

### Step 14: Call self.assertIn()

```python
self.assertIn(date(2023, 2, 12), holidays)
```

### Step 15: Call self.assertIn()

```python
self.assertIn(date(2023, 2, 19), holidays)
```

### Step 16: Call self.assertIn()

```python
self.assertIn(date(2023, 2, 26), holidays)
```

### Step 17: Call self.assertNotIn()

```python
self.assertNotIn(date(2023, 3, 5), holidays)
```


## Complete Example

```python
# Workflow
holiday_list = frappe.new_doc('Holiday List')
holiday_list.from_date = '2023-01-01'
holiday_list.to_date = '2023-02-28'
holiday_list.weekly_off = 'Sunday'
holiday_list.get_weekly_off_dates()
holidays = [holiday.holiday_date for holiday in holiday_list.holidays]
self.assertNotIn(date(2022, 12, 25), holidays)
self.assertIn(date(2023, 1, 1), holidays)
self.assertIn(date(2023, 1, 8), holidays)
self.assertIn(date(2023, 1, 15), holidays)
self.assertIn(date(2023, 1, 22), holidays)
self.assertIn(date(2023, 1, 29), holidays)
self.assertIn(date(2023, 2, 5), holidays)
self.assertIn(date(2023, 2, 12), holidays)
self.assertIn(date(2023, 2, 19), holidays)
self.assertIn(date(2023, 2, 26), holidays)
self.assertNotIn(date(2023, 3, 5), holidays)
```

## Next Steps


---

*Source: test_holiday_list.py:27 | Complexity: Advanced | Last updated: 2026-02-04*