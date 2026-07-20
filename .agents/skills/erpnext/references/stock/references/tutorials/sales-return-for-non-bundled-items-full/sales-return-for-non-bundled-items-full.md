# How To: Sales Return For Non Bundled Items Full

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales return for non bundled items full

## Prerequisites

**Required Modules:**
- `json`
- `collections`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.accounts.utils`
- `erpnext.controllers.accounts_controller`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_trip.test_delivery_trip`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.stock_ledger`
- `frappe.model.naming`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.accounts.doctype.cost_center.test_cost_center`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.stock_balance`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign company = frappe.db.get_value(...)

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
```

### Step 2: Call make_item()

```python
make_item('Box', {'is_stock_item': 1})
```

### Step 3: Call make_stock_entry()

```python
make_stock_entry(item_code='Box', target='Stores - TCP1', qty=10, basic_rate=100)
```

### Step 4: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code='Box', qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
```

### Step 5: Assign dn1 = create_delivery_note(...)

```python
dn1 = create_delivery_note(item_code='Box', is_return=1, return_against=dn.name, qty=-5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1', do_not_submit=1)
```

### Step 6: Assign unknown.dn_detail = value

```python
dn1.items[0].dn_detail = dn.items[0].name
```

### Step 7: Call dn1.submit()

```python
dn1.submit()
```

### Step 8: Assign returned = frappe.get_doc(...)

```python
returned = frappe.get_doc('Delivery Note', dn1.name)
```

### Step 9: Call returned.update_prevdoc_status()

```python
returned.update_prevdoc_status()
```

### Step 10: Call dn.load_from_db()

```python
dn.load_from_db()
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(dn.items[0].returned_qty, 5)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(dn.per_returned, 100)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dn.status, 'Return Issued')
```


## Complete Example

```python
# Workflow
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_item('Box', {'is_stock_item': 1})
make_stock_entry(item_code='Box', target='Stores - TCP1', qty=10, basic_rate=100)
dn = create_delivery_note(item_code='Box', qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
dn1 = create_delivery_note(item_code='Box', is_return=1, return_against=dn.name, qty=-5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1', do_not_submit=1)
dn1.items[0].dn_detail = dn.items[0].name
dn1.submit()
returned = frappe.get_doc('Delivery Note', dn1.name)
returned.update_prevdoc_status()
dn.load_from_db()
self.assertEqual(dn.items[0].returned_qty, 5)
self.assertEqual(dn.per_returned, 100)
self.assertEqual(dn.status, 'Return Issued')
```

## Next Steps


---

*Source: test_delivery_note.py:392 | Complexity: Advanced | Last updated: 2026-02-04*