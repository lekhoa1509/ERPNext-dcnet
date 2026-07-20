# How To: Make Multi Uom Supplier Quotation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make multi uom supplier quotation

## Prerequisites

**Required Modules:**
- `urllib.parse`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.buying.doctype.request_for_quotation.request_for_quotation`
- `erpnext.controllers.accounts_controller`
- `erpnext.crm.doctype.opportunity.opportunity`
- `erpnext.crm.doctype.opportunity.test_opportunity`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.templates.pages.rfq`


## Step-by-Step Guide

### Step 1: Assign item_code = '_Test Multi UOM RFQ Item'

```python
item_code = '_Test Multi UOM RFQ Item'
```

### Step 2: Assign rfq = make_request_for_quotation(...)

```python
rfq = make_request_for_quotation(item_code='_Test Multi UOM RFQ Item', uom='Kg', conversion_factor=2)
```

### Step 3: Assign unknown.rate = 100

```python
rfq.get('items')[0].rate = 100
```

### Step 4: Assign rfq.supplier = value

```python
rfq.supplier = rfq.suppliers[0].supplier
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(rfq.items[0].stock_qty, 10)
```

### Step 6: Assign supplier_quotation_name = create_supplier_quotation(...)

```python
supplier_quotation_name = create_supplier_quotation(rfq)
```

### Step 7: Assign supplier_quotation = frappe.get_doc(...)

```python
supplier_quotation = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation.items[0].qty, 5)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation.items[0].stock_qty, 10)
```

### Step 10: Assign item = make_item(...)

```python
item = make_item(item_code, {'stock_uom': '_Test UOM'})
```

### Step 11: Assign row = item.append(...)

```python
row = item.append('uoms', {'uom': 'Kg', 'conversion_factor': 2})
```

### Step 12: Call row.db_update()

```python
row.db_update()
```


## Complete Example

```python
# Workflow
item_code = '_Test Multi UOM RFQ Item'
if not frappe.db.exists('Item', item_code):
    item = make_item(item_code, {'stock_uom': '_Test UOM'})
    row = item.append('uoms', {'uom': 'Kg', 'conversion_factor': 2})
    row.db_update()
rfq = make_request_for_quotation(item_code='_Test Multi UOM RFQ Item', uom='Kg', conversion_factor=2)
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
self.assertEqual(rfq.items[0].stock_qty, 10)
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation.items[0].qty, 5)
self.assertEqual(supplier_quotation.items[0].stock_qty, 10)
```

## Next Steps


---

*Source: test_request_for_quotation.py:152 | Complexity: Advanced | Last updated: 2026-02-04*