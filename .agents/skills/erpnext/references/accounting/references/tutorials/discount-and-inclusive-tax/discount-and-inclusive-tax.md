# How To: Discount And Inclusive Tax

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test discount and inclusive tax

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.mode_of_payment.test_mode_of_payment`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_profile.test_pos_profile`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry`
- `time`
- `time`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.doctype.loyalty_program.test_loyalty_program`
- `erpnext.accounts.doctype.loyalty_program.loyalty_program`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry`
- `erpnext.accounts.doctype.pos_invoice_merge_log.pos_invoice_merge_log`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.serial_batch_bundle`
- `erpnext.accounts.doctype.pricing_rule.test_pricing_rule`
- `erpnext.accounts.doctype.pos_invoice_merge_log.test_pos_invoice_merge_log`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.accounts.doctype.pos_invoice.pos_invoice`
- `erpnext.accounts.doctype.pos_invoice_merge_log.test_pos_invoice_merge_log`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign inv = create_pos_invoice(...)

```python
inv = create_pos_invoice(qty=100, rate=50, do_not_save=1)
```

### Step 2: Call inv.append()

```python
inv.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 14, 'included_in_print_rate': 1})
```

### Step 3: Call inv.insert()

```python
inv.insert()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(inv.net_total, 4385.96)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(inv.grand_total, 5000)
```

### Step 6: Call inv.reload()

```python
inv.reload()
```

### Step 7: Assign inv.discount_amount = 100

```python
inv.discount_amount = 100
```

### Step 8: Assign inv.apply_discount_on = 'Net Total'

```python
inv.apply_discount_on = 'Net Total'
```

### Step 9: Assign inv.payment_schedule = value

```python
inv.payment_schedule = []
```

### Step 10: Call inv.save()

```python
inv.save()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(inv.net_total, 4285.96)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(inv.grand_total, 4885.99)
```

### Step 13: Call inv.reload()

```python
inv.reload()
```

### Step 14: Assign inv.discount_amount = 100

```python
inv.discount_amount = 100
```

### Step 15: Assign inv.apply_discount_on = 'Grand Total'

```python
inv.apply_discount_on = 'Grand Total'
```

### Step 16: Assign inv.payment_schedule = value

```python
inv.payment_schedule = []
```

### Step 17: Call inv.save()

```python
inv.save()
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(inv.net_total, 4298.24)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(inv.grand_total, 4900.0)
```


## Complete Example

```python
# Workflow
inv = create_pos_invoice(qty=100, rate=50, do_not_save=1)
inv.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 14, 'included_in_print_rate': 1})
inv.insert()
self.assertEqual(inv.net_total, 4385.96)
self.assertEqual(inv.grand_total, 5000)
inv.reload()
inv.discount_amount = 100
inv.apply_discount_on = 'Net Total'
inv.payment_schedule = []
inv.save()
self.assertEqual(inv.net_total, 4285.96)
self.assertEqual(inv.grand_total, 4885.99)
inv.reload()
inv.discount_amount = 100
inv.apply_discount_on = 'Grand Total'
inv.payment_schedule = []
inv.save()
self.assertEqual(inv.net_total, 4298.24)
self.assertEqual(inv.grand_total, 4900.0)
```

## Next Steps


---

*Source: test_pos_invoice.py:79 | Complexity: Advanced | Last updated: 2026-02-03*