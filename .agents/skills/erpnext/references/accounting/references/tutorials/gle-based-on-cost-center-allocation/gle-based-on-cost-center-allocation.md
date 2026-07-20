# How To: Gle Based On Cost Center Allocation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test gle based on cost center allocation

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
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 1 - _TC': 60, 'Sub Cost Center 2 - _TC': 40})
```

### Step 2: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 1 - _TC', submit=True)
```

### Step 3: Assign expected_values = value

```python
expected_values = [['Sub Cost Center 1 - _TC', 0.0, 60], ['Sub Cost Center 2 - _TC', 0.0, 40]]
```

### Step 4: Assign gle = frappe.qb.DocType(...)

```python
gle = frappe.qb.DocType('GL Entry')
```

### Step 5: Assign gl_entries = frappe.qb.from_.select.where.where.where.orderby.run(...)

```python
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
```

### Step 6: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 7: Call cca.cancel()

```python
cca.cancel()
```

### Step 8: Call jv.cancel()

```python
jv.cancel()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][0], gle.cost_center)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][1], gle.debit)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(expected_values[i][2], gle.credit)
```


## Complete Example

```python
# Workflow
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 1 - _TC': 60, 'Sub Cost Center 2 - _TC': 40})
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 1 - _TC', submit=True)
expected_values = [['Sub Cost Center 1 - _TC', 0.0, 60], ['Sub Cost Center 2 - _TC', 0.0, 40]]
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for i, gle in enumerate(gl_entries):
    self.assertEqual(expected_values[i][0], gle.cost_center)
    self.assertEqual(expected_values[i][1], gle.debit)
    self.assertEqual(expected_values[i][2], gle.credit)
cca.cancel()
jv.cancel()
```

## Next Steps


---

*Source: test_cost_center_allocation.py:33 | Complexity: Advanced | Last updated: 2026-02-03*