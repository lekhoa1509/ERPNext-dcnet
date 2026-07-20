# How To: Naming

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test naming

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

### Step 1: Assign company = 'Wind Power LLC'

```python
company = 'Wind Power LLC'
```

### Step 2: Assign warehouse_name = 'Named Warehouse - WP'

```python
warehouse_name = 'Named Warehouse - WP'
```

### Step 3: Assign wh = frappe.get_doc.insert(...)

```python
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(wh.name, warehouse_name)
```

### Step 5: Assign warehouse_name = 'Unnamed Warehouse'

```python
warehouse_name = 'Unnamed Warehouse'
```

### Step 6: Assign wh = frappe.get_doc.insert(...)

```python
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
```

### Step 7: Call self.assertIn()

```python
self.assertIn(warehouse_name, wh.name)
```


## Complete Example

```python
# Workflow
company = 'Wind Power LLC'
warehouse_name = 'Named Warehouse - WP'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertEqual(wh.name, warehouse_name)
warehouse_name = 'Unnamed Warehouse'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertIn(warehouse_name, wh.name)
```

## Next Steps


---

*Source: test_warehouse.py:33 | Complexity: Intermediate | Last updated: 2026-02-04*