# How To: Available Serial No

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test available serial no

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`


## Step-by-Step Guide

### Step 1: Assign report = frappe.get_doc(...)

```python
report = frappe.get_doc('Report', 'Available Serial No')
```

### Step 2: Call make_purchase_receipt()

```python
make_purchase_receipt(qty=10, item_code='_Test Item with Serial No')
```

### Step 3: Assign data = report.get_data(...)

```python
data = report.get_data(filters=self.filters)
```

### Step 4: Assign serial_nos = value

```python
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(serial_nos), 10)
```

### Step 6: Call create_delivery_note()

```python
create_delivery_note(qty=5, item_code='_Test Item with Serial No')
```

### Step 7: Assign data = report.get_data(...)

```python
data = report.get_data(filters=self.filters)
```

### Step 8: Assign serial_nos = value

```python
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(serial_nos), 5)
```


## Complete Example

```python
# Workflow
report = frappe.get_doc('Report', 'Available Serial No')
make_purchase_receipt(qty=10, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 10)
create_delivery_note(qty=5, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 5)
```

## Next Steps


---

*Source: test_available_serial_no.py:30 | Complexity: Advanced | Last updated: 2026-02-04*