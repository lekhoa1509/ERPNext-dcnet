# How To: Supplier Ledger Summary With Filters

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test supplier ledger summary with filters

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.report.supplier_ledger_summary.supplier_ledger_summary`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: Call self.create_purchase_invoice()

```python
self.create_purchase_invoice()
```

### Step 2: Assign supplier_group = frappe.db.get_value(...)

```python
supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
```

### Step 3: Assign filters = value

```python
filters = {'company': self.company, 'from_date': today(), 'to_date': today(), 'supplier_group': supplier_group}
```

### Step 4: Assign expected = value

```python
expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
```

### Step 5: Assign report_output = value

```python
report_output = execute(filters)[1]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(report_output), 1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(report_output[0].get(field), expected.get(field))
```


## Complete Example

```python
# Workflow
self.create_purchase_invoice()
supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
filters = {'company': self.company, 'from_date': today(), 'to_date': today(), 'supplier_group': supplier_group}
expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
report_output = execute(filters)[1]
self.assertEqual(len(report_output), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report_output[0].get(field), expected.get(field))
```

## Next Steps


---

*Source: test_supplier_ledger_summary.py:63 | Complexity: Intermediate | Last updated: 2026-02-03*