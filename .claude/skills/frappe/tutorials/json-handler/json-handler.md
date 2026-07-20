# How To: Json Handler

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test json handler

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

### Step 1: Assign GOOD_OBJECT = value

```python
GOOD_OBJECT = {'time_types': [date(year=2020, month=12, day=2), datetime(year=2020, month=12, day=2, hour=23, minute=23, second=23, microsecond=23, tzinfo=UTC), time(hour=23, minute=23, second=23, microsecond=23, tzinfo=UTC), timedelta(days=10, hours=12, minutes=120, seconds=10)], 'float': [Decimal('29.21')], 'doc': [frappe.get_doc('System Settings')], 'iter': [{1, 2, 3}, (1, 2, 3), 'abcdef'], 'string': 'abcdef'}
```

### Step 2: Assign BAD_OBJECT = value

```python
BAD_OBJECT = {'Enum': TEST}
```

### Step 3: Assign processed_object = json.loads(...)

```python
processed_object = json.loads(json.dumps(GOOD_OBJECT, default=json_handler))
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(all([isinstance(x, str) for x in processed_object['time_types']]))
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(all([isinstance(x, float) for x in processed_object['float']]))
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(all([isinstance(x, list | str) for x in processed_object['iter']]))
```

### Step 7: Call self.assertIsInstance()

```python
self.assertIsInstance(processed_object['string'], str)
```

### Step 8: Assign ABC = '!@)@)!'

```python
ABC = '!@)@)!'
```

### Step 9: Assign BCE = 'ENJD'

```python
BCE = 'ENJD'
```

### Step 10: Call json.dumps()

```python
json.dumps(BAD_OBJECT, default=json_handler)
```


## Complete Example

```python
# Workflow
class TEST(Enum):
    ABC = '!@)@)!'
    BCE = 'ENJD'
GOOD_OBJECT = {'time_types': [date(year=2020, month=12, day=2), datetime(year=2020, month=12, day=2, hour=23, minute=23, second=23, microsecond=23, tzinfo=UTC), time(hour=23, minute=23, second=23, microsecond=23, tzinfo=UTC), timedelta(days=10, hours=12, minutes=120, seconds=10)], 'float': [Decimal('29.21')], 'doc': [frappe.get_doc('System Settings')], 'iter': [{1, 2, 3}, (1, 2, 3), 'abcdef'], 'string': 'abcdef'}
BAD_OBJECT = {'Enum': TEST}
processed_object = json.loads(json.dumps(GOOD_OBJECT, default=json_handler))
self.assertTrue(all([isinstance(x, str) for x in processed_object['time_types']]))
self.assertTrue(all([isinstance(x, float) for x in processed_object['float']]))
self.assertTrue(all([isinstance(x, list | str) for x in processed_object['iter']]))
self.assertIsInstance(processed_object['string'], str)
with self.assertRaises(TypeError):
    json.dumps(BAD_OBJECT, default=json_handler)
```

## Next Steps


---

*Source: test_utils.py:948 | Complexity: Advanced | Last updated: 2026-02-04*