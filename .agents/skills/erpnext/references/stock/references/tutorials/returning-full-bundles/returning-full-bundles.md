# How To: Returning Full Bundles

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test returning full bundles

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

### Step 1: Assign item_list = value

```python
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
```

### Step 2: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
```

### Step 3: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(so.name)
```

### Step 4: Call dn.save()

```python
dn.save()
```

### Step 5: Call dn.submit()

```python
dn.submit()
```

### Step 6: Assign dn_ret = make_sales_return(...)

```python
dn_ret = make_sales_return(dn.name)
```

### Step 7: Call dn_ret.save()

```python
dn_ret.save()
```

### Step 8: Call dn_ret.submit()

```python
dn_ret.submit()
```

### Step 9: Call self.assertReturns()

```python
self.assertReturns(dn.packed_items, dn_ret.packed_items)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.save()
dn_ret.submit()
self.assertReturns(dn.packed_items, dn_ret.packed_items)
```

## Next Steps


---

*Source: test_packed_item.py:192 | Complexity: Advanced | Last updated: 2026-02-04*