# How To: Make Rfq From Opportunity

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make rfq from opportunity

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

### Step 1: Assign opportunity = make_opportunity(...)

```python
opportunity = make_opportunity(with_items=1)
```

### Step 2: Assign supplier_data = get_supplier_data(...)

```python
supplier_data = get_supplier_data()
```

### Step 3: Assign rfq = make_rfq(...)

```python
rfq = make_rfq(opportunity.name)
```

### Step 4: Call self.assertEqual()

```python
self.assertEqual(len(rfq.get('items')), len(opportunity.get('items')))
```

### Step 5: Assign rfq.message_for_supplier = 'Please supply the specified items at the best possible rates.'

```python
rfq.message_for_supplier = 'Please supply the specified items at the best possible rates.'
```

### Step 6: Assign rfq.status = 'Draft'

```python
rfq.status = 'Draft'
```

### Step 7: Call rfq.submit()

```python
rfq.submit()
```

### Step 8: Assign item.warehouse = '_Test Warehouse - _TC'

```python
item.warehouse = '_Test Warehouse - _TC'
```

### Step 9: Call rfq.append()

```python
rfq.append('suppliers', data)
```


## Complete Example

```python
# Workflow
opportunity = make_opportunity(with_items=1)
supplier_data = get_supplier_data()
rfq = make_rfq(opportunity.name)
self.assertEqual(len(rfq.get('items')), len(opportunity.get('items')))
rfq.message_for_supplier = 'Please supply the specified items at the best possible rates.'
for item in rfq.items:
    item.warehouse = '_Test Warehouse - _TC'
for data in supplier_data:
    rfq.append('suppliers', data)
rfq.status = 'Draft'
rfq.submit()
```

## Next Steps


---

*Source: test_request_for_quotation.py:171 | Complexity: Advanced | Last updated: 2026-02-04*