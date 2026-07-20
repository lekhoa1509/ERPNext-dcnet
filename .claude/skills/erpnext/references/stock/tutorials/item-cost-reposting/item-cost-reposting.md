# How To: Item Cost Reposting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item cost reposting

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

### Step 1: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 2: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=100, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-10', posting_time='14:00')
```

### Step 3: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Finished Goods - _TC', qty=10, rate=200, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-20', posting_time='14:00')
```

### Step 4: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(item_code='_Test Item for Reposting', source='Stores - _TC', target='Finished Goods - _TC', company=company, qty=10, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-30', posting_time='14:00')
```

### Step 5: Assign target_wh_sle = frappe.db.get_value(...)

```python
target_wh_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': se.name}, ['valuation_rate'], as_dict=1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(target_wh_sle.get('valuation_rate'), 150)
```

### Step 7: Assign repack = create_repack_entry(...)

```python
repack = create_repack_entry(company=company, posting_date='2020-05-05', posting_time='14:00')
```

### Step 8: Assign finished_item_sle = frappe.db.get_value(...)

```python
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(finished_item_sle.get('incoming_rate'), 540)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(finished_item_sle.get('valuation_rate'), 540)
```

### Step 11: Call create_stock_reconciliation()

```python
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=150, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-12', posting_time='14:00')
```

### Step 12: Assign target_wh_sle = get_previous_sle(...)

```python
target_wh_sle = get_previous_sle({'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'posting_date': '2020-04-30', 'posting_time': '14:00'})
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(target_wh_sle.get('incoming_rate'), 150)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(target_wh_sle.get('valuation_rate'), 175)
```

### Step 15: Assign finished_item_sle = frappe.db.get_value(...)

```python
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(finished_item_sle.get('incoming_rate'), 790)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(finished_item_sle.get('valuation_rate'), 790)
```

### Step 18: Call repack.reload()

```python
repack.reload()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(repack.items[0].get('basic_rate'), 150)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(repack.items[1].get('basic_rate'), 750)
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
company = '_Test Company'
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=100, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-10', posting_time='14:00')
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Finished Goods - _TC', qty=10, rate=200, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-20', posting_time='14:00')
se = make_stock_entry(item_code='_Test Item for Reposting', source='Stores - _TC', target='Finished Goods - _TC', company=company, qty=10, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-30', posting_time='14:00')
target_wh_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': se.name}, ['valuation_rate'], as_dict=1)
self.assertEqual(target_wh_sle.get('valuation_rate'), 150)
repack = create_repack_entry(company=company, posting_date='2020-05-05', posting_time='14:00')
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
self.assertEqual(finished_item_sle.get('incoming_rate'), 540)
self.assertEqual(finished_item_sle.get('valuation_rate'), 540)
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=150, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-12', posting_time='14:00')
target_wh_sle = get_previous_sle({'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'posting_date': '2020-04-30', 'posting_time': '14:00'})
self.assertEqual(target_wh_sle.get('incoming_rate'), 150)
self.assertEqual(target_wh_sle.get('valuation_rate'), 175)
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
self.assertEqual(finished_item_sle.get('incoming_rate'), 790)
self.assertEqual(finished_item_sle.get('valuation_rate'), 790)
repack.reload()
self.assertEqual(repack.items[0].get('basic_rate'), 150)
self.assertEqual(repack.items[1].get('basic_rate'), 750)
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:51 | Complexity: Advanced | Last updated: 2026-02-04*