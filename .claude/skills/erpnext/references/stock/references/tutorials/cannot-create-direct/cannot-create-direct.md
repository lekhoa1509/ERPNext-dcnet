# How To: Cannot Create Direct

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test cannot create direct

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.serial_no.serial_no`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.doctype.serial_and_batch_bundle.serial_and_batch_bundle`


## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Serial No', '_TCSER0001')
```

### Step 2: Assign sr = frappe.new_doc(...)

```python
sr = frappe.new_doc('Serial No')
```

### Step 3: Assign sr.item_code = '_Test Serialized Item'

```python
sr.item_code = '_Test Serialized Item'
```

### Step 4: Assign sr.warehouse = '_Test Warehouse - _TC'

```python
sr.warehouse = '_Test Warehouse - _TC'
```

### Step 5: Assign sr.serial_no = '_TCSER0001'

```python
sr.serial_no = '_TCSER0001'
```

### Step 6: Assign sr.purchase_rate = 10

```python
sr.purchase_rate = 10
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(SerialNoCannotCreateDirectError, sr.insert)
```

### Step 8: Assign sr.warehouse = None

```python
sr.warehouse = None
```

### Step 9: Call sr.insert()

```python
sr.insert()
```

### Step 10: Call self.assertTrue()

```python
self.assertTrue(sr.name)
```

### Step 11: Assign sr.warehouse = '_Test Warehouse - _TC'

```python
sr.warehouse = '_Test Warehouse - _TC'
```

### Step 12: Call self.assertTrue()

```python
self.assertTrue(SerialNoCannotCannotChangeError, sr.save)
```


## Complete Example

```python
# Workflow
frappe.delete_doc_if_exists('Serial No', '_TCSER0001')
sr = frappe.new_doc('Serial No')
sr.item_code = '_Test Serialized Item'
sr.warehouse = '_Test Warehouse - _TC'
sr.serial_no = '_TCSER0001'
sr.purchase_rate = 10
self.assertRaises(SerialNoCannotCreateDirectError, sr.insert)
sr.warehouse = None
sr.insert()
self.assertTrue(sr.name)
sr.warehouse = '_Test Warehouse - _TC'
self.assertTrue(SerialNoCannotCannotChangeError, sr.save)
```

## Next Steps


---

*Source: test_serial_no.py:31 | Complexity: Advanced | Last updated: 2026-02-04*