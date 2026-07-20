# How To: Multiple Dn Creation

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple dn creation

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.packed_item.test_packed_item`
- `erpnext.stock.doctype.pick_list.pick_list`
- `erpnext.stock.doctype.purchase_receipt.test_purchase_receipt`
- `erpnext.stock.doctype.serial_and_batch_bundle.test_serial_and_batch_bundle`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.stock.doctype.stock_reconciliation.stock_reconciliation`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.stock.doctype.pick_list.pick_list`
- `json`
- `frappe.model.mapper`


## Step-by-Step Guide

### Step 1: Assign sales_order_1 = frappe.get_doc.insert(...)

```python
sales_order_1 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': '_Test Item', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
```

### Step 2: Call sales_order_1.submit()

```python
sales_order_1.submit()
```

### Step 3: Assign sales_order_2 = frappe.get_doc.insert(...)

```python
sales_order_2 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer 1', 'company': '_Test Company', 'items': [{'item_code': '_Test Item 2', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
```

### Step 4: Call sales_order_2.submit()

```python
sales_order_2.submit()
```

### Step 5: Assign pick_list = frappe.get_doc(...)

```python
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'customer': '_Test Customer', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_1.name, 'sales_order_item': sales_order_1.items[0].name}, {'item_code': '_Test Item 2', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_2.name, 'sales_order_item': sales_order_2.items[0].name}]})
```

### Step 6: Call pick_list.set_item_locations()

```python
pick_list.set_item_locations()
```

### Step 7: Call pick_list.submit()

```python
pick_list.submit()
```

### Step 8: Call create_delivery_note()

```python
create_delivery_note(pick_list.name)
```

### Step 9: Assign pick_list_1 = frappe.get_doc(...)

```python
pick_list_1 = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Delivery', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}, {'item_code': '_Test Item 2', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
```

### Step 10: Call pick_list_1.set_item_locations()

```python
pick_list_1.set_item_locations()
```

### Step 11: Call pick_list_1.submit()

```python
pick_list_1.submit()
```

### Step 12: Call create_delivery_note()

```python
create_delivery_note(pick_list_1.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(dn_item.item_code, '_Test Item')
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(dn_item.against_sales_order, sales_order_1.name)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(dn_item.against_pick_list, pick_list.name)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(dn_item.pick_list_item, pick_list.locations[0].name)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(dn_item.item_code, '_Test Item 2')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(dn_item.against_sales_order, sales_order_2.name)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(dn_item.against_pick_list, pick_list.name)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(dn_item.pick_list_item, pick_list.locations[1].name)
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(dn_item.qty, 1)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(dn_item.qty, 2)
```


## Complete Example

```python
# Workflow
sales_order_1 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': '_Test Item', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
sales_order_1.submit()
sales_order_2 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer 1', 'company': '_Test Company', 'items': [{'item_code': '_Test Item 2', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
sales_order_2.submit()
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'customer': '_Test Customer', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_1.name, 'sales_order_item': sales_order_1.items[0].name}, {'item_code': '_Test Item 2', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_2.name, 'sales_order_item': sales_order_2.items[0].name}]})
pick_list.set_item_locations()
pick_list.submit()
create_delivery_note(pick_list.name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list.name, 'customer': '_Test Customer'}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        self.assertEqual(dn_item.item_code, '_Test Item')
        self.assertEqual(dn_item.against_sales_order, sales_order_1.name)
        self.assertEqual(dn_item.against_pick_list, pick_list.name)
        self.assertEqual(dn_item.pick_list_item, pick_list.locations[0].name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list.name, 'customer': '_Test Customer 1'}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        self.assertEqual(dn_item.item_code, '_Test Item 2')
        self.assertEqual(dn_item.against_sales_order, sales_order_2.name)
        self.assertEqual(dn_item.against_pick_list, pick_list.name)
        self.assertEqual(dn_item.pick_list_item, pick_list.locations[1].name)
pick_list_1 = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Delivery', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}, {'item_code': '_Test Item 2', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
pick_list_1.set_item_locations()
pick_list_1.submit()
create_delivery_note(pick_list_1.name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list_1.name}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        if dn_item.item_code == '_Test Item':
            self.assertEqual(dn_item.qty, 1)
        if dn_item.item_code == '_Test Item 2':
            self.assertEqual(dn_item.qty, 2)
```

## Next Steps


---

*Source: test_pick_list.py:530 | Complexity: Advanced | Last updated: 2026-02-04*