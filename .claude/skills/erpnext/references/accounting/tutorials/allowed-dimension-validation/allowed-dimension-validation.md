# How To: Allowed Dimension Validation

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test allowed dimension validation

## Prerequisites

**Required Modules:**
- `unittest`
- `frappe`
- `erpnext.accounts.doctype.accounting_dimension.test_accounting_dimension`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.exceptions`


## Step-by-Step Guide

### Step 1: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=1)
```

### Step 2: Assign unknown.cost_center = 'Main - _TC'

```python
si.items[0].cost_center = 'Main - _TC'
```

### Step 3: Assign si.department = 'Accounts - _TC'

```python
si.department = 'Accounts - _TC'
```

### Step 4: Assign si.location = 'Block 1'

```python
si.location = 'Block 1'
```

### Step 5: Call si.save()

```python
si.save()
```

### Step 6: Call self.assertRaises()

```python
self.assertRaises(InvalidAccountDimensionError, si.submit)
```

### Step 7: Call self.invoice_list.append()

```python
self.invoice_list.append(si)
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(do_not_save=1)
si.items[0].cost_center = 'Main - _TC'
si.department = 'Accounts - _TC'
si.location = 'Block 1'
si.save()
self.assertRaises(InvalidAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

## Next Steps


---

*Source: test_accounting_dimension_filter.py:24 | Complexity: Intermediate | Last updated: 2026-02-03*