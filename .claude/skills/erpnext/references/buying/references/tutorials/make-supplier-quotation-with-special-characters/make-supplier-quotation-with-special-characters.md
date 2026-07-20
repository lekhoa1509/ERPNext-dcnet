# How To: Make Supplier Quotation With Special Characters

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make supplier quotation with special characters

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

### Step 1: Call frappe.delete_doc_if_exists()

```python
frappe.delete_doc_if_exists('Supplier', "_Test Supplier '1", force=1)
```

### Step 2: Assign supplier = frappe.new_doc(...)

```python
supplier = frappe.new_doc('Supplier')
```

### Step 3: Assign supplier.supplier_name = "_Test Supplier '1"

```python
supplier.supplier_name = "_Test Supplier '1"
```

### Step 4: Assign supplier.supplier_group = '_Test Supplier Group'

```python
supplier.supplier_group = '_Test Supplier Group'
```

### Step 5: Call supplier.insert()

```python
supplier.insert()
```

### Step 6: Assign rfq = make_request_for_quotation(...)

```python
rfq = make_request_for_quotation(supplier_data=supplier_wt_appos)
```

### Step 7: Assign sq = make_supplier_quotation_from_rfq(...)

```python
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier_wt_appos[0].get('supplier'))
```

### Step 8: Call sq.submit()

```python
sq.submit()
```

### Step 9: Assign frappe.form_dict.name = value

```python
frappe.form_dict.name = rfq.name
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)
```

### Step 11: Assign frappe.form_dict.name = None

```python
frappe.form_dict.name = None
```


## Complete Example

```python
# Workflow
frappe.delete_doc_if_exists('Supplier', "_Test Supplier '1", force=1)
supplier = frappe.new_doc('Supplier')
supplier.supplier_name = "_Test Supplier '1"
supplier.supplier_group = '_Test Supplier Group'
supplier.insert()
rfq = make_request_for_quotation(supplier_data=supplier_wt_appos)
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier_wt_appos[0].get('supplier'))
sq.submit()
frappe.form_dict.name = rfq.name
self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)
frappe.form_dict.name = None
```

## Next Steps


---

*Source: test_request_for_quotation.py:119 | Complexity: Advanced | Last updated: 2026-02-04*