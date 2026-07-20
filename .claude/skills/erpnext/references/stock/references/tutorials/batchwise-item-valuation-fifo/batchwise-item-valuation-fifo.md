# How To: Batchwise Item Valuation Fifo

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test batchwise item valuation fifo

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

### Step 1: Assign unknown = setup_item_valuation_test(...)

```python
item, warehouses, batches = setup_item_valuation_test(valuation_method='FIFO')
```

### Step 2: Assign pr_entry_list = value

```python
pr_entry_list = [(item, warehouses[0], batches[0], 1, 100), (item, warehouses[0], batches[1], 1, 50), (item, warehouses[0], batches[0], 1, 150), (item, warehouses[0], batches[1], 1, 100)]
```

### Step 3: Assign prs = create_purchase_receipt_entries_for_batchwise_item_valuation_test(...)

```python
prs = create_purchase_receipt_entries_for_batchwise_item_valuation_test(pr_entry_list)
```

### Step 4: Assign sle_details = fetch_sle_details_for_doc_list(...)

```python
sle_details = fetch_sle_details_for_doc_list(prs, ['stock_value'])
```

### Step 5: Assign sv_list = value

```python
sv_list = [d['stock_value'] for d in sle_details]
```

### Step 6: Assign expected_sv = value

```python
expected_sv = [100, 150, 300, 400]
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(expected_sv, sv_list, "Incorrect 'Stock Value' values")
```

### Step 8: Assign dn_entry_list = value

```python
dn_entry_list = [(item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200), (item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200)]
```

### Step 9: Assign frappe.flags.use_serial_and_batch_fields = True

```python
frappe.flags.use_serial_and_batch_fields = True
```

### Step 10: Assign dns = create_delivery_note_entries_for_batchwise_item_valuation_test(...)

```python
dns = create_delivery_note_entries_for_batchwise_item_valuation_test(dn_entry_list)
```

### Step 11: Assign sle_details = fetch_sle_details_for_doc_list(...)

```python
sle_details = fetch_sle_details_for_doc_list(dns, ['stock_value_difference'])
```

### Step 12: Assign svd_list = value

```python
svd_list = [-1 * d['stock_value_difference'] for d in sle_details]
```

### Step 13: Assign expected_incoming_rates, expected_abs_svd = value

```python
expected_incoming_rates = expected_abs_svd = [75.0, 125.0, 75.0, 125.0]
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")
```

### Step 15: Assign frappe.flags.use_serial_and_batch_fields = False

```python
frappe.flags.use_serial_and_batch_fields = False
```

### Step 16: Call self.assertTrue()

```python
self.assertTrue(dn.items[0].incoming_rate in expected_abs_svd, "Incorrect 'Incoming Rate' values fetched for DN items")
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
item, warehouses, batches = setup_item_valuation_test(valuation_method='FIFO')
pr_entry_list = [(item, warehouses[0], batches[0], 1, 100), (item, warehouses[0], batches[1], 1, 50), (item, warehouses[0], batches[0], 1, 150), (item, warehouses[0], batches[1], 1, 100)]
prs = create_purchase_receipt_entries_for_batchwise_item_valuation_test(pr_entry_list)
sle_details = fetch_sle_details_for_doc_list(prs, ['stock_value'])
sv_list = [d['stock_value'] for d in sle_details]
expected_sv = [100, 150, 300, 400]
self.assertEqual(expected_sv, sv_list, "Incorrect 'Stock Value' values")
dn_entry_list = [(item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200), (item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200)]
frappe.flags.use_serial_and_batch_fields = True
dns = create_delivery_note_entries_for_batchwise_item_valuation_test(dn_entry_list)
sle_details = fetch_sle_details_for_doc_list(dns, ['stock_value_difference'])
svd_list = [-1 * d['stock_value_difference'] for d in sle_details]
expected_incoming_rates = expected_abs_svd = [75.0, 125.0, 75.0, 125.0]
self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")
for dn, _incoming_rate in zip(dns, expected_incoming_rates, strict=False):
    self.assertTrue(dn.items[0].incoming_rate in expected_abs_svd, "Incorrect 'Incoming Rate' values fetched for DN items")
frappe.flags.use_serial_and_batch_fields = False
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:458 | Complexity: Advanced | Last updated: 2026-02-04*