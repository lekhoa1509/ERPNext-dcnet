# How To: Make Supplier Quotation From Portal

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make supplier quotation from portal

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

### Step 1: Assign rfq = make_request_for_quotation(...)

```python
rfq = make_request_for_quotation()
```

### Step 2: Assign unknown.rate = 100

```python
rfq.get('items')[0].rate = 100
```

### Step 3: Assign rfq.supplier = value

```python
rfq.supplier = rfq.suppliers[0].supplier
```

### Step 4: Assign supplier_quotation_name = create_supplier_quotation(...)

```python
supplier_quotation_name = create_supplier_quotation(rfq)
```

### Step 5: Assign supplier_quotation_doc = frappe.get_doc(...)

```python
supplier_quotation_doc = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation_doc.supplier, rfq.get('suppliers')[0].supplier)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation_doc.get('items')[0].request_for_quotation, rfq.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation_doc.get('items')[0].item_code, '_Test Item')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation_doc.get('items')[0].qty, 5)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)
```


## Complete Example

```python
# Workflow
rfq = make_request_for_quotation()
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation_doc = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation_doc.supplier, rfq.get('suppliers')[0].supplier)
self.assertEqual(supplier_quotation_doc.get('items')[0].request_for_quotation, rfq.name)
self.assertEqual(supplier_quotation_doc.get('items')[0].item_code, '_Test Item')
self.assertEqual(supplier_quotation_doc.get('items')[0].qty, 5)
self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)
```

## Next Steps


---

*Source: test_request_for_quotation.py:138 | Complexity: Advanced | Last updated: 2026-02-04*