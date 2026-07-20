# How To: Tax Calculation With Item Tax Template

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test tax calculation with item tax template

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
inv = create_pos_invoice(qty=84, rate=4.6, do_not_save=1)
```

### Step 2: Assign item_row = value

```python
item_row = inv.get('items')[0]
```

### Step 3: Assign add_items = value

```python
add_items = [(54, '_Test Account Excise Duty @ 12 - _TC'), (288, '_Test Account Excise Duty @ 15 - _TC'), (144, '_Test Account Excise Duty @ 20 - _TC'), (430, '_Test Item Tax Template 1 - _TC')]
```

### Step 4: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account Excise Duty - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Excise Duty', 'doctype': 'Sales Taxes and Charges', 'rate': 11})
```

### Step 5: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 0})
```

### Step 6: Call inv.append()

```python
inv.append('taxes', {'account_head': '_Test Account S&H Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'S&H Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 3})
```

### Step 7: Call inv.insert()

```python
inv.insert()
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(inv.net_total, 4600)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[0].tax_amount, 502.41)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[0].total, 5102.41)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[1].tax_amount, 197.8)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[1].total, 5300.21)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[2].tax_amount, 375.36)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(inv.get('taxes')[2].total, 5675.57)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(inv.grand_total, 5675.57)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(inv.rounding_adjustment, 0.43)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(inv.rounded_total, 5676.0)
```

### Step 18: Assign item_row_copy = copy.deepcopy(...)

```python
item_row_copy = copy.deepcopy(item_row)
```

### Step 19: Assign item_row_copy.qty = qty

```python
item_row_copy.qty = qty
```

### Step 20: Assign item_row_copy.item_tax_template = item_tax_template

```python
item_row_copy.item_tax_template = item_tax_template
```

### Step 21: Call inv.append()

```python
inv.append('items', item_row_copy)
```


## Complete Example

```python
# Workflow
inv = create_pos_invoice(qty=84, rate=4.6, do_not_save=1)
item_row = inv.get('items')[0]
add_items = [(54, '_Test Account Excise Duty @ 12 - _TC'), (288, '_Test Account Excise Duty @ 15 - _TC'), (144, '_Test Account Excise Duty @ 20 - _TC'), (430, '_Test Item Tax Template 1 - _TC')]
for qty, item_tax_template in add_items:
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.qty = qty
    item_row_copy.item_tax_template = item_tax_template
    inv.append('items', item_row_copy)
inv.append('taxes', {'account_head': '_Test Account Excise Duty - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Excise Duty', 'doctype': 'Sales Taxes and Charges', 'rate': 11})
inv.append('taxes', {'account_head': '_Test Account Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 0})
inv.append('taxes', {'account_head': '_Test Account S&H Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'S&H Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 3})
inv.insert()
self.assertEqual(inv.net_total, 4600)
self.assertEqual(inv.get('taxes')[0].tax_amount, 502.41)
self.assertEqual(inv.get('taxes')[0].total, 5102.41)
self.assertEqual(inv.get('taxes')[1].tax_amount, 197.8)
self.assertEqual(inv.get('taxes')[1].total, 5300.21)
self.assertEqual(inv.get('taxes')[2].tax_amount, 375.36)
self.assertEqual(inv.get('taxes')[2].total, 5675.57)
self.assertEqual(inv.grand_total, 5675.57)
self.assertEqual(inv.rounding_adjustment, 0.43)
self.assertEqual(inv.rounded_total, 5676.0)
```

## Next Steps


---

*Source: test_pos_invoice.py:147 | Complexity: Advanced | Last updated: 2026-02-03*