# How To: Mandatory Dimension Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: unittest, workflow, integration

## Overview

Workflow: test mandatory dimension validation

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

### Step 2: Assign si.department = ''

```python
si.department = ''
```

### Step 3: Assign si.location = 'Block 1'

```python
si.location = 'Block 1'
```

### Step 4: Assign unknown.department = ''

```python
si.items[0].department = ''
```

### Step 5: Assign unknown.cost_center = '_Test Cost Center 2 - _TC'

```python
si.items[0].cost_center = '_Test Cost Center 2 - _TC'
```

### Step 6: Call si.save()

```python
si.save()
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(MandatoryAccountDimensionError, si.submit)
```

### Step 8: Call self.invoice_list.append()

```python
self.invoice_list.append(si)
```


## Complete Example

```python
# Workflow
si = create_sales_invoice(do_not_save=1)
si.department = ''
si.location = 'Block 1'
si.items[0].department = ''
si.items[0].cost_center = '_Test Cost Center 2 - _TC'
si.save()
self.assertRaises(MandatoryAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

## Next Steps


---

*Source: test_accounting_dimension_filter.py:34 | Complexity: Advanced | Last updated: 2026-02-03*