# How To: 01 Receivable Summary Output

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: Test for Invoices, Paid, Advance and Outstanding

## Prerequisites

**Required Modules:**
- `frappe`
- `frappe.tests`
- `frappe.utils`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.accounts.report.accounts_receivable_summary.accounts_receivable_summary`
- `erpnext.accounts.test.accounts_mixin`


## Step-by-Step Guide

### Step 1: '\n\t\tTest for Invoices, Paid, Advance and Outstanding\n\t\t'

```python
'\n\t\tTest for Invoices, Paid, Advance and Outstanding\n\t\t'
```

### Step 2: Assign filters = value

```python
filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
```

### Step 3: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
```

### Step 4: Assign unknown = value

```python
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
```

### Step 5: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 6: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 7: Assign expected_data = value

```python
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'invoiced': 200.0, 'paid': 0.0, 'credit_note': 0.0, 'outstanding': 200.0, 'range1': 200.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 200.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 9: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```

### Step 10: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si.doctype, si.name)
```

### Step 11: Assign pe.paid_amount = 50

```python
pe.paid_amount = 50
```

### Step 12: Assign unknown.allocated_amount = 0

```python
pe.references[0].allocated_amount = 0
```

### Step 13: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 14: Call expected_data.update()

```python
expected_data.update({'advance': 50.0, 'outstanding': 150.0, 'range1': 150.0, 'total_due': 150.0})
```

### Step 15: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 16: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 18: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```

### Step 19: Assign pe = get_payment_entry(...)

```python
pe = get_payment_entry(si.doctype, si.name)
```

### Step 20: Assign pe.paid_amount = 125

```python
pe.paid_amount = 125
```

### Step 21: Assign unknown.allocated_amount = 125

```python
pe.references[0].allocated_amount = 125
```

### Step 22: Call pe.save.submit()

```python
pe.save().submit()
```

### Step 23: Call expected_data.update()

```python
expected_data.update({'advance': 50.0, 'paid': 125.0, 'outstanding': 25.0, 'range1': 25.0, 'total_due': 25.0})
```

### Step 24: Assign report = execute(...)

```python
report = execute(filters)
```

### Step 25: Assign rpt_output = value

```python
rpt_output = report[1]
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(len(rpt_output), 1)
```

### Step 27: Call self.assertDictEqual()

```python
self.assertDictEqual(rpt_output[0], expected_data)
```


## Complete Example

```python
# Workflow
'\n\t\tTest for Invoices, Paid, Advance and Outstanding\n\t\t'
filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
report = execute(filters)
rpt_output = report[1]
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'invoiced': 200.0, 'paid': 0.0, 'credit_note': 0.0, 'outstanding': 200.0, 'range1': 200.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 200.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
pe = get_payment_entry(si.doctype, si.name)
pe.paid_amount = 50
pe.references[0].allocated_amount = 0
pe.save().submit()
expected_data.update({'advance': 50.0, 'outstanding': 150.0, 'range1': 150.0, 'total_due': 150.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
pe = get_payment_entry(si.doctype, si.name)
pe.paid_amount = 125
pe.references[0].allocated_amount = 125
pe.save().submit()
expected_data.update({'advance': 50.0, 'paid': 125.0, 'outstanding': 25.0, 'range1': 25.0, 'total_due': 25.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
```

## Next Steps


---

*Source: test_accounts_receivable_summary.py:22 | Complexity: Advanced | Last updated: 2026-02-03*