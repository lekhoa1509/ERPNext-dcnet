# How To: Purchase Invoice With Exchange Rate Difference For Non Stock Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase invoice with exchange rate difference for non stock item

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.controllers.accounts_controller`
- `erpnext.controllers.buying_controller`
- `erpnext.exceptions`
- `erpnext.projects.doctype.project.test_project`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.material_request.material_request`
- `erpnext.stock.doctype.material_request.test_material_request`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.tests.test_utils`
- `erpnext.accounts.utils`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.accounts.doctype.shipping_rule.test_shipping_rule`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.report.trial_balance.test_trial_balance`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`


## Step-by-Step Guide

### Step 1: Assign pr = frappe.new_doc(...)

```python
pr = frappe.new_doc('Purchase Receipt')
```

### Step 2: Assign pr.currency = 'USD'

```python
pr.currency = 'USD'
```

### Step 3: Assign pr.company = '_Test Company with perpetual inventory'

```python
pr.company = '_Test Company with perpetual inventory'
```

### Step 4: Assign pr.conversion_rate = value

```python
pr.conversion_rate = (70,)
```

### Step 5: Assign pr.supplier = '_Test Supplier USD'

```python
pr.supplier = '_Test Supplier USD'
```

### Step 6: Call pr.append()

```python
pr.append('items', {'item_code': '_Test Non Stock Item', 'qty': 1, 'rate': 100})
```

### Step 7: Call pr.append()

```python
pr.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': 5, 'warehouse': 'Stores - TCP1'})
```

### Step 8: Call pr.insert()

```python
pr.insert()
```

### Step 9: Call pr.submit()

```python
pr.submit()
```

### Step 10: Assign pi = create_purchase_invoice(...)

```python
pi = create_purchase_invoice(pr.name)
```

### Step 11: Assign pi.conversion_rate = 80

```python
pi.conversion_rate = 80
```

### Step 12: Assign pi.credit_to = '_Test Payable USD - TCP1'

```python
pi.credit_to = '_Test Payable USD - TCP1'
```

### Step 13: Call pi.insert()

```python
pi.insert()
```

### Step 14: Call pi.submit()

```python
pi.submit()
```

### Step 15: Assign exchange_gain_loss_account = frappe.db.get_value(...)

```python
exchange_gain_loss_account = frappe.db.get_value('Company', pi.company, 'exchange_gain_loss_account')
```

### Step 16: Assign amount = frappe.db.get_value(...)

```python
amount = frappe.db.get_value('GL Entry', {'account': exchange_gain_loss_account, 'voucher_no': pi.name}, 'debit')
```

### Step 17: Assign discrepancy_caused_by_exchange_rate_diff = abs(...)

```python
discrepancy_caused_by_exchange_rate_diff = abs(pi.items[1].base_net_amount - pr.items[1].base_net_amount)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)
```


## Complete Example

```python
# Workflow
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice as create_purchase_invoice
pr = frappe.new_doc('Purchase Receipt')
pr.currency = 'USD'
pr.company = '_Test Company with perpetual inventory'
pr.conversion_rate = (70,)
pr.supplier = '_Test Supplier USD'
pr.append('items', {'item_code': '_Test Non Stock Item', 'qty': 1, 'rate': 100})
pr.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': 5, 'warehouse': 'Stores - TCP1'})
pr.insert()
pr.submit()
pi = create_purchase_invoice(pr.name)
pi.conversion_rate = 80
pi.credit_to = '_Test Payable USD - TCP1'
pi.insert()
pi.submit()
exchange_gain_loss_account = frappe.db.get_value('Company', pi.company, 'exchange_gain_loss_account')
amount = frappe.db.get_value('GL Entry', {'account': exchange_gain_loss_account, 'voucher_no': pi.name}, 'debit')
discrepancy_caused_by_exchange_rate_diff = abs(pi.items[1].base_net_amount - pr.items[1].base_net_amount)
self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)
```

## Next Steps


---

*Source: test_purchase_invoice.py:386 | Complexity: Advanced | Last updated: 2026-02-03*