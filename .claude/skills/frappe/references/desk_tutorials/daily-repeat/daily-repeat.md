# How To: Daily Repeat

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test daily repeat

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `datetime`
- `frappe`
- `frappe.core.utils`
- `frappe.desk.doctype.event.event`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.desk.form.assign_to`

**Setup Required:**
```python
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'
```

## Step-by-Step Guide

### Step 1: Assign ev = frappe.get_doc.insert(...)

```python
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Daily'}).insert()
```

### Step 2: Assign applicable_dates = value

```python
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2024, 1, 1), date(2024, 1, 1))]
```

### Step 3: Assign unapplicable_dates = value

```python
unapplicable_dates = [(date(2024, 2, 17), date(2024, 2, 17)), (date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18))]
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
# Setup
frappe.db.delete('Event')
make_test_objects('Event', reset=True)
self.test_user = 'test1@example.com'

# Workflow
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2023-02-17', 'repeat_till': '2024-02-17', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Daily'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2023, 2, 17), date(2023, 2, 17)), (date(2024, 1, 1), date(2024, 1, 1))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2024, 2, 17), date(2024, 2, 17)), (date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

## Next Steps


---

*Source: test_event.py:290 | Complexity: Intermediate | Last updated: 2026-02-04*