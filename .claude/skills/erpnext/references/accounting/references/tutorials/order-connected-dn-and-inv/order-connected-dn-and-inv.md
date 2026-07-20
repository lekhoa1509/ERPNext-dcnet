# How To: Order Connected Dn And Inv

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test order connected dn and inv

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

### Step 1: "\n\t\t\tTest gp calculation when invoice and delivery note aren't directly connected.\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"

```python
"\n\t\t\tTest gp calculation when invoice and delivery note aren't directly connected.\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"
```

### Step 2: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=3, basic_rate=100, do_not_submit=True)
```

### Step 3: Assign item = value

```python
item = se.items[0]
```

### Step 4: Call se.append()

```python
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 10, 'basic_rate': 200, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
```

### Step 5: Assign se = se.save.submit(...)

```python
se = se.save().submit()
```

### Step 6: Assign so = make_sales_order(...)

```python
so = make_sales_order(customer=self.customer, company=self.company, warehouse=self.warehouse, item=self.item, qty=4, do_not_save=False, do_not_submit=False)
```

### Step 7: Call make_delivery_note.submit()

```python
make_delivery_note(so.name).submit()
```

### Step 8: Assign sinv = make_sales_invoice.submit(...)

```python
sinv = make_sales_invoice(so.name).submit()
```

### Step 9: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
```

### Step 10: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 11: Assign expected_entry = value

```python
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 4.0, 'avg._selling_rate': 100.0, 'valuation_rate': 125.0, 'selling_amount': 400.0, 'buying_amount': 500.0, 'gross_profit': -100.0, 'gross_profit_%': -25.0}
```

### Step 12: Assign gp_entry = value

```python
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
```

### Step 13: Assign report_output = value

```python
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(report_output, expected_entry)
```


## Complete Example

```python
# Workflow
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
"\n\t\t\tTest gp calculation when invoice and delivery note aren't directly connected.\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=3, basic_rate=100, do_not_submit=True)
item = se.items[0]
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 10, 'basic_rate': 200, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
se = se.save().submit()
so = make_sales_order(customer=self.customer, company=self.company, warehouse=self.warehouse, item=self.item, qty=4, do_not_save=False, do_not_submit=False)
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
make_delivery_note(so.name).submit()
sinv = make_sales_invoice(so.name).submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
columns, data = execute(filters=filters)
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 4.0, 'avg._selling_rate': 100.0, 'valuation_rate': 125.0, 'selling_amount': 400.0, 'buying_amount': 500.0, 'gross_profit': -100.0, 'gross_profit_%': -25.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
```

## Next Steps


---

*Source: test_gross_profit.py:314 | Complexity: Advanced | Last updated: 2026-02-03*