# How To: Putaway Rules Multi Uom

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test rules applied on uom other than stock uom.

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.stock.doctype.batch.test_batch`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.test_stock_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.stock.get_item_details`
- `erpnext.stock.dashboard.warehouse_capacity_dashboard`


## Step-by-Step Guide

### Step 1: 'Test rules applied on uom other than stock uom.'

```python
'Test rules applied on uom other than stock uom.'
```

### Step 2: Assign item = frappe.get_doc(...)

```python
item = frappe.get_doc('Item', '_Rice')
```

### Step 3: Assign rule_1 = create_putaway_rule(...)

```python
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=3, uom='Bag')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(rule_1.stock_capacity, 3000)
```

### Step 5: Assign rule_2 = create_putaway_rule(...)

```python
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=4, uom='Bag')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(rule_2.stock_capacity, 4000)
```

### Step 7: Assign stock_receipt = make_stock_entry(...)

```python
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=1000, basic_rate=50)
```

### Step 8: Assign pr = make_purchase_receipt(...)

```python
pr = make_purchase_receipt(item_code='_Rice', qty=6, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(len(pr.items), 2)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].qty, 4)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pr.items[1].qty, 2)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
```

### Step 14: Call stock_receipt.cancel()

```python
stock_receipt.cancel()
```

### Step 15: Call pr.delete()

```python
pr.delete()
```

### Step 16: Call rule_1.delete()

```python
rule_1.delete()
```

### Step 17: Call rule_2.delete()

```python
rule_2.delete()
```

### Step 18: Call item.append()

```python
item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
```

### Step 19: Call item.save()

```python
item.save()
```


## Complete Example

```python
# Workflow
'Test rules applied on uom other than stock uom.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=3, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 3000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=4, uom='Bag')
self.assertEqual(rule_2.stock_capacity, 4000)
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=1000, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=6, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 4)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 2)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

## Next Steps


---

*Source: test_putaway_rule.py:111 | Complexity: Advanced | Last updated: 2026-02-04*