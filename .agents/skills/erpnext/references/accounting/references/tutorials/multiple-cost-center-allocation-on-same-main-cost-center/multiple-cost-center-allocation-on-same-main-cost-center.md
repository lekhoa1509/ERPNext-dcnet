# How To: Multiple Cost Center Allocation On Same Main Cost Center

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple cost center allocation on same main cost center

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

### Step 1: Assign coa1 = create_cost_center_allocation(...)

```python
coa1 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 30, 'Sub Cost Center 2 - _TC': 30, 'Sub Cost Center 3 - _TC': 40}, valid_from=add_days(today(), -5))
```

### Step 2: Assign coa2 = create_cost_center_allocation(...)

```python
coa2 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}, valid_from=add_days(today(), -1))
```

### Step 3: Assign jv = make_journal_entry(...)

```python
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 3 - _TC', posting_date=today(), submit=True)
```

### Step 4: Assign expected_values = value

```python
expected_values = {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}
```

### Step 5: Assign gle = frappe.qb.DocType(...)

```python
gle = frappe.qb.DocType('GL Entry')
```

### Step 6: Assign gl_entries = frappe.qb.from_.select.where.where.where.orderby.run(...)

```python
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 8: Call coa1.cancel()

```python
coa1.cancel()
```

### Step 9: Call coa2.cancel()

```python
coa2.cancel()
```

### Step 10: Call jv.cancel()

```python
jv.cancel()
```

### Step 11: Call self.assertTrue()

```python
self.assertTrue(gle.cost_center in expected_values)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(gle.debit, 0)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(gle.credit, expected_values[gle.cost_center])
```


## Complete Example

```python
# Workflow
coa1 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 30, 'Sub Cost Center 2 - _TC': 30, 'Sub Cost Center 3 - _TC': 40}, valid_from=add_days(today(), -5))
coa2 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}, valid_from=add_days(today(), -1))
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 3 - _TC', posting_date=today(), submit=True)
expected_values = {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for gle in gl_entries:
    self.assertTrue(gle.cost_center in expected_values)
    self.assertEqual(gle.debit, 0)
    self.assertEqual(gle.credit, expected_values[gle.cost_center])
coa1.cancel()
coa2.cancel()
jv.cancel()
```

## Next Steps


---

*Source: test_cost_center_allocation.py:146 | Complexity: Advanced | Last updated: 2026-02-03*