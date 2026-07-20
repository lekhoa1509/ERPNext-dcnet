# How To: Get Voucher Wise Gl Entry

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test get voucher wise gl entry

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

### Step 1: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Test Item', posting_date='2021-02-01', rate=100, qty=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory')
```

### Step 2: Assign future_vouchers = get_future_stock_vouchers(...)

```python
future_vouchers = get_future_stock_vouchers('2021-01-01', '00:00:00', for_items=['_Test Item'])
```

### Step 3: Assign voucher_type_and_no = value

```python
voucher_type_and_no = ('Purchase Receipt', pr.name)
```

### Step 4: Call self.assertTrue()

```python
self.assertTrue(voucher_type_and_no in future_vouchers, msg='get_future_stock_vouchers not returning correct value')
```

### Step 5: Assign posting_date = '2021-01-01'

```python
posting_date = '2021-01-01'
```

### Step 6: Assign gl_entries = get_voucherwise_gl_entries(...)

```python
gl_entries = get_voucherwise_gl_entries(future_vouchers, posting_date)
```

### Step 7: Call self.assertTrue()

```python
self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')
```


## Complete Example

```python
# Workflow
pr = make_purchase_receipt(item_code='_Test Item', posting_date='2021-02-01', rate=100, qty=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory')
future_vouchers = get_future_stock_vouchers('2021-01-01', '00:00:00', for_items=['_Test Item'])
voucher_type_and_no = ('Purchase Receipt', pr.name)
self.assertTrue(voucher_type_and_no in future_vouchers, msg='get_future_stock_vouchers not returning correct value')
posting_date = '2021-01-01'
gl_entries = get_voucherwise_gl_entries(future_vouchers, posting_date)
self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')
```

## Next Steps


---

*Source: test_utils.py:37 | Complexity: Intermediate | Last updated: 2026-02-03*