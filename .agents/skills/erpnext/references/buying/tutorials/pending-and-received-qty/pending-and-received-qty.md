# How To: Pending And Received Qty

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test pending and received qty

## Prerequisites

**Required Modules:**
- `copy`
- `frappe`
- `frappe.tests`
- `erpnext.buying.report.subcontracted_item_to_be_received.subcontracted_item_to_be_received`
- `erpnext.controllers.tests.test_subcontracting_controller`
- `erpnext.subcontracting.doctype.subcontracting_order.subcontracting_order`


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
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
```

### Step 4: Assign rm_items = get_rm_items(...)

```python
rm_items = get_rm_items(sco.supplied_items)
```

### Step 5: Assign itemwise_details = make_stock_in_entry(...)

```python
itemwise_details = make_stock_in_entry(rm_items=rm_items)
```

### Step 6: Call make_stock_transfer_entry()

```python
make_stock_transfer_entry(sco_no=sco.name, rm_items=rm_items, itemwise_details=copy.deepcopy(itemwise_details))
```

### Step 7: Call make_subcontracting_receipt_against_sco()

```python
make_subcontracting_receipt_against_sco(sco.name)
```

### Step 8: Call sco.reload()

```python
sco.reload()
```

### Step 9: Assign unknown = execute(...)

```python
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(data[0]['pending_qty'], 5)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(data[0]['received_qty'], 5)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(data[0]['subcontract_order'], sco.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(data[0]['supplier'], sco.supplier)
```

### Step 14: Assign unknown = value

```python
item['sco_rm_detail'] = sco.items[0].name
```


## Complete Example

```python
# Workflow
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
rm_items = get_rm_items(sco.supplied_items)
itemwise_details = make_stock_in_entry(rm_items=rm_items)
for item in rm_items:
    item['sco_rm_detail'] = sco.items[0].name
make_stock_transfer_entry(sco_no=sco.name, rm_items=rm_items, itemwise_details=copy.deepcopy(itemwise_details))
make_subcontracting_receipt_against_sco(sco.name)
sco.reload()
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
self.assertEqual(data[0]['pending_qty'], 5)
self.assertEqual(data[0]['received_qty'], 5)
self.assertEqual(data[0]['subcontract_order'], sco.name)
self.assertEqual(data[0]['supplier'], sco.supplier)
```

## Next Steps


---

*Source: test_subcontracted_item_to_be_received.py:28 | Complexity: Advanced | Last updated: 2026-02-04*