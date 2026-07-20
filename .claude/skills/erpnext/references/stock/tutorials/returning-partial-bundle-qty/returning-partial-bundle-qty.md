# How To: Returning Partial Bundle Qty

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test returning partial bundle qty

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`


## Step-by-Step Guide

### Step 1: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=self.bundle, warehouse=self.warehouse, qty=2)
```

### Step 2: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(so.name)
```

### Step 3: Call dn.save()

```python
dn.save()
```

### Step 4: Call dn.submit()

```python
dn.submit()
```

### Step 5: Assign dn_ret = make_sales_return(...)

```python
dn_ret = make_sales_return(dn.name)
```

### Step 6: Assign unknown.qty = value

```python
dn_ret.items[0].qty = -1
```

### Step 7: Call dn_ret.save()

```python
dn_ret.save()
```

### Step 8: Call dn_ret.submit()

```python
dn_ret.submit()
```

### Step 9: Assign expected_returns = value

```python
expected_returns = dn.packed_items
```

### Step 10: Call self.assertReturns()

```python
self.assertReturns(expected_returns, dn_ret.packed_items)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
so = make_sales_order(item_code=self.bundle, warehouse=self.warehouse, qty=2)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.items[0].qty = -1
dn_ret.save()
dn_ret.submit()
expected_returns = dn.packed_items
for d in expected_returns:
    d.qty /= 2
self.assertReturns(expected_returns, dn_ret.packed_items)
```

## Next Steps


---

*Source: test_packed_item.py:258 | Complexity: Advanced | Last updated: 2026-02-04*