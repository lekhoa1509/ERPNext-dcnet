# How To: Finance Book

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test finance book

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`


## Step-by-Step Guide

### Step 1: Assign finance_book = create_finance_book(...)

```python
finance_book = create_finance_book()
```

### Step 2: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
```

### Step 3: Call unknown.update()

```python
jv.accounts[1].update({'party_type': 'Customer', 'party': '_Test Customer'})
```

### Step 4: Assign jv.finance_book = value

```python
jv.finance_book = finance_book.finance_book_name
```

### Step 5: Call jv.submit()

```python
jv.submit()
```

### Step 6: Assign gl_entries = frappe.get_all(...)

```python
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(gl_entry.finance_book, finance_book.name)
```


## Complete Example

```python
# Workflow
finance_book = create_finance_book()
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
jv.accounts[1].update({'party_type': 'Customer', 'party': '_Test Customer'})
jv.finance_book = finance_book.finance_book_name
jv.submit()
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
for gl_entry in gl_entries:
    self.assertEqual(gl_entry.finance_book, finance_book.name)
```

## Next Steps


---

*Source: test_finance_book.py:11 | Complexity: Advanced | Last updated: 2026-02-03*