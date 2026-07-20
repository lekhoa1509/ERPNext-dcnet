# How To: Party Item Code

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test party item code

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext`
- `erpnext.stock.doctype.item.test_item`
- `blanket_order`


## Step-by-Step Guide

### Step 1: Assign item_doc = make_item(...)

```python
item_doc = make_item('_Test Item 1 for Blanket Order')
```

### Step 2: Assign item_code = value

```python
item_code = item_doc.name
```

### Step 3: Assign customer = '_Test Customer'

```python
customer = '_Test Customer'
```

### Step 4: Assign supplier = '_Test Supplier'

```python
supplier = '_Test Supplier'
```

### Step 5: Assign bo = make_blanket_order(...)

```python
bo = make_blanket_order(blanket_order_type='Selling', customer=customer, item_code=item_code)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(bo.items[0].party_item_code, 'CUST-REF-1')
```

### Step 7: Assign bo = make_blanket_order(...)

```python
bo = make_blanket_order(blanket_order_type='Purchasing', supplier=supplier, item_code=item_code)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')
```

### Step 9: Call item_doc.append()

```python
item_doc.append('customer_items', {'customer_name': customer, 'ref_code': 'CUST-REF-1'})
```

### Step 10: Call item_doc.save()

```python
item_doc.save()
```

### Step 11: Call item_doc.append()

```python
item_doc.append('supplier_items', {'supplier': supplier, 'supplier_part_no': 'SUPP-PART-1'})
```

### Step 12: Call item_doc.save()

```python
item_doc.save()
```


## Complete Example

```python
# Workflow
item_doc = make_item('_Test Item 1 for Blanket Order')
item_code = item_doc.name
customer = '_Test Customer'
supplier = '_Test Supplier'
if not frappe.db.exists('Item Customer Detail', {'customer_name': customer, 'parent': item_code}):
    item_doc.append('customer_items', {'customer_name': customer, 'ref_code': 'CUST-REF-1'})
    item_doc.save()
if not frappe.db.exists('Item Supplier', {'supplier': supplier, 'parent': item_code}):
    item_doc.append('supplier_items', {'supplier': supplier, 'supplier_part_no': 'SUPP-PART-1'})
    item_doc.save()
bo = make_blanket_order(blanket_order_type='Selling', customer=customer, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'CUST-REF-1')
bo = make_blanket_order(blanket_order_type='Purchasing', supplier=supplier, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')
```

## Next Steps


---

*Source: test_blanket_order.py:94 | Complexity: Advanced | Last updated: 2026-02-04*