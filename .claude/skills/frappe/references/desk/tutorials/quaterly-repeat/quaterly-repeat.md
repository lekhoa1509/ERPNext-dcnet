# How To: Quaterly Repeat

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test quaterly repeat

## Prerequisites

**Required Modules:**
- `json`
- `datetime`
- `frappe`
- `frappe.core.utils`
- `frappe.desk.doctype.event.event`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.desk.form.assign_to`


## Step-by-Step Guide

### Step 1: Assign ev = frappe.get_doc.insert(...)

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Quarterly'}).insert()
```

### Step 2: Assign applicable_dates = value

```python
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 8, 17), date(2023, 8, 17)), (date(2023, 11, 17), date(2023, 11, 17))]
```

### Step 3: Assign unapplicable_dates = value

```python
unapplicable_dates = [(date(2022, 11, 17), date(2022, 11, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 3, 17), date(2023, 3, 17))]
```

### Step 4: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 5: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

### Step 7: Call self.assertFalse()

```python
self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```


## Complete Example

```python
# Workflow
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Quarterly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 8, 17), date(2023, 8, 17)), (date(2023, 11, 17), date(2023, 11, 17))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 11, 17), date(2022, 11, 17)), (date(2024, 2, 17), date(2024, 2, 17)), (date(2023, 12, 17), date(2023, 12, 17)), (date(2023, 3, 17), date(2023, 3, 17))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

## Next Steps


---

*Source: test_event.py:196 | Complexity: Intermediate | Last updated: 2026-02-04*