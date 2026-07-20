# How To: Assignment Rule Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test assignment rule condition

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.tests.utils`


## Step-by-Step Guide

### Step 1: Call frappe.db.delete()

```python
frappe.db.delete('Assignment Rule')
```

### Step 2: Assign assignment_rule = frappe.get_doc.insert(...)

```python
assignment_rule = frappe.get_doc(name='Assignment with Due Date', doctype='Assignment Rule', document_type=TEST_DOCTYPE, assign_condition='public == 0', due_date_based_on='expiry_date', assignment_days=self.days, users=[dict(user='test@example.com')]).insert()
```

### Step 3: Assign expiry_date = frappe.utils.add_days(...)

```python
expiry_date = frappe.utils.add_days(frappe.utils.nowdate(), 2)
```

### Step 4: Assign note1 = _make_test_record(...)

```python
note1 = _make_test_record(expiry_date=expiry_date)
```

### Step 5: Assign note2 = _make_test_record(...)

```python
note2 = _make_test_record(expiry_date=expiry_date)
```

### Step 6: Assign note1_todo = value

```python
note1_todo = frappe.get_all('ToDo', filters=dict(reference_type=TEST_DOCTYPE, reference_name=note1.name, status='Open'))[0]
```

### Step 7: Assign note1_todo_doc = frappe.get_doc(...)

```python
note1_todo_doc = frappe.get_doc('ToDo', note1_todo.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), expiry_date)
```

### Step 9: Assign note1.expiry_date = frappe.utils.add_days(...)

```python
note1.expiry_date = frappe.utils.add_days(expiry_date, 2)
```

### Step 10: Call note1.save()

```python
note1.save()
```

### Step 11: Call note1_todo_doc.reload()

```python
note1_todo_doc.reload()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), note1.expiry_date)
```

### Step 13: Assign note2_todo = value

```python
note2_todo = frappe.get_all('ToDo', filters=dict(reference_type=TEST_DOCTYPE, reference_name=note2.name, status='Open'), fields=['name', 'date'])[0]
```

### Step 14: Call self.assertNotEqual()

```python
self.assertNotEqual(frappe.utils.get_date_str(note2_todo.date), note1.expiry_date)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(frappe.utils.get_date_str(note2_todo.date), expiry_date)
```

### Step 16: Call assignment_rule.delete()

```python
assignment_rule.delete()
```

### Step 17: Call frappe.db.commit()

```python
frappe.db.commit()
```


## Complete Example

```python
# Workflow
frappe.db.delete('Assignment Rule')
assignment_rule = frappe.get_doc(name='Assignment with Due Date', doctype='Assignment Rule', document_type=TEST_DOCTYPE, assign_condition='public == 0', due_date_based_on='expiry_date', assignment_days=self.days, users=[dict(user='test@example.com')]).insert()
expiry_date = frappe.utils.add_days(frappe.utils.nowdate(), 2)
note1 = _make_test_record(expiry_date=expiry_date)
note2 = _make_test_record(expiry_date=expiry_date)
note1_todo = frappe.get_all('ToDo', filters=dict(reference_type=TEST_DOCTYPE, reference_name=note1.name, status='Open'))[0]
note1_todo_doc = frappe.get_doc('ToDo', note1_todo.name)
self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), expiry_date)
note1.expiry_date = frappe.utils.add_days(expiry_date, 2)
note1.save()
note1_todo_doc.reload()
self.assertEqual(frappe.utils.get_date_str(note1_todo_doc.date), note1.expiry_date)
note2_todo = frappe.get_all('ToDo', filters=dict(reference_type=TEST_DOCTYPE, reference_name=note2.name, status='Open'), fields=['name', 'date'])[0]
self.assertNotEqual(frappe.utils.get_date_str(note2_todo.date), note1.expiry_date)
self.assertEqual(frappe.utils.get_date_str(note2_todo.date), expiry_date)
assignment_rule.delete()
frappe.db.commit()
```

## Next Steps


---

*Source: test_assignment_rule.py:248 | Complexity: Advanced | Last updated: 2026-02-04*