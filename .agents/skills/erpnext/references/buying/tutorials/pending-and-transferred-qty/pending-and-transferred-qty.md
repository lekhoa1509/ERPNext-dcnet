# How To: Pending And Transferred Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pending and transferred qty

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.buying.report.subcontracted_raw_materials_to_be_transferred.subcontracted_raw_materials_to_be_transferred`
- `erpnext.controllers.subcontracting_controller`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`


## Step-by-Step Guide

### Step 1: Call make_service_item()

```python
make_service_item('Subcontracted Service Item 1')
```

### Step 2: Assign service_items = value

```python
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
```

### Step 3: Assign sco = get_subcontracting_order(...)

```python
sco = get_subcontracting_order(service_items=service_items)
```

### Step 4: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
```

### Step 5: Call make_stock_entry()

```python
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
```

### Step 6: Call transfer_subcontracted_raw_materials()

```python
transfer_subcontracted_raw_materials(sco)
```

### Step 7: Assign unknown = execute(...)

```python
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
```

### Step 8: Call sco.reload()

```python
sco.reload()
```

### Step 9: Assign sco_data = value

```python
sco_data = [row for row in data if row.get('subcontract_order') == sco.name]
```

### Step 10: Assign sco_data = sorted(...)

```python
sco_data = sorted(sco_data, key=lambda i: i['rm_item_code'])
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(len(sco_data), 2)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sco_data[0]['p_qty'], 8)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sco_data[0]['transferred_qty'], 2)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(sco_data[1]['p_qty'], 19)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(sco_data[1]['transferred_qty'], 1)
```


## Complete Example

```python
# Workflow
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items)
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
transfer_subcontracted_raw_materials(sco)
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
sco.reload()
sco_data = [row for row in data if row.get('subcontract_order') == sco.name]
sco_data = sorted(sco_data, key=lambda i: i['rm_item_code'])
self.assertEqual(len(sco_data), 2)
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
self.assertEqual(sco_data[0]['p_qty'], 8)
self.assertEqual(sco_data[0]['transferred_qty'], 2)
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
self.assertEqual(sco_data[1]['p_qty'], 19)
self.assertEqual(sco_data[1]['transferred_qty'], 1)
```

## Next Steps


---

*Source: test_subcontracted_raw_materials_to_be_transferred.py:21 | Complexity: Advanced | Last updated: 2026-02-04*