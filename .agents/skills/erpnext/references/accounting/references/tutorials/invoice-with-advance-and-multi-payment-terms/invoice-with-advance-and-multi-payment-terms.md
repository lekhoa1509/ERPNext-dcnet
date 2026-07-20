# How To: Invoice With Advance And Multi Payment Terms

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test invoice with advance and multi payment terms

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

### Step 9: Call pi.update()

```python
pi.update({'payment_schedule': get_payment_terms('_Test Payment Term Template', pi.posting_date, pi.grand_total, pi.base_grand_total)})
```

### Step 10: Call pi.save()

```python
pi.save()
```

### Step 11: Call pi.submit()

```python
pi.submit()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[0].payment_amount, 606.15)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[0].due_date, pi.posting_date)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[1].payment_amount, 606.15)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[1].due_date, add_days(pi.posting_date, 30))
```

### Step 16: Call pi.load_from_db()

```python
pi.load_from_db()
```

### Step 17: Call self.assertTrue()

```python
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s and debit_in_account_currency=300", pi.name))
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pi.outstanding_amount, 1212.3)
```

### Step 19: Call pi.cancel()

```python
pi.cancel()
```

### Step 20: Call self.assertFalse()

```python
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s", pi.name))
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
pi.update({'payment_schedule': get_payment_terms('_Test Payment Term Template', pi.posting_date, pi.grand_total, pi.base_grand_total)})
pi.save()
pi.submit()
self.assertEqual(pi.payment_schedule[0].payment_amount, 606.15)
self.assertEqual(pi.payment_schedule[0].due_date, pi.posting_date)
self.assertEqual(pi.payment_schedule[1].payment_amount, 606.15)
self.assertEqual(pi.payment_schedule[1].due_date, add_days(pi.posting_date, 30))
pi.load_from_db()
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s and debit_in_account_currency=300", pi.name))
self.assertEqual(pi.outstanding_amount, 1212.3)
pi.cancel()
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s", pi.name))
```

## Next Steps


---

*Source: test_purchase_invoice.py:568 | Complexity: Advanced | Last updated: 2026-02-03*