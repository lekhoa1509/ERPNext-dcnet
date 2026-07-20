# How To: Validate Negative Stock With Multiple Dimension

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test validate negative stock with multiple dimension

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

### Step 1: Assign item_code = 'Test Negative Multi Inventory Dimension Item'

```python
item_code = 'Test Negative Multi Inventory Dimension Item'
```

### Step 2: Call create_item()

```python
create_item(item_code)
```

### Step 3: Assign inv_dimension_1 = create_inventory_dimension(...)

```python
inv_dimension_1 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
```

### Step 4: Call inv_dimension_1.db_set()

```python
inv_dimension_1.db_set('validate_negative_stock', 1)
```

### Step 5: Assign inv_dimension_2 = create_inventory_dimension(...)

```python
inv_dimension_2 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Rack', reference_document='Rack', document_type='Rack', validate_negative_stock=1)
```

### Step 6: Call inv_dimension_2.db_set()

```python
inv_dimension_2.db_set('validate_negative_stock', 1)
```

### Step 7: Assign pr_doc = make_purchase_receipt(...)

```python
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
```

### Step 8: Assign unknown.inv_site = 'Site 1'

```python
pr_doc.items[0].inv_site = 'Site 1'
```

### Step 9: Assign unknown.rack = 'Rack 1'

```python
pr_doc.items[0].rack = 'Rack 1'
```

### Step 10: Call pr_doc.save()

```python
pr_doc.save()
```

### Step 11: Call pr_doc.submit()

```python
pr_doc.submit()
```

### Step 12: Assign pr_doc = make_purchase_receipt(...)

```python
pr_doc = make_purchase_receipt(item_code=item_code, qty=15, do_not_submit=True)
```

### Step 13: Assign unknown.inv_site = 'Site 1'

```python
pr_doc.items[0].inv_site = 'Site 1'
```

### Step 14: Assign unknown.rack = 'Rack 2'

```python
pr_doc.items[0].rack = 'Rack 2'
```

### Step 15: Call pr_doc.save()

```python
pr_doc.save()
```

### Step 16: Call pr_doc.submit()

```python
pr_doc.submit()
```

### Step 17: Assign pr_doc = make_purchase_receipt(...)

```python
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
```

### Step 18: Assign unknown.inv_site = 'Site 2'

```python
pr_doc.items[0].inv_site = 'Site 2'
```

### Step 19: Assign unknown.rack = 'Rack 1'

```python
pr_doc.items[0].rack = 'Rack 1'
```

### Step 20: Call pr_doc.save()

```python
pr_doc.save()
```

### Step 21: Call pr_doc.submit()

```python
pr_doc.submit()
```

### Step 22: Assign pr_doc = make_purchase_receipt(...)

```python
pr_doc = make_purchase_receipt(item_code=item_code, qty=25, do_not_submit=True)
```

### Step 23: Assign unknown.inv_site = 'Site 2'

```python
pr_doc.items[0].inv_site = 'Site 2'
```

### Step 24: Assign unknown.rack = 'Rack 2'

```python
pr_doc.items[0].rack = 'Rack 2'
```

### Step 25: Call pr_doc.save()

```python
pr_doc.save()
```

### Step 26: Call pr_doc.submit()

```python
pr_doc.submit()
```

### Step 27: Assign dn_doc = create_delivery_note(...)

```python
dn_doc = create_delivery_note(item_code=item_code, qty=35, do_not_submit=True)
```

### Step 28: Assign unknown.inv_site = 'Site 2'

```python
dn_doc.items[0].inv_site = 'Site 2'
```

### Step 29: Assign unknown.rack = 'Rack 1'

```python
dn_doc.items[0].rack = 'Rack 1'
```

### Step 30: Call dn_doc.save()

```python
dn_doc.save()
```

### Step 31: Call self.assertRaises()

```python
self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)
```


## Complete Example

```python
# Workflow
item_code = 'Test Negative Multi Inventory Dimension Item'
create_item(item_code)
inv_dimension_1 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
inv_dimension_1.db_set('validate_negative_stock', 1)
inv_dimension_2 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Rack', reference_document='Rack', document_type='Rack', validate_negative_stock=1)
inv_dimension_2.db_set('validate_negative_stock', 1)
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=15, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=25, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
dn_doc = create_delivery_note(item_code=item_code, qty=35, do_not_submit=True)
dn_doc.items[0].inv_site = 'Site 2'
dn_doc.items[0].rack = 'Rack 1'
dn_doc.save()
self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)
```

## Next Steps


---

*Source: test_inventory_dimension.py:500 | Complexity: Advanced | Last updated: 2026-02-04*