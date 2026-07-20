# How To: Inventory Dimension For Purchase Receipt And Delivery Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test inventory dimension for purchase receipt and delivery note

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

### Step 1: Assign inv_dimension = create_inventory_dimension(...)

```python
inv_dimension = create_inventory_dimension(reference_document='Rack', dimension_name='Rack', apply_to_all_doctypes=1)
```

### Step 2: Call inv_dimension.db_set()

```python
inv_dimension.db_set('fetch_from_parent', 'Rack')
```

### Step 3: Call self.assertEqual()

```python
self.assertEqual(inv_dimension.type_of_transaction, 'Both')
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(inv_dimension.fetch_from_parent, 'Rack')
```

### Step 5: Call create_custom_field()

```python
create_custom_field('Purchase Receipt', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
```

### Step 6: Call create_custom_field()

```python
create_custom_field('Delivery Note', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
```

### Step 7: Assign pr_doc = make_purchase_receipt(...)

```python
pr_doc = make_purchase_receipt(qty=2, do_not_submit=True)
```

### Step 8: Assign pr_doc.rack = 'Rack 1'

```python
pr_doc.rack = 'Rack 1'
```

### Step 9: Call pr_doc.save()

```python
pr_doc.save()
```

### Step 10: Call pr_doc.submit()

```python
pr_doc.submit()
```

### Step 11: Call pr_doc.load_from_db()

```python
pr_doc.load_from_db()
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pr_doc.items[0].rack, 'Rack 1')
```

### Step 13: Assign sle_rack = frappe.db.get_value(...)

```python
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': pr_doc.items[0].name, 'voucher_type': pr_doc.doctype}, 'rack')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(sle_rack, 'Rack 1')
```

### Step 15: Assign dn_doc = create_delivery_note(...)

```python
dn_doc = create_delivery_note(qty=2, do_not_submit=True)
```

### Step 16: Assign dn_doc.rack = 'Rack 1'

```python
dn_doc.rack = 'Rack 1'
```

### Step 17: Call dn_doc.save()

```python
dn_doc.save()
```

### Step 18: Call dn_doc.submit()

```python
dn_doc.submit()
```

### Step 19: Call dn_doc.load_from_db()

```python
dn_doc.load_from_db()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(dn_doc.items[0].rack, 'Rack 1')
```

### Step 21: Assign sle_rack = frappe.db.get_value(...)

```python
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': dn_doc.items[0].name, 'voucher_type': dn_doc.doctype}, 'rack')
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(sle_rack, 'Rack 1')
```


## Complete Example

```python
# Workflow
inv_dimension = create_inventory_dimension(reference_document='Rack', dimension_name='Rack', apply_to_all_doctypes=1)
inv_dimension.db_set('fetch_from_parent', 'Rack')
self.assertEqual(inv_dimension.type_of_transaction, 'Both')
self.assertEqual(inv_dimension.fetch_from_parent, 'Rack')
create_custom_field('Purchase Receipt', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
create_custom_field('Delivery Note', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
pr_doc = make_purchase_receipt(qty=2, do_not_submit=True)
pr_doc.rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc.load_from_db()
self.assertEqual(pr_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': pr_doc.items[0].name, 'voucher_type': pr_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
dn_doc = create_delivery_note(qty=2, do_not_submit=True)
dn_doc.rack = 'Rack 1'
dn_doc.save()
dn_doc.submit()
dn_doc.load_from_db()
self.assertEqual(dn_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': dn_doc.items[0].name, 'voucher_type': dn_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
```

## Next Steps


---

*Source: test_inventory_dimension.py:149 | Complexity: Advanced | Last updated: 2026-02-04*