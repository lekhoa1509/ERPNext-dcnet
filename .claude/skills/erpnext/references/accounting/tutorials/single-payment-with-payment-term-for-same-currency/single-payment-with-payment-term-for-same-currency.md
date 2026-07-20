# How To: Single Payment With Payment Term For Same Currency

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test single payment with payment term for same currency

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

### Step 2: Assign po = create_purchase_order(...)

```python
po = create_purchase_order(do_not_save=1, currency='INR', qty=1, rate=20000)
```

### Step 3: Assign po.payment_terms_template = 'Test Receivable Template'

```python
po.payment_terms_template = 'Test Receivable Template'
```

### Step 4: Call po.save()

```python
po.save()
```

### Step 5: Call po.submit()

```python
po.submit()
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(po.advance_payment_status, 'Not Initiated')
```

### Step 7: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Purchase Order', dn=po.name, mute_email=1, submit_doc=1, return_doc=1)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 20000)
```

### Step 9: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, pr.grand_total)
```

### Step 10: Call self.assertEqual()

```python
self.assertEqual(pr.party_account_currency, pr.currency)
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Initiated')
```

### Step 12: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(po.advance_payment_status, 'Initiated')
```

### Step 14: Assign pe = pr.create_payment_entry(...)

```python
pe = pr.create_payment_entry()
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(len(pe.references), 2)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(pe.paid_amount, 20000)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].allocated_amount, 16949.2)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(pe.references[0].payment_request, pr.name)
```

### Step 19: Call self.assertEqual()

```python
self.assertEqual(pe.references[1].allocated_amount, 3050.8)
```

### Step 20: Call self.assertEqual()

```python
self.assertEqual(pe.references[1].payment_request, pr.name)
```

### Step 21: Call po.load_from_db()

```python
po.load_from_db()
```

### Step 22: Call self.assertEqual()

```python
self.assertEqual(po.advance_payment_status, 'Fully Paid')
```

### Step 23: Call pr.load_from_db()

```python
pr.load_from_db()
```

### Step 24: Call self.assertEqual()

```python
self.assertEqual(pr.status, 'Paid')
```

### Step 25: Call self.assertEqual()

```python
self.assertEqual(pr.outstanding_amount, 0)
```

### Step 26: Call self.assertEqual()

```python
self.assertEqual(pr.grand_total, 20000)
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
po = create_purchase_order(do_not_save=1, currency='INR', qty=1, rate=20000)
po.payment_terms_template = 'Test Receivable Template'
po.save()
po.submit()
self.assertEqual(po.advance_payment_status, 'Not Initiated')
pr = make_payment_request(dt='Purchase Order', dn=po.name, mute_email=1, submit_doc=1, return_doc=1)
self.assertEqual(pr.grand_total, 20000)
self.assertEqual(pr.outstanding_amount, pr.grand_total)
self.assertEqual(pr.party_account_currency, pr.currency)
self.assertEqual(pr.status, 'Initiated')
po.load_from_db()
self.assertEqual(po.advance_payment_status, 'Initiated')
pe = pr.create_payment_entry()
self.assertEqual(len(pe.references), 2)
self.assertEqual(pe.paid_amount, 20000)
self.assertEqual(pe.references[0].allocated_amount, 16949.2)
self.assertEqual(pe.references[0].payment_request, pr.name)
self.assertEqual(pe.references[1].allocated_amount, 3050.8)
self.assertEqual(pe.references[1].payment_request, pr.name)
po.load_from_db()
self.assertEqual(po.advance_payment_status, 'Fully Paid')
pr.load_from_db()
self.assertEqual(pr.status, 'Paid')
self.assertEqual(pr.outstanding_amount, 0)
self.assertEqual(pr.grand_total, 20000)
```

## Next Steps


---

*Source: test_payment_request.py:575 | Complexity: Advanced | Last updated: 2026-02-03*