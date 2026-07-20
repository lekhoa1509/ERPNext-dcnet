# How To: Barcode Scanning

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test barcode scanning

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.query_builder.functions`
- `frappe.tests`
- `erpnext.stock.utils`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign simple_item = self.make_item(...)

```python
simple_item = self.make_item(properties={'barcodes': [{'barcode': '12399'}]})
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(scan_barcode('12399')['item_code'], simple_item.name)
```

### Step 3: Assign batch_item = self.make_item(...)

```python
batch_item = self.make_item(properties={'has_batch_no': 1, 'create_new_batch': 1})
```

### Step 4: Assign batch = frappe.get_doc.insert(...)

```python
batch = frappe.get_doc(doctype='Batch', item=batch_item.name).insert()
```

### Step 5: Assign batch_scan = scan_barcode(...)

```python
batch_scan = scan_barcode(batch.name)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(batch_scan['item_code'], batch_item.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(batch_scan['batch_no'], batch.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(batch_scan['has_batch_no'], 1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(batch_scan['has_serial_no'], 0)
```

### Step 10: Assign serial_item = self.make_item(...)

```python
serial_item = self.make_item(properties={'has_serial_no': 1})
```

### Step 11: Assign serial = frappe.get_doc.insert(...)

```python
serial = frappe.get_doc(doctype='Serial No', item_code=serial_item.name, serial_no=frappe.generate_hash()).insert()
```

### Step 12: Assign serial_scan = scan_barcode(...)

```python
serial_scan = scan_barcode(serial.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(serial_scan['item_code'], serial_item.name)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(serial_scan['serial_no'], serial.name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(serial_scan['has_batch_no'], 0)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(serial_scan['has_serial_no'], 1)
```


## Complete Example

```python
# Workflow
simple_item = self.make_item(properties={'barcodes': [{'barcode': '12399'}]})
self.assertEqual(scan_barcode('12399')['item_code'], simple_item.name)
batch_item = self.make_item(properties={'has_batch_no': 1, 'create_new_batch': 1})
batch = frappe.get_doc(doctype='Batch', item=batch_item.name).insert()
batch_scan = scan_barcode(batch.name)
self.assertEqual(batch_scan['item_code'], batch_item.name)
self.assertEqual(batch_scan['batch_no'], batch.name)
self.assertEqual(batch_scan['has_batch_no'], 1)
self.assertEqual(batch_scan['has_serial_no'], 0)
serial_item = self.make_item(properties={'has_serial_no': 1})
serial = frappe.get_doc(doctype='Serial No', item_code=serial_item.name, serial_no=frappe.generate_hash()).insert()
serial_scan = scan_barcode(serial.name)
self.assertEqual(serial_scan['item_code'], serial_item.name)
self.assertEqual(serial_scan['serial_no'], serial.name)
self.assertEqual(serial_scan['has_batch_no'], 0)
self.assertEqual(serial_scan['has_serial_no'], 1)
```

## Next Steps


---

*Source: test_utils.py:74 | Complexity: Advanced | Last updated: 2026-02-04*