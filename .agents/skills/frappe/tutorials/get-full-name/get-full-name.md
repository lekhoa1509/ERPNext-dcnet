# How To: Get Full Name

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get full name

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.contacts.doctype.contact.contact`
- `frappe.email`
- `frappe.tests`


## Step-by-Step Guide

### Step 1: Call self.assertEqual()

```python
self.assertEqual(get_full_name(first='John'), 'John')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(get_full_name(last='Doe'), 'Doe')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(get_full_name(company='Doe Pvt Ltd'), 'Doe Pvt Ltd')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(get_full_name(first='John', last='Doe'), 'John Doe')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(get_full_name(first='John', middle='Jane'), 'John Jane')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(get_full_name(first='John', last='Doe', company='Doe Pvt Ltd'), 'John Doe')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(get_full_name(first='John', middle='Jane', last='Doe', company='Doe Pvt Ltd'), 'John Jane Doe')
```


## Complete Example

```python
# Workflow
self.assertEqual(get_full_name(first='John'), 'John')
self.assertEqual(get_full_name(last='Doe'), 'Doe')
self.assertEqual(get_full_name(company='Doe Pvt Ltd'), 'Doe Pvt Ltd')
self.assertEqual(get_full_name(first='John', last='Doe'), 'John Doe')
self.assertEqual(get_full_name(first='John', middle='Jane'), 'John Jane')
self.assertEqual(get_full_name(first='John', last='Doe', company='Doe Pvt Ltd'), 'John Doe')
self.assertEqual(get_full_name(first='John', middle='Jane', last='Doe', company='Doe Pvt Ltd'), 'John Jane Doe')
```

## Next Steps


---

*Source: test_contact.py:36 | Complexity: Intermediate | Last updated: 2026-02-04*