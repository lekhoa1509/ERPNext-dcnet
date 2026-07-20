# How To: Welcome Url

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test welcome url

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`


## Step-by-Step Guide

### Step 1: Assign email_group = frappe.new_doc(...)

```python
email_group = frappe.new_doc('Email Group')
```

### Step 2: Assign email_group.title = 'Test'

```python
email_group.title = 'Test'
```

### Step 3: Assign email_group.welcome_url = 'http://example.com/welcome?hello=world'

```python
email_group.welcome_url = 'http://example.com/welcome?hello=world'
```

### Step 4: Assign email_group.add_query_parameters = 1

```python
email_group.add_query_parameters = 1
```

### Step 5: Call email_group.insert()

```python
email_group.insert()
```

### Step 6: Assign welcome_url = email_group.get_welcome_url(...)

```python
welcome_url = email_group.get_welcome_url('mail@example.org')
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(validate_url(welcome_url))
```

### Step 8: Call self.assertIn()

```python
self.assertIn(email_group.welcome_url, welcome_url)
```

### Step 9: Call self.assertIn()

```python
self.assertIn('email_group=Test', welcome_url)
```

### Step 10: Call self.assertIn()

```python
self.assertIn('email=mail%40example.org', welcome_url)
```

### Step 11: Assign email_group.add_query_parameters = 0

```python
email_group.add_query_parameters = 0
```

### Step 12: Assign welcome_url = email_group.get_welcome_url(...)

```python
welcome_url = email_group.get_welcome_url('mail@example.org')
```

### Step 13: Call self.assertTrue()

```python
self.assertTrue(validate_url(welcome_url))
```

### Step 14: Call self.assertIn()

```python
self.assertIn(email_group.welcome_url, welcome_url)
```

### Step 15: Call self.assertNotIn()

```python
self.assertNotIn('email_group=Test', welcome_url)
```

### Step 16: Call self.assertNotIn()

```python
self.assertNotIn('email=mail%40example.org', welcome_url)
```

### Step 17: Assign email_group.welcome_url = ''

```python
email_group.welcome_url = ''
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(email_group.get_welcome_url(), None)
```


## Complete Example

```python
# Workflow
email_group = frappe.new_doc('Email Group')
email_group.title = 'Test'
email_group.welcome_url = 'http://example.com/welcome?hello=world'
email_group.add_query_parameters = 1
email_group.insert()
welcome_url = email_group.get_welcome_url('mail@example.org')
self.assertTrue(validate_url(welcome_url))
self.assertIn(email_group.welcome_url, welcome_url)
self.assertIn('email_group=Test', welcome_url)
self.assertIn('email=mail%40example.org', welcome_url)
email_group.add_query_parameters = 0
welcome_url = email_group.get_welcome_url('mail@example.org')
self.assertTrue(validate_url(welcome_url))
self.assertIn(email_group.welcome_url, welcome_url)
self.assertNotIn('email_group=Test', welcome_url)
self.assertNotIn('email=mail%40example.org', welcome_url)
email_group.welcome_url = ''
self.assertEqual(email_group.get_welcome_url(), None)
```

## Next Steps


---

*Source: test_email_group.py:9 | Complexity: Advanced | Last updated: 2026-02-04*