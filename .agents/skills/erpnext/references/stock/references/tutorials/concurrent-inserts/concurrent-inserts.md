# How To: Concurrent Inserts

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Ensure no duplicates are possible in case of concurrent inserts

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.utils`


## Step-by-Step Guide

### Step 1: 'Ensure no duplicates are possible in case of concurrent inserts'

```python
'Ensure no duplicates are possible in case of concurrent inserts'
```

### Step 2: Assign item_code = '_TestConcurrentBin'

```python
item_code = '_TestConcurrentBin'
```

### Step 3: Call make_item()

```python
make_item(item_code)
```

### Step 4: Assign warehouse = '_Test Warehouse - _TC'

```python
warehouse = '_Test Warehouse - _TC'
```

### Step 5: Assign bin1 = frappe.get_doc(...)

```python
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

### Step 6: Call bin1.insert()

```python
bin1.insert()
```

### Step 7: Assign bin2 = frappe.get_doc(...)

```python
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

### Step 8: Assign bin = _create_bin(...)

```python
bin = _create_bin(item_code, warehouse)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(bin.item_code, item_code)
```

### Step 10: Call frappe.db.rollback()

```python
frappe.db.rollback()
```

### Step 11: Call bin2.insert()

```python
bin2.insert()
```


## Complete Example

```python
# Workflow
'Ensure no duplicates are possible in case of concurrent inserts'
item_code = '_TestConcurrentBin'
make_item(item_code)
warehouse = '_Test Warehouse - _TC'
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
bin1.insert()
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
with self.assertRaises(frappe.UniqueValidationError):
    bin2.insert()
bin = _create_bin(item_code, warehouse)
self.assertEqual(bin.item_code, item_code)
frappe.db.rollback()
```

## Next Steps


---

*Source: test_bin.py:12 | Complexity: Advanced | Last updated: 2026-02-04*