# How To: Payment Entry

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment entry

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

### Step 1: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'exchange_gain_loss_account', '_Test Exchange Gain/Loss - _TC')
```

### Step 2: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'write_off_account', '_Test Write Off - _TC')
```

### Step 3: Call frappe.db.set_value()

```python
frappe.db.set_value('Company', '_Test Company', 'cost_center', '_Test Cost Center - _TC')
```

### Step 4: Assign so_inr = make_sales_order(...)

```python
so_inr = make_sales_order(currency='INR')
```

### Step 5: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Order', dn=so_inr.name, recipient_id='saurabh@erpnext.com', mute_email=1, payment_gateway_account='_Test Gateway - INR - _TC', submit_doc=1, return_doc=1)
```

### Step 6: Assign pe = pr.set_as_paid(...)

```python
pe = pr.set_as_paid()
```

### Step 7: Assign so_inr = frappe.get_doc(...)

```python
so_inr = frappe.get_doc('Sales Order', so_inr.name)
```

### Step 8: Call self.assertEqual()

```python
self.assertEqual(so_inr.advance_paid, 1000)
```

### Step 9: Assign si_usd = create_sales_invoice(...)

```python
si_usd = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
```

### Step 10: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Invoice', dn=si_usd.name, recipient_id='saurabh@erpnext.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', submit_doc=1, return_doc=1)
```

### Step 11: Assign pe = pr.set_as_paid(...)

```python
pe = pr.set_as_paid()
```

### Step 12: Assign expected_gle = dict(...)

```python
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5000, si_usd.name], [pr.payment_account, 5000.0, 0, None]]))
```

### Step 13: Assign gl_entries = frappe.db.sql(...)

```python
gl_entries = frappe.db.sql("select account, debit, credit, against_voucher\n\t\t\tfrom `tabGL Entry` where voucher_type='Payment Entry' and voucher_no=%s\n\t\t\torder by account asc", pe.name, as_dict=1)
```

### Step 14: Call self.assertTrue()

```python
self.assertTrue(gl_entries)
```

### Step 15: Call self.assertEqual()

```python
self.assertEqual(expected_gle[gle.account][0], gle.account)
```

### Step 16: Call self.assertEqual()

```python
self.assertEqual(expected_gle[gle.account][1], gle.debit)
```

### Step 17: Call self.assertEqual()

```python
self.assertEqual(expected_gle[gle.account][2], gle.credit)
```

### Step 18: Call self.assertEqual()

```python
self.assertEqual(expected_gle[gle.account][3], gle.against_voucher)
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
frappe.db.set_value('Company', '_Test Company', 'exchange_gain_loss_account', '_Test Exchange Gain/Loss - _TC')
frappe.db.set_value('Company', '_Test Company', 'write_off_account', '_Test Write Off - _TC')
frappe.db.set_value('Company', '_Test Company', 'cost_center', '_Test Cost Center - _TC')
so_inr = make_sales_order(currency='INR')
pr = make_payment_request(dt='Sales Order', dn=so_inr.name, recipient_id='saurabh@erpnext.com', mute_email=1, payment_gateway_account='_Test Gateway - INR - _TC', submit_doc=1, return_doc=1)
pe = pr.set_as_paid()
so_inr = frappe.get_doc('Sales Order', so_inr.name)
self.assertEqual(so_inr.advance_paid, 1000)
si_usd = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
pr = make_payment_request(dt='Sales Invoice', dn=si_usd.name, recipient_id='saurabh@erpnext.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', submit_doc=1, return_doc=1)
pe = pr.set_as_paid()
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5000, si_usd.name], [pr.payment_account, 5000.0, 0, None]]))
gl_entries = frappe.db.sql("select account, debit, credit, against_voucher\n\t\t\tfrom `tabGL Entry` where voucher_type='Payment Entry' and voucher_no=%s\n\t\t\torder by account asc", pe.name, as_dict=1)
self.assertTrue(gl_entries)
for _i, gle in enumerate(gl_entries):
    self.assertEqual(expected_gle[gle.account][0], gle.account)
    self.assertEqual(expected_gle[gle.account][1], gle.debit)
    self.assertEqual(expected_gle[gle.account][2], gle.credit)
    self.assertEqual(expected_gle[gle.account][3], gle.against_voucher)
```

## Next Steps


---

*Source: test_payment_request.py:297 | Complexity: Advanced | Last updated: 2026-02-03*