# Test Example Extraction Report

**Total Examples**: 74  
**High Value Examples** (confidence > 0.7): 74  
**Average Complexity**: 0.59  

## Examples by Category

- **instantiation**: 10
- **method_call**: 32
- **workflow**: 32

## Examples by Language

- **Python**: 74

## Extracted Examples

### test_pending_and_received_qty

**Category**: workflow  
**Description**: Workflow: test pending and received qty  
**Expected**: self.assertEqual(data[0]['supplier'], sco.supplier)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
rm_items = get_rm_items(sco.supplied_items)
itemwise_details = make_stock_in_entry(rm_items=rm_items)
for item in rm_items:
    item['sco_rm_detail'] = sco.items[0].name
make_stock_transfer_entry(sco_no=sco.name, rm_items=rm_items, itemwise_details=copy.deepcopy(itemwise_details))
make_subcontracting_receipt_against_sco(sco.name)
sco.reload()
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
self.assertEqual(data[0]['pending_qty'], 5)
self.assertEqual(data[0]['received_qty'], 5)
self.assertEqual(data[0]['subcontract_order'], sco.name)
self.assertEqual(data[0]['supplier'], sco.supplier)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:28*

### test_pending_and_received_qty

**Category**: workflow  
**Description**: Workflow: test pending and received qty  
**Expected**: self.assertEqual(data[0]['supplier'], sco.supplier)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
rm_items = get_rm_items(sco.supplied_items)
itemwise_details = make_stock_in_entry(rm_items=rm_items)
for item in rm_items:
    item['sco_rm_detail'] = sco.items[0].name
make_stock_transfer_entry(sco_no=sco.name, rm_items=rm_items, itemwise_details=copy.deepcopy(itemwise_details))
make_subcontracting_receipt_against_sco(sco.name)
sco.reload()
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
self.assertEqual(data[0]['pending_qty'], 5)
self.assertEqual(data[0]['received_qty'], 5)
self.assertEqual(data[0]['subcontract_order'], sco.name)
self.assertEqual(data[0]['supplier'], sco.supplier)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:28*

### test_ordered_qty_against_pi_with_update_stock

**Category**: workflow  
**Description**: Workflow: test ordered qty against pi with update stock  
**Expected**: self.assertEqual(po.get('items')[0].received_qty, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
existing_ordered_qty = get_ordered_qty()
po = create_purchase_order()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
pi = make_pi_from_po(po.name)
pi.update_stock = 1
pi.items[0].qty = 12
pi.insert()
pi.submit()
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 12)
pi.cancel()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 10)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 0)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 0)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 0)
frappe.db.set_single_value('Accounts Settings', 'over_billing_allowance', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:99*

### test_update_remove_child_linked_to_mr

**Category**: workflow  
**Description**: Workflow: Test impact on linked PO and MR on deleting/updating row.  
**Expected**: self.assertEqual(get_ordered_qty(), existing_ordered_qty - 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact on linked PO and MR on deleting/updating row.'
mr = make_material_request(qty=10)
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save()
po.submit()
first_item_of_po = po.get('items')[0]
existing_ordered_qty = get_ordered_qty()
existing_requested_qty = get_requested_qty()
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': 7, 'docname': first_item_of_po.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(get_requested_qty(), existing_requested_qty + 3)
self.assertEqual(mr.items[0].ordered_qty, 7)
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 3)
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 200, 'qty': 2}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(get_requested_qty(), existing_requested_qty + 10)
self.assertEqual(mr.items[0].ordered_qty, 0)
self.assertEqual(get_ordered_qty(), existing_ordered_qty - 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:129*

### test_update_child

**Category**: workflow  
**Description**: Workflow: test update child  
**Expected**: self.assertEqual(get_ordered_qty(), existing_ordered_qty + 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = make_material_request(qty=10)
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.items[0].qty = 4
po.save()
po.submit()
create_pr_against_po(po.name)
make_pi_from_po(po.name)
existing_ordered_qty = get_ordered_qty()
existing_requested_qty = get_requested_qty()
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
mr.reload()
self.assertEqual(mr.items[0].ordered_qty, 7)
self.assertEqual(mr.per_ordered, 70)
self.assertEqual(get_requested_qty(), existing_requested_qty - 3)
po.reload()
self.assertEqual(po.get('items')[0].rate, 200)
self.assertEqual(po.get('items')[0].qty, 7)
self.assertEqual(po.get('items')[0].amount, 1400)
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:174*

### test_update_child_adding_new_item

**Category**: workflow  
**Description**: Workflow: test update child adding new item  
**Expected**: self.assertEqual(get_ordered_qty(), existing_ordered_qty + 7)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order(do_not_save=1)
po.items[0].qty = 4
po.save()
po.submit()
make_pr_against_po(po.name, 2)
po.load_from_db()
existing_ordered_qty = get_ordered_qty()
first_item_of_po = po.get('items')[0]
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}, {'item_code': '_Test Item', 'rate': 200, 'qty': 7}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
po.reload()
self.assertEqual(len(po.get('items')), 2)
self.assertEqual(po.status, 'To Receive and Bill')
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 7)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:205*

