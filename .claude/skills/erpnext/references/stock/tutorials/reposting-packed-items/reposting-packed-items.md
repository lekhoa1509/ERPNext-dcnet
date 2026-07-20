# How To: Reposting Packed Items

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test reposting packed items

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

### Step 1: Assign warehouse = 'Stores - TCP1'

```python
warehouse = 'Stores - TCP1'
```

### Step 2: Assign company = '_Test Company with perpetual inventory'

```python
company = '_Test Company with perpetual inventory'
```

### Step 3: Assign today = nowdate(...)

```python
today = nowdate()
```

### Step 4: Assign yesterday = add_to_date(...)

```python
yesterday = add_to_date(today, days=-1, as_string=True)
```

### Step 5: Assign so = make_sales_order(...)

```python
so = make_sales_order(item_code=self.bundle, qty=1, company=company, warehouse=warehouse)
```

### Step 6: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(so.name)
```

### Step 7: Call dn.save()

```python
dn.save()
```

### Step 8: Call dn.submit()

```python
dn.submit()
```

### Step 9: Assign gles = get_gl_entries(...)

```python
gles = get_gl_entries(dn.doctype, dn.name)
```

### Step 10: Assign credit_before_repost = sum(...)

```python
credit_before_repost = sum((gle.credit for gle in gles))
```

### Step 11: Assign gles = get_gl_entries(...)

```python
gles = get_gl_entries(dn.doctype, dn.name)
```

### Step 12: Assign credit_after_reposting = sum(...)

```python
credit_after_reposting = sum((gle.credit for gle in gles))
```

### Step 13: Call self.assertNotEqual()

```python
self.assertNotEqual(credit_before_repost, credit_after_reposting)
```

### Step 14: Call self.assertAlmostEqual()

```python
self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)
```

### Step 15: Call make_stock_entry()

```python
make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=100, posting_date=today)
```

### Step 16: Call make_stock_entry()

```python
make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=200, posting_date=yesterday)
```


## Complete Example

```python
# Workflow
warehouse = 'Stores - TCP1'
company = '_Test Company with perpetual inventory'
today = nowdate()
yesterday = add_to_date(today, days=-1, as_string=True)
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=100, posting_date=today)
so = make_sales_order(item_code=self.bundle, qty=1, company=company, warehouse=warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
gles = get_gl_entries(dn.doctype, dn.name)
credit_before_repost = sum((gle.credit for gle in gles))
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=200, posting_date=yesterday)
gles = get_gl_entries(dn.doctype, dn.name)
credit_after_reposting = sum((gle.credit for gle in gles))
self.assertNotEqual(credit_before_repost, credit_after_reposting)
self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)
```

## Next Steps


---

*Source: test_packed_item.py:150 | Complexity: Advanced | Last updated: 2026-02-04*