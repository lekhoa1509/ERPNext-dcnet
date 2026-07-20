# How To: Yearly Repeat

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test yearly repeat

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
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2014-02-01', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Yearly'}).insert()
```

### Step 2: Assign applicable_dates = value

```python
applicable_dates = [(date(2014, 2, 1), date(2014, 2, 1)), (date(2015, 2, 1), date(2015, 2, 1)), (date(2016, 2, 1), date(2016, 2, 1))]
```

### Step 3: Assign unapplicable_dates = value

```python
unapplicable_dates = [(date(2014, 1, 20), date(2014, 1, 20)), (date(2015, 1, 20), date(2015, 1, 20))]
```

### Step 4: Assign ev.starts_on = date(...)

```python
ev.starts_on = date(2016, 2, 29)
```

### Step 5: Call ev.save()

```python
ev.save()
```

### Step 6: Assign applicable_dates = value

```python
applicable_dates = [(date(2016, 2, 29), date(2016, 2, 29)), (date(2024, 2, 28), date(2024, 2, 29))]
```

### Step 7: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 8: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 9: Assign event_list = get_events(...)

```python
event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

### Step 11: Call self.assertFalse()

```python
self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```


## Complete Example

```python
# Workflow
ev = frappe.get_doc({'doctype': 'Event', 'subject': '_Test Event', 'starts_on': '2014-02-01', 'event_type': 'Public', 'repeat_this_event': 1, 'repeat_on': 'Yearly'}).insert()

def test_record_matched(e):
    return e.name == ev.name
applicable_dates = [(date(2014, 2, 1), date(2014, 2, 1)), (date(2015, 2, 1), date(2015, 2, 1)), (date(2016, 2, 1), date(2016, 2, 1))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
unapplicable_dates = [(date(2014, 1, 20), date(2014, 1, 20)), (date(2015, 1, 20), date(2015, 1, 20))]
for start_date, end_date in unapplicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertFalse(find(event_list, test_record_matched), f'Event found between {start_date} and {end_date}')
ev.starts_on = date(2016, 2, 29)
ev.save()
applicable_dates = [(date(2016, 2, 29), date(2016, 2, 29)), (date(2024, 2, 28), date(2024, 2, 29))]
for start_date, end_date in applicable_dates:
    event_list = get_events(start_date, end_date, 'Administrator', for_reminder=True)
    with self.subTest(start_date=start_date, end_date=end_date):
        self.assertTrue(find(event_list, test_record_matched), f'Event not found between {start_date} and {end_date}')
```

## Next Steps


---

*Source: test_event.py:111 | Complexity: Advanced | Last updated: 2026-02-04*