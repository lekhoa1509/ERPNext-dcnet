# How To: Attribute Completions

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test attribute completions

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

### Step 1: Assign expected_attrs = value

```python
expected_attrs = {'Small', 'Extra Small', 'Extra Large', 'Large', '2XL', 'Medium'}
```

### Step 2: Assign attrs = get_item_attribute(...)

```python
attrs = get_item_attribute('Test Size')
```

### Step 3: Assign received_attrs = value

```python
received_attrs = {attr.attribute_value for attr in attrs}
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(received_attrs, expected_attrs)
```

### Step 5: Assign attrs = get_item_attribute(...)

```python
attrs = get_item_attribute('Test Size', attribute_value='extra')
```

### Step 6: Assign received_attrs = value

```python
received_attrs = {attr.attribute_value for attr in attrs}
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(received_attrs, {'Extra Small', 'Extra Large'})
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
expected_attrs = {'Small', 'Extra Small', 'Extra Large', 'Large', '2XL', 'Medium'}
attrs = get_item_attribute('Test Size')
received_attrs = {attr.attribute_value for attr in attrs}
self.assertEqual(received_attrs, expected_attrs)
attrs = get_item_attribute('Test Size', attribute_value='extra')
received_attrs = {attr.attribute_value for attr in attrs}
self.assertEqual(received_attrs, {'Extra Small', 'Extra Large'})
```

## Next Steps


---

*Source: test_item.py:688 | Complexity: Intermediate | Last updated: 2026-02-04*