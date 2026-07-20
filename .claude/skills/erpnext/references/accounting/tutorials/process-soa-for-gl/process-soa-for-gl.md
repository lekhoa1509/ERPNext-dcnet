# How To: Process Soa For Gl

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: Tests the utils for Statement of Accounts(General Ledger)

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: 'Tests the utils for Statement of Accounts(General Ledger)'

```python
'Tests the utils for Statement of Accounts(General Ledger)'
```

### Step 2: Assign process_soa = create_process_soa(...)

```python
process_soa = create_process_soa(name='_Test Process SOA for GL', customers=[{'customer': '_Test Customer'}, {'customer': 'Other Customer'}])
```

### Step 3: Assign statement_dict = get_statement_dict(...)

```python
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
```

### Step 4: Call self.assertIn()

```python
self.assertIn('Other Customer', statement_dict)
```

### Step 5: Call self.assertIn()

```python
self.assertIn('_Test Customer', statement_dict)
```

### Step 6: Assign receivable_entries = value

```python
receivable_entries = statement_dict['_Test Customer'][0]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(receivable_entries), 4)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(receivable_entries[1].balance, 100)
```


## Complete Example

```python
# Workflow
'Tests the utils for Statement of Accounts(General Ledger)'
process_soa = create_process_soa(name='_Test Process SOA for GL', customers=[{'customer': '_Test Customer'}, {'customer': 'Other Customer'}])
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 4)
self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
self.assertEqual(receivable_entries[1].balance, 100)
```

## Next Steps


---

*Source: test_process_statement_of_accounts.py:31 | Complexity: Advanced | Last updated: 2026-02-03*