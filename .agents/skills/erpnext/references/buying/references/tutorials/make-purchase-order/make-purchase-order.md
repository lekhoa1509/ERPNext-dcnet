# How To: Make Purchase Order

**Difficulty**: Advanced
**Estimated Time**: 15 minutes
**Tags**: workflow, integration

## Overview

Workflow: test make purchase order

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.buying.doctype.supplier_quotation.supplier_quotation`
- `erpnext.controllers.accounts_controller`


## Step-by-Step Guide

### Step 1: Assign sq = frappe.copy_doc.insert(...)

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0]).insert()
```

### Step 2: Call self.assertRaises()

```python
self.assertRaises(frappe.ValidationError, make_purchase_order, sq.name)
```

### Step 3: Assign sq = frappe.get_doc(...)

```python
sq = frappe.get_doc('Supplier Quotation', sq.name)
```

### Step 4: Call sq.submit()

```python
sq.submit()
```

### Step 5: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(sq.name)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(po.doctype, 'Purchase Order')
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(len(po.get('items')), len(sq.get('items')))
```

### Step 8: Assign po.naming_series = '_T-Purchase Order-'

```python
po.naming_series = '_T-Purchase Order-'
```

### Step 9: Call po.insert()

```python
po.insert()
```

### Step 10: Call doc.set()

```python
doc.set('schedule_date', add_days(today(), 1))
```


## Complete Example

```python
# Workflow
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0]).insert()
self.assertRaises(frappe.ValidationError, make_purchase_order, sq.name)
sq = frappe.get_doc('Supplier Quotation', sq.name)
sq.submit()
po = make_purchase_order(sq.name)
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(sq.get('items')))
po.naming_series = '_T-Purchase Order-'
for doc in po.get('items'):
    if doc.get('item_code'):
        doc.set('schedule_date', add_days(today(), 1))
po.insert()
```

## Next Steps


---

*Source: test_supplier_quotation.py:133 | Complexity: Advanced | Last updated: 2026-02-04*