### test_update_child_removing_item

**Category**: workflow  
**Description**: Workflow: test update child removing item  
**Expected**: self.assertEqual(get_ordered_qty(), existing_ordered_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order(do_not_save=1)
po.items[0].qty = 4
po.save()
po.submit()
make_pr_against_po(po.name, 2)
po.reload()
first_item_of_po = po.get('items')[0]
existing_ordered_qty = get_ordered_qty()
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}, {'item_code': '_Test Item', 'rate': 200, 'qty': 7}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
po.reload()
self.assertEqual(get_ordered_qty(), existing_ordered_qty + 7)
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.get('items')[1].name}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
first_item_of_po = po.get('items')[0]
trans_item = json.dumps([{'item_code': first_item_of_po.item_code, 'rate': first_item_of_po.rate, 'qty': first_item_of_po.qty, 'docname': first_item_of_po.name}])
update_child_qty_rate('Purchase Order', trans_item, po.name)
po.reload()
self.assertEqual(len(po.get('items')), 1)
self.assertEqual(po.status, 'To Receive and Bill')
self.assertEqual(get_ordered_qty(), existing_ordered_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:235*

### test_update_child_perm

**Category**: workflow  
**Description**: Workflow: test update child perm  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order(item_code='_Test Item', qty=4)
user = 'test@example.com'
test_user = frappe.get_doc('User', user)
test_user.add_roles('Accounts User')
with self.set_user(user):
    trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': po.items[0].name}])
    self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
    trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 100, 'qty': 2}])
    self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Purchase Order', trans_item, po.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:292*

### test_update_qty

**Category**: workflow  
**Description**: Workflow: test update qty  
**Expected**: self.assertEqual(po.get('items')[0].received_qty, 6)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order()
pr = make_pr_against_po(po.name, 2)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 2)
pi1 = make_pi_from_pr(pr.name)
pi1.get('items')[0].qty = 2
pi1.insert()
pi1.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 2)
pi2 = make_pi_from_po(po.name)
pi2.set('update_stock', 1)
pi2.get('items')[0].qty = 3
pi2.insert()
pi2.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 5)
pr = make_pr_against_po(po.name, 1)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:422*

### test_return_against_purchase_order

