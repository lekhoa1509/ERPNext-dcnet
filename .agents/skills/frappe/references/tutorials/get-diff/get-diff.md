# How To: Get Diff

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get diff

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe.core.doctype.version.version`
- `frappe.tests`
- `frappe.tests.utils`
- `frappe.desk.form.load`


## Step-by-Step Guide

### Step 1: Call frappe.set_user()

```python
frappe.set_user('Administrator')
```

### Step 2: Assign test_records = make_test_objects(...)

```python
test_records = make_test_objects('Event', reset=True)
```

### Step 3: Assign old_doc = frappe.get_doc(...)

```python
old_doc = frappe.get_doc('Event', test_records[0])
```

### Step 4: Assign new_doc = copy.deepcopy(...)

```python
new_doc = copy.deepcopy(old_doc)
```

### Step 5: Assign old_doc.color = None

```python
old_doc.color = None
```

### Step 6: Assign new_doc.color = '#fafafa'

```python
new_doc.color = '#fafafa'
```

### Step 7: Assign diff = value

```python
diff = get_diff(old_doc, new_doc)['changed']
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(get_fieldnames(diff)[0], 'color')
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(get_old_values(diff)[0] is None)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(get_new_values(diff)[0], '#fafafa')
```

### Step 11: Assign new_doc.starts_on = '2017-07-20'

```python
new_doc.starts_on = '2017-07-20'
```

### Step 12: Assign diff = value

```python
diff = get_diff(old_doc, new_doc)['changed']
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(get_fieldnames(diff)[1], 'starts_on')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(get_old_values(diff)[1], '01-01-2014 00:00:00')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(get_new_values(diff)[1], '07-20-2017 00:00:00')
```


## Complete Example

```python
# Workflow
frappe.set_user('Administrator')
test_records = make_test_objects('Event', reset=True)
old_doc = frappe.get_doc('Event', test_records[0])
new_doc = copy.deepcopy(old_doc)
old_doc.color = None
new_doc.color = '#fafafa'
diff = get_diff(old_doc, new_doc)['changed']
self.assertEqual(get_fieldnames(diff)[0], 'color')
self.assertTrue(get_old_values(diff)[0] is None)
self.assertEqual(get_new_values(diff)[0], '#fafafa')
new_doc.starts_on = '2017-07-20'
diff = get_diff(old_doc, new_doc)['changed']
self.assertEqual(get_fieldnames(diff)[1], 'starts_on')
self.assertEqual(get_old_values(diff)[1], '01-01-2014 00:00:00')
self.assertEqual(get_new_values(diff)[1], '07-20-2017 00:00:00')
```

## Next Steps


---

*Source: test_version.py:12 | Complexity: Advanced | Last updated: 2026-02-04*