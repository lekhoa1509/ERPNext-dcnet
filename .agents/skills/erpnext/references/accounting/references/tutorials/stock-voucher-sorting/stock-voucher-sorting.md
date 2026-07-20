# How To: Stock Voucher Sorting

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test stock voucher sorting

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.test_runner`
- `frappe.tests`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.utils`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.supplier.test_supplier`


## Step-by-Step Guide

### Step 1: Assign vouchers = value

```python
vouchers = []
```

### Step 2: Assign item = value

```python
item = make_item().name
```

### Step 3: Assign stock_entry = value

```python
stock_entry = {'item': item, 'to_warehouse': '_Test Warehouse - _TC', 'qty': 1, 'rate': 10}
```

### Step 4: Assign se1 = make_stock_entry(...)

```python
se1 = make_stock_entry(posting_date='2022-01-01', **stock_entry)
```

### Step 5: Assign se3 = make_stock_entry(...)

```python
se3 = make_stock_entry(posting_date='2022-03-01', **stock_entry)
```

### Step 6: Assign se2 = make_stock_entry(...)

```python
se2 = make_stock_entry(posting_date='2022-02-01', **stock_entry)
```

### Step 7: Call vouchers.append()

```python
vouchers.append(('Stock Entry', 'Wat'))
```

### Step 8: Assign sorted_vouchers = sort_stock_vouchers_by_posting_date(...)

```python
sorted_vouchers = sort_stock_vouchers_by_posting_date(list(reversed(vouchers)))
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(sorted_vouchers, vouchers)
```

### Step 10: Call vouchers.append()

```python
vouchers.append((doc.doctype, doc.name))
```


## Complete Example

```python
# Workflow
vouchers = []
item = make_item().name
stock_entry = {'item': item, 'to_warehouse': '_Test Warehouse - _TC', 'qty': 1, 'rate': 10}
se1 = make_stock_entry(posting_date='2022-01-01', **stock_entry)
se3 = make_stock_entry(posting_date='2022-03-01', **stock_entry)
se2 = make_stock_entry(posting_date='2022-02-01', **stock_entry)
for doc in (se1, se2, se3):
    vouchers.append((doc.doctype, doc.name))
vouchers.append(('Stock Entry', 'Wat'))
sorted_vouchers = sort_stock_vouchers_by_posting_date(list(reversed(vouchers)))
self.assertEqual(sorted_vouchers, vouchers)
```

## Next Steps


---

*Source: test_utils.py:62 | Complexity: Advanced | Last updated: 2026-02-03*