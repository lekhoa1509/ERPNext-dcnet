# How To: Purchase Return For Rejected Qty

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase return for rejected qty

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

### Step 1: Assign rejected_warehouse = '_Test Rejected Warehouse - TCP1'

```python
rejected_warehouse = '_Test Rejected Warehouse - TCP1'
```

### Step 2: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', qty=2, rejected_qty=2, rejected_warehouse=rejected_warehouse)
```

### Step 3: Assign return_pr = make_purchase_receipt(...)

```python
return_pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', is_return=1, return_against=pr.name, qty=-2, rejected_qty=-2, rejected_warehouse=rejected_warehouse)
```

### Step 4: Assign actual_qty = frappe.db.get_value(...)

```python
actual_qty = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name, 'warehouse': return_pr.items[0].rejected_warehouse}, 'actual_qty')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(actual_qty, -2)
```

### Step 6: Call return_pr.cancel()

```python
return_pr.cancel()
```

### Step 7: Call pr.cancel()

```python
pr.cancel()
```

### Step 8: get_warehouse(company='_Test Company with perpetual inventory', abbr=' - TCP1', warehouse_name='_Test Rejected Warehouse').name

```python
get_warehouse(company='_Test Company with perpetual inventory', abbr=' - TCP1', warehouse_name='_Test Rejected Warehouse').name
```


## Complete Example

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

# Workflow
from erpnext.stock.doctype.warehouse.test_warehouse import get_warehouse
rejected_warehouse = '_Test Rejected Warehouse - TCP1'
if not frappe.db.exists('Warehouse', rejected_warehouse):
    get_warehouse(company='_Test Company with perpetual inventory', abbr=' - TCP1', warehouse_name='_Test Rejected Warehouse').name
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', qty=2, rejected_qty=2, rejected_warehouse=rejected_warehouse)
return_pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', is_return=1, return_against=pr.name, qty=-2, rejected_qty=-2, rejected_warehouse=rejected_warehouse)
actual_qty = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name, 'warehouse': return_pr.items[0].rejected_warehouse}, 'actual_qty')
self.assertEqual(actual_qty, -2)
return_pr.cancel()
pr.cancel()
```

## Next Steps


---

*Source: test_purchase_receipt.py:526 | Complexity: Advanced | Last updated: 2026-02-04*