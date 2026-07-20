# Test Example Extraction Report

**Total Examples**: 728  
**High Value Examples** (confidence > 0.7): 728  
**Average Complexity**: 0.65  

## Examples by Category

- **config**: 16
- **instantiation**: 148
- **method_call**: 164
- **workflow**: 400

## Examples by Language

- **Python**: 728

## Extracted Examples

### test_ignore_cr_dr_notes_filter

**Category**: workflow  
**Description**: Workflow: test ignore cr dr notes filter  
**Expected**: self.assertEqual(expected, actual)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

si = create_sales_invoice()
cr_note = make_return_doc(si.doctype, si.name)
cr_note.submit()
pr = frappe.get_doc('Payment Reconciliation')
pr.company = si.company
pr.party_type = 'Customer'
pr.party = si.customer
pr.receivable_payable_account = si.debit_to
pr.get_unreconciled_entries()
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
self.assertEqual(len(system_generated_journal), 1)
expected = set([si.name, cr_note.name, system_generated_journal[0].name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': False}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
expected = set([si.name, cr_note.name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': True}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:271*

### test_ignore_cr_dr_notes_filter

**Category**: workflow  
**Description**: Workflow: test ignore cr dr notes filter  
**Expected**: self.assertEqual(expected, actual)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice()
cr_note = make_return_doc(si.doctype, si.name)
cr_note.submit()
pr = frappe.get_doc('Payment Reconciliation')
pr.company = si.company
pr.party_type = 'Customer'
pr.party = si.customer
pr.receivable_payable_account = si.debit_to
pr.get_unreconciled_entries()
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
self.assertEqual(len(system_generated_journal), 1)
expected = set([si.name, cr_note.name, system_generated_journal[0].name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': False}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
expected = set([si.name, cr_note.name])
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'account': [si.debit_to], 'categorize_by': 'Categorize by Voucher (Consolidated)', 'ignore_cr_dr_notes': True}))
actual = set([x.voucher_no for x in data if x.voucher_no])
self.assertEqual(expected, actual)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:271*

### test_01_unreconcile_invoice

**Category**: workflow  
**Description**: Workflow: test 01 unreconcile invoice  
**Expected**: self.assertEqual(pe.unallocated_amount, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

si1 = self.create_sales_invoice()
si2 = self.create_sales_invoice()
pe = self.create_payment_entry()
pe.append('references', {'reference_doctype': si1.doctype, 'reference_name': si1.name, 'allocated_amount': 100})
pe.append('references', {'reference_doctype': si2.doctype, 'reference_name': si2.name, 'allocated_amount': 100})
pe.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 0)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(pe.unallocated_amount, 0)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([si1.name, si2.name], allocations)
for x in unreconcile.allocations:
    if x.reference_name != si1.name:
        unreconcile.remove(x)
unreconcile.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 100)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:67*

### test_05_unreconcile_order

**Category**: workflow  
**Description**: Workflow: test 05 unreconcile order  
**Expected**: self.assertEqual(so.advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

so = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 100
pe.append('references', {'reference_doctype': so.doctype, 'reference_name': so.name, 'allocated_amount': 100})
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([so.name], allocations)
unreconcile.save().submit()
so.reload()
pe.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(len(pe.references), 0)
self.assertEqual(pe.unallocated_amount, 100)
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:335*

### test_06_unreconcile_advance_from_payment_entry

**Category**: workflow  
**Description**: Workflow: test 06 unreconcile advance from payment entry  
**Expected**: self.assertEqual(pe.unallocated_amount, 110)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

self.enable_advance_as_liability()
so1 = self.create_sales_order()
so2 = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 260
pe.append('references', {'reference_doctype': so1.doctype, 'reference_name': so1.name, 'allocated_amount': 150})
pe.append('references', {'reference_doctype': so2.doctype, 'reference_name': so2.name, 'allocated_amount': 110})
pe.save().submit()
so1.reload()
self.assertEqual(so1.advance_paid, 150)
so2.reload()
self.assertEqual(so2.advance_paid, 110)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [(x.reference_name, x.allocated_amount) for x in unreconcile.allocations]
self.assertListEqual(allocations, [(so1.name, 150), (so2.name, 110)])
unreconcile.remove(unreconcile.allocations[0])
unreconcile.save().submit()
so1.reload()
so2.reload()
pe.reload()
self.assertEqual(so1.advance_paid, 150)
self.assertEqual(so2.advance_paid, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 110)
self.disable_advance_as_liability()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:377*

### test_unreconcile_advance_from_journal_entry

**Category**: workflow  
**Description**: Workflow: test unreconcile advance from journal entry  
**Expected**: self.assertEqual(po.advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

po = create_purchase_order(company=self.company, supplier=self.supplier, item=self.item, qty=1, rate=100, transaction_date=today(), do_not_submit=False)
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': 'Creditors - _TC', 'party_type': 'Supplier', 'party': po.supplier, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name}, {'account': 'Cash - _TC', 'credit_in_account_currency': 100}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': je.doctype, 'voucher_no': je.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([po.name], allocations)
unreconcile.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:490*

### test_01_unreconcile_invoice

**Category**: workflow  
**Description**: Workflow: test 01 unreconcile invoice  
**Expected**: self.assertEqual(pe.unallocated_amount, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si1 = self.create_sales_invoice()
si2 = self.create_sales_invoice()
pe = self.create_payment_entry()
pe.append('references', {'reference_doctype': si1.doctype, 'reference_name': si1.name, 'allocated_amount': 100})
pe.append('references', {'reference_doctype': si2.doctype, 'reference_name': si2.name, 'allocated_amount': 100})
pe.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 0)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(pe.unallocated_amount, 0)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([si1.name, si2.name], allocations)
for x in unreconcile.allocations:
    if x.reference_name != si1.name:
        unreconcile.remove(x)
unreconcile.save().submit()
[doc.reload() for doc in [si1, si2, pe]]
self.assertEqual(si1.outstanding_amount, 100)
self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:67*

### test_05_unreconcile_order

**Category**: workflow  
**Description**: Workflow: test 05 unreconcile order  
**Expected**: self.assertEqual(so.advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 100
pe.append('references', {'reference_doctype': so.doctype, 'reference_name': so.name, 'allocated_amount': 100})
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([so.name], allocations)
unreconcile.save().submit()
so.reload()
pe.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(len(pe.references), 0)
self.assertEqual(pe.unallocated_amount, 100)
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:335*

### test_06_unreconcile_advance_from_payment_entry

**Category**: workflow  
**Description**: Workflow: test 06 unreconcile advance from payment entry  
**Expected**: self.assertEqual(pe.unallocated_amount, 110)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.enable_advance_as_liability()
so1 = self.create_sales_order()
so2 = self.create_sales_order()
pe = self.create_payment_entry()
pe.paid_amount = 260
pe.append('references', {'reference_doctype': so1.doctype, 'reference_name': so1.name, 'allocated_amount': 150})
pe.append('references', {'reference_doctype': so2.doctype, 'reference_name': so2.name, 'allocated_amount': 110})
pe.save().submit()
so1.reload()
self.assertEqual(so1.advance_paid, 150)
so2.reload()
self.assertEqual(so2.advance_paid, 110)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': pe.doctype, 'voucher_no': pe.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 2)
allocations = [(x.reference_name, x.allocated_amount) for x in unreconcile.allocations]
self.assertListEqual(allocations, [(so1.name, 150), (so2.name, 110)])
unreconcile.remove(unreconcile.allocations[0])
unreconcile.save().submit()
so1.reload()
so2.reload()
pe.reload()
self.assertEqual(so1.advance_paid, 150)
self.assertEqual(so2.advance_paid, 0)
self.assertEqual(len(pe.references), 1)
self.assertEqual(pe.unallocated_amount, 110)
self.disable_advance_as_liability()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:377*

### test_unreconcile_advance_from_journal_entry

**Category**: workflow  
**Description**: Workflow: test unreconcile advance from journal entry  
**Expected**: self.assertEqual(po.advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order(company=self.company, supplier=self.supplier, item=self.item, qty=1, rate=100, transaction_date=today(), do_not_submit=False)
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': 'Creditors - _TC', 'party_type': 'Supplier', 'party': po.supplier, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name}, {'account': 'Cash - _TC', 'credit_in_account_currency': 100}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
unreconcile = frappe.get_doc({'doctype': 'Unreconcile Payment', 'company': self.company, 'voucher_type': je.doctype, 'voucher_no': je.name})
unreconcile.add_references()
self.assertEqual(len(unreconcile.allocations), 1)
allocations = [x.reference_name for x in unreconcile.allocations]
self.assertEqual([po.name], allocations)
unreconcile.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:490*

### test_update_received_qty_in_material_request

**Category**: workflow  
**Description**: Workflow: test update received qty in material request  
**Expected**: self.assertEqual(mr.items[0].received_qty, 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_invoice
'\n\t\tTest if the received_qty in Material Request is updated correctly when\n\t\ta Purchase Invoice with update_stock=True is submitted.\n\t\t'
mr = make_material_request(item_code='_Test Item', qty=10)
mr.save()
mr.submit()
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save()
po.submit()
pi = make_purchase_invoice(po.name)
pi.update_stock = True
pi.insert()
pi.submit()
mr.reload()
self.assertEqual(mr.items[0].received_qty, 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:92*

### test_payment_entry_unlink_against_purchase_invoice

**Category**: workflow  
**Description**: Workflow: test payment entry unlink against purchase invoice  
**Expected**: self.assertRaises(frappe.LinkExistsError, pi_doc.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.payment_entry.test_payment_entry import get_payment_entry
unlink_payment_on_cancel_of_invoice(0)
pi_doc = make_purchase_invoice()
pe = get_payment_entry('Purchase Invoice', pi_doc.name, bank_account='_Test Bank - _TC')
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from_account_currency = pi_doc.currency
pe.paid_to_account_currency = pi_doc.currency
pe.source_exchange_rate = 1
pe.target_exchange_rate = 1
pe.paid_amount = pi_doc.grand_total
pe.save(ignore_permissions=True)
pe.submit()
pi_doc = frappe.get_doc('Purchase Invoice', pi_doc.name)
pi_doc.load_from_db()
self.assertTrue(pi_doc.status, 'Paid')
self.assertRaises(frappe.LinkExistsError, pi_doc.cancel)
unlink_payment_on_cancel_of_invoice()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:165*

### test_purchase_invoice_for_blocked_supplier_invoice

**Category**: workflow  
**Description**: Workflow: test purchase invoice for blocked supplier invoice  
**Expected**: self.assertRaises(frappe.ValidationError, make_purchase_invoice)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Invoices'
supplier.save()
self.assertRaises(frappe.ValidationError, make_purchase_invoice)
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:200*

### test_purchase_invoice_for_blocked_supplier_payment

**Category**: workflow  
**Description**: Workflow: test purchase invoice for blocked supplier payment  
**Expected**: self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Payments'
supplier.save()
pi = make_purchase_invoice()
self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:211*

### test_purchase_invoice_for_blocked_supplier_payment_today_date

**Category**: workflow  
**Description**: Workflow: test purchase invoice for blocked supplier payment today date  
**Expected**: self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Payments'
supplier.release_date = nowdate()
supplier.save()
pi = make_purchase_invoice()
self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:230*

### test_purchase_invoice_with_exchange_rate_difference

**Category**: workflow  
**Description**: Workflow: test purchase invoice with exchange rate difference  
**Expected**: self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice as create_purchase_invoice
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', currency='USD', conversion_rate=70)
pi = create_purchase_invoice(pr.name)
pi.conversion_rate = 80
pi.insert()
pi.submit()
exchange_gain_loss_account = frappe.db.get_value('Company', pi.company, 'exchange_gain_loss_account')
amount = frappe.db.get_value('GL Entry', {'account': exchange_gain_loss_account, 'voucher_no': pi.name}, 'debit')
discrepancy_caused_by_exchange_rate_diff = abs(pi.items[0].base_net_amount - pr.items[0].base_net_amount)
self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:355*

### test_purchase_invoice_with_exchange_rate_difference_for_non_stock_item

**Category**: workflow  
**Description**: Workflow: test purchase invoice with exchange rate difference for non stock item  
**Expected**: self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import make_purchase_invoice as create_purchase_invoice
pr = frappe.new_doc('Purchase Receipt')
pr.currency = 'USD'
pr.company = '_Test Company with perpetual inventory'
pr.conversion_rate = (70,)
pr.supplier = '_Test Supplier USD'
pr.append('items', {'item_code': '_Test Non Stock Item', 'qty': 1, 'rate': 100})
pr.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': 5, 'warehouse': 'Stores - TCP1'})
pr.insert()
pr.submit()
pi = create_purchase_invoice(pr.name)
pi.conversion_rate = 80
pi.credit_to = '_Test Payable USD - TCP1'
pi.insert()
pi.submit()
exchange_gain_loss_account = frappe.db.get_value('Company', pi.company, 'exchange_gain_loss_account')
amount = frappe.db.get_value('GL Entry', {'account': exchange_gain_loss_account, 'voucher_no': pi.name}, 'debit')
discrepancy_caused_by_exchange_rate_diff = abs(pi.items[1].base_net_amount - pr.items[1].base_net_amount)
self.assertEqual(discrepancy_caused_by_exchange_rate_diff, amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:386*

### test_purchase_invoice_change_naming_series

**Category**: workflow  
**Description**: Workflow: test purchase invoice change naming series  
**Expected**: self.assertRaises(frappe.CannotChangeConstantError, pi.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][1])
pi.insert()
pi.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
pi.insert()
pi.load_from_db()
self.assertTrue(pi.status, 'Draft')
pi.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, pi.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:433*

### test_purchase_invoice_with_advance

**Category**: workflow  
**Description**: Workflow: test purchase invoice with advance  
**Expected**: self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice' and reference_name=%s", pi.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = frappe.copy_doc(self.globalTestRecords['Journal Entry'][1])
jv.insert()
jv.submit()
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
pi.disable_rounded_total = 1
pi.allocate_advances_automatically = 0
pi.append('advances', {'reference_type': 'Journal Entry', 'reference_name': jv.name, 'reference_row': jv.get('accounts')[0].name, 'advance_amount': 400, 'allocated_amount': 300, 'remarks': jv.remark})
pi.insert()
self.assertEqual(pi.outstanding_amount, 1212.3)
pi.disable_rounded_total = 0
pi.get('payment_schedule')[0].payment_amount = 1512.0
pi.save()
self.assertEqual(pi.outstanding_amount, 1212.0)
pi.submit()
pi.load_from_db()
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice'\n\t\t\tand reference_name=%s and debit_in_account_currency=300", pi.name))
pi.cancel()
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account`\n\t\t\twhere reference_type='Purchase Invoice' and reference_name=%s", pi.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:515*

### test_invoice_with_advance_and_multi_payment_terms

**Category**: workflow  
**Description**: Workflow: test invoice with advance and multi payment terms  
**Expected**: self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s", pi.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = frappe.copy_doc(self.globalTestRecords['Journal Entry'][1])
jv.insert()
jv.submit()
pi = frappe.copy_doc(self.globalTestRecords['Purchase Invoice'][0])
pi.disable_rounded_total = 1
pi.allocate_advances_automatically = 0
pi.append('advances', {'reference_type': 'Journal Entry', 'reference_name': jv.name, 'reference_row': jv.get('accounts')[0].name, 'advance_amount': 400, 'allocated_amount': 300, 'remarks': jv.remark})
pi.insert()
pi.update({'payment_schedule': get_payment_terms('_Test Payment Term Template', pi.posting_date, pi.grand_total, pi.base_grand_total)})
pi.save()
pi.submit()
self.assertEqual(pi.payment_schedule[0].payment_amount, 606.15)
self.assertEqual(pi.payment_schedule[0].due_date, pi.posting_date)
self.assertEqual(pi.payment_schedule[1].payment_amount, 606.15)
self.assertEqual(pi.payment_schedule[1].due_date, add_days(pi.posting_date, 30))
pi.load_from_db()
self.assertTrue(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s and debit_in_account_currency=300", pi.name))
self.assertEqual(pi.outstanding_amount, 1212.3)
pi.cancel()
self.assertFalse(frappe.db.sql("select name from `tabJournal Entry Account` where reference_type='Purchase Invoice' and reference_name=%s", pi.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/purchase_invoice/test_purchase_invoice.py:568*

### test_01_receivable_summary_output

**Category**: workflow  
**Description**: Workflow: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:22*

### test_02_various_filters_and_output

**Category**: workflow  
**Description**: Workflow: test 02 various filters and output  
**Expected**: self.assertEqual(len(rpt_output), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
pe = get_payment_entry(si.doctype, si.name)
pe.paid_amount = 150
pe.references[0].allocated_amount = 150
pe.save().submit()
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
report = execute(filters)
rpt_output = report[1]
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'party_name': self.customer, 'invoiced': 200.0, 'paid': 150.0, 'credit_note': 0.0, 'outstanding': 50.0, 'range1': 50.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 50.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_gl_balance': True})
expected_data.update({'gl_balance': 50.0, 'diff': 0.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_future_payments': True})
expected_data.update({'remaining_balance': 50.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
pe = get_payment_entry(si.doctype, si.name).save().submit()
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:116*

### test_01_receivable_summary_output

**Category**: workflow  
**Description**: Workflow: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:22*

### test_02_various_filters_and_output

**Category**: workflow  
**Description**: Workflow: test 02 various filters and output  
**Expected**: self.assertEqual(len(rpt_output), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = {'company': self.company, 'customer': self.customer, 'posting_date': today(), 'range': '30, 60, 90, 120'}
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=200, price_list_rate=200)
pe = get_payment_entry(si.doctype, si.name)
pe.paid_amount = 150
pe.references[0].allocated_amount = 150
pe.save().submit()
customer_group, customer_territory = frappe.db.get_all('Customer', filters={'name': self.customer}, fields=['customer_group', 'territory'], as_list=True)[0]
report = execute(filters)
rpt_output = report[1]
expected_data = {'party_type': 'Customer', 'advance': 0, 'party': self.customer, 'party_name': self.customer, 'invoiced': 200.0, 'paid': 150.0, 'credit_note': 0.0, 'outstanding': 50.0, 'range1': 50.0, 'range2': 0.0, 'range3': 0.0, 'range4': 0.0, 'range5': 0.0, 'total_due': 50.0, 'future_amount': 0.0, 'sales_person': [], 'currency': si.currency, 'territory': customer_territory, 'customer_group': customer_group}
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_gl_balance': True})
expected_data.update({'gl_balance': 50.0, 'diff': 0.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
filters.update({'show_future_payments': True})
expected_data.update({'remaining_balance': 50.0})
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
pe = get_payment_entry(si.doctype, si.name).save().submit()
report = execute(filters)
rpt_output = report[1]
self.assertEqual(len(rpt_output), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:116*

### test_payment_against_invoice

**Category**: workflow  
**Description**: Workflow: test payment against invoice  
**Expected**: self.assertEqual(pl_entries[1], expected_values[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
ple = self.ple
si1 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
pe1 = get_payment_entry(si1.doctype, si1.name).save().submit()
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si1.doctype) & (ple.against_voucher_no == si1.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si1.doctype, 'voucher_no': si1.name, 'against_voucher_type': si1.doctype, 'against_voucher_no': si1.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe1.doctype, 'voucher_no': pe1.name, 'against_voucher_type': si1.doctype, 'against_voucher_no': si1.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries[0], expected_values[0])
self.assertEqual(pl_entries[1], expected_values[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:194*

### test_partial_payment_against_invoice

**Category**: workflow  
**Description**: Workflow: test partial payment against invoice  
**Expected**: self.assertEqual(pl_entries[1], expected_values[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

ple = self.ple
transaction_date = nowdate()
amount = 100
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
pe2 = get_payment_entry(si2.doctype, si2.name)
pe2.get('references')[0].allocated_amount = 50
pe2.get('references')[0].outstanding_amount = 50
pe2 = pe2.save().submit()
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si2.doctype) & (ple.against_voucher_no == si2.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si2.doctype, 'voucher_no': si2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe2.doctype, 'voucher_no': pe2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': -50, 'delinked': 0}]
self.assertEqual(pl_entries[0], expected_values[0])
self.assertEqual(pl_entries[1], expected_values[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:239*

### test_cr_note_against_invoice

**Category**: workflow  
**Description**: Workflow: test cr note against invoice  
**Expected**: self.assertEqual(pl_entries_cr_note1, expected_values_for_cr_note1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

ple = self.ple
transaction_date = nowdate()
amount = 100
si3 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
cr_note1 = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
cr_note1.is_return = 1
cr_note1.return_against = si3.name
cr_note1 = cr_note1.save().submit()
pl_entries_si3 = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si3.doctype) & (ple.against_voucher_no == si3.name)).orderby(ple.creation).run(as_dict=True)
pl_entries_cr_note1 = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == cr_note1.doctype) & (ple.against_voucher_no == cr_note1.name)).orderby(ple.creation).run(as_dict=True)
expected_values_for_si3 = [{'voucher_type': si3.doctype, 'voucher_no': si3.name, 'against_voucher_type': si3.doctype, 'against_voucher_no': si3.name, 'amount': amount, 'delinked': 0}]
expected_values_for_cr_note1 = [{'voucher_type': cr_note1.doctype, 'voucher_no': cr_note1.name, 'against_voucher_type': cr_note1.doctype, 'against_voucher_no': cr_note1.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries_si3, expected_values_for_si3)
self.assertEqual(pl_entries_cr_note1, expected_values_for_cr_note1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:287*

### test_je_against_inv_and_note

**Category**: workflow  
**Description**: Workflow: test je against inv and note  
**Expected**: self.assertEqual(pl_entries_for_crnote[1], expected_values[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

ple = self.ple
transaction_date = nowdate()
amount = 100
si4 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
cr_note2 = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
cr_note2.is_return = 1
cr_note2 = cr_note2.save().submit()
je1 = self.create_journal_entry(self.debit_to, self.debit_to, amount, posting_date=transaction_date)
je1.get('accounts')[0].party_type = je1.get('accounts')[1].party_type = 'Customer'
je1.get('accounts')[0].party = je1.get('accounts')[1].party = self.customer
je1.get('accounts')[0].reference_type = cr_note2.doctype
je1.get('accounts')[0].reference_name = cr_note2.name
je1.get('accounts')[1].reference_type = si4.doctype
je1.get('accounts')[1].reference_name = si4.name
je1 = je1.save().submit()
pl_entries_for_invoice = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si4.doctype) & (ple.against_voucher_no == si4.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si4.doctype, 'voucher_no': si4.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': si4.doctype, 'against_voucher_no': si4.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries_for_invoice[0], expected_values[0])
self.assertEqual(pl_entries_for_invoice[1], expected_values[1])
pl_entries_for_crnote = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == cr_note2.doctype) & (ple.against_voucher_no == cr_note2.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': cr_note2.doctype, 'voucher_no': cr_note2.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': -amount, 'delinked': 0}, {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'against_voucher_type': cr_note2.doctype, 'against_voucher_no': cr_note2.name, 'amount': amount, 'delinked': 0}]
self.assertEqual(pl_entries_for_crnote[0], expected_values[0])
self.assertEqual(pl_entries_for_crnote[1], expected_values[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:355*

### test_multi_payment_unlink_on_invoice_cancellation

**Category**: workflow  
**Description**: Workflow: test multi payment unlink on invoice cancellation  
**Expected**: self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
for amt in [40, 40, 20]:
    pe = get_payment_entry(si.doctype, si.name)
    pe.paid_amount = amt
    pe.get('references')[0].allocated_amount = amt
    pe = pe.save().submit()
si.reload()
si.cancel()
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': si.doctype, 'against_voucher_no': si.name, 'delinked': 0})
self.assertEqual(entries, [])
si.delete()
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:452*

### test_multi_je_unlink_on_invoice_cancellation

**Category**: workflow  
**Description**: Workflow: test multi je unlink on invoice cancellation  
**Expected**: self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
for amt in [40, 40, 20]:
    je1 = self.create_journal_entry(self.income_account, self.debit_to, amt, posting_date=transaction_date)
    je1.get('accounts')[1].party_type = 'Customer'
    je1.get('accounts')[1].party = self.customer
    je1.get('accounts')[1].reference_type = si.doctype
    je1.get('accounts')[1].reference_name = si.name
    je1 = je1.save().submit()
si.reload()
si.cancel()
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': si.doctype, 'against_voucher_no': si.name, 'delinked': 0})
self.assertEqual(entries, [])
si.delete()
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, si.doctype, si.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:481*

### test_advance_payment_unlink_on_order_cancellation

**Category**: workflow  
**Description**: Workflow: test advance payment unlink on order cancellation  
**Expected**: self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, so.doctype, so.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ple = qb.DocType('Payment Ledger Entry')
self.create_company()
self.create_item()
self.create_customer()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
so = self.create_sales_order(qty=1, rate=amount, posting_date=transaction_date).save().submit()
get_payment_entry(so.doctype, so.name).save().submit()
so.reload()
so.cancel()
entries = frappe.db.get_list('Payment Ledger Entry', filters={'against_voucher_type': so.doctype, 'against_voucher_no': so.name, 'delinked': 0})
self.assertEqual(entries, [])
so.delete()
self.assertRaises(frappe.DoesNotExistError, frappe.get_doc, so.doctype, so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:518*

### test_payment_against_invoice

**Category**: workflow  
**Description**: Workflow: test payment against invoice  
**Expected**: self.assertEqual(pl_entries[1], expected_values[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = nowdate()
amount = 100
ple = self.ple
si1 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
pe1 = get_payment_entry(si1.doctype, si1.name).save().submit()
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si1.doctype) & (ple.against_voucher_no == si1.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si1.doctype, 'voucher_no': si1.name, 'against_voucher_type': si1.doctype, 'against_voucher_no': si1.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe1.doctype, 'voucher_no': pe1.name, 'against_voucher_type': si1.doctype, 'against_voucher_no': si1.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries[0], expected_values[0])
self.assertEqual(pl_entries[1], expected_values[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:194*

### test_partial_payment_against_invoice

**Category**: workflow  
**Description**: Workflow: test partial payment against invoice  
**Expected**: self.assertEqual(pl_entries[1], expected_values[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ple = self.ple
transaction_date = nowdate()
amount = 100
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
pe2 = get_payment_entry(si2.doctype, si2.name)
pe2.get('references')[0].allocated_amount = 50
pe2.get('references')[0].outstanding_amount = 50
pe2 = pe2.save().submit()
pl_entries = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si2.doctype) & (ple.against_voucher_no == si2.name)).orderby(ple.creation).run(as_dict=True)
expected_values = [{'voucher_type': si2.doctype, 'voucher_no': si2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': amount, 'delinked': 0}, {'voucher_type': pe2.doctype, 'voucher_no': pe2.name, 'against_voucher_type': si2.doctype, 'against_voucher_no': si2.name, 'amount': -50, 'delinked': 0}]
self.assertEqual(pl_entries[0], expected_values[0])
self.assertEqual(pl_entries[1], expected_values[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:239*

### test_cr_note_against_invoice

**Category**: workflow  
**Description**: Workflow: test cr note against invoice  
**Expected**: self.assertEqual(pl_entries_cr_note1, expected_values_for_cr_note1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ple = self.ple
transaction_date = nowdate()
amount = 100
si3 = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
cr_note1 = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
cr_note1.is_return = 1
cr_note1.return_against = si3.name
cr_note1 = cr_note1.save().submit()
pl_entries_si3 = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == si3.doctype) & (ple.against_voucher_no == si3.name)).orderby(ple.creation).run(as_dict=True)
pl_entries_cr_note1 = qb.from_(ple).select(ple.voucher_type, ple.voucher_no, ple.against_voucher_type, ple.against_voucher_no, ple.amount, ple.delinked).where((ple.against_voucher_type == cr_note1.doctype) & (ple.against_voucher_no == cr_note1.name)).orderby(ple.creation).run(as_dict=True)
expected_values_for_si3 = [{'voucher_type': si3.doctype, 'voucher_no': si3.name, 'against_voucher_type': si3.doctype, 'against_voucher_no': si3.name, 'amount': amount, 'delinked': 0}]
expected_values_for_cr_note1 = [{'voucher_type': cr_note1.doctype, 'voucher_no': cr_note1.name, 'against_voucher_type': cr_note1.doctype, 'against_voucher_no': cr_note1.name, 'amount': -amount, 'delinked': 0}]
self.assertEqual(pl_entries_si3, expected_values_for_si3)
self.assertEqual(pl_entries_cr_note1, expected_values_for_cr_note1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_ledger_entry/test_payment_ledger_entry.py:287*

### test_bank_clearance

**Category**: workflow  
**Description**: Workflow: test bank clearance  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:38*

### test_bank_clearance_with_loan

**Category**: workflow  
**Description**: Workflow: test bank clearance with loan  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from lending.loan_management.doctype.loan.test_loan import create_loan, create_loan_accounts, create_loan_product, create_repayment_entry, make_loan_disbursement_entry

def create_loan_masters():
    create_loan_product('Clearance Loan', 'Clearance Loan', 2000000, 13.5, 25, 0, 5, 'Cash', '_Test Bank Clearance - _TC', '_Test Bank Clearance - _TC', 'Loan Account - _TC', 'Interest Income Account - _TC', 'Penalty Income Account - _TC')

def make_loan():
    loan = create_loan('_Test Customer', 'Clearance Loan', 280000, 'Repay Over Number of Periods', 20, applicant_type='Customer')
    loan.submit()
    make_loan_disbursement_entry(loan.name, loan.loan_amount, disbursement_date=getdate())
    repayment_entry = create_repayment_entry(loan.name, '_Test Customer', getdate(), loan.loan_amount)
    repayment_entry.save()
    repayment_entry.submit()
create_loan_accounts()
create_loan_masters()
make_loan()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:47*

### test_update_clearance_date_on_si

**Category**: workflow  
**Description**: Workflow: test update clearance date on si  
**Expected**: self.assertEqual(si_clearance_date, date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sales_invoice = make_pos_sales_invoice()
date = getdate()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(date, -1)
bank_clearance.to_date = date
bank_clearance.include_pos_transactions = 1
bank_clearance.get_payment_entries()
self.assertNotEqual(len(bank_clearance.payment_entries), 0)
for payment in bank_clearance.payment_entries:
    if payment.payment_entry == sales_invoice.name:
        payment.clearance_date = date
bank_clearance.update_clearance_date()
si_clearance_date = frappe.db.get_value('Sales Invoice Payment', {'parent': sales_invoice.name, 'account': bank_clearance.account}, 'clearance_date')
self.assertEqual(si_clearance_date, date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:99*

### test_bank_clearance

**Category**: workflow  
**Description**: Workflow: test bank clearance  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:38*

### test_bank_clearance_with_loan

**Category**: workflow  
**Description**: Workflow: test bank clearance with loan  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from lending.loan_management.doctype.loan.test_loan import create_loan, create_loan_accounts, create_loan_product, create_repayment_entry, make_loan_disbursement_entry

def create_loan_masters():
    create_loan_product('Clearance Loan', 'Clearance Loan', 2000000, 13.5, 25, 0, 5, 'Cash', '_Test Bank Clearance - _TC', '_Test Bank Clearance - _TC', 'Loan Account - _TC', 'Interest Income Account - _TC', 'Penalty Income Account - _TC')

def make_loan():
    loan = create_loan('_Test Customer', 'Clearance Loan', 280000, 'Repay Over Number of Periods', 20, applicant_type='Customer')
    loan.submit()
    make_loan_disbursement_entry(loan.name, loan.loan_amount, disbursement_date=getdate())
    repayment_entry = create_repayment_entry(loan.name, '_Test Customer', getdate(), loan.loan_amount)
    repayment_entry.save()
    repayment_entry.submit()
create_loan_accounts()
create_loan_masters()
make_loan()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(getdate(), -1)
bank_clearance.to_date = getdate()
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:47*

### test_update_clearance_date_on_si

**Category**: workflow  
**Description**: Workflow: test update clearance date on si  
**Expected**: self.assertEqual(si_clearance_date, date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sales_invoice = make_pos_sales_invoice()
date = getdate()
bank_clearance = frappe.get_doc('Bank Clearance')
bank_clearance.account = '_Test Bank Clearance - _TC'
bank_clearance.from_date = add_months(date, -1)
bank_clearance.to_date = date
bank_clearance.include_pos_transactions = 1
bank_clearance.get_payment_entries()
self.assertNotEqual(len(bank_clearance.payment_entries), 0)
for payment in bank_clearance.payment_entries:
    if payment.payment_entry == sales_invoice.name:
        payment.clearance_date = date
bank_clearance.update_clearance_date()
si_clearance_date = frappe.db.get_value('Sales Invoice Payment', {'parent': sales_invoice.name, 'account': bank_clearance.account}, 'clearance_date')
self.assertEqual(si_clearance_date, date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:99*

### test_accounting_period_exempted_role

**Category**: workflow  
**Description**: Workflow: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ap = create_accounting_period(period_name='Test Accounting Period Exempted', exempted_role='Accounts Manager', start_date='2025-12-01', end_date='2025-12-31')
ap.save()
users = frappe.get_all('User', filters={'email': ['like', 'test%']}, limit=1)
user = None
if users[0].name:
    user = frappe.get_doc('User', users[0].name)
else:
    user = frappe.get_doc({'doctype': 'User', 'email': 'test1@example.com', 'first_name': 'Test1'})
    user.insert()
user.roles = []
user.append('roles', {'role': 'Accounts User'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
frappe.set_user(user.name)
posting_date = '2025-12-11'
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
with self.assertRaises(frappe.ValidationError):
    doc.submit()
user.append('roles', {'role': 'Accounts Manager'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
doc.submit()
self.assertEqual(doc.docstatus, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:39*

### test_accounting_period_exempted_role

**Category**: workflow  
**Description**: Workflow: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ap = create_accounting_period(period_name='Test Accounting Period Exempted', exempted_role='Accounts Manager', start_date='2025-12-01', end_date='2025-12-31')
ap.save()
users = frappe.get_all('User', filters={'email': ['like', 'test%']}, limit=1)
user = None
if users[0].name:
    user = frappe.get_doc('User', users[0].name)
else:
    user = frappe.get_doc({'doctype': 'User', 'email': 'test1@example.com', 'first_name': 'Test1'})
    user.insert()
user.roles = []
user.append('roles', {'role': 'Accounts User'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
frappe.set_user(user.name)
posting_date = '2025-12-11'
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
with self.assertRaises(frappe.ValidationError):
    doc.submit()
user.append('roles', {'role': 'Accounts Manager'})
user.save(ignore_permissions=True)
frappe.clear_cache(user=user.name)
doc = create_sales_invoice(do_not_save=1, posting_date=posting_date)
doc.submit()
self.assertEqual(doc.docstatus, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:39*

### test_allowed_dimension_validation

**Category**: workflow  
**Description**: Workflow: test allowed dimension validation  
**Expected**: self.assertRaises(InvalidAccountDimensionError, si.submit)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si = create_sales_invoice(do_not_save=1)
si.items[0].cost_center = 'Main - _TC'
si.department = 'Accounts - _TC'
si.location = 'Block 1'
si.save()
self.assertRaises(InvalidAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:24*

### test_mandatory_dimension_validation

**Category**: workflow  
**Description**: Workflow: test mandatory dimension validation  
**Expected**: self.assertRaises(MandatoryAccountDimensionError, si.submit)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si = create_sales_invoice(do_not_save=1)
si.department = ''
si.location = 'Block 1'
si.items[0].department = ''
si.items[0].cost_center = '_Test Cost Center 2 - _TC'
si.save()
self.assertRaises(MandatoryAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:34*

### test_allowed_dimension_validation

**Category**: workflow  
**Description**: Workflow: test allowed dimension validation  
**Expected**: self.assertRaises(InvalidAccountDimensionError, si.submit)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
si = create_sales_invoice(do_not_save=1)
si.items[0].cost_center = 'Main - _TC'
si.department = 'Accounts - _TC'
si.location = 'Block 1'
si.save()
self.assertRaises(InvalidAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:24*

### test_mandatory_dimension_validation

**Category**: workflow  
**Description**: Workflow: test mandatory dimension validation  
**Expected**: self.assertRaises(MandatoryAccountDimensionError, si.submit)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
si = create_sales_invoice(do_not_save=1)
si.department = ''
si.location = 'Block 1'
si.items[0].department = ''
si.items[0].cost_center = '_Test Cost Center 2 - _TC'
si.save()
self.assertRaises(MandatoryAccountDimensionError, si.submit)
self.invoice_list.append(si)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:34*

### test_gle_based_on_cost_center_allocation

**Category**: workflow  
**Description**: Workflow: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 1 - _TC': 60, 'Sub Cost Center 2 - _TC': 40})
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 1 - _TC', submit=True)
expected_values = [['Sub Cost Center 1 - _TC', 0.0, 60], ['Sub Cost Center 2 - _TC', 0.0, 40]]
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for i, gle in enumerate(gl_entries):
    self.assertEqual(expected_values[i][0], gle.cost_center)
    self.assertEqual(expected_values[i][1], gle.debit)
    self.assertEqual(expected_values[i][2], gle.credit)
cca.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:33*

### test_multiple_cost_center_allocation_on_same_main_cost_center

**Category**: workflow  
**Description**: Workflow: test multiple cost center allocation on same main cost center  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

coa1 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 30, 'Sub Cost Center 2 - _TC': 30, 'Sub Cost Center 3 - _TC': 40}, valid_from=add_days(today(), -5))
coa2 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}, valid_from=add_days(today(), -1))
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 3 - _TC', posting_date=today(), submit=True)
expected_values = {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for gle in gl_entries:
    self.assertTrue(gle.cost_center in expected_values)
    self.assertEqual(gle.debit, 0)
    self.assertEqual(gle.credit, expected_values[gle.cost_center])
coa1.cancel()
coa2.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:146*

### test_debit_credit_on_cost_center_allocation_for_commercial_rounding

**Category**: workflow  
**Description**: Workflow: test debit credit on cost center allocation for commercial rounding  
**Expected**: self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 2 - _TC': 50, 'Sub Cost Center 3 - _TC': 50})
si = create_sales_invoice(rate=145.65, cost_center='Main Cost Center 1 - _TC')
gl_entry = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gl_entry).select(Sum(gl_entry.credit).as_('cr'), Sum(gl_entry.debit).as_('dr')).where(gl_entry.voucher_type == 'Sales Invoice').where(gl_entry.voucher_no == si.name).run(as_dict=1)
self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)
si.cancel()
cca.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:194*

### test_gle_based_on_cost_center_allocation

**Category**: workflow  
**Description**: Workflow: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 1 - _TC': 60, 'Sub Cost Center 2 - _TC': 40})
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 1 - _TC', submit=True)
expected_values = [['Sub Cost Center 1 - _TC', 0.0, 60], ['Sub Cost Center 2 - _TC', 0.0, 40]]
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for i, gle in enumerate(gl_entries):
    self.assertEqual(expected_values[i][0], gle.cost_center)
    self.assertEqual(expected_values[i][1], gle.debit)
    self.assertEqual(expected_values[i][2], gle.credit)
cca.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:33*

### test_multiple_cost_center_allocation_on_same_main_cost_center

**Category**: workflow  
**Description**: Workflow: test multiple cost center allocation on same main cost center  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
coa1 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 30, 'Sub Cost Center 2 - _TC': 30, 'Sub Cost Center 3 - _TC': 40}, valid_from=add_days(today(), -5))
coa2 = create_cost_center_allocation('_Test Company', 'Main Cost Center 3 - _TC', {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}, valid_from=add_days(today(), -1))
jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 3 - _TC', posting_date=today(), submit=True)
expected_values = {'Sub Cost Center 1 - _TC': 50, 'Sub Cost Center 2 - _TC': 50}
gle = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
self.assertTrue(gl_entries)
for gle in gl_entries:
    self.assertTrue(gle.cost_center in expected_values)
    self.assertEqual(gle.debit, 0)
    self.assertEqual(gle.credit, expected_values[gle.cost_center])
coa1.cancel()
coa2.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:146*

### test_debit_credit_on_cost_center_allocation_for_commercial_rounding

**Category**: workflow  
**Description**: Workflow: test debit credit on cost center allocation for commercial rounding  
**Expected**: self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 2 - _TC': 50, 'Sub Cost Center 3 - _TC': 50})
si = create_sales_invoice(rate=145.65, cost_center='Main Cost Center 1 - _TC')
gl_entry = frappe.qb.DocType('GL Entry')
gl_entries = frappe.qb.from_(gl_entry).select(Sum(gl_entry.credit).as_('cr'), Sum(gl_entry.debit).as_('dr')).where(gl_entry.voucher_type == 'Sales Invoice').where(gl_entry.voucher_no == si.name).run(as_dict=1)
self.assertEqual(gl_entries[0].cr, gl_entries[0].dr)
si.cancel()
cca.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:194*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

si = self.create_sales_invoice()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'item_code': si.items[0].item_code, 'invoice': si.name, 'posting_date': getdate(), 'customer': si.customer, 'debit_to': si.debit_to, 'company': self.company, 'income_account': si.items[0].income_account, 'stock_qty': 1.0, 'stock_uom': si.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total_other_charges': 0, 'total': 100.0, 'currency': 'INR'}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:37*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = self.create_sales_invoice()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'item_code': si.items[0].item_code, 'invoice': si.name, 'posting_date': getdate(), 'customer': si.customer, 'debit_to': si.debit_to, 'company': self.company, 'income_account': si.items[0].income_account, 'stock_qty': 1.0, 'stock_uom': si.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total_other_charges': 0, 'total': 100.0, 'currency': 'INR'}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:37*

### test_pos_closing_entry

**Category**: workflow  
**Description**: Workflow: test pos closing entry  
**Expected**: self.assertEqual(pcv_doc.net_total, 6700)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 6700
pcv_doc.submit()
self.assertEqual(pcv_doc.total_quantity, 2)
self.assertEqual(pcv_doc.net_total, 6700)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:45*

### test_pos_closing_without_item_code

**Category**: workflow  
**Description**: Workflow: Test if POS Closing Entry is created without item code  
**Expected**: self.assertTrue(pcv_doc.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

'\n\t\tTest if POS Closing Entry is created without item code\n\t\t'
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=3500, do_not_submit=1, item_name='Test Item', without_item_code=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv.save()
pos_inv.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
self.assertTrue(pcv_doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:73*

### test_pos_qty_for_item

**Category**: workflow  
**Description**: Workflow: Test if quantity is calculated correctly for an item in POS Closing Entry  
**Expected**: self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

'\n\t\tTest if quantity is calculated correctly for an item in POS Closing Entry\n\t\t'
from erpnext.accounts.doctype.pos_invoice.pos_invoice import make_sales_return
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty = get_test_item_qty(pos_profile)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_return = make_sales_return(pos_inv2.name)
pos_return.paid_amount = pos_return.grand_total
pos_return.save()
pos_return.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty_after_sales = get_test_item_qty(pos_profile)
self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:90*

### test_cancelling_of_pos_closing_entry

**Category**: workflow  
**Description**: Workflow: test cancelling of pos closing entry  
**Expected**: self.assertEqual(pos_inv1.status, 'Paid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 6700
pcv_doc.submit()
pos_inv1.load_from_db()
self.assertRaises(frappe.ValidationError, pos_inv1.cancel)
si_doc = frappe.get_doc('Sales Invoice', pos_inv1.consolidated_invoice)
self.assertRaises(frappe.ValidationError, si_doc.cancel)
pcv_doc.load_from_db()
pcv_doc.cancel()
cancelled_invoice = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': pcv_doc.name}, 'consolidated_invoice')
docstatus = frappe.db.get_value('Sales Invoice', cancelled_invoice, 'docstatus')
self.assertEqual(docstatus, 2)
pos_inv1.load_from_db()
self.assertEqual(pos_inv1.status, 'Paid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:124*

### test_pos_closing_for_required_accounting_dimension_in_pos_profile

**Category**: workflow  
**Description**: Workflow: test case to check whether we can create POS Closing Entry without mandatory accounting dimension  
**Expected**: self.assertRaises(frappe.ValidationError, pcv_doc.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

'\n\t\ttest case to check whether we can create POS Closing Entry without mandatory accounting dimension\n\t\t'
create_dimension()
location = frappe.get_doc('Accounting Dimension', 'Location')
location.dimension_defaults[0].mandatory_for_bs = True
location.save()
pos_profile = make_pos_profile(do_not_insert=1, do_not_set_accounting_dimension=1)
self.assertRaises(frappe.ValidationError, pos_profile.insert)
pos_profile.location = 'Block 1'
pos_profile.insert()
self.assertTrue(frappe.db.exists('POS Profile', pos_profile.name))
test_user = init_user_and_profile(do_not_create_pos_profile=1)
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=350, do_not_submit=1, pos_profile=pos_profile.name)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
accounting_dimension_department = frappe.get_doc('Accounting Dimension', {'name': 'Department'})
accounting_dimension_department.dimension_defaults[0].mandatory_for_bs = 1
accounting_dimension_department.save()
pcv_doc = make_closing_entry_from_opening(opening_entry)
self.assertRaises(frappe.ValidationError, pcv_doc.submit)
accounting_dimension_department = frappe.get_doc('Accounting Dimension Detail', {'parent': 'Department'})
accounting_dimension_department.mandatory_for_bs = 0
accounting_dimension_department.save()
disable_dimension()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:167*

### test_closing_entries_with_sales_invoice

**Category**: workflow  
**Description**: Workflow: test closing entries with sales invoice  
**Expected**: self.assertEqual(pos_si2.pos_closing_entry, pcv_doc.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)

test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_si = create_sales_invoice(qty=10, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=1)
pos_si.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
pos_si.save()
pos_si.submit()
pos_si2 = create_sales_invoice(qty=5, is_created_using_pos=1, pos_profile=pos_profile.name, do_not_save=11)
pos_si2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1000})
pos_si2.save()
pos_si2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 1500
pcv_doc.submit()
self.assertEqual(pcv_doc.total_quantity, 15)
self.assertEqual(pcv_doc.net_total, 1500)
pos_si2.reload()
self.assertEqual(pos_si2.pos_closing_entry, pcv_doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:305*

### test_pos_closing_entry

**Category**: workflow  
**Description**: Workflow: test pos closing entry  
**Expected**: self.assertEqual(pcv_doc.net_total, 6700)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 6700
pcv_doc.submit()
self.assertEqual(pcv_doc.total_quantity, 2)
self.assertEqual(pcv_doc.net_total, 6700)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:45*

### test_pos_closing_without_item_code

**Category**: workflow  
**Description**: Workflow: Test if POS Closing Entry is created without item code  
**Expected**: self.assertTrue(pcv_doc.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest if POS Closing Entry is created without item code\n\t\t'
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=3500, do_not_submit=1, item_name='Test Item', without_item_code=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv.save()
pos_inv.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
self.assertTrue(pcv_doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:73*

### test_pos_qty_for_item

**Category**: workflow  
**Description**: Workflow: Test if quantity is calculated correctly for an item in POS Closing Entry  
**Expected**: self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest if quantity is calculated correctly for an item in POS Closing Entry\n\t\t'
from erpnext.accounts.doctype.pos_invoice.pos_invoice import make_sales_return
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty = get_test_item_qty(pos_profile)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_return = make_sales_return(pos_inv2.name)
pos_return.paid_amount = pos_return.grand_total
pos_return.save()
pos_return.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
pcv_doc.submit()
opening_entry = create_opening_entry(pos_profile, test_user.name)
test_item_qty_after_sales = get_test_item_qty(pos_profile)
self.assertEqual(test_item_qty_after_sales, test_item_qty - 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:90*

### test_cancelling_of_pos_closing_entry

**Category**: workflow  
**Description**: Workflow: test cancelling of pos closing entry  
**Expected**: self.assertEqual(pos_inv1.status, 'Paid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv1 = create_pos_invoice(rate=3500, do_not_submit=1)
pos_inv1.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3500})
pos_inv1.save()
pos_inv1.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pcv_doc = make_closing_entry_from_opening(opening_entry)
payment = pcv_doc.payment_reconciliation[0]
self.assertEqual(payment.mode_of_payment, 'Cash')
for d in pcv_doc.payment_reconciliation:
    if d.mode_of_payment == 'Cash':
        d.closing_amount = 6700
pcv_doc.submit()
pos_inv1.load_from_db()
self.assertRaises(frappe.ValidationError, pos_inv1.cancel)
si_doc = frappe.get_doc('Sales Invoice', pos_inv1.consolidated_invoice)
self.assertRaises(frappe.ValidationError, si_doc.cancel)
pcv_doc.load_from_db()
pcv_doc.cancel()
cancelled_invoice = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': pcv_doc.name}, 'consolidated_invoice')
docstatus = frappe.db.get_value('Sales Invoice', cancelled_invoice, 'docstatus')
self.assertEqual(docstatus, 2)
pos_inv1.load_from_db()
self.assertEqual(pos_inv1.status, 'Paid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_closing_entry/test_pos_closing_entry.py:124*

### test_rename_account

**Category**: workflow  
**Description**: Workflow: test rename account  
**Expected**: self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', '1210 - Debtors - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Debtors'
    acc.parent_account = 'Accounts Receivable - _TC'
    acc.account_number = '1210'
    acc.company = '_Test Company'
    acc.insert()
account_number, account_name = frappe.db.get_value('Account', '1210 - Debtors - _TC', ['account_number', 'account_name'])
self.assertEqual(account_number, '1210')
self.assertEqual(account_name, 'Debtors')
new_account_number = '1211-11-4 - 6 - '
new_account_name = 'Debtors 1 - Test - '
update_account_number('1210 - Debtors - _TC', new_account_name, new_account_number)
new_acc = frappe.db.get_value('Account', '1211-11-4 - 6 - - Debtors 1 - Test - - _TC', ['account_name', 'account_number'], as_dict=1)
self.assertEqual(new_acc.account_name, 'Debtors 1 - Test -')
self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')
frappe.delete_doc('Account', '1211-11-4 - 6 - Debtors 1 - Test - - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:19*

### test_account_sync

**Category**: workflow  
**Description**: Workflow: test account sync  
**Expected**: self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Sync Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.company = '_Test Company 3'
acc.insert()
acc_tc_4 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 4'})
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 5'})
self.assertEqual(acc_tc_4, 'Test Sync Account - _TC4')
self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:131*

### test_add_account_to_a_group

**Category**: workflow  
**Description**: Workflow: test add account to a group  
**Expected**: self.assertRaises(frappe.ValidationError, acc.insert)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 1)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Group Account'
acc.parent_account = 'Office Rent - _TC3'
acc.company = '_Test Company 3'
self.assertRaises(frappe.ValidationError, acc.insert)
frappe.db.set_value('Account', 'Office Rent - _TC3', 'is_group', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:149*

### test_account_rename_sync

**Category**: workflow  
**Description**: Workflow: test account rename sync  
**Expected**: self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 5', 'account_number': '1234'}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Rename Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.company = '_Test Company 3'
acc.insert()
update_account_number(acc.name, 'Test Rename Sync Account', '1234')
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 4', 'account_number': '1234'}))
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Rename Sync Account', 'company': '_Test Company 5', 'account_number': '1234'}))
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC3')
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC4')
frappe.delete_doc('Account', '1234 - Test Rename Sync Account - _TC5')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:160*

### test_account_currency_sync

**Category**: workflow  
**Description**: Workflow: In a parent->child company setup, child should inherit parent account currency if explicitly specified.  
**Expected**: self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'USD', 'company': '_Test Company 7'}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tIn a parent->child company setup, child should inherit parent account currency if explicitly specified.\n\t\t'
frappe.local.flags.pop('ignore_root_company_validation', None)

def create_bank_account():
    acc = frappe.new_doc('Account')
    acc.account_name = '_Test Bank JPY'
    acc.parent_account = 'Temporary Accounts - _TC6'
    acc.company = '_Test Company 6'
    return acc
acc = create_bank_account()
acc.account_currency = 'JPY'
acc.insert()
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'JPY', 'company': '_Test Company 7'}))
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
acc = create_bank_account()
acc.insert()
self.assertTrue(frappe.db.exists({'doctype': 'Account', 'account_name': '_Test Bank JPY', 'account_currency': 'USD', 'company': '_Test Company 7'}))
frappe.delete_doc('Account', '_Test Bank JPY - _TC6')
frappe.delete_doc('Account', '_Test Bank JPY - _TC7')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:198*

### test_child_company_account_rename_sync

**Category**: workflow  
**Description**: Workflow: test child company account rename sync  
**Expected**: self.assertTrue(frappe.db.exists('Account', {'name': 'Test Modified Account - _TC5', 'company': '_Test Company 5'}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Group Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.is_group = 1
acc.company = '_Test Company 3'
acc.insert()
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 4'}))
self.assertTrue(frappe.db.exists('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'}))
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Group Account', 'company': '_Test Company 5'})
self.assertRaises(frappe.ValidationError, update_account_number, acc_tc_5, 'Test Modified Account')
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 1)
update_account_number(acc_tc_5, 'Test Modified Account')
self.assertTrue(frappe.db.exists('Account', {'name': 'Test Modified Account - _TC5', 'company': '_Test Company 5'}))
frappe.db.set_value('Company', '_Test Company 5', 'allow_account_creation_against_child_company', 0)
to_delete = ['Test Group Account - _TC3', 'Test Group Account - _TC4', 'Test Modified Account - _TC5']
for doc in to_delete:
    frappe.delete_doc('Account', doc)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:248*

### test_validate_account_currency

**Category**: workflow  
**Description**: Workflow: test validate account currency  
**Expected**: self.assertRaises(frappe.ValidationError, acc.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.journal_entry.test_journal_entry import make_journal_entry
if not frappe.db.get_value('Account', 'Test Currency Account - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Test Currency Account'
    acc.parent_account = 'Tax Assets - _TC'
    acc.company = '_Test Company'
    acc.insert()
else:
    acc = frappe.get_doc('Account', 'Test Currency Account - _TC')
self.assertEqual(acc.account_currency, 'INR')
make_journal_entry('Test Currency Account - _TC', 'Miscellaneous Expenses - _TC', 100, submit=True)
acc.account_currency = 'USD'
self.assertRaises(frappe.ValidationError, acc.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:291*

### test_account_balance

**Category**: workflow  
**Description**: Workflow: test account balance  
**Expected**: self.assertEqual(balance, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.utils import get_balance_on
if not frappe.db.exists('Account', 'Test Percent Account %5 - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Test Percent Account %5'
    acc.parent_account = 'Tax Assets - _TC'
    acc.company = '_Test Company'
    acc.insert()
balance = get_balance_on(account='Test Percent Account %5 - _TC', date=nowdate())
self.assertEqual(balance, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:311*

### test_rename_account

**Category**: workflow  
**Description**: Workflow: test rename account  
**Expected**: self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', '1210 - Debtors - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Debtors'
    acc.parent_account = 'Accounts Receivable - _TC'
    acc.account_number = '1210'
    acc.company = '_Test Company'
    acc.insert()
account_number, account_name = frappe.db.get_value('Account', '1210 - Debtors - _TC', ['account_number', 'account_name'])
self.assertEqual(account_number, '1210')
self.assertEqual(account_name, 'Debtors')
new_account_number = '1211-11-4 - 6 - '
new_account_name = 'Debtors 1 - Test - '
update_account_number('1210 - Debtors - _TC', new_account_name, new_account_number)
new_acc = frappe.db.get_value('Account', '1211-11-4 - 6 - - Debtors 1 - Test - - _TC', ['account_name', 'account_number'], as_dict=1)
self.assertEqual(new_acc.account_name, 'Debtors 1 - Test -')
self.assertEqual(new_acc.account_number, '1211-11-4 - 6 -')
frappe.delete_doc('Account', '1211-11-4 - 6 - Debtors 1 - Test - - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:19*

### test_account_sync

**Category**: workflow  
**Description**: Workflow: test account sync  
**Expected**: self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.local.flags.pop('ignore_root_company_validation', None)
acc = frappe.new_doc('Account')
acc.account_name = 'Test Sync Account'
acc.parent_account = 'Temporary Accounts - _TC3'
acc.company = '_Test Company 3'
acc.insert()
acc_tc_4 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 4'})
acc_tc_5 = frappe.db.get_value('Account', {'account_name': 'Test Sync Account', 'company': '_Test Company 5'})
self.assertEqual(acc_tc_4, 'Test Sync Account - _TC4')
self.assertEqual(acc_tc_5, 'Test Sync Account - _TC5')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/account/test_account.py:131*

### test_stale_days

**Category**: workflow  
**Description**: Workflow: test stale days  
**Expected**: self.assertRaises(frappe.ValidationError, cur_settings.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
cur_settings.allow_stale = 0
cur_settings.stale_days = 0
self.assertRaises(frappe.ValidationError, cur_settings.save)
cur_settings.stale_days = -1
self.assertRaises(frappe.ValidationError, cur_settings.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounts_settings/test_accounts_settings.py:13*

### test_stale_days

**Category**: workflow  
**Description**: Workflow: test stale days  
**Expected**: self.assertRaises(frappe.ValidationError, cur_settings.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
cur_settings.allow_stale = 0
cur_settings.stale_days = 0
self.assertRaises(frappe.ValidationError, cur_settings.save)
cur_settings.stale_days = -1
self.assertRaises(frappe.ValidationError, cur_settings.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounts_settings/test_accounts_settings.py:13*

### test_round_off_entry

**Category**: workflow  
**Description**: Workflow: test round off entry  
**Expected**: self.assertTrue(round_off_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Company', '_Test Company', 'round_off_account', '_Test Write Off - _TC')
frappe.db.set_value('Company', '_Test Company', 'round_off_cost_center', '_Test Cost Center - _TC')
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', submit=False)
jv.get('accounts')[0].debit = 100.01
jv.flags.ignore_validate = True
jv.submit()
round_off_entry = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\tand account='_Test Write Off - _TC' and cost_center='_Test Cost Center - _TC'\n\t\t\tand debit = 0 and credit = '.01'", jv.name)
self.assertTrue(round_off_entry)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:13*

### test_rename_entries

**Category**: workflow  
**Description**: Workflow: test rename entries  
**Expected**: self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
rename_gle_sle_docs()
naming_series = parse_naming_series(parts=frappe.get_meta('GL Entry').autoname.split('.')[:-1])
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 1 for entry in gl_entries)))
old_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
rename_gle_sle_docs()
new_gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
new_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:39*

### test_validate_account_party_type

**Category**: workflow  
**Description**: Workflow: test validate account party type  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Supplier'
    break
jv.save()
try:
    jv.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
jv1 = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Customer'
    break
jv1.save()
try:
    jv1.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:81*

### test_round_off_entry

**Category**: workflow  
**Description**: Workflow: test round off entry  
**Expected**: self.assertTrue(round_off_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Company', '_Test Company', 'round_off_account', '_Test Write Off - _TC')
frappe.db.set_value('Company', '_Test Company', 'round_off_cost_center', '_Test Cost Center - _TC')
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', submit=False)
jv.get('accounts')[0].debit = 100.01
jv.flags.ignore_validate = True
jv.submit()
round_off_entry = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\tand account='_Test Write Off - _TC' and cost_center='_Test Cost Center - _TC'\n\t\t\tand debit = 0 and credit = '.01'", jv.name)
self.assertTrue(round_off_entry)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:13*

### test_rename_entries

**Category**: workflow  
**Description**: Workflow: test rename entries  
**Expected**: self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
rename_gle_sle_docs()
naming_series = parse_naming_series(parts=frappe.get_meta('GL Entry').autoname.split('.')[:-1])
je = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, submit=True)
gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 1 for entry in gl_entries)))
old_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
rename_gle_sle_docs()
new_gl_entries = frappe.get_all('GL Entry', fields=['name', 'to_rename'], filters={'voucher_type': 'Journal Entry', 'voucher_no': je.name}, order_by='creation')
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
new_naming_series_current_value = frappe.db.sql('SELECT current from tabSeries where name = %s', naming_series)[0][0]
self.assertEqual(old_naming_series_current_value + 2, new_naming_series_current_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:39*

### test_validate_account_party_type

**Category**: workflow  
**Description**: Workflow: test validate account party type  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Supplier'
    break
jv.save()
try:
    jv.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
jv1 = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 100, '_Test Cost Center - _TC', save=False, submit=False)
for row in jv.accounts:
    row.party_type = 'Customer'
    break
jv1.save()
try:
    jv1.submit()
except Exception as e:
    self.assertEqual(str(e), 'Party Type and Party can only be set for Receivable / Payable account_Test Account Cost for Goods Sold - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:81*

### test_filter_min_max

**Category**: workflow  
**Description**: Workflow: test filter min max  
**Expected**: self.assertEqual(len(pr.get('payments')), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

self.create_sales_invoice(qty=1, rate=300)
self.create_sales_invoice(qty=1, rate=400)
self.create_sales_invoice(qty=1, rate=500)
self.create_payment_entry(amount=300).save().submit()
self.create_payment_entry(amount=400).save().submit()
self.create_payment_entry(amount=500).save().submit()
pr = self.create_payment_reconciliation()
pr.minimum_invoice_amount = 400
pr.maximum_invoice_amount = 500
pr.minimum_payment_amount = 300
pr.maximum_payment_amount = 600
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 3)
pr.minimum_invoice_amount = 300
pr.maximum_invoice_amount = 600
pr.minimum_payment_amount = 400
pr.maximum_payment_amount = 500
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 3)
self.assertEqual(len(pr.get('payments')), 2)
pr.minimum_invoice_amount = pr.maximum_invoice_amount = pr.minimum_payment_amount = pr.maximum_payment_amount = 0
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 3)
self.assertEqual(len(pr.get('payments')), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:324*

### test_filter_posting_date

**Category**: workflow  
**Description**: Workflow: test filter posting date  
**Expected**: self.assertEqual(len(pr.get('payments')), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

date1 = nowdate()
date2 = add_days(nowdate(), -1)
amount = 100
self.create_sales_invoice(qty=1, rate=amount, posting_date=date1)
si2 = self.create_sales_invoice(qty=1, rate=amount, posting_date=date2, do_not_save=True, do_not_submit=True)
si2.set_posting_time = 1
si2.posting_date = date2
si2.save().submit()
self.create_payment_entry(amount=amount, posting_date=date1).save().submit()
self.create_payment_entry(amount=amount, posting_date=date2).save().submit()
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.to_invoice_date = date1
pr.from_payment_date = pr.to_payment_date = date1
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(len(pr.get('payments')), 1)
pr.from_invoice_date = date2
pr.to_invoice_date = date1
pr.from_payment_date = date2
pr.to_payment_date = date1
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:357*

### test_filter_posting_date_case2

**Category**: workflow  
**Description**: Workflow: Posting date should not affect outstanding amount calculation  
**Expected**: self.assertEqual(len(pr.invoices), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

'\n\t\tPosting date should not affect outstanding amount calculation\n\t\t'
from_date = add_days(nowdate(), -30)
to_date = nowdate()
self.create_payment_entry(amount=25, posting_date=from_date).submit()
self.create_sales_invoice(rate=25, qty=1, posting_date=to_date)
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.from_payment_date = from_date
pr.to_invoice_date = pr.to_payment_date = to_date
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 1)
self.assertEqual(len(pr.payments), 1)
invoices = [x.as_dict() for x in pr.invoices]
payments = [x.as_dict() for x in pr.payments]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 0)
self.assertEqual(len(pr.payments), 0)
pr.from_invoice_date = pr.from_payment_date = to_date
pr.to_invoice_date = pr.to_payment_date = to_date
pr.get_unreconciled_entries()
self.assertEqual(len(pr.invoices), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:391*

### test_filter_invoice_limit

**Category**: workflow  
**Description**: Workflow: test filter invoice limit  
**Expected**: self.assertEqual(len(pr.get('payments')), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
rate = 100
invoices = []
payments = []
for _i in range(5):
    invoices.append(self.create_sales_invoice(qty=1, rate=rate, posting_date=transaction_date))
    pe = self.create_payment_entry(amount=rate, posting_date=transaction_date).save().submit()
    payments.append(pe)
pr = self.create_payment_reconciliation()
pr.from_invoice_date = pr.to_invoice_date = transaction_date
pr.from_payment_date = pr.to_payment_date = transaction_date
pr.invoice_limit = 2
pr.payment_limit = 3
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 2)
self.assertEqual(len(pr.get('payments')), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:426*

### test_payment_against_invoice

**Category**: workflow  
**Description**: Workflow: test payment against invoice  
**Expected**: self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 165)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

si = self.create_sales_invoice(qty=1, rate=200)
pe = self.create_payment_entry(amount=55).save().submit()
self.create_payment_entry(amount=35).save().submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
si.reload()
self.assertEqual(si.status, 'Partly Paid')
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 110)
self.assertEqual(pr.get('payments'), [])
pe.reload()
pe.cancel()
pr.get_unreconciled_entries()
self.assertEqual(len(pr.get('invoices')), 1)
self.assertEqual(len(pr.get('payments')), 0)
self.assertEqual(pr.get('invoices')[0].get('outstanding_amount'), 165)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:447*

### test_payment_against_journal

**Category**: workflow  
**Description**: Workflow: test payment against journal  
**Expected**: self.assertEqual(len(pr.get('payments')), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
sales = 'Sales - _PR'
amount = 921
je = self.create_journal_entry(self.debit_to, sales, amount, transaction_date)
je.accounts[0].party_type = 'Customer'
je.accounts[0].party = self.customer
je.save()
je.submit()
self.create_payment_entry(amount=amount, posting_date=transaction_date).save().submit()
pr = self.create_payment_reconciliation()
pr.minimum_invoice_amount = pr.maximum_invoice_amount = amount
pr.from_invoice_date = pr.to_invoice_date = transaction_date
pr.from_payment_date = pr.to_payment_date = transaction_date
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
self.assertEqual(len(pr.get('invoices')), 0)
self.assertEqual(len(pr.get('payments')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:483*

### test_journal_against_invoice

**Category**: workflow  
**Description**: Workflow: test journal against invoice  
**Expected**: self.assertEqual(len(pr.get('payments')), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
je = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
je.accounts[1].party_type = 'Customer'
je.accounts[1].party = self.customer
je.save()
je.submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
si.reload()
self.assertEqual(si.status, 'Paid')
self.assertEqual(si.outstanding_amount, 0)
self.assertEqual(len(pr.get('invoices')), 0)
self.assertEqual(len(pr.get('payments')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:602*

### test_negative_debit_or_credit_journal_against_invoice

**Category**: workflow  
**Description**: Workflow: test negative debit or credit journal against invoice  
**Expected**: self.assertEqual(len(pr.get('payments')), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
je = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
je.accounts[1].party_type = 'Customer'
je.accounts[1].party = self.customer
je.accounts[1].credit_in_account_currency = 0
je.accounts[1].debit_in_account_currency = -1 * amount
je.save()
je.submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
si.reload()
self.assertEqual(si.status, 'Paid')
self.assertEqual(si.outstanding_amount, 0)
self.assertEqual(len(pr.get('invoices')), 0)
self.assertEqual(len(pr.get('payments')), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:636*

### test_journal_against_journal

**Category**: workflow  
**Description**: Workflow: test journal against journal  
**Expected**: self.assertEqual(pr.get('payments'), [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
sales = 'Sales - _PR'
amount = 100
je1 = self.create_journal_entry(self.debit_to, sales, amount, transaction_date)
je1.accounts[0].party_type = 'Customer'
je1.accounts[0].party = self.customer
je1.save()
je1.submit()
je2 = self.create_journal_entry(self.bank, self.debit_to, amount, transaction_date)
je2.accounts[1].party_type = 'Customer'
je2.accounts[1].party = self.customer
je2.save()
je2.submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
self.assertEqual(pr.get('invoices'), [])
self.assertEqual(pr.get('payments'), [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:672*

### test_cr_note_against_invoice

**Category**: workflow  
**Description**: Workflow: test cr note against invoice  
**Expected**: self.assertEqual(si.outstanding_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_customer()
self.create_account()
self.create_cost_center()
self.clear_old_entries()

transaction_date = nowdate()
amount = 100
si = self.create_sales_invoice(qty=1, rate=amount, posting_date=transaction_date)
cr_note = self.create_sales_invoice(qty=-1, rate=amount, posting_date=transaction_date, do_not_save=True, do_not_submit=True)
cr_note.is_return = 1
cr_note = cr_note.save().submit()
pr = self.create_payment_reconciliation()
pr.get_unreconciled_entries()
invoices = [x.as_dict() for x in pr.get('invoices')]
payments = [x.as_dict() for x in pr.get('payments')]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
for row in pr.allocation:
    self.assertEqual(flt(row.get('difference_amount')), 0.0)
pr.reconcile()
pr.get_unreconciled_entries()
self.assertEqual(pr.get('invoices'), [])
self.assertEqual(pr.get('payments'), [])
si.reload()
self.assertEqual(si.status, 'Paid')
self.assertEqual(si.outstanding_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_reconciliation/test_payment_reconciliation.py:707*

### test_gl_entries_in_base_currency

**Category**: workflow  
**Description**: Workflow: test gl entries in base currency  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=200)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account)
gle = get_gl_entries('Invoice Discounting', inv_disc.name)
expected_gle = {inv.debit_to: [0.0, 200], self.ar_credit: [200, 0.0]}
for _i, gle_value in enumerate(gle):
    self.assertEqual([gle_value.debit, gle_value.credit], expected_gle.get(gle_value.account))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:62*

### test_on_disbursed

**Category**: workflow  
**Description**: Workflow: test on disbursed  
**Expected**: self.assertEqual(inv.outstanding_amount, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=500)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, bank_charges=100)
je = inv_disc.create_disbursement_entry()
self.assertEqual(je.accounts[0].account, self.bank_account)
self.assertEqual(je.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount) - flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[1].account, self.bank_charges_account)
self.assertEqual(je.accounts[1].debit_in_account_currency, flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[2].account, self.short_term_loan)
self.assertEqual(je.accounts[2].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je.accounts[3].account, self.ar_discounted)
self.assertEqual(je.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je.accounts[4].account, self.ar_credit)
self.assertEqual(je.accounts[4].credit_in_account_currency, flt(inv.outstanding_amount))
je.posting_date = nowdate()
je.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Disbursed')
inv.reload()
self.assertEqual(inv.outstanding_amount, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:96*

### test_on_close_after_loan_period

**Category**: workflow  
**Description**: Workflow: test on close after loan period  
**Expected**: self.assertEqual(inv_disc.status, 'Settled')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=600)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je2 = inv_disc.close_loan()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[2].account, self.ar_discounted)
self.assertEqual(je2.accounts[2].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je2.accounts[3].account, self.ar_unpaid)
self.assertEqual(je2.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
je2.posting_date = nowdate()
je2.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Settled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:138*

### test_on_close_after_loan_period_after_inv_payment

**Category**: workflow  
**Description**: Workflow: test on close after loan period after inv payment  
**Expected**: self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=600)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
je_on_payment.posting_date = nowdate()
je_on_payment.cheque_no = '126981'
je_on_payment.cheque_date = nowdate()
je_on_payment.save()
je_on_payment.submit()
je2 = inv_disc.close_loan()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:176*

### test_on_close_before_loan_period

**Category**: workflow  
**Description**: Workflow: test on close before loan period  
**Expected**: self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=700)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=add_days(nowdate(), -80), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je2 = inv_disc.close_loan()
je2.posting_date = nowdate()
je2.submit()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:209*

### test_make_payment_before_loan_period

**Category**: workflow  
**Description**: Workflow: test make payment before loan period  
**Expected**: self.assertEqual(inv.outstanding_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=700)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account)
je = inv_disc.create_disbursement_entry()
inv_disc.reload()
je.posting_date = nowdate()
je.submit()
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
je_on_payment.posting_date = nowdate()
je_on_payment.cheque_no = '126981'
je_on_payment.cheque_date = nowdate()
je_on_payment.save()
je_on_payment.submit()
self.assertEqual(je_on_payment.accounts[0].account, self.ar_discounted)
self.assertEqual(je_on_payment.accounts[0].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je_on_payment.accounts[1].account, self.bank_account)
self.assertEqual(je_on_payment.accounts[1].debit_in_account_currency, flt(inv.outstanding_amount))
inv.reload()
self.assertEqual(inv.outstanding_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:237*

### test_make_payment_before_after_period

**Category**: workflow  
**Description**: Workflow: test make payment before after period  
**Expected**: self.assertEqual(inv.outstanding_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.ar_credit = create_account(account_name='_Test Accounts Receivable Credit', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_discounted = create_account(account_name='_Test Accounts Receivable Discounted', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.ar_unpaid = create_account(account_name='_Test Accounts Receivable Unpaid', parent_account='Accounts Receivable - _TC', company='_Test Company')
self.short_term_loan = create_account(account_name='_Test Short Term Loan', parent_account='Source of Funds (Liabilities) - _TC', company='_Test Company')
self.bank_account = create_account(account_name='_Test Bank 2', parent_account='Bank Accounts - _TC', company='_Test Company')
self.bank_charges_account = create_account(account_name='_Test Bank Charges Account', parent_account='Expenses - _TC', company='_Test Company')
frappe.db.set_value('Company', '_Test Company', 'default_bank_account', self.bank_account)

inv = create_sales_invoice(rate=700)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, loan_start_date=add_days(nowdate(), -10), period=5)
je = inv_disc.create_disbursement_entry()
inv_disc.reload()
je.posting_date = nowdate()
je.submit()
je = inv_disc.close_loan()
inv_disc.reload()
je.posting_date = nowdate()
je.submit()
je_on_payment = frappe.get_doc(get_payment_entry_against_invoice('Sales Invoice', inv.name))
je_on_payment.posting_date = nowdate()
je_on_payment.cheque_no = '126981'
je_on_payment.cheque_date = nowdate()
je_on_payment.submit()
self.assertEqual(je_on_payment.accounts[0].account, self.ar_unpaid)
self.assertEqual(je_on_payment.accounts[0].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je_on_payment.accounts[1].account, self.bank_account)
self.assertEqual(je_on_payment.accounts[1].debit_in_account_currency, flt(inv.outstanding_amount))
inv.reload()
self.assertEqual(inv.outstanding_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:269*

### test_gl_entries_in_base_currency

**Category**: workflow  
**Description**: Workflow: test gl entries in base currency  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_sales_invoice(rate=200)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account)
gle = get_gl_entries('Invoice Discounting', inv_disc.name)
expected_gle = {inv.debit_to: [0.0, 200], self.ar_credit: [200, 0.0]}
for _i, gle_value in enumerate(gle):
    self.assertEqual([gle_value.debit, gle_value.credit], expected_gle.get(gle_value.account))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:62*

### test_on_disbursed

**Category**: workflow  
**Description**: Workflow: test on disbursed  
**Expected**: self.assertEqual(inv.outstanding_amount, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_sales_invoice(rate=500)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, bank_charges=100)
je = inv_disc.create_disbursement_entry()
self.assertEqual(je.accounts[0].account, self.bank_account)
self.assertEqual(je.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount) - flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[1].account, self.bank_charges_account)
self.assertEqual(je.accounts[1].debit_in_account_currency, flt(inv_disc.bank_charges))
self.assertEqual(je.accounts[2].account, self.short_term_loan)
self.assertEqual(je.accounts[2].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je.accounts[3].account, self.ar_discounted)
self.assertEqual(je.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je.accounts[4].account, self.ar_credit)
self.assertEqual(je.accounts[4].credit_in_account_currency, flt(inv.outstanding_amount))
je.posting_date = nowdate()
je.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Disbursed')
inv.reload()
self.assertEqual(inv.outstanding_amount, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:96*

### test_on_close_after_loan_period

**Category**: workflow  
**Description**: Workflow: test on close after loan period  
**Expected**: self.assertEqual(inv_disc.status, 'Settled')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_sales_invoice(rate=600)
inv_disc = create_invoice_discounting([inv.name], accounts_receivable_credit=self.ar_credit, accounts_receivable_discounted=self.ar_discounted, accounts_receivable_unpaid=self.ar_unpaid, short_term_loan=self.short_term_loan, bank_charges_account=self.bank_charges_account, bank_account=self.bank_account, start=nowdate(), period=60)
je1 = inv_disc.create_disbursement_entry()
je1.posting_date = nowdate()
je1.submit()
je2 = inv_disc.close_loan()
self.assertEqual(je2.accounts[0].account, self.short_term_loan)
self.assertEqual(je2.accounts[0].debit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[1].account, self.bank_account)
self.assertEqual(je2.accounts[1].credit_in_account_currency, flt(inv_disc.total_amount))
self.assertEqual(je2.accounts[2].account, self.ar_discounted)
self.assertEqual(je2.accounts[2].credit_in_account_currency, flt(inv.outstanding_amount))
self.assertEqual(je2.accounts[3].account, self.ar_unpaid)
self.assertEqual(je2.accounts[3].debit_in_account_currency, flt(inv.outstanding_amount))
je2.posting_date = nowdate()
je2.submit()
inv_disc.reload()
self.assertEqual(inv_disc.status, 'Settled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/invoice_discounting/test_invoice_discounting.py:138*

### test_offsetting_entries_for_accounting_dimensions

**Category**: workflow  
**Description**: Workflow: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.accounts.doctype.account.test_account import create_account
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_fiscal_year
self.company = create_company()
create_cost_center(cost_center_name='Test Cost Center', company='Trial Balance Company', parent_cost_center='Trial Balance Company - TBC')
create_account(account_name='Offsetting', company='Trial Balance Company', parent_account='Temporary Accounts - TBC')
self.fiscal_year = get_fiscal_year(today(), company='Trial Balance Company')[0]
create_accounting_dimension()

'\n\t\tChecks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension\n\t\t'
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
frappe.db.sql("delete from `tabSales Invoice` where company='Trial Balance Company'")
frappe.db.sql("delete from `tabGL Entry` where company='Trial Balance Company'")
branch1 = frappe.new_doc('Branch')
branch1.branch = 'Location 1'
branch1.insert(ignore_if_duplicate=True)
branch2 = frappe.new_doc('Branch')
branch2.branch = 'Location 2'
branch2.insert(ignore_if_duplicate=True)
si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
si.branch = 'Location 1'
si.items[0].branch = 'Location 2'
si.save()
si.submit()
filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
total_row = execute(filters)[1][-1]
self.assertEqual(total_row['debit'], total_row['credit'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:31*

### test_offsetting_entries_for_accounting_dimensions

**Category**: workflow  
**Description**: Workflow: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tChecks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension\n\t\t'
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
frappe.db.sql("delete from `tabSales Invoice` where company='Trial Balance Company'")
frappe.db.sql("delete from `tabGL Entry` where company='Trial Balance Company'")
branch1 = frappe.new_doc('Branch')
branch1.branch = 'Location 1'
branch1.insert(ignore_if_duplicate=True)
branch2 = frappe.new_doc('Branch')
branch2.branch = 'Location 2'
branch2.insert(ignore_if_duplicate=True)
si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
si.branch = 'Location 1'
si.items[0].branch = 'Location 2'
si.save()
si.submit()
filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
total_row = execute(filters)[1][-1]
self.assertEqual(total_row['debit'], total_row['credit'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:31*

### test_purchase_register

**Category**: workflow  
**Description**: Workflow: test purchase register  
**Expected**: self.assertEqual(first_row.grand_total, 1100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today())
pi = make_purchase_invoice()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][0])
self.assertEqual(first_row.voucher_type, 'Purchase Invoice')
self.assertEqual(first_row.voucher_no, pi.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.net_total, 1000)
self.assertEqual(first_row.total_tax, 100)
self.assertEqual(first_row.grand_total, 1100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:12*

### test_purchase_register_ledger_view

**Category**: workflow  
**Description**: Workflow: test purchase register ledger view  
**Expected**: self.assertEqual(first_row.balance, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today(), include_payments=True, supplier='_Test Supplier')
make_purchase_invoice()
pe = make_payment_entry()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][2])
self.assertEqual(first_row.voucher_type, 'Payment Entry')
self.assertEqual(first_row.voucher_no, pe.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.debit, 0)
self.assertEqual(first_row.credit, 600)
self.assertEqual(first_row.balance, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:29*

### test_purchase_register

**Category**: workflow  
**Description**: Workflow: test purchase register  
**Expected**: self.assertEqual(first_row.grand_total, 1100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today())
pi = make_purchase_invoice()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][0])
self.assertEqual(first_row.voucher_type, 'Purchase Invoice')
self.assertEqual(first_row.voucher_no, pi.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.net_total, 1000)
self.assertEqual(first_row.total_tax, 100)
self.assertEqual(first_row.grand_total, 1100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:12*

### test_purchase_register_ledger_view

**Category**: workflow  
**Description**: Workflow: test purchase register ledger view  
**Expected**: self.assertEqual(first_row.balance, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabPurchase Invoice` where company='_Test Company 6'")
frappe.db.sql("delete from `tabGL Entry` where company='_Test Company 6'")
filters = frappe._dict(company='_Test Company 6', from_date=add_months(today(), -1), to_date=today(), include_payments=True, supplier='_Test Supplier')
make_purchase_invoice()
pe = make_payment_entry()
report_results = execute(filters)
first_row = frappe._dict(report_results[1][2])
self.assertEqual(first_row.voucher_type, 'Payment Entry')
self.assertEqual(first_row.voucher_no, pe.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.debit, 0)
self.assertEqual(first_row.credit, 600)
self.assertEqual(first_row.balance, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:29*

### test_monthly_budget_crossed_stop2

**Category**: workflow  
**Description**: Workflow: test monthly budget crossed stop2  
**Expected**: self.assertRaises(BudgetError, jv.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

set_total_expense_zero(nowdate(), 'project')
budget = make_budget(budget_against='Project', do_not_save=False, submit_budget=True)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, '_Test Cost Center - _TC', project=project, posting_date=nowdate())
self.assertRaises(BudgetError, jv.submit)
budget.load_from_db()
budget.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:179*

### test_monthly_budget_on_cancellation1

**Category**: workflow  
**Description**: Workflow: test monthly budget on cancellation1  
**Expected**: self.assertRaises(BudgetError, jv.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

set_total_expense_zero(nowdate(), 'cost_center')
budget = make_budget(budget_against='Cost Center', do_not_save=False, submit_budget=True)
month = now_datetime().month
if month > 9:
    month = 9
for _i in range(month + 1):
    jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 20000, '_Test Cost Center - _TC', posting_date=nowdate(), submit=True)
    self.assertTrue(frappe.db.get_value('GL Entry', {'voucher_type': 'Journal Entry', 'voucher_no': jv.name}))
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
self.assertRaises(BudgetError, jv.cancel)
budget.load_from_db()
budget.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:242*

### test_monthly_budget_on_cancellation2

**Category**: workflow  
**Description**: Workflow: test monthly budget on cancellation2  
**Expected**: self.assertRaises(BudgetError, jv.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

set_total_expense_zero(nowdate(), 'project')
budget = make_budget(budget_against='Project', do_not_save=False, submit_budget=True)
month = now_datetime().month
if month > 9:
    month = 9
project = frappe.get_value('Project', {'project_name': '_Test Project'})
for _i in range(month + 1):
    jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', 20000, '_Test Cost Center - _TC', posting_date=nowdate(), submit=True, project=project)
    self.assertTrue(frappe.db.get_value('GL Entry', {'voucher_type': 'Journal Entry', 'voucher_no': jv.name}))
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
self.assertRaises(BudgetError, jv.cancel)
budget.load_from_db()
budget.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:271*

### test_monthly_budget_against_parent_group_cost_center

**Category**: workflow  
**Description**: Workflow: test monthly budget against parent group cost center  
**Expected**: self.assertRaises(BudgetError, jv.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

cost_center = '_Test Cost Center 3 - _TC'
if not frappe.db.exists('Cost Center', cost_center):
    frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Cost Center 3', 'parent_cost_center': '_Test Company - _TC', 'company': '_Test Company', 'is_group': 0}).insert(ignore_permissions=True)
budget = make_budget(budget_against='Cost Center', cost_center=cost_center, do_not_save=False, submit_budget=True)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, cost_center, posting_date=nowdate())
self.assertRaises(BudgetError, jv.submit)
budget.load_from_db()
budget.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:331*

### test_action_for_cumulative_limit

**Category**: workflow  
**Description**: Workflow: test action for cumulative limit  
**Expected**: self.assertRaises(BudgetError, po.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

set_total_expense_zero(nowdate(), 'cost_center')
budget = make_budget(budget_against='Cost Center', applicable_on_cumulative_expense=True, do_not_save=False, submit_budget=True)
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit - 1, '_Test Cost Center - _TC', posting_date=nowdate())
jv.submit()
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Stop')
po = create_purchase_order(transaction_date=nowdate(), qty=1, rate=accumulated_limit + 1, do_not_submit=True)
po.set_missing_values()
self.assertRaises(BudgetError, po.submit)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_exceeded_on_cumulative_expense', 'Ignore')
po.submit()
budget.load_from_db()
budget.cancel()
po.cancel()
jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:406*

### test_create_revised_budget

**Category**: workflow  
**Description**: Workflow: test create revised budget  
**Expected**: self.assertEqual(old_budget.docstatus, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
revised_name = revise_budget(budget.name)
revised_budget = frappe.get_doc('Budget', revised_name)
self.assertNotEqual(budget.name, revised_budget.name)
self.assertEqual(revised_budget.budget_against, budget.budget_against)
self.assertEqual(revised_budget.budget_amount, budget.budget_amount)
old_budget = frappe.get_doc('Budget', budget.name)
self.assertEqual(old_budget.docstatus, 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:494*

### test_revision_preserves_distribution

**Category**: workflow  
**Description**: Workflow: test revision preserves distribution  
**Expected**: self.assertEqual(total, revised_budget.budget_amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

set_total_expense_zero(nowdate(), 'cost_center', '_Test Cost Center - _TC')
budget = make_budget(budget_against='Cost Center', budget_amount=120000, do_not_save=False, submit_budget=True)
revised_name = revise_budget(budget.name)
revised_budget = frappe.get_doc('Budget', revised_name)
self.assertGreater(len(revised_budget.budget_distribution), 0)
total = sum((row.amount for row in revised_budget.budget_distribution))
self.assertEqual(total, revised_budget.budget_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:509*

### test_fiscal_year_company_mismatch

**Category**: workflow  
**Description**: Workflow: test fiscal year company mismatch  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

budget = make_budget(budget_against='Cost Center', do_not_save=True, submit_budget=False)
fy = frappe.get_doc({'doctype': 'Fiscal Year', 'year': '2099', 'year_start_date': '2099-04-01', 'year_end_date': '2100-03-31', 'companies': [{'company': '_Test Company 2'}]}).insert(ignore_permissions=True)
budget.from_fiscal_year = fy.name
budget.to_fiscal_year = fy.name
budget.company = '_Test Company'
with self.assertRaises(frappe.ValidationError):
    budget.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:549*

### test_duplicate_budget_validation

**Category**: workflow  
**Description**: Workflow: test duplicate budget validation  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Accounts Settings', 'use_legacy_budget_controller', False)
self.company = '_Test Company'
self.fiscal_year = frappe.db.get_value('Fiscal Year', {}, 'name')
self.account = '_Test Account Cost for Goods Sold - _TC'
self.cost_center = '_Test Cost Center - _TC'

budget = make_budget(budget_against='Cost Center', distribute_equally=1, budget_amount=15000, do_not_save=False, submit_budget=True)
new_budget = frappe.new_doc('Budget')
new_budget.company = '_Test Company'
new_budget.from_fiscal_year = budget.from_fiscal_year
new_budget.to_fiscal_year = new_budget.from_fiscal_year
new_budget.budget_against = 'Cost Center'
new_budget.cost_center = '_Test Cost Center - _TC'
new_budget.account = '_Test Account Cost for Goods Sold - _TC'
new_budget.budget_amount = 10000
with self.assertRaises(frappe.ValidationError):
    new_budget.insert()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:585*

### test_monthly_budget_crossed_stop2

**Category**: workflow  
**Description**: Workflow: test monthly budget crossed stop2  
**Expected**: self.assertRaises(BudgetError, jv.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
set_total_expense_zero(nowdate(), 'project')
budget = make_budget(budget_against='Project', do_not_save=False, submit_budget=True)
frappe.db.set_value('Budget', budget.name, 'action_if_accumulated_monthly_budget_exceeded', 'Stop')
project = frappe.get_value('Project', {'project_name': '_Test Project'})
accumulated_limit = get_accumulated_monthly_budget(budget.name, nowdate())
jv = make_journal_entry('_Test Account Cost for Goods Sold - _TC', '_Test Bank - _TC', accumulated_limit + 1, '_Test Cost Center - _TC', project=project, posting_date=nowdate())
self.assertRaises(BudgetError, jv.submit)
budget.load_from_db()
budget.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/budget/test_budget.py:179*

### test_supplier_ledger_summary_with_filters

**Category**: workflow  
**Description**: Workflow: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

self.create_purchase_invoice()
supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
filters = {'company': self.company, 'from_date': today(), 'to_date': today(), 'supplier_group': supplier_group}
expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
report_output = execute(filters)[1]
self.assertEqual(len(report_output), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report_output[0].get(field), expected.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:63*

### test_supplier_ledger_summary_with_filters

**Category**: workflow  
**Description**: Workflow: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_purchase_invoice()
supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
filters = {'company': self.company, 'from_date': today(), 'to_date': today(), 'supplier_group': supplier_group}
expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
report_output = execute(filters)[1]
self.assertEqual(len(report_output), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report_output[0].get(field), expected.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:63*

### test_01_revaluation_of_forex_balance

**Category**: workflow  
**Description**: Workflow: Test Forex account balance and Journal creation post Revaluation  
**Expected**: self.assertEqual(acc_balance.balance, 8500.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

'\n\t\tTest Forex account balance and Journal creation post Revaluation\n\t\t'
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
err = frappe.new_doc('Exchange Rate Revaluation')
err.company = self.company
err.posting_date = today()
accounts = err.get_accounts_data()
err.extend('accounts', accounts)
row = err.accounts[0]
row.new_exchange_rate = 85
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
err.set_total_gain_loss()
err = err.save().submit()
err_journals = err.make_jv_entries()
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
je = je.submit()
je.reload()
self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
self.assertEqual(je.total_debit, 8500.0)
self.assertEqual(je.total_credit, 8500.0)
gl = DocType('GL Entry')
acc_balance = frappe.db.get_all('GL Entry', filters={'account': self.debtors_usd, 'is_cancelled': 0}, fields=[(functions.Sum(gl.debit) - functions.Sum(gl.credit)).as_('balance')])[0]
self.assertEqual(acc_balance.balance, 8500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:44*

### test_04_get_account_details_function

**Category**: workflow  
**Description**: Workflow: test 04 get account details function  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
from erpnext.accounts.doctype.exchange_rate_revaluation.exchange_rate_revaluation import get_account_details
account_details = get_account_details(self.company, si.posting_date, self.debtors_usd, 'Customer', self.customer, 0.05)
expected_data = {'account_currency': 'USD', 'balance_in_base_currency': 8000.0, 'balance_in_account_currency': 100.0, 'current_exchange_rate': 80.0, 'zero_balance': False, 'new_balance_in_account_currency': 100.0}
for key, _val in expected_data.items():
    self.assertEqual(expected_data.get(key), account_details.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:266*

### test_01_revaluation_of_forex_balance

**Category**: workflow  
**Description**: Workflow: Test Forex account balance and Journal creation post Revaluation  
**Expected**: self.assertEqual(acc_balance.balance, 8500.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest Forex account balance and Journal creation post Revaluation\n\t\t'
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
err = frappe.new_doc('Exchange Rate Revaluation')
err.company = self.company
err.posting_date = today()
accounts = err.get_accounts_data()
err.extend('accounts', accounts)
row = err.accounts[0]
row.new_exchange_rate = 85
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
err.set_total_gain_loss()
err = err.save().submit()
err_journals = err.make_jv_entries()
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
je = je.submit()
je.reload()
self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
self.assertEqual(je.total_debit, 8500.0)
self.assertEqual(je.total_credit, 8500.0)
gl = DocType('GL Entry')
acc_balance = frappe.db.get_all('GL Entry', filters={'account': self.debtors_usd, 'is_cancelled': 0}, fields=[(functions.Sum(gl.debit) - functions.Sum(gl.credit)).as_('balance')])[0]
self.assertEqual(acc_balance.balance, 8500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:44*

### test_04_get_account_details_function

**Category**: workflow  
**Description**: Workflow: test 04 get account details function  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, price_list_rate=100, do_not_submit=1)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
from erpnext.accounts.doctype.exchange_rate_revaluation.exchange_rate_revaluation import get_account_details
account_details = get_account_details(self.company, si.posting_date, self.debtors_usd, 'Customer', self.customer, 0.05)
expected_data = {'account_currency': 'USD', 'balance_in_base_currency': 8000.0, 'balance_in_account_currency': 100.0, 'current_exchange_rate': 80.0, 'zero_balance': False, 'new_balance_in_account_currency': 100.0}
for key, _val in expected_data.items():
    self.assertEqual(expected_data.get(key), account_details.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:266*

### test_profit_and_loss_output_and_summary

**Category**: workflow  
**Description**: Workflow: test profit and loss output and summary  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity, company=filters.company)
result = execute(filters)[1]
current_period = next((x for x in period_list if x.from_date <= getdate() and x.to_date >= getdate()))
current_period_key = current_period.key
without_current_period = [x for x in period_list if x.key != current_period.key]
for acc in result:
    if acc:
        with self.subTest(acc=acc):
            for period in without_current_period:
                self.assertEqual(acc[period.key], 0)
for acc in result:
    if acc:
        with self.subTest(current_period_key=current_period_key):
            self.assertEqual(acc[current_period_key], 150)
            self.assertEqual(acc['total'], 150)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:64*

### test_p_and_l_export

**Category**: workflow  
**Description**: Workflow: test p and l export  
**Expected**: self.assertIn(sales_account, contents)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
frappe.local.form_dict = frappe._dict({'report_name': 'Profit and Loss Statement', 'file_format_type': 'CSV', 'filters': filters, 'visible_idx': [0, 1, 2, 3, 4, 5, 6]})
export_query()
contents = frappe.response['filecontent'].decode()
sales_account = frappe.db.get_value('Company', self.company, 'default_income_account')
self.assertIn(sales_account, contents)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:95*

### test_accumulate_filter

**Category**: workflow  
**Description**: Workflow: test accumulate filter  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

cur_fy = self.get_fiscal_year()
find_for = add_days(cur_fy.year_start_date, -1)
_x = frappe.db.get_all('Fiscal Year', filters={'disabled': 0, 'year_start_date': ('<=', find_for), 'year_end_date': ('>=', find_for)})[0]
prev_fy = frappe.get_doc('Fiscal Year', _x.name)
prev_fy.append('companies', {'company': self.company})
prev_fy.save()
prev_fy_si = self.create_sales_invoice(qty=1, rate=450, do_not_submit=True)
prev_fy_si.posting_date = add_days(prev_fy.year_end_date, -1)
prev_fy_si.save().submit()
income_acc = prev_fy_si.items[0].income_account
self.create_sales_invoice(qty=1, rate=120)
filters = frappe._dict(company=self.company, from_fiscal_year=prev_fy.name, to_fiscal_year=cur_fy.name, period_start_date=prev_fy.year_start_date, period_end_date=cur_fy.year_end_date, filter_based_on='Date Range', periodicity='Yearly', accumulated_values=False)
result = execute(filters)
columns = [result[0][4], result[0][5]]
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 120.0}
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
filters.update({'accumulated_values': True})
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 570.0}
result = execute(filters)
columns = [result[0][4], result[0][5]]
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:113*

### test_profit_and_loss_output_and_summary

**Category**: workflow  
**Description**: Workflow: test profit and loss output and summary  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity, company=filters.company)
result = execute(filters)[1]
current_period = next((x for x in period_list if x.from_date <= getdate() and x.to_date >= getdate()))
current_period_key = current_period.key
without_current_period = [x for x in period_list if x.key != current_period.key]
for acc in result:
    if acc:
        with self.subTest(acc=acc):
            for period in without_current_period:
                self.assertEqual(acc[period.key], 0)
for acc in result:
    if acc:
        with self.subTest(current_period_key=current_period_key):
            self.assertEqual(acc[current_period_key], 150)
            self.assertEqual(acc['total'], 150)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:64*

### test_p_and_l_export

**Category**: workflow  
**Description**: Workflow: test p and l export  
**Expected**: self.assertIn(sales_account, contents)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_sales_invoice(qty=1, rate=150)
filters = self.get_report_filters()
frappe.local.form_dict = frappe._dict({'report_name': 'Profit and Loss Statement', 'file_format_type': 'CSV', 'filters': filters, 'visible_idx': [0, 1, 2, 3, 4, 5, 6]})
export_query()
contents = frappe.response['filecontent'].decode()
sales_account = frappe.db.get_value('Company', self.company, 'default_income_account')
self.assertIn(sales_account, contents)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:95*

### test_accumulate_filter

**Category**: workflow  
**Description**: Workflow: test accumulate filter  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
cur_fy = self.get_fiscal_year()
find_for = add_days(cur_fy.year_start_date, -1)
_x = frappe.db.get_all('Fiscal Year', filters={'disabled': 0, 'year_start_date': ('<=', find_for), 'year_end_date': ('>=', find_for)})[0]
prev_fy = frappe.get_doc('Fiscal Year', _x.name)
prev_fy.append('companies', {'company': self.company})
prev_fy.save()
prev_fy_si = self.create_sales_invoice(qty=1, rate=450, do_not_submit=True)
prev_fy_si.posting_date = add_days(prev_fy.year_end_date, -1)
prev_fy_si.save().submit()
income_acc = prev_fy_si.items[0].income_account
self.create_sales_invoice(qty=1, rate=120)
filters = frappe._dict(company=self.company, from_fiscal_year=prev_fy.name, to_fiscal_year=cur_fy.name, period_start_date=prev_fy.year_start_date, period_end_date=cur_fy.year_end_date, filter_based_on='Date Range', periodicity='Yearly', accumulated_values=False)
result = execute(filters)
columns = [result[0][4], result[0][5]]
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 120.0}
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
filters.update({'accumulated_values': True})
expected = {'account': income_acc, columns[0].get('fieldname'): 450.0, columns[1].get('fieldname'): 570.0}
result = execute(filters)
columns = [result[0][4], result[0][5]]
actual = [x for x in result[1] if x.get('account') == income_acc]
self.assertEqual(len(actual), 1)
actual = actual[0]
for key in expected.keys():
    with self.subTest(key=key):
        self.assertEqual(expected.get(key), actual.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:113*

### test_get_mode_of_payments

**Category**: workflow  
**Description**: Workflow: test get mode of payments  
**Expected**: self.assertTrue('Cash' not in next(iter(mop.values())))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = get_filters()
for _dummy in range(2):
    si = create_sales_invoice_record()
    si.insert()
    si.submit()
    if int(si.name[-3:]) % 2 == 0:
        bank_account = '_Test Cash - _TC'
        mode_of_payment = 'Cash'
    else:
        bank_account = '_Test Bank - _TC'
        mode_of_payment = 'Credit Card'
    pe = get_payment_entry('Sales Invoice', si.name, bank_account=bank_account)
    pe.reference_no = '_Test'
    pe.reference_date = today()
    pe.mode_of_payment = mode_of_payment
    pe.insert()
    pe.submit()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' in next(iter(mop.values())))
payment_entries = frappe.get_all('Payment Entry', filters={'mode_of_payment': 'Cash', 'docstatus': 1}, fields=['name', 'docstatus'])
for payment_entry in payment_entries:
    pe = frappe.get_doc('Payment Entry', payment_entry.name)
    pe.cancel()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' not in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:32*

### test_get_mode_of_payments

**Category**: workflow  
**Description**: Workflow: test get mode of payments  
**Expected**: self.assertTrue('Cash' not in next(iter(mop.values())))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = get_filters()
for _dummy in range(2):
    si = create_sales_invoice_record()
    si.insert()
    si.submit()
    if int(si.name[-3:]) % 2 == 0:
        bank_account = '_Test Cash - _TC'
        mode_of_payment = 'Cash'
    else:
        bank_account = '_Test Bank - _TC'
        mode_of_payment = 'Credit Card'
    pe = get_payment_entry('Sales Invoice', si.name, bank_account=bank_account)
    pe.reference_no = '_Test'
    pe.reference_date = today()
    pe.mode_of_payment = mode_of_payment
    pe.insert()
    pe.submit()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' in next(iter(mop.values())))
payment_entries = frappe.get_all('Payment Entry', filters={'mode_of_payment': 'Cash', 'docstatus': 1}, fields=['name', 'docstatus'])
for payment_entry in payment_entries:
    pe = frappe.get_doc('Payment Entry', payment_entry.name)
    pe.cancel()
mop = get_mode_of_payments(filters)
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' not in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:32*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: workflow  
**Description**: Workflow: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('currency'), 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_supplier(currency='USD', supplier_name='Test Supplier2')
self.create_usd_payable_account()

pi = self.create_purchase_invoice(do_not_submit=True)
pi.currency = 'USD'
pi.conversion_rate = 80
pi.credit_to = self.creditors_usd
pi = pi.save().submit()
filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
data = execute(filters)
self.assertEqual(data[1][0].get('outstanding'), 300)
self.assertEqual(data[1][0].get('currency'), 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:21*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: workflow  
**Description**: Workflow: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('currency'), 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = self.create_purchase_invoice(do_not_submit=True)
pi.currency = 'USD'
pi.conversion_rate = 80
pi.credit_to = self.creditors_usd
pi = pi.save().submit()
filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
data = execute(filters)
self.assertEqual(data[1][0].get('outstanding'), 300)
self.assertEqual(data[1][0].get('currency'), 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:21*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: workflow  
**Description**: Workflow: test child company with different default currency from parent company  
**Expected**: self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = frappe._dict({'company': ['Parent Group Company India', 'Child Company US'], 'fiscal_year': self.fiscal_year})
report = execute(filters)
total_row = report[1][-1]
exchange_rate = get_exchange_rate('USD', 'INR')
fctr = [d for d in report[1] if d.get('account') == _('Foreign Currency Translation Reserve')]
if not fctr:
    raise ForeignCurrencyTranslationReserveNotFoundError
ccu_total_credit = 1000 * flt(exchange_rate)
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:75*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: workflow  
**Description**: Workflow: test child company with different default currency from parent company  
**Expected**: self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = frappe._dict({'company': ['Parent Group Company India', 'Child Company US'], 'fiscal_year': self.fiscal_year})
report = execute(filters)
total_row = report[1][-1]
exchange_rate = get_exchange_rate('USD', 'INR')
fctr = [d for d in report[1] if d.get('account') == _('Foreign Currency Translation Reserve')]
if not fctr:
    raise ForeignCurrencyTranslationReserveNotFoundError
ccu_total_credit = 1000 * flt(exchange_rate)
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:75*

### test_closing_entry

**Category**: workflow  
**Description**: Workflow: test closing entry  
**Expected**: self.assertEqual(pcv_gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
jv1.submit()
jv2 = make_journal_entry(posting_date='2021-03-15', amount=600, account1='Cost of Goods Sold - TPC', account2='Cash - TPC', cost_center=cost_center, company=company, save=False)
jv2.company = company
jv2.save()
jv2.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = (('Cost of Goods Sold - TPC', 0.0, 600.0), (surplus_account, 200.0, 0.0), ('Sales - TPC', 400.0, 0.0))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit from `tabGL Entry` where voucher_no=%s order by account\n\t\t', pcv.name)
pcv.reload()
self.assertEqual(pcv.gle_processing_status, 'Completed')
self.assertEqual(pcv_gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:19*

### test_cost_center_wise_posting

**Category**: workflow  
**Description**: Workflow: test cost center wise posting  
**Expected**: self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center1 = create_cost_center('Main')
cost_center2 = create_cost_center('Western Branch')
create_sales_invoice(company=company, cost_center=cost_center1, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
create_sales_invoice(company=company, cost_center=cost_center2, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=200, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
pcv = self.make_period_closing_voucher(posting_date='2021-03-31', submit=False)
pcv.save()
pcv.submit()
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, cost_center1), (surplus_account, 0.0, 200.0, cost_center2), ('Sales - TPC', 400.0, 0.0, cost_center1), ('Sales - TPC', 200.0, 0.0, cost_center2))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, cost_center\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, cost_center\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
pcv.reload()
pcv.cancel()
self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:71*

### test_period_closing_with_finance_book_entries

**Category**: workflow  
**Description**: Workflow: test period closing with finance book entries  
**Expected**: self.assertSequenceEqual(pcv_gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center = create_cost_center('Test Cost Center 1')
create_sales_invoice(company=company, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', cost_center=cost_center, rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
jv = make_journal_entry(account1='Cash - TPC', account2='Sales - TPC', amount=400, cost_center=cost_center, posting_date='2021-03-15', company=company)
jv.company = company
jv.finance_book = create_finance_book().name
jv.save()
jv.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, None), (surplus_account, 0.0, 400.0, jv.finance_book), ('Sales - TPC', 400.0, 0.0, None), ('Sales - TPC', 400.0, 0.0, jv.finance_book))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, finance_book\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, finance_book\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:137*

### test_gl_entries_restrictions

**Category**: workflow  
**Description**: Workflow: test gl entries restrictions  
**Expected**: self.assertRaises(frappe.ValidationError, jv1.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
self.make_period_closing_voucher(posting_date='2021-03-31')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
self.assertRaises(frappe.ValidationError, jv1.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:191*

### test_closing_entry

**Category**: workflow  
**Description**: Workflow: test closing entry  
**Expected**: self.assertEqual(pcv_gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
jv1.submit()
jv2 = make_journal_entry(posting_date='2021-03-15', amount=600, account1='Cost of Goods Sold - TPC', account2='Cash - TPC', cost_center=cost_center, company=company, save=False)
jv2.company = company
jv2.save()
jv2.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = (('Cost of Goods Sold - TPC', 0.0, 600.0), (surplus_account, 200.0, 0.0), ('Sales - TPC', 400.0, 0.0))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit from `tabGL Entry` where voucher_no=%s order by account\n\t\t', pcv.name)
pcv.reload()
self.assertEqual(pcv.gle_processing_status, 'Completed')
self.assertEqual(pcv_gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:19*

### test_cost_center_wise_posting

**Category**: workflow  
**Description**: Workflow: test cost center wise posting  
**Expected**: self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center1 = create_cost_center('Main')
cost_center2 = create_cost_center('Western Branch')
create_sales_invoice(company=company, cost_center=cost_center1, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
create_sales_invoice(company=company, cost_center=cost_center2, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', rate=200, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
pcv = self.make_period_closing_voucher(posting_date='2021-03-31', submit=False)
pcv.save()
pcv.submit()
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, cost_center1), (surplus_account, 0.0, 200.0, cost_center2), ('Sales - TPC', 400.0, 0.0, cost_center1), ('Sales - TPC', 200.0, 0.0, cost_center2))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, cost_center\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, cost_center\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
pcv.reload()
pcv.cancel()
self.assertFalse(frappe.db.get_value('GL Entry', {'voucher_type': 'Period Closing Voucher', 'voucher_no': pcv.name, 'is_cancelled': 0}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:71*

### test_period_closing_with_finance_book_entries

**Category**: workflow  
**Description**: Workflow: test period closing with finance book entries  
**Expected**: self.assertSequenceEqual(pcv_gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
surplus_account = create_account()
cost_center = create_cost_center('Test Cost Center 1')
create_sales_invoice(company=company, income_account='Sales - TPC', expense_account='Cost of Goods Sold - TPC', cost_center=cost_center, rate=400, debit_to='Debtors - TPC', currency='USD', customer='_Test Customer USD', posting_date='2021-03-15')
jv = make_journal_entry(account1='Cash - TPC', account2='Sales - TPC', amount=400, cost_center=cost_center, posting_date='2021-03-15', company=company)
jv.company = company
jv.finance_book = create_finance_book().name
jv.save()
jv.submit()
pcv = self.make_period_closing_voucher(posting_date='2021-03-31')
surplus_account = pcv.closing_account_head
expected_gle = ((surplus_account, 0.0, 400.0, None), (surplus_account, 0.0, 400.0, jv.finance_book), ('Sales - TPC', 400.0, 0.0, None), ('Sales - TPC', 400.0, 0.0, jv.finance_book))
pcv_gle = frappe.db.sql('\n\t\t\tselect account, debit, credit, finance_book\n\t\t\tfrom `tabGL Entry` where voucher_no=%s\n\t\t\torder by account, finance_book\n\t\t', pcv.name)
self.assertSequenceEqual(pcv_gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:137*

### test_gl_entries_restrictions

**Category**: workflow  
**Description**: Workflow: test gl entries restrictions  
**Expected**: self.assertRaises(frappe.ValidationError, jv1.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.sql("delete from `tabGL Entry` where company='Test PCV Company'")
frappe.db.sql("delete from `tabPeriod Closing Voucher` where company='Test PCV Company'")
company = create_company()
cost_center = create_cost_center('Test Cost Center 1')
self.make_period_closing_voucher(posting_date='2021-03-31')
jv1 = make_journal_entry(posting_date='2021-03-15', amount=400, account1='Cash - TPC', account2='Sales - TPC', cost_center=cost_center, company=company, save=False)
jv1.company = company
jv1.save()
self.assertRaises(frappe.ValidationError, jv1.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:191*

### test_pos_profile

**Category**: workflow  
**Description**: Workflow: test pos profile  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_pos_profile()
pos_profile = get_pos_profile('_Test Company') or {}
if pos_profile:
    doc = frappe.get_doc('POS Profile', pos_profile.get('name'))
    doc.append('item_groups', {'item_group': '_Test Item Group'})
    doc.append('customer_groups', {'customer_group': '_Test Customer Group'})
    doc.save()
    items = get_items_list(doc, doc.company)
    customers = get_customers_list(doc)
    products_count = frappe.db.sql(" select count(name) from tabItem where item_group = '_Test Item Group'", as_list=1)
    customers_count = frappe.db.sql(" select count(name) from tabCustomer where customer_group = '_Test Customer Group'")
    self.assertEqual(len(items), products_count[0][0])
    self.assertEqual(len(customers), customers_count[0][0])
frappe.db.sql('delete from `tabPOS Profile`')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:17*

### test_disabled_pos_profile_after_completing_session

**Category**: workflow  
**Description**: Workflow: test disabled pos profile after completing session  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
from erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry import create_opening_entry
test_user, pos_profile = init_user_and_profile()
if pos_profile:
    opening_entry = create_opening_entry(pos_profile, test_user.name)
    closing_entry = make_closing_entry_from_opening(opening_entry)
    closing_entry.submit()
    pos_profile.disabled = 1
    pos_profile.save()
    pos_profile.reload()
    self.assertEqual(pos_profile.disabled, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:62*

### test_pos_profile

**Category**: workflow  
**Description**: Workflow: test pos profile  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_pos_profile()
pos_profile = get_pos_profile('_Test Company') or {}
if pos_profile:
    doc = frappe.get_doc('POS Profile', pos_profile.get('name'))
    doc.append('item_groups', {'item_group': '_Test Item Group'})
    doc.append('customer_groups', {'customer_group': '_Test Customer Group'})
    doc.save()
    items = get_items_list(doc, doc.company)
    customers = get_customers_list(doc)
    products_count = frappe.db.sql(" select count(name) from tabItem where item_group = '_Test Item Group'", as_list=1)
    customers_count = frappe.db.sql(" select count(name) from tabCustomer where customer_group = '_Test Customer Group'")
    self.assertEqual(len(items), products_count[0][0])
    self.assertEqual(len(customers), customers_count[0][0])
frappe.db.sql('delete from `tabPOS Profile`')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:17*

### test_disabled_pos_profile_after_completing_session

**Category**: workflow  
**Description**: Workflow: test disabled pos profile after completing session  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
from erpnext.accounts.doctype.pos_opening_entry.test_pos_opening_entry import create_opening_entry
test_user, pos_profile = init_user_and_profile()
if pos_profile:
    opening_entry = create_opening_entry(pos_profile, test_user.name)
    closing_entry = make_closing_entry_from_opening(opening_entry)
    closing_entry.submit()
    pos_profile.disabled = 1
    pos_profile.save()
    pos_profile.reload()
    self.assertEqual(pos_profile.disabled, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:62*

### test_loyalty_points_earned_single_tier

**Category**: workflow  
**Description**: Workflow: test loyalty points earned single tier  
**Expected**: self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
for d in [si_redeem, si_original]:
    d.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:23*

### test_loyalty_points_earned_multiple_tier

**Category**: workflow  
**Description**: Workflow: test loyalty points earned multiple tier  
**Expected**: self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Multiple Loyalty')
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
customer.loyalty_program = frappe.get_doc('Loyalty Program', {'loyalty_program_name': 'Test Multiple Loyalty'}).name
customer.save()
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer.reload()
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
customer.reload()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)
for d in [si_redeem, si_original]:
    d.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:72*

### test_sales_invoice_return

**Category**: workflow  
**Description**: Workflow: test sales invoice return  
**Expected**: self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record(2)
si_original.conversion_rate = flt(1)
si_original.insert()
si_original.submit()
earned_points = get_points_earned(si_original)
lpe_original = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_original.loyalty_points, earned_points)
si_return = create_sales_invoice_record(-1)
si_return.conversion_rate = flt(1)
si_return.is_return = 1
si_return.return_against = si_original.name
si_return.insert()
si_return.submit()
si_original = frappe.get_doc('Sales Invoice', lpe_original.invoice)
earned_points = get_points_earned(si_original)
lpe_after_return = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_after_return.loyalty_points, earned_points)
self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)
for d in [si_return, si_original]:
    try:
        d.cancel()
    except frappe.TimestampMismatchError:
        frappe.get_doc('Sales Invoice', d.name).cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:148*

### test_tier_selection

**Category**: workflow  
**Description**: Workflow: test tier selection  
**Confidence**: 0.90  
**Tags**: mock, unittest, workflow, integration  

```python
loyalty_program = frappe.get_doc({'doctype': 'Loyalty Program', 'loyalty_program_name': 'Test Tier Selection', 'auto_opt_in': 1, 'from_date': today(), 'loyalty_program_type': 'Multiple Tier Program', 'conversion_factor': 1, 'expiry_duration': 10, 'company': '_Test Company', 'cost_center': 'Main - _TC', 'expense_account': 'Loyalty - _TC', 'collection_rules': [{'tier_name': 'Gold', 'collection_factor': 1000, 'min_spent': 20000}, {'tier_name': 'Silver', 'collection_factor': 1000, 'min_spent': 10000}, {'tier_name': 'Bronze', 'collection_factor': 1000, 'min_spent': 0}]})
loyalty_program.insert()
test_cases = [(0, 6000, 'Bronze'), (0, 15000, 'Silver'), (0, 25000, 'Gold'), (4000, 500, 'Bronze'), (8000, 3000, 'Silver'), (18000, 3000, 'Gold'), (22000, 5000, 'Gold')]
for total_spent, current_transaction_amount, expected_tier in test_cases:
    with self.subTest(total_spent=total_spent, current_transaction_amount=current_transaction_amount):

        def side_effect(*args, **kwargs):
            result = get_loyalty_details(*args, **kwargs)
            result.update({'total_spent': total_spent})
            return result
        mock_get_loyalty_details.side_effect = side_effect
        lp_details = get_loyalty_program_details_with_points('Test Loyalty Customer', loyalty_program=loyalty_program.name, company='_Test Company', current_transaction_amount=current_transaction_amount)
        selected_tier = lp_details.tier_name
        self.assertEqual(selected_tier, expected_tier, f'Expected tier {expected_tier} for total_spent {total_spent} and current_transaction_amount {current_transaction_amount}, but got {selected_tier}')
loyalty_program.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:205*

### test_loyalty_points_earned_single_tier

**Category**: workflow  
**Description**: Workflow: test loyalty points earned single tier  
**Expected**: self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
for d in [si_redeem, si_original]:
    d.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:23*

### test_loyalty_points_earned_multiple_tier

**Category**: workflow  
**Description**: Workflow: test loyalty points earned multiple tier  
**Expected**: self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Multiple Loyalty')
customer = frappe.get_doc('Customer', {'customer_name': 'Test Loyalty Customer'})
customer.loyalty_program = frappe.get_doc('Loyalty Program', {'loyalty_program_name': 'Test Multiple Loyalty'}).name
customer.save()
si_original = create_sales_invoice_record()
si_original.insert()
si_original.submit()
customer.reload()
earned_points = get_points_earned(si_original)
lpe = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
self.assertEqual(lpe.loyalty_points, earned_points)
si_redeem = create_sales_invoice_record()
si_redeem.redeem_loyalty_points = 1
si_redeem.loyalty_points = earned_points
si_redeem.insert()
si_redeem.submit()
customer.reload()
earned_after_redemption = get_points_earned(si_redeem)
lpe_redeem = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'redeem_against': lpe.name})
lpe_earn = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_redeem.name, 'name': ['!=', lpe_redeem.name]})
self.assertEqual(lpe_earn.loyalty_points, earned_after_redemption)
self.assertEqual(lpe_redeem.loyalty_points, -1 * earned_points)
self.assertEqual(lpe_earn.loyalty_program_tier, customer.loyalty_program_tier)
for d in [si_redeem, si_original]:
    d.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:72*

### test_sales_invoice_return

**Category**: workflow  
**Description**: Workflow: test sales invoice return  
**Expected**: self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
frappe.db.set_value('Customer', 'Test Loyalty Customer', 'loyalty_program', 'Test Single Loyalty')
si_original = create_sales_invoice_record(2)
si_original.conversion_rate = flt(1)
si_original.insert()
si_original.submit()
earned_points = get_points_earned(si_original)
lpe_original = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_original.loyalty_points, earned_points)
si_return = create_sales_invoice_record(-1)
si_return.conversion_rate = flt(1)
si_return.is_return = 1
si_return.return_against = si_original.name
si_return.insert()
si_return.submit()
si_original = frappe.get_doc('Sales Invoice', lpe_original.invoice)
earned_points = get_points_earned(si_original)
lpe_after_return = frappe.get_doc('Loyalty Point Entry', {'invoice_type': 'Sales Invoice', 'invoice': si_original.name, 'customer': si_original.customer})
self.assertEqual(lpe_after_return.loyalty_points, earned_points)
self.assertEqual(True, lpe_original.loyalty_points > lpe_after_return.loyalty_points)
for d in [si_return, si_original]:
    try:
        d.cancel()
    except frappe.TimestampMismatchError:
        frappe.get_doc('Sales Invoice', d.name).cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:148*

### test_tier_selection

**Category**: workflow  
**Description**: Workflow: test tier selection  
**Confidence**: 0.90  
**Tags**: mock, unittest, workflow, integration  

```python
# Setup
# Fixtures: mock_get_loyalty_details

loyalty_program = frappe.get_doc({'doctype': 'Loyalty Program', 'loyalty_program_name': 'Test Tier Selection', 'auto_opt_in': 1, 'from_date': today(), 'loyalty_program_type': 'Multiple Tier Program', 'conversion_factor': 1, 'expiry_duration': 10, 'company': '_Test Company', 'cost_center': 'Main - _TC', 'expense_account': 'Loyalty - _TC', 'collection_rules': [{'tier_name': 'Gold', 'collection_factor': 1000, 'min_spent': 20000}, {'tier_name': 'Silver', 'collection_factor': 1000, 'min_spent': 10000}, {'tier_name': 'Bronze', 'collection_factor': 1000, 'min_spent': 0}]})
loyalty_program.insert()
test_cases = [(0, 6000, 'Bronze'), (0, 15000, 'Silver'), (0, 25000, 'Gold'), (4000, 500, 'Bronze'), (8000, 3000, 'Silver'), (18000, 3000, 'Gold'), (22000, 5000, 'Gold')]
for total_spent, current_transaction_amount, expected_tier in test_cases:
    with self.subTest(total_spent=total_spent, current_transaction_amount=current_transaction_amount):

        def side_effect(*args, **kwargs):
            result = get_loyalty_details(*args, **kwargs)
            result.update({'total_spent': total_spent})
            return result
        mock_get_loyalty_details.side_effect = side_effect
        lp_details = get_loyalty_program_details_with_points('Test Loyalty Customer', loyalty_program=loyalty_program.name, company='_Test Company', current_transaction_amount=current_transaction_amount)
        selected_tier = lp_details.tier_name
        self.assertEqual(selected_tier, expected_tier, f'Expected tier {expected_tier} for total_spent {total_spent} and current_transaction_amount {current_transaction_amount}, but got {selected_tier}')
loyalty_program.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:205*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

si = self.create_sales_invoice(rate=98)
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'voucher_type': si.doctype, 'voucher_no': si.name, 'posting_date': getdate(), 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'grand_total': 98.0, 'debit': 98.0}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:56*

### test_journal_with_cost_center_filter

**Category**: workflow  
**Description**: Workflow: test journal with cost center filter  
**Expected**: self.assertDictEqual(result_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

je1 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 77, 'credit': 77, 'is_advance': 'Yes', 'cost_center': self.cost_center}, {'account': self.cash, 'debit_in_account_currency': 77, 'debit': 77}]})
je1.submit()
je2 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 98, 'credit': 98, 'is_advance': 'Yes', 'cost_center': self.south_cc}, {'account': self.cash, 'debit_in_account_currency': 98, 'debit': 98}]})
je2.submit()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.cost_center})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je1.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'posting_date': je1.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 77.0, 'credit': 77.0}
result_fields = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_fields, expected_result)
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.south_cc})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je2.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je2.doctype, 'voucher_no': je2.name, 'posting_date': je2.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'credit': 98.0}
result_output = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:78*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = self.create_sales_invoice(rate=98)
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'voucher_type': si.doctype, 'voucher_no': si.name, 'posting_date': getdate(), 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'grand_total': 98.0, 'debit': 98.0}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:56*

### test_journal_with_cost_center_filter

**Category**: workflow  
**Description**: Workflow: test journal with cost center filter  
**Expected**: self.assertDictEqual(result_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
je1 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 77, 'credit': 77, 'is_advance': 'Yes', 'cost_center': self.cost_center}, {'account': self.cash, 'debit_in_account_currency': 77, 'debit': 77}]})
je1.submit()
je2 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 98, 'credit': 98, 'is_advance': 'Yes', 'cost_center': self.south_cc}, {'account': self.cash, 'debit_in_account_currency': 98, 'debit': 98}]})
je2.submit()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.cost_center})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je1.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je1.doctype, 'voucher_no': je1.name, 'posting_date': je1.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 77.0, 'credit': 77.0}
result_fields = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_fields, expected_result)
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.south_cc})
report_output = execute(filters)[1]
filtered_output = [x for x in report_output if x.get('voucher_no') == je2.name]
self.assertEqual(len(filtered_output), 1)
expected_result = {'voucher_type': je2.doctype, 'voucher_no': je2.name, 'posting_date': je2.posting_date, 'customer': self.customer, 'receivable_account': self.debit_to, 'net_total': 98.0, 'credit': 98.0}
result_output = {k: v for k, v in filtered_output[0].items() if k in expected_result}
self.assertDictEqual(result_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:78*

### test_so_advance_paid_and_currency_with_payment

**Category**: workflow  
**Description**: Workflow: test so advance paid and currency with payment  
**Expected**: self.assertEqual(so.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

self.create_customer('_Test USD Customer', 'USD')
so = self.create_sales_order(currency='USD', do_not_submit=True)
so.conversion_rate = 80
so.submit()
pe_exchange_rate = 85
pe = get_payment_entry(so.doctype, so.name, bank_account=self.cash)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from = self.debtors_usd
pe.paid_from_account_currency = 'USD'
pe.source_exchange_rate = pe_exchange_rate
pe.paid_amount = so.grand_total
pe.received_amount = pe_exchange_rate * pe.paid_amount
pe.references[0].outstanding_amount = 100
pe.references[0].total_amount = 100
pe.references[0].allocated_amount = 100
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
pe.reload()
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:68*

### test_so_advance_paid_and_currency_with_journal

**Category**: workflow  
**Description**: Workflow: test so advance paid and currency with journal  
**Expected**: self.assertEqual(so.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

self.create_customer('_Test USD Customer', 'USD')
so = self.create_sales_order(currency='USD', do_not_submit=True)
so.conversion_rate = 80
so.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': so.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.debtors_usd, 'party_type': 'Customer', 'party': so.customer, 'credit': 8500, 'credit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': so.doctype, 'reference_name': so.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'debit': 8500, 'debit_in_account_currency': 8500}]})
je.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
je.reload()
je.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:101*

### test_po_advance_paid_and_currency_with_payment

**Category**: workflow  
**Description**: Workflow: test po advance paid and currency with payment  
**Expected**: self.assertEqual(po.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

self.create_supplier('_Test USD Supplier', 'USD')
po = self.create_purchase_order(currency='USD', do_not_submit=True)
po.conversion_rate = 80
po.submit()
pe_exchange_rate = 85
pe = get_payment_entry(po.doctype, po.name, bank_account=self.cash)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_to = self.creditors_usd
pe.paid_to_account_currency = 'USD'
pe.target_exchange_rate = pe_exchange_rate
pe.received_amount = po.grand_total
pe.paid_amount = pe_exchange_rate * pe.received_amount
pe.references[0].outstanding_amount = 100
pe.references[0].total_amount = 100
pe.references[0].allocated_amount = 100
pe.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
self.assertEqual(po.party_account_currency, 'USD')
pe.reload()
pe.cancel()
po.reload()
self.assertEqual(po.advance_paid, 0)
self.assertEqual(po.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:149*

### test_po_advance_paid_and_currency_with_journal

**Category**: workflow  
**Description**: Workflow: test po advance paid and currency with journal  
**Expected**: self.assertEqual(po.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

self.create_supplier('_Test USD Supplier', 'USD')
po = self.create_purchase_order(currency='USD', do_not_submit=True)
po.conversion_rate = 80
po.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.creditors_usd, 'party_type': 'Supplier', 'party': po.supplier, 'debit': 8500, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'credit': 8500, 'credit_in_account_currency': 8500}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
self.assertEqual(po.party_account_currency, 'USD')
je.reload()
je.cancel()
po.reload()
self.assertEqual(po.advance_paid, 0)
self.assertEqual(po.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:182*

### test_so_advance_paid_and_currency_with_payment

**Category**: workflow  
**Description**: Workflow: test so advance paid and currency with payment  
**Expected**: self.assertEqual(so.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_customer('_Test USD Customer', 'USD')
so = self.create_sales_order(currency='USD', do_not_submit=True)
so.conversion_rate = 80
so.submit()
pe_exchange_rate = 85
pe = get_payment_entry(so.doctype, so.name, bank_account=self.cash)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from = self.debtors_usd
pe.paid_from_account_currency = 'USD'
pe.source_exchange_rate = pe_exchange_rate
pe.paid_amount = so.grand_total
pe.received_amount = pe_exchange_rate * pe.paid_amount
pe.references[0].outstanding_amount = 100
pe.references[0].total_amount = 100
pe.references[0].allocated_amount = 100
pe.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
pe.reload()
pe.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:68*

### test_so_advance_paid_and_currency_with_journal

**Category**: workflow  
**Description**: Workflow: test so advance paid and currency with journal  
**Expected**: self.assertEqual(so.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_customer('_Test USD Customer', 'USD')
so = self.create_sales_order(currency='USD', do_not_submit=True)
so.conversion_rate = 80
so.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': so.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.debtors_usd, 'party_type': 'Customer', 'party': so.customer, 'credit': 8500, 'credit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': so.doctype, 'reference_name': so.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'debit': 8500, 'debit_in_account_currency': 8500}]})
je.save().submit()
so.reload()
self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
je.reload()
je.cancel()
so.reload()
self.assertEqual(so.advance_paid, 0)
self.assertEqual(so.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:101*

### test_po_advance_paid_and_currency_with_payment

**Category**: workflow  
**Description**: Workflow: test po advance paid and currency with payment  
**Expected**: self.assertEqual(po.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_supplier('_Test USD Supplier', 'USD')
po = self.create_purchase_order(currency='USD', do_not_submit=True)
po.conversion_rate = 80
po.submit()
pe_exchange_rate = 85
pe = get_payment_entry(po.doctype, po.name, bank_account=self.cash)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_to = self.creditors_usd
pe.paid_to_account_currency = 'USD'
pe.target_exchange_rate = pe_exchange_rate
pe.received_amount = po.grand_total
pe.paid_amount = pe_exchange_rate * pe.received_amount
pe.references[0].outstanding_amount = 100
pe.references[0].total_amount = 100
pe.references[0].allocated_amount = 100
pe.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
self.assertEqual(po.party_account_currency, 'USD')
pe.reload()
pe.cancel()
po.reload()
self.assertEqual(po.advance_paid, 0)
self.assertEqual(po.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:149*

### test_po_advance_paid_and_currency_with_journal

**Category**: workflow  
**Description**: Workflow: test po advance paid and currency with journal  
**Expected**: self.assertEqual(po.party_account_currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_supplier('_Test USD Supplier', 'USD')
po = self.create_purchase_order(currency='USD', do_not_submit=True)
po.conversion_rate = 80
po.submit()
je_exchange_rate = 85
je = frappe.get_doc({'doctype': 'Journal Entry', 'company': self.company, 'voucher_type': 'Journal Entry', 'posting_date': po.transaction_date, 'multi_currency': True, 'accounts': [{'account': self.creditors_usd, 'party_type': 'Supplier', 'party': po.supplier, 'debit': 8500, 'debit_in_account_currency': 100, 'is_advance': 'Yes', 'reference_type': po.doctype, 'reference_name': po.name, 'exchange_rate': je_exchange_rate}, {'account': self.cash, 'credit': 8500, 'credit_in_account_currency': 8500}]})
je.save().submit()
po.reload()
self.assertEqual(po.advance_paid, 100)
self.assertEqual(po.party_account_currency, 'USD')
je.reload()
je.cancel()
po.reload()
self.assertEqual(po.advance_paid, 0)
self.assertEqual(po.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:182*

### test_sales_invoice_change_naming_series

**Category**: workflow  
**Description**: Workflow: test sales invoice change naming series  
**Expected**: self.assertRaises(frappe.CannotChangeConstantError, si.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][2])
si.insert()
si.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, si.save)
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][1])
si.insert()
si.naming_series = 'TEST-'
self.assertRaises(frappe.CannotChangeConstantError, si.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:138*

### test_payment_entry_unlink_against_invoice

**Category**: workflow  
**Description**: Workflow: test payment entry unlink against invoice  
**Expected**: self.assertRaises(frappe.LinkExistsError, si.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

from erpnext.accounts.doctype.payment_entry.test_payment_entry import get_payment_entry
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][0])
si.is_pos = 0
si.insert()
si.submit()
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank - _TC')
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.paid_from_account_currency = si.currency
pe.paid_to_account_currency = si.currency
pe.source_exchange_rate = 1
pe.target_exchange_rate = 1
pe.paid_amount = si.outstanding_amount
pe.insert()
pe.submit()
unlink_payment_on_cancel_of_invoice(0)
si = frappe.get_doc('Sales Invoice', si.name)
self.assertRaises(frappe.LinkExistsError, si.cancel)
unlink_payment_on_cancel_of_invoice()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:208*

### test_payment_entry_unlink_against_standalone_credit_note

**Category**: workflow  
**Description**: Workflow: test payment entry unlink against standalone credit note  
**Expected**: self.assertRaises(PaymentEntryUnlinkError, si1.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

from erpnext.accounts.doctype.payment_entry.test_payment_entry import get_payment_entry
si1 = create_sales_invoice(rate=1000)
si2 = create_sales_invoice(rate=300)
si3 = create_sales_invoice(qty=-1, rate=300, is_return=1)
pe = get_payment_entry('Sales Invoice', si1.name, bank_account='_Test Bank - _TC')
pe.append('references', {'reference_doctype': 'Sales Invoice', 'reference_name': si2.name, 'total_amount': si2.grand_total, 'outstanding_amount': si2.outstanding_amount, 'allocated_amount': si2.outstanding_amount})
pe.append('references', {'reference_doctype': 'Sales Invoice', 'reference_name': si3.name, 'total_amount': si3.grand_total, 'outstanding_amount': si3.outstanding_amount, 'allocated_amount': si3.outstanding_amount})
pe.reference_no = 'Test001'
pe.reference_date = nowdate()
pe.save()
pe.submit()
si2.load_from_db()
si2.cancel()
si1.load_from_db()
self.assertRaises(PaymentEntryUnlinkError, si1.cancel)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:235*

### test_sales_invoice_calculation_export_currency

**Category**: workflow  
**Description**: Workflow: test sales invoice calculation export currency  
**Expected**: self.assertEqual(si.grand_total, 32.54)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][2])
si.currency = 'USD'
si.conversion_rate = 50
si.get('items')[0].rate = 1
si.get('items')[0].price_list_rate = 1
si.get('items')[1].rate = 3
si.get('items')[1].price_list_rate = 3
si.get('taxes')[0].tax_amount = 2
si.insert()
expected_values = {'keys': ['price_list_rate', 'discount_percentage', 'rate', 'amount', 'base_price_list_rate', 'base_rate', 'base_amount'], '_Test Item Home Desktop 100': [1, 0, 1, 10, 50, 50, 500], '_Test Item Home Desktop 200': [3, 0, 3, 15, 150, 150, 750]}
self.assertEqual(len(si.get('items')), len(expected_values) - 1)
for d in si.get('items'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.item_code][i])
self.assertEqual(si.total, 25)
self.assertEqual(si.base_total, 1250)
self.assertEqual(si.net_total, 25)
self.assertEqual(si.base_net_total, 1250)
expected_values = {'keys': ['base_tax_amount', 'base_total', 'tax_amount', 'total'], '_Test Account Shipping Charges - _TC': [100, 1350, 2, 27], '_Test Account Customs Duty - _TC': [125, 1475, 2.5, 29.5], '_Test Account Excise Duty - _TC': [140, 1615, 2.8, 32.3], '_Test Account Education Cess - _TC': [3, 1618, 0.06, 32.36], '_Test Account S&H Education Cess - _TC': [1.5, 1619.5, 0.03, 32.39], '_Test Account CST - _TC': [32.5, 1652, 0.65, 33.04], '_Test Account VAT - _TC': [156.0, 1808.0, 3.12, 36.16], '_Test Account Discount - _TC': [-181.0, 1627.0, -3.62, 32.54]}
for d in si.get('taxes'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.account_head][i])
self.assertEqual(si.base_grand_total, 1627.0)
self.assertEqual(si.grand_total, 32.54)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:276*

### test_sales_invoice_with_discount_and_inclusive_tax

**Category**: workflow  
**Description**: Workflow: test sales invoice with discount and inclusive tax  
**Expected**: self.assertEqual(si.grand_total, 4900.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = create_sales_invoice(qty=100, rate=50, do_not_save=True)
si.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 14, 'included_in_print_rate': 1})
si.append('taxes', {'charge_type': 'On Item Quantity', 'account_head': '_Test Account Education Cess - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'CESS', 'rate': 5, 'included_in_print_rate': 1})
si.insert()
self.assertEqual(si.items[0].net_amount, 3947.37)
self.assertEqual(si.net_total, si.base_net_total)
self.assertEqual(si.net_total, 3947.37)
self.assertEqual(si.grand_total, 5000)
si.reload()
si.discount_amount = 100
si.apply_discount_on = 'Net Total'
si.payment_schedule = []
si.save()
self.assertEqual(si.net_total, 3847.37)
self.assertEqual(si.grand_total, 4886)
si.reload()
si.discount_amount = 100
si.apply_discount_on = 'Grand Total'
si.payment_schedule = []
si.save()
self.assertEqual(si.net_total, 3859.65)
self.assertEqual(si.grand_total, 4900.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:337*

### test_sales_invoice_discount_amount

**Category**: workflow  
**Description**: Workflow: test sales invoice discount amount  
**Expected**: self.assertEqual(si.rounding_adjustment, 0.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
si.discount_amount = 104.94
si.append('taxes', {'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
si.insert()
expected_values = [{'item_code': '_Test Item Home Desktop 100', 'price_list_rate': 62.5, 'discount_percentage': 0, 'rate': 62.5, 'amount': 625, 'base_price_list_rate': 62.5, 'base_rate': 62.5, 'base_amount': 625, 'net_rate': 46.54, 'net_amount': 465.37, 'base_net_rate': 46.54, 'base_net_amount': 465.37}, {'item_code': '_Test Item Home Desktop 200', 'price_list_rate': 190.66, 'discount_percentage': 0, 'rate': 190.66, 'amount': 953.3, 'base_price_list_rate': 190.66, 'base_rate': 190.66, 'base_amount': 953.3, 'net_rate': 139.62, 'net_amount': 698.08, 'base_net_rate': 139.62, 'base_net_amount': 698.08}]
self.assertEqual(len(si.get('items')), len(expected_values))
for i, d in enumerate(si.get('items')):
    for k, v in expected_values[i].items():
        self.assertEqual(d.get(k), v)
self.assertEqual(si.base_net_total, 1163.45)
self.assertEqual(si.total, 1578.3)
expected_values = {'keys': ['tax_amount', 'tax_amount_after_discount_amount', 'total'], '_Test Account Excise Duty - _TC': [140, 130.31, 1293.76], '_Test Account Education Cess - _TC': [2.8, 2.61, 1296.37], '_Test Account S&H Education Cess - _TC': [1.4, 1.3, 1297.67], '_Test Account CST - _TC': [27.88, 25.95, 1323.62], '_Test Account VAT - _TC': [156.25, 145.43, 1469.05], '_Test Account Customs Duty - _TC': [125, 116.34, 1585.39], '_Test Account Shipping Charges - _TC': [100, 100, 1685.39], '_Test Account Discount - _TC': [-180.33, -168.54, 1516.85], '_Test Account Service Tax - _TC': [-18.03, -16.85, 1500.0]}
for d in si.get('taxes'):
    for i, k in enumerate(expected_values['keys']):
        self.assertEqual(d.get(k), expected_values[d.account_head][i])
self.assertEqual(si.base_grand_total, 1500)
self.assertEqual(si.grand_total, 1500)
self.assertEqual(si.rounding_adjustment, 0.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:395*

### test_discount_amount_gl_entry

**Category**: workflow  
**Description**: Workflow: test discount amount gl entry  
**Expected**: self.assertTrue(gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

frappe.db.set_value('Company', '_Test Company', 'round_off_account', 'Round Off - _TC')
si = frappe.copy_doc(self.globalTestRecords['Sales Invoice'][3])
si.discount_amount = 104.94
si.append('taxes', {'doctype': 'Sales Taxes and Charges', 'charge_type': 'On Previous Row Amount', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 10, 'row_id': 8})
si.insert()
si.submit()
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Sales Invoice' and voucher_no=%s\n\t\t\torder by account asc", si.name, as_dict=1)
self.assertTrue(gl_entries)
expected_values = dict(((d[0], d) for d in [[si.debit_to, 1500, 0.0], [self.globalTestRecords['Sales Invoice'][3]['items'][0]['income_account'], 0.0, 1163.45], [self.globalTestRecords['Sales Invoice'][3]['taxes'][0]['account_head'], 0.0, 130.31], [self.globalTestRecords['Sales Invoice'][3]['taxes'][1]['account_head'], 0.0, 2.61], [self.globalTestRecords['Sales Invoice'][3]['taxes'][2]['account_head'], 0.0, 1.3], [self.globalTestRecords['Sales Invoice'][3]['taxes'][3]['account_head'], 0.0, 25.95], [self.globalTestRecords['Sales Invoice'][3]['taxes'][4]['account_head'], 0.0, 145.43], [self.globalTestRecords['Sales Invoice'][3]['taxes'][5]['account_head'], 0.0, 116.34], [self.globalTestRecords['Sales Invoice'][3]['taxes'][6]['account_head'], 0.0, 100], [self.globalTestRecords['Sales Invoice'][3]['taxes'][7]['account_head'], 168.54, 0.0], ['_Test Account Service Tax - _TC', 16.85, 0.0], ['Round Off - _TC', 0.01, 0.0]]))
for gle in gl_entries:
    self.assertEqual(expected_values[gle.account][0], gle.account)
    self.assertEqual(expected_values[gle.account][1], gle.debit)
    self.assertEqual(expected_values[gle.account][2], gle.credit)
si.cancel()
gle = frappe.db.sql("select * from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", si.name)
self.assertTrue(gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:476*

### test_tax_calculation_with_multiple_items

**Category**: workflow  
**Description**: Workflow: test tax calculation with multiple items  
**Expected**: self.assertEqual(si.grand_total, 5474.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = create_sales_invoice(qty=84, rate=4.6, do_not_save=True)
item_row = si.get('items')[0]
for qty in (54, 288, 144, 430):
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.qty = qty
    si.append('items', item_row_copy)
si.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 19})
si.insert()
self.assertEqual(si.net_total, 4600)
self.assertEqual(si.get('taxes')[0].tax_amount, 874.0)
self.assertEqual(si.get('taxes')[0].total, 5474.0)
self.assertEqual(si.grand_total, 5474.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:539*

### test_tax_calculation_with_item_tax_template

**Category**: workflow  
**Description**: Workflow: test tax calculation with item tax template  
**Expected**: self.assertEqual(si.rounded_total, 5676.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = create_sales_invoice(qty=84, rate=4.6, do_not_save=True)
item_row = si.get('items')[0]
add_items = [(54, '_Test Account Excise Duty @ 12 - _TC'), (288, '_Test Account Excise Duty @ 15 - _TC'), (144, '_Test Account Excise Duty @ 20 - _TC'), (430, '_Test Item Tax Template 1 - _TC')]
for qty, item_tax_template in add_items:
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.qty = qty
    item_row_copy.item_tax_template = item_tax_template
    si.append('items', item_row_copy)
si.append('taxes', {'account_head': '_Test Account Excise Duty - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Excise Duty', 'doctype': 'Sales Taxes and Charges', 'rate': 11})
si.append('taxes', {'account_head': '_Test Account Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 0})
si.append('taxes', {'account_head': '_Test Account S&H Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'S&H Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 3})
si.insert()
self.assertEqual(si.net_total, 4600)
self.assertEqual(si.get('taxes')[0].tax_amount, 502.41)
self.assertEqual(si.get('taxes')[0].total, 5102.41)
self.assertEqual(si.get('taxes')[1].tax_amount, 197.8)
self.assertEqual(si.get('taxes')[1].total, 5300.21)
self.assertEqual(si.get('taxes')[2].tax_amount, 375.36)
self.assertEqual(si.get('taxes')[2].total, 5675.57)
self.assertEqual(si.grand_total, 5675.57)
self.assertEqual(si.rounding_adjustment, 0.43)
self.assertEqual(si.rounded_total, 5676.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:567*

### test_tax_calculation_with_multiple_items_and_discount

**Category**: workflow  
**Description**: Workflow: test tax calculation with multiple items and discount  
**Expected**: self.assertEqual(si.grand_total, 1116.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
from erpnext.stock.doctype.stock_ledger_entry.test_stock_ledger_entry import create_items
create_items(['_Test Internal Transfer Item'], uoms=[{'uom': 'Box', 'conversion_factor': 10}])
create_internal_parties()
setup_accounts()
mode_of_payment = frappe.get_doc('Mode of Payment', 'Bank Draft')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company', '_Test Bank - _TC')
set_default_account_for_mode_of_payment(mode_of_payment, '_Test Company with perpetual inventory', '_Test Bank - TCP1')
for company in frappe.get_all('Company', pluck='name'):
    frappe.db.set_value('Company', company, 'accounts_frozen_till_date', None)

si = create_sales_invoice(qty=1, rate=75, do_not_save=True)
item_row = si.get('items')[0]
for rate in (500, 200, 100, 50, 50):
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.price_list_rate = rate
    item_row_copy.rate = rate
    si.append('items', item_row_copy)
si.apply_discount_on = 'Net Total'
si.discount_amount = 75.0
si.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 24})
si.insert()
self.assertEqual(si.total, 975)
self.assertEqual(si.net_total, 900)
self.assertEqual(si.get('taxes')[0].tax_amount, 216.0)
self.assertEqual(si.get('taxes')[0].total, 1116.0)
self.assertEqual(si.grand_total, 1116.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/sales_invoice/test_sales_invoice.py:633*

### test_payment_request_linkings

**Category**: workflow  
**Description**: Workflow: test payment request linkings  
**Expected**: self.assertEqual(pr.currency, 'USD')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:104*

### test_multiple_payment_entry_against_purchase_invoice

**Category**: workflow  
**Description**: Workflow: test multiple payment entry against purchase invoice  
**Expected**: self.assertEqual(purchase_invoice.status, 'Paid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

purchase_invoice = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
pr.grand_total = pr.grand_total / 2
pr.submit()
pr.create_payment_entry()
purchase_invoice.load_from_db()
self.assertEqual(purchase_invoice.status, 'Partly Paid')
pr = make_payment_request(dt='Purchase Invoice', party_type='Supplier', party='_Test Supplier USD', dn=purchase_invoice.name, recipient_id='user@example.com', mute_email=1, payment_gateway_account='_Test Gateway - USD - _TC', return_doc=1)
pr.save()
pr.submit()
pr.create_payment_entry()
purchase_invoice.load_from_db()
self.assertEqual(purchase_invoice.status, 'Paid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:252*

### test_payment_entry

**Category**: workflow  
**Description**: Workflow: test payment entry  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:297*

### test_multiple_payment_entries_against_sales_order

**Category**: workflow  
**Description**: Workflow: test multiple payment entries against sales order  
**Expected**: self.assertRaises(frappe.ValidationError, pr2.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

so = make_sales_order()
pr1 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
pr1.grand_total = 200
pr1.submit()
pr2 = make_payment_request(dt='Sales Order', dn=so.name, recipient_id='nabin@erpnext.com', return_doc=1)
self.assertEqual(pr2.grand_total, 800)
pr2.grand_total = 900
self.assertRaises(frappe.ValidationError, pr2.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:391*

### test_conversion_on_foreign_currency_accounts

**Category**: workflow  
**Description**: Workflow: test conversion on foreign currency accounts  
**Expected**: self.assertEqual(pe.received_amount, 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

po_doc = create_purchase_order(supplier='_Test Supplier USD', currency='USD', do_not_submit=1)
po_doc.conversion_rate = 80
po_doc.items[0].qty = 1
po_doc.items[0].rate = 10
po_doc.save().submit()
pr = make_payment_request(dt=po_doc.doctype, dn=po_doc.name, recipient_id='nabin@erpnext.com')
pr = frappe.get_doc(pr).save().submit()
pe = pr.create_payment_entry()
self.assertEqual(pe.base_paid_amount, 800)
self.assertEqual(pe.paid_amount, 800)
self.assertEqual(pe.base_received_amount, 800)
self.assertEqual(pe.received_amount, 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:413*

### test_multiple_payment_if_partially_paid_for_multi_currency

**Category**: workflow  
**Description**: Workflow: test multiple payment if partially paid for multi currency  
**Expected**: self.assertRaisesRegex(frappe.exceptions.ValidationError, re.compile('Payment Entry is already created'), make_payment_request, dt='Purchase Invoice', dn=pi.name, mute_email=1, submit_doc=1, return_doc=1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:507*

### test_single_payment_with_payment_term_for_same_currency

**Category**: workflow  
**Description**: Workflow: test single payment with payment term for same currency  
**Expected**: self.assertEqual(pr.grand_total, 20000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:575*

### test_single_payment_with_payment_term_for_multi_currency

**Category**: workflow  
**Description**: Workflow: test single payment with payment term for multi currency  
**Expected**: self.assertEqual(pr.grand_total, 200)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:625*

### test_payment_cancel_process

**Category**: workflow  
**Description**: Workflow: test payment cancel process  
**Expected**: self.assertEqual(so.advance_payment_status, 'Requested')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

so = make_sales_order(currency='INR', qty=1, rate=1000)
self.assertEqual(so.advance_payment_status, 'Not Requested')
pr = make_payment_request(dt='Sales Order', dn=so.name, mute_email=1, submit_doc=1, return_doc=1)
self.assertEqual(pr.status, 'Requested')
self.assertEqual(pr.grand_total, 1000)
self.assertEqual(pr.outstanding_amount, pr.grand_total)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Requested')
pe = pr.create_payment_entry(submit=False)
pe.paid_amount = 800
pe.references[0].allocated_amount = 800
pe.submit()
self.assertEqual(pe.references[0].payment_request, pr.name)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Partially Paid')
pr.load_from_db()
self.assertEqual(pr.status, 'Partially Paid')
self.assertEqual(pr.outstanding_amount, 200)
self.assertEqual(pr.grand_total, 1000)
pe.cancel()
pr.load_from_db()
self.assertEqual(pr.status, 'Requested')
self.assertEqual(pr.outstanding_amount, 1000)
self.assertEqual(pr.grand_total, 1000)
so.load_from_db()
self.assertEqual(so.advance_payment_status, 'Requested')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:668*

### test_partial_paid_invoice_with_payment_request

**Category**: workflow  
**Description**: Workflow: test partial paid invoice with payment request  
**Expected**: self.assertEqual(pr.grand_total, si.outstanding_amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

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

si = create_sales_invoice(currency='INR', qty=1, rate=5000)
si.save()
si.submit()
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank - _TC')
pe.reference_no = 'PAYEE0002'
pe.reference_date = frappe.utils.nowdate()
pe.paid_amount = 2500
pe.references[0].allocated_amount = 2500
pe.save()
pe.submit()
si.load_from_db()
pr = make_payment_request(dt='Sales Invoice', dn=si.name, mute_email=1)
self.assertEqual(pr.grand_total, si.outstanding_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_request/test_payment_request.py:713*

### test_promotional_scheme

**Category**: workflow  
**Description**: Workflow: test promotional scheme  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

ps = make_promotional_scheme(applicable_for='Customer', customer='_Test Customer')
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name', 'creation'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 4)
self.assertTrue(price_doc_details.discount_percentage, 20)
ps.price_discount_slabs[0].min_qty = 6
ps.append('customer', {'customer': '_Test Customer 2'})
ps.save()
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 2)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[1].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer 2')
self.assertTrue(price_doc_details.min_qty, 6)
self.assertTrue(price_doc_details.discount_percentage, 20)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 6)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:16*

### test_change_applicable_for_in_promotional_scheme

**Category**: workflow  
**Description**: Workflow: test change applicable for in promotional scheme  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

ps = make_promotional_scheme()
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
so = make_sales_order(qty=5, currency='USD', do_not_save=True)
so.set_missing_values()
so.save()
self.assertEqual(price_rules[0].name, so.pricing_rules[0].pricing_rule)
ps.applicable_for = 'Customer'
ps.append('customer', {'customer': '_Test Customer'})
self.assertRaises(TransactionExists, ps.save)
frappe.delete_doc('Sales Order', so.name)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:72*

### test_min_max_amount_configuration

**Category**: workflow  
**Description**: Workflow: test min max amount configuration  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

ps = make_promotional_scheme()
ps.price_discount_slabs[0].min_amount = 10
ps.price_discount_slabs[0].max_amount = 1000
ps.save()
price_rules_data = frappe.db.get_value('Pricing Rule', {'promotional_scheme': ps.name}, ['min_amt', 'max_amt'], as_dict=1)
self.assertEqual(price_rules_data.min_amt, 10)
self.assertEqual(price_rules_data.max_amt, 1000)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:117*

### test_promotional_scheme

**Category**: workflow  
**Description**: Workflow: test promotional scheme  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ps = make_promotional_scheme(applicable_for='Customer', customer='_Test Customer')
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name', 'creation'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 4)
self.assertTrue(price_doc_details.discount_percentage, 20)
ps.price_discount_slabs[0].min_qty = 6
ps.append('customer', {'customer': '_Test Customer 2'})
ps.save()
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 2)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[1].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer 2')
self.assertTrue(price_doc_details.min_qty, 6)
self.assertTrue(price_doc_details.discount_percentage, 20)
price_doc_details = frappe.db.get_value('Pricing Rule', price_rules[0].name, ['customer', 'min_qty', 'discount_percentage'], as_dict=1)
self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 6)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', fields=['promotional_scheme_id', 'name'], filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:16*

### test_change_applicable_for_in_promotional_scheme

**Category**: workflow  
**Description**: Workflow: test change applicable for in promotional scheme  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ps = make_promotional_scheme()
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertTrue(len(price_rules), 1)
so = make_sales_order(qty=5, currency='USD', do_not_save=True)
so.set_missing_values()
so.save()
self.assertEqual(price_rules[0].name, so.pricing_rules[0].pricing_rule)
ps.applicable_for = 'Customer'
ps.append('customer', {'customer': '_Test Customer'})
self.assertRaises(TransactionExists, ps.save)
frappe.delete_doc('Sales Order', so.name)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:72*

### test_min_max_amount_configuration

**Category**: workflow  
**Description**: Workflow: test min max amount configuration  
**Expected**: self.assertEqual(price_rules, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
ps = make_promotional_scheme()
ps.price_discount_slabs[0].min_amount = 10
ps.price_discount_slabs[0].max_amount = 1000
ps.save()
price_rules_data = frappe.db.get_value('Pricing Rule', {'promotional_scheme': ps.name}, ['min_amt', 'max_amt'], as_dict=1)
self.assertEqual(price_rules_data.min_amt, 10)
self.assertEqual(price_rules_data.max_amt, 1000)
frappe.delete_doc('Promotional Scheme', ps.name)
price_rules = frappe.get_all('Pricing Rule', filters={'promotional_scheme': ps.name})
self.assertEqual(price_rules, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:117*

### test_deferred_revenue

**Category**: workflow  
**Description**: Workflow: test deferred revenue  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_revenue = 1
item.item_defaults[0].deferred_revenue_account = self.deferred_revenue_account
item.no_of_months = 3
item.save()
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
si.items[0].income_account = self.income_account
si.items[0].enable_deferred_revenue = 1
si.items[0].service_start_date = '2021-05-01'
si.items[0].service_end_date = '2021-08-01'
si.items[0].deferred_revenue_account = self.deferred_revenue_account
si.save()
si.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'jun_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'jul_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:74*

### test_deferred_expense

**Category**: workflow  
**Description**: Workflow: test deferred expense  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_expense = 1
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
item.no_of_months_exp = 3
item.save()
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 5, 1), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300, warehouse=self.warehouse, qty=1)
pi.set_posting_time = True
pi.items[0].enable_deferred_expense = 1
pi.items[0].service_start_date = '2021-05-01'
pi.items[0].service_end_date = '2021-08-01'
pi.items[0].deferred_expense_account = self.deferred_expense_account
pi.items[0].expense_account = self.expense_account
pi.save()
pi.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Expense', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jun_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jul_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:141*

### test_zero_months

**Category**: workflow  
**Description**: Workflow: test zero months  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_revenue = 1
item.deferred_revenue_account = self.deferred_revenue_account
item.no_of_months = 0
item.save()
si = create_sales_invoice(item=item.name, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
si.items[0].enable_deferred_revenue = 1
si.items[0].income_account = self.income_account
si.items[0].deferred_revenue_account = self.deferred_revenue_account
si.save()
si.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': 300.0, 'actual': 300.0}, {'key': 'jun_2021', 'total': 0, 'actual': 0}, {'key': 'jul_2021', 'total': 0, 'actual': 0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:211*

### test_zero_amount

**Category**: workflow  
**Description**: Workflow: test zero amount  
**Expected**: self.assertLess(deferred_exp, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_expense = 1
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
item.no_of_months_exp = 12
item.save()
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 12, 30), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=3910, price_list_rate=3910, warehouse=self.warehouse, qty=1)
pi.set_posting_time = True
pi.items[0].enable_deferred_expense = 1
pi.items[0].service_start_date = '2021-12-30'
pi.items[0].service_end_date = '2022-12-30'
pi.items[0].deferred_expense_account = self.deferred_expense_account
pi.items[0].expense_account = self.expense_account
pi.save()
pi.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2022-01-01', end_date='2022-01-31', type='Expense', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2022-01-31')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2022-01-01', 'period_end_date': '2022-01-31', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
inv = [d for d in report.deferred_invoices if d.name == pi.name]
self.assertTrue(inv)
inv = inv[0].calculate_invoice_revenue_expense_for_period()
deferred_exp = sum([inv[idx].actual for idx in range(len(report.period_list))])
self.assertLess(deferred_exp, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:279*

### test_deferred_revenue

**Category**: workflow  
**Description**: Workflow: test deferred revenue  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_revenue = 1
item.item_defaults[0].deferred_revenue_account = self.deferred_revenue_account
item.no_of_months = 3
item.save()
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
si.items[0].income_account = self.income_account
si.items[0].enable_deferred_revenue = 1
si.items[0].service_start_date = '2021-05-01'
si.items[0].service_end_date = '2021-08-01'
si.items[0].deferred_revenue_account = self.deferred_revenue_account
si.save()
si.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'jun_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'jul_2021', 'total': 100.0, 'actual': 100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:74*

### test_deferred_expense

**Category**: workflow  
**Description**: Workflow: test deferred expense  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_expense = 1
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
item.no_of_months_exp = 3
item.save()
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 5, 1), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300, warehouse=self.warehouse, qty=1)
pi.set_posting_time = True
pi.items[0].enable_deferred_expense = 1
pi.items[0].service_start_date = '2021-05-01'
pi.items[0].service_end_date = '2021-08-01'
pi.items[0].deferred_expense_account = self.deferred_expense_account
pi.items[0].expense_account = self.expense_account
pi.save()
pi.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Expense', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jun_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'jul_2021', 'total': -100.0, 'actual': -100.0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:141*

### test_zero_months

**Category**: workflow  
**Description**: Workflow: test zero months  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_item('_Test Internet Subscription', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_revenue = 1
item.deferred_revenue_account = self.deferred_revenue_account
item.no_of_months = 0
item.save()
si = create_sales_invoice(item=item.name, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
si.items[0].enable_deferred_revenue = 1
si.items[0].income_account = self.income_account
si.items[0].deferred_revenue_account = self.deferred_revenue_account
si.save()
si.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2021-05-01', end_date='2021-08-01', type='Income', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2021-05-01')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2021-05-01', 'period_end_date': '2021-08-01', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Revenue', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
expected = [{'key': 'may_2021', 'total': 300.0, 'actual': 300.0}, {'key': 'jun_2021', 'total': 0, 'actual': 0}, {'key': 'jul_2021', 'total': 0, 'actual': 0}, {'key': 'aug_2021', 'total': 0, 'actual': 0}]
self.assertEqual(report.period_total, expected)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:211*

### test_zero_amount

**Category**: workflow  
**Description**: Workflow: test zero amount  
**Expected**: self.assertLess(deferred_exp, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_item('_Test Office Desk', 0, self.warehouse, self.company)
item = frappe.get_doc('Item', self.item)
item.enable_deferred_expense = 1
item.item_defaults[0].deferred_expense_account = self.deferred_expense_account
item.no_of_months_exp = 12
item.save()
pi = make_purchase_invoice(item=self.item, company=self.company, supplier=self.supplier, is_return=False, update_stock=False, posting_date=frappe.utils.datetime.date(2021, 12, 30), parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=3910, price_list_rate=3910, warehouse=self.warehouse, qty=1)
pi.set_posting_time = True
pi.items[0].enable_deferred_expense = 1
pi.items[0].service_start_date = '2021-12-30'
pi.items[0].service_end_date = '2022-12-30'
pi.items[0].deferred_expense_account = self.deferred_expense_account
pi.items[0].expense_account = self.expense_account
pi.save()
pi.submit()
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date=nowdate(), start_date='2022-01-01', end_date='2022-01-31', type='Expense', company=self.company)
pda.insert()
pda.submit()
fiscal_year = frappe.get_doc('Fiscal Year', get_fiscal_year(date='2022-01-31')[0])
self.filters = frappe._dict({'company': self.company, 'filter_based_on': 'Date Range', 'period_start_date': '2022-01-01', 'period_end_date': '2022-01-31', 'from_fiscal_year': fiscal_year.year, 'to_fiscal_year': fiscal_year.year, 'periodicity': 'Monthly', 'type': 'Expense', 'with_upcoming_postings': False})
report = Deferred_Revenue_and_Expense_Report(filters=self.filters)
report.run()
inv = [d for d in report.deferred_invoices if d.name == pi.name]
self.assertTrue(inv)
inv = inv[0].calculate_invoice_revenue_expense_for_period()
deferred_exp = sum([inv[idx].actual for idx in range(len(report.period_list))])
self.assertLess(deferred_exp, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:279*

### test_unpaid_invoice_outstanding

**Category**: workflow  
**Description**: Workflow: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.cleanup()

sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
get_payment_entry(sinv.doctype, sinv.name).save().submit()
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
outstanding = [x for x in data if x.get('against_voucher_no') == 'Outstanding:']
self.assertEqual(outstanding[0].get('amount'), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:49*

### test_unpaid_invoice_outstanding

**Category**: workflow  
**Description**: Workflow: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
get_payment_entry(sinv.doctype, sinv.name).save().submit()
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
outstanding = [x for x in data if x.get('against_voucher_no') == 'Outstanding:']
self.assertEqual(outstanding[0].get('amount'), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:49*

### test_process_soa_for_gl

**Category**: workflow  
**Description**: Workflow: Tests the utils for Statement of Accounts(General Ledger)  
**Expected**: self.assertEqual(receivable_entries[1].balance, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

'Tests the utils for Statement of Accounts(General Ledger)'
process_soa = create_process_soa(name='_Test Process SOA for GL', customers=[{'customer': '_Test Customer'}, {'customer': 'Other Customer'}])
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 4)
self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
self.assertEqual(receivable_entries[1].balance, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:31*

### test_process_soa_for_ar

**Category**: workflow  
**Description**: Workflow: Tests the utils for Statement of Accounts(Accounts Receivable)  
**Expected**: self.check_ageing_summary(ageing_summary, expected_summary)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

'Tests the utils for Statement of Accounts(Accounts Receivable)'
process_soa = create_process_soa(name='_Test Process SOA for AR', report='Accounts Receivable')
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertNotIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 1)
self.assertEqual(receivable_entries[0].voucher_no, self.si.name)
self.assertEqual(receivable_entries[0].total_due, 100)
ageing_summary = statement_dict['_Test Customer'][1][0]
expected_summary = frappe._dict(range1=100, range2=0, range3=0, range4=0, range5=0)
self.check_ageing_summary(ageing_summary, expected_summary)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:52*

### test_auto_email_for_process_soa_ar

**Category**: workflow  
**Description**: Workflow: test auto email for process soa ar  
**Expected**: self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

process_soa = create_process_soa(name='_Test Process SOA', enable_auto_email=1, report='Accounts Receivable')
send_emails(process_soa.name, from_scheduler=True)
process_soa.load_from_db()
self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:80*

### test_process_soa_for_gl

**Category**: workflow  
**Description**: Workflow: Tests the utils for Statement of Accounts(General Ledger)  
**Expected**: self.assertEqual(receivable_entries[1].balance, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Tests the utils for Statement of Accounts(General Ledger)'
process_soa = create_process_soa(name='_Test Process SOA for GL', customers=[{'customer': '_Test Customer'}, {'customer': 'Other Customer'}])
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 4)
self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
self.assertEqual(receivable_entries[1].balance, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:31*

### test_process_soa_for_ar

**Category**: workflow  
**Description**: Workflow: Tests the utils for Statement of Accounts(Accounts Receivable)  
**Expected**: self.check_ageing_summary(ageing_summary, expected_summary)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Tests the utils for Statement of Accounts(Accounts Receivable)'
process_soa = create_process_soa(name='_Test Process SOA for AR', report='Accounts Receivable')
statement_dict = get_statement_dict(process_soa, get_statement_dict=True)
self.assertNotIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
receivable_entries = statement_dict['_Test Customer'][0]
self.assertEqual(len(receivable_entries), 1)
self.assertEqual(receivable_entries[0].voucher_no, self.si.name)
self.assertEqual(receivable_entries[0].total_due, 100)
ageing_summary = statement_dict['_Test Customer'][1][0]
expected_summary = frappe._dict(range1=100, range2=0, range3=0, range4=0, range5=0)
self.check_ageing_summary(ageing_summary, expected_summary)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:52*

### test_auto_email_for_process_soa_ar

**Category**: workflow  
**Description**: Workflow: test auto email for process soa ar  
**Expected**: self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
process_soa = create_process_soa(name='_Test Process SOA', enable_auto_email=1, report='Accounts Receivable')
send_emails(process_soa.name, from_scheduler=True)
process_soa.load_from_db()
self.assertEqual(process_soa.posting_date, getdate(add_days(today(), 7)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:80*

### test_ledger_summary_basic_output

**Category**: workflow  
**Description**: Workflow: test ledger summary basic output  
**Expected**: self.assertEqual(len(report), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
si = self.create_sales_invoice(do_not_submit=True)
si.save().submit()
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:65*

### test_summary_with_return_and_payment

**Category**: workflow  
**Description**: Workflow: test summary with return and payment  
**Expected**: self.assertEqual(len(report), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
si = self.create_sales_invoice(do_not_submit=True)
si.save().submit()
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected.get(field))
cr_note = self.create_credit_note(si.name, True)
cr_note.items[0].qty = -2
cr_note.save().submit()
expected_after_cr_note = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 200.0, 'closing_balance': 800.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_note:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_note.get(field))
pe = self.create_payment_entry(si.name, True)
pe.paid_amount = 500
pe.save().submit()
expected_after_cr_and_payment = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 500.0, 'return_amount': 200.0, 'closing_balance': 300.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_and_payment:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_and_payment.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:89*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: workflow  
**Description**: Workflow: test customer ledger ignore cr dr filter  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

si = create_sales_invoice()
cr_note = make_return_doc(si.doctype, si.name)
cr_note.submit()
pr = frappe.get_doc('Payment Reconciliation')
pr.company = si.company
pr.party_type = 'Customer'
pr.party = si.customer
pr.receivable_payable_account = si.debit_to
pr.get_unreconciled_entries()
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
self.assertEqual(len(system_generated_journal), 1)
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': False}))
self.assertEqual(len(data), 1)
self.assertDictEqual(expected, data[0])
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': True}))
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:154*

### test_ledger_summary_basic_output

**Category**: workflow  
**Description**: Workflow: test ledger summary basic output  
**Expected**: self.assertEqual(len(report), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
si = self.create_sales_invoice(do_not_submit=True)
si.save().submit()
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:65*

### test_summary_with_return_and_payment

**Category**: workflow  
**Description**: Workflow: test summary with return and payment  
**Expected**: self.assertEqual(len(report), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
si = self.create_sales_invoice(do_not_submit=True)
si.save().submit()
expected = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 1000.0, 'currency': 'INR', 'customer_name': '_Test Customer'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected.get(field))
cr_note = self.create_credit_note(si.name, True)
cr_note.items[0].qty = -2
cr_note.save().submit()
expected_after_cr_note = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 0, 'return_amount': 200.0, 'closing_balance': 800.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_note:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_note.get(field))
pe = self.create_payment_entry(si.name, True)
pe.paid_amount = 500
pe.save().submit()
expected_after_cr_and_payment = {'party': '_Test Customer', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 1000.0, 'paid_amount': 500.0, 'return_amount': 200.0, 'closing_balance': 300.0, 'currency': 'INR'}
report = execute(filters)[1]
self.assertEqual(len(report), 1)
for field in expected_after_cr_and_payment:
    with self.subTest(field=field):
        self.assertEqual(report[0].get(field), expected_after_cr_and_payment.get(field))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:89*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: workflow  
**Description**: Workflow: test customer ledger ignore cr dr filter  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice()
cr_note = make_return_doc(si.doctype, si.name)
cr_note.submit()
pr = frappe.get_doc('Payment Reconciliation')
pr.company = si.company
pr.party_type = 'Customer'
pr.party = si.customer
pr.receivable_payable_account = si.debit_to
pr.get_unreconciled_entries()
invoices = [invoice.as_dict() for invoice in pr.invoices if invoice.invoice_number == si.name]
payments = [payment.as_dict() for payment in pr.payments if payment.reference_name == cr_note.name]
pr.allocate_entries(frappe._dict({'invoices': invoices, 'payments': payments}))
pr.reconcile()
system_generated_journal = frappe.db.get_all('Journal Entry', filters={'docstatus': 1, 'reference_type': si.doctype, 'reference_name': si.name, 'voucher_type': 'Credit Note', 'is_system_generated': True}, fields=['name'])
self.assertEqual(len(system_generated_journal), 1)
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': False}))
self.assertEqual(len(data), 1)
self.assertDictEqual(expected, data[0])
expected = {'party': '_Test Customer', 'customer_name': '_Test Customer', 'customer_group': '_Test Customer Group', 'territory': '_Test Territory', 'party_name': '_Test Customer', 'opening_balance': 0, 'invoiced_amount': 100.0, 'paid_amount': 0.0, 'return_amount': 100.0, 'closing_balance': 0.0, 'currency': 'INR', 'dr_or_cr': ''}
columns, data = execute(frappe._dict({'company': si.company, 'from_date': si.posting_date, 'to_date': si.posting_date, 'ignore_cr_dr_notes': True}))
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:154*

### test_01_basic_functions

**Category**: workflow  
**Description**: Workflow: test 01 basic functions  
**Expected**: self.assertEqual(res[0], (si.name, 100, 100))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
preq = frappe.get_doc(make_payment_request(dt=si.doctype, dn=si.name, payment_request_type='Inward', party_type='Customer', party=si.customer))
preq.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': preq.doctype, 'voucher_no': preq.name})
self.assertRaises(frappe.ValidationError, ral.save)
ral.vouchers.pop()
preq.cancel()
preq.delete()
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save()
gle = frappe.db.get_all('GL Entry', filters={'voucher_no': si.name, 'account': self.debit_to})
frappe.db.set_value('GL Entry', gle[0], 'debit', 90)
gl = qb.DocType('GL Entry')
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertNotEqual(res[0], (si.name, 100, 100))
ral.save().submit()
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertEqual(res[0], (si.name, 100, 100))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:34*

### test_02_deferred_accounting_valiations

**Category**: workflow  
**Description**: Workflow: test 02 deferred accounting valiations  
**Expected**: self.assertRaises(frappe.ValidationError, ral.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, do_not_submit=True)
si.items[0].enable_deferred_revenue = True
si.items[0].deferred_revenue_account = self.deferred_revenue
si.items[0].service_start_date = nowdate()
si.items[0].service_end_date = add_days(nowdate(), 90)
si.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:102*

### test_04_pcv_validation

**Category**: workflow  
**Description**: Workflow: test 04 pcv validation  
**Expected**: self.assertRaises(frappe.ValidationError, ral.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

gl = frappe.qb.DocType('GL Entry')
qb.from_(gl).delete().where(gl.company == self.company).run()
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
fy = get_fiscal_year(today(), company=self.company)
pcv = frappe.get_doc({'doctype': 'Period Closing Voucher', 'transaction_date': today(), 'period_start_date': fy[1], 'period_end_date': today(), 'company': self.company, 'fiscal_year': fy[0], 'cost_center': self.cost_center, 'closing_account_head': self.retained_earnings, 'remarks': 'test'})
pcv.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
pcv.reload()
pcv.cancel()
pcv.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:125*

### test_03_deletion_flag_and_preview_function

**Category**: workflow  
**Description**: Workflow: test 03 deletion flag and preview function  
**Expected**: self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save().submit()
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': si.name, 'is_cancelled': 1}))
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:164*

### test_05_without_deletion_flag

**Category**: workflow  
**Description**: Workflow: test 05 without deletion flag  
**Expected**: self.assertIsNotNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = False
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save().submit()
self.assertIsNotNone(frappe.db.exists('GL Entry', {'voucher_no': si.name, 'is_cancelled': 1}))
self.assertIsNotNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:189*

### test_06_repost_purchase_receipt

**Category**: workflow  
**Description**: Workflow: test 06 repost purchase receipt  
**Expected**: self.assertEqual(expected_pr_gles_after_repost, pr_gles_after_repost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
update_repost_settings()

from erpnext.accounts.doctype.account.test_account import create_account
provisional_account = create_account(account_name='Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
another_provisional_account = create_account(account_name='Another Provision Account', parent_account='Current Liabilities - _TC', company=self.company)
company = frappe.get_doc('Company', self.company)
company.enable_provisional_accounting_for_non_stock_items = 1
company.default_provisional_account = provisional_account
company.save()
test_cc = company.cost_center
default_expense_account = company.service_expense_account
item = make_item(properties={'is_stock_item': 0})
pr = make_purchase_receipt(company=self.company, item_code=item.name, rate=1000.0, qty=1.0)
pr_gl_entries = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
expected_pr_gles = [{'account': provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}, {'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}]
self.assertEqual(expected_pr_gles, pr_gl_entries)
frappe.db.set_value('Purchase Receipt Item', pr.items[0].name, 'provisional_expense_account', another_provisional_account)
repost_doc = frappe.new_doc('Repost Accounting Ledger')
repost_doc.company = self.company
repost_doc.delete_cancelled_entries = True
repost_doc.append('vouchers', {'voucher_type': pr.doctype, 'voucher_no': pr.name})
repost_doc.save().submit()
pr_gles_after_repost = get_gl_entries(pr.doctype, pr.name, skip_cancelled=True)
expected_pr_gles_after_repost = [{'account': default_expense_account, 'debit': 1000.0, 'credit': 0.0, 'cost_center': test_cc}, {'account': another_provisional_account, 'debit': 0.0, 'credit': 1000.0, 'cost_center': test_cc}]
self.assertEqual(len(pr_gles_after_repost), len(expected_pr_gles_after_repost))
self.assertEqual(expected_pr_gles_after_repost, pr_gles_after_repost)
repost_doc.cancel()
repost_doc.delete()
pr.reload()
pr.cancel()
company.enable_provisional_accounting_for_non_stock_items = 0
company.default_provisional_account = None
company.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:214*

### test_01_basic_functions

**Category**: workflow  
**Description**: Workflow: test 01 basic functions  
**Expected**: self.assertEqual(res[0], (si.name, 100, 100))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
preq = frappe.get_doc(make_payment_request(dt=si.doctype, dn=si.name, payment_request_type='Inward', party_type='Customer', party=si.customer))
preq.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': preq.doctype, 'voucher_no': preq.name})
self.assertRaises(frappe.ValidationError, ral.save)
ral.vouchers.pop()
preq.cancel()
preq.delete()
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save()
gle = frappe.db.get_all('GL Entry', filters={'voucher_no': si.name, 'account': self.debit_to})
frappe.db.set_value('GL Entry', gle[0], 'debit', 90)
gl = qb.DocType('GL Entry')
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertNotEqual(res[0], (si.name, 100, 100))
ral.save().submit()
res = qb.from_(gl).select(gl.voucher_no, Sum(gl.debit).as_('debit'), Sum(gl.credit).as_('credit')).where((gl.voucher_no == si.name) & (gl.is_cancelled == 0)).run()
self.assertEqual(res[0], (si.name, 100, 100))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:34*

### test_02_deferred_accounting_valiations

**Category**: workflow  
**Description**: Workflow: test 02 deferred accounting valiations  
**Expected**: self.assertRaises(frappe.ValidationError, ral.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, do_not_submit=True)
si.items[0].enable_deferred_revenue = True
si.items[0].deferred_revenue_account = self.deferred_revenue
si.items[0].service_start_date = nowdate()
si.items[0].service_end_date = add_days(nowdate(), 90)
si.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:102*

### test_04_pcv_validation

**Category**: workflow  
**Description**: Workflow: test 04 pcv validation  
**Expected**: self.assertRaises(frappe.ValidationError, ral.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
gl = frappe.qb.DocType('GL Entry')
qb.from_(gl).delete().where(gl.company == self.company).run()
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
fy = get_fiscal_year(today(), company=self.company)
pcv = frappe.get_doc({'doctype': 'Period Closing Voucher', 'transaction_date': today(), 'period_start_date': fy[1], 'period_end_date': today(), 'company': self.company, 'fiscal_year': fy[0], 'cost_center': self.cost_center, 'closing_account_head': self.retained_earnings, 'remarks': 'test'})
pcv.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
self.assertRaises(frappe.ValidationError, ral.save)
pcv.reload()
pcv.cancel()
pcv.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:125*

### test_03_deletion_flag_and_preview_function

**Category**: workflow  
**Description**: Workflow: test 03 deletion flag and preview function  
**Expected**: self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100)
pe = get_payment_entry(si.doctype, si.name)
pe.save().submit()
ral = frappe.new_doc('Repost Accounting Ledger')
ral.company = self.company
ral.delete_cancelled_entries = True
ral.append('vouchers', {'voucher_type': si.doctype, 'voucher_no': si.name})
ral.append('vouchers', {'voucher_type': pe.doctype, 'voucher_no': pe.name})
ral.save().submit()
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': si.name, 'is_cancelled': 1}))
self.assertIsNone(frappe.db.exists('GL Entry', {'voucher_no': pe.name, 'is_cancelled': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/repost_accounting_ledger/test_repost_accounting_ledger.py:164*

### test_multiple_pos_opening_entry_for_multiple_pos_profiles

**Category**: workflow  
**Description**: Workflow: test multiple pos opening entry for multiple pos profiles  
**Expected**: self.assertEqual(opening_entry_2.user, cashier_user.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

test_user, pos_profile = self.init_user_and_profile()
opening_entry_1 = create_opening_entry(pos_profile, test_user.name)
self.assertEqual(opening_entry_1.status, 'Open')
self.assertEqual(opening_entry_1.user, test_user.name)
cashier_user = create_user('test_cashier@example.com', 'Accounts Manager', 'Sales Manager')
frappe.set_user(cashier_user.name)
pos_profile2 = make_pos_profile(name='_Test POS Profile 2')
opening_entry_2 = create_opening_entry(pos_profile2, cashier_user.name)
self.assertEqual(opening_entry_2.status, 'Open')
self.assertEqual(opening_entry_2.user, cashier_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:56*

### test_multiple_pos_opening_entry_for_multiple_pos_profiles

**Category**: workflow  
**Description**: Workflow: test multiple pos opening entry for multiple pos profiles  
**Expected**: self.assertEqual(opening_entry_2.user, cashier_user.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_user, pos_profile = self.init_user_and_profile()
opening_entry_1 = create_opening_entry(pos_profile, test_user.name)
self.assertEqual(opening_entry_1.status, 'Open')
self.assertEqual(opening_entry_1.user, test_user.name)
cashier_user = create_user('test_cashier@example.com', 'Accounts Manager', 'Sales Manager')
frappe.set_user(cashier_user.name)
pos_profile2 = make_pos_profile(name='_Test POS Profile 2')
opening_entry_2 = create_opening_entry(pos_profile2, cashier_user.name)
self.assertEqual(opening_entry_2.status, 'Open')
self.assertEqual(opening_entry_2.user, cashier_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:56*

### test_pricing_rule_for_margin

**Category**: workflow  
**Description**: Workflow: test pricing rule for margin  
**Expected**: self.assertEqual(details.get('margin_rate_or_amount'), 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

from erpnext.stock.get_item_details import get_item_details
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test FG Item 2'}], 'selling': 1, 'currency': 'USD', 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 10, 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
item_price = frappe.get_doc({'doctype': 'Item Price', 'price_list': '_Test Price List 2', 'item_code': '_Test FG Item 2', 'price_list_rate': 100})
item_price.insert(ignore_permissions=True)
args = frappe._dict({'item_code': '_Test FG Item 2', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
details = get_item_details(args)
self.assertEqual(details.get('margin_type'), 'Percentage')
self.assertEqual(details.get('margin_rate_or_amount'), 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:107*

### test_unset_group_condition

**Category**: workflow  
**Description**: Workflow: If args are not set for group condition, then pricing rule should not be applied.  
**Expected**: self.assertEqual(details.get('discount_percentage'), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

'\n\t\tIf args are not set for group condition, then pricing rule should not be applied.\n\t\t'
from erpnext.stock.get_item_details import get_item_details
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Item'}], 'currency': 'USD', 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'discount_percentage': 10, 'applicable_for': 'Territory', 'territory': 'All Territories', 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
args = frappe._dict({'item_code': '_Test Item', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'name': None})
customer = frappe.get_doc('Customer', '_Test Customer')
territory = customer.territory
customer.territory = None
customer.save()
details = get_item_details(args)
self.assertEqual(details.get('discount_percentage'), 0)
customer.territory = territory
customer.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:207*

### test_pricing_rule_for_stock_qty

**Category**: workflow  
**Description**: Workflow: test pricing rule for stock qty  
**Expected**: self.assertEqual(so.items[0].rate, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 5, 'max_qty': 7, 'discount_percentage': 17.5, 'company': '_Test Company'}
frappe.get_doc(test_record.copy()).insert()
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Test Item', 'uom': 'box'}):
    item = frappe.get_doc('Item', '_Test Item')
    item.append('uoms', {'uom': 'Box', 'conversion_factor': 5})
    item.save(ignore_permissions=True)
so = make_sales_order(item_code='_Test Item', qty=1, uom='Box', do_not_submit=True)
so.items[0].price_list_rate = 100
so.submit()
so = frappe.get_doc('Sales Order', so.name)
self.assertEqual(so.items[0].discount_percentage, 17.5)
self.assertEqual(so.items[0].rate, 82.5)
so = make_sales_order(item_code='_Test Item', qty=2, uom='Box', do_not_submit=True)
so.items[0].price_list_rate = 100
so.submit()
so = frappe.get_doc('Sales Order', so.name)
self.assertEqual(so.items[0].discount_percentage, 0)
self.assertEqual(so.items[0].rate, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:338*

### test_pricing_rule_with_margin_and_discount

**Category**: workflow  
**Description**: Workflow: test pricing rule with margin and discount  
**Expected**: self.assertEqual(item.rate, 990)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
make_pricing_rule(selling=1, margin_type='Percentage', margin_rate_or_amount=10, discount_percentage=10)
si = create_sales_invoice(do_not_save=True)
si.items[0].price_list_rate = 1000
si.payment_schedule = []
si.insert(ignore_permissions=True)
item = si.items[0]
self.assertEqual(item.margin_rate_or_amount, 10)
self.assertEqual(item.rate_with_margin, 1100)
self.assertEqual(item.discount_percentage, 10)
self.assertEqual(item.discount_amount, 110)
self.assertEqual(item.rate, 990)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:380*

### test_pricing_rule_with_margin_and_discount_amount

**Category**: workflow  
**Description**: Workflow: test pricing rule with margin and discount amount  
**Expected**: self.assertEqual(item.rate, 990)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
make_pricing_rule(selling=1, margin_type='Percentage', margin_rate_or_amount=10, rate_or_discount='Discount Amount', discount_amount=110)
si = create_sales_invoice(do_not_save=True)
si.items[0].price_list_rate = 1000
si.payment_schedule = []
si.insert(ignore_permissions=True)
item = si.items[0]
self.assertEqual(item.margin_rate_or_amount, 10)
self.assertEqual(item.rate_with_margin, 1100)
self.assertEqual(item.discount_amount, 110)
self.assertEqual(item.rate, 990)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:397*

### test_dont_enforce_free_item_qty

**Category**: workflow  
**Description**: Workflow: test dont enforce free item qty  
**Expected**: self.assertEqual(len(so.items), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
test_record = {'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule', 'apply_on': 'Item Code', 'currency': 'USD', 'items': [{'item_code': '_Test Item'}], 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'rate': 0, 'min_qty': 0, 'max_qty': 7, 'discount_percentage': 17.5, 'price_or_product_discount': 'Product', 'same_item': 0, 'free_item': '_Test Item 2', 'free_qty': 1, 'company': '_Test Company'}
pricing_rule = frappe.get_doc(test_record.copy()).insert()
so = make_sales_order(item_code='_Test Item', qty=1, do_not_submit=True)
self.assertEqual(so.items[1].is_free_item, 1)
self.assertEqual(so.items[1].item_code, '_Test Item 2')
so.items.pop(1)
so.save()
so.reload()
self.assertEqual(len(so.items), 2)
pricing_rule.dont_enforce_free_item_qty = 1
pricing_rule.save()
so.items.pop(1)
so.save()
so.reload()
self.assertEqual(len(so.items), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:480*

### test_pricing_rule_for_condition

**Category**: workflow  
**Description**: Workflow: test pricing rule for condition  
**Expected**: self.assertEqual(item.rate, 900)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

frappe.delete_doc_if_exists('Pricing Rule', '_Test Pricing Rule')
make_pricing_rule(selling=1, margin_type='Percentage', condition="customer=='_Test Customer 1' and is_return==0", discount_percentage=10)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 2', is_return=0)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 100)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=1, qty=-1)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 100)
si = create_sales_invoice(do_not_submit=True, customer='_Test Customer 1', is_return=0)
si.items[0].price_list_rate = 1000
si.submit()
item = si.items[0]
self.assertEqual(item.rate, 900)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:576*

### test_item_price_with_pricing_rule

**Category**: workflow  
**Description**: Workflow: test item price with pricing rule  
**Expected**: self.assertEqual(si.items[0].rate, 102)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

item = make_item('Water Flask')
make_item_price('Water Flask', '_Test Price List', 100)
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Water Flask Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Water Flask'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 0, 'margin_type': 'Percentage', 'margin_rate_or_amount': 2, 'company': '_Test Company'}
rule = frappe.get_doc(pricing_rule_record)
rule.insert()
si = create_sales_invoice(do_not_save=True, item_code='Water Flask')
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 100)
self.assertEqual(si.items[0].margin_rate_or_amount, 2)
self.assertEqual(si.items[0].rate_with_margin, 102)
self.assertEqual(si.items[0].rate, 102)
si.delete()
rule.delete()
frappe.get_doc('Item Price', {'item_code': 'Water Flask'}).delete()
item.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:655*

### test_item_price_with_blank_uom_pricing_rule

**Category**: workflow  
**Description**: Workflow: test item price with blank uom pricing rule  
**Expected**: self.assertEqual(si.items[0].rate, 101)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

properties = {'item_code': 'Item Blank UOM', 'stock_uom': 'Nos', 'sales_uom': 'Box', 'uoms': [dict(uom='Box', conversion_factor=10)]}
item = make_item(properties=properties)
make_item_price('Item Blank UOM', '_Test Price List', 100)
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Item Blank UOM Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Item Blank UOM'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 101, 'company': '_Test Company'}
rule = frappe.get_doc(pricing_rule_record)
rule.insert()
si = create_sales_invoice(do_not_save=True, item_code='Item Blank UOM', uom='Box', conversion_factor=10)
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 1010)
self.assertEqual(si.items[0].rate, 1010)
si.delete()
si = create_sales_invoice(do_not_save=True, item_code='Item Blank UOM', uom='Nos')
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 101)
self.assertEqual(si.items[0].rate, 101)
si.delete()
rule.delete()
frappe.get_doc('Item Price', {'item_code': 'Item Blank UOM'}).delete()
item.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:694*

### test_item_price_with_selling_uom_pricing_rule

**Category**: workflow  
**Description**: Workflow: test item price with selling uom pricing rule  
**Expected**: self.assertEqual(si.items[0].rate, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
delete_existing_pricing_rules()
setup_pricing_rule_data()
self.enterClassContext(self.change_settings('Selling Settings', validate_selling_price=0))

properties = {'item_code': 'Item UOM other than Stock', 'stock_uom': 'Nos', 'sales_uom': 'Box', 'uoms': [dict(uom='Box', conversion_factor=10)]}
item = make_item(properties=properties)
make_item_price('Item UOM other than Stock', '_Test Price List', 100)
pricing_rule_record = {'doctype': 'Pricing Rule', 'title': '_Test Item UOM other than Stock Rule', 'apply_on': 'Item Code', 'items': [{'item_code': 'Item UOM other than Stock', 'uom': 'Box'}], 'selling': 1, 'currency': 'INR', 'rate_or_discount': 'Rate', 'rate': 101, 'company': '_Test Company'}
rule = frappe.get_doc(pricing_rule_record)
rule.insert()
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Box', conversion_factor=10)
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 101)
self.assertEqual(si.items[0].rate, 101)
si.delete()
si = create_sales_invoice(do_not_save=True, item_code='Item UOM other than Stock', uom='Nos')
si.selling_price_list = '_Test Price List'
si.save()
self.assertEqual(si.items[0].price_list_rate, 100)
self.assertEqual(si.items[0].rate, 100)
si.delete()
rule.delete()
frappe.get_doc('Item Price', {'item_code': 'Item UOM other than Stock'}).delete()
item.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pricing_rule/test_pricing_rule.py:751*

### test_resolve_basic_processing_order

**Category**: workflow  
**Description**: Workflow: test resolve basic processing order  
**Expected**: self.assertTrue(all((ai < fi for ai in account_indices for fi in formula_indices)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
resolver = DependencyResolver(self.test_template)
order = resolver.get_processing_order()
account_indices = [i for i, row in enumerate(order) if row.data_source == 'Account Data']
formula_indices = [i for i, row in enumerate(order) if row.data_source == 'Calculated Amount']
self.assertTrue(all((ai < fi for ai in account_indices for fi in formula_indices)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:28*

### test_resolve_simple_dependency

**Category**: workflow  
**Description**: Workflow: test resolve simple dependency  
**Expected**: self.assertLess(a001_index, b001_index, 'A001 should be processed before B001')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Calculated Row', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 2'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
self.assertIn('B001', resolver.dependencies)
self.assertEqual(resolver.dependencies['B001'], ['A001'])
order = resolver.get_processing_order()
a001_index = next((i for i, row in enumerate(order) if row.reference_code == 'A001'))
b001_index = next((i for i, row in enumerate(order) if row.reference_code == 'B001'))
self.assertLess(a001_index, b001_index, 'A001 should be processed before B001')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:38*

### test_resolve_multiple_dependencies

**Category**: workflow  
**Description**: Workflow: test resolve multiple dependencies  
**Expected**: self.assertLess(positions['GROSS001'], positions['MARGIN001'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'INC001', 'display_name': 'Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXP001', 'display_name': 'Expenses', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'GROSS001', 'display_name': 'Gross Profit', 'data_source': 'Calculated Amount', 'calculation_formula': 'INC001 - EXP001'}, {'reference_code': 'MARGIN001', 'display_name': 'Profit Margin', 'data_source': 'Calculated Amount', 'calculation_formula': 'GROSS001 / INC001 * 100'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
self.assertEqual(set(resolver.dependencies['GROSS001']), {'INC001', 'EXP001'})
self.assertEqual(set(resolver.dependencies['MARGIN001']), {'GROSS001', 'INC001'})
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
self.assertLess(positions['INC001'], positions['GROSS001'])
self.assertLess(positions['EXP001'], positions['GROSS001'])
self.assertLess(positions['GROSS001'], positions['MARGIN001'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:71*

### test_resolve_chain_dependencies

**Category**: workflow  
**Description**: Workflow: Test dependency resolution with chain of dependencies (A -> B -> C -> D)  
**Expected**: self.assertLess(positions['C001'], positions['D001'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test dependency resolution with chain of dependencies (A -> B -> C -> D)'
test_rows = [{'reference_code': 'A001', 'display_name': 'Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Level 1', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 + 100'}, {'reference_code': 'C001', 'display_name': 'Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 * 1.2'}, {'reference_code': 'D001', 'display_name': 'Level 3', 'data_source': 'Calculated Amount', 'calculation_formula': 'C001 - 50'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order) if row.reference_code}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['B001'], positions['C001'])
self.assertLess(positions['C001'], positions['D001'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:119*

### test_resolve_diamond_dependency_pattern

**Category**: workflow  
**Description**: Workflow: Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D  
**Expected**: self.assertEqual(set(resolver.dependencies['D001']), {'B001', 'C001'})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test Diamond Dependency Pattern - A → B, A → C, and both B,C → D'
test_rows = [{'reference_code': 'A001', 'display_name': 'Base Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'B001', 'display_name': 'Branch B', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.6'}, {'reference_code': 'C001', 'display_name': 'Branch C', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 0.4'}, {'reference_code': 'D001', 'display_name': 'Final Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + C001'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['A001'], positions['C001'])
self.assertLess(positions['A001'], positions['D001'])
self.assertLess(positions['B001'], positions['D001'])
self.assertLess(positions['C001'], positions['D001'])
self.assertEqual(set(resolver.dependencies['D001']), {'B001', 'C001'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:159*

### test_resolve_independent_formula_row_groups

**Category**: workflow  
**Description**: Workflow: test resolve independent formula row groups  
**Expected**: self.assertLess(positions['Y001'], positions['Z001'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'A001', 'display_name': 'Chain 1 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Asset"]'}, {'reference_code': 'B001', 'display_name': 'Chain 1 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'A001 * 1.1'}, {'reference_code': 'C001', 'display_name': 'Chain 1 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'B001 + 100'}, {'reference_code': 'X001', 'display_name': 'Chain 2 Base', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Liability"]'}, {'reference_code': 'Y001', 'display_name': 'Chain 2 Level 2', 'data_source': 'Calculated Amount', 'calculation_formula': 'X001 * 0.9'}, {'reference_code': 'Z001', 'display_name': 'Chain 2 Final', 'data_source': 'Calculated Amount', 'calculation_formula': 'Y001 - 50'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['A001'], positions['B001'])
self.assertLess(positions['B001'], positions['C001'])
self.assertLess(positions['X001'], positions['Y001'])
self.assertLess(positions['Y001'], positions['Z001'])
chain1_codes = {'A001', 'B001', 'C001'}
chain2_codes = {'X001', 'Y001', 'Z001'}
for code in chain1_codes:
    if code in resolver.dependencies:
        deps = set(resolver.dependencies[code])
        self.assertFalse(deps.intersection(chain2_codes), f'{code} should not depend on chain 2')
for code in chain2_codes:
    if code in resolver.dependencies:
        deps = set(resolver.dependencies[code])
        self.assertFalse(deps.intersection(chain1_codes), f'{code} should not depend on chain 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:206*

### test_resolve_mixed_data_sources

**Category**: workflow  
**Description**: Workflow: test resolve mixed data sources  
**Expected**: self.assertEqual(len(order), 4)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'CALC001', 'display_name': 'Calculated', 'data_source': 'Calculated Amount', 'calculation_formula': 'ACC001 + 100'}, {'reference_code': None, 'display_name': 'Spacing', 'data_source': 'Blank Line'}, {'reference_code': 'ACC001', 'display_name': 'Account', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': None, 'display_name': 'Custom', 'data_source': 'Custom API'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {}
for i, row in enumerate(order):
    if row.reference_code:
        positions[row.reference_code] = i
    else:
        positions[f'{row.data_source}_{i}'] = i
self.assertLess(positions['ACC001'], positions['CALC001'])
self.assertEqual(len(order), 4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:278*

### test_resolve_api_to_formula_dependencies

**Category**: workflow  
**Description**: Workflow: test resolve api to formula dependencies  
**Expected**: self.assertLess(positions['API001'], positions['ACC001'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'API001', 'display_name': 'Custom API Result', 'data_source': 'Custom API'}, {'reference_code': 'ACC001', 'display_name': 'Account Data', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'CALC001', 'display_name': 'Calculated Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'API001 + ACC001'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['API001'], positions['CALC001'])
self.assertLess(positions['ACC001'], positions['CALC001'])
self.assertLess(positions['API001'], positions['ACC001'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:323*

### test_resolve_cross_datasource_dependencies

**Category**: workflow  
**Description**: Workflow: test resolve cross datasource dependencies  
**Expected**: self.assertEqual(set(resolver.dependencies['FINAL001']), {'MIXED001', 'API001'})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'API001', 'display_name': 'API Data', 'data_source': 'Custom API'}, {'reference_code': 'ACC001', 'display_name': 'Account Total', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_type", "=", "Income"]'}, {'reference_code': 'MIXED001', 'display_name': 'Mixed Calculation', 'data_source': 'Calculated Amount', 'calculation_formula': '(API001 + ACC001) * 0.5'}, {'reference_code': 'FINAL001', 'display_name': 'Final Result', 'data_source': 'Calculated Amount', 'calculation_formula': 'MIXED001 + API001'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
order = resolver.get_processing_order()
positions = {row.reference_code: i for i, row in enumerate(order)}
self.assertLess(positions['API001'], positions['ACC001'])
self.assertLess(positions['API001'], positions['MIXED001'])
self.assertLess(positions['ACC001'], positions['MIXED001'])
self.assertLess(positions['MIXED001'], positions['FINAL001'])
self.assertEqual(set(resolver.dependencies['MIXED001']), {'API001', 'ACC001'})
self.assertEqual(set(resolver.dependencies['FINAL001']), {'MIXED001', 'API001'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:357*

### test_extract_from_complex_formulas

**Category**: workflow  
**Description**: Workflow: test extract from complex formulas  
**Expected**: self.assertEqual(set(net_deps), {'INCOME', 'EXPENSE', 'TAX_RATE'})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_rows = [{'reference_code': 'INCOME', 'display_name': 'Total Income', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Income"]'}, {'reference_code': 'EXPENSE', 'display_name': 'Total Expense', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["root_type", "=", "Expense"]'}, {'reference_code': 'TAX_RATE', 'display_name': 'Tax Rate', 'data_source': 'Account Data', 'balance_type': 'Closing Balance', 'calculation_formula': '["account_name", "like", "Tax"]'}, {'reference_code': 'NET_RESULT', 'display_name': 'Net Result', 'data_source': 'Calculated Amount', 'calculation_formula': '(INCOME - EXPENSE) * (1 - TAX_RATE / 100)'}]
test_template = FinancialReportTemplateTestCase.create_test_template_with_rows(test_rows)
resolver = DependencyResolver(test_template)
net_deps = resolver.dependencies.get('NET_RESULT', [])
self.assertEqual(set(net_deps), {'INCOME', 'EXPENSE', 'TAX_RATE'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/financial_report_template/test_financial_report_engine.py:405*

### test_discount_and_inclusive_tax

**Category**: workflow  
**Description**: Workflow: test discount and inclusive tax  
**Expected**: self.assertEqual(inv.grand_total, 4900.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_pos_invoice(qty=100, rate=50, do_not_save=1)
inv.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 14, 'included_in_print_rate': 1})
inv.insert()
self.assertEqual(inv.net_total, 4385.96)
self.assertEqual(inv.grand_total, 5000)
inv.reload()
inv.discount_amount = 100
inv.apply_discount_on = 'Net Total'
inv.payment_schedule = []
inv.save()
self.assertEqual(inv.net_total, 4285.96)
self.assertEqual(inv.grand_total, 4885.99)
inv.reload()
inv.discount_amount = 100
inv.apply_discount_on = 'Grand Total'
inv.payment_schedule = []
inv.save()
self.assertEqual(inv.net_total, 4298.24)
self.assertEqual(inv.grand_total, 4900.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:79*

### test_tax_calculation_with_multiple_items

**Category**: workflow  
**Description**: Workflow: test tax calculation with multiple items  
**Expected**: self.assertEqual(inv.grand_total, 5474.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_pos_invoice(qty=84, rate=4.6, do_not_save=True)
item_row = inv.get('items')[0]
for qty in (54, 288, 144, 430):
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.qty = qty
    inv.append('items', item_row_copy)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 19})
inv.insert()
self.assertEqual(inv.net_total, 4600)
self.assertEqual(inv.get('taxes')[0].tax_amount, 874.0)
self.assertEqual(inv.get('taxes')[0].total, 5474.0)
self.assertEqual(inv.grand_total, 5474.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:119*

### test_tax_calculation_with_item_tax_template

**Category**: workflow  
**Description**: Workflow: test tax calculation with item tax template  
**Expected**: self.assertEqual(inv.rounded_total, 5676.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_pos_invoice(qty=84, rate=4.6, do_not_save=1)
item_row = inv.get('items')[0]
add_items = [(54, '_Test Account Excise Duty @ 12 - _TC'), (288, '_Test Account Excise Duty @ 15 - _TC'), (144, '_Test Account Excise Duty @ 20 - _TC'), (430, '_Test Item Tax Template 1 - _TC')]
for qty, item_tax_template in add_items:
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.qty = qty
    item_row_copy.item_tax_template = item_tax_template
    inv.append('items', item_row_copy)
inv.append('taxes', {'account_head': '_Test Account Excise Duty - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Excise Duty', 'doctype': 'Sales Taxes and Charges', 'rate': 11})
inv.append('taxes', {'account_head': '_Test Account Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 0})
inv.append('taxes', {'account_head': '_Test Account S&H Education Cess - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'S&H Education Cess', 'doctype': 'Sales Taxes and Charges', 'rate': 3})
inv.insert()
self.assertEqual(inv.net_total, 4600)
self.assertEqual(inv.get('taxes')[0].tax_amount, 502.41)
self.assertEqual(inv.get('taxes')[0].total, 5102.41)
self.assertEqual(inv.get('taxes')[1].tax_amount, 197.8)
self.assertEqual(inv.get('taxes')[1].total, 5300.21)
self.assertEqual(inv.get('taxes')[2].tax_amount, 375.36)
self.assertEqual(inv.get('taxes')[2].total, 5675.57)
self.assertEqual(inv.grand_total, 5675.57)
self.assertEqual(inv.rounding_adjustment, 0.43)
self.assertEqual(inv.rounded_total, 5676.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:147*

### test_tax_calculation_with_multiple_items_and_discount

**Category**: workflow  
**Description**: Workflow: test tax calculation with multiple items and discount  
**Expected**: self.assertEqual(inv.grand_total, 1116.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv = create_pos_invoice(qty=1, rate=75, do_not_save=True)
item_row = inv.get('items')[0]
for rate in (500, 200, 100, 50, 50):
    item_row_copy = copy.deepcopy(item_row)
    item_row_copy.price_list_rate = rate
    item_row_copy.rate = rate
    inv.append('items', item_row_copy)
inv.apply_discount_on = 'Net Total'
inv.discount_amount = 75.0
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 24})
inv.insert()
self.assertEqual(inv.total, 975)
self.assertEqual(inv.net_total, 900)
self.assertEqual(inv.get('taxes')[0].tax_amount, 216.0)
self.assertEqual(inv.get('taxes')[0].total, 1116.0)
self.assertEqual(inv.grand_total, 1116.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:213*

### test_pos_return_for_serialized_item

**Category**: workflow  
**Description**: Workflow: test pos return for serialized item  
**Expected**: self.assertEqual(get_serial_nos_from_bundle(pos_return.get('items')[0].serial_and_batch_bundle)[0], serial_nos[0])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, serial_no=[serial_nos[0]], rate=1000, do_not_save=1)
pos.append('payments', {'mode_of_payment': 'Cash', 'amount': 1000, 'default': 1})
pos.insert()
pos.submit()
pos_return = make_sales_return(pos.name)
pos_return.insert()
pos_return.submit()
self.assertEqual(get_serial_nos_from_bundle(pos_return.get('items')[0].serial_and_batch_bundle)[0], serial_nos[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:263*

### test_partial_pos_returns

**Category**: workflow  
**Description**: Workflow: test partial pos returns  
**Expected**: self.assertEqual(serial_no, serial_nos[1])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, serial_no=serial_nos, qty=2, rate=1000, do_not_save=1)
pos.append('payments', {'mode_of_payment': 'Cash', 'amount': 2000, 'default': 1})
pos.insert()
pos.submit()
pos.reload()
pos_return1 = make_sales_return(pos.name)
pos_return1.get('items')[0].qty = -1
pos_return1.set('payments', [])
pos_return1.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
pos_return1.paid_amount = -1000
pos_return1.submit()
pos_return1.reload()
bundle_id = frappe.get_doc('Serial and Batch Bundle', pos_return1.get('items')[0].serial_and_batch_bundle)
bundle_id.load_from_db()
serial_no = bundle_id.entries[0].serial_no
self.assertEqual(serial_no, serial_nos[0])
pos_return2 = make_sales_return(pos.name)
pos_return2.set('payments', [])
pos_return2.append('payments', {'mode_of_payment': 'Cash', 'amount': -1000, 'default': 1})
pos_return2.paid_amount = -1000
pos_return2.submit()
self.assertEqual(pos_return2.get('items')[0].qty, -1)
serial_no = get_serial_nos_from_bundle(pos_return2.get('items')[0].serial_and_batch_bundle)[0]
self.assertEqual(serial_no, serial_nos[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:303*

### test_serialized_item_transaction

**Category**: workflow  
**Description**: Workflow: test serialized item transaction  
**Expected**: self.assertRaises(frappe.ValidationError, pos2.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
pos.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
pos.insert()
pos.submit()
pos2 = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1)
pos2.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
pos2.insert()
self.assertRaises(frappe.ValidationError, pos2.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:447*

### test_delivered_serialized_item_transaction

**Category**: workflow  
**Description**: Workflow: test delivered serialized item transaction  
**Expected**: self.assertRaises(frappe.ValidationError, pos2.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
si = create_sales_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, update_stock=1, serial_no=[serial_nos[0]], do_not_save=1)
si.insert()
si.submit()
pos2 = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], do_not_save=1, ignore_sabb_validation=True)
pos2.append('payments', {'mode_of_payment': 'Bank Draft', 'amount': 1000})
pos2.insert()
self.assertRaises(frappe.ValidationError, pos2.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:498*

### test_invalid_serial_no_validation

**Category**: workflow  
**Description**: Workflow: test invalid serial no validation  
**Expected**: self.assertRaises(frappe.ValidationError, pos.insert)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0] + 'wrong'
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, qty=2, serial_nos=[serial_nos], do_not_save=1)
pos.get('items')[0].has_serial_no = 1
self.assertRaises(frappe.ValidationError, pos.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:549*

### test_value_error_on_serial_no_validation

**Category**: workflow  
**Description**: Workflow: test value error on serial no validation  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self, company='_Test Company', target_warehouse='Stores - _TC', cost_center='Main - _TC', expense_account='Cost of Goods Sold - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
pos = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], qty=1, do_not_save=1)
pos.get('items')[0].has_serial_no = 1
pos.set('payments', [])
pos.append('payments', {'mode_of_payment': 'Cash', 'amount': 1000, 'default': 1})
pos = pos.save().submit()
pos_return = make_sales_return(pos.name)
pos_return.paid_amount = pos_return.grand_total
pos_return.save()
pos_return.submit()
frappe.db.set_value('POS Invoice', pos.name, 'docstatus', 2)
pos2 = create_pos_invoice(company='_Test Company', debit_to='Debtors - _TC', account_for_change_amount='Cash - _TC', warehouse='Stores - _TC', income_account='Sales - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC', item=se.get('items')[0].item_code, rate=1000, serial_no=[serial_nos[0]], qty=1, do_not_save=1)
pos2.get('items')[0].has_serial_no = 1
pos2.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice/test_pos_invoice.py:580*

### test_tax_withholding_for_customers

**Category**: workflow  
**Description**: Workflow: test tax withholding for customers  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

create_tax_category(cumulative_threshold=300)
frappe.db.set_value('Customer', '_Test Customer', 'tax_withholding_category', 'TCS')
si = create_sales_invoice(rate=1000)
pe = create_tcs_payment_entry()
jv = create_tcs_journal_entry()
filters = frappe._dict(company='_Test Company', party_type='Customer', from_date=today(), to_date=today())
result = execute(filters)[1]
expected_values = [[jv.name, 'TCS', 0.075, -10000.0, -7.5, -10000.0], [pe.name, 'TCS', 0.075, 2550, 0.53, 2550.53], [si.name, 'TCS', 0.075, 1000, 0.52, 1000.52]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:25*

### test_single_account_for_multiple_categories

**Category**: workflow  
**Description**: Workflow: test single account for multiple categories  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

create_tax_category('TDS - 1', rate=10, account='TDS - _TC')
inv_1 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_1.tax_withholding_category = 'TDS - 1'
inv_1.submit()
create_tax_category('TDS - 2', rate=20, account='TDS - _TC')
inv_2 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_2.tax_withholding_category = 'TDS - 2'
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=today(), to_date=today()))[1]
expected_values = [[inv_1.name, 'TDS - 1', 10, 5000, 500, 5500], [inv_2.name, 'TDS - 2', 20, 5000, 1000, 6000]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:44*

### test_date_filters_in_multiple_tax_withholding_rules

**Category**: workflow  
**Description**: Workflow: test date filters in multiple tax withholding rules  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

create_tax_category('TDS - 3', rate=10, account='TDS - _TC', cumulative_threshold=1)
fiscal_year = get_fiscal_year(today(), company='_Test Company')
mid_year = add_to_date(fiscal_year[1], months=6)
tds_doc = frappe.get_doc('Tax Withholding Category', 'TDS - 3')
tds_doc.rates[0].to_date = mid_year
from_date = add_to_date(mid_year, days=1)
tds_doc.append('rates', {'tax_withholding_rate': 20, 'from_date': from_date, 'to_date': fiscal_year[2], 'single_threshold': 1, 'cumulative_threshold': 1})
tds_doc.save()
inv_1 = make_purchase_invoice(rate=1000, posting_date=add_to_date(fiscal_year[1], days=1), do_not_save=True, do_not_submit=True)
inv_1.set_posting_time = 1
inv_1.apply_tds = 1
inv_1.tax_withholding_category = tds_doc.name
inv_1.save()
inv_1.submit()
inv_2 = make_purchase_invoice(rate=1000, posting_date=from_date, do_not_save=True, do_not_submit=True)
inv_2.set_posting_time = 1
inv_2.apply_tds = 1
inv_2.tax_withholding_category = tds_doc.name
inv_2.save()
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=fiscal_year[1], to_date=fiscal_year[2]))[1]
expected_values = [[inv_1.name, 'TDS - 3', 10.0, 5000, 500, 4500], [inv_2.name, 'TDS - 3', 20.0, 5000, 1000, 4000]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:63*

### test_tax_withholding_for_customers

**Category**: workflow  
**Description**: Workflow: test tax withholding for customers  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
create_tax_category(cumulative_threshold=300)
frappe.db.set_value('Customer', '_Test Customer', 'tax_withholding_category', 'TCS')
si = create_sales_invoice(rate=1000)
pe = create_tcs_payment_entry()
jv = create_tcs_journal_entry()
filters = frappe._dict(company='_Test Company', party_type='Customer', from_date=today(), to_date=today())
result = execute(filters)[1]
expected_values = [[jv.name, 'TCS', 0.075, -10000.0, -7.5, -10000.0], [pe.name, 'TCS', 0.075, 2550, 0.53, 2550.53], [si.name, 'TCS', 0.075, 1000, 0.52, 1000.52]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:25*

### test_single_account_for_multiple_categories

**Category**: workflow  
**Description**: Workflow: test single account for multiple categories  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
create_tax_category('TDS - 1', rate=10, account='TDS - _TC')
inv_1 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_1.tax_withholding_category = 'TDS - 1'
inv_1.submit()
create_tax_category('TDS - 2', rate=20, account='TDS - _TC')
inv_2 = make_purchase_invoice(rate=1000, do_not_submit=True)
inv_2.tax_withholding_category = 'TDS - 2'
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=today(), to_date=today()))[1]
expected_values = [[inv_1.name, 'TDS - 1', 10, 5000, 500, 5500], [inv_2.name, 'TDS - 2', 20, 5000, 1000, 6000]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:44*

### test_date_filters_in_multiple_tax_withholding_rules

**Category**: workflow  
**Description**: Workflow: test date filters in multiple tax withholding rules  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
create_tax_category('TDS - 3', rate=10, account='TDS - _TC', cumulative_threshold=1)
fiscal_year = get_fiscal_year(today(), company='_Test Company')
mid_year = add_to_date(fiscal_year[1], months=6)
tds_doc = frappe.get_doc('Tax Withholding Category', 'TDS - 3')
tds_doc.rates[0].to_date = mid_year
from_date = add_to_date(mid_year, days=1)
tds_doc.append('rates', {'tax_withholding_rate': 20, 'from_date': from_date, 'to_date': fiscal_year[2], 'single_threshold': 1, 'cumulative_threshold': 1})
tds_doc.save()
inv_1 = make_purchase_invoice(rate=1000, posting_date=add_to_date(fiscal_year[1], days=1), do_not_save=True, do_not_submit=True)
inv_1.set_posting_time = 1
inv_1.apply_tds = 1
inv_1.tax_withholding_category = tds_doc.name
inv_1.save()
inv_1.submit()
inv_2 = make_purchase_invoice(rate=1000, posting_date=from_date, do_not_save=True, do_not_submit=True)
inv_2.set_posting_time = 1
inv_2.apply_tds = 1
inv_2.tax_withholding_category = tds_doc.name
inv_2.save()
inv_2.submit()
result = execute(frappe._dict(company='_Test Company', party_type='Supplier', from_date=fiscal_year[1], to_date=fiscal_year[2]))[1]
expected_values = [[inv_1.name, 'TDS - 3', 10.0, 5000, 500, 4500], [inv_2.name, 'TDS - 3', 20.0, 5000, 1000, 4000]]
self.check_expected_values(result, expected_values)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:63*

### test_merge_success

**Category**: workflow  
**Description**: Workflow: test merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', 'Indirect Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Expenses'
    acc.parent_account = 'Indirect Test Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Test Expenses - _TC', 'root_type'), 'account': 'Indirect Expenses - _TC', 'merge_accounts': [{'account': 'Indirect Test Expenses - _TC', 'account_name': 'Indirect Expenses'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Expenses - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Expenses - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:11*

### test_partial_merge_success

**Category**: workflow  
**Description**: Workflow: test partial merge success  
**Expected**: self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', 'Indirect Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Income'
    acc.parent_account = 'Indirect Test Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Income - _TC', 'root_type'), 'account': 'Indirect Income - _TC', 'merge_accounts': [{'account': 'Indirect Test Income - _TC', 'account_name': 'Indirect Test Income'}, {'account': 'Administrative Test Income - _TC', 'account_name': 'Administrative Test Income'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Income - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Income - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:55*

### test_merge_success

**Category**: workflow  
**Description**: Workflow: test merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', 'Indirect Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Expenses'
    acc.is_group = 1
    acc.parent_account = 'Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Expenses - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Expenses'
    acc.parent_account = 'Indirect Test Expenses - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Test Expenses - _TC', 'root_type'), 'account': 'Indirect Expenses - _TC', 'merge_accounts': [{'account': 'Indirect Test Expenses - _TC', 'account_name': 'Indirect Expenses'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Expenses - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Expenses - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Expenses - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:11*

### test_partial_merge_success

**Category**: workflow  
**Description**: Workflow: test partial merge success  
**Expected**: self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.exists('Account', 'Indirect Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Indirect Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Indirect Test Income'
    acc.is_group = 1
    acc.parent_account = 'Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
if not frappe.db.exists('Account', 'Administrative Test Income - _TC'):
    acc = frappe.new_doc('Account')
    acc.account_name = 'Administrative Test Income'
    acc.parent_account = 'Indirect Test Income - _TC'
    acc.company = '_Test Company'
    acc.insert()
doc = frappe.get_doc({'doctype': 'Ledger Merge', 'company': '_Test Company', 'root_type': frappe.db.get_value('Account', 'Indirect Income - _TC', 'root_type'), 'account': 'Indirect Income - _TC', 'merge_accounts': [{'account': 'Indirect Test Income - _TC', 'account_name': 'Indirect Test Income'}, {'account': 'Administrative Test Income - _TC', 'account_name': 'Administrative Test Income'}]}).insert(ignore_permissions=True)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Test Income - _TC')
start_merge(doc.name)
parent = frappe.db.get_value('Account', 'Administrative Test Income - _TC', 'parent_account')
self.assertEqual(parent, 'Indirect Income - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:55*

### test_create_test_data

**Category**: workflow  
**Description**: Workflow: test create test data  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.set_user('Administrator')
if not frappe.db.exists('Item', '_Test Tesla Car'):
    item = frappe.get_doc({'description': '_Test Tesla Car', 'doctype': 'Item', 'has_batch_no': 0, 'has_serial_no': 0, 'inspection_required': 0, 'is_stock_item': 1, 'opening_stock': 100, 'is_sub_contracted_item': 0, 'item_code': '_Test Tesla Car', 'item_group': '_Test Item Group', 'item_name': '_Test Tesla Car', 'apply_warehouse_wise_reorder_level': 0, 'warehouse': 'Stores - _TC', 'valuation_rate': 5000, 'standard_rate': 5000, 'item_defaults': [{'company': '_Test Company', 'default_warehouse': 'Stores - _TC', 'default_price_list': '_Test Price List', 'expense_account': 'Cost of Goods Sold - _TC', 'buying_cost_center': 'Main - _TC', 'selling_cost_center': 'Main - _TC', 'income_account': 'Sales - _TC'}]})
    item.insert()
item_price = frappe.get_list('Item Price', filters={'item_code': '_Test Tesla Car', 'price_list': '_Test Price List'}, fields=['name'])
if len(item_price) == 0:
    item_price = frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test Tesla Car', 'price_list': '_Test Price List', 'price_list_rate': 5000})
    item_price.insert()
if not frappe.db.exists('Pricing Rule', {'title': '_Test Pricing Rule for _Test Item'}):
    item_pricing_rule = frappe.get_doc({'doctype': 'Pricing Rule', 'title': '_Test Pricing Rule for _Test Item', 'apply_on': 'Item Code', 'items': [{'item_code': '_Test Tesla Car'}], 'warehouse': 'Stores - _TC', 'coupon_code_based': 1, 'selling': 1, 'rate_or_discount': 'Discount Percentage', 'discount_percentage': 30, 'company': '_Test Company', 'currency': 'INR', 'for_price_list': '_Test Price List'})
    item_pricing_rule.insert()
if not frappe.db.exists('Sales Partner', '_Test Coupon Partner'):
    sales_partner = frappe.get_doc({'doctype': 'Sales Partner', 'partner_name': '_Test Coupon Partner', 'commission_rate': 2, 'referral_code': 'COPART'})
    sales_partner.insert()
if not frappe.db.exists('Coupon Code', 'SAVE30'):
    pricing_rule = frappe.db.get_value('Pricing Rule', {'title': '_Test Pricing Rule for _Test Item'}, ['name'])
    coupon_code = frappe.get_doc({'doctype': 'Coupon Code', 'coupon_name': 'SAVE30', 'coupon_code': 'SAVE30', 'pricing_rule': pricing_rule, 'valid_from': '2014-01-01', 'maximum_use': 1, 'used': 0})
    coupon_code.insert()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:12*

### test_finance_book

**Category**: workflow  
**Description**: Workflow: test finance book  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
finance_book = create_finance_book()
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
jv.accounts[1].update({'party_type': 'Customer', 'party': '_Test Customer'})
jv.finance_book = finance_book.finance_book_name
jv.submit()
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
for gl_entry in gl_entries:
    self.assertEqual(gl_entry.finance_book, finance_book.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:11*

### test_finance_book

**Category**: workflow  
**Description**: Workflow: test finance book  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
finance_book = create_finance_book()
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
jv.accounts[1].update({'party_type': 'Customer', 'party': '_Test Customer'})
jv.finance_book = finance_book.finance_book_name
jv.submit()
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
for gl_entry in gl_entries:
    self.assertEqual(gl_entry.finance_book, finance_book.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:11*

### test_excluded_fee_noop_when_zero

**Category**: workflow  
**Description**: Workflow: When there is no excluded fee to apply, the amounts should remain
unchanged.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When there is no excluded fee to apply, the amounts should remain\n\t\tunchanged.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 100
bt.withdrawal = 0
bt.included_fee = 5
bt.excluded_fee = 0
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 100)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:36*

### test_excluded_fee_deducts_from_deposit

**Category**: workflow  
**Description**: Workflow: When a fee is deducted from an incoming payment, the net received
amount decreases and the fee is tracked as included.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When a fee is deducted from an incoming payment, the net received\n\t\tamount decreases and the fee is tracked as included.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 100
bt.withdrawal = 0
bt.included_fee = 2
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 95)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 7)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:71*

### test_excluded_fee_can_reduce_an_incoming_payment_to_zero

**Category**: workflow  
**Description**: Workflow: A separately-deducted fee may reduce an incoming payment to zero,
while still tracking the fee.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'A separately-deducted fee may reduce an incoming payment to zero,\n\t\twhile still tracking the fee.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 5
bt.withdrawal = 0
bt.included_fee = 0
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:87*

### test_excluded_fee_increases_outgoing_payment

**Category**: workflow  
**Description**: Workflow: When a separately-deducted fee is provided for an outgoing payment,
the total money leaving increases and the fee is tracked.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When a separately-deducted fee is provided for an outgoing payment,\n\t\tthe total money leaving increases and the fee is tracked.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 100
bt.included_fee = 2
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 105)
self.assertEqual(bt.included_fee, 7)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:103*

### test_excluded_fee_turns_zero_amount_into_withdrawal

**Category**: workflow  
**Description**: Workflow: If only an excluded fee is provided, it should be treated as an
outgoing payment and the fee is then tracked as included.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'If only an excluded fee is provided, it should be treated as an\n\t\toutgoing payment and the fee is then tracked as included.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 0
bt.included_fee = 0
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 5)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:119*

### test_excluded_fee_noop_when_zero

**Category**: workflow  
**Description**: Workflow: When there is no excluded fee to apply, the amounts should remain
unchanged.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When there is no excluded fee to apply, the amounts should remain\n\t\tunchanged.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 100
bt.withdrawal = 0
bt.included_fee = 5
bt.excluded_fee = 0
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 100)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:36*

### test_excluded_fee_deducts_from_deposit

**Category**: workflow  
**Description**: Workflow: When a fee is deducted from an incoming payment, the net received
amount decreases and the fee is tracked as included.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When a fee is deducted from an incoming payment, the net received\n\t\tamount decreases and the fee is tracked as included.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 100
bt.withdrawal = 0
bt.included_fee = 2
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 95)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 7)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:71*

### test_excluded_fee_can_reduce_an_incoming_payment_to_zero

**Category**: workflow  
**Description**: Workflow: A separately-deducted fee may reduce an incoming payment to zero,
while still tracking the fee.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'A separately-deducted fee may reduce an incoming payment to zero,\n\t\twhile still tracking the fee.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 5
bt.withdrawal = 0
bt.included_fee = 0
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 0)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:87*

### test_excluded_fee_increases_outgoing_payment

**Category**: workflow  
**Description**: Workflow: When a separately-deducted fee is provided for an outgoing payment,
the total money leaving increases and the fee is tracked.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'When a separately-deducted fee is provided for an outgoing payment,\n\t\tthe total money leaving increases and the fee is tracked.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 100
bt.included_fee = 2
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 105)
self.assertEqual(bt.included_fee, 7)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:103*

### test_excluded_fee_turns_zero_amount_into_withdrawal

**Category**: workflow  
**Description**: Workflow: If only an excluded fee is provided, it should be treated as an
outgoing payment and the fee is then tracked as included.  
**Expected**: self.assertEqual(bt.excluded_fee, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'If only an excluded fee is provided, it should be treated as an\n\t\toutgoing payment and the fee is then tracked as included.'
bt = frappe.new_doc('Bank Transaction')
bt.deposit = 0
bt.withdrawal = 0
bt.included_fee = 0
bt.excluded_fee = 5
bt.handle_excluded_fee()
self.assertEqual(bt.deposit, 0)
self.assertEqual(bt.withdrawal, 5)
self.assertEqual(bt.included_fee, 5)
self.assertEqual(bt.excluded_fee, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction_fees.py:119*

### test_opening_sales_invoice_creation_with_missing_debit_account

**Category**: workflow  
**Description**: Workflow: test opening sales invoice creation with missing debit account  
**Expected**: self.assertTrue(error_log)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
old_default_receivable_account = frappe.db.get_value('Company', company, 'default_receivable_account')
frappe.db.set_value('Company', company, 'default_receivable_account', '')
if not frappe.db.exists('Cost Center', '_Test Opening Invoice Company - _TOIC'):
    cc = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Opening Invoice Company', 'is_group': 1, 'company': '_Test Opening Invoice Company'})
    cc.insert(ignore_mandatory=True)
    cc2 = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': 'Main', 'is_group': 0, 'company': '_Test Opening Invoice Company', 'parent_cost_center': cc.name})
    cc2.insert()
frappe.db.set_value('Company', company, 'cost_center', 'Main - _TOIC')
self.make_invoices(company='_Test Opening Invoice Company', party_1=party_1, party_2=party_2)
error_log = frappe.db.exists('Error Log', {'error': ['like', '%erpnext.controllers.accounts_controller.AccountMissingError%']})
self.assertTrue(error_log)
frappe.db.set_value('Company', company, 'default_receivable_account', old_default_receivable_account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:82*

### test_renaming_of_invoice_using_invoice_number_field

**Category**: workflow  
**Description**: Workflow: test renaming of invoice using invoice number field  
**Expected**: self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
self.make_invoices(company=company, party_1=party_1, party_2=party_2, invoice_number='TEST-NEW-INV-11')
sales_inv1 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer A'})[0].get('name')
sales_inv2 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer B'})[0].get('name')
self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')
for inv in [sales_inv1, sales_inv2]:
    doc = frappe.get_doc('Sales Invoice', inv)
    doc.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:124*

### test_opening_sales_invoice_creation_with_missing_debit_account

**Category**: workflow  
**Description**: Workflow: test opening sales invoice creation with missing debit account  
**Expected**: self.assertTrue(error_log)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
old_default_receivable_account = frappe.db.get_value('Company', company, 'default_receivable_account')
frappe.db.set_value('Company', company, 'default_receivable_account', '')
if not frappe.db.exists('Cost Center', '_Test Opening Invoice Company - _TOIC'):
    cc = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Opening Invoice Company', 'is_group': 1, 'company': '_Test Opening Invoice Company'})
    cc.insert(ignore_mandatory=True)
    cc2 = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': 'Main', 'is_group': 0, 'company': '_Test Opening Invoice Company', 'parent_cost_center': cc.name})
    cc2.insert()
frappe.db.set_value('Company', company, 'cost_center', 'Main - _TOIC')
self.make_invoices(company='_Test Opening Invoice Company', party_1=party_1, party_2=party_2)
error_log = frappe.db.exists('Error Log', {'error': ['like', '%erpnext.controllers.accounts_controller.AccountMissingError%']})
self.assertTrue(error_log)
frappe.db.set_value('Company', company, 'default_receivable_account', old_default_receivable_account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:82*

### test_renaming_of_invoice_using_invoice_number_field

**Category**: workflow  
**Description**: Workflow: test renaming of invoice using invoice number field  
**Expected**: self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Opening Invoice Company'
party_1, party_2 = (make_customer('Customer A'), make_customer('Customer B'))
self.make_invoices(company=company, party_1=party_1, party_2=party_2, invoice_number='TEST-NEW-INV-11')
sales_inv1 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer A'})[0].get('name')
sales_inv2 = frappe.get_all('Sales Invoice', filters={'customer': 'Customer B'})[0].get('name')
self.assertEqual(sales_inv1, 'TEST-NEW-INV-11')
for inv in [sales_inv1, sales_inv2]:
    doc = frappe.get_doc('Sales Invoice', inv)
    doc.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:124*

### test_dunning_with_payment_entry

**Category**: workflow  
**Description**: Workflow: test dunning with payment entry  
**Expected**: self.assertEqual(dunning.status, 'Resolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
dunning = create_dunning(overdue_days=15, dunning_type_name='Second Notice - _TC')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.insert()
pe.submit()
for overdue_payment in dunning.overdue_payments:
    outstanding_amount = frappe.get_value('Sales Invoice', overdue_payment.sales_invoice, 'outstanding_amount')
    self.assertEqual(outstanding_amount, 0)
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:56*

### test_fetch_overdue_payments

**Category**: workflow  
**Description**: Workflow: Create SI with overdue payment. Check if overdue payment is fetched in Dunning.  
**Expected**: self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tCreate SI with overdue payment. Check if overdue payment is fetched in Dunning.\n\t\t'
si1 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100)
si2 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=300)
dunning = create_dunning_from_sales_invoice(si1.name)
dunning.overdue_payments = []
method = 'erpnext.accounts.doctype.sales_invoice.sales_invoice.create_dunning'
updated_dunning = mapper.map_docs(method, json.dumps([si1.name, si2.name]), dunning)
self.assertEqual(len(updated_dunning.overdue_payments), 2)
self.assertEqual(updated_dunning.overdue_payments[0].sales_invoice, si1.name)
self.assertEqual(updated_dunning.overdue_payments[0].outstanding, si1.outstanding_amount)
self.assertEqual(updated_dunning.overdue_payments[1].sales_invoice, si2.name)
self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:74*

### test_dunning_and_payment_against_partially_due_invoice

**Category**: workflow  
**Description**: Workflow: Create SI with first installment overdue. Check impact of Dunning and Payment Entry.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tCreate SI with first installment overdue. Check impact of Dunning and Payment Entry.\n\t\t'
create_payment_terms_template_for_dunning()
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100, do_not_submit=True)
sales_invoice.payment_terms_template = '_Test 50-50 for Dunning'
sales_invoice.submit()
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
self.assertEqual(len(dunning.overdue_payments), 1)
self.assertEqual(dunning.overdue_payments[0].payment_term, '_Test Payment Term 1 for Dunning')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no, pe.reference_date = ('2', nowdate())
pe.insert()
pe.submit()
sales_invoice.load_from_db()
dunning.load_from_db()
self.assertEqual(sales_invoice.status, 'Partly Paid')
self.assertEqual(sales_invoice.payment_schedule[0].outstanding, 0)
self.assertEqual(dunning.status, 'Resolved')
pe.cancel()
sales_invoice.reload()
dunning.reload()
self.assertEqual(sales_invoice.status, 'Overdue')
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:104*

### test_dunning_resolution_from_credit_note

**Category**: workflow  
**Description**: Workflow: Test that dunning is resolved when a credit note is issued against the original invoice.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest that dunning is resolved when a credit note is issued against the original invoice.\n\t\t'
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
dunning.submit()
self.assertEqual(dunning.status, 'Unresolved')
credit_note = frappe.copy_doc(sales_invoice)
credit_note.is_return = 1
credit_note.return_against = sales_invoice.name
credit_note.update_outstanding_for_self = 0
for item in credit_note.items:
    item.qty = -item.qty
credit_note.save()
credit_note.submit()
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
credit_note.cancel()
dunning.reload()
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:142*

### test_dunning_not_affected_by_standalone_credit_note

**Category**: workflow  
**Description**: Workflow: Test that dunning is NOT resolved when a credit note has update_outstanding_for_self checked.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest that dunning is NOT resolved when a credit note has update_outstanding_for_self checked.\n\t\t'
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
dunning.submit()
self.assertEqual(dunning.status, 'Unresolved')
credit_note = frappe.copy_doc(sales_invoice)
credit_note.is_return = 1
credit_note.return_against = sales_invoice.name
credit_note.update_outstanding_for_self = 1
for item in credit_note.items:
    item.qty = -item.qty
credit_note.save()
credit_note = frappe.get_doc('Sales Invoice', credit_note.name)
credit_note.submit()
dunning.reload()
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:172*

### test_dunning_with_payment_entry

**Category**: workflow  
**Description**: Workflow: test dunning with payment entry  
**Expected**: self.assertEqual(dunning.status, 'Resolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
dunning = create_dunning(overdue_days=15, dunning_type_name='Second Notice - _TC')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no = '1'
pe.reference_date = nowdate()
pe.insert()
pe.submit()
for overdue_payment in dunning.overdue_payments:
    outstanding_amount = frappe.get_value('Sales Invoice', overdue_payment.sales_invoice, 'outstanding_amount')
    self.assertEqual(outstanding_amount, 0)
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:56*

### test_fetch_overdue_payments

**Category**: workflow  
**Description**: Workflow: Create SI with overdue payment. Check if overdue payment is fetched in Dunning.  
**Expected**: self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tCreate SI with overdue payment. Check if overdue payment is fetched in Dunning.\n\t\t'
si1 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100)
si2 = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=300)
dunning = create_dunning_from_sales_invoice(si1.name)
dunning.overdue_payments = []
method = 'erpnext.accounts.doctype.sales_invoice.sales_invoice.create_dunning'
updated_dunning = mapper.map_docs(method, json.dumps([si1.name, si2.name]), dunning)
self.assertEqual(len(updated_dunning.overdue_payments), 2)
self.assertEqual(updated_dunning.overdue_payments[0].sales_invoice, si1.name)
self.assertEqual(updated_dunning.overdue_payments[0].outstanding, si1.outstanding_amount)
self.assertEqual(updated_dunning.overdue_payments[1].sales_invoice, si2.name)
self.assertEqual(updated_dunning.overdue_payments[1].outstanding, si2.outstanding_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:74*

### test_dunning_and_payment_against_partially_due_invoice

**Category**: workflow  
**Description**: Workflow: Create SI with first installment overdue. Check impact of Dunning and Payment Entry.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tCreate SI with first installment overdue. Check impact of Dunning and Payment Entry.\n\t\t'
create_payment_terms_template_for_dunning()
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -1 * 6), qty=1, rate=100, do_not_submit=True)
sales_invoice.payment_terms_template = '_Test 50-50 for Dunning'
sales_invoice.submit()
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
self.assertEqual(len(dunning.overdue_payments), 1)
self.assertEqual(dunning.overdue_payments[0].payment_term, '_Test Payment Term 1 for Dunning')
dunning.submit()
pe = get_payment_entry('Dunning', dunning.name)
pe.reference_no, pe.reference_date = ('2', nowdate())
pe.insert()
pe.submit()
sales_invoice.load_from_db()
dunning.load_from_db()
self.assertEqual(sales_invoice.status, 'Partly Paid')
self.assertEqual(sales_invoice.payment_schedule[0].outstanding, 0)
self.assertEqual(dunning.status, 'Resolved')
pe.cancel()
sales_invoice.reload()
dunning.reload()
self.assertEqual(sales_invoice.status, 'Overdue')
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:104*

### test_dunning_resolution_from_credit_note

**Category**: workflow  
**Description**: Workflow: Test that dunning is resolved when a credit note is issued against the original invoice.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest that dunning is resolved when a credit note is issued against the original invoice.\n\t\t'
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
dunning.submit()
self.assertEqual(dunning.status, 'Unresolved')
credit_note = frappe.copy_doc(sales_invoice)
credit_note.is_return = 1
credit_note.return_against = sales_invoice.name
credit_note.update_outstanding_for_self = 0
for item in credit_note.items:
    item.qty = -item.qty
credit_note.save()
credit_note.submit()
dunning.reload()
self.assertEqual(dunning.status, 'Resolved')
credit_note.cancel()
dunning.reload()
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:142*

### test_dunning_not_affected_by_standalone_credit_note

**Category**: workflow  
**Description**: Workflow: Test that dunning is NOT resolved when a credit note has update_outstanding_for_self checked.  
**Expected**: self.assertEqual(dunning.status, 'Unresolved')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest that dunning is NOT resolved when a credit note has update_outstanding_for_self checked.\n\t\t'
sales_invoice = create_sales_invoice_against_cost_center(posting_date=add_days(today(), -10), qty=1, rate=100)
dunning = create_dunning_from_sales_invoice(sales_invoice.name)
dunning.submit()
self.assertEqual(dunning.status, 'Unresolved')
credit_note = frappe.copy_doc(sales_invoice)
credit_note.is_return = 1
credit_note.return_against = sales_invoice.name
credit_note.update_outstanding_for_self = 1
for item in credit_note.items:
    item.qty = -item.qty
credit_note.save()
credit_note = frappe.get_doc('Sales Invoice', credit_note.name)
credit_note.submit()
dunning.reload()
self.assertEqual(dunning.status, 'Unresolved')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/dunning/test_dunning.py:172*

### test_creation_of_ledger_entry_on_submit

**Category**: workflow  
**Description**: Workflow: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'test creation of gl entries on submission of document'
change_acc_settings(acc_frozen_till_date='2023-05-31', book_deferred_entries_based_on='Months')
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
item = create_item('_Test Item for Deferred Accounting')
item.enable_deferred_revenue = 1
item.deferred_revenue_account = deferred_account
item.no_of_months = 12
item.save()
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
si.items[0].enable_deferred_revenue = 1
si.items[0].service_start_date = '2023-05-01'
si.items[0].service_end_date = '2023-07-31'
si.items[0].deferred_revenue_account = deferred_account
si.save()
si.submit()
original_gle = [['Debtors - _TC', 3000.0, 0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01']]
check_gl_entries(self, si.name, original_gle, '2023-07-01')
process_deferred_accounting = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2023-07-01', start_date='2023-05-01', end_date='2023-06-30', type='Income')
process_deferred_accounting.insert()
process_deferred_accounting.submit()
expected_gle = [['Debtors - _TC', 3000, 0.0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30']]
check_gl_entries(self, si.name, expected_gle, '2023-07-01')
process_deferred_accounting.cancel()
check_gl_entries(self, si.name, original_gle, '2023-07-01')
change_acc_settings()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:16*

### test_creation_of_ledger_entry_on_submit

**Category**: workflow  
**Description**: Workflow: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'test creation of gl entries on submission of document'
change_acc_settings(acc_frozen_till_date='2023-05-31', book_deferred_entries_based_on='Months')
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
item = create_item('_Test Item for Deferred Accounting')
item.enable_deferred_revenue = 1
item.deferred_revenue_account = deferred_account
item.no_of_months = 12
item.save()
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
si.items[0].enable_deferred_revenue = 1
si.items[0].service_start_date = '2023-05-01'
si.items[0].service_end_date = '2023-07-31'
si.items[0].deferred_revenue_account = deferred_account
si.save()
si.submit()
original_gle = [['Debtors - _TC', 3000.0, 0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01']]
check_gl_entries(self, si.name, original_gle, '2023-07-01')
process_deferred_accounting = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2023-07-01', start_date='2023-05-01', end_date='2023-06-30', type='Income')
process_deferred_accounting.insert()
process_deferred_accounting.submit()
expected_gle = [['Debtors - _TC', 3000, 0.0, '2023-07-01'], [deferred_account, 0.0, 3000, '2023-07-01'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30'], ['Sales - _TC', 0.0, 1000, '2023-06-30'], [deferred_account, 1000, 0.0, '2023-06-30']]
check_gl_entries(self, si.name, expected_gle, '2023-07-01')
process_deferred_accounting.cancel()
check_gl_entries(self, si.name, original_gle, '2023-07-01')
change_acc_settings()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:16*

### test_consolidated_invoice_creation

**Category**: workflow  
**Description**: Workflow: test consolidated invoice creation  
**Expected**: self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
pos_inv.save()
pos_inv.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_inv3 = create_pos_invoice(customer='_Test Customer 2', rate=2300, do_not_submit=1)
pos_inv3.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 2300})
pos_inv3.save()
pos_inv3.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
pos_inv.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv.consolidated_invoice))
pos_inv3.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv3.consolidated_invoice))
self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:41*

### test_consolidated_invoice_item_taxes

**Category**: workflow  
**Description**: Workflow: test consolidated invoice item taxes  
**Expected**: self.assertEqual(actual, expected_item_wise_tax_details)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 9})
inv.insert()
inv.payments[0].amount = inv.grand_total
inv.save()
inv.submit()
inv2 = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv2.get('items')[0].item_code = '_Test Item 2'
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 5})
inv2.insert()
inv2.payments[0].amount = inv.grand_total
inv2.save()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
expected_item_wise_tax_details = [{'item_row': consolidated_invoice.items[0].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 9.0, 'amount': 9.0, 'taxable_amount': 100.0}, {'item_row': consolidated_invoice.items[1].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 5.0, 'amount': 5.0, 'taxable_amount': 100.0}]
actual = [{'item_row': d.item_row, 'tax_row': d.tax_row, 'rate': d.rate, 'amount': d.amount, 'taxable_amount': d.taxable_amount} for d in consolidated_invoice.get('item_wise_tax_details')]
self.assertEqual(actual, expected_item_wise_tax_details)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:119*

### test_consolidation_round_off_error_1

**Category**: workflow  
**Description**: Workflow: Test round off error in consolidated invoice creation if POS Invoice has inclusive tax  
**Expected**: self.assertEqual(consolidated_invoice.status, 'Paid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

'\n\t\tTest round off error in consolidated invoice creation if POS Invoice has inclusive tax\n\t\t'
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=3, rate=10000, do_not_save=True)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 7.5, 'included_in_print_rate': 1})
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 30000})
inv.insert()
inv.submit()
inv2 = create_pos_invoice(qty=3, rate=10000, do_not_save=True)
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 7.5, 'included_in_print_rate': 1})
inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 30000})
inv2.insert()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertEqual(consolidated_invoice.outstanding_amount, 0)
self.assertEqual(consolidated_invoice.status, 'Paid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:197*

### test_consolidation_round_off_error_2

**Category**: workflow  
**Description**: Workflow: Test the same case as above but with an Unpaid POS Invoice  
**Expected**: self.assertEqual(consolidated_invoice.status, 'Paid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

'\n\t\tTest the same case as above but with an Unpaid POS Invoice\n\t\t'
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=6, rate=10000, do_not_save=True)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 7.5, 'included_in_print_rate': 1})
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 60000})
inv.insert()
inv.submit()
inv2 = create_pos_invoice(qty=6, rate=10000, do_not_save=True)
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 7.5, 'included_in_print_rate': 1})
inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 60000})
inv2.insert()
inv2.submit()
inv3 = create_pos_invoice(qty=3, rate=600, do_not_save=True)
inv3.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 1800})
inv3.insert()
inv3.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertNotEqual(consolidated_invoice.outstanding_amount, 800)
self.assertEqual(consolidated_invoice.status, 'Paid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:255*

### test_consolidation_round_off_error_3

**Category**: workflow  
**Description**: Workflow: test consolidation round off error 3  
**Expected**: self.assertEqual(consolidated_invoice.rounding_adjustment, -0.002)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
item_rates = [69, 59, 29]
for _i in [1, 2]:
    inv = create_pos_invoice(is_return=1, do_not_save=1)
    inv.items = []
    for rate in item_rates:
        inv.append('items', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'qty': -1, 'rate': rate, 'income_account': 'Sales - _TC', 'expense_account': 'Cost of Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC'})
    inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 15, 'included_in_print_rate': 1})
    inv.payments = []
    inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': -157})
    inv.paid_amount = -157
    inv.save()
    inv.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertEqual(consolidated_invoice.status, 'Return')
self.assertEqual(consolidated_invoice.rounding_adjustment, -0.002)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:320*

### test_consolidation_rounding_adjustment

**Category**: workflow  
**Description**: Workflow: Test if the rounding adjustment is calculated correctly  
**Expected**: self.assertEqual(consolidated_invoice.rounding_adjustment, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

'\n\t\tTest if the rounding adjustment is calculated correctly\n\t\t'
make_stock_entry(to_warehouse='_Test Warehouse - _TC', item_code='_Test Item', rate=8000, qty=10)
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=1, rate=69.5, do_not_save=True)
inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 70})
inv.insert()
inv.submit()
inv2 = create_pos_invoice(qty=1, rate=59.5, do_not_save=True)
inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 60})
inv2.insert()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
self.assertEqual(consolidated_invoice.rounding_adjustment, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:374*

### test_serial_no_case_1

**Category**: workflow  
**Description**: Workflow: Create a POS Invoice with serial no
Create a Return Invoice with serial no
Create a POS Invoice with serial no again
Consolidate the invoices

The first POS Invoice should be consolidated with a separate single Merge Log
The second and third POS Invoice should be consolidated with a single Merge Log  
**Expected**: self.assertNotEqual(pos_inv.consolidated_invoice, pos_inv2.consolidated_invoice)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

'\n\t\tCreate a POS Invoice with serial no\n\t\tCreate a Return Invoice with serial no\n\t\tCreate a POS Invoice with serial no again\n\t\tConsolidate the invoices\n\n\t\tThe first POS Invoice should be consolidated with a separate single Merge Log\n\t\tThe second and third POS Invoice should be consolidated with a single Merge Log\n\t\t'
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
se = make_serialized_item(self)
serial_no = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
pos_inv.save()
pos_inv.submit()
pos_inv_cn = make_sales_return(pos_inv.name)
pos_inv_cn.paid_amount = -100
pos_inv_cn.submit()
pos_inv2 = create_pos_invoice(item_code='_Test Serialized Item With Series', serial_no=[serial_no], qty=1, rate=100, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 100})
pos_inv2.save()
pos_inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
pos_inv.load_from_db()
pos_inv2.load_from_db()
self.assertNotEqual(pos_inv.consolidated_invoice, pos_inv2.consolidated_invoice)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:406*

### test_company_in_pos_invoice_merge_log

**Category**: workflow  
**Description**: Workflow: Test if the company is fetched from POS Closing Entry  
**Expected**: self.assertEqual(pos_merge_log_company, closing_entry.company)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.sql('delete from `tabPOS Invoice`')

'\n\t\tTest if the company is fetched from POS Closing Entry\n\t\t'
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
pos_inv.save()
pos_inv.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
self.assertTrue(frappe.db.exists('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}))
pos_merge_log_company = frappe.db.get_value('POS Invoice Merge Log', {'pos_closing_entry': closing_entry.name}, 'company')
self.assertEqual(pos_merge_log_company, closing_entry.company)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:510*

### test_consolidated_invoice_creation

**Category**: workflow  
**Description**: Workflow: test consolidated invoice creation  
**Expected**: self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
pos_inv = create_pos_invoice(rate=300, do_not_submit=1)
pos_inv.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 300})
pos_inv.save()
pos_inv.submit()
pos_inv2 = create_pos_invoice(rate=3200, do_not_submit=1)
pos_inv2.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 3200})
pos_inv2.save()
pos_inv2.submit()
pos_inv3 = create_pos_invoice(customer='_Test Customer 2', rate=2300, do_not_submit=1)
pos_inv3.append('payments', {'mode_of_payment': 'Cash', 'account': 'Cash - _TC', 'amount': 2300})
pos_inv3.save()
pos_inv3.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
pos_inv.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv.consolidated_invoice))
pos_inv3.load_from_db()
self.assertTrue(frappe.db.exists('Sales Invoice', pos_inv3.consolidated_invoice))
self.assertFalse(pos_inv.consolidated_invoice == pos_inv3.consolidated_invoice)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:41*

### test_consolidated_invoice_item_taxes

**Category**: workflow  
**Description**: Workflow: test consolidated invoice item taxes  
**Expected**: self.assertEqual(actual, expected_item_wise_tax_details)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_user, pos_profile = init_user_and_profile()
opening_entry = create_opening_entry(pos_profile, test_user.name)
inv = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 9})
inv.insert()
inv.payments[0].amount = inv.grand_total
inv.save()
inv.submit()
inv2 = create_pos_invoice(qty=1, rate=100, do_not_save=True)
inv2.get('items')[0].item_code = '_Test Item 2'
inv2.append('taxes', {'account_head': '_Test Account VAT - _TC', 'charge_type': 'On Net Total', 'cost_center': '_Test Cost Center - _TC', 'description': 'VAT', 'doctype': 'Sales Taxes and Charges', 'rate': 5})
inv2.insert()
inv2.payments[0].amount = inv.grand_total
inv2.save()
inv2.submit()
closing_entry = make_closing_entry_from_opening(opening_entry)
closing_entry.insert()
closing_entry.submit()
inv.load_from_db()
consolidated_invoice = frappe.get_doc('Sales Invoice', inv.consolidated_invoice)
expected_item_wise_tax_details = [{'item_row': consolidated_invoice.items[0].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 9.0, 'amount': 9.0, 'taxable_amount': 100.0}, {'item_row': consolidated_invoice.items[1].name, 'tax_row': consolidated_invoice.taxes[0].name, 'rate': 5.0, 'amount': 5.0, 'taxable_amount': 100.0}]
actual = [{'item_row': d.item_row, 'tax_row': d.tax_row, 'rate': d.rate, 'amount': d.amount, 'taxable_amount': d.taxable_amount} for d in consolidated_invoice.get('item_wise_tax_details')]
self.assertEqual(actual, expected_item_wise_tax_details)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_invoice_merge_log/test_pos_invoice_merge_log.py:119*

### test_invoice_without_only_delivery_note

**Category**: workflow  
**Description**: Workflow: Test buying amount for Invoice without `update_stock` flag set but has Delivery Note  
**Expected**: self.assertEqual(report_output, expected_entry_with_dn)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:157*

### test_bundled_delivery_note_with_different_warehouses

**Category**: workflow  
**Description**: Workflow: Test Delivery Note with bundled item. Packed Item from the bundle having different warehouses  
**Expected**: self.assertGreater(len(data), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:262*

### test_order_connected_dn_and_inv

**Category**: workflow  
**Description**: Workflow: test order connected dn and inv  
**Expected**: self.assertEqual(report_output, expected_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:314*

### test_crnote_against_invoice_with_multiple_instances_of_same_item

**Category**: workflow  
**Description**: Workflow: Item Qty for Sales Invoices with multiple instances of same item go in the -ve. Ideally, the credit noteshould cancel out the invoice items.  
**Expected**: self.assertEqual(report_output, expected_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

'\n\t\tItem Qty for Sales Invoices with multiple instances of same item go in the -ve. Ideally, the credit noteshould cancel out the invoice items.\n\t\t'
sinv = self.create_sales_invoice(qty=1, rate=100, posting_date=nowdate(), do_not_submit=True)
sinv.append('items', frappe.copy_doc(sinv.items[0], ignore_no_copy=False))
sinv = sinv.save().submit()
cr_note = make_sales_return(sinv.name)
cr_note = cr_note.save().submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice')
columns, data = execute(filters=filters)
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': 0.0, 'avg._selling_rate': 100, 'valuation_rate': 0.0, 'selling_amount': 0.0, 'buying_amount': 0.0, 'gross_profit': 0.0, 'gross_profit_%': 0.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
self.assertEqual(len(gp_entry), 2)
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
report_output = {k: v for k, v in gp_entry[1].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:394*

### test_standalone_cr_notes

**Category**: workflow  
**Description**: Workflow: Standalone cr notes will be reported as usual  
**Expected**: self.assertEqual(report_output, expected_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

'\n\t\tStandalone cr notes will be reported as usual\n\t\t'
sinv = self.create_sales_invoice(qty=-1, rate=100, posting_date=nowdate(), do_not_save=True, do_not_submit=True)
sinv.is_return = 1
sinv = sinv.save().submit()
filters = frappe._dict(company=self.company, from_date=nowdate(), to_date=nowdate(), group_by='Invoice', include_returned_invoices=1)
columns, data = execute(filters=filters)
expected_entry = {'parent_invoice': sinv.name, 'currency': 'INR', 'sales_invoice': self.item, 'customer': self.customer, 'posting_date': frappe.utils.datetime.date.fromisoformat(nowdate()), 'item_code': self.item, 'item_name': self.item, 'warehouse': 'Stores - _GP', 'qty': -1.0, 'avg._selling_rate': 100.0, 'valuation_rate': 0.0, 'selling_amount': -100.0, 'buying_amount': 0.0, 'gross_profit': -100.0, 'gross_profit_%': 100.0}
gp_entry = [x for x in data if x.parent_invoice == sinv.name]
report_output = {k: v for k, v in gp_entry[0].items() if k in expected_entry}
self.assertEqual(report_output, expected_entry)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:438*

### test_different_rates_in_si_and_dn

**Category**: workflow  
**Description**: Workflow: test different rates in si and dn  
**Expected**: self.assertEqual(report_output, expected_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:479*

### test_profit_for_later_period_return

**Category**: workflow  
**Description**: Workflow: test profit for later period return  
**Expected**: self.assertEqual(total.get('gross_profit_%'), 0.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_item()
self.create_bundle()
self.create_customer()
self.create_sales_invoice()
self.clear_old_entries()

month_start_date, month_end_date = (get_first_day(nowdate()), get_last_day(nowdate()))
sinv = self.create_sales_invoice(qty=1, rate=100, do_not_save=True, do_not_submit=True)
sinv.set_posting_time = 1
sinv.posting_date = month_start_date
sinv.save().submit()
cr_note = make_sales_return(sinv.name)
cr_note.set_posting_time = 1
cr_note.posting_date = add_days(month_end_date, 1)
cr_note.save().submit()
filters = frappe._dict(company=self.company, from_date=month_start_date, to_date=month_end_date, group_by='Invoice')
_, data = execute(filters=filters)
total = data[-1]
self.assertEqual(total.selling_amount, 100.0)
self.assertEqual(total.buying_amount, 0.0)
self.assertEqual(total.gross_profit, 100.0)
self.assertEqual(total.get('gross_profit_%'), 100.0)
filters.update(to_date=add_days(month_end_date, 1))
_, data = execute(filters=filters)
total = data[-1]
self.assertEqual(total.selling_amount, 0.0)
self.assertEqual(total.buying_amount, 0.0)
self.assertEqual(total.gross_profit, 0.0)
self.assertEqual(total.get('gross_profit_%'), 0.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:649*

### test_invoice_without_only_delivery_note

**Category**: workflow  
**Description**: Workflow: Test buying amount for Invoice without `update_stock` flag set but has Delivery Note  
**Expected**: self.assertEqual(report_output, expected_entry_with_dn)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:157*

### test_bundled_delivery_note_with_different_warehouses

**Category**: workflow  
**Description**: Workflow: Test Delivery Note with bundled item. Packed Item from the bundle having different warehouses  
**Expected**: self.assertGreater(len(data), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:262*

### test_order_connected_dn_and_inv

**Category**: workflow  
**Description**: Workflow: test order connected dn and inv  
**Expected**: self.assertEqual(report_output, expected_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
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

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/gross_profit/test_gross_profit.py:314*

### test_company_fiscal_year_overlap

**Category**: workflow  
**Description**: Workflow: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for name in ['_Test Global FY 2001', '_Test Company FY 2001']:
    if frappe.db.exists('Fiscal Year', name):
        frappe.delete_doc('Fiscal Year', name)
global_fy = frappe.new_doc('Fiscal Year')
global_fy.year = '_Test Global FY 2001'
global_fy.year_start_date = '2001-04-01'
global_fy.year_end_date = '2002-03-31'
global_fy.insert()
company_fy = frappe.new_doc('Fiscal Year')
company_fy.year = '_Test Company FY 2001'
company_fy.year_start_date = '2001-01-01'
company_fy.year_end_date = '2001-12-31'
company_fy.append('companies', {'company': '_Test Company'})
company_fy.insert()
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:27*

### test_record_generator

**Category**: workflow  
**Description**: Workflow: test record generator  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
test_records = [{'doctype': 'Fiscal Year', 'year': '_Test Short Fiscal Year 2011', 'is_short_year': 1, 'year_start_date': '2011-04-01', 'year_end_date': '2011-12-31'}]
start = 2012
this_year = now_datetime().year
end = now_datetime().year + 25
for year in range(start, this_year):
    test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
for year in range(this_year + 1, end):
    test_records.append({'doctype': 'Fiscal Year', 'year': f'_Test Fiscal Year {year}', 'year_start_date': f'{year}-01-01', 'year_end_date': f'{year}-12-31'})
return test_records
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:49*

### test_company_fiscal_year_overlap

**Category**: workflow  
**Description**: Workflow: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for name in ['_Test Global FY 2001', '_Test Company FY 2001']:
    if frappe.db.exists('Fiscal Year', name):
        frappe.delete_doc('Fiscal Year', name)
global_fy = frappe.new_doc('Fiscal Year')
global_fy.year = '_Test Global FY 2001'
global_fy.year_start_date = '2001-04-01'
global_fy.year_end_date = '2002-03-31'
global_fy.insert()
company_fy = frappe.new_doc('Fiscal Year')
company_fy.year = '_Test Company FY 2001'
company_fy.year_start_date = '2001-01-01'
company_fy.year_end_date = '2001-12-31'
company_fy.append('companies', {'company': '_Test Company'})
company_fy.insert()
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:27*

### test_cumulative_threshold_tds

**Category**: workflow  
**Description**: Workflow: Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold  
**Expected**: self.validate_tax_withholding_entries('Purchase Invoice', pi4.name, expected_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Tax withholding entries for cumulative threshold TDS with Tax on excess without single threshold'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
invoices = []
pi1 = create_purchase_invoice(supplier='Test TDS Supplier')
pi1.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
pi2 = create_purchase_invoice(supplier='Test TDS Supplier')
pi2.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Under Withheld', withholding_doctype=None, withholding_name=None, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi2.name, expected_entries)
pi3 = create_purchase_invoice(supplier='Test TDS Supplier')
pi3.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi2.name, withholding_amount=1000.0, tax_rate=10.0, taxable_amount=10000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi3.name, tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi3.name, under_withheld_reason=None)]
self.validate_tax_deduction(pi3, 3000)
self.validate_tax_withholding_entries('Purchase Invoice', pi3.name, expected_entries)
invoices.append(pi3)
pi4 = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
pi4.submit()
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', taxable_doctype='Purchase Invoice', taxable_name=pi4.name, tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', withholding_doctype='Purchase Invoice', withholding_name=pi4.name, under_withheld_reason=None)]
self.validate_tax_deduction(pi4, 500)
self.validate_tax_withholding_entries('Purchase Invoice', pi4.name, expected_entries)
invoices.append(pi4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:132*

### test_cumulative_threshold_tds_with_account_change

**Category**: workflow  
**Description**: Workflow: Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year  
**Expected**: self.assertEqual(pi.taxes_and_charges_deducted, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Cumulative threshold TDS without tax_on_excess, with account change in the middle of the year'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Multi Account TDS Category')
invoices = []
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier')
    pi.submit()
    invoices.append(pi)
pi = create_purchase_invoice(supplier='Test TDS Supplier')
pi.submit()
self.assertEqual(pi.taxes_and_charges_deducted, 3000)
self.assertEqual(pi.grand_total, 7000)
invoices.append(pi)
frappe.db.set_value('Tax Withholding Account', {'parent': 'Multi Account TDS Category'}, 'account', '_Test Account VAT - _TC')
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=5000)
pi.submit()
self.assertEqual(pi.taxes_and_charges_deducted, 500)
invoices.append(pi)
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:261*

### test_single_threshold_tds

**Category**: workflow  
**Description**: Workflow: test single threshold tds  
**Expected**: self.assertEqual(pi.taxes_and_charges_deducted, 1000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
invoices = []
frappe.db.set_value('Supplier', 'Test TDS Supplier1', 'tax_withholding_category', 'Single Threshold TDS')
pi = create_purchase_invoice(supplier='Test TDS Supplier1', rate=20000)
pi.submit()
invoices.append(pi)
self.assertEqual(pi.taxes_and_charges_deducted, 2000)
self.assertEqual(pi.grand_total, 18000)
gl_entries = frappe.db.get_all('GL Entry', filters={'voucher_no': pi.name}, fields=['account', {'SUM': 'debit', 'as': 'debit'}, {'SUM': 'credit', 'as': 'credit'}], group_by='account')
self.assertEqual(len(gl_entries), 3)
for d in gl_entries:
    if d.account == pi.credit_to:
        self.assertEqual(d.credit, 20000)
        self.assertEqual(d.debit, 2000)
    elif d.account == pi.items[0].get('expense_account'):
        self.assertEqual(d.debit, 20000)
    elif d.account == pi.taxes[0].get('account_head'):
        self.assertEqual(d.credit, 2000)
    else:
        raise ValueError('Account head does not match.')
pi = create_purchase_invoice(supplier='Test TDS Supplier1')
pi.submit()
invoices.append(pi)
self.assertEqual(pi.taxes_and_charges_deducted, 1000)
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:301*

### test_tax_withholding_category_checks

**Category**: workflow  
**Description**: Workflow: test tax withholding category checks  
**Expected**: self.assertEqual(pi1.taxes, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000, do_not_save=True)
pi.apply_tds = 0
pi.save()
pi.submit()
invoices.append(pi)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
pi1.submit()
invoices.append(pi1)
self.assertEqual(pi1.taxes, [])
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:341*

### test_cumulative_threshold_with_party_ledger_amount_on_net_total

**Category**: workflow  
**Description**: Workflow: test cumulative threshold with party ledger amount on net total  
**Expected**: self.assertEqual(pi1.taxes[0].tax_amount, 800)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'Advance TDS Category')
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=1000, do_not_save=True)
    pi.apply_tds = 1
    pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test', 'add_deduct_tax': 'Add'})
    pi.save()
    pi.submit()
    invoices.append(pi)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=6000)
pi1.apply_tds = 1
pi1.save()
pi1.submit()
invoices.append(pi1)
self.assertEqual(pi1.taxes[0].tax_amount, 800)
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:364*

### test_cumulative_threshold_with_tax_on_excess_amount

**Category**: workflow  
**Description**: Workflow: test cumulative threshold with tax on excess amount  
**Expected**: self.assertEqual(pi1.taxes[0].tax_amount, 1000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
invoices = []
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
for _ in range(2):
    pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=10000, do_not_save=True)
    pi.apply_tds = 1
    pi.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'Test'})
    pi.save()
    pi.submit()
    invoices.append(pi)
    expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name, under_withheld_reason='Threshold Exemption')]
    self.validate_tax_withholding_entries('Purchase Invoice', pi.name, expected_entries)
pi1 = create_purchase_invoice(supplier='Test TDS Supplier3', rate=20000)
pi1.apply_tds = 1
pi1.save()
pi1.submit()
invoices.append(pi1)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=10000.0, withholding_amount=1000.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi1.name, withholding_doctype='Purchase Invoice', withholding_name=pi1.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Purchase Invoice', pi1.name, expected_entries)
self.assertTrue(len(pi1.taxes) > 0)
self.assertEqual(pi1.taxes[0].tax_amount, 1000)
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:401*

### test_cumulative_threshold_tcs_on_gross_amount

**Category**: workflow  
**Description**: Workflow: test cumulative threshold tcs on gross amount  
**Expected**: self.assertEqual(si.grand_total, 6050)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.setup_party_with_category('Customer', 'Test TCS Customer', 'Cumulative Threshold TCS')
invoices = []
for _ in range(2):
    si = create_sales_invoice(customer='Test TCS Customer')
    si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 200, 'description': 'Test Gross Tax'})
    si.save()
    si.submit()
    invoices.append(si)
    expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=10200.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption')]
    self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
si = create_sales_invoice(customer='Test TCS Customer', rate=12000)
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': 'TCS - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 400, 'description': 'Test Gross Tax'})
si.save()
si.reload()
si.submit()
invoices.append(si)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=9600.0, withholding_amount=0.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=2800.0, withholding_amount=280.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
self.validate_tax_deduction(si, 280)
self.assertEqual(si.grand_total, 12680)
si = create_sales_invoice(customer='Test TCS Customer', rate=5000)
si.append('taxes', {'category': 'Total', 'charge_type': 'Actual', 'account_head': '_Test Account VAT - _TC', 'cost_center': 'Main - _TC', 'tax_amount': 500, 'description': 'VAT added to test TDS calculation on gross amount'})
si.save()
si.submit()
invoices.append(si)
expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=5500.0, withholding_amount=550.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason=None)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, expected_entries)
self.validate_tax_deduction(si, 550)
self.assertEqual(si.grand_total, 6050)
self.cleanup_invoices(invoices)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:492*

### test_tcs_on_allocated_advance_payments

**Category**: workflow  
**Description**: Workflow: test tcs on allocated advance payments  
**Expected**: self.validate_tax_withholding_entries('Sales Invoice', si.name, invoice_expected_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.setup_party_with_category('Customer', 'Test TCS Customer', 'Cumulative Threshold TCS')
vouchers = []
pe = create_payment_entry(payment_type='Receive', party_type='Customer', party='Test TCS Customer', paid_amount=30000)
pe.paid_from = 'Debtors - _TC'
pe.paid_to = 'Cash - _TC'
pe.apply_tds = 1
pe.tax_withholding_category = 'Cumulative Threshold TCS'
pe.submit()
vouchers.append(pe)
payment_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000.0, withholding_amount=3000.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe.name)]
self.validate_tax_withholding_entries('Payment Entry', pe.name, payment_expected_entries)
si = create_sales_invoice(customer='Test TCS Customer', rate=50000)
advances = si.get_advance_entries()
si.append('advances', {'reference_type': advances[0].reference_type, 'reference_name': advances[0].reference_name, 'advance_amount': advances[0].amount, 'allocated_amount': 30000})
si.submit()
vouchers.append(si)
tcs_charged = sum([d.base_tax_amount for d in si.taxes if d.account_head == 'TCS - _TC'])
self.assertEqual(tcs_charged, 0)
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=30000, withholding_amount=0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Sales Invoice', withholding_name=si.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TCS', party_type='Customer', party='Test TCS Customer', tax_rate=10.0, taxable_amount=20000.0, withholding_amount=2000.0, status='Settled', taxable_doctype='Sales Invoice', taxable_name=si.name, withholding_doctype='Payment Entry', withholding_name=pe.name)]
self.validate_tax_withholding_entries('Sales Invoice', si.name, invoice_expected_entries)
self.cleanup_invoices(vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:623*

### test_tds_multiple_payments_adjust_only_linked

**Category**: workflow  
**Description**: Workflow: Test that when multiple advance payment entries exist for the same supplier,
only the payment entry that is linked/allocated to the invoice is adjusted.  
**Expected**: self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest that when multiple advance payment entries exist for the same supplier,\n\t\tonly the payment entry that is linked/allocated to the invoice is adjusted.\n\t\t'
self.setup_party_with_category('Supplier', 'Test TDS Supplier', 'Cumulative Threshold TDS')
vouchers = []
pe1 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=5000)
pe1.apply_tds = 1
pe1.tax_withholding_category = 'Cumulative Threshold TDS'
pe1.save()
pe1.submit()
vouchers.append(pe1)
pe1_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Payment Entry', pe1.name, pe1_expected_entries)
pe2 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier', paid_amount=3000)
pe2.apply_tds = 1
pe2.tax_withholding_category = 'Cumulative Threshold TDS'
pe2.save()
pe2.submit()
vouchers.append(pe2)
pe2_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=3000.0, withholding_amount=300.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe2.name)]
self.validate_tax_withholding_entries('Payment Entry', pe2.name, pe2_expected_entries)
pi = create_purchase_invoice(supplier='Test TDS Supplier', rate=40000)
pi.append('advances', {'reference_type': pe1.doctype, 'reference_name': pe1.name, 'advance_amount': 5000, 'allocated_amount': 5000})
pi.submit()
vouchers.append(pi)
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=35000.0, withholding_amount=3500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name), self.get_tax_withholding_entry(tax_withholding_category='Cumulative Threshold TDS', party_type='Supplier', party='Test TDS Supplier', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)
self.cleanup_invoices(vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:714*

### test_tds_multiple_payments_with_unused_threshold

**Category**: workflow  
**Description**: Workflow: Test multiple payment entries with unused threshold (tax_on_excess_amount enabled).
Only the linked payment entry should be adjusted, and threshold exemption should apply.  
**Expected**: self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest multiple payment entries with unused threshold (tax_on_excess_amount enabled).\n\t\tOnly the linked payment entry should be adjusted, and threshold exemption should apply.\n\t\t'
self.setup_party_with_category('Supplier', 'Test TDS Supplier3', 'New TDS Category')
vouchers = []
pe1 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier3', paid_amount=5000)
pe1.apply_tds = 1
pe1.tax_withholding_category = 'New TDS Category'
pe1.save()
pe1.submit()
vouchers.append(pe1)
pe1_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Payment Entry', pe1.name, pe1_expected_entries)
pe2 = create_payment_entry(payment_type='Pay', party_type='Supplier', party='Test TDS Supplier3', paid_amount=3000)
pe2.apply_tds = 1
pe2.tax_withholding_category = 'New TDS Category'
pe2.save()
pe2.submit()
vouchers.append(pe2)
pe2_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=3000.0, withholding_amount=300.0, status='Over Withheld', taxable_doctype='', taxable_name='', withholding_doctype='Payment Entry', withholding_name=pe2.name)]
self.validate_tax_withholding_entries('Payment Entry', pe2.name, pe2_expected_entries)
pi = create_purchase_invoice(supplier='Test TDS Supplier3', rate=40000)
pi.append('advances', {'reference_type': pe1.doctype, 'reference_name': pe1.name, 'advance_amount': 5000, 'allocated_amount': 5000})
pi.submit()
vouchers.append(pi)
invoice_expected_entries = [self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=30000.0, withholding_amount=0.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name, under_withheld_reason='Threshold Exemption'), self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Purchase Invoice', withholding_name=pi.name), self.get_tax_withholding_entry(tax_withholding_category='New TDS Category', party_type='Supplier', party='Test TDS Supplier3', tax_rate=10.0, taxable_amount=5000.0, withholding_amount=500.0, status='Settled', taxable_doctype='Purchase Invoice', taxable_name=pi.name, withholding_doctype='Payment Entry', withholding_name=pe1.name)]
self.validate_tax_withholding_entries('Purchase Invoice', pi.name, invoice_expected_entries)
self.cleanup_invoices(vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_withholding_category/test_tax_withholding_category.py:819*

### test_reconcile

**Category**: workflow  
**Description**: Workflow: test reconcile  
**Expected**: self.assertFalse(clearance_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000003025 OPSKATTUZWXXX AT776000000098709849 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1700))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
unallocated_amount = frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount')
self.assertTrue(unallocated_amount == 0)
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertTrue(clearance_date is not None)
bank_transaction.reload()
bank_transaction.cancel()
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertFalse(clearance_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:56*

### test_already_reconciled

**Category**: workflow  
**Description**: Workflow: test already reconciled  
**Expected**: self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:125*

### test_matching_loan_repayment

**Category**: workflow  
**Description**: Workflow: test matching loan repayment  
**Expected**: self.assertEqual(linked_payments[0]['name'], repayment_entry.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

from lending.loan_management.doctype.loan.test_loan import create_loan_accounts
create_loan_accounts()
bank_account = frappe.get_doc({'doctype': 'Bank Account', 'account_name': 'Payment Account', 'bank': 'Citi Bank', 'account': 'Payment Account - _TC'}).insert(ignore_if_duplicate=True)
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'description': 'Loan Repayment - OPSKATTUZWXXX AT776000000098709837 Herr G', 'date': '2018-10-27', 'deposit': 500, 'currency': 'INR', 'bank_account': bank_account.name}).submit()
repayment_entry = create_loan_and_repayment()
linked_payments = get_linked_payments(bank_transaction.name, ['loan_repayment', 'exact_match'])
self.assertEqual(linked_payments[0]['name'], repayment_entry.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:190*

### test_reconcile

**Category**: workflow  
**Description**: Workflow: test reconcile  
**Expected**: self.assertFalse(clearance_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000003025 OPSKATTUZWXXX AT776000000098709849 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1700))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
unallocated_amount = frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount')
self.assertTrue(unallocated_amount == 0)
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertTrue(clearance_date is not None)
bank_transaction.reload()
bank_transaction.cancel()
clearance_date = frappe.db.get_value('Payment Entry', payment.name, 'clearance_date')
self.assertFalse(clearance_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:56*

### test_already_reconciled

**Category**: workflow  
**Description**: Workflow: test already reconciled  
**Expected**: self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
reconcile_vouchers(bank_transaction.name, vouchers)
bank_transaction = frappe.get_doc('Bank Transaction', dict(description='1512567 BG/000002918 OPSKATTUZWXXX AT776000000098709837 Herr G'))
payment = frappe.get_doc('Payment Entry', dict(party='Mr G', paid_amount=1200))
vouchers = json.dumps([{'payment_doctype': 'Payment Entry', 'payment_name': payment.name, 'amount': bank_transaction.unallocated_amount}])
self.assertRaises(frappe.ValidationError, reconcile_vouchers, bank_transaction_name=bank_transaction.name, vouchers=vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:125*

### test_matching_loan_repayment

**Category**: workflow  
**Description**: Workflow: test matching loan repayment  
**Expected**: self.assertEqual(linked_payments[0]['name'], repayment_entry.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from lending.loan_management.doctype.loan.test_loan import create_loan_accounts
create_loan_accounts()
bank_account = frappe.get_doc({'doctype': 'Bank Account', 'account_name': 'Payment Account', 'bank': 'Citi Bank', 'account': 'Payment Account - _TC'}).insert(ignore_if_duplicate=True)
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'description': 'Loan Repayment - OPSKATTUZWXXX AT776000000098709837 Herr G', 'date': '2018-10-27', 'deposit': 500, 'currency': 'INR', 'bank_account': bank_account.name}).submit()
repayment_entry = create_loan_and_repayment()
linked_payments = get_linked_payments(bank_transaction.name, ['loan_repayment', 'exact_match'])
self.assertEqual(linked_payments[0]['name'], repayment_entry.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:190*

### test_subscription_unpaid_after_grace_period

**Category**: workflow  
**Description**: Workflow: test subscription unpaid after grace period  
**Expected**: self.assertEqual(subscription.status, 'Unpaid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
default_grace_period_action = settings.cancel_after_grace
settings.cancel_after_grace = 0
settings.save()
subscription = create_subscription(start_date='2018-01-01')
subscription.process(posting_date='2018-01-31')
self.assertEqual(subscription.status, 'Unpaid')
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:115*

### test_subscription_is_past_due_doesnt_change_within_grace_period

**Category**: workflow  
**Description**: Workflow: test subscription is past due doesnt change within grace period  
**Expected**: self.assertEqual(subscription.status, 'Grace Period')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
grace_period = settings.grace_period
settings.grace_period = 1000
settings.save()
subscription = create_subscription(start_date=add_days(nowdate(), -1000))
subscription.process(posting_date=subscription.current_invoice_end)
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
subscription.process()
self.assertEqual(subscription.status, 'Grace Period')
settings.grace_period = grace_period
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:138*

### test_subscription_cancellation_invoices

**Category**: workflow  
**Description**: Workflow: test subscription cancellation invoices  
**Expected**: self.assertEqual(subscription.status, 'Cancelled')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
to_prorate = settings.prorate
settings.prorate = 1
settings.save()
subscription = create_subscription()
self.assertEqual(subscription.status, 'Active')
subscription.cancel_subscription()
self.assertEqual(len(subscription.invoices), 1)
invoice = subscription.get_current_invoice()
diff = flt(date_diff(nowdate(), subscription.current_invoice_start) + 1)
plan_days = flt(date_diff(subscription.current_invoice_end, subscription.current_invoice_start) + 1)
prorate_factor = flt(diff / plan_days)
self.assertEqual(flt(get_prorata_factor(subscription.current_invoice_end, subscription.current_invoice_start, cint(subscription.generate_invoice_at == 'Beginning of the current subscription period')), 2), flt(prorate_factor, 2))
self.assertEqual(flt(invoice.grand_total, 2), flt(prorate_factor * 900, 2))
self.assertEqual(subscription.status, 'Cancelled')
settings.prorate = to_prorate
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:188*

### test_subscription_cancellation_invoices_with_prorata_false

**Category**: workflow  
**Description**: Workflow: test subscription cancellation invoices with prorata false  
**Expected**: self.assertEqual(invoice.grand_total, 900)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
to_prorate = settings.prorate
settings.prorate = 0
settings.save()
subscription = create_subscription()
subscription.cancel_subscription()
invoice = subscription.get_current_invoice()
self.assertEqual(invoice.grand_total, 900)
settings.prorate = to_prorate
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:224*

### test_subscription_cancellation_invoices_with_prorata_true

**Category**: workflow  
**Description**: Workflow: test subscription cancellation invoices with prorata true  
**Expected**: self.assertEqual(flt(invoice.grand_total, 2), flt(prorate_factor * 900, 2))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
to_prorate = settings.prorate
settings.prorate = 1
settings.save()
subscription = create_subscription()
subscription.cancel_subscription()
invoice = subscription.get_current_invoice()
diff = flt(date_diff(nowdate(), subscription.current_invoice_start) + 1)
plan_days = flt(date_diff(subscription.current_invoice_end, subscription.current_invoice_start) + 1)
prorate_factor = flt(diff / plan_days)
self.assertEqual(flt(invoice.grand_total, 2), flt(prorate_factor * 900, 2))
settings.prorate = to_prorate
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:239*

### test_subscription_cancellation_and_process

**Category**: workflow  
**Description**: Workflow: test subscription cancellation and process  
**Expected**: self.assertEqual(len(subscription.invoices), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
default_grace_period_action = settings.cancel_after_grace
settings.cancel_after_grace = 1
settings.save()
subscription = create_subscription(start_date='2018-01-01')
subscription.process()
subscription.cancel_subscription()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Cancelled')
self.assertEqual(len(subscription.invoices), 1)
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:258*

### test_subscription_restart_and_process

**Category**: workflow  
**Description**: Workflow: test subscription restart and process  
**Expected**: self.assertEqual(len(subscription.invoices), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
default_grace_period_action = settings.cancel_after_grace
settings.grace_period = 0
settings.cancel_after_grace = 0
settings.save()
subscription = create_subscription(start_date='2018-01-01')
subscription.process(posting_date='2018-01-31')
self.assertEqual(subscription.status, 'Unpaid')
subscription.cancel_subscription()
self.assertEqual(subscription.status, 'Cancelled')
subscription.restart_subscription()
self.assertEqual(subscription.status, 'Active')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Unpaid')
self.assertEqual(len(subscription.invoices), 1)
subscription.process()
self.assertEqual(subscription.status, 'Unpaid')
self.assertEqual(len(subscription.invoices), 1)
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:283*

### test_subscription_unpaid_back_to_active

**Category**: workflow  
**Description**: Workflow: test subscription unpaid back to active  
**Expected**: self.assertEqual(subscription.status, 'Unpaid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
default_grace_period_action = settings.cancel_after_grace
settings.cancel_after_grace = 0
settings.save()
subscription = create_subscription(start_date='2018-01-01', generate_invoice_at='Beginning of the current subscription period')
subscription.process(subscription.current_invoice_start)
self.assertEqual(subscription.status, 'Unpaid')
invoice = subscription.get_current_invoice()
invoice.db_set('outstanding_amount', 0)
invoice.db_set('status', 'Paid')
subscription.process()
self.assertEqual(subscription.status, 'Active')
subscription.process(posting_date=subscription.current_invoice_start)
self.assertEqual(subscription.status, 'Unpaid')
settings.cancel_after_grace = default_grace_period_action
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:314*

### test_prepaid_subscriptions_with_prorate_true

**Category**: workflow  
**Description**: Workflow: test prepaid subscriptions with prorate true  
**Expected**: self.assertEqual(flt(current_inv.grand_total, 2), flt(prorate_factor * 900, 2))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

settings = frappe.get_single('Subscription Settings')
to_prorate = settings.prorate
settings.prorate = 1
settings.save()
subscription = create_subscription(generate_invoice_at='Beginning of the current subscription period')
subscription.process()
subscription.cancel_subscription()
self.assertEqual(len(subscription.invoices), 1)
current_inv = subscription.get_current_invoice()
self.assertEqual(current_inv.status, 'Unpaid')
prorate_factor = 1
self.assertEqual(flt(current_inv.grand_total, 2), flt(prorate_factor * 900, 2))
settings.prorate = to_prorate
settings.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:378*

### test_subscription_with_follow_calendar_months

**Category**: workflow  
**Description**: Workflow: test subscription with follow calendar months  
**Expected**: self.assertEqual(get_date_str(subscription.current_invoice_end), '2018-03-31')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
make_plans()
create_parties()
reset_settings()
frappe.db.set_value('Company', '_Test Company', 'accounts_frozen_till_date', None)

subscription = frappe.new_doc('Subscription')
subscription.company = '_Test Company'
subscription.party_type = 'Supplier'
subscription.party = '_Test Supplier'
subscription.generate_invoice_at = 'Beginning of the current subscription period'
subscription.follow_calendar_months = 1
subscription.start_date = '2018-01-15'
subscription.end_date = '2018-07-15'
subscription.append('plans', {'plan': '_Test Plan Name 4', 'qty': 1})
subscription.save()
self.assertEqual(get_date_str(subscription.current_invoice_end), '2018-03-31')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/subscription/test_subscription.py:400*

### test_pos_receivable

**Category**: workflow  
**Description**: Workflow: test pos receivable  
**Expected**: self.assertEqual(expected_data[0], [row.invoiced, row.paid, row.credit_note])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'party_type': 'Customer', 'party': [self.customer], 'report_date': add_days(today(), 2), 'based_on_payment_terms': 0, 'range': '30, 60, 90, 120', 'show_remarks': False}
pos_inv = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
pos_inv.posting_date = add_days(today(), 2)
pos_inv.is_pos = 1
pos_inv.append('payments', frappe._dict(mode_of_payment='Cash', amount=flt(pos_inv.grand_total / 2)))
pos_inv.disable_rounded_total = 1
pos_inv.save()
pos_inv.submit()
report = execute(filters)
expected_data = [[pos_inv.grand_total, pos_inv.paid_amount, 0]]
row = report[1][-1]
self.assertEqual(expected_data[0], [row.invoiced, row.paid, row.credit_note])
pos_inv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:80*

### test_accounts_receivable_with_payment

**Category**: workflow  
**Description**: Workflow: test accounts receivable with payment  
**Expected**: self.assertEqual(expected_data_after_credit_note, [row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.party_account])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice()
report = execute(filters)
expected_data = [[100, 30, 'No Remarks'], [100, 50, 'No Remarks'], [100, 20, 'No Remarks']]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_payment_entry(si.name)
report = execute(filters)
expected_data_after_payment = [[100, 50, 10, 40], [100, 20, 0, 20]]
for i in range(2):
    row = report[1][i - 1]
    self.assertEqual(expected_data_after_payment[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = False
cr_note.save().submit()
self.assertEqual(cr_note.update_outstanding_for_self, True)
report = execute(filters)
expected_data_after_credit_note = [0, 0, 100, 0, -100, self.debit_to]
row = report[1][-1]
self.assertEqual(expected_data_after_credit_note, [row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.party_account])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:112*

### test_accounts_receivable_without_payment

**Category**: workflow  
**Description**: Workflow: test accounts receivable without payment  
**Expected**: self.assertTrue(len(row) == 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice()
report = execute(filters)
expected_data = [[100, 30, 'No Remarks'], [100, 50, 'No Remarks'], [100, 20, 'No Remarks']]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = False
cr_note.save().submit()
self.assertEqual(cr_note.update_outstanding_for_self, False)
report = execute(filters)
row = report[1]
self.assertTrue(len(row) == 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:170*

### test_allow_multi_currency_invoices_against_single_party_account

**Category**: workflow  
**Description**: Workflow: test allow multi currency invoices against single party account  
**Expected**: self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True, 'in_party_currency': 1}
si = self.create_sales_invoice(qty=1, no_payment_schedule=True, do_not_submit=True)
si.currency = 'USD'
si.conversion_rate = 80
si.save().submit()
filters.update({'party_type': 'Customer', 'party': [self.customer]})
report = execute(filters)
row = report[1][0]
expected_data = [8000, 8000, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_customer('USD Customer', currency='USD', default_account=self.debtors_usd, company=self.company)
si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debtors_usd, posting_date=today(), parent_cost_center=self.cost_center, cost_center=self.cost_center, rate=100, currency='USD', conversion_rate=80, price_list_rate=100, do_not_save=1)
si.save().submit()
filters.update({'party_type': 'Customer', 'party': [self.customer]})
report = execute(filters)
row = report[1][0]
expected_data = [100, 100, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
filters.pop('in_party_currency')
report = execute(filters)
row = report[1][0]
expected_data = [8000, 8000, 'No Remarks']
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:206*

### test_accounts_receivable_with_partial_payment

**Category**: workflow  
**Description**: Workflow: test accounts receivable with partial payment  
**Expected**: self.assertFalse(cr_note.update_outstanding_for_self)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'based_on_payment_terms': 1, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice(qty=2)
report = execute(filters)
expected_data = [[200, 60, 'No Remarks'], [200, 100, 'No Remarks'], [200, 40, 'No Remarks']]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data[i - 1], [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_payment_entry(si.name)
report = execute(filters)
expected_data_after_payment = [[200, 60, 40, 20], [200, 100, 0, 100], [200, 40, 0, 40]]
for i in range(3):
    row = report[1][i - 1]
    self.assertEqual(expected_data_after_payment[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = False
cr_note.save().submit()
self.assertFalse(cr_note.update_outstanding_for_self)
report = execute(filters)
expected_data_after_credit_note = [[200, 100, 0, 80, 20, self.debit_to], [200, 40, 0, 0, 40, self.debit_to]]
for i in range(2):
    row = report[1][i - 1]
    self.assertEqual(expected_data_after_credit_note[i - 1], [row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.party_account])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:277*

### test_cr_note_flag_to_update_self

**Category**: workflow  
**Description**: Workflow: test cr note flag to update self  
**Expected**: self.assertEqual(expected_data_after_credit_note[1], cr_note_row)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'show_remarks': True}
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
si.set_posting_time = True
si.posting_date = add_days(today(), -1)
si.save().submit()
report = execute(filters)
expected_data = [100, 100, 'No Remarks']
self.assertEqual(len(report[1]), 1)
row = report[1][0]
self.assertEqual(expected_data, [row.invoice_grand_total, row.invoiced, row.remarks])
self.create_payment_entry(si.name)
report = execute(filters)
expected_data_after_payment = [100, 100, 40, 60]
self.assertEqual(len(report[1]), 1)
row = report[1][0]
self.assertEqual(expected_data_after_payment, [row.invoice_grand_total, row.invoiced, row.paid, row.outstanding])
cr_note = self.create_credit_note(si.name, do_not_submit=True)
cr_note.update_outstanding_for_self = True
cr_note.save().submit()
report = execute(filters)
expected_data_after_credit_note = [[100.0, 100.0, 40.0, 0.0, 60.0, si.name], [0, 0, 100.0, 0.0, -100.0, cr_note.name]]
self.assertEqual(len(report[1]), 2)
si_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == si.name))
cr_note_row = next(([row.invoice_grand_total, row.invoiced, row.paid, row.credit_note, row.outstanding, row.voucher_no] for row in report[1] if row.voucher_no == cr_note.name))
self.assertEqual(expected_data_after_credit_note[0], si_row)
self.assertEqual(expected_data_after_credit_note[1], cr_note_row)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:338*

### test_payment_againt_po_in_receivable_report

**Category**: workflow  
**Description**: Workflow: Payments made against Purchase Order will show up as outstanding amount  
**Expected**: self.assertEqual(expected_data_after_payment, [row.invoiced, row.paid, row.credit_note, row.outstanding])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

'\n\t\tPayments made against Purchase Order will show up as outstanding amount\n\t\t'
so = make_sales_order(company=self.company, customer=self.customer, warehouse=self.warehouse, debit_to=self.debit_to, income_account=self.income_account, expense_account=self.expense_account, cost_center=self.cost_center)
pe = get_payment_entry(so.doctype, so.name)
pe = pe.save().submit()
filters = {'company': self.company, 'based_on_payment_terms': 0, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
expected_data_after_payment = [0, 1000, 0, -1000]
row = report[1][0]
self.assertEqual(expected_data_after_payment, [row.invoiced, row.paid, row.credit_note, row.outstanding])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:411*

### test_exchange_revaluation_for_party

**Category**: workflow  
**Description**: Workflow: Exchange Revaluation for party on Receivable/Payable should be included  
**Expected**: self.assertEqual(expected_data_for_err, [row.invoiced, row.paid, row.credit_note, row.outstanding])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

'\n\t\tExchange Revaluation for party on Receivable/Payable should be included\n\t\t'
company_doc = frappe.get_doc('Company', self.company)
company_doc.unrealized_exchange_gain_loss_account = company_doc.exchange_gain_loss_account
company_doc.save()
si = self.create_sales_invoice(no_payment_schedule=True, do_not_submit=True)
si.currency = 'USD'
si.conversion_rate = 80
si.debit_to = self.debtors_usd
si = si.save().submit()
err = frappe.new_doc('Exchange Rate Revaluation')
err.company = self.company
err.posting_date = today()
accounts = err.get_accounts_data()
err.extend('accounts', accounts)
err.accounts[0].new_exchange_rate = 85
row = err.accounts[0]
row.new_balance_in_base_currency = flt(row.new_exchange_rate * flt(row.balance_in_account_currency))
row.gain_loss = row.new_balance_in_base_currency - flt(row.balance_in_base_currency)
err.set_total_gain_loss()
err = err.save().submit()
err_journals = err.make_jv_entries()
je = frappe.get_doc('Journal Entry', err_journals.get('revaluation_jv'))
je = je.submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
expected_data_for_err = [0, -500, 0, 500]
row = next((x for x in report[1] if x.voucher_type == je.doctype and x.voucher_no == je.name))
self.assertEqual(expected_data_for_err, [row.invoiced, row.paid, row.credit_note, row.outstanding])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:455*

### test_payment_against_credit_note

**Category**: workflow  
**Description**: Workflow: Payment against credit/debit note should be considered against the parent invoice  
**Expected**: self.assertEqual(report[1], [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

'\n\t\tPayment against credit/debit note should be considered against the parent invoice\n\t\t'
si1 = self.create_sales_invoice()
pe = get_payment_entry(si1.doctype, si1.name, bank_account=self.cash)
pe.paid_from = self.debit_to
pe.insert()
pe.submit()
cr_note = self.create_credit_note(si1.name)
si2 = self.create_sales_invoice()
je = frappe.new_doc('Journal Entry')
je.company = self.company
je.voucher_type = 'Credit Note'
je.posting_date = today()
debit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'debit': 100, 'debit_in_account_currency': 100, 'reference_type': cr_note.doctype, 'reference_name': cr_note.name, 'cost_center': self.cost_center}
credit_entry = {'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit': 100, 'credit_in_account_currency': 100, 'reference_type': si2.doctype, 'reference_name': si2.name, 'cost_center': self.cost_center}
je.append('accounts', debit_entry)
je.append('accounts', credit_entry)
je = je.save().submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120'}
report = execute(filters)
self.assertEqual(report[1], [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:508*

### test_group_by_party

**Category**: workflow  
**Description**: Workflow: test group by party  
**Expected**: self.assertEqual(expected_total_rows[2], [grand_total_row.get('party'), grand_total_row.get('invoiced'), grand_total_row.get('outstanding')])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_usd_receivable_account()
self.clear_old_entries()

si1 = self.create_sales_invoice(do_not_submit=True)
si1.posting_date = add_days(today(), -1)
si1.save().submit()
si2 = self.create_sales_invoice(do_not_submit=True)
si2.items[0].rate = 85
si2.save().submit()
filters = {'company': self.company, 'report_date': today(), 'range': '30, 60, 90, 120', 'group_by_party': True}
report = execute(filters)[1]
self.assertEqual(len(report), 5)
expected_voucher_rows = [[100.0, 100.0, 100.0, 100.0], [85.0, 85.0, 85.0, 85.0]]
voucher_rows = []
for x in report[0:2]:
    voucher_rows.append([x.invoiced, x.outstanding, x.invoiced_in_account_currency, x.outstanding_in_account_currency])
self.assertEqual(expected_voucher_rows, voucher_rows)
expected_total_rows = [[self.customer, 185.0, 185.0], {}, ['Total', 185.0, 185.0]]
party_total_row = report[2]
self.assertEqual(expected_total_rows[0], [party_total_row.get('party'), party_total_row.get('invoiced'), party_total_row.get('outstanding')])
empty_row = report[3]
self.assertEqual(expected_total_rows[1], empty_row)
grand_total_row = report[4]
self.assertEqual(expected_total_rows[2], [grand_total_row.get('party'), grand_total_row.get('invoiced'), grand_total_row.get('outstanding')])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable/test_accounts_receivable.py:563*

### test_payment_order_creation_against_payment_entry

**Category**: workflow  
**Description**: Workflow: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.amount, 250)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

purchase_invoice = make_purchase_invoice()
payment_entry = get_payment_entry('Purchase Invoice', purchase_invoice.name, bank_account=self.gl_account)
payment_entry.reference_no = '_Test_Payment_Order'
payment_entry.reference_date = getdate()
payment_entry.party_bank_account = self.bank_account
payment_entry.insert()
payment_entry.submit()
doc = create_payment_order_against_payment_entry(payment_entry, 'Payment Entry', self.bank_account)
reference_doc = doc.get('references')[0]
self.assertEqual(reference_doc.reference_name, payment_entry.name)
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
self.assertEqual(reference_doc.supplier, '_Test Supplier')
self.assertEqual(reference_doc.amount, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:32*

### test_payment_order_creation_against_payment_entry

**Category**: workflow  
**Description**: Workflow: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.amount, 250)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
purchase_invoice = make_purchase_invoice()
payment_entry = get_payment_entry('Purchase Invoice', purchase_invoice.name, bank_account=self.gl_account)
payment_entry.reference_no = '_Test_Payment_Order'
payment_entry.reference_date = getdate()
payment_entry.party_bank_account = self.bank_account
payment_entry.insert()
payment_entry.submit()
doc = create_payment_order_against_payment_entry(payment_entry, 'Payment Entry', self.bank_account)
reference_doc = doc.get('references')[0]
self.assertEqual(reference_doc.reference_name, payment_entry.name)
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
self.assertEqual(reference_doc.supplier, '_Test Supplier')
self.assertEqual(reference_doc.amount, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:32*

### test_preprocess_mt940_content_with_long_statement_number

**Category**: workflow  
**Description**: Workflow: Test that statement numbers longer than 5 digits are truncated to last 5 digits  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test that statement numbers longer than 5 digits are truncated to last 5 digits'
mt940_content = ':28C:167619/1'
expected_content = ':28C:67619/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:15*

### test_preprocess_mt940_content_with_normal_statement_number

**Category**: workflow  
**Description**: Workflow: Test that statement numbers with 5 or fewer digits are unchanged  
**Expected**: self.assertEqual(result, mt940_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test that statement numbers with 5 or fewer digits are unchanged'
mt940_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
mt940_content = ':28C:1234/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:23*

### test_preprocess_mt940_content_without_sequence_number

**Category**: workflow  
**Description**: Workflow: Test statement number truncation without sequence number  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test statement number truncation without sequence number'
mt940_content = ':28C:987654321'
expected_content = ':28C:54321'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:35*

### test_preprocess_mt940_content_multiple_occurrences

**Category**: workflow  
**Description**: Workflow: Test multiple statement numbers in the same content  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test multiple statement numbers in the same content'
mt940_content = ':28C:167619/1\n:28C:987654/2'
expected_content = ':28C:67619/1\n:28C:87654/2'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:43*

### test_preprocess_mt940_content_edge_cases

**Category**: workflow  
**Description**: Workflow: Test edge cases like empty content and content without :28C: tags  
**Expected**: self.assertEqual(result, content_without_28c)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test edge cases like empty content and content without :28C: tags'
self.assertEqual(preprocess_mt940_content(''), '')
content_without_28c = ':20:STARTUMSE\n:25:12345678901234567890\n:60F:C031002EUR0,00'
result = preprocess_mt940_content(content_without_28c)
self.assertEqual(result, content_without_28c)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:52*

### test_preprocess_mt940_content_with_full_mt940_document

**Category**: workflow  
**Description**: Workflow: Test preprocessing with complete MT940 document  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test preprocessing with complete MT940 document'
mt940_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:167619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
expected_content = ':20:STARTUMSE\n:25:12345678901234567890\n:28C:67619/1\n:60F:C031002EUR0,00\n:61:0310021002DR123,45NMSCNONREF//8327000090031789\n:86:806?20EREF+NONREF?21MREF+M180031?22CRED+DE98ZZZ09999999999\n:62F:C031002EUR-123,45\n-'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:64*

### test_preprocess_mt940_content_boundary_conditions

**Category**: workflow  
**Description**: Workflow: Test boundary conditions for statement number length  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test boundary conditions for statement number length'
mt940_content = ':28C:123456/1'
expected_content = ':28C:23456/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
mt940_content = ':28C:123456789012345/1'
expected_content = ':28C:12345/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:110*

### test_preprocess_mt940_content_real_world_case

**Category**: workflow  
**Description**: Workflow: Test with real-world MT940 content that was failing in production  
**Expected**: self.assertIn('UPI/TEST USER/123456789/PaidViaTestApp', result)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test with real-world MT940 content that was failing in production'
mt940_content = '{1:F0112345678901X0000000000}{2:I94012345678901XN}{4:\n:20:STMTREF167619\n:25:1234567890\n:28C:167619/1\n:60F:C250622USD0,00\n:61:2507170717C100000,00NMSCNOREF\n:86:BY EXAMPLE INST 123456/03-07-25/TESTBANK/CITY\n:61:2507240724C1,00NMSCNEFTINW-1234567890\n:86:NEFT TEST123456789 EXAMPLE MERCHANT SERVICES\n:61:2507310731D305,62NMSCTBMS-1234567890\n:86:Chrg: Debit Card Annual Fee 1234 for 2025\n:61:2508030803D1066,00NMSC123456789\n:86:PCD/1234/EXAMPLE DOMAIN/01234567890123/23:27\n:61:2508060806D2000,00NMSCUPI-123456789\n:86:UPI/TEST USER/123456789/PaidViaTestApp\n:61:2508140814D5000,00NMSCUPI-123456789\n:86:UPI/TEST USER/123456789/PaidViaTestApp\n:61:2509190919D900,00NMSCUPI-123456789\n:86:UPI/EXAMPLE MERCHANT/123456789/Pay\n:61:2509190919D2606,00NMSCUPI-123456789\n:86:UPI/JOHN DOE/123456789/PaidViaTestApp\n:62F:C250922USD88123,38\n-}'
expected_content = '{1:F0112345678901X0000000000}{2:I94012345678901XN}{4:\n:20:STMTREF167619\n:25:1234567890\n:28C:67619/1\n:60F:C250622USD0,00\n:61:2507170717C100000,00NMSCNOREF\n:86:BY EXAMPLE INST 123456/03-07-25/TESTBANK/CITY\n:61:2507240724C1,00NMSCNEFTINW-1234567890\n:86:NEFT TEST123456789 EXAMPLE MERCHANT SERVICES\n:61:2507310731D305,62NMSCTBMS-1234567890\n:86:Chrg: Debit Card Annual Fee 1234 for 2025\n:61:2508030803D1066,00NMSC123456789\n:86:PCD/1234/EXAMPLE DOMAIN/01234567890123/23:27\n:61:2508060806D2000,00NMSCUPI-123456789\n:86:UPI/TEST USER/123456789/PaidViaTestApp\n:61:2508140814D5000,00NMSCUPI-123456789\n:86:UPI/TEST USER/123456789/PaidViaTestApp\n:61:2509190919D900,00NMSCUPI-123456789\n:86:UPI/EXAMPLE MERCHANT/123456789/Pay\n:61:2509190919D2606,00NMSCUPI-123456789\n:86:UPI/JOHN DOE/123456789/PaidViaTestApp\n:62F:C250922USD88123,38\n-}'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
self.assertIn(':28C:67619/1', result)
self.assertNotIn(':28C:167619/1', result)
self.assertIn(':20:STMTREF167619', result)
self.assertIn('UPI/TEST USER/123456789/PaidViaTestApp', result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:129*

### test_preprocess_mt940_content_whitespace_variants

**Category**: workflow  
**Description**: Workflow: Test handling of whitespace and different line endings  
**Expected**: self.assertEqual(result, mt940_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test handling of whitespace and different line endings'
mt940_content = ':28C:167619/1   \n'
expected_content = ':28C:67619/1   \n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = ':28C:167619/1\r\n'
expected_content = ':28C:67619/1\r\n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
mt940_content = '   :28C:167619/1\n'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, mt940_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:192*

### test_preprocess_mt940_content_with_long_statement_number

**Category**: workflow  
**Description**: Workflow: Test that statement numbers longer than 5 digits are truncated to last 5 digits  
**Expected**: self.assertEqual(result, expected_content)  
**Confidence**: 0.90  
**Tags**: unittest, workflow, integration  

```python
'Test that statement numbers longer than 5 digits are truncated to last 5 digits'
mt940_content = ':28C:167619/1'
expected_content = ':28C:67619/1'
result = preprocess_mt940_content(mt940_content)
self.assertEqual(result, expected_content)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_statement_import/test_bank_statement_import.py:15*

### test_auto_reconcile

**Category**: workflow  
**Description**: Workflow: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_customer()
self.clear_old_entries()
bank_dt = qb.DocType('Bank')
qb.from_(bank_dt).delete().where(bank_dt.name == 'HDFC').run()
self.create_bank_account()

from_date = add_days(today(), -1)
to_date = today()
payment = create_payment_entry(company=self.company, posting_date=from_date, payment_type='Receive', party_type='Customer', party=self.customer, paid_from=self.debit_to, paid_to=self.bank, paid_amount=100).save()
payment.reference_no = '123'
payment = payment.save().submit()
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'date': to_date, 'deposit': 100, 'bank_account': self.bank_account, 'reference_number': '123', 'currency': 'INR'}).save().submit()
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 1)
self.assertEqual(transactions[0].name, bank_transaction.name)
auto_reconcile_vouchers(bank_account=self.bank_account, from_date=from_date, to_date=to_date, filter_by_reference_date=False)
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:52*

### test_auto_reconcile

**Category**: workflow  
**Description**: Workflow: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from_date = add_days(today(), -1)
to_date = today()
payment = create_payment_entry(company=self.company, posting_date=from_date, payment_type='Receive', party_type='Customer', party=self.customer, paid_from=self.debit_to, paid_to=self.bank, paid_amount=100).save()
payment.reference_no = '123'
payment = payment.save().submit()
bank_transaction = frappe.get_doc({'doctype': 'Bank Transaction', 'date': to_date, 'deposit': 100, 'bank_account': self.bank_account, 'reference_number': '123', 'currency': 'INR'}).save().submit()
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 1)
self.assertEqual(transactions[0].name, bank_transaction.name)
auto_reconcile_vouchers(bank_account=self.bank_account, from_date=from_date, to_date=to_date, filter_by_reference_date=False)
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
self.assertEqual(len(transactions), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:52*

### test_01_basic_report_functionality

**Category**: workflow  
**Description**: Workflow: test 01 basic report functionality  
**Expected**: self.assertEqual([], data)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.cleanup()

sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
ple = frappe.db.get_all('Payment Ledger Entry', filters={'voucher_no': sinv.name, 'delinked': 0})[0]
frappe.db.set_value('Payment Ledger Entry', ple.name, 'amount', sinv.grand_total - 1)
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
expected = {'company': sinv.company, 'account': sinv.debit_to, 'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'party_type': 'Customer', 'party': sinv.customer, 'gl_balance': sinv.grand_total, 'pl_balance': sinv.grand_total - 1}
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.debit_to})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.creditors})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name + '-1'})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'period_start_date': sinv.posting_date, 'period_end_date': sinv.posting_date})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'period_start_date': add_days(sinv.posting_date, -1), 'period_end_date': add_days(sinv.posting_date, -1)})
columns, data = execute(filters=filters)
self.assertEqual([], data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:30*

### test_01_basic_report_functionality

**Category**: workflow  
**Description**: Workflow: test 01 basic report functionality  
**Expected**: self.assertEqual([], data)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
ple = frappe.db.get_all('Payment Ledger Entry', filters={'voucher_no': sinv.name, 'delinked': 0})[0]
frappe.db.set_value('Payment Ledger Entry', ple.name, 'amount', sinv.grand_total - 1)
filters = frappe._dict({'company': self.company})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
expected = {'company': sinv.company, 'account': sinv.debit_to, 'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'party_type': 'Customer', 'party': sinv.customer, 'gl_balance': sinv.grand_total, 'pl_balance': sinv.grand_total - 1}
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.debit_to})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'account': self.creditors})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'voucher_no': sinv.name + '-1'})
columns, data = execute(filters=filters)
self.assertEqual([], data)
filters = frappe._dict({'company': self.company, 'period_start_date': sinv.posting_date, 'period_end_date': sinv.posting_date})
columns, data = execute(filters=filters)
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
filters = frappe._dict({'company': self.company, 'period_start_date': add_days(sinv.posting_date, -1), 'period_end_date': add_days(sinv.posting_date, -1)})
columns, data = execute(filters=filters)
self.assertEqual([], data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:30*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()

pi = self.create_purchase_invoice()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:37*

### test_basic_report_output

**Category**: workflow  
**Description**: Workflow: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = self.create_purchase_invoice()
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
report = execute(filters)
self.assertEqual(len(report[1]), 1)
expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
report_output = {k: v for k, v in report[1][0].items() if k in expected_result}
self.assertDictEqual(report_output, expected_result)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:37*

### test_payment_entry_against_order

**Category**: workflow  
**Description**: Workflow: test payment entry against order  
**Expected**: self.assertEqual(so_advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order()
pe = get_payment_entry('Sales Order', so.name, bank_account='_Test Cash - _TC')
pe.paid_from = 'Debtors - _TC'
pe.insert()
pe.submit()
self.assertEqual(pe.paid_to_account_type, 'Cash')
expected_gle = dict(((d[0], d) for d in [['Debtors - _TC', 0, 1000, pe.name], ['_Test Cash - _TC', 1000.0, 0, None]]))
self.validate_gl_entries(pe.name, expected_gle)
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 1000)
pe.cancel()
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:45*

### test_payment_against_sales_order_usd_to_inr

**Category**: workflow  
**Description**: Workflow: test payment against sales order usd to inr  
**Expected**: self.assertEqual(so_advance_paid, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order(customer='_Test Customer USD', currency='USD', qty=1, rate=100, do_not_submit=True)
so.conversion_rate = 50
so.submit()
pe = get_payment_entry('Sales Order', so.name)
pe.source_exchange_rate = 55
pe.received_amount = 5500
pe.insert()
pe.submit()
pe.reload()
self.assertEqual(pe.difference_amount, 0)
self.assertEqual(pe.deductions, [])
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5500, pe.name], [pe.paid_to, 5500.0, 0, None]]))
self.validate_gl_entries(pe.name, expected_gle)
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 100)
pe.cancel()
so_advance_paid = frappe.db.get_value('Sales Order', so.name, 'advance_paid')
self.assertEqual(so_advance_paid, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:68*

### test_payment_entry_for_blocked_supplier_invoice

**Category**: workflow  
**Description**: Workflow: test payment entry for blocked supplier invoice  
**Expected**: self.assertRaises(frappe.ValidationError, make_purchase_invoice)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Invoices'
supplier.save()
self.assertRaises(frappe.ValidationError, make_purchase_invoice)
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:100*

### test_payment_entry_for_blocked_supplier_payments

**Category**: workflow  
**Description**: Workflow: test payment entry for blocked supplier payments  
**Expected**: self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Payments'
supplier.save()
pi = make_purchase_invoice()
self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:111*

### test_payment_entry_for_blocked_supplier_payments_today_date

**Category**: workflow  
**Description**: Workflow: test payment entry for blocked supplier payments today date  
**Expected**: self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Payments'
supplier.release_date = nowdate()
supplier.save()
pi = make_purchase_invoice()
self.assertRaises(frappe.ValidationError, get_payment_entry, dt='Purchase Invoice', dn=pi.name, bank_account='_Test Bank - _TC')
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:130*

### test_payment_entry_against_si_usd_to_usd

**Category**: workflow  
**Description**: Workflow: test payment entry against si usd to usd  
**Expected**: self.assertEqual(outstanding_amount, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank USD - _TC')
pe.reference_no = '1'
pe.reference_date = '2016-01-01'
pe.source_exchange_rate = 50
pe.insert()
pe.submit()
expected_gle = dict(((d[0], d) for d in [['_Test Receivable USD - _TC', 0, 5000, si.name], ['_Test Bank USD - _TC', 5000.0, 0, None]]))
self.validate_gl_entries(pe.name, expected_gle)
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 0)
pe.cancel()
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', si.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:171*

### test_payment_entry_against_pi

**Category**: workflow  
**Description**: Workflow: test payment entry against pi  
**Expected**: self.assertEqual(outstanding_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = make_purchase_invoice(supplier='_Test Supplier USD', debit_to='_Test Payable USD - _TC', currency='USD', conversion_rate=50)
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Bank USD - _TC')
pe.reference_no = '1'
pe.reference_date = '2016-01-01'
pe.source_exchange_rate = 50
pe.insert()
pe.submit()
expected_gle = dict(((d[0], d) for d in [['_Test Payable USD - _TC', 12500, 0, pi.name], ['_Test Bank USD - _TC', 0, 12500, None]]))
self.validate_gl_entries(pe.name, expected_gle)
outstanding_amount = flt(frappe.db.get_value('Sales Invoice', pi.name, 'outstanding_amount'))
self.assertEqual(outstanding_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:203*

### test_payment_against_sales_invoice_to_check_status

**Category**: workflow  
**Description**: Workflow: test payment against sales invoice to check status  
**Expected**: self.assertEqual(status, 'Unpaid')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(customer='_Test Customer USD', debit_to='_Test Receivable USD - _TC', currency='USD', conversion_rate=50)
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Bank USD - _TC')
pe.reference_no = '1'
pe.reference_date = '2016-01-01'
pe.source_exchange_rate = 50
pe.insert()
pe.submit()
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
self.assertEqual(flt(outstanding_amount), 0)
self.assertEqual(status, 'Paid')
pe.cancel()
outstanding_amount, status = frappe.db.get_value('Sales Invoice', si.name, ['outstanding_amount', 'status'])
self.assertEqual(flt(outstanding_amount), 100)
self.assertEqual(status, 'Unpaid')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:230*

### test_payment_entry_against_payment_terms_with_discount_on_pi

**Category**: workflow  
**Description**: Workflow: test payment entry against payment terms with discount on pi  
**Expected**: self.assertEqual(pe.difference_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = make_purchase_invoice(do_not_save=1)
create_payment_terms_template_with_discount()
pi.payment_terms_template = 'Test Discount Template'
frappe.db.set_value('Company', pi.company, 'default_discount_account', 'Write Off - _TC')
pi.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
pi.save()
pi.submit()
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
pe_with_tax_loss = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe_with_tax_loss.payment_type, 'Pay')
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 295.0)
self.assertEqual(pe_with_tax_loss.paid_amount, 265.5)
self.assertEqual(pe_with_tax_loss.difference_amount, 0)
self.assertEqual(pe_with_tax_loss.deductions[0].amount, -25.0)
self.assertEqual(pe_with_tax_loss.deductions[1].amount, -4.5)
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
pe = get_payment_entry('Purchase Invoice', pi.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe.payment_type, 'Pay')
self.assertEqual(pe.references[0].allocated_amount, 295.0)
self.assertEqual(pe.paid_amount, 265.5)
self.assertEqual(pe.deductions[0].amount, -29.5)
self.assertEqual(pe.difference_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:287*

### test_payment_entry_against_payment_terms_with_discount

**Category**: workflow  
**Description**: Workflow: test payment entry against payment terms with discount  
**Expected**: self.assertEqual(si.payment_schedule[0].discounted_amount, 23.6)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
si = create_sales_invoice(do_not_save=1, qty=1, rate=200)
create_payment_terms_template_with_discount()
si.payment_terms_template = 'Test Discount Template'
frappe.db.set_value('Company', si.company, 'default_discount_account', 'Write Off - _TC')
si.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'cost_center': '_Test Cost Center - _TC', 'description': 'Service Tax', 'rate': 18})
si.save()
si.submit()
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 1)
pe_with_tax_loss = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe_with_tax_loss.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(pe_with_tax_loss.references[0].allocated_amount, 236.0)
self.assertEqual(pe_with_tax_loss.paid_amount, 212.4)
self.assertEqual(pe_with_tax_loss.deductions[0].amount, 20.0)
self.assertEqual(pe_with_tax_loss.deductions[1].amount, 3.6)
self.assertEqual(pe_with_tax_loss.deductions[1].account, '_Test Account Service Tax - _TC')
frappe.db.set_single_value('Accounts Settings', 'book_tax_discount_loss', 0)
pe = get_payment_entry('Sales Invoice', si.name, bank_account='_Test Cash - _TC')
self.assertEqual(pe.references[0].allocated_amount, 236.0)
self.assertEqual(pe.paid_amount, 212.4)
self.assertEqual(pe.deductions[0].amount, 23.6)
pe.submit()
si.load_from_db()
self.assertEqual(pe.references[0].payment_term, '30 Credit Days with 10% Discount')
self.assertEqual(si.payment_schedule[0].payment_amount, 236.0)
self.assertEqual(si.payment_schedule[0].paid_amount, 212.4)
self.assertEqual(si.payment_schedule[0].outstanding, 0)
self.assertEqual(si.payment_schedule[0].discounted_amount, 23.6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_entry/test_payment_entry.py:329*

### test_jv_against_stock_account

**Category**: workflow  
**Description**: Workflow: test jv against stock account  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company with perpetual inventory'
stock_account = get_inventory_account(company)
from erpnext.accounts.utils import get_stock_and_account_balance
account_bal, stock_bal, warehouse_list = get_stock_and_account_balance(stock_account, nowdate(), company)
diff = flt(account_bal) - flt(stock_bal)
if not diff:
    diff = 100
jv = frappe.new_doc('Journal Entry')
jv.company = company
jv.posting_date = nowdate()
jv.append('accounts', {'account': stock_account, 'cost_center': 'Main - TCP1', 'debit_in_account_currency': 0 if diff > 0 else abs(diff), 'credit_in_account_currency': diff if diff > 0 else 0})
jv.append('accounts', {'account': 'Stock Adjustment - TCP1', 'cost_center': 'Main - TCP1', 'debit_in_account_currency': diff if diff > 0 else 0, 'credit_in_account_currency': 0 if diff > 0 else abs(diff)})
if account_bal == stock_bal:
    self.assertRaises(StockAccountInvalidTransaction, jv.save)
    frappe.db.rollback()
else:
    jv.submit()
    jv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:113*

### test_multi_currency

**Category**: workflow  
**Description**: Workflow: test multi currency  
**Expected**: self.assertFalse(gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = make_journal_entry('_Test Bank USD - _TC', '_Test Bank - _TC', 100, exchange_rate=50, save=False)
jv.get('accounts')[1].credit_in_account_currency = 5000
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'account_currency', 'debit', 'debit_in_account_currency', 'credit', 'credit_in_account_currency']
self.expected_gle = [{'account': '_Test Bank - _TC', 'account_currency': 'INR', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 5000}, {'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 5000, 'debit_in_account_currency': 100, 'credit': 0, 'credit_in_account_currency': 0}]
self.check_gl_entries()
jv.cancel()
gle = frappe.db.sql("select name from `tabGL Entry`\n\t\t\twhere voucher_type='Sales Invoice' and voucher_no=%s", jv.name)
self.assertFalse(gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:157*

### test_reverse_journal_entry

**Category**: workflow  
**Description**: Workflow: test reverse journal entry  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.journal_entry.journal_entry import make_reverse_journal_entry
jv = make_journal_entry('_Test Bank USD - _TC', 'Sales - _TC', 100, exchange_rate=50, save=False)
jv.get('accounts')[1].credit_in_account_currency = 5000
jv.get('accounts')[1].exchange_rate = 1
jv.submit()
rjv = make_reverse_journal_entry(jv.name)
rjv.posting_date = nowdate()
rjv.submit()
self.voucher_no = rjv.name
self.fields = ['account', 'account_currency', 'debit', 'credit', 'debit_in_account_currency', 'credit_in_account_currency']
self.expected_gle = [{'account': '_Test Bank USD - _TC', 'account_currency': 'USD', 'debit': 0, 'debit_in_account_currency': 0, 'credit': 5000, 'credit_in_account_currency': 100}, {'account': 'Sales - _TC', 'account_currency': 'INR', 'debit': 5000, 'debit_in_account_currency': 5000, 'credit': 0, 'credit_in_account_currency': 0}]
self.check_gl_entries()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:206*

### test_inter_company_jv

**Category**: workflow  
**Description**: Workflow: test inter company jv  
**Expected**: self.assertEqual(jv1.inter_company_journal_entry_reference, '')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
jv = make_journal_entry('Sales Expenses - _TC', 'Buildings - _TC', 100, posting_date=nowdate(), cost_center='Main - _TC', save=False)
jv.voucher_type = 'Inter Company Journal Entry'
jv.multi_currency = 0
jv.insert()
jv.submit()
jv1 = make_journal_entry('Sales Expenses - _TC1', 'Buildings - _TC1', 100, posting_date=nowdate(), cost_center='Main - _TC1', save=False)
jv1.inter_company_journal_entry_reference = jv.name
jv1.company = '_Test Company 1'
jv1.voucher_type = 'Inter Company Journal Entry'
jv1.multi_currency = 0
jv1.insert()
jv1.submit()
jv.reload()
self.assertEqual(jv.inter_company_journal_entry_reference, jv1.name)
self.assertEqual(jv1.inter_company_journal_entry_reference, jv.name)
jv.cancel()
jv1.reload()
jv.reload()
self.assertEqual(jv.inter_company_journal_entry_reference, '')
self.assertEqual(jv1.inter_company_journal_entry_reference, '')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:273*

### test_jv_with_cost_centre

**Category**: workflow  
**Description**: Workflow: test jv with cost centre  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
cost_center = '_Test Cost Center for BS Account - _TC'
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'cost_center']
self.expected_gle = [{'account': '_Test Bank - _TC', 'cost_center': cost_center}, {'account': '_Test Cash - _TC', 'cost_center': cost_center}]
self.check_gl_entries()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:314*

### test_jv_with_project

**Category**: workflow  
**Description**: Workflow: test jv with project  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.projects.doctype.project.test_project import make_project
if not frappe.db.exists('Project', {'project_name': 'Journal Entry Project'}):
    project = make_project({'project_name': 'Journal Entry Project', 'project_template_name': 'Test Project Template', 'start_date': '2020-01-01'})
    project_name = project.name
else:
    project_name = frappe.get_value('Project', {'project_name': '_Test Project'})
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
for d in jv.accounts:
    d.project = project_name
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'project']
self.expected_gle = [{'account': '_Test Bank - _TC', 'project': project_name}, {'account': '_Test Cash - _TC', 'project': project_name}]
self.check_gl_entries()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:349*

### test_jv_account_and_party_balance_with_cost_centre

**Category**: workflow  
**Description**: Workflow: test jv account and party balance with cost centre  
**Expected**: self.assertEqual(expected_account_balance, account_balance)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_balance_on
cost_center = '_Test Cost Center for BS Account - _TC'
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, cost_center=cost_center, save=False)
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
jv.voucher_type = 'Bank Entry'
jv.multi_currency = 0
jv.cheque_no = '112233'
jv.cheque_date = nowdate()
jv.insert()
jv.submit()
expected_account_balance = account_balance - 100
account_balance = get_balance_on(account='_Test Bank - _TC', cost_center=cost_center)
self.assertEqual(expected_account_balance, account_balance)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:391*

### test_repost_accounting_entries

**Category**: workflow  
**Description**: Workflow: test repost accounting entries  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
settings = frappe.get_doc('Repost Accounting Ledger Settings')
if not [x for x in settings.allowed_types if x.document_type == 'Journal Entry']:
    settings.append('allowed_types', {'document_type': 'Journal Entry', 'allowed': True})
settings.save()
jv = make_journal_entry('_Test Cash - _TC', '_Test Bank - _TC', 100, save=False)
jv.multi_currency = 0
jv.submit()
self.voucher_no = jv.name
self.fields = ['account', 'debit_in_account_currency', 'credit_in_account_currency', 'cost_center']
self.expected_gle = [{'account': '_Test Bank - _TC', 'debit_in_account_currency': 0, 'credit_in_account_currency': 100, 'cost_center': '_Test Cost Center - _TC'}, {'account': '_Test Cash - _TC', 'debit_in_account_currency': 100, 'credit_in_account_currency': 0, 'cost_center': '_Test Cost Center - _TC'}]
self.check_gl_entries()
create_cost_center(cost_center_name='_Test Cost Center for BS Account', company='_Test Company')
jv.accounts[1].cost_center = '_Test Cost Center for BS Account - _TC'
jv.save()
jv.load_from_db()
self.expected_gle[0]['cost_center'] = '_Test Cost Center for BS Account - _TC'
self.check_gl_entries()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:412*

### test_negative_debit_and_credit_with_same_account_head

**Category**: workflow  
**Description**: Workflow: test negative debit and credit with same account head  
**Expected**: self.assertEqual(len(jv.accounts), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.general_ledger import process_gl_map
frappe.db.set_single_value('Accounts Settings', 'merge_similar_account_heads', 0)
jv = make_journal_entry('_Test Bank - _TC', '_Test Bank - _TC', 100 * -1, save=True)
jv.append('accounts', {'account': '_Test Cash - _TC', 'debit': 100 * -1, 'credit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1})
jv.flags.ignore_validate = True
jv.save()
self.assertEqual(len(jv.accounts), 3)
gl_map = jv.build_gl_map()
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit_in_account_currency, 100 * -1)
        self.assertEqual(row.credit_in_account_currency, 100 * -1)
gl_map = process_gl_map(gl_map, False)
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit_in_account_currency, 100)
        self.assertEqual(row.credit_in_account_currency, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:480*

### test_toggle_debit_credit_if_negative

**Category**: workflow  
**Description**: Workflow: test toggle debit credit if negative  
**Expected**: self.assertEqual(len(jv.accounts), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.general_ledger import process_gl_map
frappe.db.set_single_value('Accounts Settings', 'merge_similar_account_heads', 0)
jv = frappe.new_doc('Journal Entry')
jv.posting_date = nowdate()
jv.company = '_Test Company'
jv.user_remark = 'test'
jv.extend('accounts', [{'account': '_Test Cash - _TC', 'debit': 100 * -1, 'debit_in_account_currency': 100 * -1, 'exchange_rate': 1}, {'account': '_Test Bank - _TC', 'credit': 100 * -1, 'credit_in_account_currency': 100 * -1, 'exchange_rate': 1}])
jv.flags.ignore_validate = True
jv.save()
self.assertEqual(len(jv.accounts), 2)
gl_map = jv.build_gl_map()
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.debit, 100 * -1)
        self.assertEqual(row.debit_in_account_currency, 100 * -1)
        self.assertEqual(row.debit_in_transaction_currency, 100 * -1)
gl_map = process_gl_map(gl_map, False)
for row in gl_map:
    if row.account == '_Test Cash - _TC':
        self.assertEqual(row.credit, 100)
        self.assertEqual(row.credit_in_account_currency, 100)
        self.assertEqual(row.credit_in_transaction_currency, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/journal_entry/test_journal_entry.py:517*

### test_get_voucher_wise_gl_entry

**Category**: workflow  
**Description**: Workflow: test get voucher wise gl entry  
**Expected**: self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='_Test Item', posting_date='2021-02-01', rate=100, qty=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory')
future_vouchers = get_future_stock_vouchers('2021-01-01', '00:00:00', for_items=['_Test Item'])
voucher_type_and_no = ('Purchase Receipt', pr.name)
self.assertTrue(voucher_type_and_no in future_vouchers, msg='get_future_stock_vouchers not returning correct value')
posting_date = '2021-01-01'
gl_entries = get_voucherwise_gl_entries(future_vouchers, posting_date)
self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:37*

### test_stock_voucher_sorting

**Category**: workflow  
**Description**: Workflow: test stock voucher sorting  
**Expected**: self.assertEqual(sorted_vouchers, vouchers)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
vouchers = []
item = make_item().name
stock_entry = {'item': item, 'to_warehouse': '_Test Warehouse - _TC', 'qty': 1, 'rate': 10}
se1 = make_stock_entry(posting_date='2022-01-01', **stock_entry)
se3 = make_stock_entry(posting_date='2022-03-01', **stock_entry)
se2 = make_stock_entry(posting_date='2022-02-01', **stock_entry)
for doc in (se1, se2, se3):
    vouchers.append((doc.doctype, doc.name))
vouchers.append(('Stock Entry', 'Wat'))
sorted_vouchers = sort_stock_vouchers_by_posting_date(list(reversed(vouchers)))
self.assertEqual(sorted_vouchers, vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:62*

### test_update_reference_in_payment_entry

**Category**: workflow  
**Description**: Workflow: test update reference in payment entry  
**Expected**: self.assertEqual(payment_entry.difference_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = make_item().name
purchase_invoice = make_purchase_invoice(item=item, supplier='_Test Supplier USD', currency='USD', conversion_rate=82.32, do_not_submit=1)
purchase_invoice.credit_to = '_Test Payable USD - _TC'
purchase_invoice.submit()
payment_entry = get_payment_entry(purchase_invoice.doctype, purchase_invoice.name)
payment_entry.paid_amount = 15725
payment_entry.deductions = []
payment_entry.save()
self.assertEqual(payment_entry.deductions[0].amount, -4855.0)
payment_entry.target_exchange_rate = 62.9
payment_entry.save()
self.assertEqual(payment_entry.deductions, [])
payment_entry.references = []
self.assertEqual(payment_entry.difference_amount, 0.0)
payment_entry.submit()
payment_reconciliation = frappe.new_doc('Payment Reconciliation')
payment_reconciliation.company = payment_entry.company
payment_reconciliation.party_type = 'Supplier'
payment_reconciliation.party = purchase_invoice.supplier
payment_reconciliation.receivable_payable_account = payment_entry.paid_to
payment_reconciliation.get_unreconciled_entries()
payment_reconciliation.allocate_entries({'payments': [d.__dict__ for d in payment_reconciliation.payments], 'invoices': [d.__dict__ for d in payment_reconciliation.invoices]})
for d in payment_reconciliation.invoices:
    d.outstanding_amount = d.amount
for d in payment_reconciliation.allocation:
    d.difference_account = 'Exchange Gain/Loss - _TC'
payment_reconciliation.reconcile()
payment_entry.load_from_db()
self.assertEqual(len(payment_entry.references), 1)
self.assertEqual(payment_entry.difference_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:81*

### test_get_voucher_wise_gl_entry

**Category**: workflow  
**Description**: Workflow: test get voucher wise gl entry  
**Expected**: self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='_Test Item', posting_date='2021-02-01', rate=100, qty=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory')
future_vouchers = get_future_stock_vouchers('2021-01-01', '00:00:00', for_items=['_Test Item'])
voucher_type_and_no = ('Purchase Receipt', pr.name)
self.assertTrue(voucher_type_and_no in future_vouchers, msg='get_future_stock_vouchers not returning correct value')
posting_date = '2021-01-01'
gl_entries = get_voucherwise_gl_entries(future_vouchers, posting_date)
self.assertTrue(voucher_type_and_no in gl_entries, msg='get_voucherwise_gl_entries not returning expected GLes')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:37*

### test_stock_voucher_sorting

**Category**: workflow  
**Description**: Workflow: test stock voucher sorting  
**Expected**: self.assertEqual(sorted_vouchers, vouchers)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
vouchers = []
item = make_item().name
stock_entry = {'item': item, 'to_warehouse': '_Test Warehouse - _TC', 'qty': 1, 'rate': 10}
se1 = make_stock_entry(posting_date='2022-01-01', **stock_entry)
se3 = make_stock_entry(posting_date='2022-03-01', **stock_entry)
se2 = make_stock_entry(posting_date='2022-02-01', **stock_entry)
for doc in (se1, se2, se3):
    vouchers.append((doc.doctype, doc.name))
vouchers.append(('Stock Entry', 'Wat'))
sorted_vouchers = sort_stock_vouchers_by_posting_date(list(reversed(vouchers)))
self.assertEqual(sorted_vouchers, vouchers)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:62*

### test_update_reference_in_payment_entry

**Category**: workflow  
**Description**: Workflow: test update reference in payment entry  
**Expected**: self.assertEqual(payment_entry.difference_amount, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = make_item().name
purchase_invoice = make_purchase_invoice(item=item, supplier='_Test Supplier USD', currency='USD', conversion_rate=82.32, do_not_submit=1)
purchase_invoice.credit_to = '_Test Payable USD - _TC'
purchase_invoice.submit()
payment_entry = get_payment_entry(purchase_invoice.doctype, purchase_invoice.name)
payment_entry.paid_amount = 15725
payment_entry.deductions = []
payment_entry.save()
self.assertEqual(payment_entry.deductions[0].amount, -4855.0)
payment_entry.target_exchange_rate = 62.9
payment_entry.save()
self.assertEqual(payment_entry.deductions, [])
payment_entry.references = []
self.assertEqual(payment_entry.difference_amount, 0.0)
payment_entry.submit()
payment_reconciliation = frappe.new_doc('Payment Reconciliation')
payment_reconciliation.company = payment_entry.company
payment_reconciliation.party_type = 'Supplier'
payment_reconciliation.party = purchase_invoice.supplier
payment_reconciliation.receivable_payable_account = payment_entry.paid_to
payment_reconciliation.get_unreconciled_entries()
payment_reconciliation.allocate_entries({'payments': [d.__dict__ for d in payment_reconciliation.payments], 'invoices': [d.__dict__ for d in payment_reconciliation.invoices]})
for d in payment_reconciliation.invoices:
    d.outstanding_amount = d.amount
for d in payment_reconciliation.allocation:
    d.difference_account = 'Exchange Gain/Loss - _TC'
payment_reconciliation.reconcile()
payment_entry.load_from_db()
self.assertEqual(len(payment_entry.references), 1)
self.assertEqual(payment_entry.difference_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:81*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[1]['debit'], 1000)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[1]['account'], account.name)
self.assertEqual(data[1]['debit'], 1000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:163*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[1]['credit'], 0)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[1]['debit'], 1000)
self.assertEqual(data[1]['credit'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:164*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[2]['debit'], 0)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[1]['credit'], 0)
self.assertEqual(data[2]['debit'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:165*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[2]['credit'], 900)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[2]['debit'], 0)
self.assertEqual(data[2]['credit'], 900)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:166*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[3]['debit'], 100)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[2]['credit'], 900)
self.assertEqual(data[3]['debit'], 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:167*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[3]['credit'], 100)  
**Confidence**: 0.85  

```python
# Setup
self.company = '_Test Company'
self.clear_old_entries()

self.assertEqual(data[3]['debit'], 100)
self.assertEqual(data[3]['credit'], 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:168*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[1]['debit'], 1000)  
**Confidence**: 0.85  

```python
self.assertEqual(data[1]['account'], account.name)
self.assertEqual(data[1]['debit'], 1000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:163*

### test_foreign_account_balance_after_exchange_rate_revaluation

**Category**: method_call  
**Description**: Checks the correctness of balance after exchange rate revaluation  
**Expected**: self.assertEqual(data[1]['credit'], 0)  
**Confidence**: 0.85  

```python
self.assertEqual(data[1]['debit'], 1000)
self.assertEqual(data[1]['credit'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_ledger/test_general_ledger.py:164*

### test_01_unreconcile_invoice

**Category**: method_call  
**Description**: test 01 unreconcile invoice  
**Expected**: self.assertEqual(si2.outstanding_amount, 0)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

self.assertEqual(si1.outstanding_amount, 0)
self.assertEqual(si2.outstanding_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:85*

### test_01_unreconcile_invoice

**Category**: method_call  
**Description**: test 01 unreconcile invoice  
**Expected**: self.assertEqual(pe.unallocated_amount, 0)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_supplier()
self.create_usd_receivable_account()
self.create_item()
self.clear_old_entries()

self.assertEqual(si2.outstanding_amount, 0)
self.assertEqual(pe.unallocated_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/unreconcile_payment/test_unreconcile_payment.py:86*

### test_dimension_against_journal_entry

**Category**: method_call  
**Description**: test dimension against journal entry  
**Expected**: self.assertEqual(gle1.get('department'), '_Test Department - _TC')  
**Confidence**: 0.85  

```python
# Setup
create_dimension()

self.assertEqual(gle.get('department'), '_Test Department - _TC')
self.assertEqual(gle1.get('department'), '_Test Department - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:56*

### test_mandatory

**Category**: method_call  
**Description**: test mandatory  
**Expected**: self.assertRaises(frappe.ValidationError, si.submit)  
**Confidence**: 0.85  

```python
# Setup
create_dimension()

si.save()
self.assertRaises(frappe.ValidationError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:79*

### test_dimension_against_journal_entry

**Category**: method_call  
**Description**: test dimension against journal entry  
**Expected**: self.assertEqual(gle1.get('department'), '_Test Department - _TC')  
**Confidence**: 0.85  

```python
self.assertEqual(gle.get('department'), '_Test Department - _TC')
self.assertEqual(gle1.get('department'), '_Test Department - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:56*

### test_mandatory

**Category**: method_call  
**Description**: test mandatory  
**Expected**: self.assertRaises(frappe.ValidationError, si.submit)  
**Confidence**: 0.85  

```python
si.save()
self.assertRaises(frappe.ValidationError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:79*

### test_conflict_with_non_overlapping_dates

**Category**: method_call  
**Description**: test conflict with non overlapping dates  
**Expected**: self.assertTrue(tax_rule2.name)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

tax_rule2.save()
self.assertTrue(tax_rule2.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:57*

### test_for_parent_customer_group

**Category**: method_call  
**Description**: test for parent customer group  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer_group': 'Commercial', 'use_for_shopping_cart': 1}), '_Test Sales Taxes and Charges Template - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

tax_rule1.save()
self.assertEqual(get_tax_template('2015-01-01', {'customer_group': 'Commercial', 'use_for_shopping_cart': 1}), '_Test Sales Taxes and Charges Template - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:67*

### test_select_tax_rule_based_on_customer

**Category**: method_call  
**Description**: test select tax rule based on customer  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer 2'}), '_Test Sales Taxes and Charges Template 2 - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer 2', sales_tax_template='_Test Sales Taxes and Charges Template 2 - _TC', save=1)
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer 2'}), '_Test Sales Taxes and Charges Template 2 - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:110*

### test_select_tax_rule_based_on_tax_category

**Category**: method_call  
**Description**: test select tax rule based on tax category  
**Expected**: self.assertFalse(get_tax_template('2015-01-01', {'customer': '_Test Customer'}))  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer', tax_category='_Test Tax Category 2', sales_tax_template='_Test Sales Taxes and Charges Template 2 - _TC', save=1)
self.assertFalse(get_tax_template('2015-01-01', {'customer': '_Test Customer'}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:129*

### test_select_tax_rule_based_on_tax_category

**Category**: method_call  
**Description**: test select tax rule based on tax category  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'tax_category': '_Test Tax Category 1'}), '_Test Sales Taxes and Charges Template 1 - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

self.assertFalse(get_tax_template('2015-01-01', {'customer': '_Test Customer'}))
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'tax_category': '_Test Tax Category 1'}), '_Test Sales Taxes and Charges Template 1 - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:136*

### test_select_tax_rule_based_on_tax_category

**Category**: method_call  
**Description**: test select tax rule based on tax category  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'tax_category': '_Test Tax Category 2'}), '_Test Sales Taxes and Charges Template 2 - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'tax_category': '_Test Tax Category 1'}), '_Test Sales Taxes and Charges Template 1 - _TC')
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'tax_category': '_Test Tax Category 2'}), '_Test Sales Taxes and Charges Template 2 - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:138*

### test_select_tax_rule_based_on_tax_category

**Category**: method_call  
**Description**: test select tax rule based on tax category  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer'}), '_Test Sales Taxes and Charges Template - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer', tax_category='', sales_tax_template='_Test Sales Taxes and Charges Template - _TC', save=1)
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer'}), '_Test Sales Taxes and Charges Template - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:151*

### test_select_tax_rule_based_on_better_match

**Category**: method_call  
**Description**: test select tax rule based on better match  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'billing_city': 'Test City', 'billing_state': 'Test State'}), '_Test Sales Taxes and Charges Template - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer', billing_city='Test City1', billing_state='Test State', sales_tax_template='_Test Sales Taxes and Charges Template 1 - _TC', save=1)
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'billing_city': 'Test City', 'billing_state': 'Test State'}), '_Test Sales Taxes and Charges Template - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:172*

### test_select_tax_rule_based_on_state_match

**Category**: method_call  
**Description**: test select tax rule based on state match  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'shipping_state': 'Test State'}), '_Test Sales Taxes and Charges Template - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer', shipping_state='Test State12', sales_tax_template='_Test Sales Taxes and Charges Template 1 - _TC', priority=2, save=1)
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'shipping_state': 'Test State'}), '_Test Sales Taxes and Charges Template - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:196*

### test_select_tax_rule_based_on_better_priority

**Category**: method_call  
**Description**: test select tax rule based on better priority  
**Expected**: self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'billing_city': 'Test City'}), '_Test Sales Taxes and Charges Template 1 - _TC')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabTax Rule`')

make_tax_rule(customer='_Test Customer', billing_city='Test City', sales_tax_template='_Test Sales Taxes and Charges Template 1 - _TC', priority=2, save=1)
self.assertEqual(get_tax_template('2015-01-01', {'customer': '_Test Customer', 'billing_city': 'Test City'}), '_Test Sales Taxes and Charges Template 1 - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/tax_rule/test_tax_rule.py:218*

### test_01_receivable_summary_output

**Category**: method_call  
**Description**: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:75*

### test_01_receivable_summary_output

**Category**: method_call  
**Description**: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: expected_data.update({'advance': 50.0, 'outstanding': 150.0, 'range1': 150.0, 'total_due': 150.0})  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

pe.save().submit()
expected_data.update({'advance': 50.0, 'outstanding': 150.0, 'range1': 150.0, 'total_due': 150.0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:82*

### test_01_receivable_summary_output

**Category**: method_call  
**Description**: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:96*

### test_01_receivable_summary_output

**Category**: method_call  
**Description**: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: expected_data.update({'advance': 50.0, 'paid': 125.0, 'outstanding': 25.0, 'range1': 25.0, 'total_due': 25.0})  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

pe.save().submit()
expected_data.update({'advance': 50.0, 'paid': 125.0, 'outstanding': 25.0, 'range1': 25.0, 'total_due': 25.0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:103*

### test_01_receivable_summary_output

**Category**: method_call  
**Description**: Test for Invoices, Paid, Advance and Outstanding  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:112*

### test_02_various_filters_and_output

**Category**: method_call  
**Description**: test 02 various filters and output  
**Expected**: self.assertDictEqual(rpt_output[0], expected_data)  
**Confidence**: 0.85  

```python
# Setup
self.maxDiff = None
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(rpt_output), 1)
self.assertDictEqual(rpt_output[0], expected_data)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_receivable_summary/test_accounts_receivable_summary.py:172*

### test_match_by_account_number

**Category**: method_call  
**Description**: test match by account number  
**Expected**: self.assertEqual(doc.party, 'John Doe & Co.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'John Doe & Co.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:36*

### test_match_by_iban

**Category**: method_call  
**Description**: test match by iban  
**Expected**: self.assertEqual(doc.party, 'John Doe & Co.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'John Doe & Co.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:48*

### test_match_by_party_name

**Category**: method_call  
**Description**: test match by party name  
**Expected**: self.assertEqual(doc.party, 'Jackson Ella W.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'Jackson Ella W.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:59*

### test_match_by_description

**Category**: method_call  
**Description**: test match by description  
**Expected**: self.assertEqual(doc.party, 'Microsoft')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'Microsoft')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:70*

### test_skip_match_if_multiple_close_results

**Category**: method_call  
**Description**: test skip match if multiple close results  
**Expected**: self.assertEqual(doc.party, None)  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, None)
self.assertEqual(doc.party, None)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:85*

### test_match_by_account_number

**Category**: method_call  
**Description**: test match by account number  
**Expected**: self.assertEqual(doc.party, 'John Doe & Co.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'John Doe & Co.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:36*

### test_match_by_iban

**Category**: method_call  
**Description**: test match by iban  
**Expected**: self.assertEqual(doc.party, 'John Doe & Co.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'John Doe & Co.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:48*

### test_match_by_party_name

**Category**: method_call  
**Description**: test match by party name  
**Expected**: self.assertEqual(doc.party, 'Jackson Ella W.')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'Jackson Ella W.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:59*

### test_match_by_description

**Category**: method_call  
**Description**: test match by description  
**Expected**: self.assertEqual(doc.party, 'Microsoft')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, 'Supplier')
self.assertEqual(doc.party, 'Microsoft')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:70*

### test_skip_match_if_multiple_close_results

**Category**: method_call  
**Description**: test skip match if multiple close results  
**Expected**: self.assertEqual(doc.party, None)  
**Confidence**: 0.85  

```python
self.assertEqual(doc.party_type, None)
self.assertEqual(doc.party, None)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_auto_match_party.py:85*

### test_bank_clearance

**Category**: method_call  
**Description**: test bank clearance  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 1)  
**Confidence**: 0.85  

```python
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:43*

### test_bank_clearance_with_loan

**Category**: method_call  
**Description**: test bank clearance with loan  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 3)  
**Confidence**: 0.85  

```python
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:96*

### test_update_clearance_date_on_si

**Category**: method_call  
**Description**: test update clearance date on si  
**Expected**: self.assertNotEqual(len(bank_clearance.payment_entries), 0)  
**Confidence**: 0.85  

```python
bank_clearance.get_payment_entries()
self.assertNotEqual(len(bank_clearance.payment_entries), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:108*

### test_bank_clearance

**Category**: method_call  
**Description**: test bank clearance  
**Expected**: self.assertEqual(len(bank_clearance.payment_entries), 1)  
**Confidence**: 0.85  

```python
bank_clearance.get_payment_entries()
self.assertEqual(len(bank_clearance.payment_entries), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_clearance/test_bank_clearance.py:43*

### test_accounting_period_exempted_role

**Category**: method_call  
**Description**: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.85  

```python
doc.submit()
self.assertEqual(doc.docstatus, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:89*

### test_accounting_period_exempted_role

**Category**: method_call  
**Description**: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.85  

```python
doc.submit()
self.assertEqual(doc.docstatus, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:89*

### test_allowed_dimension_validation

**Category**: method_call  
**Description**: test allowed dimension validation  
**Expected**: self.assertRaises(InvalidAccountDimensionError, si.submit)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si.save()
self.assertRaises(InvalidAccountDimensionError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:29*

### test_mandatory_dimension_validation

**Category**: method_call  
**Description**: test mandatory dimension validation  
**Expected**: self.assertRaises(MandatoryAccountDimensionError, si.submit)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si.save()
self.assertRaises(MandatoryAccountDimensionError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:42*

### test_allowed_dimension_validation

**Category**: method_call  
**Description**: test allowed dimension validation  
**Expected**: self.assertRaises(InvalidAccountDimensionError, si.submit)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
si.save()
self.assertRaises(InvalidAccountDimensionError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:29*

### test_mandatory_dimension_validation

**Category**: method_call  
**Description**: test mandatory dimension validation  
**Expected**: self.assertRaises(MandatoryAccountDimensionError, si.submit)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
si.save()
self.assertRaises(MandatoryAccountDimensionError, si.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:42*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertIn('My Bank', name_and_total)  
**Confidence**: 0.85  

```python
self.assertNotIn('Sales', name_and_total)
self.assertIn('My Bank', name_and_total)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:91*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertEqual(name_and_total['My Bank'], 1100)  
**Confidence**: 0.85  

```python
self.assertIn('My Bank', name_and_total)
self.assertEqual(name_and_total['My Bank'], 1100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:93*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertIn('VAT Liabilities', name_and_total)  
**Confidence**: 0.85  

```python
self.assertEqual(name_and_total['My Bank'], 1100)
self.assertIn('VAT Liabilities', name_and_total)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:94*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertEqual(name_and_total['VAT Liabilities'], 10)  
**Confidence**: 0.85  

```python
self.assertIn('VAT Liabilities', name_and_total)
self.assertEqual(name_and_total['VAT Liabilities'], 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:96*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertIn('Advance VAT Paid', name_and_total)  
**Confidence**: 0.85  

```python
self.assertEqual(name_and_total['VAT Liabilities'], 10)
self.assertIn('Advance VAT Paid', name_and_total)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:97*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertEqual(name_and_total['Advance VAT Paid'], -10)  
**Confidence**: 0.85  

```python
self.assertIn('Advance VAT Paid', name_and_total)
self.assertEqual(name_and_total['Advance VAT Paid'], -10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:99*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertIn('Duties and Taxes', name_and_total)  
**Confidence**: 0.85  

```python
self.assertEqual(name_and_total['Advance VAT Paid'], -10)
self.assertIn('Duties and Taxes', name_and_total)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:100*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertEqual(name_and_total['Duties and Taxes'], 0)  
**Confidence**: 0.85  

```python
self.assertIn('Duties and Taxes', name_and_total)
self.assertEqual(name_and_total['Duties and Taxes'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:102*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertIn('Application of Funds (Assets)', name_and_total)  
**Confidence**: 0.85  

```python
self.assertEqual(name_and_total['Duties and Taxes'], 0)
self.assertIn('Application of Funds (Assets)', name_and_total)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:103*

### test_balance_sheet

**Category**: method_call  
**Description**: test balance sheet  
**Expected**: self.assertEqual(name_and_total['Application of Funds (Assets)'], 1100)  
**Confidence**: 0.85  

```python
self.assertIn('Application of Funds (Assets)', name_and_total)
self.assertEqual(name_and_total['Application of Funds (Assets)'], 1100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/balance_sheet/test_balance_sheet.py:105*

### test_rename_entries

**Category**: method_call  
**Description**: test rename entries  
**Expected**: self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))  
**Confidence**: 0.85  

```python
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:70*

### test_validate_account_party_type_shareholder

**Category**: method_call  
**Description**: test validate account party type shareholder  
**Expected**: self.assertEqual(1, jv.docstatus)  
**Confidence**: 0.85  

```python
jv.save().submit()
self.assertEqual(1, jv.docstatus)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:140*

### test_rename_entries

**Category**: method_call  
**Description**: test rename entries  
**Expected**: self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))  
**Confidence**: 0.85  

```python
self.assertTrue(all((entry.to_rename == 0 for entry in new_gl_entries)))
self.assertTrue(all((new.name != old.name for new, old in zip(gl_entries, new_gl_entries, strict=False))))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:70*

### test_validate_account_party_type_shareholder

**Category**: method_call  
**Description**: test validate account party type shareholder  
**Expected**: self.assertEqual(1, jv.docstatus)  
**Confidence**: 0.85  

```python
jv.save().submit()
self.assertEqual(1, jv.docstatus)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/gl_entry/test_gl_entry.py:140*

### test_purchase_register

**Category**: method_call  
**Description**: test purchase register  
**Expected**: self.assertEqual(first_row.voucher_no, pi.name)  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.voucher_type, 'Purchase Invoice')
self.assertEqual(first_row.voucher_no, pi.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:22*

### test_purchase_register

**Category**: method_call  
**Description**: test purchase register  
**Expected**: self.assertEqual(first_row.payable_account, 'Creditors - _TC6')  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.voucher_no, pi.name)
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:23*

### test_purchase_register

**Category**: method_call  
**Description**: test purchase register  
**Expected**: self.assertEqual(first_row.net_total, 1000)  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.payable_account, 'Creditors - _TC6')
self.assertEqual(first_row.net_total, 1000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:24*

### test_purchase_register

**Category**: method_call  
**Description**: test purchase register  
**Expected**: self.assertEqual(first_row.total_tax, 100)  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.net_total, 1000)
self.assertEqual(first_row.total_tax, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:25*

### test_purchase_register

**Category**: method_call  
**Description**: test purchase register  
**Expected**: self.assertEqual(first_row.grand_total, 1100)  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.total_tax, 100)
self.assertEqual(first_row.grand_total, 1100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:26*

### test_purchase_register_ledger_view

**Category**: method_call  
**Description**: test purchase register ledger view  
**Expected**: self.assertEqual(first_row.voucher_no, pe.name)  
**Confidence**: 0.85  

```python
self.assertEqual(first_row.voucher_type, 'Payment Entry')
self.assertEqual(first_row.voucher_no, pe.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/purchase_register/test_purchase_register.py:46*

### test_01_revaluation_of_forex_balance

**Category**: method_call  
**Description**: Test Forex account balance and Journal creation post Revaluation  
**Expected**: self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

je.reload()
self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:81*

### test_01_revaluation_of_forex_balance

**Category**: method_call  
**Description**: Test Forex account balance and Journal creation post Revaluation  
**Expected**: self.assertEqual(je.total_debit, 8500.0)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

self.assertEqual(je.voucher_type, 'Exchange Rate Revaluation')
self.assertEqual(je.total_debit, 8500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:82*

### test_01_revaluation_of_forex_balance

**Category**: method_call  
**Description**: Test Forex account balance and Journal creation post Revaluation  
**Expected**: self.assertEqual(je.total_credit, 8500.0)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

self.assertEqual(je.total_debit, 8500.0)
self.assertEqual(je.total_credit, 8500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:83*

### test_02_accounts_only_with_base_currency_balance

**Category**: method_call  
**Description**: Test Revaluation on Forex account with balance only in base currency  
**Expected**: self.assertEqual(je.voucher_type, 'Exchange Gain Or Loss')  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

je.reload()
self.assertEqual(je.voucher_type, 'Exchange Gain Or Loss')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:141*

### test_02_accounts_only_with_base_currency_balance

**Category**: method_call  
**Description**: Test Revaluation on Forex account with balance only in base currency  
**Expected**: self.assertEqual(len(je.accounts), 2)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

self.assertEqual(je.voucher_type, 'Exchange Gain Or Loss')
self.assertEqual(len(je.accounts), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:142*

### test_02_accounts_only_with_base_currency_balance

**Category**: method_call  
**Description**: Test Revaluation on Forex account with balance only in base currency  
**Expected**: self.assertEqual(je.total_credit, 500.0)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_item()
self.create_customer()
self.clear_old_entries()
self.set_system_and_company_settings()

self.assertEqual(je.total_debit, 500.0)
self.assertEqual(je.total_credit, 500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/exchange_rate_revaluation/test_exchange_rate_revaluation.py:149*

### test_get_mode_of_payments

**Category**: method_call  
**Description**: test get mode of payments  
**Expected**: self.assertTrue('Cash' in next(iter(mop.values())))  
**Confidence**: 0.85  

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:55*

### test_get_mode_of_payments

**Category**: method_call  
**Description**: test get mode of payments  
**Expected**: self.assertTrue('Cash' not in next(iter(mop.values())))  
**Confidence**: 0.85  

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' not in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:69*

### test_get_mode_of_payments

**Category**: method_call  
**Description**: test get mode of payments  
**Expected**: self.assertTrue('Cash' in next(iter(mop.values())))  
**Confidence**: 0.85  

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:55*

### test_get_mode_of_payments

**Category**: method_call  
**Description**: test get mode of payments  
**Expected**: self.assertTrue('Cash' not in next(iter(mop.values())))  
**Confidence**: 0.85  

```python
self.assertTrue('Credit Card' in next(iter(mop.values())))
self.assertTrue('Cash' not in next(iter(mop.values())))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:69*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: method_call  
**Description**: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('currency'), 'USD')  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_supplier(currency='USD', supplier_name='Test Supplier2')
self.create_usd_payable_account()

self.assertEqual(data[1][0].get('outstanding'), 300)
self.assertEqual(data[1][0].get('currency'), 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:38*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: method_call  
**Description**: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('currency'), 'USD')  
**Confidence**: 0.85  

```python
self.assertEqual(data[1][0].get('outstanding'), 300)
self.assertEqual(data[1][0].get('currency'), 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:38*

### test_single_company_report

**Category**: method_call  
**Description**: test single company report  
**Expected**: self.assertEqual(total_row['closing_credit'], 100000)  
**Confidence**: 0.85  

```python
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertEqual(total_row['closing_credit'], 100000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:59*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: method_call  
**Description**: test child company with different default currency from parent company  
**Expected**: self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)  
**Confidence**: 0.85  

```python
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:95*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: method_call  
**Description**: test child company with different default currency from parent company  
**Expected**: self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))  
**Confidence**: 0.85  

```python
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:96*

### test_single_company_report

**Category**: method_call  
**Description**: test single company report  
**Expected**: self.assertEqual(total_row['closing_credit'], 100000)  
**Confidence**: 0.85  

```python
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertEqual(total_row['closing_credit'], 100000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:59*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: method_call  
**Description**: test child company with different default currency from parent company  
**Expected**: self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)  
**Confidence**: 0.85  

```python
self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:95*

### test_child_company_with_different_default_currency_from_parent_company

**Category**: method_call  
**Description**: test child company with different default currency from parent company  
**Expected**: self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))  
**Confidence**: 0.85  

```python
self.assertNotEqual(total_row['closing_credit'], ccu_total_credit)
self.assertEqual(total_row['closing_credit'], flt(100000 + ccu_total_credit))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:96*

### test_closing_entry

**Category**: method_call  
**Description**: test closing entry  
**Expected**: self.assertEqual(pcv.gle_processing_status, 'Completed')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

pcv.reload()
self.assertEqual(pcv.gle_processing_status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:67*

### test_closing_entry

**Category**: method_call  
**Description**: test closing entry  
**Expected**: self.assertEqual(pcv_gle, expected_gle)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Accounts Settings', 'use_legacy_controller_for_pcv', 1)

self.assertEqual(pcv.gle_processing_status, 'Completed')
self.assertEqual(pcv_gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/period_closing_voucher/test_period_closing_voucher.py:68*

### test_loyalty_points_earned_single_tier

**Category**: method_call  
**Description**: test loyalty points earned single tier  
**Expected**: self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(si_original.get('loyalty_program'), customer.loyalty_program)
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:42*

### test_loyalty_points_earned_single_tier

**Category**: method_call  
**Description**: test loyalty points earned single tier  
**Expected**: self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)  
**Confidence**: 0.85  
**Tags**: unittest  

```python
self.assertEqual(lpe.get('loyalty_program_tier'), 'Bronce')
self.assertEqual(lpe.get('loyalty_program_tier'), customer.loyalty_program_tier)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_program/test_loyalty_program.py:43*

### test_so_advance_paid_and_currency_with_payment

**Category**: method_call  
**Description**: test so advance paid and currency with payment  
**Expected**: self.assertEqual(so.advance_paid, 100)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

so.reload()
self.assertEqual(so.advance_paid, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:89*

### test_so_advance_paid_and_currency_with_payment

**Category**: method_call  
**Description**: test so advance paid and currency with payment  
**Expected**: self.assertEqual(so.party_account_currency, 'USD')  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_usd_receivable_account()
self.create_usd_payable_account()
self.create_item()
self.clear_old_entries()

self.assertEqual(so.advance_paid, 100)
self.assertEqual(so.party_account_currency, 'USD')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/advance_payment_ledger_entry/test_advance_payment_ledger_entry.py:90*

### test_promotional_scheme

**Category**: method_call  
**Description**: test promotional scheme  
**Expected**: self.assertTrue(price_doc_details.min_qty, 4)  
**Confidence**: 0.85  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

self.assertTrue(price_doc_details.customer, '_Test Customer')
self.assertTrue(price_doc_details.min_qty, 4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:27*

### test_promotional_scheme

**Category**: method_call  
**Description**: test promotional scheme  
**Expected**: self.assertTrue(price_doc_details.discount_percentage, 20)  
**Confidence**: 0.85  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

self.assertTrue(price_doc_details.min_qty, 4)
self.assertTrue(price_doc_details.discount_percentage, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:28*

### test_promotional_scheme

**Category**: method_call  
**Description**: test promotional scheme  
**Expected**: self.assertTrue(price_doc_details.min_qty, 6)  
**Confidence**: 0.85  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

self.assertTrue(price_doc_details.customer, '_Test Customer 2')
self.assertTrue(price_doc_details.min_qty, 6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:44*

### test_promotional_scheme

**Category**: method_call  
**Description**: test promotional scheme  
**Expected**: self.assertTrue(price_doc_details.discount_percentage, 20)  
**Confidence**: 0.85  

```python
# Setup
if frappe.db.exists('Promotional Scheme', '_Test Scheme'):
    frappe.delete_doc('Promotional Scheme', '_Test Scheme')

self.assertTrue(price_doc_details.min_qty, 6)
self.assertTrue(price_doc_details.discount_percentage, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/promotional_scheme/test_promotional_scheme.py:45*

### test_process_soa_for_gl

**Category**: method_call  
**Description**: Tests the utils for Statement of Accounts(General Ledger)  
**Expected**: self.assertIn('_Test Customer', statement_dict)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

self.assertIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:40*

### test_process_soa_for_gl

**Category**: method_call  
**Description**: Tests the utils for Statement of Accounts(General Ledger)  
**Expected**: self.assertEqual(receivable_entries[1].voucher_no, self.si.name)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

self.assertEqual(len(receivable_entries), 4)
self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:46*

### test_process_soa_for_gl

**Category**: method_call  
**Description**: Tests the utils for Statement of Accounts(General Ledger)  
**Expected**: self.assertEqual(receivable_entries[1].balance, 100)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

self.assertEqual(receivable_entries[1].voucher_no, self.si.name)
self.assertEqual(receivable_entries[1].balance, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:49*

### test_process_soa_for_ar

**Category**: method_call  
**Description**: Tests the utils for Statement of Accounts(Accounts Receivable)  
**Expected**: self.assertIn('_Test Customer', statement_dict)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_customer(customer_name='Other Customer')
self.clear_old_entries()
self.si = create_sales_invoice()
create_sales_invoice(customer='Other Customer')

self.assertNotIn('Other Customer', statement_dict)
self.assertIn('_Test Customer', statement_dict)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_statement_of_accounts/test_process_statement_of_accounts.py:58*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: method_call  
**Description**: test customer ledger ignore cr dr filter  
**Expected**: self.assertDictEqual(expected, data[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(data), 1)
self.assertDictEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:210*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: method_call  
**Description**: test customer ledger ignore cr dr filter  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.clear_old_entries()

self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:238*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: method_call  
**Description**: test customer ledger ignore cr dr filter  
**Expected**: self.assertDictEqual(expected, data[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertDictEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:210*

### test_customer_ledger_ignore_cr_dr_filter

**Category**: method_call  
**Description**: test customer ledger ignore cr dr filter  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/customer_ledger_summary/test_customer_ledger_summary.py:238*

### test_pos_opening_entry

**Category**: method_call  
**Description**: test pos opening entry  
**Expected**: self.assertNotEqual(opening_entry.docstatus, 0)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

self.assertEqual(opening_entry.status, 'Open')
self.assertNotEqual(opening_entry.docstatus, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:39*

### test_multiple_pos_opening_entry_for_multiple_pos_profiles

**Category**: method_call  
**Description**: test multiple pos opening entry for multiple pos profiles  
**Expected**: self.assertEqual(opening_entry_1.user, test_user.name)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

self.assertEqual(opening_entry_1.status, 'Open')
self.assertEqual(opening_entry_1.user, test_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:60*

### test_multiple_pos_opening_entry_for_multiple_pos_profiles

**Category**: method_call  
**Description**: test multiple pos opening entry for multiple pos profiles  
**Expected**: self.assertEqual(opening_entry_2.user, cashier_user.name)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

self.assertEqual(opening_entry_2.status, 'Open')
self.assertEqual(opening_entry_2.user, cashier_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:69*

### test_cancel_pos_opening_entry_without_invoices

**Category**: method_call  
**Description**: test cancel pos opening entry without invoices  
**Expected**: self.assertEqual(opening_entry.status, 'Cancelled')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

opening_entry.cancel()
self.assertEqual(opening_entry.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:95*

### test_cancel_pos_opening_entry_without_invoices

**Category**: method_call  
**Description**: test cancel pos opening entry without invoices  
**Expected**: self.assertNotEqual(opening_entry.docstatus, 1)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

self.assertEqual(opening_entry.status, 'Cancelled')
self.assertNotEqual(opening_entry.docstatus, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:96*

### test_cancel_pos_opening_entry_with_invoice

**Category**: method_call  
**Description**: test cancel pos opening entry with invoice  
**Expected**: self.assertRaises(frappe.ValidationError, opening_entry.cancel)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.sql('delete from `tabPOS Opening Entry`')
make_stock_entry(target='_Test Warehouse - _TC', qty=2, basic_rate=100)
from erpnext.accounts.doctype.pos_closing_entry.test_pos_closing_entry import init_user_and_profile
self.init_user_and_profile = init_user_and_profile

pos_inv1.submit()
self.assertRaises(frappe.ValidationError, opening_entry.cancel)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:106*

### test_pos_opening_entry

**Category**: method_call  
**Description**: test pos opening entry  
**Expected**: self.assertNotEqual(opening_entry.docstatus, 0)  
**Confidence**: 0.85  

```python
self.assertEqual(opening_entry.status, 'Open')
self.assertNotEqual(opening_entry.docstatus, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:39*

### test_multiple_pos_opening_entry_for_multiple_pos_profiles

**Category**: method_call  
**Description**: test multiple pos opening entry for multiple pos profiles  
**Expected**: self.assertEqual(opening_entry_1.user, test_user.name)  
**Confidence**: 0.85  

```python
self.assertEqual(opening_entry_1.status, 'Open')
self.assertEqual(opening_entry_1.user, test_user.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_opening_entry/test_pos_opening_entry.py:60*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(doc.loyalty_points, 75)  
**Confidence**: 0.85  

```python
doc.insert(ignore_permissions=True)
self.assertEqual(doc.loyalty_points, 75)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:61*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(doc.discretionary_reason, 'Customer Appreciation')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.loyalty_points, 75)
self.assertEqual(doc.discretionary_reason, 'Customer Appreciation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:62*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(entry.discretionary_reason, 'Customer Appreciation')  
**Confidence**: 0.85  

```python
self.assertEqual(entry.loyalty_points, 75)
self.assertEqual(entry.discretionary_reason, 'Customer Appreciation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:67*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(doc.loyalty_points, 75)  
**Confidence**: 0.85  

```python
doc.insert(ignore_permissions=True)
self.assertEqual(doc.loyalty_points, 75)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:61*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(doc.discretionary_reason, 'Customer Appreciation')  
**Confidence**: 0.85  

```python
self.assertEqual(doc.loyalty_points, 75)
self.assertEqual(doc.discretionary_reason, 'Customer Appreciation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:62*

### test_add_loyalty_points_with_discretionary_reason

**Category**: method_call  
**Description**: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(entry.discretionary_reason, 'Customer Appreciation')  
**Confidence**: 0.85  

```python
self.assertEqual(entry.loyalty_points, 75)
self.assertEqual(entry.discretionary_reason, 'Customer Appreciation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:67*

### test_merge_success

**Category**: method_call  
**Description**: test merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))  
**Confidence**: 0.85  

```python
self.assertEqual(parent, 'Indirect Expenses - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:51*

### test_partial_merge_success

**Category**: method_call  
**Description**: test partial merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))  
**Confidence**: 0.85  

```python
self.assertEqual(parent, 'Indirect Income - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:99*

### test_partial_merge_success

**Category**: method_call  
**Description**: test partial merge success  
**Expected**: self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))  
**Confidence**: 0.85  

```python
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:101*

### test_merge_success

**Category**: method_call  
**Description**: test merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))  
**Confidence**: 0.85  

```python
self.assertEqual(parent, 'Indirect Expenses - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Expenses - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:51*

### test_partial_merge_success

**Category**: method_call  
**Description**: test partial merge success  
**Expected**: self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))  
**Confidence**: 0.85  

```python
self.assertEqual(parent, 'Indirect Income - _TC')
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:99*

### test_partial_merge_success

**Category**: method_call  
**Description**: test partial merge success  
**Expected**: self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))  
**Confidence**: 0.85  

```python
self.assertFalse(frappe.db.exists('Account', 'Indirect Test Income - _TC'))
self.assertTrue(frappe.db.exists('Account', 'Administrative Test Income - _TC'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_merge/test_ledger_merge.py:101*

### test_sales_order_with_coupon_code

**Category**: method_call  
**Description**: test sales order with coupon code  
**Expected**: self.assertEqual(so.items[0].rate, 3500)  
**Confidence**: 0.85  

```python
# Setup
test_create_test_data()

so.save()
self.assertEqual(so.items[0].rate, 3500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:137*

### test_sales_order_with_coupon_code

**Category**: method_call  
**Description**: test sales order with coupon code  
**Expected**: self.assertEqual(frappe.db.get_value('Coupon Code', 'SAVE30', 'used'), 1)  
**Confidence**: 0.85  

```python
# Setup
test_create_test_data()

so.submit()
self.assertEqual(frappe.db.get_value('Coupon Code', 'SAVE30', 'used'), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:142*

### test_coupon_without_max_use

**Category**: method_call  
**Description**: test coupon without max use  
**Expected**: self.assertEqual(coupon.used, 0)  
**Confidence**: 0.85  

```python
# Setup
test_create_test_data()

coupon.insert(ignore_permissions=True)
self.assertEqual(coupon.used, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:162*

### test_coupon_without_max_use

**Category**: method_call  
**Description**: test coupon without max use  
**Expected**: self.assertEqual(coupon.maximum_use, 0)  
**Confidence**: 0.85  

```python
# Setup
test_create_test_data()

self.assertEqual(coupon.used, 0)
self.assertEqual(coupon.maximum_use, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:165*

### test_sales_order_with_coupon_code

**Category**: method_call  
**Description**: test sales order with coupon code  
**Expected**: self.assertEqual(so.items[0].rate, 3500)  
**Confidence**: 0.85  

```python
so.save()
self.assertEqual(so.items[0].rate, 3500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:137*

### test_sales_order_with_coupon_code

**Category**: method_call  
**Description**: test sales order with coupon code  
**Expected**: self.assertEqual(frappe.db.get_value('Coupon Code', 'SAVE30', 'used'), 1)  
**Confidence**: 0.85  

```python
so.submit()
self.assertEqual(frappe.db.get_value('Coupon Code', 'SAVE30', 'used'), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:142*

### test_coupon_without_max_use

**Category**: method_call  
**Description**: test coupon without max use  
**Expected**: self.assertEqual(coupon.used, 0)  
**Confidence**: 0.85  

```python
coupon.insert(ignore_permissions=True)
self.assertEqual(coupon.used, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:162*

### test_coupon_without_max_use

**Category**: method_call  
**Description**: test coupon without max use  
**Expected**: self.assertEqual(coupon.maximum_use, 0)  
**Confidence**: 0.85  

```python
self.assertEqual(coupon.used, 0)
self.assertEqual(coupon.maximum_use, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:165*

### test_debit_credit_mismatch

**Category**: method_call  
**Description**: test debit credit mismatch  
**Expected**: self.assertEqual(expected, actual[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

self.assertEqual(len(actual), 1)
self.assertEqual(expected, actual[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:82*

### test_gl_and_pl_mismatch

**Category**: method_call  
**Description**: test gl and pl mismatch  
**Expected**: self.assertEqual(expected, actual[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

self.assertEqual(len(actual), 1)
self.assertEqual(expected, actual[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:108*

### test_debit_credit_mismatch

**Category**: method_call  
**Description**: test debit credit mismatch  
**Expected**: self.assertEqual(expected, actual[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(actual), 1)
self.assertEqual(expected, actual[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:82*

### test_gl_and_pl_mismatch

**Category**: method_call  
**Description**: test gl and pl mismatch  
**Expected**: self.assertEqual(expected, actual[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(actual), 1)
self.assertEqual(expected, actual[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:108*

### test_company_fiscal_year_overlap

**Category**: method_call  
**Description**: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))  
**Confidence**: 0.85  

```python
company_fy.insert()
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:44*

### test_company_fiscal_year_overlap

**Category**: method_call  
**Description**: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))  
**Confidence**: 0.85  

```python
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:45*

### test_company_fiscal_year_overlap

**Category**: method_call  
**Description**: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))  
**Confidence**: 0.85  

```python
company_fy.insert()
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:44*

### test_company_fiscal_year_overlap

**Category**: method_call  
**Description**: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))  
**Confidence**: 0.85  

```python
self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))
self.assertTrue(frappe.db.exists('Fiscal Year', company_fy.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:45*

### test_cancel_voucher

**Category**: method_call  
**Description**: test cancel voucher  
**Expected**: self.assertEqual(bank_transaction.docstatus, DocStatus.submitted())  
**Confidence**: 0.85  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

bank_transaction.reload()
self.assertEqual(bank_transaction.docstatus, DocStatus.submitted())
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:105*

### test_cancel_voucher

**Category**: method_call  
**Description**: test cancel voucher  
**Expected**: self.assertEqual(bank_transaction.unallocated_amount, 1700)  
**Confidence**: 0.85  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

self.assertEqual(bank_transaction.docstatus, DocStatus.submitted())
self.assertEqual(bank_transaction.unallocated_amount, 1700)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:106*

### test_cancel_voucher

**Category**: method_call  
**Description**: test cancel voucher  
**Expected**: self.assertEqual(bank_transaction.payment_entries, [])  
**Confidence**: 0.85  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

self.assertEqual(bank_transaction.unallocated_amount, 1700)
self.assertEqual(bank_transaction.payment_entries, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:107*

### test_clear_sales_invoice

**Category**: method_call  
**Description**: test clear sales invoice  
**Expected**: self.assertEqual(frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount'), 0)  
**Confidence**: 0.85  

```python
# Setup
make_pos_profile()
uniq_identifier = frappe.generate_hash(length=10)
gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
bank_account = create_bank_account(gl_account=gl_account, bank_account_name='Checking Account ' + uniq_identifier)
add_transactions(bank_account=bank_account)
add_vouchers(gl_account=gl_account)

reconcile_vouchers(bank_transaction.name, vouchers=vouchers)
self.assertEqual(frappe.db.get_value('Bank Transaction', bank_transaction.name, 'unallocated_amount'), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_transaction/test_bank_transaction.py:179*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')  
**Confidence**: 0.85  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

self.assertEqual(reference_doc.reference_name, payment_entry.name)
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:45*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.supplier, '_Test Supplier')  
**Confidence**: 0.85  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
self.assertEqual(reference_doc.supplier, '_Test Supplier')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:46*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.amount, 250)  
**Confidence**: 0.85  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

self.assertEqual(reference_doc.supplier, '_Test Supplier')
self.assertEqual(reference_doc.amount, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:47*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')  
**Confidence**: 0.85  

```python
self.assertEqual(reference_doc.reference_name, payment_entry.name)
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:45*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.supplier, '_Test Supplier')  
**Confidence**: 0.85  

```python
self.assertEqual(reference_doc.reference_doctype, 'Payment Entry')
self.assertEqual(reference_doc.supplier, '_Test Supplier')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:46*

### test_payment_order_creation_against_payment_entry

**Category**: method_call  
**Description**: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.amount, 250)  
**Confidence**: 0.85  

```python
self.assertEqual(reference_doc.supplier, '_Test Supplier')
self.assertEqual(reference_doc.amount, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:47*

### test_auto_reconcile

**Category**: method_call  
**Description**: test auto reconcile  
**Expected**: self.assertEqual(transactions[0].name, bank_transaction.name)  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.create_customer()
self.clear_old_entries()
bank_dt = qb.DocType('Bank')
qb.from_(bank_dt).delete().where(bank_dt.name == 'HDFC').run()
self.create_bank_account()

self.assertEqual(len(transactions), 1)
self.assertEqual(transactions[0].name, bank_transaction.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:87*

### test_auto_reconcile

**Category**: method_call  
**Description**: test auto reconcile  
**Expected**: self.assertEqual(transactions[0].name, bank_transaction.name)  
**Confidence**: 0.85  

```python
self.assertEqual(len(transactions), 1)
self.assertEqual(transactions[0].name, bank_transaction.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:87*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.cleanup()

self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:63*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.cleanup()

self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:73*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
# Setup
self.create_company()
self.cleanup()

self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:89*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:63*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:73*

### test_01_basic_report_functionality

**Category**: method_call  
**Description**: test 01 basic report functionality  
**Expected**: self.assertEqual(expected, data[0])  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(expected, data[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:89*

### test_update_reference_in_payment_entry

**Category**: method_call  
**Description**: test update reference in payment entry  
**Expected**: self.assertEqual(payment_entry.deductions[0].amount, -4855.0)  
**Confidence**: 0.85  

```python
payment_entry.save()
self.assertEqual(payment_entry.deductions[0].amount, -4855.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:93*

### test_update_reference_in_payment_entry

**Category**: method_call  
**Description**: test update reference in payment entry  
**Expected**: self.assertEqual(payment_entry.deductions, [])  
**Confidence**: 0.85  

```python
payment_entry.save()
self.assertEqual(payment_entry.deductions, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:99*

### test_update_reference_in_payment_entry

**Category**: method_call  
**Description**: test update reference in payment entry  
**Expected**: self.assertEqual(len(payment_entry.references), 1)  
**Confidence**: 0.85  

```python
payment_entry.load_from_db()
self.assertEqual(len(payment_entry.references), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:127*

### test_update_reference_in_payment_entry

**Category**: method_call  
**Description**: test update reference in payment entry  
**Expected**: self.assertEqual(payment_entry.difference_amount, 0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(payment_entry.references), 1)
self.assertEqual(payment_entry.difference_amount, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test/test_utils.py:128*

### test_dimension_against_sales_invoice

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test dimension against sales invoice  
**Expected**: self.assertEqual(gle.get('department'), '_Test Department - _TC')  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

si = create_sales_invoice(do_not_save=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:18*

### test_dimension_against_sales_invoice

**Category**: instantiation  
**Description**: Instantiate get_doc: test dimension against sales invoice  
**Expected**: self.assertEqual(gle.get('department'), '_Test Department - _TC')  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

gle = frappe.get_doc('GL Entry', {'voucher_no': si.name, 'account': 'Sales - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:39*

### test_dimension_against_journal_entry

**Category**: instantiation  
**Description**: Instantiate make_journal_entry: test dimension against journal entry  
**Expected**: self.assertEqual(gle.get('department'), '_Test Department - _TC')  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

je = make_journal_entry('Sales - _TC', 'Sales Expenses - _TC', 500, save=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:44*

### test_dimension_against_journal_entry

**Category**: instantiation  
**Description**: Instantiate get_doc: test dimension against journal entry  
**Expected**: self.assertEqual(gle.get('department'), '_Test Department - _TC')  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

gle = frappe.get_doc('GL Entry', {'voucher_no': je.name, 'account': 'Sales - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:54*

### test_dimension_against_journal_entry

**Category**: instantiation  
**Description**: Instantiate get_doc: test dimension against journal entry  
**Expected**: self.assertEqual(gle.get('department'), '_Test Department - _TC')  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

gle1 = frappe.get_doc('GL Entry', {'voucher_no': je.name, 'account': 'Sales Expenses - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:55*

### test_mandatory

**Category**: instantiation  
**Description**: Instantiate get_doc: test mandatory  
**Expected**: self.assertRaises(frappe.ValidationError, si.submit)  
**Confidence**: 0.80  

```python
# Setup
create_dimension()

location = frappe.get_doc('Accounting Dimension', 'Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension/test_accounting_dimension.py:60*

### test_from_greater_than_to

**Category**: instantiation  
**Description**: Instantiate copy_doc: test from greater than to  
**Expected**: self.assertRaises(FromGreaterThanToError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule = frappe.copy_doc(self.globalTestRecords['Shipping Rule'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:16*

### test_from_greater_than_to

**Category**: instantiation  
**Description**: Instantiate get: test from greater than to  
**Expected**: self.assertRaises(FromGreaterThanToError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule.name = self.globalTestRecords['Shipping Rule'][0].get('name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:17*

### test_many_zero_to_values

**Category**: instantiation  
**Description**: Instantiate copy_doc: test many zero to values  
**Expected**: self.assertRaises(ManyBlankToValuesError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule = frappe.copy_doc(self.globalTestRecords['Shipping Rule'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:22*

### test_many_zero_to_values

**Category**: instantiation  
**Description**: Instantiate get: test many zero to values  
**Expected**: self.assertRaises(ManyBlankToValuesError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule.name = self.globalTestRecords['Shipping Rule'][0].get('name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:23*

### test_overlapping_conditions

**Category**: instantiation  
**Description**: Instantiate copy_doc: test overlapping conditions  
**Confidence**: 0.80  

```python
shipping_rule = frappe.copy_doc(self.globalTestRecords['Shipping Rule'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:35*

### test_overlapping_conditions

**Category**: instantiation  
**Description**: Instantiate get: test overlapping conditions  
**Confidence**: 0.80  

```python
shipping_rule.name = self.globalTestRecords['Shipping Rule'][0].get('name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:36*

### test_from_greater_than_to

**Category**: instantiation  
**Description**: Instantiate copy_doc: test from greater than to  
**Expected**: self.assertRaises(FromGreaterThanToError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule = frappe.copy_doc(self.globalTestRecords['Shipping Rule'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:16*

### test_from_greater_than_to

**Category**: instantiation  
**Description**: Instantiate get: test from greater than to  
**Expected**: self.assertRaises(FromGreaterThanToError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule.name = self.globalTestRecords['Shipping Rule'][0].get('name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:17*

### test_many_zero_to_values

**Category**: instantiation  
**Description**: Instantiate copy_doc: test many zero to values  
**Expected**: self.assertRaises(ManyBlankToValuesError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule = frappe.copy_doc(self.globalTestRecords['Shipping Rule'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:22*

### test_many_zero_to_values

**Category**: instantiation  
**Description**: Instantiate get: test many zero to values  
**Expected**: self.assertRaises(ManyBlankToValuesError, shipping_rule.insert)  
**Confidence**: 0.80  

```python
shipping_rule.name = self.globalTestRecords['Shipping Rule'][0].get('name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/shipping_rule/test_shipping_rule.py:23*

### test_overlap

**Category**: instantiation  
**Description**: Instantiate create_accounting_period: test overlap  
**Expected**: self.assertRaises(OverlapError, ap2.save)  
**Confidence**: 0.80  

```python
ap1 = create_accounting_period(start_date='2018-04-01', end_date='2018-06-30', company='Wind Power LLC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:19*

### test_overlap

**Category**: instantiation  
**Description**: Instantiate create_accounting_period: test overlap  
**Expected**: self.assertRaises(OverlapError, ap2.save)  
**Confidence**: 0.80  

```python
ap2 = create_accounting_period(start_date='2018-06-30', end_date='2018-07-10', company='Wind Power LLC', period_name='Test Accounting Period 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:24*

### test_accounting_period

**Category**: instantiation  
**Description**: Instantiate create_accounting_period: test accounting period  
**Expected**: self.assertRaises(ClosedAccountingPeriod, doc.save)  
**Confidence**: 0.80  

```python
ap1 = create_accounting_period(period_name='Test Accounting Period 2')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:33*

### test_accounting_period

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test accounting period  
**Expected**: self.assertRaises(ClosedAccountingPeriod, doc.save)  
**Confidence**: 0.80  

```python
doc = create_sales_invoice(do_not_save=1, cost_center='_Test Company - _TC', warehouse='Stores - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:36*

### test_accounting_period_exempted_role

**Category**: instantiation  
**Description**: Instantiate create_accounting_period: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.80  

```python
ap = create_accounting_period(period_name='Test Accounting Period Exempted', exempted_role='Accounts Manager', start_date='2025-12-01', end_date='2025-12-31')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:41*

### test_accounting_period_exempted_role

**Category**: instantiation  
**Description**: Instantiate get_all: test accounting period exempted role  
**Expected**: self.assertEqual(doc.docstatus, 1)  
**Confidence**: 0.80  

```python
users = frappe.get_all('User', filters={'email': ['like', 'test%']}, limit=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_period/test_accounting_period.py:50*

### test_allowed_dimension_validation

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test allowed dimension validation  
**Expected**: self.assertRaises(InvalidAccountDimensionError, si.submit)  
**Confidence**: 0.80  
**Tags**: unittest  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si = create_sales_invoice(do_not_save=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:25*

### test_mandatory_dimension_validation

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test mandatory dimension validation  
**Expected**: self.assertRaises(MandatoryAccountDimensionError, si.submit)  
**Confidence**: 0.80  
**Tags**: unittest  

```python
# Setup
create_dimension()
create_accounting_dimension_filter()
self.invoice_list = []

si = create_sales_invoice(do_not_save=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounting_dimension_filter/test_accounting_dimension_filter.py:35*

### test_gle_based_on_cost_center_allocation

**Category**: instantiation  
**Description**: Instantiate create_cost_center_allocation: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.80  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

cca = create_cost_center_allocation('_Test Company', 'Main Cost Center 1 - _TC', {'Sub Cost Center 1 - _TC': 60, 'Sub Cost Center 2 - _TC': 40})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:34*

### test_gle_based_on_cost_center_allocation

**Category**: instantiation  
**Description**: Instantiate make_journal_entry: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.80  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

jv = make_journal_entry('Cash - _TC', 'Sales - _TC', 100, cost_center='Main Cost Center 1 - _TC', submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:40*

### test_gle_based_on_cost_center_allocation

**Category**: instantiation  
**Description**: Instantiate DocType: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.80  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

gle = frappe.qb.DocType('GL Entry')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:46*

### test_gle_based_on_cost_center_allocation

**Category**: instantiation  
**Description**: Instantiate run: test gle based on cost center allocation  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.80  

```python
# Setup
cost_centers = ['Main Cost Center 1', 'Main Cost Center 2', 'Main Cost Center 3', 'Sub Cost Center 1', 'Sub Cost Center 2', 'Sub Cost Center 3']
for cc in cost_centers:
    create_cost_center(cost_center_name=cc, company='_Test Company')

gl_entries = frappe.qb.from_(gle).select(gle.cost_center, gle.debit, gle.credit).where(gle.voucher_type == 'Journal Entry').where(gle.voucher_no == jv.name).where(gle.account == 'Sales - _TC').orderby(gle.cost_center).run(as_dict=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center_allocation/test_cost_center_allocation.py:47*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate _dict: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:40*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate execute: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:41*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate _dict: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:40*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate execute: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:41*

### test_stale_days

**Category**: instantiation  
**Description**: Instantiate get_doc: test stale days  
**Expected**: self.assertRaises(frappe.ValidationError, cur_settings.save)  
**Confidence**: 0.80  

```python
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounts_settings/test_accounts_settings.py:14*

### test_stale_days

**Category**: instantiation  
**Description**: Instantiate get_doc: test stale days  
**Expected**: self.assertRaises(frappe.ValidationError, cur_settings.save)  
**Confidence**: 0.80  

```python
cur_settings = frappe.get_doc('Accounts Settings', 'Accounts Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/accounts_settings/test_accounts_settings.py:14*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate new_doc: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
# Setup
from erpnext.accounts.doctype.account.test_account import create_account
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_fiscal_year
self.company = create_company()
create_cost_center(cost_center_name='Test Cost Center', company='Trial Balance Company', parent_cost_center='Trial Balance Company - TBC')
create_account(account_name='Offsetting', company='Trial Balance Company', parent_account='Temporary Accounts - TBC')
self.fiscal_year = get_fiscal_year(today(), company='Trial Balance Company')[0]
create_accounting_dimension()

branch1 = frappe.new_doc('Branch')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:40*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate new_doc: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
# Setup
from erpnext.accounts.doctype.account.test_account import create_account
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_fiscal_year
self.company = create_company()
create_cost_center(cost_center_name='Test Cost Center', company='Trial Balance Company', parent_cost_center='Trial Balance Company - TBC')
create_account(account_name='Offsetting', company='Trial Balance Company', parent_account='Temporary Accounts - TBC')
self.fiscal_year = get_fiscal_year(today(), company='Trial Balance Company')[0]
create_accounting_dimension()

branch2 = frappe.new_doc('Branch')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:43*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
# Setup
from erpnext.accounts.doctype.account.test_account import create_account
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_fiscal_year
self.company = create_company()
create_cost_center(cost_center_name='Test Cost Center', company='Trial Balance Company', parent_cost_center='Trial Balance Company - TBC')
create_account(account_name='Offsetting', company='Trial Balance Company', parent_account='Temporary Accounts - TBC')
self.fiscal_year = get_fiscal_year(today(), company='Trial Balance Company')[0]
create_accounting_dimension()

si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:47*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate _dict: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
# Setup
from erpnext.accounts.doctype.account.test_account import create_account
from erpnext.accounts.doctype.cost_center.test_cost_center import create_cost_center
from erpnext.accounts.utils import get_fiscal_year
self.company = create_company()
create_cost_center(cost_center_name='Test Cost Center', company='Trial Balance Company', parent_cost_center='Trial Balance Company - TBC')
create_account(account_name='Offsetting', company='Trial Balance Company', parent_account='Temporary Accounts - TBC')
self.fiscal_year = get_fiscal_year(today(), company='Trial Balance Company')[0]
create_accounting_dimension()

filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:59*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate new_doc: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
branch1 = frappe.new_doc('Branch')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:40*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate new_doc: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
branch2 = frappe.new_doc('Branch')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:43*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
si = create_sales_invoice(company=self.company, debit_to='Debtors - TBC', cost_center='Test Cost Center - TBC', income_account='Sales - TBC', do_not_submit=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:47*

### test_offsetting_entries_for_accounting_dimensions

**Category**: instantiation  
**Description**: Instantiate _dict: Checks if Trial Balance Report is balanced when filtered using a particular Accounting Dimension  
**Expected**: self.assertEqual(total_row['debit'], total_row['credit'])  
**Confidence**: 0.80  

```python
filters = frappe._dict({'company': self.company, 'fiscal_year': self.fiscal_year, 'branch': ['Location 1']})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/trial_balance/test_trial_balance.py:59*

### test_supplier_ledger_summary_with_filters

**Category**: instantiation  
**Description**: Instantiate get_value: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:66*

### test_supplier_ledger_summary_with_filters

**Category**: instantiation  
**Description**: Instantiate get_value: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.80  

```python
supplier_group = frappe.db.get_value('Supplier', self.supplier, 'supplier_group')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:66*

### test_profit_and_loss_output_and_summary

**Category**: instantiation  
**Description**: Instantiate get_period_list: test profit and loss output and summary  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

period_list = get_period_list(filters.from_fiscal_year, filters.to_fiscal_year, filters.period_start_date, filters.period_end_date, filters.filter_based_on, filters.periodicity, company=filters.company)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:68*

### test_profit_and_loss_output_and_summary

**Category**: instantiation  
**Description**: Instantiate next: test profit and loss output and summary  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

current_period = next((x for x in period_list if x.from_date <= getdate() and x.to_date >= getdate()))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:79*

### test_p_and_l_export

**Category**: instantiation  
**Description**: Instantiate _dict: test p and l export  
**Expected**: self.assertIn(sales_account, contents)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

frappe.local.form_dict = frappe._dict({'report_name': 'Profit and Loss Statement', 'file_format_type': 'CSV', 'filters': filters, 'visible_idx': [0, 1, 2, 3, 4, 5, 6]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:99*

### test_p_and_l_export

**Category**: instantiation  
**Description**: Instantiate get_value: test p and l export  
**Expected**: self.assertIn(sales_account, contents)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

sales_account = frappe.db.get_value('Company', self.company, 'default_income_account')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/profit_and_loss_statement/test_profit_and_loss_statement.py:109*

### test_get_mode_of_payments

**Category**: instantiation  
**Description**: Instantiate get_mode_of_payments: test get mode of payments  
**Expected**: self.assertTrue('Credit Card' in next(iter(mop.values())))  
**Confidence**: 0.80  

```python
mop = get_mode_of_payments(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:54*

### test_get_mode_of_payments

**Category**: instantiation  
**Description**: Instantiate get_all: test get mode of payments  
**Expected**: self.assertTrue('Credit Card' in next(iter(mop.values())))  
**Confidence**: 0.80  

```python
payment_entries = frappe.get_all('Payment Entry', filters={'mode_of_payment': 'Cash', 'docstatus': 1}, fields=['name', 'docstatus'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:59*

### test_get_mode_of_payments

**Category**: instantiation  
**Description**: Instantiate get_mode_of_payments: test get mode of payments  
**Expected**: self.assertTrue('Credit Card' in next(iter(mop.values())))  
**Confidence**: 0.80  

```python
mop = get_mode_of_payments(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:68*

### test_get_mode_of_payments

**Category**: instantiation  
**Description**: Instantiate get_payment_entry: test get mode of payments  
**Confidence**: 0.80  

```python
pe = get_payment_entry('Sales Invoice', si.name, bank_account=bank_account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_payment_summary/test_sales_payment_summary.py:47*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: instantiation  
**Description**: Instantiate create_purchase_invoice: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_supplier(currency='USD', supplier_name='Test Supplier2')
self.create_usd_payable_account()

pi = self.create_purchase_invoice(do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:22*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: instantiation  
**Description**: Instantiate execute: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_supplier(currency='USD', supplier_name='Test Supplier2')
self.create_usd_payable_account()

data = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:37*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: instantiation  
**Description**: Instantiate create_purchase_invoice: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.80  

```python
pi = self.create_purchase_invoice(do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:22*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: instantiation  
**Description**: Instantiate execute: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.80  

```python
data = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:37*

### test_create_template

**Category**: instantiation  
**Description**: Instantiate get_doc: test create template  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:13*

### test_credit_days

**Category**: instantiation  
**Description**: Instantiate get_doc: test credit days  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 100.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': -30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:43*

### test_duplicate_terms

**Category**: instantiation  
**Description**: Instantiate get_doc: test duplicate terms  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}, {'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:61*

### test_create_template

**Category**: instantiation  
**Description**: Instantiate get_doc: test create template  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:13*

### test_credit_days

**Category**: instantiation  
**Description**: Instantiate get_doc: test credit days  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 100.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': -30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:43*

### test_duplicate_terms

**Category**: instantiation  
**Description**: Instantiate get_doc: test duplicate terms  
**Expected**: self.assertRaises(frappe.ValidationError, template.insert)  
**Confidence**: 0.80  

```python
template = frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Test', 'terms': [{'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}, {'doctype': 'Payment Terms Template Detail', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_terms_template/test_payment_terms_template.py:61*

### test_single_company_report

**Category**: instantiation  
**Description**: Instantiate _dict: test single company report  
**Expected**: self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])  
**Confidence**: 0.80  

```python
filters = frappe._dict({'company': ['Parent Group Company India'], 'fiscal_year': self.fiscal_year})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:54*

### test_single_company_report

**Category**: instantiation  
**Description**: Instantiate execute: test single company report  
**Expected**: self.assertEqual(total_row['closing_debit'], total_row['closing_credit'])  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/consolidated_trial_balance/test_consolidated_trial_balance.py:56*

### test_pos_profile

**Category**: instantiation  
**Description**: Instantiate get_doc: test pos profile  
**Confidence**: 0.80  

```python
doc = frappe.get_doc('POS Profile', pos_profile.get('name'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:22*

### test_pos_profile

**Category**: instantiation  
**Description**: Instantiate get_items_list: test pos profile  
**Confidence**: 0.80  

```python
items = get_items_list(doc, doc.company)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:26*

### test_pos_profile

**Category**: instantiation  
**Description**: Instantiate get_customers_list: test pos profile  
**Confidence**: 0.80  

```python
customers = get_customers_list(doc)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:27*

### test_pos_profile

**Category**: instantiation  
**Description**: Instantiate sql: test pos profile  
**Confidence**: 0.80  

```python
products_count = frappe.db.sql(" select count(name) from tabItem where item_group = '_Test Item Group'", as_list=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:29*

### test_pos_profile

**Category**: instantiation  
**Description**: Instantiate sql: test pos profile  
**Confidence**: 0.80  

```python
customers_count = frappe.db.sql(" select count(name) from tabCustomer where customer_group = '_Test Customer Group'")
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:32*

### test_disabled_pos_profile_creation

**Category**: instantiation  
**Description**: Instantiate get_doc: test disabled pos profile creation  
**Confidence**: 0.80  

```python
pos_profile = frappe.get_doc('POS Profile', '_Test POS Profile 001')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/pos_profile/test_pos_profile.py:44*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

si = self.create_sales_invoice(rate=98)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:57*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate _dict: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:59*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate execute: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:60*

### test_journal_with_cost_center_filter

**Category**: instantiation  
**Description**: Instantiate get_doc: test journal with cost center filter  
**Expected**: self.assertEqual(len(filtered_output), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

je1 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 77, 'credit': 77, 'is_advance': 'Yes', 'cost_center': self.cost_center}, {'account': self.cash, 'debit_in_account_currency': 77, 'debit': 77}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:79*

### test_journal_with_cost_center_filter

**Category**: instantiation  
**Description**: Instantiate get_doc: test journal with cost center filter  
**Expected**: self.assertEqual(len(filtered_output), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

je2 = frappe.get_doc({'doctype': 'Journal Entry', 'voucher_type': 'Journal Entry', 'company': self.company, 'posting_date': getdate(), 'accounts': [{'account': self.debit_to, 'party_type': 'Customer', 'party': self.customer, 'credit_in_account_currency': 98, 'credit': 98, 'is_advance': 'Yes', 'cost_center': self.south_cc}, {'account': self.cash, 'debit_in_account_currency': 98, 'debit': 98}]})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:105*

### test_journal_with_cost_center_filter

**Category**: instantiation  
**Description**: Instantiate _dict: test journal with cost center filter  
**Expected**: self.assertEqual(len(filtered_output), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_child_cost_center()

filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company, 'include_payments': True, 'customer': self.customer, 'cost_center': self.cost_center})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/sales_register/test_sales_register.py:131*

### test_deferred_revenue

**Category**: instantiation  
**Description**: Instantiate get_doc: test deferred revenue  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

item = frappe.get_doc('Item', self.item)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:76*

### test_deferred_revenue

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test deferred revenue  
**Expected**: self.assertEqual(report.period_total, expected)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer('_Test Customer')
self.create_supplier('_Test Furniture Supplier')
self.setup_deferred_accounts_and_items()
self.clear_old_entries()

si = create_sales_invoice(item=self.item, company=self.company, customer=self.customer, debit_to=self.debit_to, posting_date='2021-05-01', parent_cost_center=self.cost_center, cost_center=self.cost_center, do_not_save=True, rate=300, price_list_rate=300)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/deferred_revenue_and_expense/test_deferred_revenue_and_expense.py:82*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.cleanup()

sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:50*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate _dict: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.cleanup()

filters = frappe._dict({'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:60*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate execute: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.cleanup()

columns, data = execute(filters=filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:61*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:50*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate _dict: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:60*

### test_unpaid_invoice_outstanding

**Category**: instantiation  
**Description**: Instantiate execute: test unpaid invoice outstanding  
**Expected**: self.assertEqual(outstanding[0].get('amount'), 0)  
**Confidence**: 0.80  

```python
columns, data = execute(filters=filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/payment_ledger/test_payment_ledger.py:61*

### test_add_loyalty_points

**Category**: instantiation  
**Description**: Instantiate get_last_doc: test add loyalty points  
**Expected**: self.assertEqual(doc.loyalty_points, 10)  
**Confidence**: 0.80  

```python
doc = frappe.get_last_doc('Loyalty Point Entry')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:43*

### test_add_loyalty_points_with_discretionary_reason

**Category**: instantiation  
**Description**: Instantiate get_doc: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(doc.loyalty_points, 75)  
**Confidence**: 0.80  

```python
doc = frappe.get_doc({'doctype': 'Loyalty Point Entry', 'loyalty_program': 'Test Single Loyalty', 'loyalty_program_tier': 'Bronce', 'customer': self.customer_name, 'invoice_type': 'Sales Invoice', 'loyalty_points': 75, 'expiry_date': today(), 'posting_date': today(), 'company': '_Test Company', 'discretionary_reason': 'Customer Appreciation'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:47*

### test_add_loyalty_points_with_discretionary_reason

**Category**: instantiation  
**Description**: Instantiate get_doc: test add loyalty points with discretionary reason  
**Expected**: self.assertEqual(entry.loyalty_points, 75)  
**Confidence**: 0.80  

```python
entry = frappe.get_doc('Loyalty Point Entry', doc.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:66*

### test_redeem_loyalty_points

**Category**: instantiation  
**Description**: Instantiate get_last_doc: test redeem loyalty points  
**Expected**: self.assertEqual(doc.loyalty_points, -10)  
**Confidence**: 0.80  

```python
doc = frappe.get_last_doc('Loyalty Point Entry')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/loyalty_point_entry/test_loyalty_point_entry.py:72*

### test_tax_withholding_for_customers

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test tax withholding for customers  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

si = create_sales_invoice(rate=1000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:28*

### test_tax_withholding_for_customers

**Category**: instantiation  
**Description**: Instantiate _dict: test tax withholding for customers  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

filters = frappe._dict(company='_Test Company', party_type='Customer', from_date=today(), to_date=today())
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:32*

### test_single_account_for_multiple_categories

**Category**: instantiation  
**Description**: Instantiate make_purchase_invoice: test single account for multiple categories  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

inv_1 = make_purchase_invoice(rate=1000, do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:46*

### test_single_account_for_multiple_categories

**Category**: instantiation  
**Description**: Instantiate make_purchase_invoice: test single account for multiple categories  
**Expected**: self.check_expected_values(result, expected_values)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.clear_old_entries()
create_tax_accounts()

inv_2 = make_purchase_invoice(rate=1000, do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/tax_withholding_details/test_tax_withholding_details.py:51*

### test_loan_entries_in_bank_reco_statement

**Category**: instantiation  
**Description**: Instantiate _dict: test loan entries in bank reco statement  
**Expected**: self.assertEqual(result[1][0].payment_entry, repayment_entry.name)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'company': 'Test Company', 'account': 'Payment Account - _TC', 'report_date': '2018-10-30'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/bank_reconciliation_statement/test_bank_reconciliation_statement.py:26*

### test_loan_entries_in_bank_reco_statement

**Category**: instantiation  
**Description**: Instantiate execute: test loan entries in bank reco statement  
**Expected**: self.assertEqual(result[1][0].payment_entry, repayment_entry.name)  
**Confidence**: 0.80  

```python
result = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/bank_reconciliation_statement/test_bank_reconciliation_statement.py:33*

### test_loan_entries_in_bank_reco_statement

**Category**: instantiation  
**Description**: Instantiate _dict: test loan entries in bank reco statement  
**Expected**: self.assertEqual(result[1][0].payment_entry, repayment_entry.name)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'company': 'Test Company', 'account': 'Payment Account - _TC', 'report_date': '2018-10-30'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/bank_reconciliation_statement/test_bank_reconciliation_statement.py:26*

### test_loan_entries_in_bank_reco_statement

**Category**: instantiation  
**Description**: Instantiate execute: test loan entries in bank reco statement  
**Expected**: self.assertEqual(result[1][0].payment_entry, repayment_entry.name)  
**Confidence**: 0.80  

```python
result = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/bank_reconciliation_statement/test_bank_reconciliation_statement.py:33*

### test_invalid_share_transfer

**Category**: instantiation  
**Description**: Instantiate get_doc: test invalid share transfer  
**Expected**: self.assertRaises(ShareDontExists, doc.insert)  
**Confidence**: 0.80  

```python
# Setup
frappe.db.sql('delete from `tabShare Transfer`')
frappe.db.sql('delete from `tabShare Balance`')
share_transfers = [{'doctype': 'Share Transfer', 'transfer_type': 'Issue', 'date': '2018-01-01', 'to_shareholder': 'SH-00001', 'share_type': 'Equity', 'from_no': 1, 'to_no': 500, 'no_of_shares': 500, 'rate': 10, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-02', 'from_shareholder': 'SH-00001', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 101, 'to_no': 200, 'no_of_shares': 100, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-03', 'from_shareholder': 'SH-00001', 'to_shareholder': 'SH-00003', 'share_type': 'Equity', 'from_no': 201, 'to_no': 500, 'no_of_shares': 300, 'rate': 20, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-04', 'from_shareholder': 'SH-00003', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 201, 'to_no': 400, 'no_of_shares': 200, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Purchase', 'date': '2018-01-05', 'from_shareholder': 'SH-00003', 'share_type': 'Equity', 'from_no': 401, 'to_no': 500, 'no_of_shares': 100, 'rate': 25, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'}]
for d in share_transfers:
    st = frappe.get_doc(d)
    st.submit()

doc = frappe.get_doc({'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-05', 'from_shareholder': 'SH-00003', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 1, 'to_no': 100, 'no_of_shares': 100, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/share_transfer/test_share_transfer.py:93*

### test_invalid_share_transfer

**Category**: instantiation  
**Description**: Instantiate get_doc: test invalid share transfer  
**Expected**: self.assertRaises(ShareDontExists, doc.insert)  
**Confidence**: 0.80  

```python
# Setup
frappe.db.sql('delete from `tabShare Transfer`')
frappe.db.sql('delete from `tabShare Balance`')
share_transfers = [{'doctype': 'Share Transfer', 'transfer_type': 'Issue', 'date': '2018-01-01', 'to_shareholder': 'SH-00001', 'share_type': 'Equity', 'from_no': 1, 'to_no': 500, 'no_of_shares': 500, 'rate': 10, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-02', 'from_shareholder': 'SH-00001', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 101, 'to_no': 200, 'no_of_shares': 100, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-03', 'from_shareholder': 'SH-00001', 'to_shareholder': 'SH-00003', 'share_type': 'Equity', 'from_no': 201, 'to_no': 500, 'no_of_shares': 300, 'rate': 20, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-04', 'from_shareholder': 'SH-00003', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 201, 'to_no': 400, 'no_of_shares': 200, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'}, {'doctype': 'Share Transfer', 'transfer_type': 'Purchase', 'date': '2018-01-05', 'from_shareholder': 'SH-00003', 'share_type': 'Equity', 'from_no': 401, 'to_no': 500, 'no_of_shares': 100, 'rate': 25, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'}]
for d in share_transfers:
    st = frappe.get_doc(d)
    st.submit()

doc = frappe.get_doc({'doctype': 'Share Transfer', 'transfer_type': 'Purchase', 'date': '2018-01-02', 'from_shareholder': 'SH-00001', 'share_type': 'Equity', 'from_no': 1, 'to_no': 200, 'no_of_shares': 200, 'rate': 15, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/share_transfer/test_share_transfer.py:111*

### test_invalid_share_transfer

**Category**: instantiation  
**Description**: Instantiate get_doc: test invalid share transfer  
**Expected**: self.assertRaises(ShareDontExists, doc.insert)  
**Confidence**: 0.80  

```python
doc = frappe.get_doc({'doctype': 'Share Transfer', 'transfer_type': 'Transfer', 'date': '2018-01-05', 'from_shareholder': 'SH-00003', 'to_shareholder': 'SH-00002', 'share_type': 'Equity', 'from_no': 1, 'to_no': 100, 'no_of_shares': 100, 'rate': 15, 'company': '_Test Company', 'equity_or_liability_account': 'Creditors - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/share_transfer/test_share_transfer.py:93*

### test_invalid_share_transfer

**Category**: instantiation  
**Description**: Instantiate get_doc: test invalid share transfer  
**Expected**: self.assertRaises(ShareDontExists, doc.insert)  
**Confidence**: 0.80  

```python
doc = frappe.get_doc({'doctype': 'Share Transfer', 'transfer_type': 'Purchase', 'date': '2018-01-02', 'from_shareholder': 'SH-00001', 'share_type': 'Equity', 'from_no': 1, 'to_no': 200, 'no_of_shares': 200, 'rate': 15, 'company': '_Test Company', 'asset_account': 'Cash - _TC', 'equity_or_liability_account': 'Creditors - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/share_transfer/test_share_transfer.py:111*

### test_create_test_data

**Category**: instantiation  
**Description**: Instantiate get_list: test create test data  
**Confidence**: 0.80  

```python
item_price = frappe.get_list('Item Price', filters={'item_code': '_Test Tesla Car', 'price_list': '_Test Price List'}, fields=['name'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/coupon_code/test_coupon_code.py:48*

### test_finance_book

**Category**: instantiation  
**Description**: Instantiate make_journal_entry: test finance book  
**Confidence**: 0.80  

```python
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:15*

### test_finance_book

**Category**: instantiation  
**Description**: Instantiate get_all: test finance book  
**Confidence**: 0.80  

```python
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:23*

### test_finance_book

**Category**: instantiation  
**Description**: Instantiate make_journal_entry: test finance book  
**Confidence**: 0.80  

```python
jv = make_journal_entry('_Test Bank - _TC', 'Debtors - _TC', 100, save=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:15*

### test_finance_book

**Category**: instantiation  
**Description**: Instantiate get_all: test finance book  
**Confidence**: 0.80  

```python
gl_entries = frappe.get_all('GL Entry', fields=['name', 'finance_book'], filters={'voucher_type': 'Journal Entry', 'voucher_no': jv.name})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/finance_book/test_finance_book.py:23*

### test_opening_sales_invoice_creation

**Category**: instantiation  
**Description**: Instantiate make_invoices: test opening sales invoice creation  
**Expected**: self.assertEqual(len(invoices), 2)  
**Confidence**: 0.80  

```python
invoices = self.make_invoices(company='_Test Opening Invoice Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:48*

### test_opening_sales_invoice_creation

**Category**: instantiation  
**Description**: Instantiate get_doc: test opening sales invoice creation  
**Expected**: self.assertEqual(si.update_stock, 0)  
**Confidence**: 0.80  

```python
si = frappe.get_doc('Sales Invoice', invoices[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:58*

### test_opening_purchase_invoice_creation

**Category**: instantiation  
**Description**: Instantiate make_invoices: test opening purchase invoice creation  
**Expected**: self.assertEqual(len(invoices), 2)  
**Confidence**: 0.80  

```python
invoices = self.make_invoices(invoice_type='Purchase', company='_Test Opening Invoice Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:72*

### test_opening_sales_invoice_creation_with_missing_debit_account

**Category**: instantiation  
**Description**: Instantiate get_value: test opening sales invoice creation with missing debit account  
**Expected**: self.assertTrue(error_log)  
**Confidence**: 0.80  

```python
old_default_receivable_account = frappe.db.get_value('Company', company, 'default_receivable_account')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:86*

### test_opening_sales_invoice_creation_with_missing_debit_account

**Category**: instantiation  
**Description**: Instantiate exists: test opening sales invoice creation with missing debit account  
**Expected**: self.assertTrue(error_log)  
**Confidence**: 0.80  

```python
error_log = frappe.db.exists('Error Log', {'error': ['like', '%erpnext.controllers.accounts_controller.AccountMissingError%']})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:115*

### test_opening_sales_invoice_creation_with_missing_debit_account

**Category**: instantiation  
**Description**: Instantiate get_doc: test opening sales invoice creation with missing debit account  
**Confidence**: 0.80  

```python
cc = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Opening Invoice Company', 'is_group': 1, 'company': '_Test Opening Invoice Company'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/opening_invoice_creation_tool/test_opening_invoice_creation_tool.py:90*

### test_debit_credit_mismatch

**Category**: instantiation  
**Description**: Instantiate get_all: test debit credit mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

actual = frappe.db.get_all('Ledger Health', fields=['voucher_type', 'voucher_no', 'debit_credit_mismatch', 'general_and_payment_ledger_mismatch'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:73*

### test_gl_and_pl_mismatch

**Category**: instantiation  
**Description**: Instantiate get_all: test gl and pl mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

actual = frappe.db.get_all('Ledger Health', fields=['voucher_type', 'voucher_no', 'debit_credit_mismatch', 'general_and_payment_ledger_mismatch'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:99*

### test_debit_credit_mismatch

**Category**: instantiation  
**Description**: Instantiate get_all: test debit credit mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.80  

```python
actual = frappe.db.get_all('Ledger Health', fields=['voucher_type', 'voucher_no', 'debit_credit_mismatch', 'general_and_payment_ledger_mismatch'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:73*

### test_gl_and_pl_mismatch

**Category**: instantiation  
**Description**: Instantiate get_all: test gl and pl mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.80  

```python
actual = frappe.db.get_all('Ledger Health', fields=['voucher_type', 'voucher_no', 'debit_credit_mismatch', 'general_and_payment_ledger_mismatch'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:99*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_account: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:20*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_item: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
item = create_item('_Test Item for Deferred Accounting')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:26*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:32*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate get_doc: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
process_deferred_accounting = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2023-07-01', start_date='2023-05-01', end_date='2023-06-30', type='Income')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:49*

### test_pda_submission_and_cancellation

**Category**: instantiation  
**Description**: Instantiate get_doc: test pda submission and cancellation  
**Confidence**: 0.80  

```python
pda = frappe.get_doc(doctype='Process Deferred Accounting', posting_date='2019-01-01', start_date='2019-01-01', end_date='2019-01-31', type='Income')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:79*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_account: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
deferred_account = create_account(account_name='Deferred Revenue for Accounts Frozen', parent_account='Current Liabilities - _TC', company='_Test Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:20*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_item: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
item = create_item('_Test Item for Deferred Accounting')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:26*

### test_creation_of_ledger_entry_on_submit

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test creation of gl entries on submission of document  
**Expected**: check_gl_entries(self, si.name, expected_gle, '2023-07-01')  
**Confidence**: 0.80  

```python
si = create_sales_invoice(item=item.name, rate=3000, update_stock=0, posting_date='2023-07-01', do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/process_deferred_accounting/test_process_deferred_accounting.py:32*

### test_get_default_price_list_should_return_none_for_invalid_group

**Category**: instantiation  
**Description**: Instantiate insert: test get default price list should return none for invalid group  
**Expected**: assert price_list is None  
**Confidence**: 0.80  

```python
customer = frappe.get_doc({'doctype': 'Customer', 'customer_name': 'test customer'}).insert(ignore_permissions=True, ignore_mandatory=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test_party.py:9*

### test_get_default_price_list_should_return_none_for_invalid_group

**Category**: instantiation  
**Description**: Instantiate get_default_price_list: test get default price list should return none for invalid group  
**Expected**: assert price_list is None  
**Confidence**: 0.80  

```python
price_list = get_default_price_list(customer)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test_party.py:17*

### test_get_default_price_list_should_return_none_for_invalid_group

**Category**: instantiation  
**Description**: Instantiate insert: test get default price list should return none for invalid group  
**Expected**: assert price_list is None  
**Confidence**: 0.80  

```python
customer = frappe.get_doc({'doctype': 'Customer', 'customer_name': 'test customer'}).insert(ignore_permissions=True, ignore_mandatory=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test_party.py:9*

### test_get_default_price_list_should_return_none_for_invalid_group

**Category**: instantiation  
**Description**: Instantiate get_default_price_list: test get default price list should return none for invalid group  
**Expected**: assert price_list is None  
**Confidence**: 0.80  

```python
price_list = get_default_price_list(customer)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/test_party.py:17*

### test_extra_year

**Category**: instantiation  
**Description**: Instantiate get_doc: test extra year  
**Expected**: self.assertRaises(frappe.exceptions.InvalidDates, fy.insert)  
**Confidence**: 0.80  

```python
fy = frappe.get_doc({'doctype': 'Fiscal Year', 'year': '_Test Fiscal Year 2000', 'year_end_date': '2002-12-31', 'year_start_date': '2000-04-01'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:16*

### test_company_fiscal_year_overlap

**Category**: instantiation  
**Description**: Instantiate new_doc: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))  
**Confidence**: 0.80  

```python
global_fy = frappe.new_doc('Fiscal Year')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:32*

### test_company_fiscal_year_overlap

**Category**: instantiation  
**Description**: Instantiate new_doc: test company fiscal year overlap  
**Expected**: self.assertTrue(frappe.db.exists('Fiscal Year', global_fy.name))  
**Confidence**: 0.80  

```python
company_fy = frappe.new_doc('Fiscal Year')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/fiscal_year/test_fiscal_year.py:38*

### test_payment_order_creation_against_payment_entry

**Category**: instantiation  
**Description**: Instantiate get_payment_entry: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.reference_name, payment_entry.name)  
**Confidence**: 0.80  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

payment_entry = get_payment_entry('Purchase Invoice', purchase_invoice.name, bank_account=self.gl_account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:34*

### test_payment_order_creation_against_payment_entry

**Category**: instantiation  
**Description**: Instantiate create_payment_order_against_payment_entry: test payment order creation against payment entry  
**Expected**: self.assertEqual(reference_doc.reference_name, payment_entry.name)  
**Confidence**: 0.80  

```python
# Setup
uniq_identifier = frappe.generate_hash(length=10)
self.gl_account = create_gl_account('_Test Bank ' + uniq_identifier)
self.bank_account = create_bank_account(gl_account=self.gl_account, bank_account_name='Checking Account ' + uniq_identifier)

doc = create_payment_order_against_payment_entry(payment_entry, 'Payment Entry', self.bank_account)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/payment_order/test_payment_order.py:43*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate add_days: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.clear_old_entries()
bank_dt = qb.DocType('Bank')
qb.from_(bank_dt).delete().where(bank_dt.name == 'HDFC').run()
self.create_bank_account()

from_date = add_days(today(), -1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:54*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate get_bank_transactions: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.clear_old_entries()
bank_dt = qb.DocType('Bank')
qb.from_(bank_dt).delete().where(bank_dt.name == 'HDFC').run()
self.create_bank_account()

transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:86*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate get_bank_transactions: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 0)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_customer()
self.clear_old_entries()
bank_dt = qb.DocType('Bank')
qb.from_(bank_dt).delete().where(bank_dt.name == 'HDFC').run()
self.create_bank_account()

transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:99*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate add_days: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 1)  
**Confidence**: 0.80  

```python
from_date = add_days(today(), -1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:54*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate get_bank_transactions: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 1)  
**Confidence**: 0.80  

```python
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:86*

### test_auto_reconcile

**Category**: instantiation  
**Description**: Instantiate get_bank_transactions: test auto reconcile  
**Expected**: self.assertEqual(len(transactions), 0)  
**Confidence**: 0.80  

```python
transactions = get_bank_transactions(self.bank_account, from_date, to_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/bank_reconciliation_tool/test_bank_reconciliation_tool.py:99*

### test_01_basic_report_functionality

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test 01 basic report functionality  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.cleanup()

sinv = create_sales_invoice(company=self.company, debit_to=self.debit_to, expense_account=self.expense_account, cost_center=self.cost_center, income_account=self.income_account, warehouse=self.warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:31*

### test_01_basic_report_functionality

**Category**: instantiation  
**Description**: Instantiate _dict: test 01 basic report functionality  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.cleanup()

filters = frappe._dict({'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/general_and_payment_ledger_comparison/test_general_and_payment_ledger_comparison.py:44*

### test_cost_center_creation_against_child_node

**Category**: instantiation  
**Description**: Instantiate get_doc: test cost center creation against child node  
**Expected**: self.assertRaises(frappe.ValidationError, cost_center.save)  
**Confidence**: 0.80  

```python
cost_center = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Cost Center 3', 'parent_cost_center': '_Test Cost Center 2 - _TC', 'is_group': 0, 'company': '_Test Company'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center/test_cost_center.py:10*

### test_cost_center_creation_against_child_node

**Category**: instantiation  
**Description**: Instantiate get_doc: test cost center creation against child node  
**Expected**: self.assertRaises(frappe.ValidationError, cost_center.save)  
**Confidence**: 0.80  

```python
cost_center = frappe.get_doc({'doctype': 'Cost Center', 'cost_center_name': '_Test Cost Center 3', 'parent_cost_center': '_Test Cost Center 2 - _TC', 'is_group': 0, 'company': '_Test Company'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/cost_center/test_cost_center.py:10*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate _dict: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()

filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:40*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate execute: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()

report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:41*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate _dict: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'from_date': today(), 'to_date': today(), 'company': self.company})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:40*

### test_basic_report_output

**Category**: instantiation  
**Description**: Instantiate execute: test basic report output  
**Expected**: self.assertEqual(len(report[1]), 1)  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:41*

### test_account_balance

**Category**: instantiation  
**Description**: Instantiate execute: test account balance  
**Expected**: self.assertEqual(expected_data, report[1])  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/account_balance/test_account_balance.py:22*

### test_account_balance

**Category**: instantiation  
**Description**: Instantiate execute: test account balance  
**Expected**: self.assertEqual(expected_data, report[1])  
**Confidence**: 0.80  

```python
report = execute(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/account_balance/test_account_balance.py:22*

### test_basic_report_output

**Category**: config  
**Description**: Configuration example: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()

expected_result = {'item_code': si.items[0].item_code, 'invoice': si.name, 'posting_date': getdate(), 'customer': si.customer, 'debit_to': si.debit_to, 'company': self.company, 'income_account': si.items[0].income_account, 'stock_qty': 1.0, 'stock_uom': si.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total_other_charges': 0, 'total': 100.0, 'currency': 'INR'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:45*

### test_basic_report_output

**Category**: config  
**Description**: Configuration example: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.75  

```python
expected_result = {'item_code': si.items[0].item_code, 'invoice': si.name, 'posting_date': getdate(), 'customer': si.customer, 'debit_to': si.debit_to, 'company': self.company, 'income_account': si.items[0].income_account, 'stock_qty': 1.0, 'stock_uom': si.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total_other_charges': 0, 'total': 100.0, 'currency': 'INR'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_sales_register/test_item_wise_sales_register.py:45*

### test_basic_supplier_ledger_summary

**Category**: config  
**Description**: Configuration example: test basic supplier ledger summary  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:43*

### test_basic_supplier_ledger_summary

**Category**: config  
**Description**: Configuration example: test basic supplier ledger summary  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:45*

### test_supplier_ledger_summary_with_filters

**Category**: config  
**Description**: Configuration example: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

filters = {'company': self.company, 'from_date': today(), 'to_date': today(), 'supplier_group': supplier_group}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:68*

### test_supplier_ledger_summary_with_filters

**Category**: config  
**Description**: Configuration example: test supplier ledger summary with filters  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()
self.clear_old_entries()

expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:75*

### test_basic_supplier_ledger_summary

**Category**: config  
**Description**: Configuration example: test basic supplier ledger summary  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
filters = {'company': self.company, 'from_date': today(), 'to_date': today()}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:43*

### test_basic_supplier_ledger_summary

**Category**: config  
**Description**: Configuration example: test basic supplier ledger summary  
**Expected**: self.assertEqual(len(report_output), 1)  
**Confidence**: 0.75  

```python
expected = {'party': '_Test Supplier', 'party_name': '_Test Supplier', 'opening_balance': 0, 'invoiced_amount': 300.0, 'paid_amount': 0, 'return_amount': 0, 'closing_balance': 300.0, 'currency': 'INR', 'supplier_name': '_Test Supplier'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/supplier_ledger_summary/test_supplier_ledger_summary.py:45*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: config  
**Description**: Configuration example: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_customer()
self.create_item()
self.create_supplier(currency='USD', supplier_name='Test Supplier2')
self.create_usd_payable_account()

filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:28*

### test_accounts_payable_for_foreign_currency_supplier

**Category**: config  
**Description**: Configuration example: test accounts payable for foreign currency supplier  
**Expected**: self.assertEqual(data[1][0].get('outstanding'), 300)  
**Confidence**: 0.75  

```python
filters = {'company': self.company, 'party_type': 'Supplier', 'party': [self.supplier], 'report_date': today(), 'range': '30, 60, 90, 120', 'in_party_currency': 1}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/accounts_payable/test_accounts_payable.py:28*

### test_debit_credit_mismatch

**Category**: config  
**Description**: Configuration example: test debit credit mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

expected = {'voucher_type': self.je.doctype, 'voucher_no': self.je.name, 'debit_credit_mismatch': True, 'general_and_payment_ledger_mismatch': False}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:67*

### test_gl_and_pl_mismatch

**Category**: config  
**Description**: Configuration example: test gl and pl mismatch  
**Expected**: self.assertEqual(len(actual), 1)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_customer()
self.configure_monitoring_tool()
self.clear_old_entries()

expected = {'voucher_type': self.je.doctype, 'voucher_no': self.je.name, 'debit_credit_mismatch': False, 'general_and_payment_ledger_mismatch': True}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/doctype/ledger_health/test_ledger_health.py:93*

### test_basic_report_output

**Category**: config  
**Description**: Configuration example: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.75  

```python
# Setup
self.create_company()
self.create_supplier()
self.create_item()

expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:45*

### test_basic_report_output

**Category**: config  
**Description**: Configuration example: test basic report output  
**Expected**: self.assertDictEqual(report_output, expected_result)  
**Confidence**: 0.75  

```python
expected_result = {'item_code': pi.items[0].item_code, 'invoice': pi.name, 'posting_date': getdate(), 'supplier': pi.supplier, 'credit_to': pi.credit_to, 'company': self.company, 'expense_account': pi.items[0].expense_account, 'stock_qty': 1.0, 'stock_uom': pi.items[0].stock_uom, 'rate': 100.0, 'amount': 100.0, 'total_tax': 0, 'total': 100.0, 'currency': 'INR'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/item_wise_purchase_register/test_item_wise_purchase_register.py:45*

### test_account_balance

**Category**: config  
**Description**: Configuration example: test account balance  
**Expected**: self.assertEqual(expected_data, report[1])  
**Confidence**: 0.75  

```python
filters = {'company': '_Test Company 2', 'report_date': getdate(), 'root_type': 'Income'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/account_balance/test_account_balance.py:14*

### test_account_balance

**Category**: config  
**Description**: Configuration example: test account balance  
**Expected**: self.assertEqual(expected_data, report[1])  
**Confidence**: 0.75  

```python
filters = {'company': '_Test Company 2', 'report_date': getdate(), 'root_type': 'Income'}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/accounts/report/account_balance/test_account_balance.py:14*

