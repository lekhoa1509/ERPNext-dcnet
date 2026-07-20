# How To: Validate Negative Stock For Inventory Dimension

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate negative stock for inventory dimension

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

### Step 1: Assign item_code = 'Test Negative Inventory Dimension Item'

```python
item_code = 'Test Negative Inventory Dimension Item'
```

### Step 2: Call frappe.db.set_single_value()

```python
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
```

### Step 3: Call create_item()

```python
create_item(item_code)
```

### Step 4: Assign inv_dimension = create_inventory_dimension(...)

```python
inv_dimension = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
```

### Step 5: Assign warehouse = create_warehouse(...)

```python
warehouse = create_warehouse('Negative Stock Warehouse')
```

### Step 6: Assign doc = make_stock_entry(...)

```python
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=10, do_not_submit=True)
```

### Step 7: Assign unknown.inv_site = 'Site 1'

```python
doc.items[0].inv_site = 'Site 1'
```

### Step 8: Call self.assertRaises()

```python
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
```

### Step 9: Call doc.reload()

```python
doc.reload()
```

### Step 10: Assign doc = make_stock_entry(...)

```python
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=10, do_not_submit=True)
```

### Step 11: Assign unknown.to_inv_site = 'Site 1'

```python
doc.items[0].to_inv_site = 'Site 1'
```

### Step 12: Call doc.submit()

```python
doc.submit()
```

### Step 13: Assign site_name = value

```python
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(site_name, 'Site 1')
```

### Step 15: Assign doc = make_stock_entry(...)

```python
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=100)
```

### Step 16: Assign doc = make_stock_entry(...)

```python
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
```

### Step 17: Assign unknown.inv_site = 'Site 1'

```python
doc.items[0].inv_site = 'Site 1'
```

### Step 18: Call self.assertRaises()

```python
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
```

### Step 19: Call inv_dimension.reload()

```python
inv_dimension.reload()
```

### Step 20: Call inv_dimension.db_set()

```python
inv_dimension.db_set('validate_negative_stock', 0)
```

### Step 21: Call frappe.clear_cache()

```python
frappe.clear_cache(doctype='Inventory Dimension')
```

### Step 22: Assign doc = make_stock_entry(...)

```python
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
```

### Step 23: Assign unknown.inv_site = 'Site 1'

```python
doc.items[0].inv_site = 'Site 1'
```

### Step 24: Call doc.submit()

```python
doc.submit()
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(doc.docstatus, 1)
```

### Step 26: Assign site_name = value

```python
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(site_name, 'Site 1')
```

### Step 28: Call doc.cancel()

```python
doc.cancel()
```


## Complete Example

```python
# Workflow
item_code = 'Test Negative Inventory Dimension Item'
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
create_item(item_code)
inv_dimension = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
warehouse = create_warehouse('Negative Stock Warehouse')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=10, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
doc.reload()
if doc.docstatus == 1:
    doc.cancel()
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=10, do_not_submit=True)
doc.items[0].to_inv_site = 'Site 1'
doc.submit()
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=100)
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
inv_dimension.reload()
inv_dimension.db_set('validate_negative_stock', 0)
frappe.clear_cache(doctype='Inventory Dimension')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
doc.submit()
self.assertEqual(doc.docstatus, 1)
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
```

## Next Steps


---

*Source: test_inventory_dimension.py:435 | Complexity: Advanced | Last updated: 2026-02-04*