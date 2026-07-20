# How To: Bundled Delivery Note With Different Warehouses

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test Delivery Note with bundled item. Packed Item from the bundle having different warehouses

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.sales_invoice.sales_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.gross_profit.gross_profit`
- `erpnext.stock.doctype.delivery_note.delivery_note`
- `erpnext.stock.doctype.delivery_note.test_delivery_note`
- `erpnext.stock.doctype.item.test_item`
- `erpnext.stock.doctype.stock_entry.stock_entry_utils`
- `erpnext.selling.doctype.product_bundle.test_product_bundle`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.selling.doctype.sales_order.sales_order`


## Step-by-Step Guide

### Step 1: '\n\t\tTest Delivery Note with bundled item. Packed Item from the bundle having different warehouses\n\t\t'

```python
'\n\t\tTest Delivery Note with bundled item. Packed Item from the bundle having different warehouses\n\t\t'
```

### Step 2: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=1, basic_rate=100, do_not_submit=True)
```

### Step 3: Assign item = value

```python
item = se.items[0]
```

### Step 4: Call se.append()

```python
se.append('items', {'item_code': self.item2, 's_warehouse': '', 't_warehouse': self.finished_warehouse, 'qty': 1, 'basic_rate': 100, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
```

### Step 5: Assign se = se.save.submit(...)

```python
se = se.save().submit()
```

### Step 6: Assign dnote = self.create_delivery_note(...)

```python
dnote = self.create_delivery_note(item=self.bundle, qty=1, rate=200, do_not_submit=True)
```

### Step 7: Assign unknown.warehouse = value

```python
dnote.packed_items[1].warehouse = self.finished_warehouse
```

### Step 8: Assign dnote = dnote.submit(...)

```python
dnote = dnote.submit()
```

### Step 9: Assign sinv = make_sales_invoice(...)

```python
sinv = make_sales_invoice(dnote.name)
```

### Step 10: Assign sinv = sinv.save.submit(...)

```python
sinv = sinv.save().submit()
```

### Step 11: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice', sales_invoice=sinv.name)
```

### Step 12: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 13: Call self.assertGreater()

```python
self.assertGreater(len(data), 0)
```


## Complete Example

```python
# Workflow
'\n\t\tTest Delivery Note with bundled item. Packed Item from the bundle having different warehouses\n\t\t'
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=1, basic_rate=100, do_not_submit=True)
item = se.items[0]
se.append('items', {'item_code': self.item2, 's_warehouse': '', 't_warehouse': self.finished_warehouse, 'qty': 1, 'basic_rate': 100, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
se = se.save().submit()
dnote = self.create_delivery_note(item=self.bundle, qty=1, rate=200, do_not_submit=True)
dnote.packed_items[1].warehouse = self.finished_warehouse
dnote = dnote.submit()
sinv = make_sales_invoice(dnote.name)
sinv = sinv.save().submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice', sales_invoice=sinv.name)
columns, data = execute(filters=filters)
self.assertGreater(len(data), 0)
```

## Next Steps


---

*Source: test_gross_profit.py:262 | Complexity: Advanced | Last updated: 2026-02-03*