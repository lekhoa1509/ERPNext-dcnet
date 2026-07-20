# How To: Add Item Barcode

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test add item barcode

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

### Step 1: Call frappe.db.sql()

```python
frappe.db.sql('delete from `tabItem Barcode`')
```

### Step 2: Assign item_code = 'Test Item Barcode'

```python
item_code = 'Test Item Barcode'
```

### Step 3: Assign barcode_properties_list = value

```python
barcode_properties_list = [{'barcode': '0012345678905', 'barcode_type': 'EAN'}, {'barcode': '012345678905', 'barcode_type': 'UAN'}, {'barcode': 'ARBITRARY_TEXT'}, {'barcode': '72527273070', 'barcode_type': 'UPC-A'}, {'barcode': '123456', 'barcode_type': 'CODE-39'}, {'barcode': '401268452363', 'barcode_type': 'EAN'}, {'barcode': '90311017', 'barcode_type': 'EAN'}, {'barcode': '73513537', 'barcode_type': 'EAN'}, {'barcode': '0123456789012', 'barcode_type': 'GS1'}, {'barcode': '2211564566668', 'barcode_type': 'GTIN'}, {'barcode': '0256480249', 'barcode_type': 'ISBN'}, {'barcode': '0192552570', 'barcode_type': 'ISBN-10'}, {'barcode': '9781234567897', 'barcode_type': 'ISBN-13'}, {'barcode': '9771234567898', 'barcode_type': 'ISSN'}, {'barcode': '4581171967072', 'barcode_type': 'JAN'}, {'barcode': '12345678', 'barcode_type': 'PZN'}, {'barcode': '725272730706', 'barcode_type': 'UPC'}]
```

### Step 4: Call create_item()

```python
create_item(item_code)
```

### Step 5: Assign barcodes = frappe.get_all(...)

```python
barcodes = frappe.get_all('Item Barcode', fields=['barcode', 'barcode_type'], filters={'parent': item_code})
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(len(matching_barcodes), 1)
```

### Step 7: Assign details = value

```python
details = matching_barcodes[0]
```

### Step 8: Assign item_doc = frappe.get_doc(...)

```python
item_doc = frappe.get_doc('Item', item_code)
```

### Step 9: Assign new_barcode = item_doc.append(...)

```python
new_barcode = item_doc.append('barcodes')
```

### Step 10: Call new_barcode.update()

```python
new_barcode.update(barcode_properties_list[0])
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.UniqueValidationError, item_doc.save)
```

### Step 12: Assign item_doc = frappe.get_doc(...)

```python
item_doc = frappe.get_doc('Item', item_code)
```

### Step 13: Assign new_barcode = item_doc.append(...)

```python
new_barcode = item_doc.append('barcodes')
```

### Step 14: Assign new_barcode.barcode = '9999999999999'

```python
new_barcode.barcode = '9999999999999'
```

### Step 15: Assign new_barcode.barcode_type = 'EAN'

```python
new_barcode.barcode_type = 'EAN'
```

### Step 16: Call self.assertRaises()

```python
self.assertRaises(InvalidBarcode, item_doc.save)
```

### Step 17: Call frappe.delete_doc()

```python
frappe.delete_doc('Item', item_code)
```

### Step 18: Assign item_doc = frappe.get_doc(...)

```python
item_doc = frappe.get_doc('Item', item_code)
```

### Step 19: Assign new_barcode = item_doc.append(...)

```python
new_barcode = item_doc.append('barcodes')
```

### Step 20: Call new_barcode.update()

```python
new_barcode.update(barcode_properties)
```

### Step 21: Call item_doc.save()

```python
item_doc.save()
```

### Step 22: Assign barcode_to_find = value

```python
barcode_to_find = barcode_properties['barcode']
```

### Step 23: Assign matching_barcodes = value

```python
matching_barcodes = [x for x in barcodes if x['barcode'] == barcode_to_find]
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(value, details.get(key))
```


## Complete Example

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

# Workflow
frappe.db.sql('delete from `tabItem Barcode`')
item_code = 'Test Item Barcode'
if frappe.db.exists('Item', item_code):
    frappe.delete_doc('Item', item_code)
barcode_properties_list = [{'barcode': '0012345678905', 'barcode_type': 'EAN'}, {'barcode': '012345678905', 'barcode_type': 'UAN'}, {'barcode': 'ARBITRARY_TEXT'}, {'barcode': '72527273070', 'barcode_type': 'UPC-A'}, {'barcode': '123456', 'barcode_type': 'CODE-39'}, {'barcode': '401268452363', 'barcode_type': 'EAN'}, {'barcode': '90311017', 'barcode_type': 'EAN'}, {'barcode': '73513537', 'barcode_type': 'EAN'}, {'barcode': '0123456789012', 'barcode_type': 'GS1'}, {'barcode': '2211564566668', 'barcode_type': 'GTIN'}, {'barcode': '0256480249', 'barcode_type': 'ISBN'}, {'barcode': '0192552570', 'barcode_type': 'ISBN-10'}, {'barcode': '9781234567897', 'barcode_type': 'ISBN-13'}, {'barcode': '9771234567898', 'barcode_type': 'ISSN'}, {'barcode': '4581171967072', 'barcode_type': 'JAN'}, {'barcode': '12345678', 'barcode_type': 'PZN'}, {'barcode': '725272730706', 'barcode_type': 'UPC'}]
create_item(item_code)
for barcode_properties in barcode_properties_list:
    item_doc = frappe.get_doc('Item', item_code)
    new_barcode = item_doc.append('barcodes')
    new_barcode.update(barcode_properties)
    item_doc.save()
barcodes = frappe.get_all('Item Barcode', fields=['barcode', 'barcode_type'], filters={'parent': item_code})
for barcode_properties in barcode_properties_list:
    barcode_to_find = barcode_properties['barcode']
    matching_barcodes = [x for x in barcodes if x['barcode'] == barcode_to_find]
self.assertEqual(len(matching_barcodes), 1)
details = matching_barcodes[0]
for key, value in barcode_properties.items():
    self.assertEqual(value, details.get(key))
item_doc = frappe.get_doc('Item', item_code)
new_barcode = item_doc.append('barcodes')
new_barcode.update(barcode_properties_list[0])
self.assertRaises(frappe.UniqueValidationError, item_doc.save)
item_doc = frappe.get_doc('Item', item_code)
new_barcode = item_doc.append('barcodes')
new_barcode.barcode = '9999999999999'
new_barcode.barcode_type = 'EAN'
self.assertRaises(InvalidBarcode, item_doc.save)
```

## Next Steps


---

*Source: test_item.py:599 | Complexity: Advanced | Last updated: 2026-02-04*