# Test Example Extraction Report

**Total Examples**: 86  
**High Value Examples** (confidence > 0.7): 86  
**Average Complexity**: 0.66  

## Examples by Category

- **config**: 4
- **instantiation**: 28
- **method_call**: 2
- **workflow**: 52

## Examples by Language

- **Python**: 86

## Extracted Examples

### test_01_so_to_deliver_and_bill

**Category**: workflow  
**Description**: Workflow: test 01 so to deliver and bill  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver and Bill']})
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 10, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:54*

### test_02_so_to_deliver

**Category**: workflow  
**Description**: Workflow: test 02 so to deliver  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_sales_invoice(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver']})
expected_value = {'status': 'To Deliver', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 0, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:80*

### test_03_so_to_bill

**Category**: workflow  
**Description**: Workflow: test 03 so to bill  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_delivery_note(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Bill']})
expected_value = {'status': 'To Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 10, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:107*

### test_04_so_completed

**Category**: workflow  
**Description**: Workflow: test 04 so completed  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_sales_invoice(so)
self.create_delivery_note(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['Completed']})
expected_value = {'status': 'Completed', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 0, 'billed_qty': 10, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:134*

### test_06_so_pending_delivery_with_multiple_delivery_notes

**Category**: workflow  
**Description**: Workflow: test 06 so pending delivery with multiple delivery notes  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
sinv1 = self.create_sales_invoice(so, do_not_save=True)
sinv1.items[0].qty = 2
sinv1 = sinv1.save().submit()
dn1 = self.create_delivery_note(so, do_not_save=True)
dn1.items[0].qty = 2
dn1 = dn1.save().submit()
sinv2 = self.create_sales_invoice(so, do_not_save=True)
sinv2.items[0].qty = 2
sinv2 = sinv2.save().submit()
dn2 = self.create_delivery_note(so, do_not_save=True)
dn2.items[0].qty = 1
dn2 = dn2.save().submit()
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 3, 'pending_qty': 7, 'qty_to_bill': 6, 'billed_qty': 4, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:174*

### test_07_so_delivered_with_multiple_delivery_notes

**Category**: workflow  
**Description**: Workflow: test 07 so delivered with multiple delivery notes  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
dn1 = self.create_delivery_note(so, do_not_save=True)
dn1.items[0].qty = 5
dn1 = dn1.save().submit()
dn2 = self.create_delivery_note(so, do_not_save=True)
dn2.items[0].qty = 5
dn2 = dn2.save().submit()
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'sales_order': [so.name]})
expected_value = {'status': 'To Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 10, 'billed_qty': 0, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:220*

### test_01_so_to_deliver_and_bill

**Category**: workflow  
**Description**: Workflow: test 01 so to deliver and bill  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver and Bill']})
expected_value = {'status': 'To Deliver and Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 10, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:54*

### test_02_so_to_deliver

**Category**: workflow  
**Description**: Workflow: test 02 so to deliver  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_sales_invoice(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Deliver']})
expected_value = {'status': 'To Deliver', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 0, 'pending_qty': 10, 'qty_to_bill': 0, 'time_taken_to_deliver': 0}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:80*

### test_03_so_to_bill

**Category**: workflow  
**Description**: Workflow: test 03 so to bill  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_delivery_note(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['To Bill']})
expected_value = {'status': 'To Bill', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 10, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:107*

### test_04_so_completed

**Category**: workflow  
**Description**: Workflow: test 04 so completed  
**Expected**: self.assertEqual(len(data), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-01'
item, so = self.create_sales_order(transaction_date)
self.create_sales_invoice(so)
self.create_delivery_note(so)
columns, data, message, chart = execute({'company': '_Test Company', 'from_date': '2021-06-01', 'to_date': '2021-06-30', 'status': ['Completed']})
expected_value = {'status': 'Completed', 'sales_order': so.name, 'delay_days': frappe.utils.date_diff(frappe.utils.datetime.date.today(), so.delivery_date), 'qty': 10, 'delivered_qty': 10, 'pending_qty': 0, 'qty_to_bill': 0, 'billed_qty': 10, 'time_taken_to_deliver': 86400}
self.assertEqual(len(data), 1)
for key, val in expected_value.items():
    with self.subTest(key=key, val=val):
        self.assertEqual(data[0][key], val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_order_analysis/test_sales_order_analysis.py:134*

### test_result_for_partial_material_request

**Category**: workflow  
**Description**: Workflow: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order()
mr = make_material_request(so.name)
mr.items[0].qty = 4
mr.schedule_date = add_months(nowdate(), 1)
mr.submit()
report = execute()
l = len(report[1])
self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:16*

### test_result_for_partial_material_request

**Category**: workflow  
**Description**: Workflow: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order()
mr = make_material_request(so.name)
mr.items[0].qty = 4
mr.schedule_date = add_months(nowdate(), 1)
mr.submit()
report = execute()
l = len(report[1])
self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:16*

### test_sales_order_with_negative_rate

**Category**: workflow  
**Description**: Workflow: Test if negative rate is allowed in Sales Order via doc submission and update items  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

'\n\t\tTest if negative rate is allowed in Sales Order via doc submission and update items\n\t\t'
so = make_sales_order(qty=1, rate=100, do_not_save=True)
so.append('items', {'item_code': '_Test Item', 'qty': 1, 'rate': -10})
so.save()
so.submit()
first_item = so.get('items')[0]
second_item = so.get('items')[1]
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': first_item.qty, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': -20, 'qty': second_item.qty, 'docname': second_item.name}])
update_child_qty_rate('Sales Order', trans_item, so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:61*

### test_so_billed_amount_against_return_entry

**Category**: workflow  
**Description**: Workflow: test so billed amount against return entry  
**Expected**: self.assertEqual(so.per_billed, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

from erpnext.accounts.doctype.sales_invoice.sales_invoice import make_sales_return
so = make_sales_order(do_not_submit=True)
so.submit()
si = make_sales_invoice(so.name)
si.insert()
si.submit()
si1 = make_sales_return(si.name)
si1.update_billed_amount_in_sales_order = 1
si1.submit()
so.load_from_db()
self.assertEqual(so.per_billed, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:165*

### test_update_qty

**Category**: workflow  
**Description**: Workflow: test update qty  
**Expected**: self.assertEqual(so.get('items')[0].delivered_qty, 9)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

so = make_sales_order()
create_dn_against_so(so.name, 6)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 6)
si1 = make_sales_invoice(so.name)
si1.get('items')[0].qty = 6
si1.insert()
si1.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 6)
si2 = make_sales_invoice(so.name)
si2.set('update_stock', 1)
si2.get('items')[0].qty = 3
si2.insert()
si2.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 9)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:244*

### test_return_against_sales_order

**Category**: workflow  
**Description**: Workflow: test return against sales order  
**Expected**: self.assertEqual(so.get('items')[0].delivered_qty, 5)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

so = make_sales_order()
dn = create_dn_against_so(so.name, 6)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 6)
si2 = make_sales_invoice(so.name)
si2.set('update_stock', 1)
si2.get('items')[0].qty = 3
si2.insert()
si2.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 9)
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-3, do_not_submit=True)
dn1.items[0].against_sales_order = so.name
dn1.items[0].so_detail = so.items[0].name
dn1.submit()
si1 = create_sales_invoice(is_return=1, return_against=si2.name, qty=-1, update_stock=1, do_not_submit=True)
si1.items[0].sales_order = so.name
si1.items[0].so_detail = so.items[0].name
si1.submit()
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:271*

### test_reserved_qty_for_over_delivery_via_sales_invoice

**Category**: workflow  
**Description**: Workflow: test reserved qty for over delivery via sales invoice  
**Expected**: self.assertEqual(so.per_delivered, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
frappe.db.set_value('Item', '_Test Item', 'over_delivery_receipt_allowance', 50)
frappe.db.set_value('Item', '_Test Item', 'over_billing_allowance', 20)
existing_reserved_qty = get_reserved_qty()
so = make_sales_order()
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
si = make_sales_invoice(so.name)
si.update_stock = 1
si.get('items')[0].qty = 12
si.insert()
si.submit()
self.assertEqual(get_reserved_qty(), existing_reserved_qty)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 12)
self.assertEqual(so.per_delivered, 100)
si.cancel()
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 10)
so.load_from_db()
self.assertEqual(so.get('items')[0].delivered_qty, 0)
self.assertEqual(so.per_delivered, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:353*

### test_reserved_qty_for_partial_delivery_with_packing_list

**Category**: workflow  
**Description**: Workflow: test reserved qty for partial delivery with packing list  
**Expected**: self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
make_stock_entry(item='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=10, rate=100)
existing_reserved_qty_item1 = get_reserved_qty('_Test Item')
existing_reserved_qty_item2 = get_reserved_qty('_Test Item Home Desktop 100')
so = make_sales_order(item_code='_Test Product Bundle Item')
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
dn = create_dn_against_so(so.name)
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 25)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 10)
so.load_from_db()
so.update_status('Closed')
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)
so.load_from_db()
so.update_status('Draft')
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 25)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 10)
dn.cancel()
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
so.load_from_db()
so.cancel()
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:384*

