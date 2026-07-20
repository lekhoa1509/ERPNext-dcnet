# How To: Putaway Rule On Stock Entry Material Transfer

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test if source warehouse is considered while applying rules.

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()
```

## Step-by-Step Guide

### Step 1: 'Test if source warehouse is considered while applying rules.'

```python
'Test if source warehouse is considered while applying rules.'
```

### Step 2: Assign rule_1 = create_putaway_rule(...)

```python
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
```

### Step 3: Assign rule_2 = create_putaway_rule(...)

```python
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=100, uom='Kg', priority=2)
```

### Step 4: Assign stock_entry = make_stock_entry(...)

```python
stock_entry = make_stock_entry(item_code='_Rice', source=self.warehouse_1, qty=200, target='_Test Warehouse - _TC', purpose='Material Transfer', apply_putaway_rule=1, do_not_submit=1)
```

### Step 5: Assign stock_entry_item = value

```python
stock_entry_item = stock_entry.get('items')[0]
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(stock_entry_item.t_warehouse, self.warehouse_2)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(stock_entry_item.qty, 100)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(stock_entry_item.putaway_rule, rule_2.name)
```

### Step 9: Call self.assertUnchangedItemsOnResave()

```python
self.assertUnchangedItemsOnResave(stock_entry)
```

### Step 10: Call stock_entry.delete()

```python
stock_entry.delete()
```

### Step 11: Call rule_1.delete()

```python
rule_1.delete()
```

### Step 12: Call rule_2.delete()

```python
rule_2.delete()
```


## Complete Example

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

# Workflow
'Test if source warehouse is considered while applying rules.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=100, uom='Kg', priority=2)
stock_entry = make_stock_entry(item_code='_Rice', source=self.warehouse_1, qty=200, target='_Test Warehouse - _TC', purpose='Material Transfer', apply_putaway_rule=1, do_not_submit=1)
stock_entry_item = stock_entry.get('items')[0]
self.assertEqual(stock_entry_item.t_warehouse, self.warehouse_2)
self.assertEqual(stock_entry_item.qty, 100)
self.assertEqual(stock_entry_item.putaway_rule, rule_2.name)
self.assertUnchangedItemsOnResave(stock_entry)
stock_entry.delete()
rule_1.delete()
rule_2.delete()
```

## Next Steps


---

*Source: test_putaway_rule.py:239 | Complexity: Advanced | Last updated: 2026-02-04*