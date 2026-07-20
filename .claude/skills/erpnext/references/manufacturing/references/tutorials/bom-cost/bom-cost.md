# How To: Bom Cost

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test bom cost

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `erpnext.manufacturing.doctype.bom_update_log.test_bom_update_log`
- `erpnext.manufacturing.doctype.bom_update_tool.bom_update_tool`
- `erpnext.manufacturing.doctype.production_plan.test_production_plan`
- `erpnext.stock.doctype.item.test_item`


## Step-by-Step Guide

### Step 1: Assign bom_no = frappe.db.get_value(...)

```python
bom_no = frappe.db.get_value('BOM', {'item': 'BOM Cost Test Item 1'}, 'name')
```

### Step 2: Call self.assertEqual()

```python
self.assertEqual(doc.total_cost, 200)
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 200)
```

### Step 4: Call update_cost_in_all_boms_in_test()

```python
update_cost_in_all_boms_in_test()
```

### Step 5: Call doc.load_from_db()

```python
doc.load_from_db()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(doc.total_cost, 300)
```

### Step 7: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 100)
```

### Step 8: Call update_cost_in_all_boms_in_test()

```python
update_cost_in_all_boms_in_test()
```

### Step 9: Call doc.load_from_db()

```python
doc.load_from_db()
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(doc.total_cost, 200)
```

### Step 11: Assign item_doc = create_item(...)

```python
item_doc = create_item(item, valuation_rate=100)
```

### Step 12: Assign doc = make_bom(...)

```python
doc = make_bom(item='BOM Cost Test Item 1', raw_materials=['BOM Cost Test Item 2', 'BOM Cost Test Item 3'], currency='INR')
```

### Step 13: Assign doc = frappe.get_doc(...)

```python
doc = frappe.get_doc('BOM', bom_no)
```

### Step 14: Call frappe.db.set_value()

```python
frappe.db.set_value('Item', item_doc.name, 'valuation_rate', 100)
```


## Complete Example

```python
# Workflow
for item in ['BOM Cost Test Item 1', 'BOM Cost Test Item 2', 'BOM Cost Test Item 3']:
    item_doc = create_item(item, valuation_rate=100)
    if item_doc.valuation_rate != 100.0:
        frappe.db.set_value('Item', item_doc.name, 'valuation_rate', 100)
bom_no = frappe.db.get_value('BOM', {'item': 'BOM Cost Test Item 1'}, 'name')
if not bom_no:
    doc = make_bom(item='BOM Cost Test Item 1', raw_materials=['BOM Cost Test Item 2', 'BOM Cost Test Item 3'], currency='INR')
else:
    doc = frappe.get_doc('BOM', bom_no)
self.assertEqual(doc.total_cost, 200)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 200)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 300)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 100)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 200)
```

## Next Steps


---

*Source: test_bom_update_tool.py:38 | Complexity: Advanced | Last updated: 2026-02-04*