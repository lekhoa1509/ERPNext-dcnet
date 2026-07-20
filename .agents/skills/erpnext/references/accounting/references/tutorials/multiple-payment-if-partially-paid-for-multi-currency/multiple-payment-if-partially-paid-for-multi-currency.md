# How To: Multiple Payment If Partially Paid For Multi Currency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test multiple payment if partially paid for multi currency

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

### Step 1: Assign pi = make_purchase_invoice(...)

```python
pi = make_purchase_invoice(currency='USD', conversion_rate=50, qty=1, rate=100, do_not_save=1)
```

### Step 2: Assign pi.credit_to = 'Creditors - _TC'

```python
pi.credit_to = 'Creditors - _TC'
```

### Step 3: Call pi.submit()

```python
pi.submit()
```

### Step 4: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 100)
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 5000)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pr.currency, 'USD')
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pr.party_account_currency, 'INR')
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Initiated')
```

### Step 10: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(frappe.exceptions.ValidationError, re.compile('Payment Request is already created'), make_payment_request, dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
```

### Step 11: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry(submit=False)
```

### Step 12: Assign pe.paid_amount = 2000

```python
pe.paid_amount = 2000
```

### Step 13: Assign unknown.allocated_amount = 2000

```python
pe.references[0].allocated_amount = 2000
```

### Step 14: Call pe.submit()

```python
pe.submit()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_request, pr.name)
```

### Step 16: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Partially Paid')
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 3000)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 100)
```

### Step 20: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry()
```

### Step 21: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 3000)
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].allocated_amount, 3000)
```

### Step 23: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].outstanding_amount, 0)
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_request, pr.name)
```

### Step 25: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Paid')
```

### Step 27: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 0)
```

### Step 28: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 100)
```

### Step 29: Call self.assertRaisesRegex()

```python
self.assertRaisesRegex(frappe.exceptions.ValidationError, re.compile('Payment Entry is already created'), make_payment_request, dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
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
pi = make_purchase_invoice(currency='USD', conversion_rate=50, qty=1, rate=100, do_not_save=1)
pi.credit_to = 'Creditors - _TC'
pi.submit()
pr = make_payment_request(dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
self.assertEqual(pr.grand_total, 100)
self.assertEqual(pr.outstanding_amount, 5000)
self.assertEqual(pr.currency, 'USD')
self.assertEqual(pr.party_account_currency, 'INR')
self.assertEqual(pr.status, 'Initiated')
self.assertRaisesRegex(frappe.exceptions.ValidationError, re.compile('Payment Request is already created'), make_payment_request, dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
pe = pr.create_payment_entry(submit=False)
pe.paid_amount = 2000
pe.references[0].allocated_amount = 2000
pe.submit()
self.assertEqual(pe.references[0].payment_request, pr.name)
pr.load_from_db()
self.assertEqual(pr.status, 'Partially Paid')
self.assertEqual(pr.outstanding_amount, 3000)
self.assertEqual(pr.grand_total, 100)
pe = pr.create_payment_entry()
self.assertEqual(pe.paid_amount, 3000)
self.assertEqual(pe.references[0].allocated_amount, 3000)
self.assertEqual(pe.references[0].outstanding_amount, 0)
self.assertEqual(pe.references[0].payment_request, pr.name)
pr.load_from_db()
self.assertEqual(pr.status, 'Paid')
self.assertEqual(pr.outstanding_amount, 0)
self.assertEqual(pr.grand_total, 100)
self.assertRaisesRegex(frappe.exceptions.ValidationError, re.compile('Payment Entry is already created'), make_payment_request, dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)
```

## Next Steps


---

*Source: test_payment_request.py:507 | Complexity: Advanced | Last updated: 2026-02-03*