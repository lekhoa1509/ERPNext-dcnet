# How To: Single Payment With Payment Term For Multi Currency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test single payment with payment term for multi currency

## Prerequisites

- [ ] Setup code must be executed first

**Required Modules:**
- `re`
- `unittest.mock`
- `frappe`
- `frappe.tests`
- `erpnext.accounts.doctype.payment_entry.payment_entry`
- `erpnext.accounts.doctype.payment_entry.test_payment_entry`
- `erpnext.accounts.doctype.payment_request.payment_request`
- `erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice`
- `erpnext.accounts.doctype.sales_invoice.test_sales_invoice`
- `erpnext.buying.doctype.purchase_order.test_purchase_order`
- `erpnext.selling.doctype.sales_order.test_sales_order`
- `erpnext.setup.utils`
- `erpnext.accounts.doctype.journal_entry.test_journal_entry`

**Setup Required:**
```python
for payment_gateway in payment_gateways:
    if not frappe.db.get_value('Payment Gateway', payment_gateway['gateway'], 'name'):
        frappe.get_doc(payment_gateway).insert(ignore_permissions=True)
for method in payment_method:
    if not frappe.db.get_value('Payment Gateway Account', {'payment_gateway': method['payment_gateway'], 'currency': method['currency'], 'company': method['company']}, 'name'):
        frappe.get_doc(method).insert(ignore_permissions=True)
send_email = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.send_email', return_value=None)
self.send_email = send_email.start()
self.addCleanup(send_email.stop)
get_payment_url = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.get_payment_url', return_value=PAYMENT_URL)
self.get_payment_url = get_payment_url.start()
self.addCleanup(get_payment_url.stop)
_get_payment_gateway_controller = patch('erpnext.accounts.doctype.payment_request.payment_request._get_payment_gateway_controller')
self._get_payment_gateway_controller = _get_payment_gateway_controller.start()
self.addCleanup(_get_payment_gateway_controller.stop)
```

## Step-by-Step Guide

### Step 1: Call create_payment_terms_template()

```python
create_payment_terms_template()
```

### Step 2: Assign si = create_sales_invoice(...)

```python
si = create_sales_invoice(do_not_save=1, currency='USD', debit_to='Debtors - _TC', qty=1, rate=200, conversion_rate=50)
```

### Step 3: Assign si.payment_terms_template = 'Test Receivable Template'

```python
si.payment_terms_template = 'Test Receivable Template'
```

### Step 4: Call si.save()

```python
si.save()
```

### Step 5: Call si.submit()

```python
si.submit()
```

### Step 6: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Invoice', dn=si.name, mute_email=1, submit_doc=1, return_doc=1)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 200)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 10000)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pr.currency, 'USD')
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pr.party_account_currency, 'INR')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Requested')
```

### Step 12: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(len(pe.references), 2)
```

### Step 14: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 10000)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].allocated_amount, 8474.5)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_request, pr.name)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pe.references[1].allocated_amount, 1525.5)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pe.references[1].payment_request, pr.name)
```

### Step 19: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Paid')
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 0)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 200)
```


## Complete Example

```python
# Setup
for payment_gateway in payment_gateways:
    if not frappe.db.get_value('Payment Gateway', payment_gateway['gateway'], 'name'):
        frappe.get_doc(payment_gateway).insert(ignore_permissions=True)
for method in payment_method:
    if not frappe.db.get_value('Payment Gateway Account', {'payment_gateway': method['payment_gateway'], 'currency': method['currency'], 'company': method['company']}, 'name'):
        frappe.get_doc(method).insert(ignore_permissions=True)
send_email = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.send_email', return_value=None)
self.send_email = send_email.start()
self.addCleanup(send_email.stop)
get_payment_url = patch('erpnext.accounts.doctype.payment_request.payment_request.PaymentRequest.get_payment_url', return_value=PAYMENT_URL)
self.get_payment_url = get_payment_url.start()
self.addCleanup(get_payment_url.stop)
_get_payment_gateway_controller = patch('erpnext.accounts.doctype.payment_request.payment_request._get_payment_gateway_controller')
self._get_payment_gateway_controller = _get_payment_gateway_controller.start()
self.addCleanup(_get_payment_gateway_controller.stop)

# Workflow
create_payment_terms_template()
si = create_sales_invoice(do_not_save=1, currency='USD', debit_to='Debtors - _TC', qty=1, rate=200, conversion_rate=50)
si.payment_terms_template = 'Test Receivable Template'
si.save()
si.submit()
pr = make_payment_request(dt='Sales Invoice', dn=si.name, mute_email=1, submit_doc=1, return_doc=1)
self.assertEqual(pr.grand_total, 200)
self.assertEqual(pr.outstanding_amount, 10000)
self.assertEqual(pr.currency, 'USD')
self.assertEqual(pr.party_account_currency, 'INR')
self.assertEqual(pr.status, 'Requested')
pe = pr.create_payment_entry()
self.assertEqual(len(pe.references), 2)
self.assertEqual(pe.paid_amount, 10000)
self.assertEqual(pe.references[0].allocated_amount, 8474.5)
self.assertEqual(pe.references[0].payment_request, pr.name)
self.assertEqual(pe.references[1].allocated_amount, 1525.5)
self.assertEqual(pe.references[1].payment_request, pr.name)
pr.load_from_db()
self.assertEqual(pr.status, 'Paid')
self.assertEqual(pr.outstanding_amount, 0)
self.assertEqual(pr.grand_total, 200)
```

## Next Steps


---

*Source: test_payment_request.py:625 | Complexity: Advanced | Last updated: 2026-02-03*