**Category**: workflow  
**Description**: Workflow: test return against purchase order  
**Expected**: self.assertEqual(po.get('items')[0].received_qty, 5)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
po = create_purchase_order()
pr = make_pr_against_po(po.name, 6)
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 6)
pi2 = make_pi_from_po(po.name)
pi2.set('update_stock', 1)
pi2.get('items')[0].qty = 3
pi2.insert()
pi2.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 9)
from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice as make_purchase_invoice_return
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt as make_purchase_receipt_return
pr1 = make_purchase_receipt_return(is_return=1, return_against=pr.name, qty=-3, do_not_submit=True)
pr1.items[0].purchase_order = po.name
pr1.items[0].purchase_order_item = po.items[0].name
pr1.submit()
pi1 = make_purchase_invoice_return(is_return=1, return_against=pi2.name, qty=-1, update_stock=1, do_not_submit=True)
pi1.items[0].purchase_order = po.name
pi1.items[0].po_detail = po.items[0].name
pi1.submit()
po.load_from_db()
self.assertEqual(po.get('items')[0].received_qty, 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:455*

### test_purchase_order_invoice_receipt_workflow

**Category**: workflow  
**Description**: Workflow: test purchase order invoice receipt workflow  
**Expected**: self.assertEqual(po.per_billed, 100.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import make_purchase_receipt
po = create_purchase_order()
pi = make_pi_from_po(po.name)
pi.submit()
pr = make_purchase_receipt(pi.name)
pr.submit()
pi.load_from_db()
self.assertEqual(pi.per_received, 100.0)
self.assertEqual(pi.items[0].qty, pi.items[0].received_qty)
po.load_from_db()
self.assertEqual(po.per_received, 100.0)
self.assertEqual(po.per_billed, 100.0)
pr.cancel()
pi.load_from_db()
pi.cancel()
po.load_from_db()
po.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:495*

### test_po_for_blocked_supplier_invoices

**Category**: workflow  
**Description**: Workflow: test po for blocked supplier invoices  
**Expected**: self.assertRaises(frappe.ValidationError, create_purchase_order)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
supplier = frappe.get_doc('Supplier', '_Test Supplier')
supplier.on_hold = 1
supplier.hold_type = 'Invoices'
supplier.save()
self.assertRaises(frappe.ValidationError, create_purchase_order)
supplier.on_hold = 0
supplier.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/purchase_order/test_purchase_order.py:639*

### test_get_supplier_group_details

**Category**: workflow  
**Description**: Workflow: test get supplier group details  
**Expected**: self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doc = frappe.new_doc('Supplier Group')
doc.supplier_group_name = '_Testing Supplier Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
doc.append('accounts', test_account_details)
doc.save()
s_doc = frappe.new_doc('Supplier')
s_doc.supplier_name = 'Testing Supplier'
s_doc.supplier_group = '_Testing Supplier Group'
s_doc.payment_terms = ''
s_doc.accounts = []
s_doc.insert()
s_doc.get_supplier_group_details()
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')
s_doc.delete()
doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:18*

### test_supplier_default_payment_terms

**Category**: workflow  
**Description**: Workflow: test supplier default payment terms  
**Expected**: self.assertEqual(due_date, '2017-01-22')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-21')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '')
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', '')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2016-01-22')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2017-01-22')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:42*

### test_get_supplier_group_details

**Category**: workflow  
**Description**: Workflow: test get supplier group details  
**Expected**: self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doc = frappe.new_doc('Supplier Group')
doc.supplier_group_name = '_Testing Supplier Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
doc.append('accounts', test_account_details)
doc.save()
s_doc = frappe.new_doc('Supplier')
s_doc.supplier_name = 'Testing Supplier'
s_doc.supplier_group = '_Testing Supplier Group'
s_doc.payment_terms = ''
s_doc.accounts = []
s_doc.insert()
s_doc.get_supplier_group_details()
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')
s_doc.delete()
doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:18*

### test_supplier_default_payment_terms

**Category**: workflow  
**Description**: Workflow: test supplier default payment terms  
**Expected**: self.assertEqual(due_date, '2017-01-22')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-21')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier', '_Test Supplier With Template 1', 'payment_terms', '')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-21')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier With Template 1')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Supplier Group', '_Test Supplier Group', 'payment_terms', '')
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', '')
due_date = get_due_date('2016-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2016-01-22')
due_date = get_due_date('2017-01-22', 'Supplier', '_Test Supplier')
self.assertEqual(due_date, '2017-01-22')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:42*

### test_pending_and_transferred_qty

