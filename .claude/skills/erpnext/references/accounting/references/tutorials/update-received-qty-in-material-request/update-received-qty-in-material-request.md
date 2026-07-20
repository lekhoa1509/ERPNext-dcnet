# How To: Update Received Qty In Material Request

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update received qty in material request

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

### Step 1: '\n\t\tTest if the received_qty in Material Request is updated correctly when\n\t\ta Purchase Invoice with update_stock=True is submitted.\n\t\t'

```python
'\n\t\tTest if the received_qty in Material Request is updated correctly when\n\t\ta Purchase Invoice with update_stock=True is submitted.\n\t\t'
```

### Step 2: Assign mr = make_material_request(...)

```python
mr = make_material_request(item_code='_Test Item', qty=10)
```

### Step 3: Call mr.save()

```python
mr.save()
```

### Step 4: Call mr.submit()

```python
mr.submit()
```

### Step 5: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(mr.name)
```

### Step 6: Assign po.supplier = '_Test Supplier'

```python
po.supplier = '_Test Supplier'
```

### Step 7: Call po.save()

```python
po.save()
```

### Step 8: Call po.submit()

```python
po.submit()
```

### Step 9: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(po.name)
```

### Step 10: Assign pi.update_stock = True

```python
pi.update_stock = True
```

### Step 11: Call pi.insert()

```python
pi.insert()
```

### Step 12: Call pi.submit()

```python
pi.submit()
```

### Step 13: Call mr.reload()

```python
mr.reload()
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(mr.items[0].received_qty, 10)
```


## Complete Example

```python
# Workflow
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice
'\n\t\tTest if the received_qty in Material Request is updated correctly when\n\t\ta Purchase Invoice with update_stock=True is submitted.\n\t\t'
mr = make_material_request(item_code='_Test Item', qty=10)
mr.save()
mr.submit()
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save()
po.submit()
pi = make_purchase_invoice(po.name)
pi.update_stock = True
pi.insert()
pi.submit()
mr.reload()
self.assertEqual(mr.items[0].received_qty, 10)
```

## Next Steps


---

*Source: test_purchase_invoice.py:92 | Complexity: Advanced | Last updated: 2026-02-03*