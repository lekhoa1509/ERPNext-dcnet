# How To: Item Variant By Manufacturer

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item variant by manufacturer

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

### Step 1: Assign template = value

```python
template = make_item('_Test Item Variant By Manufacturer', {'has_variants': 1, 'variant_based_on': 'Manufacturer'}).name
```

### Step 2: Call self.assertFalse()

```python
self.assertFalse(frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS'}))
```

### Step 3: Assign variant = get_variant(...)

```python
variant = get_variant(template, manufacturer='DFSS', manufacturer_part_no='DFSS-123')
```

### Step 4: Assign item_manufacturer = frappe.db.exists(...)

```python
item_manufacturer = frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS', 'item_code': variant.name})
```

### Step 5: Call self.assertTrue()

```python
self.assertTrue(item_manufacturer)
```

### Step 6: Call frappe.delete_doc()

```python
frappe.delete_doc('Item Manufacturer', item_manufacturer)
```

### Step 7: Assign m_doc = frappe.new_doc(...)

```python
m_doc = frappe.new_doc('Manufacturer')
```

### Step 8: Assign m_doc.short_name = manufacturer

```python
m_doc.short_name = manufacturer
```

### Step 9: Call m_doc.insert()

```python
m_doc.insert()
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
template = make_item('_Test Item Variant By Manufacturer', {'has_variants': 1, 'variant_based_on': 'Manufacturer'}).name
for manufacturer in ['DFSS', 'DASA', 'ASAAS']:
    if not frappe.db.exists('Manufacturer', manufacturer):
        m_doc = frappe.new_doc('Manufacturer')
        m_doc.short_name = manufacturer
        m_doc.insert()
self.assertFalse(frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS'}))
variant = get_variant(template, manufacturer='DFSS', manufacturer_part_no='DFSS-123')
item_manufacturer = frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS', 'item_code': variant.name})
self.assertTrue(item_manufacturer)
frappe.delete_doc('Item Manufacturer', item_manufacturer)
```

## Next Steps


---

*Source: test_item.py:569 | Complexity: Advanced | Last updated: 2026-02-04*