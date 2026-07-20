# How To: Safe Eval

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test safe eval

## Prerequisites

**Required Modules:**
- `types`
- `frappe`
- `frappe.tests`
- `frappe.utils.jinja`
- `frappe.utils.safe_exec`


## Step-by-Step Guide

### Step 1: Assign TEST_CASES = value

```python
TEST_CASES = {'1+1': 2, '"abc" in "abl"': False, '"a" in "abl"': True, '"a" in ("a", "b")': True, '"a" in {"a", "b"}': True, '"a" in {"a": 1, "b": 2}': True, '"a" in ["a" ,"b"]': True}
```

### Step 2: Call self.assertRaises()

```python
self.assertRaises(AttributeError, frappe.safe_eval, 'frappe.utils.os.path', get_safe_globals())
```

### Step 3: Assign user = frappe.new_doc(...)

```python
user = frappe.new_doc('User')
```

### Step 4: Assign user.user_type = 'System User'

```python
user.user_type = 'System User'
```

### Step 5: Assign user.enabled = 1

```python
user.enabled = 1
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(frappe.safe_eval("user_type == 'System User'", eval_locals=user.as_dict()))
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual('System User Test', frappe.safe_eval("user_type + ' Test'", eval_locals=user.as_dict()))
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(1, frappe.safe_eval('int(enabled)', eval_locals=user.as_dict()))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(frappe.safe_eval(code), result)
```


## Complete Example

```python
# Workflow
TEST_CASES = {'1+1': 2, '"abc" in "abl"': False, '"a" in "abl"': True, '"a" in ("a", "b")': True, '"a" in {"a", "b"}': True, '"a" in {"a": 1, "b": 2}': True, '"a" in ["a" ,"b"]': True}
for code, result in TEST_CASES.items():
    self.assertEqual(frappe.safe_eval(code), result)
self.assertRaises(AttributeError, frappe.safe_eval, 'frappe.utils.os.path', get_safe_globals())
user = frappe.new_doc('User')
user.user_type = 'System User'
user.enabled = 1
self.assertTrue(frappe.safe_eval("user_type == 'System User'", eval_locals=user.as_dict()))
self.assertEqual('System User Test', frappe.safe_eval("user_type + ' Test'", eval_locals=user.as_dict()))
self.assertEqual(1, frappe.safe_eval('int(enabled)', eval_locals=user.as_dict()))
```

## Next Steps


---

*Source: test_safe_exec.py:26 | Complexity: Advanced | Last updated: 2026-02-04*