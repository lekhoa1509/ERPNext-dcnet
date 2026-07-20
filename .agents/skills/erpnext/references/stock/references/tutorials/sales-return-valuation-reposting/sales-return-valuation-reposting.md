# How To: Sales Return Valuation Reposting

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test sales return valuation reposting

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

### Step 2: Assign item_code = '_Test Item for Reposting'

```python
item_code = '_Test Item for Reposting'
```

### Step 3: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(company=company, posting_date='2020-04-10', warehouse='Stores - _TC', item_code=item_code, qty=5, rate=100)
```

### Step 4: Assign dn = create_delivery_note(...)

```python
dn = create_delivery_note(item_code=item_code, qty=5, rate=150, warehouse='Stores - _TC', company=company, expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
```

### Step 5: Assign outgoing_rate = abs(...)

```python
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(dn.items[0].incoming_rate, 100)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(outgoing_rate, 100)
```

### Step 8: Assign return_dn = create_delivery_note(...)

```python
return_dn = create_delivery_note(is_return=1, return_against=dn.name, item_code=item_code, qty=-2, rate=150, company=company, warehouse='Stores - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
```

### Step 9: Assign unknown = frappe.db.get_value(...)

```python
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(return_dn.items[0].incoming_rate, 100)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(incoming_rate, 100)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(stock_value_difference, 200)
```

### Step 13: Assign lcv = create_landed_cost_voucher(...)

```python
lcv = create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
```

### Step 14: Assign outgoing_rate = abs(...)

```python
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(outgoing_rate, 110)
```

### Step 16: Call dn.reload()

```python
dn.reload()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(dn.items[0].incoming_rate, 110)
```

### Step 18: Assign unknown = frappe.db.get_value(...)

```python
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(incoming_rate, 110)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(stock_value_difference, 220)
```

### Step 21: Call return_dn.reload()

```python
return_dn.reload()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(return_dn.items[0].incoming_rate, 110)
```

### Step 23: Call return_dn.cancel()

```python
return_dn.cancel()
```

### Step 24: Call dn.cancel()

```python
dn.cancel()
```

### Step 25: Call lcv.cancel()

```python
lcv.cancel()
```

### Step 26: Call pr.cancel()

```python
pr.cancel()
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
item_code = '_Test Item for Reposting'
pr = make_purchase_receipt(company=company, posting_date='2020-04-10', warehouse='Stores - _TC', item_code=item_code, qty=5, rate=100)
dn = create_delivery_note(item_code=item_code, qty=5, rate=150, warehouse='Stores - _TC', company=company, expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
self.assertEqual(dn.items[0].incoming_rate, 100)
self.assertEqual(outgoing_rate, 100)
return_dn = create_delivery_note(is_return=1, return_against=dn.name, item_code=item_code, qty=-2, rate=150, company=company, warehouse='Stores - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(return_dn.items[0].incoming_rate, 100)
self.assertEqual(incoming_rate, 100)
self.assertEqual(stock_value_difference, 200)
lcv = create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
self.assertEqual(outgoing_rate, 110)
dn.reload()
self.assertEqual(dn.items[0].incoming_rate, 110)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(incoming_rate, 110)
self.assertEqual(stock_value_difference, 220)
return_dn.reload()
self.assertEqual(return_dn.items[0].incoming_rate, 110)
return_dn.cancel()
dn.cancel()
lcv.cancel()
pr.cancel()
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:213 | Complexity: Advanced | Last updated: 2026-02-04*