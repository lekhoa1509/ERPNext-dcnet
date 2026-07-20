# How To: Different Rates In Si And Dn

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test different rates in si and dn

## Prerequisites

- [ ] Setup code must be executed first

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

**Setup Required:**
```python
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()
```

## Step-by-Step Guide

### Step 1: "\n\t\t\tTest gp calculation when invoice and delivery note differ in qty and aren't connected\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"

```python
"\n\t\t\tTest gp calculation when invoice and delivery note differ in qty and aren't connected\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"
```

### Step 2: Assign se = make_stock_entry(...)

```python
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=3, basic_rate=700, do_not_submit=True)
```

### Step 3: Assign item = value

```python
item = se.items[0]
```

### Step 4: Call se.append()

```python
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 10, 'basic_rate': 700, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
```

### Step 5: Assign se = se.save.submit(...)

```python
se = se.save().submit()
```

### Step 6: Assign so = make_sales_order(...)

```python
so = make_sales_order(customer=self.customer, company=self.company, warehouse=self.warehouse, item=self.item, rate=800, qty=10, do_not_save=False, do_not_submit=False)
```

### Step 7: Assign dn1 = make_delivery_note(...)

```python
dn1 = make_delivery_note(so.name)
```

### Step 8: Assign unknown.qty = 4

```python
dn1.items[0].qty = 4
```

### Step 9: Assign unknown.rate = 800

```python
dn1.items[0].rate = 800
```

### Step 10: Call dn1.save.submit()

```python
dn1.save().submit()
```

### Step 11: Assign dn2 = make_delivery_note(...)

```python
dn2 = make_delivery_note(so.name)
```

### Step 12: Assign unknown.qty = 6

```python
dn2.items[0].qty = 6
```

### Step 13: Assign unknown.rate = 800

```python
dn2.items[0].rate = 800
```

### Step 14: Call dn2.save.submit()

```python
dn2.save().submit()
```

### Step 15: Assign sinv = make_sales_invoice(...)

```python
sinv = make_sales_invoice(so.name)
```

### Step 16: Assign unknown.qty = 4

```python
sinv.items[0].qty = 4
```

### Step 17: Assign unknown.rate = 800

```python
sinv.items[0].rate = 800
```

### Step 18: Call sinv.save.submit()

```python
sinv.save().submit()
```

### Step 19: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
```

### Step 20: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 21: Assign expected_entry = value

```python
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 4.0, 'avg._selling_rate': 800.0, 'valuation_rate': 700.0, 'selling_amount': 3200.0, 'buying_amount': 2800.0, 'gross_profit': 400.0, 'gross_profit_%': 12.5}
```

### Step 22: Assign gp_entry = value

```python
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
```

### Step 23: Assign report_output = value

```python
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(report_output, expected_entry)
```


## Complete Example

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

# Workflow
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
"\n\t\t\tTest gp calculation when invoice and delivery note differ in qty and aren't connected\n\t\t\tSO -- INV\n\t\t\t|\n\t\t\tDN\n\t\t"
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=3, basic_rate=700, do_not_submit=True)
item = se.items[0]
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 10, 'basic_rate': 700, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
se = se.save().submit()
so = make_sales_order(customer=self.customer, company=self.company, warehouse=self.warehouse, item=self.item, rate=800, qty=10, do_not_save=False, do_not_submit=False)
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
dn1 = make_delivery_note(so.name)
dn1.items[0].qty = 4
dn1.items[0].rate = 800
dn1.save().submit()
dn2 = make_delivery_note(so.name)
dn2.items[0].qty = 6
dn2.items[0].rate = 800
dn2.save().submit()
sinv = make_sales_invoice(so.name)
sinv.items[0].qty = 4
sinv.items[0].rate = 800
sinv.save().submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
columns, data = execute(filters=filters)
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 4.0, 'avg._selling_rate': 800.0, 'valuation_rate': 700.0, 'selling_amount': 3200.0, 'buying_amount': 2800.0, 'gross_profit': 400.0, 'gross_profit_%': 12.5}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
```

## Next Steps


---

*Source: test_gross_profit.py:479 | Complexity: Advanced | Last updated: 2026-02-03*