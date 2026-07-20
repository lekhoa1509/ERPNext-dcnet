# How To: Item Attribute Change After Variant

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test item attribute change after variant

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
frappe.delete_doc_if_exists('Item', '_Test Variant Item-L', force=1)
```

### Step 2: Assign variant = create_variant(...)

```python
variant = create_variant('_Test Variant Item', {'Test Size': 'Large'})
```

### Step 3: Call variant.save()

```python
variant.save()
```

### Step 4: Assign attribute = frappe.get_doc(...)

```python
attribute = frappe.get_doc('Item Attribute', 'Test Size')
```

### Step 5: Assign attribute.item_attribute_values = value

```python
attribute.item_attribute_values = []
```

### Step 6: Assign frappe.flags.attribute_values = None

```python
frappe.flags.attribute_values = None
```

### Step 7: Call self.assertRaises()

```python
self.assertRaises(InvalidItemAttributeValueError, attribute.save)
```

### Step 8: Call frappe.db.rollback()

```python
frappe.db.rollback()
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
frappe.delete_doc_if_exists('Item', '_Test Variant Item-L', force=1)
variant = create_variant('_Test Variant Item', {'Test Size': 'Large'})
variant.save()
attribute = frappe.get_doc('Item Attribute', 'Test Size')
attribute.item_attribute_values = []
frappe.flags.attribute_values = None
self.assertRaises(InvalidItemAttributeValueError, attribute.save)
frappe.db.rollback()
```

## Next Steps


---

*Source: test_item.py:388 | Complexity: Advanced | Last updated: 2026-02-04*