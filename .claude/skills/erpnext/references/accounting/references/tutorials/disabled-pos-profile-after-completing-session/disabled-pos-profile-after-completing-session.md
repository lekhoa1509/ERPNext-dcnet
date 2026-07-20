# How To: Disabled Pos Profile After Completing Session

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test disabled pos profile after completing session

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.pos_profile.pos_profile`
- `erpnext.stock.get_item_details`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`


## Step-by-Step Guide

### Step 1: Assign unknown = init_user_and_profile(...)

```python
test_user, pos_profile = init_user_and_profile()
```

### Step 2: Assign opening_entry = create_opening_entry(...)

```python
opening_entry = create_opening_entry(pos_profile, test_user.name)
```

### Step 3: Assign closing_entry = make_closing_entry_from_opening(...)

```python
closing_entry = make_closing_entry_from_opening(opening_entry)
```

### Step 4: Call closing_entry.submit()

```python
closing_entry.submit()
```

### Step 5: Assign pos_profile.disabled = 1

```python
pos_profile.disabled = 1
```

### Step 6: Call pos_profile.save()

```python
pos_profile.save()
```

### Step 7: Call pos_profile.reload()

```python
pos_profile.reload()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pos_profile.disabled, 1)
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
from erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry import create_opening_entry
test_user, pos_profile = init_user_and_profile()
if pos_profile:
    opening_entry = create_opening_entry(pos_profile, test_user.name)
    closing_entry = make_closing_entry_from_opening(opening_entry)
    closing_entry.submit()
    pos_profile.disabled = 1
    pos_profile.save()
    pos_profile.reload()
    self.assertEqual(pos_profile.disabled, 1)
```

## Next Steps


---

*Source: test_pos_profile.py:62 | Complexity: Advanced | Last updated: 2026-02-03*