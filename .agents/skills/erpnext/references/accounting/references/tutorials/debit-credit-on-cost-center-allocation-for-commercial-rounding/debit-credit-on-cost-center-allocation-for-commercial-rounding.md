# How To: Debit Credit On Cost Center Allocation For Commercial Rounding

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test debit credit on cost center allocation for commercial rounding

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.cost_center_allocation.cost_center_allocation`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`


## Step-by-Step Guide

### Step 1: Assign cca = create_cost_center_allocation(...)

```python
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 2 - _TC': 50, 'Sub Cost Center 3 - _TC': 50})
```

### Step 2: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(rate=145.65, cost_center='Main Cost Center 1 - _TC')
```

### Step 3: Assign gl_entry = frappe.qb.DocType(...)

```python
gl_entry = frappe.qb.DocType('GL Entry')
```

### Step 4: Assign gl_entries = frappe.qb.from_.select.where.where.run(...)

```python
gl_entries = frappe.qb.from_(gl_entry).select(Sum(gl_entry.credit).as_('cr'), Sum(gl_entry.debit).as_('dr')).where(gl_entry.voucher_type == 'Sales Invoice').where(gl_entry.voucher_no == si.name).run(as_dict=1)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)
```

### Step 6: Call si.cancel()

```python
si.cancel()
```

### Step 7: Call cca.cancel()

```python
cca.cancel()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 2 - _TC': 50, 'Sub Cost Center 3 - _TC': 50})
si = create_sales_invoice(rate=145.65, cost_center='Main Cost Center 1 - _TC')
gl_entry = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gl_entry).select(Sum(gl_entry.credit).as_('cr'), Sum(gl_entry.debit).as_('dr')).where(gl_entry.voucher_type == 'Sales Invoice').where(gl_entry.voucher_no == si.name).run(as_dict=1)
self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)
si.cancel()
cca.cancel()
```

## Next Steps


---

*Source: test_cost_center_allocation.py:194 | Complexity: Advanced | Last updated: 2026-02-03*