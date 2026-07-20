# How To: Make Purchase Invoice

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make purchase invoice

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `pypika`
- `erpnext`
- `erpnext.controllers`
- `erpnext.controllers.status_updater`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.controllers.accounts_controller`
- `erpnext.controllers.buying_controller`
- `erpnext.stock`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.get_item_details`
- `erpnext.stock.utils`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.buying.doctype.purchase_order`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.party`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.get_item_details`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.buying.doctype.supplier.test_supplier`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.accounts.doctype.purchase_invoice.purchase_invoice`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.report.stock_balance.stock_balance`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.stock_ledger`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.purchase_order`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.purchase_receipt.purchase_receipt`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.stock_ledger`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`

**Setup Required:**
```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
```

## Step-by-Step Guide

### Step 1: Call create_payment_term()

```python
create_payment_term('_Test Payment Term 1 for Purchase Invoice')
```

### Step 2: Call create_payment_term()

```python
create_payment_term('_Test Payment Term 2 for Purchase Invoice')
```

### Step 3: Assign template = frappe.db.get_value(...)

```python
template = frappe.db.get_value('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice')
```

### Step 4: Assign old_template_in_supplier = frappe.db.get_value(...)

```python
old_template_in_supplier = frappe.db.get_value('Supplier', '_Test Supplier', 'payment_terms')
```

### Step 5: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', template)
```

### Step 6: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(do_not_save=True)
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_purchase_invoice, pr.name)
```

### Step 8: Call pr.submit()

```python
pr.submit()
```

### Step 9: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(pr.name)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pi.doctype, 'Purchase Invoice')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(pi.get('items')), len(pr.get('items')))
```

### Step 12: Assign unknown.rate = 200

```python
pi.get('items')[0].rate = 200
```

### Step 13: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, frappe.get_doc(pi).submit)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pi.payment_terms_template, template)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[0].payment_amount, flt(pi.grand_total) / 2)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[0].invoice_portion, 50)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[1].payment_amount, flt(pi.grand_total) / 2)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pi.payment_schedule[1].invoice_portion, 50)
```

### Step 19: Call pi.delete()

```python
pi.delete()
```

### Step 20: Call pr.cancel()

```python
pr.cancel()
```

### Step 21: Call frappe.db.set_value()

```python
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', old_template_in_supplier)
```

### Step 22: Call frappe.get_doc.delete()

```python
frappe.get_doc('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice').delete()
```

### Step 23: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Purchase Invoice', 'allocate_payment_based_on_payment_terms': 1, 'terms': [{'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 1 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 0}, {'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 2 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]}).insert()
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

# Workflow
from erpnext.accounts.doctype.payment_entry.test_payment_entry import create_payment_term
create_payment_term('_Test Payment Term 1 for Purchase Invoice')
create_payment_term('_Test Payment Term 2 for Purchase Invoice')
if not frappe.db.exists('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice'):
    frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Purchase Invoice', 'allocate_payment_based_on_payment_terms': 1, 'terms': [{'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 1 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 0}, {'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 2 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]}).insert()
template = frappe.db.get_value('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice')
old_template_in_supplier = frappe.db.get_value('Supplier', '_Test Supplier', 'payment_terms')
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', template)
pr = make_purchase_receipt(do_not_save=True)
self.assertRaises(frappe.ValidationError, make_purchase_invoice, pr.name)
pr.submit()
pi = make_purchase_invoice(pr.name)
self.assertEqual(pi.doctype, 'Purchase Invoice')
self.assertEqual(len(pi.get('items')), len(pr.get('items')))
pi.get('items')[0].rate = 200
self.assertRaises(frappe.ValidationError, frappe.get_doc(pi).submit)
self.assertEqual(pi.payment_terms_template, template)
self.assertEqual(pi.payment_schedule[0].payment_amount, flt(pi.grand_total) / 2)
self.assertEqual(pi.payment_schedule[0].invoice_portion, 50)
self.assertEqual(pi.payment_schedule[1].payment_amount, flt(pi.grand_total) / 2)
self.assertEqual(pi.payment_schedule[1].invoice_portion, 50)
pi.delete()
pr.cancel()
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', old_template_in_supplier)
frappe.get_doc('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice').delete()
```

## Next Steps


---

*Source: test_purchase_receipt.py:93 | Complexity: Advanced | Last updated: 2026-02-04*