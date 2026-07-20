# How To: Rename Entries

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test rename entries

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.model.naming`
- `frappe.tests`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`


## Step-by-Step Guide

### Step 1: Assign je = make_journal_entry(...)

```python
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
```

### Step 2: Call rename_gle_sle_docs()

```python
rename_gle_sle_docs()
```

### Step 3: Assign naming_series = parse_naming_series(...)

```python
naming_series = parse_naming_series(parts=frappe.get_meta('GL Entry').autoname.split('.')[:-1])
```

### Step 4: Assign je = make_journal_entry(...)

```python
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
```

### Step 5: Assign gl_entries = frappe.get_all(...)

```python
gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(all((entry.to_rename == 1 for entry in gl_entries)))
```

### Step 7: Assign old_naming_series_current_value = value

```python
old_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
```

### Step 8: Call rename_gle_sle_docs()

```python
rename_gle_sle_docs()
```

### Step 9: Assign new_gl_entries = frappe.get_all(...)

```python
new_gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
```

### Step 12: Assign new_naming_series_current_value = value

```python
new_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)
```


## Complete Example

```python
# Workflow
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
rename_gle_sle_docs()
naming_series = parse_naming_series(parts=frappe.get_meta('GL Entry').autoname.split('.')[:-1])
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 1 for entry in gl_entries)))
old_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
rename_gle_sle_docs()
new_gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
new_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)
```

## Next Steps


---

*Source: test_gl_entry.py:39 | Complexity: Advanced | Last updated: 2026-02-03*