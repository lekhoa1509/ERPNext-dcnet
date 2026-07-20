# How To: Supplier Quotation From Zero Qty Rfq In Portal

**Difficulty**: Intermediate
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test supplier quotation from zero qty rfq in portal

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
rfq = make_request_for_quotation(qty=0)
```

### Step 2: Assign rfq.supplier = value

```python
rfq.supplier = rfq.suppliers[0].supplier
```

### Step 3: Assign sq_name = create_supplier_quotation(...)

```python
sq_name = create_supplier_quotation(rfq)
```

### Step 4: Assign sq = frappe.get_doc(...)

```python
sq = frappe.get_doc('Supplier Quotation', sq_name)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(len(sq.items), 1)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(sq.items[0].qty, 0)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(sq.items[0].item_code, rfq.items[0].item_code)
```


## Complete Example

```python
# Workflow
rfq = make_request_for_quotation(qty=0)
rfq.supplier = rfq.suppliers[0].supplier
sq_name = create_supplier_quotation(rfq)
sq = frappe.get_doc('Supplier Quotation', sq_name)
self.assertEqual(len(sq.items), 1)
self.assertEqual(sq.items[0].qty, 0)
self.assertEqual(sq.items[0].item_code, rfq.items[0].item_code)
```

## Next Steps


---

*Source: test_request_for_quotation.py:241 | Complexity: Intermediate | Last updated: 2026-02-04*