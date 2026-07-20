# How To: Naming Rule By Condition

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming rule by condition

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Assign naming_rule = frappe.get_doc.insert(...)

```python
naming_rule = frappe.get_doc(doctype='Document Naming Rule', document_type='ToDo', prefix='test-high-', prefix_digits=5, priority=10, conditions=[dict(field='priority', condition='=', value='High')]).insert()
```

### Step 2: Assign naming_rule_1 = frappe.copy_doc(...)

```python
naming_rule_1 = frappe.copy_doc(naming_rule)
```

### Step 3: Assign naming_rule_1.prefix = 'test-medium-'

```python
naming_rule_1.prefix = 'test-medium-'
```

### Step 4: Assign unknown.value = 'Medium'

```python
naming_rule_1.conditions[0].value = 'Medium'
```

### Step 5: Call naming_rule_1.insert()

```python
naming_rule_1.insert()
```

### Step 6: Assign naming_rule_2 = frappe.copy_doc(...)

```python
naming_rule_2 = frappe.copy_doc(naming_rule)
```

### Step 7: Assign naming_rule_2.prefix = 'test-low-'

```python
naming_rule_2.prefix = 'test-low-'
```

### Step 8: Assign naming_rule_2.priority = 0

```python
naming_rule_2.priority = 0
```

### Step 9: Assign naming_rule_2.conditions = value

```python
naming_rule_2.conditions = []
```

### Step 10: Call naming_rule_2.insert()

```python
naming_rule_2.insert()
```

### Step 11: Assign todo = frappe.get_doc.insert(...)

```python
todo = frappe.get_doc(doctype='ToDo', priority='High', description='Is this my name ' + frappe.generate_hash()).insert()
```

### Step 12: Assign todo_1 = frappe.get_doc.insert(...)

```python
todo_1 = frappe.get_doc(doctype='ToDo', priority='Medium', description='Is this my name ' + frappe.generate_hash()).insert()
```

### Step 13: Assign todo_2 = frappe.get_doc.insert(...)

```python
todo_2 = frappe.get_doc(doctype='ToDo', priority='Low', description='Is this my name ' + frappe.generate_hash()).insert()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(todo.name, 'test-high-00001')
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(todo_1.name, 'test-medium-00001')
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(todo_2.name, 'test-low-00001')
```

### Step 17: Call naming_rule.delete()

```python
naming_rule.delete()
```

### Step 18: Call naming_rule_1.delete()

```python
naming_rule_1.delete()
```

### Step 19: Call naming_rule_2.delete()

```python
naming_rule_2.delete()
```

### Step 20: Call todo.delete()

```python
todo.delete()
```

### Step 21: Call todo_1.delete()

```python
todo_1.delete()
```

### Step 22: Call todo_2.delete()

```python
todo_2.delete()
```


## Complete Example

```python
# Workflow
naming_rule = frappe.get_doc(doctype='Document Naming Rule', document_type='ToDo', prefix='test-high-', prefix_digits=5, priority=10, conditions=[dict(field='priority', condition='=', value='High')]).insert()
naming_rule_1 = frappe.copy_doc(naming_rule)
naming_rule_1.prefix = 'test-medium-'
naming_rule_1.conditions[0].value = 'Medium'
naming_rule_1.insert()
naming_rule_2 = frappe.copy_doc(naming_rule)
naming_rule_2.prefix = 'test-low-'
naming_rule_2.priority = 0
naming_rule_2.conditions = []
naming_rule_2.insert()
todo = frappe.get_doc(doctype='ToDo', priority='High', description='Is this my name ' + frappe.generate_hash()).insert()
todo_1 = frappe.get_doc(doctype='ToDo', priority='Medium', description='Is this my name ' + frappe.generate_hash()).insert()
todo_2 = frappe.get_doc(doctype='ToDo', priority='Low', description='Is this my name ' + frappe.generate_hash()).insert()
try:
    self.assertEqual(todo.name, 'test-high-00001')
    self.assertEqual(todo_1.name, 'test-medium-00001')
    self.assertEqual(todo_2.name, 'test-low-00001')
finally:
    naming_rule.delete()
    naming_rule_1.delete()
    naming_rule_2.delete()
    todo.delete()
    todo_1.delete()
    todo_2.delete()
```

## Next Steps


---

*Source: test_document_naming_rule.py:22 | Complexity: Advanced | Last updated: 2026-02-04*