**Category**: workflow  
**Description**: Workflow: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[1]['transferred_qty'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items)
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
transfer_subcontracted_raw_materials(sco)
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
sco.reload()
sco_data = [row for row in data if row.get('subcontract_order') == sco.name]
sco_data = sorted(sco_data, key=lambda i: i['rm_item_code'])
self.assertEqual(len(sco_data), 2)
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
self.assertEqual(sco_data[0]['p_qty'], 8)
self.assertEqual(sco_data[0]['transferred_qty'], 2)
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
self.assertEqual(sco_data[1]['p_qty'], 19)
self.assertEqual(sco_data[1]['transferred_qty'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:21*

### test_pending_and_transferred_qty

**Category**: workflow  
**Description**: Workflow: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[1]['transferred_qty'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 10, 'rate': 500, 'fg_item': '_Test FG Item', 'fg_item_qty': 10}]
sco = get_subcontracting_order(service_items=service_items)
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
transfer_subcontracted_raw_materials(sco)
col, data = execute(filters=frappe._dict({'order_type': 'Subcontracting Order', 'supplier': sco.supplier, 'from_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=-10)), 'to_date': frappe.utils.get_datetime(frappe.utils.add_to_date(sco.transaction_date, days=10))}))
sco.reload()
sco_data = [row for row in data if row.get('subcontract_order') == sco.name]
sco_data = sorted(sco_data, key=lambda i: i['rm_item_code'])
self.assertEqual(len(sco_data), 2)
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
self.assertEqual(sco_data[0]['p_qty'], 8)
self.assertEqual(sco_data[0]['transferred_qty'], 2)
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
self.assertEqual(sco_data[1]['p_qty'], 19)
self.assertEqual(sco_data[1]['transferred_qty'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:21*

### test_make_supplier_quotation_with_taxes

**Category**: workflow  
**Description**: Workflow: Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set  
**Expected**: self.assertGreaterEqual(len(sq.get('taxes')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set'
tax_template = frappe.new_doc('Purchase Taxes and Charges Template')
tax_template.doctype = 'Purchase Taxes and Charges Template'
tax_template.title = '_Test Purchase Taxes Template for RFQ'
tax_template.company = '_Test Company'
tax_template.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'description': 'VAT', 'rate': 10})
tax_template.save()
rfq = make_request_for_quotation()
supplier = rfq.get('suppliers')[0].supplier
tax_rule = frappe.new_doc('Tax Rule')
tax_rule.company = '_Test Company'
tax_rule.tax_type = 'Purchase'
tax_rule.supplier = supplier
tax_rule.purchase_tax_template = tax_template.name
tax_rule.save()
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier)
self.assertEqual(sq.taxes_and_charges, tax_template.name)
self.assertGreaterEqual(len(sq.get('taxes')), 1)
tax_rule.delete()
tax_template.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:79*

### test_make_supplier_quotation_with_special_characters

**Category**: workflow  
**Description**: Workflow: test make supplier quotation with special characters  
**Expected**: self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.delete_doc_if_exists('Supplier', "_Test Supplier '1", force=1)
supplier = frappe.new_doc('Supplier')
supplier.supplier_name = "_Test Supplier '1"
supplier.supplier_group = '_Test Supplier Group'
supplier.insert()
rfq = make_request_for_quotation(supplier_data=supplier_wt_appos)
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier_wt_appos[0].get('supplier'))
sq.submit()
frappe.form_dict.name = rfq.name
self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)
frappe.form_dict.name = None
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:119*

### test_make_supplier_quotation_from_portal

**Category**: workflow  
**Description**: Workflow: test make supplier quotation from portal  
**Expected**: self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
rfq = make_request_for_quotation()
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation_doc = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation_doc.supplier, rfq.get('suppliers')[0].supplier)
self.assertEqual(supplier_quotation_doc.get('items')[0].request_for_quotation, rfq.name)
self.assertEqual(supplier_quotation_doc.get('items')[0].item_code, '_Test Item')
self.assertEqual(supplier_quotation_doc.get('items')[0].qty, 5)
self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:138*

### test_make_multi_uom_supplier_quotation

**Category**: workflow  
**Description**: Workflow: test make multi uom supplier quotation  
**Expected**: self.assertEqual(supplier_quotation.items[0].stock_qty, 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_Test Multi UOM RFQ Item'
if not frappe.db.exists('Item', item_code):
    item = make_item(item_code, {'stock_uom': '_Test UOM'})
    row = item.append('uoms', {'uom': 'Kg', 'conversion_factor': 2})
    row.db_update()
rfq = make_request_for_quotation(item_code='_Test Multi UOM RFQ Item', uom='Kg', conversion_factor=2)
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
self.assertEqual(rfq.items[0].stock_qty, 10)
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation.items[0].qty, 5)
self.assertEqual(supplier_quotation.items[0].stock_qty, 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:152*

### test_make_rfq_from_opportunity

**Category**: workflow  
**Description**: Workflow: test make rfq from opportunity  
**Expected**: self.assertEqual(len(rfq.get('items')), len(opportunity.get('items')))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
opportunity = make_opportunity(with_items=1)
supplier_data = get_supplier_data()
rfq = make_rfq(opportunity.name)
self.assertEqual(len(rfq.get('items')), len(opportunity.get('items')))
rfq.message_for_supplier = 'Please supply the specified items at the best possible rates.'
for item in rfq.items:
    item.warehouse = '_Test Warehouse - _TC'
for data in supplier_data:
    rfq.append('suppliers', data)
rfq.status = 'Draft'
rfq.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:171*

### test_supplier_quotation_from_zero_qty_rfq_in_portal

**Category**: workflow  
**Description**: Workflow: test supplier quotation from zero qty rfq in portal  
**Expected**: self.assertEqual(sq.items[0].item_code, rfq.items[0].item_code)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
rfq = make_request_for_quotation(qty=0)
rfq.supplier = rfq.suppliers[0].supplier
sq_name = create_supplier_quotation(rfq)
sq = frappe.get_doc('Supplier Quotation', sq_name)
self.assertEqual(len(sq.items), 1)
self.assertEqual(sq.items[0].qty, 0)
self.assertEqual(sq.items[0].item_code, rfq.items[0].item_code)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:241*

### test_make_supplier_quotation_with_taxes

**Category**: workflow  
**Description**: Workflow: Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set  
**Expected**: self.assertGreaterEqual(len(sq.get('taxes')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automatic tax addition when supplier quotation is created from RFQ taxes_and_charges are set'
tax_template = frappe.new_doc('Purchase Taxes and Charges Template')
tax_template.doctype = 'Purchase Taxes and Charges Template'
tax_template.title = '_Test Purchase Taxes Template for RFQ'
tax_template.company = '_Test Company'
tax_template.append('taxes', {'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'description': 'VAT', 'rate': 10})
tax_template.save()
rfq = make_request_for_quotation()
supplier = rfq.get('suppliers')[0].supplier
tax_rule = frappe.new_doc('Tax Rule')
tax_rule.company = '_Test Company'
tax_rule.tax_type = 'Purchase'
tax_rule.supplier = supplier
tax_rule.purchase_tax_template = tax_template.name
tax_rule.save()
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier)
self.assertEqual(sq.taxes_and_charges, tax_template.name)
self.assertGreaterEqual(len(sq.get('taxes')), 1)
tax_rule.delete()
tax_template.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:79*

### test_make_supplier_quotation_with_special_characters

**Category**: workflow  
**Description**: Workflow: test make supplier quotation with special characters  
**Expected**: self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.delete_doc_if_exists('Supplier', "_Test Supplier '1", force=1)
supplier = frappe.new_doc('Supplier')
supplier.supplier_name = "_Test Supplier '1"
supplier.supplier_group = '_Test Supplier Group'
supplier.insert()
rfq = make_request_for_quotation(supplier_data=supplier_wt_appos)
sq = make_supplier_quotation_from_rfq(rfq.name, for_supplier=supplier_wt_appos[0].get('supplier'))
sq.submit()
frappe.form_dict.name = rfq.name
self.assertEqual(check_supplier_has_docname_access(supplier_wt_appos[0].get('supplier')), True)
frappe.form_dict.name = None
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:119*

### test_make_supplier_quotation_from_portal

**Category**: workflow  
**Description**: Workflow: test make supplier quotation from portal  
**Expected**: self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
rfq = make_request_for_quotation()
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation_doc = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation_doc.supplier, rfq.get('suppliers')[0].supplier)
self.assertEqual(supplier_quotation_doc.get('items')[0].request_for_quotation, rfq.name)
self.assertEqual(supplier_quotation_doc.get('items')[0].item_code, '_Test Item')
self.assertEqual(supplier_quotation_doc.get('items')[0].qty, 5)
self.assertEqual(supplier_quotation_doc.get('items')[0].amount, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:138*

### test_make_multi_uom_supplier_quotation

**Category**: workflow  
**Description**: Workflow: test make multi uom supplier quotation  
**Expected**: self.assertEqual(supplier_quotation.items[0].stock_qty, 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_Test Multi UOM RFQ Item'
if not frappe.db.exists('Item', item_code):
    item = make_item(item_code, {'stock_uom': '_Test UOM'})
    row = item.append('uoms', {'uom': 'Kg', 'conversion_factor': 2})
    row.db_update()
rfq = make_request_for_quotation(item_code='_Test Multi UOM RFQ Item', uom='Kg', conversion_factor=2)
rfq.get('items')[0].rate = 100
rfq.supplier = rfq.suppliers[0].supplier
self.assertEqual(rfq.items[0].stock_qty, 10)
supplier_quotation_name = create_supplier_quotation(rfq)
supplier_quotation = frappe.get_doc('Supplier Quotation', supplier_quotation_name)
self.assertEqual(supplier_quotation.items[0].qty, 5)
self.assertEqual(supplier_quotation.items[0].stock_qty, 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/request_for_quotation/test_request_for_quotation.py:152*

### test_update_supplier_quotation_child_remove_item

**Category**: workflow  
**Description**: Workflow: test update supplier quotation child remove item  
**Expected**: self.assertEqual(len(sq.get('items')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0])
sq.submit()
po = make_purchase_order(sq.name)
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}, {'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
po.get('items')[0].schedule_date = add_days(today(), 1)
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
po.submit()
sq.reload()
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
frappe.db.savepoint('before_cancel')
self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)
frappe.db.rollback(save_point='before_cancel')
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}])
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
sq.reload()
self.assertEqual(len(sq.get('items')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:54*

### test_make_purchase_order

**Category**: workflow  
**Description**: Workflow: test make purchase order  
**Expected**: self.assertEqual(len(po.get('items')), len(sq.get('items')))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0]).insert()
self.assertRaises(frappe.ValidationError, make_purchase_order, sq.name)
sq = frappe.get_doc('Supplier Quotation', sq.name)
sq.submit()
po = make_purchase_order(sq.name)
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(sq.get('items')))
po.naming_series = '_T-Purchase Order-'
for doc in po.get('items'):
    if doc.get('item_code'):
        doc.set('schedule_date', add_days(today(), 1))
po.insert()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:133*

### test_update_supplier_quotation_child_remove_item

**Category**: workflow  
**Description**: Workflow: test update supplier quotation child remove item  
**Expected**: self.assertEqual(len(sq.get('items')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0])
sq.submit()
po = make_purchase_order(sq.name)
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}, {'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
po.get('items')[0].schedule_date = add_days(today(), 1)
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
po.submit()
sq.reload()
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 300, 'qty': 3}])
frappe.db.savepoint('before_cancel')
self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)
frappe.db.rollback(save_point='before_cancel')
trans_item = json.dumps([{'item_code': sq.items[0].item_code, 'rate': sq.items[0].rate, 'qty': sq.items[0].qty, 'docname': sq.items[0].name}])
update_child_qty_rate('Supplier Quotation', trans_item, sq.name)
sq.reload()
self.assertEqual(len(sq.get('items')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:54*

### test_make_purchase_order

**Category**: workflow  
**Description**: Workflow: test make purchase order  
**Expected**: self.assertEqual(len(po.get('items')), len(sq.get('items')))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sq = frappe.copy_doc(self.globalTestRecords['Supplier Quotation'][0]).insert()
self.assertRaises(frappe.ValidationError, make_purchase_order, sq.name)
sq = frappe.get_doc('Supplier Quotation', sq.name)
sq.submit()
po = make_purchase_order(sq.name)
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(sq.get('items')))
po.naming_series = '_T-Purchase Order-'
for doc in po.get('items'):
    if doc.get('item_code'):
        doc.set('schedule_date', add_days(today(), 1))
po.insert()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:133*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['received_qty'], 5)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['pending_qty'], 5)
self.assertEqual(data[0]['received_qty'], 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:71*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['subcontract_order'], sco.name)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['received_qty'], 5)
self.assertEqual(data[0]['subcontract_order'], sco.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:72*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['supplier'], sco.supplier)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['subcontract_order'], sco.name)
self.assertEqual(data[0]['supplier'], sco.supplier)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:73*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['received_qty'], 5)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['pending_qty'], 5)
self.assertEqual(data[0]['received_qty'], 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:71*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['subcontract_order'], sco.name)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['received_qty'], 5)
self.assertEqual(data[0]['subcontract_order'], sco.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:72*

### test_pending_and_received_qty

**Category**: method_call  
**Description**: test pending and received qty  
**Expected**: self.assertEqual(data[0]['supplier'], sco.supplier)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0]['subcontract_order'], sco.name)
self.assertEqual(data[0]['supplier'], sco.supplier)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:73*

