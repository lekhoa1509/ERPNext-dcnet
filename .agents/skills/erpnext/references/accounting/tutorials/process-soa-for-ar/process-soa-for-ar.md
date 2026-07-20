# How To: Process Soa For Ar

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Tests the utils for Statement of Accounts(Accounts Receivable)

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: 'Tests the utils for Statement of Accounts(Accounts Receivable)'

```python
'Tests the utils for Statement of Accounts(Accounts Receivable)'
```

### Step 2: Assign process_soa = create_process_soa(...)

```python
process_soa = create_process_soa(name='_Test Process SOA for AR', report='Accounts Receivable')
```

### Step 3: Assign statement_dict = get_statement_dict(...)

```python
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
```

### Step 4: Call self.assertNotIn()

```python
self.assertNotIn('Other Customer', statement_dict)
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
self.assertEqual(len(receivable_entries), 1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(receivable_entries[0].voucher_no, self.si.name)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(receivable_entries[0].total_due, 100)
```

### Step 10: Assign ageing_summary = value

```python
ageing_summary = statement_dict['_Test Customer'][1][0]
```

### Step 11: Assign expected_summary = frappe._dict(...)

```python
expected_summary = frappe._dict(range1=100, range2=0, range3=0, range4=0, range5=0)
```

### Step 12: Call self.check_ageing_summary()

```python
self.check_ageing_summary(ageing_summary, expected_summary)
```


## Complete Example

```python
# Workflow
'Tests the utils for Statement of Accounts(Accounts Receivable)'
process_soa = create_process_soa(name='_Test Process SOA for AR', report='Accounts Receivable')
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertNotIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 1)
self.assertEqual(receivable_entries[0].voucher_no, self.si.name)
self.assertEqual(receivable_entries[0].total_due, 100)
ageing_summary = statement_dict['_Test Customer'][1][0]
expected_summary = frappe._dict(range1=100, range2=0, range3=0, range4=0, range5=0)
self.check_ageing_summary(ageing_summary, expected_summary)
```

## Next Steps


---

*Source: test_process_statement_of_accounts.py:52 | Complexity: Advanced | Last updated: 2026-02-03*