# How To: Invoice Without Only Delivery Note

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test buying amount for Invoice without `update_stock` flag set but has Delivery Note

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

### Step 1: '\n\t\tTest buying amount for Invoice without `update_stock` flag set but has Delivery Note\n\t\t'

```python
'\n\t\tTest buying amount for Invoice without `update_stock` flag set but has Delivery Note\n\t\t'
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
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 1, 'basic_rate': 200, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
```

### Step 5: Assign se = se.save.submit(...)

```python
se = se.save().submit()
```

### Step 6: Assign sinv = create_sales_invoice(...)

```python
sinv = create_sales_invoice(qty=1, rate=100, company=self.company, customer=self.customer, item_code=self.item, item_name=self.item, cost_center=self.cost_center, warehouse=self.warehouse, debit_to=self.debit_to, parent_cost_center=self.cost_center, update_stock=0, currency='INR', income_account=self.income_account, expense_account=self.expense_account)
```

### Step 7: Assign filters = frappe._dict(...)

```python
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
```

### Step 8: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 9: Assign expected_entry_without_dn = value

```python
expected_entry_without_dn = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 150.0, 'selling_amount': 100.0, 'buying_amount': 150.0, 'gross_profit': -50.0, 'gross_profit_%': -50.0}
```

### Step 10: Assign gp_entry = value

```python
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
```

### Step 11: Assign report_output = value

```python
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry_without_dn}
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(report_output, expected_entry_without_dn)
```

### Step 13: Assign dn = make_delivery_note(...)

```python
dn = make_delivery_note(sinv.name)
```

### Step 14: Assign unknown.qty = 1

```python
dn.items[0].qty = 1
```

### Step 15: Assign dn = dn.save.submit(...)

```python
dn = dn.save().submit()
```

### Step 16: Assign unknown = execute(...)

```python
columns, data = execute(filters=filters)
```

### Step 17: Assign expected_entry_with_dn = value

```python
expected_entry_with_dn = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 100.0, 'selling_amount': 100.0, 'buying_amount': 100.0, 'gross_profit': 0.0, 'gross_profit_%': 0.0}
```

### Step 18: Assign gp_entry = value

```python
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
```

### Step 19: Assign report_output = value

```python
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry_with_dn}
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(report_output, expected_entry_with_dn)
```


## Complete Example

```python
# Workflow
'\n\t\tTest buying amount for Invoice without `update_stock` flag set but has Delivery Note\n\t\t'
se = make_stock_entry(company=self.company, item_code=self.item, target=self.warehouse, qty=1, basic_rate=100, do_not_submit=True)
item = se.items[0]
se.append('items', {'item_code': item.item_code, 's_warehouse': item.s_warehouse, 't_warehouse': item.t_warehouse, 'qty': 1, 'basic_rate': 200, 'conversion_factor': item.conversion_factor or 1.0, 'transfer_qty': flt(item.qty) * (flt(item.conversion_factor) or 1.0), 'serial_no': item.serial_no, 'batch_no': item.batch_no, 'cost_center': item.cost_center, 'expense_account': item.expense_account})
se = se.save().submit()
sinv = create_sales_invoice(qty=1, rate=100, company=self.company, customer=self.customer, item_code=self.item, item_name=self.item, cost_center=self.cost_center, warehouse=self.warehouse, debit_to=self.debit_to, parent_cost_center=self.cost_center, update_stock=0, currency='INR', income_account=self.income_account, expense_account=self.expense_account)
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
columns, data = execute(filters=filters)
expected_entry_without_dn = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 150.0, 'selling_amount': 100.0, 'buying_amount': 150.0, 'gross_profit': -50.0, 'gross_profit_%': -50.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry_without_dn}
self.assertEqual(report_output, expected_entry_without_dn)
dn = make_delivery_note(sinv.name)
dn.items[0].qty = 1
dn = dn.save().submit()
columns, data = execute(filters=filters)
expected_entry_with_dn = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 100.0, 'selling_amount': 100.0, 'buying_amount': 100.0, 'gross_profit': 0.0, 'gross_profit_%': 0.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry_with_dn}
self.assertEqual(report_output, expected_entry_with_dn)
```

## Next Steps


---

*Source: test_gross_profit.py:157 | Complexity: Advanced | Last updated: 2026-02-03*