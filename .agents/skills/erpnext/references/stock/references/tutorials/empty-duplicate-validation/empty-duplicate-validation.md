# How To: Empty Duplicate Validation

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test empty duplicate validation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.tests.utils`
- `erpnext.stock.doctype.item_price.item_price`
- `erpnext.stock.get_item_details`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign doc = frappe.copy_doc(...)

```python
doc = frappe.copy_doc(self.globalTestRecords['Item Price'][2])
```

### Step 2: Assign doc.customer = None

```python
doc.customer = None
```

### Step 3: Assign doc.price_list_rate = 21

```python
doc.price_list_rate = 21
```

### Step 4: Call doc.insert()

```python
doc.insert()
```

### Step 5: Assign ctx = ItemDetailsCtx(...)

```python
ctx = ItemDetailsCtx({'price_list': doc.price_list, 'uom': '_Test UOM', 'transaction_date': '2017-04-18', 'qty': 7})
```

### Step 6: Assign price = get_price_list_rate_for(...)

```python
price = get_price_list_rate_for(ctx, doc.item_code)
```

### Step 7: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(price, 21)
```


## Complete Example

```python
# Workflow
doc = frappe.copy_doc(self.globalTestRecords['Item Price'][2])
doc.customer = None
doc.price_list_rate = 21
doc.insert()
ctx = ItemDetailsCtx({'price_list': doc.price_list, 'uom': '_Test UOM', 'transaction_date': '2017-04-18', 'qty': 7})
price = get_price_list_rate_for(ctx, doc.item_code)
frappe.db.rollback()
self.assertEqual(price, 21)
```

## Next Steps


---

*Source: test_item_price.py:181 | Complexity: Advanced | Last updated: 2026-02-04*