### test_formula_validate

**Category**: method_call  
**Description**: test formula validate  
**Expected**: self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[1]).insert)  
**Confidence**: 0.85  

```python
delete_test_scorecards()
self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[1]).insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_scorecard_criteria/test_supplier_scorecard_criteria.py:18*

### test_formula_validate

**Category**: method_call  
**Description**: test formula validate  
**Expected**: self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[1]).insert)  
**Confidence**: 0.85  

```python
delete_test_scorecards()
self.assertRaises(frappe.ValidationError, frappe.get_doc(test_bad_criteria[1]).insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_scorecard_criteria/test_supplier_scorecard_criteria.py:18*

### test_ordered_received_material_requests

**Category**: method_call  
**Description**: test ordered received material requests  
**Expected**: self.assertEqual(data[0].ordered_qty, 0.0)  
**Confidence**: 0.85  

```python
# Setup
create_item('Test MR Report Item')
self.setup_material_request()
self.setup_material_request(order=True, days=1)
self.setup_material_request(order=True, receive=True, days=2)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='Test MR Report Item')

self.assertEqual(len(data), 2)
self.assertEqual(data[0].ordered_qty, 0.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:44*

### test_ordered_received_material_requests

**Category**: method_call  
**Description**: test ordered received material requests  
**Expected**: self.assertEqual(data[1].ordered_qty, 57.0)  
**Confidence**: 0.85  

```python
# Setup
create_item('Test MR Report Item')
self.setup_material_request()
self.setup_material_request(order=True, days=1)
self.setup_material_request(order=True, receive=True, days=2)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='Test MR Report Item')

