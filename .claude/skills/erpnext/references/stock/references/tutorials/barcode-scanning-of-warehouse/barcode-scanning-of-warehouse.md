# How To: Barcode Scanning Of Warehouse

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test barcode scanning of warehouse

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign warehouse = frappe.get_doc.insert(...)

```python
warehouse = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode', 'company': '_Test Company'}).insert()
```

### Step 2: Assign warehouse_2 = frappe.get_doc.insert(...)

```python
warehouse_2 = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode 2', 'company': '_Test Company'}).insert()
```

### Step 3: Assign warehouse_scan = scan_barcode(...)

```python
warehouse_scan = scan_barcode(warehouse.name)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(warehouse_scan['warehouse'], warehouse.name)
```

### Step 5: Assign item_with_warehouse = self.make_item(...)

```python
item_with_warehouse = self.make_item(properties={'item_defaults': [{'company': '_Test Company', 'default_warehouse': warehouse.name}], 'barcodes': [{'barcode': 'w12345'}]})
```

### Step 6: Assign item_scan = scan_barcode(...)

```python
item_scan = scan_barcode('w12345')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(item_scan['item_code'], item_with_warehouse.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(item_scan.get('default_warehouse'), None)
```

### Step 9: Assign ctx = value

```python
ctx = {'company': '_Test Company'}
```

### Step 10: Assign item_scan_with_ctx = scan_barcode(...)

```python
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse.name)
```

### Step 13: Assign ctx = value

```python
ctx = {'company': '_Test Company', 'set_warehouse': warehouse_2.name}
```

### Step 14: Assign item_scan_with_ctx = scan_barcode(...)

```python
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)
```


## Complete Example

```python
# Workflow
warehouse = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode', 'company': '_Test Company'}).insert()
warehouse_2 = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode 2', 'company': '_Test Company'}).insert()
warehouse_scan = scan_barcode(warehouse.name)
self.assertEqual(warehouse_scan['warehouse'], warehouse.name)
item_with_warehouse = self.make_item(properties={'item_defaults': [{'company': '_Test Company', 'default_warehouse': warehouse.name}], 'barcodes': [{'barcode': 'w12345'}]})
item_scan = scan_barcode('w12345')
self.assertEqual(item_scan['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan.get('default_warehouse'), None)
ctx = {'company': '_Test Company'}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse.name)
ctx = {'company': '_Test Company', 'set_warehouse': warehouse_2.name}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)
```

## Next Steps


---

*Source: test_utils.py:98 | Complexity: Advanced | Last updated: 2026-02-04*