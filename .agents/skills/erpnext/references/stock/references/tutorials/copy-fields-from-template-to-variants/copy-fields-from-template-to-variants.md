# How To: Copy Fields From Template To Variants

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test copy fields from template to variants

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `json`
- `frappe`
- `frappe.custom.doctype.property_setter.property_setter`
- `frappe.test_runner`
- `frappe.tests`
- `frappe.utils`
- `erpnext.controllers.item_variant`
- `erpnext.stock.doctype.item.item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.get_item_details`
- `erpnext.assets.doctype.asset.test_asset`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `time`
- `erpnext.stock.stock_balance`
- `erpnext.stock.stock_ledger`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.dashboard.item_dashboard`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.controllers.queries`
- `erpnext.stock.doctype.warehouse.test_warehouse`

**Setup Required:**
```python
super().setUp()
frappe.flags.attribute_values = None
```

## Step-by-Step Guide

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Item', '_Test Variant Item-XL', force=1)
```

### Step 2: Assign fields = value

```python
fields = [{'field_name': 'item_group'}, {'field_name': 'is_stock_item'}]
```

### Step 3: Assign allow_fields = value

```python
allow_fields = [d.get('field_name') for d in fields]
```

### Step 4: Call set_item_variant_settings()

```python
set_item_variant_settings(fields)
```

### Step 5: Assign template = frappe.get_doc(...)

```python
template = frappe.get_doc('Item', '_Test Variant Item')
```

### Step 6: Assign template.item_group = '_Test Item Group D'

```python
template.item_group = '_Test Item Group D'
```

### Step 7: Call template.save()

```python
template.save()
```

### Step 8: Assign variant = create_variant(...)

```python
variant = create_variant('_Test Variant Item', {'Test Size': 'Extra Large'})
```

### Step 9: Assign variant.item_code = '_Test Variant Item-XL'

```python
variant.item_code = '_Test Variant Item-XL'
```

### Step 10: Assign variant.item_name = '_Test Variant Item-XL'

```python
variant.item_name = '_Test Variant Item-XL'
```

### Step 11: Call variant.save()

```python
variant.save()
```

### Step 12: Assign variant = frappe.get_doc(...)

```python
variant = frappe.get_doc('Item', '_Test Variant Item-XL')
```

### Step 13: Assign template = frappe.get_doc(...)

```python
template = frappe.get_doc('Item', '_Test Variant Item')
```

### Step 14: Assign template.item_group = '_Test Item Group Desktops'

```python
template.item_group = '_Test Item Group Desktops'
```

### Step 15: Call template.save()

```python
template.save()
```

### Step 16: Assign item_attribute = frappe.get_doc(...)

```python
item_attribute = frappe.get_doc('Item Attribute', 'Test Size')
```

### Step 17: Call item_attribute.append()

```python
item_attribute.append('item_attribute_values', {'attribute_value': 'Extra Large', 'abbr': 'XL'})
```

### Step 18: Call item_attribute.save()

```python
item_attribute.save()
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(template.get(fieldname), variant.get(fieldname))
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
frappe.delete_doc_if_exists('Item', '_Test Variant Item-XL', force=1)
fields = [{'field_name': 'item_group'}, {'field_name': 'is_stock_item'}]
allow_fields = [d.get('field_name') for d in fields]
set_item_variant_settings(fields)
if not frappe.db.get_value('Item Attribute Value', {'parent': 'Test Size', 'attribute_value': 'Extra Large'}, 'name'):
    item_attribute = frappe.get_doc('Item Attribute', 'Test Size')
    item_attribute.append('item_attribute_values', {'attribute_value': 'Extra Large', 'abbr': 'XL'})
    item_attribute.save()
template = frappe.get_doc('Item', '_Test Variant Item')
template.item_group = '_Test Item Group D'
template.save()
variant = create_variant('_Test Variant Item', {'Test Size': 'Extra Large'})
variant.item_code = '_Test Variant Item-XL'
variant.item_name = '_Test Variant Item-XL'
variant.save()
variant = frappe.get_doc('Item', '_Test Variant Item-XL')
for fieldname in allow_fields:
    self.assertEqual(template.get(fieldname), variant.get(fieldname))
template = frappe.get_doc('Item', '_Test Variant Item')
template.item_group = '_Test Item Group Desktops'
template.save()
```

## Next Steps


---

*Source: test_item.py:414 | Complexity: Advanced | Last updated: 2026-02-04*