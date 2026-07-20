# How To: Tax Calculation With Multiple Items And Discount

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test tax calculation with multiple items and discount

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
inv = create_pos_invoice(qty=1, rate=75, do_not_save=True)
```

### Step 2: Assign item_row = value

```python
item_row = inv.get('items')[0]
```

### Step 3: Assign inv.apply_discount_on = 'Net Total'

```python
inv.apply_discount_on = 'Net Total'
```

### Step 4: Assign inv.discount_amount = 75.0

```python
inv.discount_amount = 75.0
```

### Step 5: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 24})
```

### Step 6: Call inv.insert()

```python
inv.insert()
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(inv.total, 975)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(inv.net_total, 900)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[0].tax_amount, 216.0)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[0].total, 1116.0)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(inv.grand_total, 1116.0)
```

### Step 12: Assign item_row_copy = copy.deepcopy(...)

```python
item_row_copy = copy.deepcopy(item_row)
```

### Step 13: Assign item_row_copy.price_list_rate = rate

```python
item_row_copy.price_list_rate = rate
```

### Step 14: Assign item_row_copy.rate = rate

```python
item_row_copy.rate = rate
```

### Step 15: Call inv.append()

```python
inv.append('items', item_row_copy)
```


## Complete Example

```python
# Workflow
inv = create_pos_invoice(qty=1, rate=75, do_not_save=True)
item_row = inv.get('items')[0]
for rate in (500, 200, 100, 50, 50):
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.price_list_rate = rate
    item_row_copy.rate = rate
    inv.append('items', item_row_copy)
inv.apply_discount_on = 'Net Total'
inv.discount_amount = 75.0
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 24})
inv.insert()
self.assertEqual(inv.total, 975)
self.assertEqual(inv.net_total, 900)
self.assertEqual(inv.get('taxes')[0].tax_amount, 216.0)
self.assertEqual(inv.get('taxes')[0].total, 1116.0)
self.assertEqual(inv.grand_total, 1116.0)
```

## Next Steps


---

*Source: test_pos_invoice.py:213 | Complexity: Advanced | Last updated: 2026-02-03*