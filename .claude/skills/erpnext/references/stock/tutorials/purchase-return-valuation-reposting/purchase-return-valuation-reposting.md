# How To: Purchase Return Valuation Reposting

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test purchase return valuation reposting

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `time`
- `uuid`
- `frappe`
- `frappe.core.page.permission_manager.permission_manager`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.query_builder.functions`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.gl_entry.gl_entry`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.landed_cost_voucher.test_landed_cost_voucher`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.stock_reconciliation.test_stock_reconciliation`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.tests.test_utils`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.repost_item_valuation.repost_item_valuation`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.item.test_item`

**Setup Required:**
```python
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
```

## Step-by-Step Guide

### Step 1: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-10', warehouse='Stores - _TC', item_code='_Test Item for Reposting', qty=5, rate=100)
```

### Step 2: Assign return_pr = make_purchase_receipt(...)

```python
return_pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-15', warehouse='Stores - _TC', item_code='_Test Item for Reposting', is_return=1, return_against=pr.name, qty=-2)
```

### Step 3: Assign unknown = frappe.db.get_value(...)

```python
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(outgoing_rate, 100)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(stock_value_difference, -200)
```

### Step 6: Call create_landed_cost_voucher()

```python
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
```

### Step 7: Assign unknown = frappe.db.get_value(...)

```python
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(outgoing_rate, 110)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(stock_value_difference, -220)
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-10', warehouse='Stores - _TC', item_code='_Test Item for Reposting', qty=5, rate=100)
return_pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-15', warehouse='Stores - _TC', item_code='_Test Item for Reposting', is_return=1, return_against=pr.name, qty=-2)
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
self.assertEqual(outgoing_rate, 100)
self.assertEqual(stock_value_difference, -200)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
self.assertEqual(outgoing_rate, 110)
self.assertEqual(stock_value_difference, -220)
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:172 | Complexity: Advanced | Last updated: 2026-02-04*