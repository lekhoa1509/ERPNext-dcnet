# How To: Multiple Pos Opening Entry For Multiple Pos Profiles

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple pos opening entry for multiple pos profiles

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.core.doctype.user_permission.test_user_permission`
- `frappe.tests`
- `erpnext.accounts.doctype.pos_invoice.test_pos_invoice`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`


## Step-by-Step Guide

### Step 1: Assign unknown = self.init_user_and_profile(...)

```python
test_user, pos_profile = self.init_user_and_profile()
```

### Step 2: Assign opening_entry_1 = create_opening_entry(...)

```python
opening_entry_1 = create_opening_entry(pos_profile, test_user.name)
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(opening_entry_1.status, 'Open')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(opening_entry_1.user, test_user.name)
```

### Step 5: Assign cashier_user = create_user(...)

```python
cashier_user = create_user('test_cashier@example.com', 'Accounts Manager', 'Sales Manager')
```

### Step 6: Call frappe.set_user()

```python
frappe.set_user(cashier_user.name)
```

### Step 7: Assign pos_profile2 = make_pos_profile(...)

```python
pos_profile2 = make_pos_profile(name='_Test POS Profile 2')
```

### Step 8: Assign opening_entry_2 = create_opening_entry(...)

```python
opening_entry_2 = create_opening_entry(pos_profile2, cashier_user.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(opening_entry_2.status, 'Open')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(opening_entry_2.user, cashier_user.name)
```


## Complete Example

```python
# Workflow
test_user, pos_profile = self.init_user_and_profile()
opening_entry_1 = create_opening_entry(pos_profile, test_user.name)
self.assertEqual(opening_entry_1.status, 'Open')
self.assertEqual(opening_entry_1.user, test_user.name)
cashier_user = create_user('test_cashier@example.com', 'Accounts Manager', 'Sales Manager')
frappe.set_user(cashier_user.name)
pos_profile2 = make_pos_profile(name='_Test POS Profile 2')
opening_entry_2 = create_opening_entry(pos_profile2, cashier_user.name)
self.assertEqual(opening_entry_2.status, 'Open')
self.assertEqual(opening_entry_2.user, cashier_user.name)
```

## Next Steps


---

*Source: test_pos_opening_entry.py:56 | Complexity: Advanced | Last updated: 2026-02-03*