self.assertEqual(data[0].ordered_qty, 0.0)
self.assertEqual(data[1].ordered_qty, 57.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:45*

### test_ordered_received_material_requests

**Category**: method_call  
**Description**: test ordered received material requests  
**Expected**: self.assertEqual(data[0].ordered_qty, 0.0)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 2)
self.assertEqual(data[0].ordered_qty, 0.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:44*

### test_ordered_received_material_requests

**Category**: method_call  
**Description**: test ordered received material requests  
**Expected**: self.assertEqual(data[1].ordered_qty, 57.0)  
**Confidence**: 0.85  

```python
self.assertEqual(data[0].ordered_qty, 0.0)
self.assertEqual(data[1].ordered_qty, 57.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:45*

### test_get_supplier_group_details

**Category**: method_call  
**Description**: test get supplier group details  
**Expected**: self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')  
**Confidence**: 0.85  

```python
s_doc.get_supplier_group_details()
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:35*

### test_get_supplier_group_details

**Category**: method_call  
**Description**: test get supplier group details  
**Expected**: self.assertEqual(s_doc.accounts[0].company, '_Test Company')  
**Confidence**: 0.85  

```python
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:36*

### test_get_supplier_group_details

**Category**: method_call  
**Description**: test get supplier group details  
**Expected**: self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')  
**Confidence**: 0.85  

```python
self.assertEqual(s_doc.accounts[0].company, '_Test Company')
self.assertEqual(s_doc.accounts[0].account, 'Creditors - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:37*

### test_supplier_country

**Category**: method_call  
**Description**: test supplier country  
**Expected**: self.assertEqual(supplier.country, 'Greece')  
**Confidence**: 0.85  

```python
self.assertTrue('country' in supplier.as_dict())
self.assertEqual(supplier.country, 'Greece')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:113*

### test_supplier_country

**Category**: method_call  
**Description**: test supplier country  
**Expected**: self.assertEqual(supplier.country, 'Greece')  
**Confidence**: 0.85  

```python
supplier.save()
self.assertEqual(supplier.country, 'Greece')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:121*

### test_get_supplier_group_details

**Category**: method_call  
**Description**: test get supplier group details  
**Expected**: self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')  
**Confidence**: 0.85  

```python
s_doc.get_supplier_group_details()
self.assertEqual(s_doc.payment_terms, '_Test Payment Term Template 3')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier/test_supplier.py:35*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[0]['subcontract_order'], sco.name)  
**Confidence**: 0.85  

```python
self.assertEqual(len(sco_data), 2)
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:63*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:64*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[0]['p_qty'], 8)  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[0]['rm_item_code'], '_Test Item')
self.assertEqual(sco_data[0]['p_qty'], 8)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:66*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[0]['transferred_qty'], 2)  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[0]['p_qty'], 8)
self.assertEqual(sco_data[0]['transferred_qty'], 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:67*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[0]['transferred_qty'], 2)
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:68*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[1]['p_qty'], 19)  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[1]['rm_item_code'], '_Test Item Home Desktop 100')
self.assertEqual(sco_data[1]['p_qty'], 19)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:70*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[1]['transferred_qty'], 1)  
**Confidence**: 0.85  

