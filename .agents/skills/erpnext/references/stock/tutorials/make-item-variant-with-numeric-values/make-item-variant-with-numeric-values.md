# How To: Make Item Variant With Numeric Values

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make item variant with numeric values

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
frappe.delete_doc_if_exists('Item', '_Test Numeric Template Item')
```

### Step 2: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Item Attribute', 'Test Item Length')
```

### Step 3: Call frappe.db.sql()

```python
frappe.db.sql("delete from `tabItem Variant Attribute`\n\t\t\twhere attribute='Test Item Length' ")
```

### Step 4: Assign frappe.flags.attribute_values = None

```python
frappe.flags.attribute_values = None
```

### Step 5: Call frappe.get_doc.insert()

```python
frappe.get_doc({'doctype': 'Item Attribute', 'attribute_name': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}).insert()
```

### Step 6: Call make_item()

```python
make_item('_Test Numeric Template Item', {'attributes': [{'attribute': 'Test Size'}, {'attribute': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}], 'item_defaults': [{'default_warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'}], 'has_variants': 1})
```

### Step 7: Assign variant = create_variant(...)

```python
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.1})
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.1')
```

### Step 9: Assign variant.item_code = '_Test Numeric Variant-L-1.1'

```python
variant.item_code = '_Test Numeric Variant-L-1.1'
```

### Step 10: Assign variant.item_name = '_Test Numeric Variant Large 1.1m'

```python
variant.item_name = '_Test Numeric Variant Large 1.1m'
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(InvalidItemAttributeValueError, variant.save)
```

### Step 12: Assign variant = create_variant(...)

```python
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.5})
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.5')
```

### Step 14: Assign variant.item_code = '_Test Numeric Variant-L-1.5'

```python
variant.item_code = '_Test Numeric Variant-L-1.5'
```

### Step 15: Assign variant.item_name = '_Test Numeric Variant Large 1.5m'

```python
variant.item_name = '_Test Numeric Variant Large 1.5m'
```

### Step 16: Call variant.save()

```python
variant.save()
```

### Step 17: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Item', d.name)
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
for d in frappe.db.get_all('Item', filters={'variant_of': '_Test Numeric Template Item'}):
    frappe.delete_doc_if_exists('Item', d.name)
frappe.delete_doc_if_exists('Item', '_Test Numeric Template Item')
frappe.delete_doc_if_exists('Item Attribute', 'Test Item Length')
frappe.db.sql("delete from `tabItem Variant Attribute`\n\t\t\twhere attribute='Test Item Length' ")
frappe.flags.attribute_values = None
frappe.get_doc({'doctype': 'Item Attribute', 'attribute_name': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}).insert()
make_item('_Test Numeric Template Item', {'attributes': [{'attribute': 'Test Size'}, {'attribute': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}], 'item_defaults': [{'default_warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'}], 'has_variants': 1})
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.1})
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.1')
variant.item_code = '_Test Numeric Variant-L-1.1'
variant.item_name = '_Test Numeric Variant Large 1.1m'
self.assertRaises(InvalidItemAttributeValueError, variant.save)
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.5})
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.5')
variant.item_code = '_Test Numeric Variant-L-1.5'
variant.item_name = '_Test Numeric Variant Large 1.5m'
variant.save()
```

## Next Steps


---

*Source: test_item.py:445 | Complexity: Advanced | Last updated: 2026-02-04*