### test_reserved_qty_for_over_delivery_with_packing_list

**Category**: workflow  
**Description**: Workflow: test reserved qty for over delivery with packing list  
**Expected**: self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

make_stock_entry(target='_Test Warehouse - _TC', qty=10, rate=100)
make_stock_entry(item='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=10, rate=100)
frappe.db.set_value('Item', '_Test Product Bundle Item', 'over_delivery_receipt_allowance', 50)
existing_reserved_qty_item1 = get_reserved_qty('_Test Item')
existing_reserved_qty_item2 = get_reserved_qty('_Test Item Home Desktop 100')
so = make_sales_order(item_code='_Test Product Bundle Item')
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
dn = create_dn_against_so(so.name, 15)
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2)
dn.cancel()
self.assertEqual(get_reserved_qty('_Test Item'), existing_reserved_qty_item1 + 50)
self.assertEqual(get_reserved_qty('_Test Item Home Desktop 100'), existing_reserved_qty_item2 + 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:431*

### test_update_child_adding_new_item

**Category**: workflow  
**Description**: Workflow: test update child adding new item  
**Expected**: self.assertNotEqual(updated_total_in_words, prev_total_in_words)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

so = make_sales_order(item_code='_Test Item', qty=4)
create_dn_against_so(so.name, 4)
make_sales_invoice(so.name)
prev_total = so.get('base_total')
prev_total_in_words = so.get('base_in_words')
reserved_qty_for_second_item = get_reserved_qty('_Test Item 2')
first_item_of_so = so.get('items')[0]
trans_item = json.dumps([{'item_code': first_item_of_so.item_code, 'rate': first_item_of_so.rate, 'qty': first_item_of_so.qty, 'docname': first_item_of_so.name}, {'item_code': '_Test Item 2', 'rate': 200, 'qty': 7}])
update_child_qty_rate('Sales Order', trans_item, so.name)
so.reload()
self.assertEqual(so.get('items')[-1].item_code, '_Test Item 2')
self.assertEqual(so.get('items')[-1].rate, 200)
self.assertEqual(so.get('items')[-1].qty, 7)
self.assertEqual(so.get('items')[-1].amount, 1400)
self.assertEqual(get_reserved_qty('_Test Item 2'), reserved_qty_for_second_item + 7)
self.assertEqual(so.status, 'To Deliver and Bill')
updated_total = so.get('base_total')
updated_total_in_words = so.get('base_in_words')
self.assertEqual(updated_total, prev_total + 1400)
self.assertNotEqual(updated_total_in_words, prev_total_in_words)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:455*

### test_update_child_removing_item

**Category**: workflow  
**Description**: Workflow: test update child removing item  
**Expected**: self.assertEqual(so.status, 'To Deliver and Bill')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

so = make_sales_order(**{'item_list': [{'item_code': '_Test Item', 'qty': 5, 'rate': 1000}]})
create_dn_against_so(so.name, 2)
make_sales_invoice(so.name)
reserved_qty_for_second_item = get_reserved_qty('_Test Item 2')
trans_item = json.dumps([{'item_code': '_Test Item', 'qty': 5, 'rate': 1000, 'docname': so.get('items')[0].name}, {'item_code': '_Test Item 2', 'qty': 2, 'rate': 500}])
update_child_qty_rate('Sales Order', trans_item, so.name)
so.reload()
self.assertEqual(len(so.get('items')), 2)
self.assertEqual(get_reserved_qty('_Test Item 2'), reserved_qty_for_second_item + 2)
trans_item = json.dumps([{'item_code': '_Test Item 2', 'qty': 2, 'rate': 500, 'docname': so.get('items')[1].name}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Sales Order', trans_item, so.name)
trans_item = json.dumps([{'item_code': '_Test Item', 'qty': 5, 'rate': 1000, 'docname': so.get('items')[0].name}])
update_child_qty_rate('Sales Order', trans_item, so.name)
so.reload()
self.assertEqual(len(so.get('items')), 1)
self.assertEqual(get_reserved_qty('_Test Item 2'), reserved_qty_for_second_item)
self.assertEqual(so.status, 'To Deliver and Bill')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:497*

### test_update_child

**Category**: workflow  
**Description**: Workflow: test update child  
**Expected**: self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Sales Order', trans_item, so.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.create_customer('_Test Customer Credit')

so = make_sales_order(item_code='_Test Item', qty=4)
create_dn_against_so(so.name, 4)
make_sales_invoice(so.name)
existing_reserved_qty = get_reserved_qty()
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 7, 'docname': so.items[0].name}])
update_child_qty_rate('Sales Order', trans_item, so.name)
so.reload()
self.assertEqual(so.get('items')[0].rate, 200)
self.assertEqual(so.get('items')[0].qty, 7)
self.assertEqual(so.get('items')[0].amount, 1400)
self.assertEqual(so.status, 'To Deliver and Bill')
self.assertEqual(get_reserved_qty(), existing_reserved_qty + 3)
trans_item = json.dumps([{'item_code': '_Test Item', 'rate': 200, 'qty': 2, 'docname': so.items[0].name}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Sales Order', trans_item, so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/sales_order/test_sales_order.py:539*

### test_achieved_target_and_variance

**Category**: workflow  
**Description**: Workflow: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

distribution = create_target_distribution(self.fiscal_year)
person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
so = make_sales_order(rate=1000, qty=20, do_not_submit=True)
so.set('sales_team', [{'sales_person': person_1.name, 'allocated_percentage': 50, 'allocated_amount': 10000}, {'sales_person': person_2.name, 'allocated_percentage': 50, 'allocated_amount': 10000}])
so.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Order', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:19*

### test_achieved_target_and_variance

**Category**: workflow  
**Description**: Workflow: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
distribution = create_target_distribution(self.fiscal_year)
person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
so = make_sales_order(rate=1000, qty=20, do_not_submit=True)
so.set('sales_team', [{'sales_person': person_1.name, 'allocated_percentage': 50, 'allocated_amount': 10000}, {'sales_person': person_2.name, 'allocated_percentage': 50, 'allocated_amount': 10000}])
so.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Order', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:19*

### test_achieved_target_and_variance_for_partner

**Category**: workflow  
**Description**: Workflow: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

distribution = create_target_distribution(self.fiscal_year)
sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
si.sales_partner = sales_partner.name
si.commission_rate = 5
si.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Invoice', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:23*

### test_achieved_target_and_variance_for_partner

**Category**: workflow  
**Description**: Workflow: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
distribution = create_target_distribution(self.fiscal_year)
sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
si.sales_partner = sales_partner.name
si.commission_rate = 5
si.submit()
result = execute(frappe._dict({'fiscal_year': self.fiscal_year, 'doctype': 'Sales Invoice', 'period': 'Yearly', 'target_on': 'Quantity'}))[1]
row = frappe._dict(result[0])
self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:23*

### test_get_customer_group_details

**Category**: workflow  
**Description**: Workflow: test get customer group details  
**Expected**: self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doc = frappe.new_doc('Customer Group')
doc.customer_group_name = '_Testing Customer Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
doc.default_price_list = 'Standard Buying'
doc.credit_limits = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
test_credit_limits = {'company': '_Test Company', 'credit_limit': 350000}
doc.append('accounts', test_account_details)
doc.append('credit_limits', test_credit_limits)
doc.insert()
c_doc = frappe.new_doc('Customer')
c_doc.customer_name = 'Testing Customer'
c_doc.customer_group = '_Testing Customer Group'
c_doc.payment_terms = c_doc.default_price_list = ''
c_doc.accounts = []
c_doc.credit_limits = []
c_doc.insert()
c_doc.get_customer_group_details()
self.assertEqual(c_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(c_doc.accounts[0].company, '_Test Company')
self.assertEqual(c_doc.accounts[0].account, 'Creditors - _TC')
self.assertEqual(c_doc.credit_limits[0].company, '_Test Company')
self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)
c_doc.delete()
doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:28*

### test_party_details

**Category**: workflow  
**Description**: Workflow: test party details  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.party import get_party_details
to_check = {'selling_price_list': None, 'customer_group': '_Test Customer Group', 'contact_designation': None, 'customer_address': '_Test Address for Customer-Office', 'contact_department': None, 'contact_email': 'test_contact_customer@example.com', 'contact_mobile': None, 'sales_team': [], 'contact_display': '_Test Contact for _Test Customer', 'contact_person': '_Test Contact for _Test Customer-_Test Customer', 'territory': '_Test Territory', 'contact_phone': '+91 0000000000', 'customer_name': '_Test Customer'}
create_test_contact_and_address()
frappe.db.set_value('Contact', '_Test Contact for _Test Customer-_Test Customer', 'is_primary_contact', 1)
details = get_party_details('_Test Customer')
for key, value in to_check.items():
    val = details.get(key)
    if not val and (not isinstance(val, list)):
        val = None
    self.assertEqual(value, val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:62*

### test_party_details_tax_category

**Category**: workflow  
**Description**: Workflow: test party details tax category  
**Expected**: self.assertEqual(details.tax_category, '_Test Tax Category 3')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.party import get_party_details
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Billing')
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Shipping')
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 1')
billing_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 2', address_type='Billing', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
shipping_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 3', address_type='Shipping', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
settings = frappe.get_single('Accounts Settings')
rollback_setting = settings.determine_address_tax_category_from
settings.determine_address_tax_category_from = 'Billing Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 2')
settings.determine_address_tax_category_from = 'Shipping Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 3')
settings.determine_address_tax_category_from = rollback_setting
settings.save()
billing_address.delete()
shipping_address.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:96*

### test_customer_credit_limit

**Category**: workflow  
**Description**: Workflow: test customer credit limit  
**Expected**: self.assertRaises(frappe.ValidationError, si.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
outstanding_amt = self.get_customer_outstanding_amount()
credit_limit = get_credit_limit('_Test Customer', '_Test Company')
if outstanding_amt <= 0.0:
    item_qty = int((abs(outstanding_amt) + 200) / 100)
    make_sales_order(qty=item_qty)
if not credit_limit:
    set_credit_limit('_Test Customer', '_Test Company', outstanding_amt - 50)
so = make_sales_order(do_not_submit=True)
self.assertRaises(frappe.ValidationError, so.submit)
dn = create_delivery_note(do_not_submit=True)
self.assertRaises(frappe.ValidationError, dn.submit)
si = create_sales_invoice(do_not_submit=True)
self.assertRaises(frappe.ValidationError, si.submit)
if credit_limit > outstanding_amt:
    set_credit_limit('_Test Customer', '_Test Company', credit_limit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:256*

### test_customer_credit_limit_after_submit

**Category**: workflow  
**Description**: Workflow: test customer credit limit after submit  
**Expected**: self.assertRaises(frappe.ValidationError, update_child_qty_rate, so.doctype, json.dumps([modified_item]), so.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.controllers.accounts_controller import update_child_qty_rate
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
outstanding_amt = self.get_customer_outstanding_amount()
credit_limit = get_credit_limit('_Test Customer', '_Test Company')
if outstanding_amt <= 0.0:
    item_qty = int((abs(outstanding_amt) + 200) / 100)
    make_sales_order(qty=item_qty)
if credit_limit <= 0.0:
    set_credit_limit('_Test Customer', '_Test Company', outstanding_amt + 100)
so = make_sales_order(rate=100, qty=1)
fields = ['name', 'item_code', 'delivery_date', 'conversion_factor', 'qty', 'rate', 'uom', 'idx']
modified_item = frappe._dict()
for x in fields:
    modified_item[x] = so.items[0].get(x)
modified_item['docname'] = so.items[0].name
modified_item['qty'] = 2
self.assertRaises(frappe.ValidationError, update_child_qty_rate, so.doctype, json.dumps([modified_item]), so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:286*

### test_customer_payment_terms

**Category**: workflow  
**Description**: Workflow: test customer payment terms  
**Expected**: self.assertEqual(due_date, '2017-01-22')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 3')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2016-02-21')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2017-02-21')
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '_Test Payment Term Template 1')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2016-02-29')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer With Template')
self.assertEqual(due_date, '2017-02-28')
frappe.db.set_value('Customer', '_Test Customer With Template', 'payment_terms', '')
due_date = get_due_date('2016-01-22', 'Customer', '_Test Customer')
self.assertEqual(due_date, '2016-01-22')
due_date = get_due_date('2017-01-22', 'Customer', '_Test Customer')
self.assertEqual(due_date, '2017-01-22')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:329*

### test_parse_full_name

**Category**: workflow  
**Description**: Workflow: test parse full name  
**Expected**: self.assertEqual(last, 'Doe')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
first, middle, last = parse_full_name('John')
self.assertEqual(first, 'John')
self.assertEqual(middle, None)
self.assertEqual(last, None)
first, middle, last = parse_full_name('John Doe')
self.assertEqual(first, 'John')
self.assertEqual(middle, None)
self.assertEqual(last, 'Doe')
first, middle, last = parse_full_name('John Michael Doe')
self.assertEqual(first, 'John')
self.assertEqual(middle, 'Michael')
self.assertEqual(last, 'Doe')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:359*

### test_get_customer_group_details

**Category**: workflow  
**Description**: Workflow: test get customer group details  
**Expected**: self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doc = frappe.new_doc('Customer Group')
doc.customer_group_name = '_Testing Customer Group'
doc.payment_terms = '_Test Payment Term Template 3'
doc.accounts = []
doc.default_price_list = 'Standard Buying'
doc.credit_limits = []
test_account_details = {'company': '_Test Company', 'account': 'Creditors - _TC'}
test_credit_limits = {'company': '_Test Company', 'credit_limit': 350000}
doc.append('accounts', test_account_details)
doc.append('credit_limits', test_credit_limits)
doc.insert()
c_doc = frappe.new_doc('Customer')
c_doc.customer_name = 'Testing Customer'
c_doc.customer_group = '_Testing Customer Group'
c_doc.payment_terms = c_doc.default_price_list = ''
c_doc.accounts = []
c_doc.credit_limits = []
c_doc.insert()
c_doc.get_customer_group_details()
self.assertEqual(c_doc.payment_terms, '_Test Payment Term Template 3')
self.assertEqual(c_doc.accounts[0].company, '_Test Company')
self.assertEqual(c_doc.accounts[0].account, 'Creditors - _TC')
self.assertEqual(c_doc.credit_limits[0].company, '_Test Company')
self.assertEqual(c_doc.credit_limits[0].credit_limit, 350000)
c_doc.delete()
doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:28*

### test_party_details

**Category**: workflow  
**Description**: Workflow: test party details  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.party import get_party_details
to_check = {'selling_price_list': None, 'customer_group': '_Test Customer Group', 'contact_designation': None, 'customer_address': '_Test Address for Customer-Office', 'contact_department': None, 'contact_email': 'test_contact_customer@example.com', 'contact_mobile': None, 'sales_team': [], 'contact_display': '_Test Contact for _Test Customer', 'contact_person': '_Test Contact for _Test Customer-_Test Customer', 'territory': '_Test Territory', 'contact_phone': '+91 0000000000', 'customer_name': '_Test Customer'}
create_test_contact_and_address()
frappe.db.set_value('Contact', '_Test Contact for _Test Customer-_Test Customer', 'is_primary_contact', 1)
details = get_party_details('_Test Customer')
for key, value in to_check.items():
    val = details.get(key)
    if not val and (not isinstance(val, list)):
        val = None
    self.assertEqual(value, val)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:62*

### test_party_details_tax_category

**Category**: workflow  
**Description**: Workflow: test party details tax category  
**Expected**: self.assertEqual(details.tax_category, '_Test Tax Category 3')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.party import get_party_details
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Billing')
frappe.delete_doc_if_exists('Address', '_Test Address With Tax Category-Shipping')
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 1')
billing_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 2', address_type='Billing', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
shipping_address = frappe.get_doc(doctype='Address', address_title='_Test Address With Tax Category', tax_category='_Test Tax Category 3', address_type='Shipping', address_line1='Station Road', city='_Test City', country='India', links=[dict(link_doctype='Customer', link_name='_Test Customer With Tax Category')]).insert()
settings = frappe.get_single('Accounts Settings')
rollback_setting = settings.determine_address_tax_category_from
settings.determine_address_tax_category_from = 'Billing Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 2')
settings.determine_address_tax_category_from = 'Shipping Address'
settings.save()
details = get_party_details('_Test Customer With Tax Category')
self.assertEqual(details.tax_category, '_Test Tax Category 3')
settings.determine_address_tax_category_from = rollback_setting
settings.save()
billing_address.delete()
shipping_address.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/customer/test_customer.py:96*

### test_update_child_quotation_add_item

**Category**: workflow  
**Description**: Workflow: test update child quotation add item  
**Expected**: self.assertEqual(qo.get('items')[1].description, 'test')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.item.test_item import make_item
item_1 = make_item('_Test Item')
item_2 = make_item('_Test Item 1')
item_list = [{'item_code': item_1.item_code, 'warehouse': '', 'qty': 10, 'rate': 300}, {'item_code': item_2.item_code, 'warehouse': '', 'qty': 5, 'rate': 400}]
qo = make_quotation(item_list=item_list)
first_item = qo.get('items')[0]
second_item = qo.get('items')[1]
trans_item = json.dumps([{'item_code': first_item.item_code, 'rate': first_item.rate, 'qty': 11, 'docname': first_item.name}, {'item_code': second_item.item_code, 'rate': second_item.rate, 'qty': second_item.qty, 'docname': second_item.name, 'description': 'test'}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
update_child_qty_rate('Quotation', trans_item, qo.name)
qo.reload()
self.assertEqual(qo.get('items')[0].qty, 11)
self.assertEqual(qo.get('items')[-1].rate, 100)
self.assertEqual(qo.get('items')[1].description, 'test')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:17*

### test_update_child_removing_item

**Category**: workflow  
**Description**: Workflow: test update child removing item  
**Expected**: self.assertEqual(len(qo.get('items')), 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
qo = make_quotation(qty=10)
sales_order = make_sales_order(qo.name)
sales_order.delivery_date = nowdate()
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}, {'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
update_child_qty_rate('Quotation', trans_item, qo.name)
sales_order.submit()
qo.reload()
self.assertEqual(qo.status, 'Partially Ordered')
trans_item = json.dumps([{'item_code': '_Test Item 2', 'rate': 100, 'qty': 7}])
self.assertRaises(frappe.ValidationError, update_child_qty_rate, 'Quotation', trans_item, qo.name)
trans_item = json.dumps([{'item_code': qo.items[0].item_code, 'rate': qo.items[0].rate, 'qty': qo.items[0].qty, 'docname': qo.items[0].name}])
update_child_qty_rate('Quotation', trans_item, qo.name)
qo.reload()
self.assertEqual(len(qo.get('items')), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:75*

### test_make_sales_order_terms_copied

**Category**: workflow  
**Description**: Workflow: test make sales order terms copied  
**Expected**: self.assertTrue(sales_order.get('payment_schedule'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
quotation.submit()
sales_order = make_sales_order(quotation.name)
self.assertTrue(sales_order.get('payment_schedule'))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:145*

### test_do_not_add_ordered_items_in_new_sales_order

**Category**: workflow  
**Description**: Workflow: test do not add ordered items in new sales order  
**Expected**: self.assertEqual(sales_order.items[0].qty, 5.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('_Test Item for Quotation for SO', {'is_stock_item': 1})
quotation = make_quotation(qty=5, do_not_submit=True)
quotation.append('items', {'item_code': item.name, 'qty': 5, 'rate': 100, 'conversion_factor': 1, 'uom': item.stock_uom, 'warehouse': '_Test Warehouse - _TC', 'stock_uom': item.stock_uom})
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.delivery_date = nowdate()
self.assertEqual(len(sales_order.items), 2)
sales_order.remove(sales_order.items[1])
sales_order.submit()
sales_order = make_sales_order(quotation.name)
self.assertEqual(len(sales_order.items), 1)
self.assertEqual(sales_order.items[0].item_code, item.name)
self.assertEqual(sales_order.items[0].qty, 5.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:158*

### test_gross_profit

**Category**: workflow  
**Description**: Workflow: test gross profit  
**Expected**: self.assertEqual(quotation.items[0].gross_profit, 200)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.item.test_item import make_item
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
from erpnext.stock.get_item_details import ItemDetailsCtx, insert_item_price
item_doc = make_item('_Test Item for Gross Profit', {'is_stock_item': 1})
item_code = item_doc.name
make_stock_entry(item_code=item_code, qty=10, rate=100, target='_Test Warehouse - _TC')
selling_price_list = frappe.get_all('Price List', filters={'selling': 1}, limit=1)[0].name
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 1)
insert_item_price(ItemDetailsCtx({'item_code': item_code, 'price_list': selling_price_list, 'price_list_rate': 300, 'rate': 300, 'conversion_factor': 1, 'discount_amount': 0.0, 'currency': frappe.db.get_value('Price List', selling_price_list, 'currency'), 'uom': item_doc.stock_uom}))
quotation = make_quotation(item_code=item_code, qty=1, rate=300, selling_price_list=selling_price_list)
self.assertEqual(quotation.items[0].valuation_rate, 100)
self.assertEqual(quotation.items[0].gross_profit, 200)
frappe.db.set_single_value('Stock Settings', 'auto_insert_price_list_rate_if_missing', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:190*

### test_maintain_rate_in_sales_cycle_is_enforced

**Category**: workflow  
**Description**: Workflow: test maintain rate in sales cycle is enforced  
**Expected**: self.assertRaises(frappe.ValidationError, sales_order.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
maintain_rate = frappe.db.get_single_value('Selling Settings', 'maintain_same_sales_rate')
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', 1)
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.items[0].rate = 1
self.assertRaises(frappe.ValidationError, sales_order.save)
frappe.db.set_single_value('Selling Settings', 'maintain_same_sales_rate', maintain_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:223*

### test_make_sales_order_with_different_currency

**Category**: workflow  
**Description**: Workflow: test make sales order with different currency  
**Expected**: self.assertNotEqual(sales_order.currency, quotation.currency)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.currency = 'USD'
sales_order.conversion_rate = 20.0
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = nowdate()
sales_order.delivery_date = nowdate()
sales_order.insert()
self.assertEqual(sales_order.currency, 'USD')
self.assertNotEqual(sales_order.currency, quotation.currency)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:241*

### test_make_sales_order

**Category**: workflow  
**Description**: Workflow: test make sales order  
**Expected**: self.assertEqual(sales_order.customer, '_Test Customer')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
quotation.submit()
sales_order = make_sales_order(quotation.name)
self.assertEqual(sales_order.doctype, 'Sales Order')
self.assertEqual(len(sales_order.get('items')), 1)
self.assertEqual(sales_order.get('items')[0].doctype, 'Sales Order Item')
self.assertEqual(sales_order.get('items')[0].prevdoc_docname, quotation.name)
self.assertEqual(sales_order.customer, '_Test Customer')
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = nowdate()
sales_order.delivery_date = nowdate()
sales_order.insert()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:261*

### test_make_sales_order_with_terms

**Category**: workflow  
**Description**: Workflow: test make sales order with terms  
**Expected**: self.assertEqual(sales_order.payment_schedule[1].due_date, getdate(add_days(quotation.transaction_date, 30)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
quotation = frappe.copy_doc(self.globalTestRecords['Quotation'][0])
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.update({'payment_terms_template': '_Test Payment Term Template'})
quotation.insert()
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
quotation.save()
quotation.submit()
self.assertEqual(quotation.payment_schedule[0].payment_amount, 8906.0)
self.assertEqual(quotation.payment_schedule[0].due_date, quotation.transaction_date)
self.assertEqual(quotation.payment_schedule[1].payment_amount, 8906.0)
self.assertEqual(quotation.payment_schedule[1].due_date, add_days(quotation.transaction_date, 30))
sales_order = make_sales_order(quotation.name)
self.assertEqual(sales_order.doctype, 'Sales Order')
self.assertEqual(len(sales_order.get('items')), 1)
self.assertEqual(sales_order.get('items')[0].doctype, 'Sales Order Item')
self.assertEqual(sales_order.get('items')[0].prevdoc_docname, quotation.name)
self.assertEqual(sales_order.customer, '_Test Customer')
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = nowdate()
sales_order.delivery_date = nowdate()
sales_order.insert()
sales_order.set('taxes', [])
sales_order.save()
self.assertEqual(sales_order.payment_schedule[0].payment_amount, 8906.0)
self.assertEqual(sales_order.payment_schedule[0].due_date, getdate(quotation.transaction_date))
self.assertEqual(sales_order.payment_schedule[1].payment_amount, 8906.0)
self.assertEqual(sales_order.payment_schedule[1].due_date, getdate(add_days(quotation.transaction_date, 30)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:289*

### test_create_quotation_with_margin

**Category**: workflow  
**Description**: Workflow: test create quotation with margin  
**Expected**: self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.quotation.quotation import make_sales_order
from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note, make_sales_invoice
rate_with_margin = flt(1500 * 18.75 / 100 + 1500)
test_record = dict(self.globalTestRecords['Quotation'][0])
test_record['items'][0]['price_list_rate'] = 1500
test_record['items'][0]['margin_type'] = 'Percentage'
test_record['items'][0]['margin_rate_or_amount'] = 18.75
quotation = frappe.copy_doc(test_record)
quotation.transaction_date = nowdate()
quotation.valid_till = add_months(quotation.transaction_date, 1)
quotation.insert()
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
self.assertRaises(frappe.ValidationError, make_sales_order, quotation.name)
quotation.submit()
sales_order = make_sales_order(quotation.name)
sales_order.naming_series = '_T-Quotation-'
sales_order.transaction_date = '2016-01-01'
sales_order.delivery_date = '2016-01-02'
sales_order.insert()
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
sales_order.submit()
dn = make_delivery_note(sales_order.name)
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
dn.save()
si = make_sales_invoice(sales_order.name)
self.assertEqual(quotation.get('items')[0].rate, rate_with_margin)
si.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/quotation/test_quotation.py:352*

### test_01_payment_terms_status

**Category**: workflow  
**Description**: Workflow: test 01 payment terms status  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
so = make_sales_order(transaction_date='2021-06-15', delivery_date=add_days('2021-06-15', -30), item=item.item_code, qty=10, rate=100000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 100000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:60*

### test_02_alternate_currency

**Category**: workflow  
**Description**: Workflow: test 02 alternate currency  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-15'
self.create_payment_terms_template()
self.create_exchange_rate(transaction_date)
item = create_item(item_code='_Test Excavator 2', is_stock_item=0)
so = make_sales_order(transaction_date=transaction_date, currency='USD', delivery_date=add_days(transaction_date, -30), item=item.item_code, qty=10, rate=10000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.currency = 'USD'
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 3500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 700000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:151*

### test_04_due_date_filter

**Category**: workflow  
**Description**: Workflow: test 04 due date filter  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
transaction_date = nowdate()
so = make_sales_order(transaction_date=add_months(transaction_date, -1), delivery_date=add_days(transaction_date, -15), item=item.item_code, qty=10, rate=100000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
first_due_date = add_days(add_months(transaction_date, -1), 15)
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'item': item.item_code, 'from_due_date': add_months(transaction_date, -1), 'to_due_date': first_due_date}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date.fromisoformat(add_months(transaction_date, -1)), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date.fromisoformat(first_due_date), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(len(data), 1)
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:355*

### test_01_payment_terms_status

**Category**: workflow  
**Description**: Workflow: test 01 payment terms status  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
so = make_sales_order(transaction_date='2021-06-15', delivery_date=add_days('2021-06-15', -30), item=item.item_code, qty=10, rate=100000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 100000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:60*

### test_02_alternate_currency

**Category**: workflow  
**Description**: Workflow: test 02 alternate currency  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
transaction_date = '2021-06-15'
self.create_payment_terms_template()
self.create_exchange_rate(transaction_date)
item = create_item(item_code='_Test Excavator 2', is_stock_item=0)
so = make_sales_order(transaction_date=transaction_date, currency='USD', delivery_date=add_days(transaction_date, -30), item=item.item_code, qty=10, rate=10000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.currency = 'USD'
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'period_start_date': '2021-06-01', 'period_end_date': '2021-06-30', 'item': item.item_code}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 6, 30), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 3500000.0, 'invoices': ',' + sinv.name}, {'name': so.name, 'customer': so.customer, 'submitted': datetime.date(2021, 6, 15), 'status': 'Partly Paid', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date(2021, 7, 15), 'invoice_portion': 50.0, 'currency': frappe.get_cached_value('Company', '_Test Company', 'default_currency'), 'base_payment_amount': 3500000.0, 'paid_amount': 700000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:151*

### test_04_due_date_filter

**Category**: workflow  
**Description**: Workflow: test 04 due date filter  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.create_payment_terms_template()
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
transaction_date = nowdate()
so = make_sales_order(transaction_date=add_months(transaction_date, -1), delivery_date=add_days(transaction_date, -15), item=item.item_code, qty=10, rate=100000, do_not_save=True)
so.po_no = ''
so.taxes_and_charges = ''
so.taxes = ''
so.payment_terms_template = self.template.name
so.save()
so.submit()
sinv = make_sales_invoice(so.name)
sinv.taxes_and_charges = ''
sinv.taxes = ''
sinv.items[0].qty = 6
sinv.insert()
sinv.submit()
first_due_date = add_days(add_months(transaction_date, -1), 15)
columns, data, message, chart = execute(frappe._dict({'company': '_Test Company', 'item': item.item_code, 'from_due_date': add_months(transaction_date, -1), 'to_due_date': first_due_date}))
expected_value = [{'name': so.name, 'customer': so.customer, 'submitted': datetime.date.fromisoformat(add_months(transaction_date, -1)), 'status': 'Completed', 'payment_term': None, 'description': '_Test 50-50', 'due_date': datetime.date.fromisoformat(first_due_date), 'invoice_portion': 50.0, 'currency': 'INR', 'base_payment_amount': 500000.0, 'paid_amount': 500000.0, 'invoices': ',' + sinv.name}]
self.assertEqual(len(data), 1)
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:355*

### test_04_due_date_filter

**Category**: method_call  
**Description**: test 04 due date filter  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:411*

### test_04_due_date_filter

**Category**: method_call  
**Description**: test 04 due date filter  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.85  

```python
self.assertEqual(len(data), 1)
self.assertEqual(data, expected_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:411*

### test_defaults_populated

**Category**: instantiation  
**Description**: Instantiate get_single_value: test defaults populated  
**Expected**: self.assertEqual('Stop', default)  
**Confidence**: 0.80  

```python
default = frappe.db.get_single_value('Selling Settings', 'maintain_same_rate_action')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/selling_settings/test_selling_settings.py:12*

### test_defaults_populated

**Category**: instantiation  
**Description**: Instantiate get_single_value: test defaults populated  
**Expected**: self.assertEqual('Stop', default)  
**Confidence**: 0.80  

```python
default = frappe.db.get_single_value('Selling Settings', 'maintain_same_rate_action')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/selling_settings/test_selling_settings.py:12*

### test_item_query_for_customer

**Category**: instantiation  
**Description**: Instantiate item_query: test item query for customer  
**Expected**: self.assertTrue(self.item.name in flatten(items))  
**Confidence**: 0.80  

```python
# Setup
self.customer = frappe.get_last_doc('Customer')
self.supplier = frappe.get_last_doc('Supplier')
self.item = frappe.get_last_doc('Item')

items = item_query(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=filters, as_dict=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:35*

### test_item_query_for_supplier

**Category**: instantiation  
**Description**: Instantiate item_query: test item query for supplier  
**Expected**: self.assertTrue(self.item.item_group in flatten(items))  
**Confidence**: 0.80  

```python
# Setup
self.customer = frappe.get_last_doc('Customer')
self.supplier = frappe.get_last_doc('Supplier')
self.item = frappe.get_last_doc('Item')

items = item_query(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=filters, as_dict=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:48*

### test_item_query_for_customer

**Category**: instantiation  
**Description**: Instantiate item_query: test item query for customer  
**Expected**: self.assertTrue(self.item.name in flatten(items))  
**Confidence**: 0.80  

```python
items = item_query(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=filters, as_dict=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:35*

### test_item_query_for_supplier

**Category**: instantiation  
**Description**: Instantiate item_query: test item query for supplier  
**Expected**: self.assertTrue(self.item.item_group in flatten(items))  
**Confidence**: 0.80  

```python
items = item_query(doctype='Item', txt='', searchfield='name', start=0, page_len=20, filters=filters, as_dict=False)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:48*

### test_result_for_partial_material_request

**Category**: instantiation  
**Description**: Instantiate make_material_request: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.80  

```python
mr = make_material_request(so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:18*

### test_result_for_partial_material_request

**Category**: instantiation  
**Description**: Instantiate add_months: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.80  

```python
mr.schedule_date = add_months(nowdate(), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:20*

### test_result_for_partial_material_request

**Category**: instantiation  
**Description**: Instantiate make_material_request: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.80  

```python
mr = make_material_request(so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:18*

### test_result_for_partial_material_request

**Category**: instantiation  
**Description**: Instantiate add_months: test result for partial material request  
**Expected**: self.assertEqual(so.items[0].qty - mr.items[0].qty, report[1][l - 1]['pending_qty'])  
**Confidence**: 0.80  

```python
mr.schedule_date = add_months(nowdate(), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/pending_so_items_for_purchase_request/test_pending_so_items_for_purchase_request.py:20*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_target_distribution: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

distribution = create_target_distribution(self.fiscal_year)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:21*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:24*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:27*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

so = make_sales_order(rate=1000, qty=20, do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:32*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate _dict: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

row = frappe._dict(result[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:65*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_target_distribution: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
distribution = create_target_distribution(self.fiscal_year)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:21*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
person_1 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 1', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:24*

### test_achieved_target_and_variance

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 10, -40])  
**Confidence**: 0.80  

```python
person_2 = create_sales_target_doc('Sales Person', 'sales_person_name', 'Sales Person 2', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_person_target_variance_based_on_item_group/test_sales_person_target_variance_based_on_item_group.py:27*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_target_distribution: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

distribution = create_target_distribution(self.fiscal_year)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:25*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:28*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:33*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate _dict: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
# Setup
self.fiscal_year = get_fiscal_year(nowdate())[0]

row = frappe._dict(result[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:53*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_target_distribution: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
distribution = create_target_distribution(self.fiscal_year)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:25*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_sales_target_doc: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
sales_partner = create_sales_target_doc('Sales Partner', 'partner_name', 'Sales Partner 1', self.fiscal_year, distribution.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:28*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate create_sales_invoice: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
si = create_sales_invoice(rate=1000, qty=20, do_not_submit=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:33*

### test_achieved_target_and_variance_for_partner

**Category**: instantiation  
**Description**: Instantiate _dict: test achieved target and variance for partner  
**Expected**: self.assertSequenceEqual([flt(value, 2) for value in (row.total_target, row.total_achieved, row.total_variance)], [50, 20, -30])  
**Confidence**: 0.80  

```python
row = frappe._dict(result[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/sales_partner_target_variance_based_on_item_group/test_sales_partner_target_variance_based_on_item_group.py:53*

### test_01_payment_terms_status

**Category**: instantiation  
**Description**: Instantiate create_item: test 01 payment terms status  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.80  

```python
item = create_item(item_code='_Test Excavator 1', is_stock_item=0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:62*

### test_01_payment_terms_status

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test 01 payment terms status  
**Expected**: self.assertEqual(data, expected_value)  
**Confidence**: 0.80  

```python
so = make_sales_order(transaction_date='2021-06-15', delivery_date=add_days('2021-06-15', -30), item=item.item_code, qty=10, rate=100000, do_not_save=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/report/payment_terms_status_for_sales_order/test_payment_terms_status_for_sales_order.py:63*

### test_item_query_for_customer

**Category**: config  
**Description**: Configuration example: test item query for customer  
**Expected**: self.assertTrue(self.item.name in flatten(items))  
**Confidence**: 0.75  

```python
# Setup
self.customer = frappe.get_last_doc('Customer')
self.supplier = frappe.get_last_doc('Supplier')
self.item = frappe.get_last_doc('Item')

filters = {'is_sales_item': 1, 'customer': self.customer.name}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:34*

### test_item_query_for_supplier

**Category**: config  
**Description**: Configuration example: test item query for supplier  
**Expected**: self.assertTrue(self.item.item_group in flatten(items))  
**Confidence**: 0.75  

```python
# Setup
self.customer = frappe.get_last_doc('Customer')
self.supplier = frappe.get_last_doc('Supplier')
self.item = frappe.get_last_doc('Item')

filters = {'supplier': self.supplier.name, 'is_purchase_item': 1}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:47*

### test_item_query_for_customer

**Category**: config  
**Description**: Configuration example: test item query for customer  
**Expected**: self.assertTrue(self.item.name in flatten(items))  
**Confidence**: 0.75  

```python
filters = {'is_sales_item': 1, 'customer': self.customer.name}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:34*

### test_item_query_for_supplier

**Category**: config  
**Description**: Configuration example: test item query for supplier  
**Expected**: self.assertTrue(self.item.item_group in flatten(items))  
**Confidence**: 0.75  

```python
filters = {'supplier': self.supplier.name, 'is_purchase_item': 1}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/selling/doctype/party_specific_item/test_party_specific_item.py:47*

