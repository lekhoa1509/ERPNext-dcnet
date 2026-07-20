# How To: Unlinking Warehouse From Item Defaults

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test unlinking warehouse from item defaults

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext`
- `erpnext.accounts.doctype.account.test_account`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.warehouse.warehouse`


## Step-by-Step Guide

### Step 1: Assign company = '_Test Company'

```python
company = '_Test Company'
```

### Step 2: Assign warehouse_names = value

```python
warehouse_names = [f'_Test Warehouse {i} for Unlinking' for i in range(2)]
```

### Step 3: Assign warehouse_ids = value

```python
warehouse_ids = []
```

### Step 4: Assign item_names = value

```python
item_names = [f'_Test Item {i} for Unlinking' for i in range(2)]
```

### Step 5: Assign warehouse_id = create_warehouse(...)

```python
warehouse_id = create_warehouse(warehouse, company=company)
```

### Step 6: Call warehouse_ids.append()

```python
warehouse_ids.append(warehouse_id)
```

### Step 7: Call create_item()

```python
create_item(item, warehouse=warehouse, company=company)
```

### Step 8: Call frappe.delete_doc()

```python
frappe.delete_doc('Warehouse', warehouse)
```

### Step 9: Call self.assertTrue()

```python
self.assertTrue(bool(frappe.db.exists('Item', item)), f"{item} doesn't exist")
```

### Step 10: Assign item_doc = frappe.get_doc(...)

```python
item_doc = frappe.get_doc('Item', item)
```

### Step 11: Call self.assertNotIn()

```python
self.assertNotIn(item_default.default_warehouse, warehouse_ids, f'{item} linked to {item_default.default_warehouse} in {warehouse_ids}.')
```


## Complete Example

```python
# Workflow
company = '_Test Company'
warehouse_names = [f'_Test Warehouse {i} for Unlinking' for i in range(2)]
warehouse_ids = []
for warehouse in warehouse_names:
    warehouse_id = create_warehouse(warehouse, company=company)
    warehouse_ids.append(warehouse_id)
item_names = [f'_Test Item {i} for Unlinking' for i in range(2)]
for item, warehouse in zip(item_names, warehouse_ids, strict=False):
    create_item(item, warehouse=warehouse, company=company)
for warehouse in warehouse_ids:
    frappe.delete_doc('Warehouse', warehouse)
for item in item_names:
    self.assertTrue(bool(frappe.db.exists('Item', item)), f"{item} doesn't exist")
    item_doc = frappe.get_doc('Item', item)
    for item_default in item_doc.item_defaults:
        self.assertNotIn(item_default.default_warehouse, warehouse_ids, f'{item} linked to {item_default.default_warehouse} in {warehouse_ids}.')
```

## Next Steps


---

*Source: test_warehouse.py:43 | Complexity: Advanced | Last updated: 2026-02-04*