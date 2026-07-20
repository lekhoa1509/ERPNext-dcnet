# How To: Update Supplier Quotation Child Remove Item

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test update supplier quotation child remove item

## Prerequisites

**Required Modules:**
- `json`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.buying.doctype.supplier_quotation.supplier_quotation`
- `erpnext.controllers.accounts_controller`


## Step-by-Step Guide

### Step 1: Assign sq = frappe.copy_doc(...)

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0])
```

### Step 2: Call sq.submit()

```python
sq.submit()
```

### Step 3: Assign po = make_purchase_order(...)

```python
po = make_purchase_order(sq.name)
```

### Step 4: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}, {'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
```

### Step 5: Assign unknown.schedule_date = add_days(...)

```python
po.get('items')[0].schedule_date = add_days(today(), 1)
```

### Step 6: Call update_child_qty_rate()

```python
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
```

### Step 7: Call po.submit()

```python
po.submit()
```

### Step 8: Call sq.reload()

```python
sq.reload()
```

### Step 9: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
```

### Step 10: Call frappe.db.savepoint()

```python
frappe.db.savepoint('before_cancel')
```

### Step 11: Call self.assertRaises()

```python
self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)
```

### Step 12: Call frappe.db.rollback()

```python
frappe.db.rollback(save_point='before_cancel')
```

### Step 13: Assign trans_item = json.dumps(...)

```python
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}])
```

### Step 14: Call update_child_qty_rate()

```python
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
```

### Step 15: Call sq.reload()

```python
sq.reload()
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(len(sq.get('items')), 1)
```


## Complete Example

```python
# Workflow
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0])
sq.submit()
po = make_purchase_order(sq.name)
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}, {'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
po.get('items')[0].schedule_date = add_days(today(), 1)
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
po.submit()
sq.reload()
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
frappe.db.savepoint('before_cancel')
self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)
frappe.db.rollback(save_point='before_cancel')
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}])
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
sq.reload()
self.assertEqual(len(sq.get('items')), 1)
```

## Next Steps


---

*Source: test_supplier_quotation.py:54 | Complexity: Advanced | Last updated: 2026-02-04*