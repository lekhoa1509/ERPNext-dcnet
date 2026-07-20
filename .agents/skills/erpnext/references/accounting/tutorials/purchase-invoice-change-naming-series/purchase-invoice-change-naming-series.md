# How To: Purchase Invoice Change Naming Series

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase invoice change naming series

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

### Step 1: Assign pi = frappe.copy_doc(...)

```python
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][1])
```

### Step 2: Call pi.insert()

```python
pi.insert()
```

### Step 3: Assign pi.naming_series = 'TEST-'

```python
pi.naming_series = 'TEST-'
```

### Step 4: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
```

### Step 5: Assign pi = frappe.copy_doc(...)

```python
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
```

### Step 6: Call pi.insert()

```python
pi.insert()
```

### Step 7: Call pi.load_from_db()

```python
pi.load_from_db()
```

### Step 8: Call self.assertTrue()

```python
self.assertTrue(pi.status, 'Draft')
```

### Step 9: Assign pi.naming_series = 'TEST-'

```python
pi.naming_series = 'TEST-'
```

### Step 10: Call self.assertRaises()

```python
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
```


## Complete Example

```python
# Workflow
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][1])
pi.insert()
pi.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
pi.insert()
pi.load_from_db()
self.assertTrue(pi.status, 'Draft')
pi.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
```

## Next Steps


---

*Source: test_purchase_invoice.py:433 | Complexity: Advanced | Last updated: 2026-02-03*