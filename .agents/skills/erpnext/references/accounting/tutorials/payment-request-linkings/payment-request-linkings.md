# How To: Payment Request Linkings

**Difficulty**: Advanced
**Estimated Time**: 20 minutes
**Tags**: workflow, integration

## Overview

Workflow: test payment request linkings

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

### Step 1: Assign so_inr = make_sales_order(...)

```python
so_inr = make_sales_order(currency='INR', do_not_save=True)
```

### Step 2: Assign so_inr.disable_rounded_total = 1

```python
so_inr.disable_rounded_total = 1
```

### Step 3: Call so_inr.save()

```python
so_inr.save()
```

### Step 4: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Order', dn=so_inr.name, recipient_id='saurabh@erpnext.com', payment_gateway_account='_Test Gateway - INR - _TC')
```

### Step 5: Call self.assertEqual()

```python
self.assertEqual(pr.reference_doctype, 'Sales Order')
```

### Step 6: Call self.assertEqual()

```python
self.assertEqual(pr.reference_name, so_inr.name)
```

### Step 7: Call self.assertEqual()

```python
self.assertEqual(pr.currency, 'INR')
```

### Step 8: Assign conversion_rate = get_exchange_rate(...)

```python
conversion_rate = get_exchange_rate('USD', 'INR')
```

### Step 9: Assign si_usd = create_sales_invoice(...)

```python
si_usd = create_sales_invoice(currency='USD', conversion_rate=conversion_rate)
```

### Step 10: Assign pr = make_payment_request(...)

```python
pr = make_payment_request(dt='Sales Invoice', dn=si_usd.name, recipient_id='saurabh@erpnext.com', payment_gateway_account='_Test Gateway - USD - _TC')
```

### Step 11: Call self.assertEqual()

```python
self.assertEqual(pr.reference_doctype, 'Sales Invoice')
```

### Step 12: Call self.assertEqual()

```python
self.assertEqual(pr.reference_name, si_usd.name)
```

### Step 13: Call self.assertEqual()

```python
self.assertEqual(pr.currency, 'USD')
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
so_inr = make_sales_order(currency='INR', do_not_save=True)
so_inr.disable_rounded_total = 1
so_inr.save()
pr = make_payment_request(dt='Sales Order', dn=so_inr.name, recipient_id='saurabh@erpnext.com', payment_gateway_account='_Test Gateway - INR - _TC')
self.assertEqual(pr.reference_doctype, 'Sales Order')
self.assertEqual(pr.reference_name, so_inr.name)
self.assertEqual(pr.currency, 'INR')
conversion_rate = get_exchange_rate('USD', 'INR')
si_usd = create_sales_invoice(currency='USD', conversion_rate=conversion_rate)
pr = make_payment_request(dt='Sales Invoice', dn=si_usd.name, recipient_id='saurabh@erpnext.com', payment_gateway_account='_Test Gateway - USD - _TC')
self.assertEqual(pr.reference_doctype, 'Sales Invoice')
self.assertEqual(pr.reference_name, si_usd.name)
self.assertEqual(pr.currency, 'USD')
```

## Next Steps


---

*Source: test_payment_request.py:104 | Complexity: Advanced | Last updated: 2026-02-03*