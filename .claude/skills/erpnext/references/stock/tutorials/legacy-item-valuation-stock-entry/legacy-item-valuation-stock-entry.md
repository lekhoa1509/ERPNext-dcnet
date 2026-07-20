# How To: Legacy Item Valuation Stock Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test legacy item valuation stock entry

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

### Step 1: Assign columns = value

```python
columns = ['stock_value_difference', 'stock_value', 'actual_qty', 'qty_after_transaction', 'stock_queue']
```

### Step 2: Assign unknown = setup_item_valuation_test(...)

```python
item, warehouses, batches = setup_item_valuation_test()
```

### Step 3: Assign details_list = value

```python
details_list = []
```

### Step 4: Assign se_entry_list_mr = value

```python
se_entry_list_mr = [(item, None, warehouses[0], batches[0], 1, 50, '2021-01-21'), (item, None, warehouses[0], batches[1], 1, 100, '2021-01-23')]
```

### Step 5: Assign ses = create_stock_entry_entries_for_batchwise_item_valuation_test(...)

```python
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mr, 'Material Receipt')
```

### Step 6: Assign sle_details = fetch_sle_details_for_doc_list(...)

```python
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
```

### Step 7: Assign expected_sle_details = value

```python
expected_sle_details = [(50.0, 50.0, 1.0, 1.0, '[]'), (100.0, 150.0, 1.0, 2.0, '[]')]
```

### Step 8: Call details_list.append()

```python
details_list.append((sle_details, expected_sle_details, 'Material Receipt Entries', columns))
```

### Step 9: Assign se_entry_list_mi = value

```python
se_entry_list_mi = [(item, warehouses[0], None, batches[1], 1, None, '2021-01-29')]
```

### Step 10: Assign ses = create_stock_entry_entries_for_batchwise_item_valuation_test(...)

```python
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mi, 'Material Issue')
```

### Step 11: Assign sle_details = fetch_sle_details_for_doc_list(...)

```python
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
```

### Step 12: Assign expected_sle_details = value

```python
expected_sle_details = [(-100.0, 50.0, -1.0, 1.0, '[]')]
```

### Step 13: Call details_list.append()

```python
details_list.append((sle_details, expected_sle_details, 'Material Issue Entries', columns))
```

### Step 14: Call check_sle_details_against_expected()

```python
check_sle_details_against_expected(*details)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sle_val, ex_sle_val, f'Incorrect {col} value on transaction #: {i} in {detail}')
```

### Step 16: Assign sle_val = get_stock_value_from_q(...)

```python
sle_val = get_stock_value_from_q(sle_val)
```

### Step 17: Assign ex_sle_val = get_stock_value_from_q(...)

```python
ex_sle_val = get_stock_value_from_q(ex_sle_val)
```


## Complete Example

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

# Workflow
columns = ['stock_value_difference', 'stock_value', 'actual_qty', 'qty_after_transaction', 'stock_queue']
item, warehouses, batches = setup_item_valuation_test()

def check_sle_details_against_expected(sle_details, expected_sle_details, detail, columns):
    for i, (sle_vals, ex_sle_vals) in enumerate(zip(sle_details, expected_sle_details, strict=False)):
        for col, sle_val, ex_sle_val in zip(columns, sle_vals, ex_sle_vals, strict=False):
            if col == 'stock_queue':
                sle_val = get_stock_value_from_q(sle_val)
                ex_sle_val = get_stock_value_from_q(ex_sle_val)
            self.assertEqual(sle_val, ex_sle_val, f'Incorrect {col} value on transaction #: {i} in {detail}')
details_list = []
se_entry_list_mr = [(item, None, warehouses[0], batches[0], 1, 50, '2021-01-21'), (item, None, warehouses[0], batches[1], 1, 100, '2021-01-23')]
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mr, 'Material Receipt')
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
expected_sle_details = [(50.0, 50.0, 1.0, 1.0, '[]'), (100.0, 150.0, 1.0, 2.0, '[]')]
details_list.append((sle_details, expected_sle_details, 'Material Receipt Entries', columns))
se_entry_list_mi = [(item, warehouses[0], None, batches[1], 1, None, '2021-01-29')]
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mi, 'Material Issue')
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
expected_sle_details = [(-100.0, 50.0, -1.0, 1.0, '[]')]
details_list.append((sle_details, expected_sle_details, 'Material Issue Entries', columns))
for details in details_list:
    check_sle_details_against_expected(*details)
```

## Next Steps


---

*Source: test_stock_ledger_entry.py:748 | Complexity: Advanced | Last updated: 2026-02-04*