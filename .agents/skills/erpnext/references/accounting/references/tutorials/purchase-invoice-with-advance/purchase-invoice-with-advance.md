# How To: Purchase Invoice With Advance

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase invoice with advance

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

### Step 1: Assign jv = frappe.copy_doc(...)

```python
jv = frappe.copy_doc(self.globalTestRecords['Journal Entry'][1])
```

### Step 2: Call jv.insert()

```python
jv.insert()
```

### Step 3: Call jv.submit()

```python
jv.submit()
```

### Step 4: Assign pi = frappe.copy_doc(...)

```python
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
```

### Step 5: Assign pi.disable_rounded_total = 1

```python
pi.disable_rounded_total = 1
```

### Step 6: Assign pi.allocate_advances_automatically = 0

```python
pi.allocate_advances_automatically = 0
```

### Step 7: Call pi.append()

```python
pi.append('advances', {'reference_type': 'Journal Entry', 'reference_name': jv.name, 'reference_row': jv.get('accounts')[0].name, 'advance_amount': 400, 'allocated_amount': 300, 'remarks': jv.remark})
```

### Step 8: Call pi.insert()

```python
pi.insert()
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pi.outstanding_amount, 1212.3)
```

### Step 10: Assign pi.disable_rounded_total = 0

```python
pi.disable_rounded_total = 0
```

### Step 11: Assign unknown.payment_amount = 1512.0

```python
pi.get('payment_schedule')[0].payment_amount = 1512.0
```

### Step 12: Call pi.save()

```python
pi.save()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pi.outstanding_amount, 1212.0)
```

### Step 14: Call pi.submit()

```python
pi.submit()
```

### Step 15: Call pi.load_from_db()

```python
pi.load_from_db()
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice'\n\t\t\tand reference_name=%s and debit_in_account_currency=300", pi.name))
```

### Step 17: Call pi.cancel()

```python
pi.cancel()
```

### Step 18: Call self.assertFalse()

```python
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice' and reference_name=%s", pi.name))
```


## Complete Example

```python
# Workflow
jv = frappe.copy_doc(self.globalTestRecords['Journal Entry'][1])
jv.insert()
jv.submit()
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
pi.disable_rounded_total = 1
pi.allocate_advances_automatically = 0
pi.append('advances', {'reference_type': 'Journal Entry', 'reference_name': jv.name, 'reference_row': jv.get('accounts')[0].name, 'advance_amount': 400, 'allocated_amount': 300, 'remarks': jv.remark})
pi.insert()
self.assertEqual(pi.outstanding_amount, 1212.3)
pi.disable_rounded_total = 0
pi.get('payment_schedule')[0].payment_amount = 1512.0
pi.save()
self.assertEqual(pi.outstanding_amount, 1212.0)
pi.submit()
pi.load_from_db()
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice'\n\t\t\tand reference_name=%s and debit_in_account_currency=300", pi.name))
pi.cancel()
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice' and reference_name=%s", pi.name))
```

## Next Steps


---

*Source: test_purchase_invoice.py:515 | Complexity: Advanced | Last updated: 2026-02-03*