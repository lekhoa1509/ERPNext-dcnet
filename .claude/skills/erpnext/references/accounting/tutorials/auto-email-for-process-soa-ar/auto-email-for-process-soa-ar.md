# How To: Auto Email For Process Soa Ar

**Difficulty**: Intermediate
**Estimated Time**: 10 minutes
**Tags**: workflow, integration

## Overview

Workflow: test auto email for process soa ar

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.process_statement_of_accounts.process_statement_of_accounts`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Assign process_soa = create_process_soa(...)

```python
process_soa = create_process_soa(name='_Test Process SOA', enable_auto_email=1, report='Accounts Receivable')
```

### Step 2: Call send_emails()

```python
send_emails(process_soa.name, from_scheduler=True)
```

### Step 3: Call process_soa.load_from_db()

```python
process_soa.load_from_db()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))
```


## Complete Example

```python
# Workflow
process_soa = create_process_soa(name='_Test Process SOA', enable_auto_email=1, report='Accounts Receivable')
send_emails(process_soa.name, from_scheduler=True)
process_soa.load_from_db()
self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))
```

## Next Steps


---

*Source: test_process_statement_of_accounts.py:80 | Complexity: Intermediate | Last updated: 2026-02-03*