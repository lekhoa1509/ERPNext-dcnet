# How To: Holiday List

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test holiday list

## Prerequisites

**Required Modules:**
- `contextlib`
- `datetime`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.setup.doctype.holiday_list.holiday_list`


## Step-by-Step Guide

### Step 1: Assign today_date = getdate(...)

```python
today_date = getdate()
```

### Step 2: Assign test_holiday_dates = value

```python
test_holiday_dates = [today_date - timedelta(days=5), today_date - timedelta(days=4)]
```

### Step 3: Assign holiday_list = make_holiday_list(...)

```python
holiday_list = make_holiday_list('test_holiday_list', holiday_dates=[{'holiday_date': test_holiday_dates[0], 'description': 'test holiday'}, {'holiday_date': test_holiday_dates[1], 'description': 'test holiday2'}])
```

### Step 4: Assign fetched_holiday_list = frappe.get_value(...)

```python
fetched_holiday_list = frappe.get_value('Holiday List', holiday_list.name)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(holiday_list.name, fetched_holiday_list)
```


## Complete Example

```python
# Workflow
today_date = getdate()
test_holiday_dates = [today_date - timedelta(days=5), today_date - timedelta(days=4)]
holiday_list = make_holiday_list('test_holiday_list', holiday_dates=[{'holiday_date': test_holiday_dates[0], 'description': 'test holiday'}, {'holiday_date': test_holiday_dates[1], 'description': 'test holiday2'}])
fetched_holiday_list = frappe.get_value('Holiday List', holiday_list.name)
self.assertEqual(holiday_list.name, fetched_holiday_list)
```

## Next Steps


---

*Source: test_holiday_list.py:14 | Complexity: Intermediate | Last updated: 2026-02-04*