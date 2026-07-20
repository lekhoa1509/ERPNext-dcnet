# How To: Weekly Repeat

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test weekly repeat

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
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2025-04-15 16:00:00', 'repeat_till': '2025-05-06 23:59:59', 'tuesday': 1, 'wednesday': 1, 'friday': 1, 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Weekly'}).insert()
```

### Step 2: Assign applicable_dates = value

```python
applicable_dates = [(date(2025, 4, 15), date(2025, 4, 15)), (date(2025, 4, 22), date(2025, 4, 22)), (date(2025, 4, 29), date(2025, 4, 29)), (date(2025, 4, 30), date(2025, 4, 30)), (date(2025, 5, 2), date(2025, 5, 2))]
```

### Step 3: Assign unapplicable_dates = value

```python
unapplicable_dates = [(date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 5, 18), date(2023, 5, 18))]
```

### Step 4: Assign event_list = get_events(...)

```python
event_list = get_events(date(2025, 4, 29), date(2025, 5, 2), 'Administrator', for_reminder=True)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(event_list), 3)
```

### Step 6: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 7: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

### Step 9: Call self.assertFalse()

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
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2025-04-15 16:00:00', 'repeat_till': '2025-05-06 23:59:59', 'tuesday': 1, 'wednesday': 1, 'friday': 1, 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Weekly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2025, 4, 15), date(2025, 4, 15)), (date(2025, 4, 22), date(2025, 4, 22)), (date(2025, 4, 29), date(2025, 4, 29)), (date(2025, 4, 30), date(2025, 4, 30)), (date(2025, 5, 2), date(2025, 5, 2))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2022, 8, 17), date(2022, 8, 17)), (date(2024, 2, 18), date(2024, 2, 18)), (date(2023, 5, 17), date(2023, 5, 17)), (date(2023, 5, 18), date(2023, 5, 18))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
event_list = get_events(date(2025, 4, 29), date(2025, 5, 2), 'Administrator', for_reminder=True)
self.assertEqual(len(event_list), 3)
```

## Next Steps


---

*Source: test_event.py:333 | Complexity: Advanced | Last updated: 2026-02-04*