# How To: Inventory Dimension

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inventory dimension

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.custom.doctype.custom_field.custom_field`
- `frappe.tests`
- `frappe.utils`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.inventory_dimension.inventory_dimension`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_ledger_entry.stock_ledger_entry`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.selling.doctype.customer.test_customer`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.warehouse.test_warehouse`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.controllers.sales_and_purchase_return`
- `erpnext.stock.doctype.delivery_note.delivery_note`


## Step-by-Step Guide

### Step 1: Assign warehouse = 'Shelf Warehouse - _TC'

```python
warehouse = 'Shelf Warehouse - _TC'
```

### Step 2: Assign item_code = '_Test Item'

```python
item_code = '_Test Item'
```

### Step 3: Assign inv_dim1 = create_inventory_dimension(...)

```python
inv_dim1 = create_inventory_dimension(reference_document='Shelf', type_of_transaction='Outward', dimension_name='Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Issue'")
```

### Step 4: Assign inv_dim1.reqd = 0

```python
inv_dim1.reqd = 0
```

### Step 5: Call inv_dim1.save()

```python
inv_dim1.save()
```

### Step 6: Call create_inventory_dimension()

```python
create_inventory_dimension(reference_document='Shelf', type_of_transaction='Inward', dimension_name='To Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Receipt'")
```

### Step 7: Assign inward = make_stock_entry(...)

```python
inward = make_stock_entry(item_code=item_code, target=warehouse, qty=5, basic_rate=10, do_not_save=True, purpose='Material Receipt')
```

### Step 8: Assign unknown.to_shelf = 'Shelf 1'

```python
inward.items[0].to_shelf = 'Shelf 1'
```

### Step 9: Call inward.save()

```python
inward.save()
```

### Step 10: Call inward.submit()

```python
inward.submit()
```

### Step 11: Call inward.load_from_db()

```python
inward.load_from_db()
```

### Step 12: Assign sle_data = frappe.db.get_value(...)

```python
sle_data = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': inward.name}, ['shelf', 'warehouse'], as_dict=1)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(inward.items[0].to_shelf, 'Shelf 1')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sle_data.warehouse, warehouse)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(sle_data.shelf, 'Shelf 1')
```

### Step 16: Assign outward = make_stock_entry(...)

```python
outward = make_stock_entry(item_code=item_code, source=warehouse, qty=3, basic_rate=10, do_not_save=True, purpose='Material Issue')
```

### Step 17: Assign unknown.shelf = 'Shelf 1'

```python
outward.items[0].shelf = 'Shelf 1'
```

### Step 18: Call outward.save()

```python
outward.save()
```

### Step 19: Call outward.submit()

```python
outward.submit()
```

### Step 20: Call outward.load_from_db()

```python
outward.load_from_db()
```

### Step 21: Assign sle_shelf = frappe.db.get_value(...)

```python
sle_shelf = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': outward.name}, 'shelf')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(sle_shelf, 'Shelf 1')
```

### Step 23: Call inv_dim1.load_from_db()

```python
inv_dim1.load_from_db()
```

### Step 24: Assign inv_dim1.apply_to_all_doctypes = 1

```python
inv_dim1.apply_to_all_doctypes = 1
```

### Step 25: Call self.assertTrue()

```python
self.assertTrue(inv_dim1.has_stock_ledger())
```

### Step 26: Call self.assertRaises()

```python
self.assertRaises(DoNotChangeError, inv_dim1.save)
```


## Complete Example

```python
# Workflow
warehouse = 'Shelf Warehouse - _TC'
item_code = '_Test Item'
inv_dim1 = create_inventory_dimension(reference_document='Shelf', type_of_transaction='Outward', dimension_name='Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Issue'")
inv_dim1.reqd = 0
inv_dim1.save()
create_inventory_dimension(reference_document='Shelf', type_of_transaction='Inward', dimension_name='To Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Receipt'")
inward = make_stock_entry(item_code=item_code, target=warehouse, qty=5, basic_rate=10, do_not_save=True, purpose='Material Receipt')
inward.items[0].to_shelf = 'Shelf 1'
inward.save()
inward.submit()
inward.load_from_db()
sle_data = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': inward.name}, ['shelf', 'warehouse'], as_dict=1)
self.assertEqual(inward.items[0].to_shelf, 'Shelf 1')
self.assertEqual(sle_data.warehouse, warehouse)
self.assertEqual(sle_data.shelf, 'Shelf 1')
outward = make_stock_entry(item_code=item_code, source=warehouse, qty=3, basic_rate=10, do_not_save=True, purpose='Material Issue')
outward.items[0].shelf = 'Shelf 1'
outward.save()
outward.submit()
outward.load_from_db()
sle_shelf = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': outward.name}, 'shelf')
self.assertEqual(sle_shelf, 'Shelf 1')
inv_dim1.load_from_db()
inv_dim1.apply_to_all_doctypes = 1
self.assertTrue(inv_dim1.has_stock_ledger())
self.assertRaises(DoNotChangeError, inv_dim1.save)
```

## Next Steps


---

*Source: test_inventory_dimension.py:79 | Complexity: Advanced | Last updated: 2026-02-04*