```python
self.assertEqual(sco_data[1]['p_qty'], 19)
self.assertEqual(sco_data[1]['transferred_qty'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:71*

### test_pending_and_transferred_qty

**Category**: method_call  
**Description**: test pending and transferred qty  
**Expected**: self.assertEqual(sco_data[0]['subcontract_order'], sco.name)  
**Confidence**: 0.85  

```python
self.assertEqual(len(sco_data), 2)
self.assertEqual(sco_data[0]['subcontract_order'], sco.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_raw_materials_to_be_transferred/test_subcontracted_raw_materials_to_be_transferred.py:63*

### test_update_child_supplier_quotation_add_item

**Category**: method_call  
**Description**: test update child supplier quotation add item  
**Expected**: self.assertEqual(sq.get('items')[0].qty, 5)  
**Confidence**: 0.85  

```python
sq.reload()
self.assertEqual(sq.get('items')[0].qty, 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:32*

### test_update_child_supplier_quotation_add_item

**Category**: method_call  
**Description**: test update child supplier quotation add item  
**Expected**: self.assertEqual(sq.get('items')[1].rate, 300)  
**Confidence**: 0.85  

```python
self.assertEqual(sq.get('items')[0].qty, 5)
self.assertEqual(sq.get('items')[1].rate, 300)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:33*

### test_update_child_supplier_quotation_add_item

**Category**: method_call  
**Description**: test update child supplier quotation add item  
**Expected**: self.assertEqual(sq.get('items')[1].description, 'test')  
**Confidence**: 0.85  

```python
self.assertEqual(sq.get('items')[1].rate, 300)
self.assertEqual(sq.get('items')[1].description, 'test')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:34*

### test_update_supplier_quotation_child_remove_item

**Category**: method_call  
**Description**: test update supplier quotation child remove item  
**Expected**: self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)  
**Confidence**: 0.85  

```python
frappe.db.savepoint('before_cancel')
self.assertRaises(frappe.LinkExistsError, update_child_qty_rate, 'Supplier Quotation', trans_item, sq.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:89*

### test_update_supplier_quotation_child_remove_item

**Category**: method_call  
**Description**: test update supplier quotation child remove item  
**Expected**: self.assertEqual(len(sq.get('items')), 1)  
**Confidence**: 0.85  

```python
sq.reload()
self.assertEqual(len(sq.get('items')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:108*

### test_supplier_quotation_qty

**Category**: method_call  
**Description**: test supplier quotation qty  
**Expected**: self.assertEqual(sq.items[0].qty, 1)  
**Confidence**: 0.85  

```python
sq.save()
self.assertEqual(sq.items[0].qty, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_quotation/test_supplier_quotation.py:119*

### test_variable_exist

**Category**: instantiation  
**Description**: Instantiate get_doc: test variable exist  
**Confidence**: 0.80  

```python
my_doc = frappe.get_doc('Supplier Scorecard Variable', d.get('name'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_scorecard_variable/test_supplier_scorecard_variable.py:16*

### test_variable_exist

**Category**: instantiation  
**Description**: Instantiate get_doc: test variable exist  
**Confidence**: 0.80  

```python
my_doc = frappe.get_doc('Supplier Scorecard Variable', d.get('name'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/doctype/supplier_scorecard_variable/test_supplier_scorecard_variable.py:16*

### test_pending_and_received_qty

**Category**: instantiation  
**Description**: Instantiate get_subcontracting_order: test pending and received qty  
**Expected**: self.assertEqual(data[0]['pending_qty'], 5)  
**Confidence**: 0.80  

```python
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:40*

### test_pending_and_received_qty

**Category**: instantiation  
**Description**: Instantiate get_rm_items: test pending and received qty  
**Expected**: self.assertEqual(data[0]['pending_qty'], 5)  
**Confidence**: 0.80  

```python
rm_items = get_rm_items(sco.supplied_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/subcontracted_item_to_be_received/test_subcontracted_item_to_be_received.py:43*

### test_date_range

**Category**: instantiation  
**Description**: Instantiate get_data: test date range  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.80  

```python
# Setup
create_item('Test MR Report Item')
self.setup_material_request()
self.setup_material_request(order=True, days=1)
self.setup_material_request(order=True, receive=True, days=2)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='Test MR Report Item')

data = get_data(self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:34*

### test_date_range

**Category**: instantiation  
**Description**: Instantiate get_data: test date range  
**Expected**: self.assertEqual(len(data), 0)  
**Confidence**: 0.80  

```python
# Setup
create_item('Test MR Report Item')
self.setup_material_request()
self.setup_material_request(order=True, days=1)
self.setup_material_request(order=True, receive=True, days=2)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='Test MR Report Item')

data = get_data(self.filters.update({'from_date': add_days(today(), 10)}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:37*

### test_ordered_received_material_requests

**Category**: instantiation  
**Description**: Instantiate get_data: test ordered received material requests  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.80  

```python
# Setup
create_item('Test MR Report Item')
self.setup_material_request()
self.setup_material_request(order=True, days=1)
self.setup_material_request(order=True, receive=True, days=2)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='Test MR Report Item')

data = get_data(self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:41*

### test_date_range

**Category**: instantiation  
**Description**: Instantiate get_data: test date range  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.80  

```python
data = get_data(self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:34*

### test_date_range

**Category**: instantiation  
**Description**: Instantiate get_data: test date range  
**Expected**: self.assertEqual(len(data), 0)  
**Confidence**: 0.80  

```python
data = get_data(self.filters.update({'from_date': add_days(today(), 10)}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:37*

### test_ordered_received_material_requests

**Category**: instantiation  
**Description**: Instantiate get_data: test ordered received material requests  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.80  

```python
data = get_data(self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/buying/report/requested_items_to_order_and_receive/test_requested_items_to_order_and_receive.py:41*

