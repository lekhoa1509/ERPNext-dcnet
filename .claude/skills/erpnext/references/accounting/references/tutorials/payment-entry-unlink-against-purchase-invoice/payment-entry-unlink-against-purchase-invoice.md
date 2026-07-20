# How To: Payment Entry Unlink Against Purchase Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry unlink against purchase invoice

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

### Step 1: Call unlink_payment_on_cancel_of_invoice()

```python
unlink_payment_on_cancel_of_invoice(0)
```

### Step 2: Assign pi_doc = make_purchase_invoice(...)

```python
pi_doc = make_purchase_invoice()
```

### Step 3: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry('Purchase Invoice', pi_doc.name, bank_account='_Test Bank - _TC')
```

### Step 4: Assign pe.reference_no = '1'

```python
pe.reference_no = '1'
```

### Step 5: Assign pe.reference_date = nowdate(...)

```python
pe.reference_date = nowdate()
```

### Step 6: Assign pe.paid_from_account_currency = value

```python
pe.paid_from_account_currency = pi_doc.currency
```

### Step 7: Assign pe.paid_to_account_currency = value

```python
pe.paid_to_account_currency = pi_doc.currency
```

### Step 8: Assign pe.source_exchange_rate = 1

```python
pe.source_exchange_rate = 1
```

### Step 9: Assign pe.target_exchange_rate = 1

```python
pe.target_exchange_rate = 1
```

### Step 10: Assign pe.paid_amount = value

```python
pe.paid_amount = pi_doc.grand_total
```

### Step 11: Call pe.save()

```python
pe.save(ignore_permissions=True)
```

### Step 12: Call pe.submit()

```python
pe.submit()
```

### Step 13: Assign pi_doc = frappe.get_doc(...)

```python
pi_doc = frappe.get_doc('Purchase Invoice', pi_doc.name)
```

### Step 14: Call pi_doc.load_from_db()

```python
pi_doc.load_from_db()
```

### Step 15: Call self.assertTrue()

```python
self.assertTrue(pi_doc.status, 'Paid')
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(frappe.LinkExistsError, pi_doc.cancel)
```

### Step 17: Call unlink_payment_on_cancel_of_invoice()

```python
unlink_payment_on_cancel_of_invoice()
```


## Complete Example

```python
# Workflow
from erpnext.accounts.doctype.payment_entry.test_payment_entry import get_payment_entry
unlink_payment_on_cancel_of_invoice(0)
pi_doc = make_purchase_invoice()
pe = get_payment_entry('Purchase Invoice', pi_doc.name, bank_account='_Test Bank - _TC')
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from_account_currency = pi_doc.currency
pe.paid_to_account_currency = pi_doc.currency
pe.source_exchange_rate = 1
pe.target_exchange_rate = 1
pe.paid_amount = pi_doc.grand_total
pe.save(ignore_permissions=True)
pe.submit()
pi_doc = frappe.get_doc('Purchase Invoice', pi_doc.name)
pi_doc.load_from_db()
self.assertTrue(pi_doc.status, 'Paid')
self.assertRaises(frappe.LinkExistsError, pi_doc.cancel)
unlink_payment_on_cancel_of_invoice()
```

## Next Steps


---

*Source: test_purchase_invoice.py:165 | Complexity: Advanced | Last updated: 2026-02-03*