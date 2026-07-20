# Test Example Extraction Report

**Total Examples**: 344  
**High Value Examples** (confidence > 0.7): 344  
**Average Complexity**: 0.69  

## Examples by Category

- **config**: 2
- **instantiation**: 68
- **method_call**: 54
- **workflow**: 220

## Examples by Language

- **Python**: 344

## Extracted Examples

### test_normal_inward_outward_queue

**Category**: workflow  
**Description**: Workflow: Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)  
**Expected**: self.assertEqual(data[0][8], 40.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'Reference: Case 1 in stock_ageing_fifo_logic.md (same wh)'
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=30, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=50, stock_value_difference=20, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=-10, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
self.assertTrue(slots['Flask Item']['fifo_queue'])
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(queue[0][0], 20.0)
data = format_report_data(self.filters, slots, self.filters['to_date'])
self.assertEqual(data[0][8], 40.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:14*

### test_insufficient_balance

**Category**: workflow  
**Description**: Workflow: Reference: Case 3 in stock_ageing_fifo_logic.md (same wh)  
**Expected**: self.assertEqual(queue[1][0], 10.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'Reference: Case 3 in stock_ageing_fifo_logic.md (same wh)'
sle = [frappe._dict(name='Flask Item', actual_qty=-30, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=-10, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=10, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=10, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='004', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(queue[0][0], 10.0)
self.assertEqual(queue[1][0], 10.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:66*

### test_basic_stock_reconciliation

**Category**: workflow  
**Description**: Workflow: Ledger (same wh): [+30, reco reset >> 50, -10]
Bal: 40  
**Expected**: self.assertEqual(queue[1][0], 20.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tLedger (same wh): [+30, reco reset >> 50, -10]\n\t\tBal: 40\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=30, qty_after_transaction=30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=50, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=40, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(result['total_qty'], 40.0)
self.assertEqual(queue[0][0], 20.0)
self.assertEqual(queue[1][0], 20.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:128*

### test_sequential_stock_reco_same_warehouse

**Category**: workflow  
**Description**: Workflow: Test back to back stock recos (same warehouse).
Ledger: [reco opening >> +1000, reco reset >> 400, -10]
Bal: 390  
**Expected**: self.assertEqual(queue[0][0], 390.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tTest back to back stock recos (same warehouse).\n\t\tLedger: [reco opening >> +1000, reco reset >> 400, -10]\n\t\tBal: 390\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=390, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='003', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
result = slots['Flask Item']
queue = result['fifo_queue']
self.assertEqual(result['qty_after_transaction'], result['total_qty'])
self.assertEqual(result['total_qty'], 390.0)
self.assertEqual(queue[0][0], 390.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:182*

### test_sequential_stock_reco_different_warehouse

**Category**: workflow  
**Description**: Workflow: Ledger:
WH      | Voucher | Qty
-------------------
WH1 | Reco        | 1000
WH2 | Reco        | 400
WH1 | SE          | -10

Bal: WH1 bal + WH2 bal = 990 + 400 = 1390  
**Expected**: self.assertEqual(sum(item_wh_balances), item_result['qty_after_transaction'])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tLedger:\n\t\tWH\t| Voucher | Qty\n\t\t-------------------\n\t\tWH1 | Reco\t  | 1000\n\t\tWH2 | Reco\t  | 400\n\t\tWH1 | SE\t  | -10\n\n\t\tBal: WH1 bal + WH2 bal = 990 + 400 = 1390\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=1000, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-01', voucher_type='Stock Reconciliation', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=0, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 2', posting_date='2021-12-02', voucher_type='Stock Reconciliation', voucher_no='003', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-10, qty_after_transaction=990, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='004', has_serial_no=False, serial_no=None)]
item_wise_slots, item_wh_wise_slots = generate_item_and_item_wh_wise_slots(filters=self.filters, sle=sle)
item_result = item_wise_slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['qty_after_transaction'], item_result['total_qty'])
self.assertEqual(item_result['total_qty'], 1390.0)
self.assertEqual(queue[0][0], 990.0)
self.assertEqual(queue[1][0], 400.0)
item_wh_balances = [item_wh_wise_slots.get(i).get('qty_after_transaction') for i in item_wh_wise_slots]
self.assertEqual(sum(item_wh_balances), item_result['qty_after_transaction'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:235*

### test_repack_entry_same_item_split_rows

**Category**: workflow  
**Description**: Workflow: Split consumption rows and have single repacked item row (same warehouse).
Ledger:
Item    | Qty | Voucher
------------------------
Item 1  | 500 | 001
Item 1  | -50 | 002 (repack)
Item 1  | -50 | 002 (repack)
Item 1  | 100 | 002 (repack)

Case most likely for batch items. Test time bucket computation.  
**Expected**: self.assertEqual(sum([i[0] for i in queue]), 500.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tSplit consumption rows and have single repacked item row (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty | Voucher\n\t\t------------------------\n\t\tItem 1  | 500 | 001\n\t\tItem 1  | -50 | 002 (repack)\n\t\tItem 1  | -50 | 002 (repack)\n\t\tItem 1  | 100 | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=500, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=450, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=100, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], 500.0)
self.assertEqual(queue[0][0], 400.0)
self.assertEqual(queue[1][0], 50.0)
self.assertEqual(queue[2][0], 50.0)
self.assertEqual(sum([i[0] for i in queue]), 500.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:304*

### test_repack_entry_same_item_overconsume

**Category**: workflow  
**Description**: Workflow: Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 500  | 001
Item 1  | -100 | 002 (repack)
Item 1  | 50   | 002 (repack)

Case most likely for batch items. Test time bucket computation.  
**Expected**: self.assertEqual(sum([i[0] for i in queue]), 450.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 500  | 001\n\t\tItem 1  | -100 | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=500, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-100, qty_after_transaction=400, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=450, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], 450.0)
self.assertEqual(queue[0][0], 400.0)
self.assertEqual(queue[1][0], 50.0)
self.assertEqual(sum([i[0] for i in queue]), 450.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:378*

### test_repack_entry_same_item_overconsume_with_split_rows

**Category**: workflow  
**Description**: Workflow: Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 20   | 001
Item 1  | -50  | 002 (repack)
Item 1  | -50  | 002 (repack)
Item 1  | 50   | 002 (repack)  
**Expected**: self.assertEqual(transfer_bucket[0][0], 50)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 20   | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-80, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
fifo_slots = FIFOSlots(self.filters, sle)
slots = fifo_slots.generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], -30.0)
self.assertEqual(queue[0][0], -30.0)
transfer_bucket = fifo_slots.transferred_item_details['002', 'Flask Item', 'WH 1']
self.assertEqual(transfer_bucket[0][0], 50)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:438*

### test_repack_entry_same_item_overproduce

**Category**: workflow  
**Description**: Workflow: Under consume item and have more repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 500  | 001
Item 1  | -50  | 002 (repack)
Item 1  | 100  | 002 (repack)

Case most likely for batch items. Test time bucket computation.  
**Expected**: self.assertEqual(sum([i[0] for i in queue]), 550.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tUnder consume item and have more repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 500  | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 100  | 002 (repack)\n\n\t\tCase most likely for batch items. Test time bucket computation.\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=500, qty_after_transaction=500, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=450, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=100, qty_after_transaction=550, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
slots = FIFOSlots(self.filters, sle).generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], 550.0)
self.assertEqual(queue[0][0], 450.0)
self.assertEqual(queue[1][0], 50.0)
self.assertEqual(queue[2][0], 50.0)
self.assertEqual(sum([i[0] for i in queue]), 550.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:511*

### test_repack_entry_same_item_overproduce_with_split_rows

**Category**: workflow  
**Description**: Workflow: Over consume item and have less repacked item qty (same warehouse).
Ledger:
Item    | Qty  | Voucher
------------------------
Item 1  | 20   | 001
Item 1  | -50  | 002 (repack)
Item 1  | 50  | 002 (repack)
Item 1  | 50   | 002 (repack)  
**Expected**: self.assertFalse(transfer_bucket)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.filters = frappe._dict(company='_Test Company', to_date='2021-12-10', ranges=['30', '60', '90'])

'\n\t\tOver consume item and have less repacked item qty (same warehouse).\n\t\tLedger:\n\t\tItem\t| Qty  | Voucher\n\t\t------------------------\n\t\tItem 1  | 20   | 001\n\t\tItem 1  | -50  | 002 (repack)\n\t\tItem 1  | 50  | 002 (repack)\n\t\tItem 1  | 50   | 002 (repack)\n\t\t'
sle = [frappe._dict(name='Flask Item', actual_qty=20, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-03', voucher_type='Stock Entry', voucher_no='001', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=-50, qty_after_transaction=-30, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=20, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None), frappe._dict(name='Flask Item', actual_qty=50, qty_after_transaction=70, stock_value_difference=0, warehouse='WH 1', posting_date='2021-12-04', voucher_type='Stock Entry', voucher_no='002', has_serial_no=False, serial_no=None)]
fifo_slots = FIFOSlots(self.filters, sle)
slots = fifo_slots.generate()
item_result = slots['Flask Item']
queue = item_result['fifo_queue']
self.assertEqual(item_result['total_qty'], 70.0)
self.assertEqual(queue[0][0], 20.0)
self.assertEqual(queue[1][0], 50.0)
transfer_bucket = fifo_slots.transferred_item_details['002', 'Flask Item', 'WH 1']
self.assertFalse(transfer_bucket)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_ageing/test_stock_ageing.py:572*

### test_get_available_qty_to_reserve

**Category**: workflow  
**Description**: Workflow: test get available qty to reserve  
**Expected**: self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import get_available_qty_to_reserve
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse)
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, ignore_validate=True)
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse) - sre.reserved_qty
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:55*

### test_update_status

**Category**: workflow  
**Description**: Workflow: test update status  
**Expected**: self.assertEqual(sre.status, 'Cancelled')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, reserved_qty=30, ignore_validate=True, do_not_submit=True)
sre.load_from_db()
self.assertEqual(sre.status, 'Draft')
sre.submit()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Reserved')
sre.reserved_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Reserved')
sre.delivered_qty = 10
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Delivered')
sre.delivered_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Delivered')
sre.cancel()
sre.load_from_db()
self.assertEqual(sre.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:79*

### test_update_reserved_qty_in_voucher

**Category**: workflow  
**Description**: Workflow: test update reserved qty in voucher  
**Expected**: self.assertEqual(so.items[0].stock_reserved_qty, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
so.reserve_stock = 0
so.items[0].reserve_stock = 1
so.save()
so.submit()
sre1 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=30)
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty)
sre2 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=20)
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty + sre2.reserved_qty)
sre1.cancel()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.reserved_qty += sre1.reserved_qty
sre2.save()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre2.status, 'Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.cancel()
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:126*

### test_cant_consume_reserved_stock

**Category**: workflow  
**Description**: Workflow: test cant consume reserved stock  
**Expected**: self.assertRaises(NegativeStockError, se.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import cancel_stock_reservation_entries
from erpnext.stock.stock_ledger import NegativeStockError
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
so.reserve_stock = 1
so.items[0].reserve_stock = 1
so.save()
so.submit()
actual_qty = get_stock_balance(self.sr_item.name, self.warehouse)
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
self.assertRaises(NegativeStockError, se.submit)
se.cancel()
cancel_stock_reservation_entries(so.doctype, so.name)
se = make_stock_entry(item_code=self.sr_item.name, qty=actual_qty, from_warehouse=self.warehouse, rate=100, purpose='Material Issue', do_not_submit=True)
se.submit()
se.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:195*

### test_stock_reservation_from_pick_list

**Category**: workflow  
**Description**: Workflow: test stock reservation from pick list  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

items_details = create_items()
create_material_receipt(items_details, self.warehouse, qty=100)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
pl = create_pick_list(so.name)
pl.save()
pl.submit()
pl.create_stock_reservation_entries()
pl.load_from_db()
so.load_from_db()
for item in so.items:
    sre_details = get_stock_reservation_entries_for_voucher('Sales Order', so.name, item.name, fields=['reserved_qty'])[0]
    self.assertEqual(item.stock_reserved_qty, sre_details.reserved_qty)
sre = frappe.qb.DocType('Stock Reservation Entry')
sb_entry = frappe.qb.DocType('Serial and Batch Entry')
for location in pl.locations:
    self.assertEqual(location.stock_reserved_qty, location.qty)
    if location.serial_and_batch_bundle:
        picked_sb_entries = frappe.db.get_all('Serial and Batch Entry', filters={'parent': location.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        picked_sb_details: set[tuple] = set(picked_sb_entries)
        reserved_sb_entries = frappe.qb.from_(sre).inner_join(sb_entry).on(sre.name == sb_entry.parent).select(sb_entry.serial_no, sb_entry.batch_no, sb_entry.qty).where((sre.voucher_type == 'Sales Order') & (sre.voucher_no == location.sales_order) & (sre.voucher_detail_no == location.sales_order_item) & (sre.from_voucher_type == 'Pick List') & (sre.from_voucher_no == pl.name) & (sre.from_voucher_detail_no == location.name)).run(as_dict=True)
        reserved_sb_details: set[tuple] = {(sb_details.serial_no, sb_details.batch_no, -1 * sb_details.qty) for sb_details in reserved_sb_entries}
        self.assertSetEqual(picked_sb_details, reserved_sb_details)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:514*

### test_stock_reservation_from_purchase_receipt

**Category**: workflow  
**Description**: Workflow: test stock reservation from purchase receipt  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

from erpnext.buying.doctype.purchase_order.purchase_order import make_purchase_receipt
from erpnext.selling.doctype.sales_order.sales_order import make_material_request
from erpnext.stock.doctype.material_request.material_request import make_purchase_order
items_details = create_items()
create_material_receipt(items_details, self.warehouse, qty=10)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
mr = make_material_request(so.name)
mr.schedule_date = today()
mr.save().submit()
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.save().submit()
pr = make_purchase_receipt(po.name)
pr.save().submit()
for item in pr.items:
    sre, status, reserved_qty = frappe.db.get_value('Stock Reservation Entry', {'from_voucher_type': 'Purchase Receipt', 'from_voucher_no': pr.name, 'from_voucher_detail_no': item.name}, ['name', 'status', 'reserved_qty'])
    self.assertEqual(status, 'Reserved')
    self.assertEqual(reserved_qty, item.qty)
    if item.serial_and_batch_bundle:
        sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': item.serial_and_batch_bundle}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        reserved_sb_details = frappe.db.get_all('Serial and Batch Entry', filters={'parent': sre}, fields=['serial_no', 'batch_no', 'qty'], as_list=True)
        self.assertEqual(set(sb_details), set(reserved_sb_details))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:596*

### test_consider_reserved_stock_while_cancelling_an_inward_transaction

**Category**: workflow  
**Description**: Workflow: test consider reserved stock while cancelling an inward transaction  
**Expected**: self.assertRaises(frappe.ValidationError, se.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.sr_item = make_item(properties={'is_stock_item': 1, 'valuation_rate': 100})
create_material_receipt(items={self.sr_item.name: self.sr_item}, warehouse=self.warehouse, qty=100)

items_details = create_items()
se = create_material_receipt(items_details, self.warehouse, qty=100)
item_list = []
for item_code, properties in items_details.items():
    item_list.append({'item_code': item_code, 'warehouse': self.warehouse, 'qty': randint(11, 100), 'uom': properties.stock_uom, 'rate': randint(10, 400)})
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
so.create_stock_reservation_entries()
self.assertRaises(frappe.ValidationError, se.cancel)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:675*

### test_get_available_qty_to_reserve

**Category**: workflow  
**Description**: Workflow: test get available qty to reserve  
**Expected**: self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_reservation_entry.stock_reservation_entry import get_available_qty_to_reserve
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse)
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, ignore_validate=True)
available_qty_to_reserve = get_available_qty_to_reserve(self.sr_item.name, self.warehouse)
expected_available_qty_to_reserve = get_stock_balance(self.sr_item.name, self.warehouse) - sre.reserved_qty
self.assertEqual(available_qty_to_reserve, expected_available_qty_to_reserve)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:55*

### test_update_status

**Category**: workflow  
**Description**: Workflow: test update status  
**Expected**: self.assertEqual(sre.status, 'Cancelled')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sre = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, reserved_qty=30, ignore_validate=True, do_not_submit=True)
sre.load_from_db()
self.assertEqual(sre.status, 'Draft')
sre.submit()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Reserved')
sre.reserved_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Reserved')
sre.delivered_qty = 10
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Partially Delivered')
sre.delivered_qty = sre.voucher_qty
sre.db_update()
sre.update_status()
sre.load_from_db()
self.assertEqual(sre.status, 'Delivered')
sre.cancel()
sre.load_from_db()
self.assertEqual(sre.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:79*

### test_update_reserved_qty_in_voucher

**Category**: workflow  
**Description**: Workflow: test update reserved qty in voucher  
**Expected**: self.assertEqual(so.items[0].stock_reserved_qty, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order(item_code=self.sr_item.name, warehouse=self.warehouse, qty=50, rate=100, do_not_submit=True)
so.reserve_stock = 0
so.items[0].reserve_stock = 1
so.save()
so.submit()
sre1 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=30)
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty)
sre2 = make_stock_reservation_entry(item_code=self.sr_item.name, warehouse=self.warehouse, voucher_type='Sales Order', voucher_no=so.name, voucher_detail_no=so.items[0].name, reserved_qty=20)
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Partially Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre1.reserved_qty + sre2.reserved_qty)
sre1.cancel()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.reserved_qty += sre1.reserved_qty
sre2.save()
so.load_from_db()
sre1.load_from_db()
self.assertEqual(sre2.status, 'Reserved')
self.assertEqual(so.items[0].stock_reserved_qty, sre2.reserved_qty)
sre2.cancel()
so.load_from_db()
sre2.load_from_db()
self.assertEqual(sre1.status, 'Cancelled')
self.assertEqual(so.items[0].stock_reserved_qty, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reservation_entry/test_stock_reservation_entry.py:126*

### test_item_cost_reposting

**Category**: workflow  
**Description**: Workflow: test item cost reposting  
**Expected**: self.assertEqual(repack.items[1].get('basic_rate'), 750)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

company = '_Test Company'
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=100, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-10', posting_time='14:00')
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Finished Goods - _TC', qty=10, rate=200, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-20', posting_time='14:00')
se = make_stock_entry(item_code='_Test Item for Reposting', source='Stores - _TC', target='Finished Goods - _TC', company=company, qty=10, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-30', posting_time='14:00')
target_wh_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': se.name}, ['valuation_rate'], as_dict=1)
self.assertEqual(target_wh_sle.get('valuation_rate'), 150)
repack = create_repack_entry(company=company, posting_date='2020-05-05', posting_time='14:00')
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
self.assertEqual(finished_item_sle.get('incoming_rate'), 540)
self.assertEqual(finished_item_sle.get('valuation_rate'), 540)
create_stock_reconciliation(item_code='_Test Item for Reposting', warehouse='Stores - _TC', qty=50, rate=150, company=company, expense_account='Stock Adjustment - _TC' if frappe.get_all('Stock Ledger Entry') else 'Temporary Opening - _TC', posting_date='2020-04-12', posting_time='14:00')
target_wh_sle = get_previous_sle({'item_code': '_Test Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'posting_date': '2020-04-30', 'posting_time': '14:00'})
self.assertEqual(target_wh_sle.get('incoming_rate'), 150)
self.assertEqual(target_wh_sle.get('valuation_rate'), 175)
finished_item_sle = frappe.db.get_value('Stock Ledger Entry', {'item_code': '_Test Finished Item for Reposting', 'warehouse': 'Finished Goods - _TC', 'voucher_type': 'Stock Entry', 'voucher_no': repack.name}, ['incoming_rate', 'valuation_rate'], as_dict=1)
self.assertEqual(finished_item_sle.get('incoming_rate'), 790)
self.assertEqual(finished_item_sle.get('valuation_rate'), 790)
repack.reload()
self.assertEqual(repack.items[0].get('basic_rate'), 150)
self.assertEqual(repack.items[1].get('basic_rate'), 750)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:51*

### test_purchase_return_valuation_reposting

**Category**: workflow  
**Description**: Workflow: test purchase return valuation reposting  
**Expected**: self.assertEqual(stock_value_difference, -220)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-10', warehouse='Stores - _TC', item_code='_Test Item for Reposting', qty=5, rate=100)
return_pr = make_purchase_receipt(company='_Test Company', posting_date='2020-04-15', warehouse='Stores - _TC', item_code='_Test Item for Reposting', is_return=1, return_against=pr.name, qty=-2)
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
self.assertEqual(outgoing_rate, 100)
self.assertEqual(stock_value_difference, -200)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
outgoing_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name}, ['outgoing_rate', 'stock_value_difference'])
self.assertEqual(outgoing_rate, 110)
self.assertEqual(stock_value_difference, -220)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:172*

### test_sales_return_valuation_reposting

**Category**: workflow  
**Description**: Workflow: test sales return valuation reposting  
**Expected**: self.assertEqual(return_dn.items[0].incoming_rate, 110)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

company = '_Test Company'
item_code = '_Test Item for Reposting'
pr = make_purchase_receipt(company=company, posting_date='2020-04-10', warehouse='Stores - _TC', item_code=item_code, qty=5, rate=100)
dn = create_delivery_note(item_code=item_code, qty=5, rate=150, warehouse='Stores - _TC', company=company, expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
self.assertEqual(dn.items[0].incoming_rate, 100)
self.assertEqual(outgoing_rate, 100)
return_dn = create_delivery_note(is_return=1, return_against=dn.name, item_code=item_code, qty=-2, rate=150, company=company, warehouse='Stores - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(return_dn.items[0].incoming_rate, 100)
self.assertEqual(incoming_rate, 100)
self.assertEqual(stock_value_difference, 200)
lcv = create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 5)
self.assertEqual(outgoing_rate, 110)
dn.reload()
self.assertEqual(dn.items[0].incoming_rate, 110)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(incoming_rate, 110)
self.assertEqual(stock_value_difference, 220)
return_dn.reload()
self.assertEqual(return_dn.items[0].incoming_rate, 110)
return_dn.cancel()
dn.cancel()
lcv.cancel()
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:213*

### test_reposting_of_sales_return_for_packed_item

**Category**: workflow  
**Description**: Workflow: test reposting of sales return for packed item  
**Expected**: self.assertEqual(return_dn.packed_items[0].incoming_rate, 101)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

company = '_Test Company'
packed_item_code = '_Test Item for Reposting'
bundled_item = '_Test Bundled Item for Reposting'
create_product_bundle_item(bundled_item, [[packed_item_code, 4]])
pr = make_purchase_receipt(company=company, posting_date='2020-04-10', warehouse='Stores - _TC', item_code=packed_item_code, qty=50, rate=100)
dn = create_delivery_note(item_code=bundled_item, qty=5, rate=150, warehouse='Stores - _TC', company=company, expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 20)
self.assertEqual(dn.packed_items[0].incoming_rate, 100)
self.assertEqual(outgoing_rate, 100)
return_dn = create_delivery_note(is_return=1, return_against=dn.name, item_code=bundled_item, qty=-2, rate=150, company=company, warehouse='Stores - _TC', expense_account='Cost of Goods Sold - _TC', cost_center='Main - _TC')
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(return_dn.packed_items[0].incoming_rate, 100)
self.assertEqual(incoming_rate, 100)
self.assertEqual(stock_value_difference, 800)
lcv = create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
outgoing_rate = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name}, 'stock_value_difference') / 20)
self.assertEqual(outgoing_rate, 101)
dn.reload()
self.assertEqual(dn.packed_items[0].incoming_rate, 101)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': return_dn.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(incoming_rate, 101)
self.assertEqual(stock_value_difference, 808)
return_dn.reload()
self.assertEqual(return_dn.packed_items[0].incoming_rate, 101)
return_dn.cancel()
dn.cancel()
lcv.cancel()
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:313*

### test_batchwise_item_valuation_fifo

**Category**: workflow  
**Description**: Workflow: test batchwise item valuation fifo  
**Expected**: self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

item, warehouses, batches = setup_item_valuation_test(valuation_method='FIFO')
pr_entry_list = [(item, warehouses[0], batches[0], 1, 100), (item, warehouses[0], batches[1], 1, 50), (item, warehouses[0], batches[0], 1, 150), (item, warehouses[0], batches[1], 1, 100)]
prs = create_purchase_receipt_entries_for_batchwise_item_valuation_test(pr_entry_list)
sle_details = fetch_sle_details_for_doc_list(prs, ['stock_value'])
sv_list = [d['stock_value'] for d in sle_details]
expected_sv = [100, 150, 300, 400]
self.assertEqual(expected_sv, sv_list, "Incorrect 'Stock Value' values")
dn_entry_list = [(item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200), (item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200)]
frappe.flags.use_serial_and_batch_fields = True
dns = create_delivery_note_entries_for_batchwise_item_valuation_test(dn_entry_list)
sle_details = fetch_sle_details_for_doc_list(dns, ['stock_value_difference'])
svd_list = [-1 * d['stock_value_difference'] for d in sle_details]
expected_incoming_rates = expected_abs_svd = [75.0, 125.0, 75.0, 125.0]
self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")
for dn, _incoming_rate in zip(dns, expected_incoming_rates, strict=False):
    self.assertTrue(dn.items[0].incoming_rate in expected_abs_svd, "Incorrect 'Incoming Rate' values fetched for DN items")
frappe.flags.use_serial_and_batch_fields = False
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:458*

### test_batchwise_item_valuation_moving_average

**Category**: workflow  
**Description**: Workflow: test batchwise item valuation moving average  
**Expected**: self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

item, warehouses, batches = setup_item_valuation_test(valuation_method='Moving Average')
pr_entry_list = [(item, warehouses[0], batches[0], 1, 100), (item, warehouses[0], batches[1], 1, 50), (item, warehouses[0], batches[0], 1, 150), (item, warehouses[0], batches[1], 1, 100)]
prs = create_purchase_receipt_entries_for_batchwise_item_valuation_test(pr_entry_list)
sle_details = fetch_sle_details_for_doc_list(prs, ['stock_value'])
sv_list = [d['stock_value'] for d in sle_details]
expected_sv = [100, 150, 300, 400]
self.assertEqual(expected_sv, sv_list, "Incorrect 'Stock Value' values")
dn_entry_list = [(item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200), (item, warehouses[0], batches[1], 1, 200), (item, warehouses[0], batches[0], 1, 200)]
frappe.flags.use_serial_and_batch_fields = True
dns = create_delivery_note_entries_for_batchwise_item_valuation_test(dn_entry_list)
sle_details = fetch_sle_details_for_doc_list(dns, ['stock_value_difference'])
svd_list = [-1 * d['stock_value_difference'] for d in sle_details]
expected_incoming_rates = expected_abs_svd = [75.0, 125.0, 75.0, 125.0]
self.assertEqual(expected_abs_svd, svd_list, "Incorrect 'Stock Value Difference' values")
for dn, _incoming_rate in zip(dns, expected_incoming_rates, strict=False):
    self.assertTrue(dn.items[0].incoming_rate in expected_abs_svd, "Incorrect 'Incoming Rate' values fetched for DN items")
frappe.flags.use_serial_and_batch_fields = False
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:497*

### test_batchwise_item_valuation_stock_reco

**Category**: workflow  
**Description**: Workflow: test batchwise item valuation stock reco  
**Expected**: self.assertSLEs(sr2, expected_sles)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

item, warehouses, batches = setup_item_valuation_test()
state = {'stock_value': 0.0, 'qty': 0.0}

def update_invariants(exp_sles):
    for sle in exp_sles:
        state['stock_value'] += sle['stock_value_difference']
        state['qty'] += sle['actual_qty']
        sle['stock_value'] = state['stock_value']
        sle['qty_after_transaction'] = state['qty']
osr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=10, rate=100, batch_no=batches[1])
expected_sles = [{'actual_qty': 10, 'stock_value_difference': 1000}]
update_invariants(expected_sles)
self.assertSLEs(osr1, expected_sles)
osr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=13, rate=200, batch_no=batches[0])
expected_sles = [{'actual_qty': -10, 'stock_value_difference': -10 * 100}, {'actual_qty': 13, 'stock_value_difference': 200 * 13}]
update_invariants(expected_sles)
self.assertSLEs(osr2, expected_sles)
sr1 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=5, rate=50, batch_no=batches[1])
expected_sles = [{'actual_qty': -13, 'stock_value_difference': -13 * 200}, {'actual_qty': 5, 'stock_value_difference': 250}]
update_invariants(expected_sles)
self.assertSLEs(sr1, expected_sles)
sr2 = create_stock_reconciliation(warehouse=warehouses[0], item_code=item, qty=20, rate=75, batch_no=batches[0])
expected_sles = [{'actual_qty': -5, 'stock_value_difference': -5 * 50}, {'actual_qty': 20, 'stock_value_difference': 20 * 75}]
update_invariants(expected_sles)
self.assertSLEs(sr2, expected_sles)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:536*

### test_batch_wise_valuation_across_warehouse

**Category**: workflow  
**Description**: Workflow: test batch wise valuation across warehouse  
**Expected**: self.assertSLEs(transfer_unrelated, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source, 'stock_value': 15 * 5}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target, 'stock_value': 15 * 5 + 10 * 5}])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

item_code, warehouses, batches = setup_item_valuation_test()
source = warehouses[0]
target = warehouses[1]
unrelated_batch = make_stock_entry(item_code=item_code, target=source, batch_no=batches[1], qty=5, rate=10)
self.assertSLEs(unrelated_batch, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
reciept = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=10)
self.assertSLEs(reciept, [{'actual_qty': 5, 'stock_value_difference': 10 * 5}])
transfer = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[0], qty=5)
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target}])
backdated_receipt = make_stock_entry(item_code=item_code, target=source, batch_no=batches[0], qty=5, rate=20, posting_date=add_days(today(), -1))
self.assertSLEs(backdated_receipt, [{'actual_qty': 5, 'stock_value_difference': 20 * 5}])
self.assertSLEs(transfer, [{'actual_qty': -5, 'stock_value_difference': -15 * 5, 'warehouse': source, 'stock_value': 15 * 5 + 10 * 5}, {'actual_qty': 5, 'stock_value_difference': 15 * 5, 'warehouse': target, 'stock_value': 15 * 5}])
transfer_unrelated = make_stock_entry(item_code=item_code, source=source, target=target, batch_no=batches[1], qty=5)
self.assertSLEs(transfer_unrelated, [{'actual_qty': -5, 'stock_value_difference': -10 * 5, 'warehouse': source, 'stock_value': 15 * 5}, {'actual_qty': 5, 'stock_value_difference': 10 * 5, 'warehouse': target, 'stock_value': 15 * 5 + 10 * 5}])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:589*

### test_intermediate_average_batch_wise_valuation

**Category**: workflow  
**Description**: Workflow: A batch has moving average up until posting time,
check if same is respected when backdated entry is inserted in middle  
**Expected**: self.assertSLEs(consume_tomorrow, [{'stock_value_difference': -(30 + 15), 'stock_value': 0, 'qty_after_transaction': 0}])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

'A batch has moving average up until posting time,\n\t\tcheck if same is respected when backdated entry is inserted in middle'
item_code, warehouses, batches = setup_item_valuation_test()
warehouse = warehouses[0]
batch = batches[0]
yesterday = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batch, qty=1, rate=10, posting_date=add_days(today(), -1))
self.assertSLEs(yesterday, [{'actual_qty': 1, 'stock_value_difference': 10}])
tomorrow = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=30, posting_date=add_days(today(), 1))
self.assertSLEs(tomorrow, [{'actual_qty': 1, 'stock_value_difference': 30}])
create_today = make_stock_entry(item_code=item_code, target=warehouse, batch_no=batches[0], qty=1, rate=20)
self.assertSLEs(create_today, [{'actual_qty': 1, 'stock_value_difference': 20}])
consume_today = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=1)
self.assertSLEs(consume_today, [{'actual_qty': -1, 'stock_value_difference': -15}])
consume_tomorrow = make_stock_entry(item_code=item_code, source=warehouse, batch_no=batches[0], qty=2, posting_date=add_days(today(), 2))
self.assertSLEs(consume_tomorrow, [{'stock_value_difference': -(30 + 15), 'stock_value': 0, 'qty_after_transaction': 0}])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:678*

### test_legacy_item_valuation_stock_entry

**Category**: workflow  
**Description**: Workflow: test legacy item valuation stock entry  
**Expected**: details_list.append((sle_details, expected_sle_details, 'Material Issue Entries', columns))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
items = create_items()
reset('Stock Entry')
frappe.db.sql('delete from `tabStock Ledger Entry` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)
frappe.db.sql('delete from `tabBin` where item_code in (%s)' % ', '.join(['%s'] * len(items)), items)

columns = ['stock_value_difference', 'stock_value', 'actual_qty', 'qty_after_transaction', 'stock_queue']
item, warehouses, batches = setup_item_valuation_test()

def check_sle_details_against_expected(sle_details, expected_sle_details, detail, columns):
    for i, (sle_vals, ex_sle_vals) in enumerate(zip(sle_details, expected_sle_details, strict=False)):
        for col, sle_val, ex_sle_val in zip(columns, sle_vals, ex_sle_vals, strict=False):
            if col == 'stock_queue':
                sle_val = get_stock_value_from_q(sle_val)
                ex_sle_val = get_stock_value_from_q(ex_sle_val)
            self.assertEqual(sle_val, ex_sle_val, f'Incorrect {col} value on transaction #: {i} in {detail}')
details_list = []
se_entry_list_mr = [(item, None, warehouses[0], batches[0], 1, 50, '2021-01-21'), (item, None, warehouses[0], batches[1], 1, 100, '2021-01-23')]
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mr, 'Material Receipt')
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
expected_sle_details = [(50.0, 50.0, 1.0, 1.0, '[]'), (100.0, 150.0, 1.0, 2.0, '[]')]
details_list.append((sle_details, expected_sle_details, 'Material Receipt Entries', columns))
se_entry_list_mi = [(item, warehouses[0], None, batches[1], 1, None, '2021-01-29')]
ses = create_stock_entry_entries_for_batchwise_item_valuation_test(se_entry_list_mi, 'Material Issue')
sle_details = fetch_sle_details_for_doc_list(ses, columns=columns, as_dict=0)
expected_sle_details = [(-100.0, 50.0, -1.0, 1.0, '[]')]
details_list.append((sle_details, expected_sle_details, 'Material Issue Entries', columns))
for details in details_list:
    check_sle_details_against_expected(*details)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_ledger_entry/test_stock_ledger_entry.py:748*

### test_item_shortage_report

**Category**: workflow  
**Description**: Workflow: test item shortage report  
**Expected**: self.assertNotIn(item, item_code_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = make_item().name
so = make_sales_order(item_code=item)
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
self.assertEqual(reserved_qty, so.items[0].qty)
self.assertEqual(projected_qty, -so.items[0].qty)
filters = {'company': so.company}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': [so.items[0].warehouse]}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': ['Work In Progress - _TC']}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertNotIn(item, item_code_list)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:15*

### test_item_shortage_report

**Category**: workflow  
**Description**: Workflow: test item shortage report  
**Expected**: self.assertNotIn(item, item_code_list)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = make_item().name
so = make_sales_order(item_code=item)
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
self.assertEqual(reserved_qty, so.items[0].qty)
self.assertEqual(projected_qty, -so.items[0].qty)
filters = {'company': so.company}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': [so.items[0].warehouse]}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertIn(item, item_code_list)
filters = {'company': so.company, 'warehouse': ['Work In Progress - _TC']}
report_data = item_shortage_report(filters)[1]
item_code_list = [row.get('item_code') for row in report_data]
self.assertNotIn(item, item_code_list)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:15*

### test_clear_old_logs

**Category**: workflow  
**Description**: Workflow: test clear old logs  
**Expected**: self.assertTrue(len(logs) == 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for i in range(1, 20):
    repost_doc = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=nowdate(), status='Skipped', posting_time='00:01:00').insert(ignore_permissions=True)
    repost_doc.load_from_db()
    repost_doc.creation = add_days(now(), days=-i * 10)
    repost_doc.db_update_all()
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) > 10)
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import RepostItemValuation
RepostItemValuation.clear_old_logs(days=1)
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) == 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:88*

### test_deduplication

**Category**: workflow  
**Description**: Workflow: test deduplication  
**Expected**: _assert_status(riv3, 'Queued')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
def _assert_status(doc, status):
    doc.load_from_db()
    self.assertEqual(doc.status, status)
riv_args = frappe._dict(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date='2021-01-02', posting_time='00:01:00')
riv1 = frappe.get_doc(riv_args)
riv1.flags.dont_run_in_test = True
riv1.submit()
_assert_status(riv1, 'Queued')
riv2 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-03'}))
riv2.flags.dont_run_in_test = True
riv2.submit()
riv1.deduplicate_similar_repost()
_assert_status(riv2, 'Skipped')
riv3 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-01'}))
riv3.flags.dont_run_in_test = True
riv3.submit()
riv3.deduplicate_similar_repost()
_assert_status(riv3, 'Queued')
_assert_status(riv1, 'Skipped')
riv4 = frappe.get_doc(riv_args.update({'warehouse': 'Stores - _TC'}))
riv4.flags.dont_run_in_test = True
riv4.submit()
riv4.deduplicate_similar_repost()
_assert_status(riv4, 'Queued')
_assert_status(riv3, 'Queued')
riv4.set_status('Skipped')
riv3.set_status('Skipped')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:130*

### test_stock_freeze_validation

**Category**: workflow  
**Description**: Workflow: test stock freeze validation  
**Expected**: self.assertRaises(PendingRepostingError, stock_settings.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
today = nowdate()
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
riv.flags.dont_run_in_test = True
riv.submit()
stock_settings = frappe.get_doc('Stock Settings')
stock_settings.stock_frozen_upto = today
self.assertRaises(PendingRepostingError, stock_settings.save)
riv.set_status('Skipped')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:177*

### test_prevention_of_cancelled_transaction_riv

**Category**: workflow  
**Description**: Workflow: test prevention of cancelled transaction riv  
**Expected**: self.assertRaises(frappe.ValidationError, riv.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.flags.dont_execute_stock_reposts = True
item = make_item()
warehouse = '_Test Warehouse - _TC'
old = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=2, rate=5)
_new = make_stock_entry(item_code=item.name, to_warehouse=warehouse, qty=5, rate=10)
old.cancel()
riv = frappe.get_last_doc('Repost Item Valuation', {'voucher_type': old.doctype, 'voucher_no': old.name})
self.assertRaises(frappe.ValidationError, riv.cancel)
riv.db_set('status', 'Skipped')
riv.reload()
riv.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:199*

### test_gl_complete_gl_reposting

**Category**: workflow  
**Description**: Workflow: test gl complete gl reposting  
**Expected**: self.assertGLEs(consumption, [{'credit': 50, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts import utils
orig_chunk_size = utils.GL_REPOSTING_CHUNK
utils.GL_REPOSTING_CHUNK = 2
self.addCleanup(setattr, utils, 'GL_REPOSTING_CHUNK', orig_chunk_size)
item = self.make_item().name
company = '_Test Company with perpetual inventory'
for _ in range(10):
    make_stock_entry(item=item, company=company, qty=1, rate=10, target='Stores - TCP1')
consumption = make_stock_entry(item=item, company=company, qty=1, source='Stores - TCP1')
self.assertGLEs(consumption, [{'credit': 10, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
backdated_receipt = make_stock_entry(item=item, company=company, qty=1, rate=50, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
self.assertGLEs(backdated_receipt, [{'credit': 0, 'debit': 50}], gle_filters={'account': 'Stock In Hand - TCP1'})
self.assertGLEs(consumption, [{'credit': 50, 'debit': 0}], gle_filters={'account': 'Stock In Hand - TCP1'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:253*

### test_duplicate_ple_on_repost

**Category**: workflow  
**Description**: Workflow: test duplicate ple on repost  
**Expected**: self.assertEqual(sinv.outstanding_amount, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts import utils
orig_chunk_size = utils.GL_REPOSTING_CHUNK
utils.GL_REPOSTING_CHUNK = 2
self.addCleanup(setattr, utils, 'GL_REPOSTING_CHUNK', orig_chunk_size)
rate = 100
item = self.make_item()
item.valuation_rate = 90
item.allow_negative_stock = 1
item.save()
company = '_Test Company with perpetual inventory'
sinv = create_sales_invoice(company=company, posting_date=today(), debit_to='Debtors - TCP1', income_account='Sales - TCP1', expense_account='Cost of Goods Sold - TCP1', warehouse='Stores - TCP1', update_stock=1, currency='INR', item_code=item.name, cost_center='Main - TCP1', qty=1, rate=rate)
make_stock_entry(item=item.name, company=company, qty=5, rate=rate, target='Stores - TCP1', posting_date=add_to_date(today(), days=-1))
ple_entries = frappe.db.get_list('Payment Ledger Entry', filters={'voucher_type': sinv.doctype, 'voucher_no': sinv.name, 'delinked': 0})
self.assertEqual(len(ple_entries), 1)
sinv.reload()
self.assertEqual(sinv.outstanding_amount, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:299*

### test_account_freeze_validation

**Category**: workflow  
**Description**: Workflow: test account freeze validation  
**Expected**: self.assertRaises(frappe.ValidationError, riv.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
today = nowdate()
riv = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', company='_Test Company', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=today, posting_time='00:01:00')
riv.flags.dont_run_in_test = True
company = frappe.get_doc('Company', '_Test Company')
company.accounts_frozen_till_date = today
company.role_allowed_for_frozen_entries = ''
company.save()
self.assertRaises(frappe.ValidationError, riv.save)
company.accounts_frozen_till_date = ''
company.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:353*

### test_repost_item_valuation_for_closing_stock_balance

**Category**: workflow  
**Description**: Workflow: test repost item valuation for closing stock balance  
**Expected**: self.assertRaises(frappe.ValidationError, riv.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_closing_entry.stock_closing_entry import prepare_closing_stock_balance
doc = frappe.new_doc('Stock Closing Entry')
doc.company = '_Test Company'
doc.from_date = today()
doc.to_date = today()
doc.submit()
prepare_closing_stock_balance(doc.name)
doc.load_from_db()
self.assertEqual(doc.docstatus, 1)
self.assertEqual(doc.status, 'Completed')
riv = frappe.new_doc('Repost Item Valuation')
riv.update({'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'based_on': 'Item and Warehouse', 'posting_date': today(), 'posting_time': '00:01:00'})
self.assertRaises(frappe.ValidationError, riv.save)
doc.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:394*

### test_clear_old_logs

**Category**: workflow  
**Description**: Workflow: test clear old logs  
**Expected**: self.assertTrue(len(logs) == 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for i in range(1, 20):
    repost_doc = frappe.get_doc(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date=nowdate(), status='Skipped', posting_time='00:01:00').insert(ignore_permissions=True)
    repost_doc.load_from_db()
    repost_doc.creation = add_days(now(), days=-i * 10)
    repost_doc.db_update_all()
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) > 10)
from erpnext.stock.doctype.repost_item_valuation.repost_item_valuation import RepostItemValuation
RepostItemValuation.clear_old_logs(days=1)
logs = frappe.get_all('Repost Item Valuation', filters={'status': 'Skipped'})
self.assertTrue(len(logs) == 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:88*

### test_deduplication

**Category**: workflow  
**Description**: Workflow: test deduplication  
**Expected**: _assert_status(riv3, 'Queued')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
def _assert_status(doc, status):
    doc.load_from_db()
    self.assertEqual(doc.status, status)
riv_args = frappe._dict(doctype='Repost Item Valuation', item_code='_Test Item', warehouse='_Test Warehouse - _TC', based_on='Item and Warehouse', posting_date='2021-01-02', posting_time='00:01:00')
riv1 = frappe.get_doc(riv_args)
riv1.flags.dont_run_in_test = True
riv1.submit()
_assert_status(riv1, 'Queued')
riv2 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-03'}))
riv2.flags.dont_run_in_test = True
riv2.submit()
riv1.deduplicate_similar_repost()
_assert_status(riv2, 'Skipped')
riv3 = frappe.get_doc(riv_args.update({'posting_date': '2021-01-01'}))
riv3.flags.dont_run_in_test = True
riv3.submit()
riv3.deduplicate_similar_repost()
_assert_status(riv3, 'Queued')
_assert_status(riv1, 'Skipped')
riv4 = frappe.get_doc(riv_args.update({'warehouse': 'Stores - _TC'}))
riv4.flags.dont_run_in_test = True
riv4.submit()
riv4.deduplicate_similar_repost()
_assert_status(riv4, 'Queued')
_assert_status(riv3, 'Queued')
riv4.set_status('Skipped')
riv3.set_status('Skipped')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/repost_item_valuation/test_repost_item_valuation.py:130*

### test_get_item_details

**Category**: workflow  
**Description**: Workflow: test get item details  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

frappe.db.sql('delete from `tabItem Price`')
frappe.db.sql('delete from `tabBin`')
to_check = {'item_code': '_Test Item', 'item_name': '_Test Item', 'description': '_Test Item 1', 'warehouse': '_Test Warehouse - _TC', 'income_account': 'Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center - _TC', 'qty': 1.0, 'price_list_rate': 100.0, 'base_price_list_rate': 0.0, 'discount_percentage': 0.0, 'rate': 0.0, 'base_rate': 0.0, 'amount': 0.0, 'base_amount': 0.0, 'batch_no': None, 'uom': '_Test UOM', 'conversion_factor': 1.0, 'reserved_qty': 1, 'actual_qty': 5, 'projected_qty': 14}
make_test_objects('Item Price')
make_test_objects('Bin', [{'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC', 'reserved_qty': 1, 'actual_qty': 5, 'ordered_qty': 10, 'projected_qty': 14}])
company = '_Test Company'
currency = frappe.get_cached_value('Company', company, 'default_currency')
details = get_item_details(ItemDetailsCtx({'item_code': '_Test Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Order', 'conversion_rate': 1, 'price_list_currency': currency, 'plc_conversion_rate': 1, 'order_type': 'Sales', 'customer': '_Test Customer', 'conversion_factor': 1, 'price_list_uom_dependant': 1, 'ignore_pricing_rule': 1}))
for key, value in to_check.items():
    self.assertEqual(value, details.get(key), key)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:91*

### test_item_defaults

**Category**: workflow  
**Description**: Workflow: test item defaults  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

frappe.delete_doc_if_exists('Item', 'Test Item With Defaults', force=1)
make_item('Test Item With Defaults', {'item_group': '_Test Item Group', 'brand': '_Test Brand With Item Defaults', 'item_defaults': [{'company': '_Test Company', 'default_warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'default_cogs_account': '_Test Account Cost for Goods Sold - _TC', 'buying_cost_center': '_Test Write Off Cost Center - _TC'}]})
sales_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'income_account': '_Test Account Sales - _TC', 'expense_account': '_Test Account Cost for Goods Sold - _TC', 'cost_center': '_Test Cost Center 2 - _TC'}
sales_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer'}))
for key, value in sales_item_check.items():
    self.assertEqual(value, sales_item_details.get(key))
purchase_item_check = {'item_code': 'Test Item With Defaults', 'warehouse': '_Test Warehouse 2 - _TC', 'expense_account': '_Test Account Stock Expenses - _TC', 'income_account': '_Test Account Sales - _TC', 'cost_center': '_Test Write Off Cost Center - _TC'}
purchase_item_details = get_item_details(ItemDetailsCtx({'item_code': 'Test Item With Defaults', 'company': '_Test Company', 'price_list': '_Test Price List', 'currency': '_Test Currency', 'doctype': 'Purchase Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'supplier': '_Test Supplier'}))
for key, value in purchase_item_check.items():
    self.assertEqual(value, purchase_item_details.get(key))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:296*

### test_item_attribute_change_after_variant

**Category**: workflow  
**Description**: Workflow: test item attribute change after variant  
**Expected**: self.assertRaises(InvalidItemAttributeValueError, attribute.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

frappe.delete_doc_if_exists('Item', '_Test Variant Item-L', force=1)
variant = create_variant('_Test Variant Item', {'Test Size': 'Large'})
variant.save()
attribute = frappe.get_doc('Item Attribute', 'Test Size')
attribute.item_attribute_values = []
frappe.flags.attribute_values = None
self.assertRaises(InvalidItemAttributeValueError, attribute.save)
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:388*

### test_copy_fields_from_template_to_variants

**Category**: workflow  
**Description**: Workflow: test copy fields from template to variants  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

frappe.delete_doc_if_exists('Item', '_Test Variant Item-XL', force=1)
fields = [{'field_name': 'item_group'}, {'field_name': 'is_stock_item'}]
allow_fields = [d.get('field_name') for d in fields]
set_item_variant_settings(fields)
if not frappe.db.get_value('Item Attribute Value', {'parent': 'Test Size', 'attribute_value': 'Extra Large'}, 'name'):
    item_attribute = frappe.get_doc('Item Attribute', 'Test Size')
    item_attribute.append('item_attribute_values', {'attribute_value': 'Extra Large', 'abbr': 'XL'})
    item_attribute.save()
template = frappe.get_doc('Item', '_Test Variant Item')
template.item_group = '_Test Item Group D'
template.save()
variant = create_variant('_Test Variant Item', {'Test Size': 'Extra Large'})
variant.item_code = '_Test Variant Item-XL'
variant.item_name = '_Test Variant Item-XL'
variant.save()
variant = frappe.get_doc('Item', '_Test Variant Item-XL')
for fieldname in allow_fields:
    self.assertEqual(template.get(fieldname), variant.get(fieldname))
template = frappe.get_doc('Item', '_Test Variant Item')
template.item_group = '_Test Item Group Desktops'
template.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:414*

### test_make_item_variant_with_numeric_values

**Category**: workflow  
**Description**: Workflow: test make item variant with numeric values  
**Expected**: self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.5')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

for d in frappe.db.get_all('Item', filters={'variant_of': '_Test Numeric Template Item'}):
    frappe.delete_doc_if_exists('Item', d.name)
frappe.delete_doc_if_exists('Item', '_Test Numeric Template Item')
frappe.delete_doc_if_exists('Item Attribute', 'Test Item Length')
frappe.db.sql("delete from `tabItem Variant Attribute`\n\t\t\twhere attribute='Test Item Length' ")
frappe.flags.attribute_values = None
frappe.get_doc({'doctype': 'Item Attribute', 'attribute_name': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}).insert()
make_item('_Test Numeric Template Item', {'attributes': [{'attribute': 'Test Size'}, {'attribute': 'Test Item Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0.5}], 'item_defaults': [{'default_warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'}], 'has_variants': 1})
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.1})
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.1')
variant.item_code = '_Test Numeric Variant-L-1.1'
variant.item_name = '_Test Numeric Variant Large 1.1m'
self.assertRaises(InvalidItemAttributeValueError, variant.save)
variant = create_variant('_Test Numeric Template Item', {'Test Size': 'Large', 'Test Item Length': 1.5})
self.assertEqual(variant.item_code, '_Test Numeric Template Item-L-1.5')
variant.item_code = '_Test Numeric Variant-L-1.5'
variant.item_name = '_Test Numeric Variant Large 1.5m'
variant.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:445*

### test_item_variant_by_manufacturer

**Category**: workflow  
**Description**: Workflow: test item variant by manufacturer  
**Expected**: self.assertTrue(item_manufacturer)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

template = make_item('_Test Item Variant By Manufacturer', {'has_variants': 1, 'variant_based_on': 'Manufacturer'}).name
for manufacturer in ['DFSS', 'DASA', 'ASAAS']:
    if not frappe.db.exists('Manufacturer', manufacturer):
        m_doc = frappe.new_doc('Manufacturer')
        m_doc.short_name = manufacturer
        m_doc.insert()
self.assertFalse(frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS'}))
variant = get_variant(template, manufacturer='DFSS', manufacturer_part_no='DFSS-123')
item_manufacturer = frappe.db.exists('Item Manufacturer', {'manufacturer': 'DFSS', 'item_code': variant.name})
self.assertTrue(item_manufacturer)
frappe.delete_doc('Item Manufacturer', item_manufacturer)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:569*

### test_add_item_barcode

**Category**: workflow  
**Description**: Workflow: test add item barcode  
**Expected**: self.assertRaises(InvalidBarcode, item_doc.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

frappe.db.sql('delete from `tabItem Barcode`')
item_code = 'Test Item Barcode'
if frappe.db.exists('Item', item_code):
    frappe.delete_doc('Item', item_code)
barcode_properties_list = [{'barcode': '0012345678905', 'barcode_type': 'EAN'}, {'barcode': '012345678905', 'barcode_type': 'UAN'}, {'barcode': 'ARBITRARY_TEXT'}, {'barcode': '72527273070', 'barcode_type': 'UPC-A'}, {'barcode': '123456', 'barcode_type': 'CODE-39'}, {'barcode': '401268452363', 'barcode_type': 'EAN'}, {'barcode': '90311017', 'barcode_type': 'EAN'}, {'barcode': '73513537', 'barcode_type': 'EAN'}, {'barcode': '0123456789012', 'barcode_type': 'GS1'}, {'barcode': '2211564566668', 'barcode_type': 'GTIN'}, {'barcode': '0256480249', 'barcode_type': 'ISBN'}, {'barcode': '0192552570', 'barcode_type': 'ISBN-10'}, {'barcode': '9781234567897', 'barcode_type': 'ISBN-13'}, {'barcode': '9771234567898', 'barcode_type': 'ISSN'}, {'barcode': '4581171967072', 'barcode_type': 'JAN'}, {'barcode': '12345678', 'barcode_type': 'PZN'}, {'barcode': '725272730706', 'barcode_type': 'UPC'}]
create_item(item_code)
for barcode_properties in barcode_properties_list:
    item_doc = frappe.get_doc('Item', item_code)
    new_barcode = item_doc.append('barcodes')
    new_barcode.update(barcode_properties)
    item_doc.save()
barcodes = frappe.get_all('Item Barcode', fields=['barcode', 'barcode_type'], filters={'parent': item_code})
for barcode_properties in barcode_properties_list:
    barcode_to_find = barcode_properties['barcode']
    matching_barcodes = [x for x in barcodes if x['barcode'] == barcode_to_find]
self.assertEqual(len(matching_barcodes), 1)
details = matching_barcodes[0]
for key, value in barcode_properties.items():
    self.assertEqual(value, details.get(key))
item_doc = frappe.get_doc('Item', item_code)
new_barcode = item_doc.append('barcodes')
new_barcode.update(barcode_properties_list[0])
self.assertRaises(frappe.UniqueValidationError, item_doc.save)
item_doc = frappe.get_doc('Item', item_code)
new_barcode = item_doc.append('barcodes')
new_barcode.barcode = '9999999999999'
new_barcode.barcode_type = 'EAN'
self.assertRaises(InvalidBarcode, item_doc.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:599*

### test_attribute_completions

**Category**: workflow  
**Description**: Workflow: test attribute completions  
**Expected**: self.assertEqual(received_attrs, {'Extra Small', 'Extra Large'})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

expected_attrs = {'Small', 'Extra Small', 'Extra Large', 'Large', '2XL', 'Medium'}
attrs = get_item_attribute('Test Size')
received_attrs = {attr.attribute_value for attr in attrs}
self.assertEqual(received_attrs, expected_attrs)
attrs = get_item_attribute('Test Size', attribute_value='extra')
received_attrs = {attr.attribute_value for attr in attrs}
self.assertEqual(received_attrs, {'Extra Small', 'Extra Large'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:688*

### test_check_stock_uom_with_bin_no_sle

**Category**: workflow  
**Description**: Workflow: test check stock uom with bin no sle  
**Expected**: self.assertRaises(frappe.ValidationError, item.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

from erpnext.stock.stock_balance import update_bin_qty
item = create_item('_Item with bin qty')
item.stock_uom = 'Gram'
item.save()
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 10})
item.stock_uom = 'Kilometer'
self.assertRaises(frappe.ValidationError, item.save)
update_bin_qty(item.item_code, '_Test Warehouse - _TC', {'reserved_qty': 0})
item.load_from_db()
item.stock_uom = 'Kilometer'
try:
    item.save()
except frappe.ValidationError as e:
    self.fail(f'UoM change not allowed even though no SLE / BIN with positive qty exists: {e}')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:705*

### test_item_type_field_change

**Category**: workflow  
**Description**: Workflow: Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.flags.attribute_values = None

'Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.'
from erpnext.accounts.doctype.purchase_invoice.test_purchase_invoice import make_purchase_invoice
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
transaction_creators = [lambda i: make_purchase_receipt(item_code=i), lambda i: make_purchase_invoice(item_code=i, update_stock=1), lambda i: make_stock_entry(item_code=i, qty=1, target='_Test Warehouse - _TC'), lambda i: create_delivery_note(item_code=i)]
properties = {'has_batch_no': 0, 'allow_negative_stock': 1, 'valuation_rate': 10}
for transaction_creator in transaction_creators:
    item = make_item(properties=properties)
    transaction = transaction_creator(item.name)
    item.has_batch_no = 1
    self.assertRaises(frappe.ValidationError, item.save)
    transaction.cancel()
    item.reload()
    item.has_batch_no = 1
    item.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item/test_item.py:815*

### test_naming

**Category**: workflow  
**Description**: Workflow: test naming  
**Expected**: self.assertIn(warehouse_name, wh.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = 'Wind Power LLC'
warehouse_name = 'Named Warehouse - WP'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertEqual(wh.name, warehouse_name)
warehouse_name = 'Unnamed Warehouse'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertIn(warehouse_name, wh.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:33*

### test_unlinking_warehouse_from_item_defaults

**Category**: workflow  
**Description**: Workflow: test unlinking warehouse from item defaults  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company'
warehouse_names = [f'_Test Warehouse {i} for Unlinking' for i in range(2)]
warehouse_ids = []
for warehouse in warehouse_names:
    warehouse_id = create_warehouse(warehouse, company=company)
    warehouse_ids.append(warehouse_id)
item_names = [f'_Test Item {i} for Unlinking' for i in range(2)]
for item, warehouse in zip(item_names, warehouse_ids, strict=False):
    create_item(item, warehouse=warehouse, company=company)
for warehouse in warehouse_ids:
    frappe.delete_doc('Warehouse', warehouse)
for item in item_names:
    self.assertTrue(bool(frappe.db.exists('Item', item)), f"{item} doesn't exist")
    item_doc = frappe.get_doc('Item', item)
    for item_default in item_doc.item_defaults:
        self.assertNotIn(item_default.default_warehouse, warehouse_ids, f'{item} linked to {item_default.default_warehouse} in {warehouse_ids}.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:43*

### test_naming

**Category**: workflow  
**Description**: Workflow: test naming  
**Expected**: self.assertIn(warehouse_name, wh.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = 'Wind Power LLC'
warehouse_name = 'Named Warehouse - WP'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertEqual(wh.name, warehouse_name)
warehouse_name = 'Unnamed Warehouse'
wh = frappe.get_doc(doctype='Warehouse', warehouse_name=warehouse_name, company=company).insert()
self.assertIn(warehouse_name, wh.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:33*

### test_unlinking_warehouse_from_item_defaults

**Category**: workflow  
**Description**: Workflow: test unlinking warehouse from item defaults  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company'
warehouse_names = [f'_Test Warehouse {i} for Unlinking' for i in range(2)]
warehouse_ids = []
for warehouse in warehouse_names:
    warehouse_id = create_warehouse(warehouse, company=company)
    warehouse_ids.append(warehouse_id)
item_names = [f'_Test Item {i} for Unlinking' for i in range(2)]
for item, warehouse in zip(item_names, warehouse_ids, strict=False):
    create_item(item, warehouse=warehouse, company=company)
for warehouse in warehouse_ids:
    frappe.delete_doc('Warehouse', warehouse)
for item in item_names:
    self.assertTrue(bool(frappe.db.exists('Item', item)), f"{item} doesn't exist")
    item_doc = frappe.get_doc('Item', item)
    for item_default in item_doc.item_defaults:
        self.assertNotIn(item_default.default_warehouse, warehouse_ids, f'{item} linked to {item_default.default_warehouse} in {warehouse_ids}.')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:43*

### test_get_period_date_ranges_yearly

**Category**: workflow  
**Description**: Workflow: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.item = make_item().name
self.warehouse = '_Test Warehouse - _TC'

filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
ranges = get_period_date_ranges(filters)
first_date = get_fiscal_year('2021-01-28')[1]
expected_ranges = [[first_date, datetime.date(2021, 2, 6)]]
self.assertEqual(ranges, expected_ranges)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:70*

### test_get_period_date_ranges_yearly

**Category**: workflow  
**Description**: Workflow: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
ranges = get_period_date_ranges(filters)
first_date = get_fiscal_year('2021-01-28')[1]
expected_ranges = [[first_date, datetime.date(2021, 2, 6)]]
self.assertEqual(ranges, expected_ranges)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:70*

### test_landed_cost_voucher

**Category**: workflow  
**Description**: Workflow: test landed cost voucher  
**Expected**: self.assertPurchaseReceiptLCVGLEntries(pr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
pr_lc_value = frappe.db.get_value('Purchase Receipt Item', {'parent': pr.name}, 'landed_cost_voucher_amount')
self.assertEqual(pr_lc_value, 25.0)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 25.0)
self.assertPurchaseReceiptLCVGLEntries(pr)
frappe.db.set_value('Stock Ledger Entry', {'is_cancelled': 1, 'voucher_type': pr.doctype, 'voucher_no': pr.name}, 'is_cancelled', 1, modified=add_to_date(now(), hours=1, as_datetime=True, as_string=True))
items, warehouses = pr.get_items_and_warehouses()
update_gl_entries_after(pr.posting_date, pr.posting_time, warehouses, items, company=pr.company)
self.assertPurchaseReceiptLCVGLEntries(pr)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:29*

### test_landed_cost_voucher_stock_impact

**Category**: workflow  
**Description**: Workflow: Test impact of LCV on future stock balances.  
**Expected**: self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr1 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=500, rate=80, posting_date=add_days(frappe.utils.nowdate(), -2))
pr2 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=100, rate=80, posting_date=frappe.utils.nowdate())
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr1.name, pr1.company)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:128*

### test_landed_cost_voucher_for_zero_purchase_rate

**Category**: workflow  
**Description**: Workflow: Test impact of LCV on future stock balances.  
**Expected**: self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=10, rate=0, posting_date=add_days(frappe.utils.nowdate(), -2))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 0)
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, distribute_charges_based_on='Distribute Manually', do_not_save=True)
lcv.get_items_from_purchase_receipts()
lcv.items[0].applicable_charges = 100
lcv.save()
lcv.submit()
self.assertTrue(frappe.db.exists('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:181*

### test_landed_cost_voucher_against_purchase_invoice

**Category**: workflow  
**Description**: Workflow: test landed cost voucher against purchase invoice  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pi = make_purchase_invoice(update_stock=1, posting_date=frappe.utils.nowdate(), posting_time=frappe.utils.nowtime(), cash_bank_account='Cash - TCP1', company='_Test Company with perpetual inventory', supplier_warehouse='Work In Progress - TCP1', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='_Test Account Cost for Goods Sold - TCP1')
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Invoice', pi.name, pi.company)
pi_lc_value = frappe.db.get_value('Purchase Invoice Item', {'parent': pi.name}, 'landed_cost_voucher_amount')
self.assertEqual(pi_lc_value, 50.0)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pi.doctype, 'voucher_no': pi.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
gl_entries = get_gl_entries('Purchase Invoice', pi.name)
self.assertTrue(gl_entries)
stock_in_hand_account = get_inventory_account(pi.company, pi.get('items')[0].warehouse)
expected_values = {stock_in_hand_account: [300.0, 0.0], 'Creditors - TCP1': [0.0, 250.0], 'Expenses Included In Valuation - TCP1': [0.0, 50.0]}
for gle in gl_entries:
    if not gle.get('is_cancelled'):
        self.assertEqual(expected_values[gle.account][0], gle.debit)
        self.assertEqual(expected_values[gle.account][1], gle.credit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:234*

### test_landed_cost_voucher_for_serialized_item

**Category**: workflow  
**Description**: Workflow: test landed cost voucher for serialized item  
**Expected**: self.assertEqual(new_serial_no_rate - serial_no_rate, 5.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Item', '_Test Serialized Item', 'serial_no_series', 'SNJJ.###')
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True, do_not_submit=True)
pr.items[0].item_code = '_Test Serialized Item'
pr.submit()
pr.load_from_db()
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
new_serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
self.assertEqual(new_serial_no_rate - serial_no_rate, 5.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:299*

### test_serialized_lcv_delivered

**Category**: workflow  
**Description**: Workflow: In some cases you'd want to deliver before you can know all the
landed costs, this should be allowed for serial nos too.

Case:
                - receipt a serial no @ X rate
                - delivery the serial no @ X rate
                - add LCV to receipt X + Y
                - LCV should be successful
                - delivery should reflect X+Y valuation.  
**Expected**: self.assertEqual(stock_value_difference, -new_purchase_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"In some cases you'd want to deliver before you can know all the\n\t\tlanded costs, this should be allowed for serial nos too.\n\n\t\tCase:\n\t\t                - receipt a serial no @ X rate\n\t\t                - delivery the serial no @ X rate\n\t\t                - add LCV to receipt X + Y\n\t\t                - LCV should be successful\n\t\t                - delivery should reflect X+Y valuation.\n\t\t"
serial_no = 'LCV_TEST_SR_NO'
item_code = '_Test Serialized Item'
warehouse = 'Stores - TCP1'
if not frappe.db.exists('Serial No', serial_no):
    frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse=warehouse, qty=1, rate=200, item_code=item_code, serial_no=[serial_no])
sn_obj = SerialNoValuation(sle=frappe._dict({'posting_date': today(), 'posting_time': nowtime(), 'item_code': '_Test Serialized Item', 'warehouse': 'Stores - TCP1', 'serial_nos': [serial_no]}))
serial_no_rate = sn_obj.get_incoming_rate_of_serial_no(serial_no)
dn = create_delivery_note(item_code=item_code, company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', serial_no=[serial_no], qty=1, rate=500, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
charges = 10
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company, charges=charges)
new_purchase_rate = serial_no_rate + charges
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', filters={'voucher_no': dn.name, 'voucher_type': dn.doctype, 'is_cancelled': 0}, fieldname='stock_value_difference')
self.assertEqual(stock_value_difference, -new_purchase_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:349*

### test_multi_currency_lcv

**Category**: workflow  
**Description**: Workflow: test multi currency lcv  
**Expected**: self.assertEqual(pr.items[0].landed_cost_voucher_amount, 729)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.setup.doctype.currency_exchange.test_currency_exchange import save_new_records
save_new_records(self.globalTestRecords['Currency Exchange'])
usd_shipping = create_account(account_name='Shipping Charges USD', parent_account='Duties and Taxes - TCP1', company='_Test Company with perpetual inventory', account_currency='USD')
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Stores - TCP1')
pr.submit()
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, do_not_save=True)
lcv.append('taxes', {'description': 'Shipping Charges', 'expense_account': usd_shipping, 'amount': 10})
lcv.save()
lcv.submit()
pr.load_from_db()
self.assertEqual(lcv.total_taxes_and_charges, 729)
self.assertEqual(pr.items[0].landed_cost_voucher_amount, 729)
gl_entries = frappe.get_all('GL Entry', fields=['account', 'credit', 'credit_in_account_currency'], filters={'voucher_no': pr.name, 'account': ('in', ['Shipping Charges USD - TCP1', 'Expenses Included In Valuation - TCP1'])})
expected_gl_entries = {'Shipping Charges USD - TCP1': [629, 10], 'Expenses Included In Valuation - TCP1': [100, 100]}
for entry in gl_entries:
    amounts = expected_gl_entries.get(entry.account)
    self.assertEqual(entry.credit, amounts[0])
    self.assertEqual(entry.credit_in_account_currency, amounts[1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:505*

### test_landed_cost_voucher

**Category**: workflow  
**Description**: Workflow: test landed cost voucher  
**Expected**: self.assertPurchaseReceiptLCVGLEntries(pr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr.name, pr.company)
pr_lc_value = frappe.db.get_value('Purchase Receipt Item', {'parent': pr.name}, 'landed_cost_voucher_amount')
self.assertEqual(pr_lc_value, 25.0)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr.doctype, 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1', 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 25.0)
self.assertPurchaseReceiptLCVGLEntries(pr)
frappe.db.set_value('Stock Ledger Entry', {'is_cancelled': 1, 'voucher_type': pr.doctype, 'voucher_no': pr.name}, 'is_cancelled', 1, modified=add_to_date(now(), hours=1, as_datetime=True, as_string=True))
items, warehouses = pr.get_items_and_warehouses()
update_gl_entries_after(pr.posting_date, pr.posting_time, warehouses, items, company=pr.company)
self.assertPurchaseReceiptLCVGLEntries(pr)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:29*

### test_landed_cost_voucher_stock_impact

**Category**: workflow  
**Description**: Workflow: Test impact of LCV on future stock balances.  
**Expected**: self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr1 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=500, rate=80, posting_date=add_days(frappe.utils.nowdate(), -2))
pr2 = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=100, rate=80, posting_date=frappe.utils.nowdate())
last_sle = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
create_landed_cost_voucher('Purchase Receipt', pr1.name, pr1.company)
last_sle_after_landed_cost = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': pr2.doctype, 'voucher_no': pr2.name, 'item_code': item.name, 'warehouse': warehouse, 'is_cancelled': 0}, fieldname=['qty_after_transaction', 'stock_value'], as_dict=1)
self.assertEqual(last_sle.qty_after_transaction, last_sle_after_landed_cost.qty_after_transaction)
self.assertEqual(last_sle_after_landed_cost.stock_value - last_sle.stock_value, 50.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:128*

### test_landed_cost_voucher_for_zero_purchase_rate

**Category**: workflow  
**Description**: Workflow: Test impact of LCV on future stock balances.  
**Expected**: self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact of LCV on future stock balances.'
from erpnext.stock.doctype.item.test_item import make_item
item = make_item('LCV Stock Item', {'is_stock_item': 1})
warehouse = 'Stores - _TC'
pr = make_purchase_receipt(item_code=item.name, warehouse=warehouse, qty=10, rate=0, posting_date=add_days(frappe.utils.nowdate(), -2))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 0)
lcv = make_landed_cost_voucher(company=pr.company, receipt_document_type='Purchase Receipt', receipt_document=pr.name, charges=100, distribute_charges_based_on='Distribute Manually', do_not_save=True)
lcv.get_items_from_purchase_receipts()
lcv.items[0].applicable_charges = 100
lcv.save()
lcv.submit()
self.assertTrue(frappe.db.exists('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}))
self.assertEqual(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'is_cancelled': 0}, 'stock_value_difference'), 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/landed_cost_voucher/test_landed_cost_voucher.py:181*

### test_barcode_scanning

**Category**: workflow  
**Description**: Workflow: test barcode scanning  
**Expected**: self.assertEqual(serial_scan['has_serial_no'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
simple_item = self.make_item(properties={'barcodes': [{'barcode': '12399'}]})
self.assertEqual(scan_barcode('12399')['item_code'], simple_item.name)
batch_item = self.make_item(properties={'has_batch_no': 1, 'create_new_batch': 1})
batch = frappe.get_doc(doctype='Batch', item=batch_item.name).insert()
batch_scan = scan_barcode(batch.name)
self.assertEqual(batch_scan['item_code'], batch_item.name)
self.assertEqual(batch_scan['batch_no'], batch.name)
self.assertEqual(batch_scan['has_batch_no'], 1)
self.assertEqual(batch_scan['has_serial_no'], 0)
serial_item = self.make_item(properties={'has_serial_no': 1})
serial = frappe.get_doc(doctype='Serial No', item_code=serial_item.name, serial_no=frappe.generate_hash()).insert()
serial_scan = scan_barcode(serial.name)
self.assertEqual(serial_scan['item_code'], serial_item.name)
self.assertEqual(serial_scan['serial_no'], serial.name)
self.assertEqual(serial_scan['has_batch_no'], 0)
self.assertEqual(serial_scan['has_serial_no'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:74*

### test_barcode_scanning_of_warehouse

**Category**: workflow  
**Description**: Workflow: test barcode scanning of warehouse  
**Expected**: self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode', 'company': '_Test Company'}).insert()
warehouse_2 = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode 2', 'company': '_Test Company'}).insert()
warehouse_scan = scan_barcode(warehouse.name)
self.assertEqual(warehouse_scan['warehouse'], warehouse.name)
item_with_warehouse = self.make_item(properties={'item_defaults': [{'company': '_Test Company', 'default_warehouse': warehouse.name}], 'barcodes': [{'barcode': 'w12345'}]})
item_scan = scan_barcode('w12345')
self.assertEqual(item_scan['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan.get('default_warehouse'), None)
ctx = {'company': '_Test Company'}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse.name)
ctx = {'company': '_Test Company', 'set_warehouse': warehouse_2.name}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:98*

### test_barcode_scanning

**Category**: workflow  
**Description**: Workflow: test barcode scanning  
**Expected**: self.assertEqual(serial_scan['has_serial_no'], 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
simple_item = self.make_item(properties={'barcodes': [{'barcode': '12399'}]})
self.assertEqual(scan_barcode('12399')['item_code'], simple_item.name)
batch_item = self.make_item(properties={'has_batch_no': 1, 'create_new_batch': 1})
batch = frappe.get_doc(doctype='Batch', item=batch_item.name).insert()
batch_scan = scan_barcode(batch.name)
self.assertEqual(batch_scan['item_code'], batch_item.name)
self.assertEqual(batch_scan['batch_no'], batch.name)
self.assertEqual(batch_scan['has_batch_no'], 1)
self.assertEqual(batch_scan['has_serial_no'], 0)
serial_item = self.make_item(properties={'has_serial_no': 1})
serial = frappe.get_doc(doctype='Serial No', item_code=serial_item.name, serial_no=frappe.generate_hash()).insert()
serial_scan = scan_barcode(serial.name)
self.assertEqual(serial_scan['item_code'], serial_item.name)
self.assertEqual(serial_scan['serial_no'], serial.name)
self.assertEqual(serial_scan['has_batch_no'], 0)
self.assertEqual(serial_scan['has_serial_no'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:74*

### test_barcode_scanning_of_warehouse

**Category**: workflow  
**Description**: Workflow: test barcode scanning of warehouse  
**Expected**: self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode', 'company': '_Test Company'}).insert()
warehouse_2 = frappe.get_doc({'doctype': 'Warehouse', 'warehouse_name': 'Test Warehouse for Barcode 2', 'company': '_Test Company'}).insert()
warehouse_scan = scan_barcode(warehouse.name)
self.assertEqual(warehouse_scan['warehouse'], warehouse.name)
item_with_warehouse = self.make_item(properties={'item_defaults': [{'company': '_Test Company', 'default_warehouse': warehouse.name}], 'barcodes': [{'barcode': 'w12345'}]})
item_scan = scan_barcode('w12345')
self.assertEqual(item_scan['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan.get('default_warehouse'), None)
ctx = {'company': '_Test Company'}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse.name)
ctx = {'company': '_Test Company', 'set_warehouse': warehouse_2.name}
item_scan_with_ctx = scan_barcode('w12345', ctx=ctx)
self.assertEqual(item_scan_with_ctx['item_code'], item_with_warehouse.name)
self.assertEqual(item_scan_with_ctx['default_warehouse'], warehouse_2.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:98*

### test_alternative_item_for_production_rm

**Category**: workflow  
**Description**: Workflow: test alternative item for production rm  
**Expected**: self.assertEqual(status, True)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
make_items()

create_stock_reconciliation(item_code='Alternate Item For A RW 1', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
create_stock_reconciliation(item_code='Test FG A RW 2', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
pro_order = make_wo_order_test_record(production_item='Test Finished Goods - A', qty=5, source_warehouse='_Test Warehouse - _TC', wip_warehouse='Test Supplier Warehouse - _TC')
reserved_qty_for_production = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
ste = frappe.get_doc(make_stock_entry(pro_order.name, 'Material Transfer for Manufacture', 5))
ste.insert()
for item in ste.items:
    if item.item_code == 'Test FG A RW 1':
        item.item_code = 'Alternate Item For A RW 1'
        item.item_name = 'Alternate Item For A RW 1'
        item.description = 'Alternate Item For A RW 1'
        item.original_item = 'Test FG A RW 1'
ste.submit()
reserved_qty_for_production_after_transfer = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
self.assertEqual(reserved_qty_for_production_after_transfer, flt(reserved_qty_for_production - 5))
ste1 = frappe.get_doc(make_stock_entry(pro_order.name, 'Manufacture', 5))
status = False
for d in ste1.items:
    if d.item_code == 'Alternate Item For A RW 1':
        status = True
self.assertEqual(status, True)
ste1.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:121*

### test_alternative_item_for_production_rm

**Category**: workflow  
**Description**: Workflow: test alternative item for production rm  
**Expected**: self.assertEqual(status, True)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
create_stock_reconciliation(item_code='Alternate Item For A RW 1', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
create_stock_reconciliation(item_code='Test FG A RW 2', warehouse='_Test Warehouse - _TC', qty=5, rate=2000)
pro_order = make_wo_order_test_record(production_item='Test Finished Goods - A', qty=5, source_warehouse='_Test Warehouse - _TC', wip_warehouse='Test Supplier Warehouse - _TC')
reserved_qty_for_production = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
ste = frappe.get_doc(make_stock_entry(pro_order.name, 'Material Transfer for Manufacture', 5))
ste.insert()
for item in ste.items:
    if item.item_code == 'Test FG A RW 1':
        item.item_code = 'Alternate Item For A RW 1'
        item.item_name = 'Alternate Item For A RW 1'
        item.description = 'Alternate Item For A RW 1'
        item.original_item = 'Test FG A RW 1'
ste.submit()
reserved_qty_for_production_after_transfer = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_production')
self.assertEqual(reserved_qty_for_production_after_transfer, flt(reserved_qty_for_production - 5))
ste1 = frappe.get_doc(make_stock_entry(pro_order.name, 'Manufacture', 5))
status = False
for d in ste1.items:
    if d.item_code == 'Alternate Item For A RW 1':
        status = True
self.assertEqual(status, True)
ste1.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:121*

### test_notify_reposting_error_to_role

**Category**: workflow  
**Description**: Workflow: test notify reposting error to role  
**Expected**: self.assertTrue(user in users)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
role = 'Notify Reposting Role'
if not frappe.db.exists('Role', role):
    frappe.get_doc({'doctype': 'Role', 'role_name': role}).insert(ignore_permissions=True)
user = 'notify_reposting_error@test.com'
if not frappe.db.exists('User', user):
    frappe.get_doc({'doctype': 'User', 'email': user, 'first_name': 'Test', 'language': 'en', 'time_zone': 'Asia/Kolkata', 'send_welcome_email': 0, 'roles': [{'role': role}]}).insert(ignore_permissions=True)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', '')
users = get_recipients()
self.assertFalse(user in users)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', role)
users = get_recipients()
self.assertTrue(user in users)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reposting_settings/test_stock_reposting_settings.py:11*

### test_notify_reposting_error_to_role

**Category**: workflow  
**Description**: Workflow: test notify reposting error to role  
**Expected**: self.assertTrue(user in users)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
role = 'Notify Reposting Role'
if not frappe.db.exists('Role', role):
    frappe.get_doc({'doctype': 'Role', 'role_name': role}).insert(ignore_permissions=True)
user = 'notify_reposting_error@test.com'
if not frappe.db.exists('User', user):
    frappe.get_doc({'doctype': 'User', 'email': user, 'first_name': 'Test', 'language': 'en', 'time_zone': 'Asia/Kolkata', 'send_welcome_email': 0, 'roles': [{'role': role}]}).insert(ignore_permissions=True)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', '')
users = get_recipients()
self.assertFalse(user in users)
frappe.db.set_single_value('Stock Reposting Settings', 'notify_reposting_error_to_role', role)
users = get_recipients()
self.assertTrue(user in users)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reposting_settings/test_stock_reposting_settings.py:11*

### test_batch_stock_levels

**Category**: workflow  
**Description**: Workflow: Test automated batch creation from Purchase Receipt  
**Expected**: self.assertTrue(receipt2.items[0].serial_and_batch_bundle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automated batch creation from Purchase Receipt'
self.make_batch_item('ITEM-BATCH-1')
receipt = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=10, rate=10, warehouse='Stores - _TC')]).insert()
receipt.submit()
receipt.load_from_db()
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
bundle_id = SerialBatchCreation({'item_code': 'ITEM-BATCH-1', 'warehouse': '_Test Warehouse - _TC', 'actual_qty': 20, 'voucher_type': 'Purchase Receipt', 'batches': frappe._dict({batch_no: 20}), 'type_of_transaction': 'Inward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
receipt2 = frappe.get_doc(doctype='Purchase Receipt', supplier='_Test Supplier', company='_Test Company', items=[dict(item_code='ITEM-BATCH-1', qty=20, rate=10, warehouse='_Test Warehouse - _TC', serial_and_batch_bundle=bundle_id)]).insert()
receipt2.submit()
receipt.load_from_db()
receipt2.load_from_db()
self.assertTrue(receipt.items[0].serial_and_batch_bundle)
self.assertTrue(receipt2.items[0].serial_and_batch_bundle)
batchwise_qty = frappe._dict({})
for r in [receipt, receipt2]:
    batch_no = get_batch_from_bundle(r.items[0].serial_and_batch_bundle)
    key = (batch_no, r.items[0].warehouse)
    batchwise_qty[key] = r.items[0].qty
batches = get_batch_qty(batch_no)
for d in batches:
    self.assertEqual(d.qty, batchwise_qty[d.batch_no, d.warehouse])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:62*

### test_delivery_note

**Category**: workflow  
**Description**: Workflow: Test automatic batch selection for outgoing items  
**Expected**: self.assertEqual(get_batch_from_bundle(delivery_note.items[0].serial_and_batch_bundle), batch_no)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automatic batch selection for outgoing items'
batch_qty = 15
receipt = self.test_purchase_receipt(batch_qty)
item_code = 'ITEM-BATCH-1'
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
bundle_id = SerialBatchCreation({'item_code': item_code, 'warehouse': receipt.items[0].warehouse, 'actual_qty': batch_qty, 'voucher_type': 'Stock Entry', 'batches': frappe._dict({batch_no: batch_qty}), 'type_of_transaction': 'Outward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
delivery_note = frappe.get_doc(doctype='Delivery Note', customer='_Test Customer', company=receipt.company, items=[dict(item_code=item_code, qty=batch_qty, rate=10, warehouse=receipt.items[0].warehouse, serial_and_batch_bundle=bundle_id)]).insert()
delivery_note.submit()
receipt.load_from_db()
delivery_note.load_from_db()
self.assertEqual(get_batch_from_bundle(delivery_note.items[0].serial_and_batch_bundle), batch_no)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:156*

### test_stock_entry_outgoing

**Category**: workflow  
**Description**: Workflow: Test automatic batch selection for outgoing stock entry  
**Expected**: self.assertEqual(get_batch_from_bundle(stock_entry.items[0].serial_and_batch_bundle), get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test automatic batch selection for outgoing stock entry'
batch_qty = 16
receipt = self.test_purchase_receipt(batch_qty)
item_code = 'ITEM-BATCH-1'
batch_no = get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle)
bundle_id = SerialBatchCreation({'item_code': item_code, 'warehouse': receipt.items[0].warehouse, 'actual_qty': batch_qty, 'voucher_type': 'Stock Entry', 'batches': frappe._dict({batch_no: batch_qty}), 'type_of_transaction': 'Outward', 'company': receipt.company, 'do_not_submit': 1}).make_serial_and_batch_bundle().name
stock_entry = frappe.get_doc(doctype='Stock Entry', purpose='Material Issue', company=receipt.company, items=[dict(item_code=item_code, qty=batch_qty, s_warehouse=receipt.items[0].warehouse, serial_and_batch_bundle=bundle_id)])
stock_entry.set_stock_entry_type()
stock_entry.insert()
stock_entry.submit()
stock_entry.load_from_db()
self.assertEqual(get_batch_from_bundle(stock_entry.items[0].serial_and_batch_bundle), get_batch_from_bundle(receipt.items[0].serial_and_batch_bundle))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:227*

### test_ignore_reserved_qty

**Category**: workflow  
**Description**: Workflow: test ignore reserved qty  
**Expected**: self.assertEqual(batch.batch_qty, 90)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.sales_order.sales_order import create_pick_list
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
batch_item_name = 'Reserve Batch Item'
batch_id = 'Reserve Batch 1'
self.make_batch_item(batch_item_name)
self.make_new_batch_and_entry(batch_item_name, batch_id, '_Test Warehouse - _TC')
frappe.db.set_single_value('Stock Settings', 'enable_stock_reservation', 1)
sales_order = make_sales_order(item_code=batch_item_name, warehouse='_Test Warehouse - _TC', qty=50, rate=20)
pl = create_pick_list(sales_order.name)
pl.submit()
pl.create_stock_reservation_entries(notify=False)
batch = frappe.get_doc('Batch', batch_id)
batch.recalculate_batch_qty()
batch.reload()
self.assertEqual(batch.batch_qty, 90)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:315*

### test_total_batch_qty

**Category**: workflow  
**Description**: Workflow: test total batch qty  
**Expected**: self.assertEqual(current_batch_qty, existing_batch_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.make_batch_item('ITEM-BATCH-3')
existing_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
stock_entry = self.make_new_batch_and_entry('ITEM-BATCH-3', 'B100', '_Test Warehouse - _TC')
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
self.assertEqual(current_batch_qty, existing_batch_qty + 90)
stock_entry.cancel()
current_batch_qty = flt(frappe.db.get_value('Batch', 'B100', 'batch_qty'))
self.assertEqual(current_batch_qty, existing_batch_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:347*

### test_batch_name_with_naming_series

**Category**: workflow  
**Description**: Workflow: test batch name with naming series  
**Expected**: self.assertEqual(batch_name, batch.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
stock_settings = frappe.get_single('Stock Settings')
use_naming_series = cint(stock_settings.use_naming_series)
if not use_naming_series:
    frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 1)
batch = self.make_new_batch('_Test Stock Item For Batch Test1')
batch_name = batch.name
self.assertTrue(batch_name.startswith('BATCH-'))
batch.delete()
batch = self.make_new_batch('_Test Stock Item For Batch Test2')
self.assertEqual(batch_name, batch.name)
if not use_naming_series:
    frappe.set_value('Stock Settings', 'Stock Settings', 'use_naming_series', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:406*

### test_batch_wise_item_price

**Category**: workflow  
**Description**: Workflow: test batch wise item price  
**Expected**: self.assertEqual(details.get('price_list_rate'), 400)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
if not frappe.db.get_value('Item', '_Test Batch Price Item'):
    frappe.get_doc({'doctype': 'Item', 'is_stock_item': 1, 'item_code': '_Test Batch Price Item', 'item_group': 'Products', 'has_batch_no': 1, 'create_new_batch': 1}).insert(ignore_permissions=True)
batch1 = create_batch('_Test Batch Price Item', 200, 1)
batch2 = create_batch('_Test Batch Price Item', 300, 1)
batch3 = create_batch('_Test Batch Price Item', 400, 0)
company = '_Test Company with perpetual inventory'
currency = frappe.get_cached_value('Company', company, 'default_currency')
ctx = ItemDetailsCtx({'item_code': '_Test Batch Price Item', 'company': company, 'price_list': '_Test Price List', 'currency': currency, 'doctype': 'Sales Invoice', 'conversion_rate': 1, 'price_list_currency': '_Test Currency', 'plc_conversion_rate': 1, 'customer': '_Test Customer', 'name': None})
ctx.update({'batch_no': batch1})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 200)
ctx.update({'batch_no': batch2})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 300)
ctx.update({'batch_no': batch3})
details = get_item_details(ctx)
self.assertEqual(details.get('price_list_rate'), 400)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:440*

### test_basic_batch_wise_valuation

**Category**: workflow  
**Description**: Workflow: test basic batch wise valuation  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_TestBatchWiseVal'
warehouse = '_Test Warehouse - _TC'
self.make_batch_item(item_code)
rates = [42, 420]
batches = {}
for rate in rates:
    se = make_stock_entry(item_code=item_code, qty=10, rate=rate, target=warehouse)
    batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
    batches[batch_no] = rate
LOW, HIGH = list(batches.keys())
consumption_plan = [(HIGH, 1), (LOW, 2), (HIGH, 2), (HIGH, 4), (LOW, 6)]
stock_value = sum(rates) * 10
qty_after_transaction = 20
for batch, qty in consumption_plan:
    se = make_stock_entry(item_code=item_code, source=warehouse, qty=qty, batch_no=batch)
    sle = frappe.get_last_doc('Stock Ledger Entry', {'is_cancelled': 0, 'voucher_no': se.name})
    stock_value_difference = sle.actual_qty * batches[get_batch_from_bundle(sle.serial_and_batch_bundle)]
    self.assertAlmostEqual(sle.stock_value_difference, stock_value_difference)
    stock_value += stock_value_difference
    self.assertAlmostEqual(sle.stock_value, stock_value)
    qty_after_transaction += sle.actual_qty
    self.assertAlmostEqual(sle.qty_after_transaction, qty_after_transaction)
    self.assertAlmostEqual(sle.valuation_rate, stock_value / qty_after_transaction)
    self.assertEqual(json.loads(sle.stock_queue), [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:490*

### test_update_batch_properties

**Category**: workflow  
**Description**: Workflow: test update batch properties  
**Expected**: self.assertEqual(getdate(batch.expiry_date), getdate(expiry_date))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_TestBatchWiseVal'
self.make_batch_item(item_code)
se = make_stock_entry(item_code=item_code, qty=100, rate=10, target='_Test Warehouse - _TC')
batch_no = get_batch_from_bundle(se.items[0].serial_and_batch_bundle)
batch = frappe.get_doc('Batch', batch_no)
expiry_date = add_to_date(batch.manufacturing_date, days=30)
batch.expiry_date = expiry_date
batch.save()
batch.reload()
self.assertEqual(getdate(batch.expiry_date), getdate(expiry_date))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:536*

### test_autocreation_of_batches

**Category**: workflow  
**Description**: Workflow: Test if auto created Serial No excludes existing serial numbers  
**Expected**: self.assertEqual('BATCHEXISTING002', get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest if auto created Serial No excludes existing serial numbers\n\t\t'
item_code = make_item(properties={'has_batch_no': 1, 'batch_number_series': 'BATCHEXISTING.###', 'create_new_batch': 1}).name
manually_created_batch = self.make_new_batch(item_code, batch_id='BATCHEXISTING001').name
pr_1 = make_purchase_receipt(item_code=item_code, qty=1, batch_no=manually_created_batch)
pr_2 = make_purchase_receipt(item_code=item_code, qty=1)
pr_1.load_from_db()
pr_2.load_from_db()
self.assertNotEqual(get_batch_from_bundle(pr_1.items[0].serial_and_batch_bundle), get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
self.assertEqual('BATCHEXISTING002', get_batch_from_bundle(pr_2.items[0].serial_and_batch_bundle))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/batch/test_batch.py:553*

### test_make_quality_inspections_from_linked_document

**Category**: workflow  
**Description**: Workflow: test make quality inspections from linked document  
**Expected**: self.assertEqual(len(dn.items), len(quality_inspections))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
if dn.doctype in ['Purchase Receipt', 'Purchase Invoice', 'Subcontracting Receipt']:
    inspection_type = 'Incoming'
else:
    inspection_type = 'Outgoing'
for item in dn.items:
    item.sample_size = item.qty
quality_inspections = make_quality_inspections(dn.doctype, dn.name, dn.items, inspection_type)
self.assertEqual(len(dn.items), len(quality_inspections))
for qi in quality_inspections:
    frappe.delete_doc('Quality Inspection', qi)
dn.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:137*

### test_qi_status

**Category**: workflow  
**Description**: Workflow: test qi status  
**Expected**: self.assertEqual(qa.status, 'Accepted')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

make_stock_entry(item_code='_Test Item with QA', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
qa = create_quality_inspection(reference_type='Delivery Note', reference_name=dn.name, status='Accepted', do_not_save=True)
qa.readings[0].manual_inspection = 1
qa.save()
qa.status = 'Accepted'
qa.manual_inspection = 0
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Rejected')
qa.status = 'Rejected'
qa.manual_inspection = 0
qa.readings[0].status = 'Accepted'
qa.save()
self.assertEqual(qa.status, 'Accepted')
qa.status = 'Accepted'
qa.manual_inspection = 1
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Accepted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:187*

### test_delete_quality_inspection_linked_with_stock_entry

**Category**: workflow  
**Description**: Workflow: test delete quality inspection linked with stock entry  
**Expected**: self.assertFalse(qc)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

item_code = create_item('_Test Cicuular Dependecy Item with QA').name
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=1, basic_rate=100, do_not_submit=True)
se.inspection_required = 1
se.save()
qa = create_quality_inspection(item_code=item_code, reference_type='Stock Entry', reference_name=se.name, do_not_submit=True)
se.reload()
se.items[0].quality_inspection = qa.name
se.save()
qa.delete()
se.reload()
qc = se.items[0].quality_inspection
self.assertFalse(qc)
se.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:253*

### test_make_quality_inspections_from_linked_document

**Category**: workflow  
**Description**: Workflow: test make quality inspections from linked document  
**Expected**: self.assertEqual(len(dn.items), len(quality_inspections))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
if dn.doctype in ['Purchase Receipt', 'Purchase Invoice', 'Subcontracting Receipt']:
    inspection_type = 'Incoming'
else:
    inspection_type = 'Outgoing'
for item in dn.items:
    item.sample_size = item.qty
quality_inspections = make_quality_inspections(dn.doctype, dn.name, dn.items, inspection_type)
self.assertEqual(len(dn.items), len(quality_inspections))
for qi in quality_inspections:
    frappe.delete_doc('Quality Inspection', qi)
dn.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:137*

### test_qi_status

**Category**: workflow  
**Description**: Workflow: test qi status  
**Expected**: self.assertEqual(qa.status, 'Accepted')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_stock_entry(item_code='_Test Item with QA', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
dn = create_delivery_note(item_code='_Test Item with QA', do_not_submit=True)
qa = create_quality_inspection(reference_type='Delivery Note', reference_name=dn.name, status='Accepted', do_not_save=True)
qa.readings[0].manual_inspection = 1
qa.save()
qa.status = 'Accepted'
qa.manual_inspection = 0
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Rejected')
qa.status = 'Rejected'
qa.manual_inspection = 0
qa.readings[0].status = 'Accepted'
qa.save()
self.assertEqual(qa.status, 'Accepted')
qa.status = 'Accepted'
qa.manual_inspection = 1
qa.readings[0].status = 'Rejected'
qa.save()
self.assertEqual(qa.status, 'Accepted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:187*

### test_delete_quality_inspection_linked_with_stock_entry

**Category**: workflow  
**Description**: Workflow: test delete quality inspection linked with stock entry  
**Expected**: self.assertFalse(qc)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = create_item('_Test Cicuular Dependecy Item with QA').name
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=1, basic_rate=100, do_not_submit=True)
se.inspection_required = 1
se.save()
qa = create_quality_inspection(item_code=item_code, reference_type='Stock Entry', reference_name=se.name, do_not_submit=True)
se.reload()
se.items[0].quality_inspection = qa.name
se.save()
qa.delete()
se.reload()
qc = se.items[0].quality_inspection
self.assertFalse(qc)
se.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:253*

### test_delivery_note_gl_entry_packing_item

**Category**: workflow  
**Description**: Workflow: test delivery note gl entry packing item  
**Expected**: self.assertEqual(flt(bal, 2), flt(prev_bal - stock_value_diff, 2))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', qty=10, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - TCP1', qty=10, basic_rate=100)
stock_in_hand_account = get_inventory_account('_Test Company with perpetual inventory')
prev_bal = get_balance_on(stock_in_hand_account)
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1')
stock_value_diff_rm1 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
stock_value_diff_rm2 = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
stock_value_diff = stock_value_diff_rm1 + stock_value_diff_rm2
gl_entries = get_gl_entries('Delivery Note', dn.name)
self.assertTrue(gl_entries)
expected_values = {stock_in_hand_account: [0.0, stock_value_diff], 'Cost of Goods Sold - TCP1': [stock_value_diff, 0.0]}
for _i, gle in enumerate(gl_entries):
    self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
bal = get_balance_on(stock_in_hand_account)
self.assertEqual(flt(bal, 2), flt(prev_bal - stock_value_diff, 2))
dn.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:96*

### test_sales_return_for_non_bundled_items_full

**Category**: workflow  
**Description**: Workflow: test sales return for non bundled items full  
**Expected**: self.assertEqual(dn.status, 'Return Issued')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_item('Box', {'is_stock_item': 1})
make_stock_entry(item_code='Box', target='Stores - TCP1', qty=10, basic_rate=100)
dn = create_delivery_note(item_code='Box', qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
dn1 = create_delivery_note(item_code='Box', is_return=1, return_against=dn.name, qty=-5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1', do_not_submit=1)
dn1.items[0].dn_detail = dn.items[0].name
dn1.submit()
returned = frappe.get_doc('Delivery Note', dn1.name)
returned.update_prevdoc_status()
dn.load_from_db()
self.assertEqual(dn.items[0].returned_qty, 5)
self.assertEqual(dn.per_returned, 100)
self.assertEqual(dn.status, 'Return Issued')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:392*

### test_delivery_note_return_valuation_on_different_warehouse

**Category**: workflow  
**Description**: Workflow: test delivery note return valuation on different warehouse  
**Expected**: self.assertEqual(return_dn.items[0].incoming_rate, 150)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.warehouse.test_warehouse import create_warehouse
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
item_code = 'Test Return Valuation For DN'
make_item('Test Return Valuation For DN', {'is_stock_item': 1})
return_warehouse = create_warehouse('Returned Test Warehouse', company=company)
make_stock_entry(item_code=item_code, target='Stores - TCP1', qty=5, basic_rate=150)
dn = create_delivery_note(item_code=item_code, qty=5, rate=500, warehouse='Stores - TCP1', company=company, expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
dn.submit()
self.assertEqual(dn.items[0].incoming_rate, 150)
from erpnext.controllers.sales_and_purchase_return import make_return_doc
return_dn = make_return_doc(dn.doctype, dn.name)
return_dn.items[0].warehouse = return_warehouse
return_dn.save().submit()
self.assertEqual(return_dn.items[0].incoming_rate, 150)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:435*

### test_return_single_item_from_bundled_items

**Category**: workflow  
**Description**: Workflow: test return single item from bundled items  
**Expected**: self.assertEqual(gle_warehouse_amount, stock_value_difference)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
create_stock_reconciliation(item_code='_Test Item', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
create_stock_reconciliation(item_code='_Test Item Home Desktop 100', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
dn = create_delivery_note(item_code='_Test Product Bundle Item', qty=5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty_1 = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_1, 25)
outgoing_rate = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item'}, 'stock_value_difference') / 25
dn1 = create_delivery_note(is_return=1, return_against=dn.name, qty=-10, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty_2 = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_2, 35)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(flt(incoming_rate, 3), abs(flt(outgoing_rate, 3)))
stock_in_hand_account = get_inventory_account(company, dn1.items[0].warehouse)
gle_warehouse_amount = frappe.db.get_value('GL Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name, 'account': stock_in_hand_account}, 'debit')
self.assertEqual(gle_warehouse_amount, stock_value_difference)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:558*

### test_return_entire_bundled_items

**Category**: workflow  
**Description**: Workflow: test return entire bundled items  
**Expected**: self.assertEqual(gle_warehouse_amount, 1400)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
create_stock_reconciliation(item_code='_Test Item', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
create_stock_reconciliation(item_code='_Test Item Home Desktop 100', warehouse='Stores - TCP1', qty=50, rate=100, company=company, expense_account='Stock Adjustment - TCP1')
actual_qty = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty, 50)
dn = create_delivery_note(item_code='_Test Product Bundle Item', qty=5, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty, 25)
dn1 = create_delivery_note(item_code='_Test Product Bundle Item', is_return=1, return_against=dn.name, qty=-2, rate=500, company=company, warehouse='Stores - TCP1', expense_account='Cost of Goods Sold - TCP1', cost_center='Main - TCP1')
actual_qty = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty, 35)
incoming_rate, stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name}, ['incoming_rate', 'stock_value_difference'])
self.assertEqual(incoming_rate, 100)
stock_in_hand_account = get_inventory_account('_Test Company', dn1.items[0].warehouse)
gle_warehouse_amount = frappe.db.get_value('GL Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn1.name, 'account': stock_in_hand_account}, 'debit')
self.assertEqual(gle_warehouse_amount, 1400)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:637*

### test_bin_details_of_packed_item

**Category**: workflow  
**Description**: Workflow: test bin details of packed item  
**Expected**: self.assertEqual(flt(bin_details.ordered_qty), flt(packed_item.ordered_qty))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.product_bundle.test_product_bundle import make_product_bundle
from erpnext.stock.doctype.item.test_item import make_item
if not frappe.db.exists('Item', '_Test Product Bundle Item New'):
    bundle_item = make_item('_Test Product Bundle Item New', {'is_stock_item': 0})
    bundle_item.append('item_defaults', {'company': '_Test Company', 'default_warehouse': '_Test Warehouse - _TC'})
    bundle_item.save(ignore_permissions=True)
make_item('_Packed Item New 1', {'is_stock_item': 1})
make_product_bundle('_Test Product Bundle Item New', ['_Packed Item New 1'], 2)
si = create_delivery_note(item_code='_Test Product Bundle Item New', update_stock=1, warehouse='_Test Warehouse - _TC', transaction_date=add_days(nowdate(), -1), do_not_submit=1)
make_stock_entry(item='_Packed Item New 1', target='_Test Warehouse - _TC', qty=120, rate=100)
bin_details = frappe.db.get_value('Bin', {'item_code': '_Packed Item New 1', 'warehouse': '_Test Warehouse - _TC'}, ['actual_qty', 'projected_qty', 'ordered_qty'], as_dict=1)
si.transaction_date = nowdate()
si.save()
packed_item = si.packed_items[0]
self.assertEqual(flt(bin_details.actual_qty), flt(packed_item.actual_qty))
self.assertEqual(flt(bin_details.projected_qty), flt(packed_item.projected_qty))
self.assertEqual(flt(bin_details.ordered_qty), flt(packed_item.ordered_qty))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:710*

### test_return_for_serialized_items

**Category**: workflow  
**Description**: Workflow: test return for serialized items  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
se = make_serialized_item(self)
serial_no = [get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)[0]]
dn = create_delivery_note(item_code='_Test Serialized Item With Series', rate=500, serial_no=serial_no)
self.check_serial_no_values(serial_no, {'warehouse': ''})
dn1 = create_delivery_note(item_code='_Test Serialized Item With Series', is_return=1, return_against=dn.name, qty=-1, rate=500, serial_no=serial_no)
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
dn1.cancel()
self.check_serial_no_values(serial_no, {'warehouse': ''})
dn.cancel()
self.check_serial_no_values(serial_no, {'warehouse': '_Test Warehouse - _TC'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:750*

### test_delivery_note_internal_transfer_serial_no_status

**Category**: workflow  
**Description**: Workflow: test delivery note internal transfer serial no status  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.customer.test_customer import create_internal_customer
item = make_item('_Test Item for Internal Transfer With Serial No Status', properties={'has_serial_no': 1, 'is_stock_item': 1, 'serial_no_series': 'INT-SN-.####'}).name
warehouse = '_Test Warehouse - _TC'
target = 'Stores - _TC'
company = '_Test Company'
customer = create_internal_customer(represents_company=company)
rate = 42
se = make_stock_entry(target=warehouse, qty=5, basic_rate=rate, item_code=item)
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
dn = create_delivery_note(item_code=item, company=company, customer=customer, qty=5, rate=500, warehouse=warehouse, target_warehouse=target, ignore_pricing_rule=0, use_serial_batch_fields=1, serial_no='\n'.join(serial_nos))
for serial_no in serial_nos:
    sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
    self.assertEqual(sn.status, 'Active')
    self.assertEqual(sn.warehouse, target)
dn.cancel()
for serial_no in serial_nos:
    sn = frappe.db.get_value('Serial No', serial_no, ['status', 'warehouse'], as_dict=1)
    self.assertEqual(sn.status, 'Active')
    self.assertEqual(sn.warehouse, warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:784*

### test_delivery_of_bundled_items_to_target_warehouse

**Category**: workflow  
**Description**: Workflow: test delivery of bundled items to target warehouse  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.customer.test_customer import create_internal_customer
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
customer_name = create_internal_customer(customer_name='_Test Internal Customer 2', represents_company='_Test Company with perpetual inventory', allowed_to_interact_with='_Test Company with perpetual inventory')
set_valuation_method('_Test Item', 'FIFO')
set_valuation_method('_Test Item Home Desktop 100', 'FIFO')
target_warehouse = get_warehouse(company=company, abbr='TCP1', warehouse_name='_Test Customer Warehouse').name
for warehouse in ('Stores - TCP1', target_warehouse):
    create_stock_reconciliation(item_code='_Test Item', warehouse=warehouse, company=company, expense_account='Stock Adjustment - TCP1', qty=500, rate=100)
    create_stock_reconciliation(item_code='_Test Item Home Desktop 100', company=company, expense_account='Stock Adjustment - TCP1', warehouse=warehouse, qty=500, rate=100)
dn = create_delivery_note(item_code='_Test Product Bundle Item', company='_Test Company with perpetual inventory', customer=customer_name, cost_center='Main - TCP1', expense_account='Cost of Goods Sold - TCP1', qty=5, rate=500, warehouse='Stores - TCP1', target_warehouse=target_warehouse)
actual_qty_at_source = get_qty_after_transaction(warehouse='Stores - TCP1')
self.assertEqual(actual_qty_at_source, 475)
actual_qty_at_target = get_qty_after_transaction(warehouse=target_warehouse)
self.assertEqual(actual_qty_at_target, 525)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': 'Stores - TCP1'}, 'stock_value_difference')
stock_value_difference1 = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Delivery Note', 'voucher_no': dn.name, 'item_code': '_Test Item', 'warehouse': target_warehouse}, 'stock_value_difference')
self.assertEqual(abs(stock_value_difference), stock_value_difference1)
gl_entries = get_gl_entries('Delivery Note', dn.name)
self.assertTrue(gl_entries)
stock_value_difference = abs(frappe.db.sql("select sum(stock_value_difference)\n\t\t\tfrom `tabStock Ledger Entry` where voucher_type='Delivery Note' and voucher_no=%s\n\t\t\tand warehouse='Stores - TCP1'", dn.name)[0][0])
expected_values = {'Stock In Hand - TCP1': [0.0, stock_value_difference], target_warehouse: [stock_value_difference, 0.0]}
for _i, gle in enumerate(gl_entries):
    self.assertEqual([gle.debit, gle.credit], expected_values.get(gle.account))
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:826*

### test_sales_order_reference_validation

**Category**: workflow  
**Description**: Workflow: test sales order reference validation  
**Expected**: self.assertRaises(frappe.ValidationError, dn.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
so = make_sales_order(po_no='12345')
dn = create_dn_against_so(so.name, delivered_qty=2, do_not_submit=True)
dn.items[0].against_sales_order = None
self.assertRaises(frappe.ValidationError, dn.save)
dn.reload()
dn.items[0].so_detail = None
self.assertRaises(frappe.ValidationError, dn.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_note/test_delivery_note.py:952*

### test_inward_outward_serial_valuation

**Category**: workflow  
**Description**: Workflow: test inward outward serial valuation  
**Expected**: self.assertEqual(flt(stock_value_difference, 2), -500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_item_code = 'New Serial No Valuation 1'
make_item(serial_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VAL-.#####', 'is_stock_item': 1})
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
serial_no1 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
pr = make_purchase_receipt(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
serial_no2 = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no2])
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -300)
dn = create_delivery_note(item_code=serial_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=1500, serial_no=[serial_no1])
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:82*

### test_inward_outward_batch_valuation

**Category**: workflow  
**Description**: Workflow: test inward outward batch valuation  
**Expected**: self.assertEqual(flt(stock_value_difference, 2), -5000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
batch_item_code = 'New Batch No Valuation 1'
make_item(batch_item_code, {'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-BATTCCH-VAL-.#####', 'is_stock_item': 1})
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=500)
batch_no1 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
pr = make_purchase_receipt(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=300)
batch_no2 = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no2)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -3000)
dn = create_delivery_note(item_code=batch_item_code, warehouse='_Test Warehouse - _TC', qty=10, rate=1500, batch_no=batch_no1)
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(flt(stock_value_difference, 2), -5000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:140*

### test_old_serial_no_valuation

**Category**: workflow  
**Description**: Workflow: test old serial no valuation  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_no_item_code = 'Old Serial No Item Valuation 1'
make_item(serial_no_item_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
make_purchase_receipt(item_code=serial_no_item_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
frappe.flags.ignore_serial_batch_bundle_validation = True
frappe.flags.use_serial_and_batch_fields = True
serial_no_id = 'Old Serial No 1'
if not frappe.db.exists('Serial No', serial_no_id):
    sn_doc = frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no_id, 'item_code': serial_no_item_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
    sn_doc.db_set({'warehouse': '_Test Warehouse - _TC', 'purchase_rate': 100})
doc = frappe.get_doc({'doctype': 'Stock Ledger Entry', 'posting_date': today(), 'posting_time': nowtime(), 'serial_no': serial_no_id, 'incoming_rate': 100, 'qty_after_transaction': 1, 'stock_value_difference': 100, 'balance_value': 100, 'valuation_rate': 100, 'actual_qty': 1, 'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company'})
doc.flags.ignore_permissions = True
doc.flags.ignore_mandatory = True
doc.flags.ignore_links = True
doc.flags.ignore_validate = True
doc.submit()
bundle_doc = make_serial_batch_bundle({'item_code': serial_no_item_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'serial_nos': [serial_no_id], 'type_of_transaction': 'Outward', 'do_not_submit': True})
bundle_doc.reload()
for row in bundle_doc.entries:
    self.assertEqual(flt(row.stock_value_difference, 2), -100.0)
frappe.flags.ignore_serial_batch_bundle_validation = False
frappe.flags.use_serial_and_batch_fields = False
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:362*

### test_batch_not_belong_to_serial_no

**Category**: workflow  
**Description**: Workflow: test batch not belong to serial no  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, doc.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
serial_and_batch_code = 'New Serial No Valuation 1'
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'TEST-SNBAT-VAL-.#####'})
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=500)
serial_no = get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle)[0]
pr = make_purchase_receipt(item_code=serial_and_batch_code, warehouse='_Test Warehouse - _TC', qty=1, rate=300)
batch_no = get_batch_from_bundle(pr.items[0].serial_and_batch_bundle)
doc = frappe.get_doc({'doctype': 'Serial and Batch Bundle', 'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': today(), 'posting_time': nowtime(), 'qty': -1, 'type_of_transaction': 'Outward'})
doc.append('entries', {'batch_no': batch_no, 'serial_no': serial_no, 'qty': -1})
self.assertRaises(frappe.exceptions.ValidationError, doc.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:445*

### test_auto_delete_draft_serial_and_batch_bundle

**Category**: workflow  
**Description**: Workflow: test auto delete draft serial and batch bundle  
**Expected**: self.assertFalse(frappe.db.exists('Serial and Batch Bundle', bundle_doc.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
serial_and_batch_code = 'New Serial No Auto Delete 1'
make_item(serial_and_batch_code, {'has_serial_no': 1, 'serial_no_series': 'TEST-SER-VALL-.#####', 'is_stock_item': 1})
ste = make_stock_entry(item_code=serial_and_batch_code, target='_Test Warehouse - _TC', qty=1, rate=500, do_not_submit=True)
serial_no = 'SN-TEST-AUTO-DEL'
if not frappe.db.exists('Serial No', serial_no):
    frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': serial_and_batch_code, 'company': '_Test Company'}).insert(ignore_permissions=True)
bundle_doc = make_serial_batch_bundle({'item_code': serial_and_batch_code, 'warehouse': '_Test Warehouse - _TC', 'voucher_type': 'Stock Entry', 'posting_date': ste.posting_date, 'posting_time': ste.posting_time, 'qty': 1, 'serial_nos': [serial_no], 'type_of_transaction': 'Inward', 'do_not_submit': True})
bundle_doc.reload()
ste.items[0].serial_and_batch_bundle = bundle_doc.name
ste.save()
ste.reload()
ste.delete()
self.assertFalse(frappe.db.exists('Serial and Batch Bundle', bundle_doc.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:498*

### test_serial_and_batch_bundle_company

**Category**: workflow  
**Description**: Workflow: test serial and batch bundle company  
**Expected**: self.assertEqual(sn_doc.company, '_Test Company')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
item = make_item('Test Serial and Batch Bundle Company Item', properties={'has_serial_no': 1, 'serial_no_series': 'TT-SER-VAL-.#####'}).name
pr = make_purchase_receipt(item_code=item, warehouse='_Test Warehouse - _TC', qty=3, rate=500, do_not_submit=True)
entries = []
for serial_no in ['TT-SER-VAL-00001', 'TT-SER-VAL-00002', 'TT-SER-VAL-00003']:
    entries.append(frappe._dict({'serial_no': serial_no, 'qty': 1}))
    if not frappe.db.exists('Serial No', serial_no):
        frappe.get_doc({'doctype': 'Serial No', 'serial_no': serial_no, 'item_code': item}).insert(ignore_permissions=True)
item_row = pr.items[0]
item_row.type_of_transaction = 'Inward'
item_row.is_rejected = 0
sn_doc = add_serial_batch_ledgers(entries, item_row, pr, '_Test Warehouse - _TC')
self.assertEqual(sn_doc.company, '_Test Company')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:550*

### test_auto_cancel_serial_and_batch

**Category**: workflow  
**Description**: Workflow: test auto cancel serial and batch  
**Expected**: self.assertEqual(docstatus, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = make_item(properties={'has_serial_no': 1, 'serial_no_series': 'ATC-TT-SER-VAL-.#####'}).name
se = make_stock_entry(item_code=item_code, target='_Test Warehouse - _TC', qty=5, rate=500)
bundle = se.items[0].serial_and_batch_bundle
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
self.assertEqual(docstatus, 1)
se.cancel()
docstatus = frappe.db.get_value('Serial and Batch Bundle', bundle, 'docstatus')
self.assertEqual(docstatus, 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:588*

### test_batch_duplicate_entry

**Category**: workflow  
**Description**: Workflow: test batch duplicate entry  
**Expected**: self.assertTrue(frappe.db.exists('Batch', batch_id))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = make_item(properties={'has_batch_no': 1}).name
batch_id = 'TEST-BATTCCH-VAL-00001'
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
make_batch_nos(item_code, batch_nos)
self.assertTrue(frappe.db.exists('Batch', batch_id))
use_batchwise_valuation = frappe.db.get_value('Batch', batch_id, 'use_batchwise_valuation')
self.assertEqual(use_batchwise_valuation, 1)
batch_id = 'TEST-BATTCCH-VAL-00001'
batch_nos = [{'batch_no': batch_id, 'qty': 1}]
make_batch_nos(item_code, batch_nos)
self.assertTrue(frappe.db.exists('Batch', batch_id))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:608*

### test_serial_no_duplicate_entry

**Category**: workflow  
**Description**: Workflow: test serial no duplicate entry  
**Expected**: self.assertTrue(frappe.db.exists('Serial No', serial_no_id))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = make_item(properties={'has_serial_no': 1}).name
serial_no_id = 'TEST-SNID-VAL-00001'
serial_nos = [{'serial_no': serial_no_id, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
serial_no_id = 'TEST-SNID-VAL-00001'
serial_nos = [{'batch_no': serial_no_id, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
self.assertTrue(frappe.db.exists('Serial No', serial_no_id))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:626*

### test_duplicate_serial_and_batch_bundle

**Category**: workflow  
**Description**: Workflow: test duplicate serial and batch bundle  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, pr2.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.purchase_receipt.test_purchase_receipt import make_purchase_receipt
item_code = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1}).name
serial_no = f'{item_code}-001'
serial_nos = [{'serial_no': serial_no, 'qty': 1}]
make_serial_nos(item_code, serial_nos)
pr1 = make_purchase_receipt(item=item_code, qty=1, rate=500, serial_no=[serial_no])
pr2 = make_purchase_receipt(item=item_code, qty=1, rate=500, do_not_save=True)
pr1.reload()
pr2.items[0].serial_and_batch_bundle = pr1.items[0].serial_and_batch_bundle
self.assertRaises(frappe.exceptions.ValidationError, pr2.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_and_batch_bundle/test_serial_and_batch_bundle.py:645*

### test_empty_duplicate_validation

**Category**: workflow  
**Description**: Workflow: test empty duplicate validation  
**Expected**: self.assertEqual(price, 21)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

doc = frappe.copy_doc(self.globalTestRecords['Item Price'][2])
doc.customer = None
doc.price_list_rate = 21
doc.insert()
ctx = ItemDetailsCtx({'price_list': doc.price_list, 'uom': '_Test UOM', 'transaction_date': '2017-04-18', 'qty': 7})
price = get_price_list_rate_for(ctx, doc.item_code)
frappe.db.rollback()
self.assertEqual(price, 21)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:181*

### test_empty_duplicate_validation

**Category**: workflow  
**Description**: Workflow: test empty duplicate validation  
**Expected**: self.assertEqual(price, 21)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
doc = frappe.copy_doc(self.globalTestRecords['Item Price'][2])
doc.customer = None
doc.price_list_rate = 21
doc.insert()
ctx = ItemDetailsCtx({'price_list': doc.price_list, 'uom': '_Test UOM', 'transaction_date': '2017-04-18', 'qty': 7})
price = get_price_list_rate_for(ctx, doc.item_code)
frappe.db.rollback()
self.assertEqual(price, 21)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:181*

### test_purchase_receipt_qty

**Category**: workflow  
**Description**: Workflow: test purchase receipt qty  
**Expected**: self.assertEqual(pr.items[0].rejected_qty, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

pr = make_purchase_receipt(qty=0, rejected_qty=0, do_not_save=True)
with self.assertRaises(InvalidQtyError):
    pr.save()
pr.items[0].qty = 1
pr.save()
self.assertEqual(pr.items[0].qty, 1)
pr.items[0].rejected_warehouse = '_Test Rejected Warehouse - _TC'
pr.items[0].rejected_qty = 1
pr.items[0].qty = 0
pr.save()
self.assertEqual(pr.items[0].rejected_qty, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:35*

### test_make_purchase_invoice

**Category**: workflow  
**Description**: Workflow: test make purchase invoice  
**Expected**: self.assertEqual(pi.payment_schedule[1].invoice_portion, 50)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

from erpnext.accounts.doctype.payment_entry.test_payment_entry import create_payment_term
create_payment_term('_Test Payment Term 1 for Purchase Invoice')
create_payment_term('_Test Payment Term 2 for Purchase Invoice')
if not frappe.db.exists('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice'):
    frappe.get_doc({'doctype': 'Payment Terms Template', 'template_name': '_Test Payment Terms Template For Purchase Invoice', 'allocate_payment_based_on_payment_terms': 1, 'terms': [{'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 1 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 0}, {'doctype': 'Payment Terms Template Detail', 'payment_term': '_Test Payment Term 2 for Purchase Invoice', 'invoice_portion': 50.0, 'credit_days_based_on': 'Day(s) after invoice date', 'credit_days': 30}]}).insert()
template = frappe.db.get_value('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice')
old_template_in_supplier = frappe.db.get_value('Supplier', '_Test Supplier', 'payment_terms')
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', template)
pr = make_purchase_receipt(do_not_save=True)
self.assertRaises(frappe.ValidationError, make_purchase_invoice, pr.name)
pr.submit()
pi = make_purchase_invoice(pr.name)
self.assertEqual(pi.doctype, 'Purchase Invoice')
self.assertEqual(len(pi.get('items')), len(pr.get('items')))
pi.get('items')[0].rate = 200
self.assertRaises(frappe.ValidationError, frappe.get_doc(pi).submit)
self.assertEqual(pi.payment_terms_template, template)
self.assertEqual(pi.payment_schedule[0].payment_amount, flt(pi.grand_total) / 2)
self.assertEqual(pi.payment_schedule[0].invoice_portion, 50)
self.assertEqual(pi.payment_schedule[1].payment_amount, flt(pi.grand_total) / 2)
self.assertEqual(pi.payment_schedule[1].invoice_portion, 50)
pi.delete()
pr.cancel()
frappe.db.set_value('Supplier', '_Test Supplier', 'payment_terms', old_template_in_supplier)
frappe.get_doc('Payment Terms Template', '_Test Payment Terms Template For Purchase Invoice').delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:93*

### test_purchase_receipt_no_gl_entry

**Category**: workflow  
**Description**: Workflow: test purchase receipt no gl entry  
**Expected**: self.assertFalse(get_gl_entries('Purchase Receipt', pr.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

from erpnext.stock.doctype.stock_entry.test_stock_entry import make_stock_entry
existing_bin_qty, existing_bin_stock_value = frappe.db.get_value('Bin', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC'}, ['actual_qty', 'stock_value'])
if existing_bin_qty < 0:
    make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=abs(existing_bin_qty))
existing_bin_qty, existing_bin_stock_value = frappe.db.get_value('Bin', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC'}, ['actual_qty', 'stock_value'])
pr = make_purchase_receipt()
stock_value_difference = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC'}, 'stock_value_difference')
self.assertEqual(stock_value_difference, 250)
current_bin_stock_value = frappe.db.get_value('Bin', {'item_code': '_Test Item', 'warehouse': '_Test Warehouse - _TC'}, 'stock_value')
self.assertEqual(current_bin_stock_value, existing_bin_stock_value + 250)
self.assertFalse(get_gl_entries('Purchase Receipt', pr.name))
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:158*

### test_batched_serial_no_purchase

**Category**: workflow  
**Description**: Workflow: test batched serial no purchase  
**Expected**: self.assertTrue(frappe.db.get_value('Batch', {'item': item.name, 'reference_name': pr.name}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

item = frappe.db.exists('Item', {'item_name': 'Batched Serialized Item'})
if not item:
    item = create_item('Batched Serialized Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.has_serial_no = 1
    item.batch_number_series = 'BS-BATCH-.##'
    item.serial_no_series = 'BS-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched Serialized Item'})
pr = make_purchase_receipt(item_code=item.name, qty=5, rate=500)
self.assertTrue(frappe.db.get_value('Batch', {'item': item.name, 'reference_name': pr.name}))
pr.load_from_db()
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:202*

### test_duplicate_serial_nos

**Category**: workflow  
**Description**: Workflow: test duplicate serial nos  
**Expected**: self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
item = frappe.db.exists('Item', {'item_name': 'Test Serialized Item 123'})
if not item:
    item = create_item('Test Serialized Item 123')
    item.has_serial_no = 1
    item.serial_no_series = 'TSI123-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Test Serialized Item 123'})
pr = make_purchase_receipt(item_code=item.name, qty=2, rate=500)
pr.load_from_db()
bundle_id = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': pr.name, 'item_code': item.name}, 'serial_and_batch_bundle')
serial_nos = get_serial_nos_from_bundle(bundle_id)
self.assertEqual(get_serial_nos_from_bundle(pr.items[0].serial_and_batch_bundle), serial_nos)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': today(), 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoDuplicateError, bundle_id.make_serial_and_batch_bundle)
dn = create_delivery_note(item_code=item.name, qty=2, rate=1500, serial_no=serial_nos)
dn.load_from_db()
self.assertEqual(get_serial_nos_from_bundle(dn.items[0].serial_and_batch_bundle), serial_nos)
posting_date = add_days(today(), -3)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse - _TC', 'company': '_Test Company', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': item.item_code, 'warehouse': '_Test Warehouse 2 - _TC1', 'company': '_Test Company 1', 'qty': 2, 'rate': 500, 'voucher_type': 'Purchase Receipt', 'serial_nos': serial_nos, 'posting_date': posting_date, 'posting_time': nowtime(), 'do_not_save': True}))
self.assertRaises(SerialNoExistsInFutureTransactionError, bundle_id.make_serial_and_batch_bundle)
make_purchase_receipt(item_code=item.name, qty=2, rate=500, serial_no=serial_nos)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:222*

### test_purchase_receipt_gl_entry

**Category**: workflow  
**Description**: Workflow: test purchase receipt gl entry  
**Expected**: self.assertTrue(get_gl_entries('Purchase Receipt', pr.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', get_multiple_items=True, get_taxes_and_charges=True)
self.assertEqual(cint(erpnext.is_perpetual_inventory_enabled(pr.company)), 1)
gl_entries = get_gl_entries('Purchase Receipt', pr.name)
self.assertTrue(gl_entries)
stock_in_hand_account = get_inventory_account(pr.company, pr.items[0].warehouse)
fixed_asset_account = get_inventory_account(pr.company, pr.items[1].warehouse)
if stock_in_hand_account == fixed_asset_account:
    expected_values = {stock_in_hand_account: [750.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 100.0], '_Test Account Customs Duty - TCP1': [0.0, 150.0]}
else:
    expected_values = {stock_in_hand_account: [375.0, 0.0], fixed_asset_account: [375.0, 0.0], 'Stock Received But Not Billed - TCP1': [0.0, 500.0], '_Test Account Shipping Charges - TCP1': [0.0, 250.0]}
for gle in gl_entries:
    self.assertEqual(expected_values[gle.account][0], gle.debit)
    self.assertEqual(expected_values[gle.account][1], gle.credit)
pr.cancel()
self.assertTrue(get_gl_entries('Purchase Receipt', pr.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:319*

### test_rejected_warehouse_filter

**Category**: workflow  
**Description**: Workflow: test rejected warehouse filter  
**Expected**: self.assertRaises(frappe.ValidationError, pr.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

pr = frappe.copy_doc(self.globalTestRecords['Purchase Receipt'][0])
pr.get('items')[0].item_code = '_Test Serialized Item With Series'
pr.get('items')[0].qty = 3
pr.get('items')[0].rejected_qty = 2
pr.get('items')[0].received_qty = 5
pr.get('items')[0].rejected_warehouse = pr.get('items')[0].warehouse
self.assertRaises(frappe.ValidationError, pr.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:369*

### test_rejected_serial_no

**Category**: workflow  
**Description**: Workflow: test rejected serial no  
**Expected**: self.assertEqual(len(rejected_serial_nos), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

pr = frappe.copy_doc(self.globalTestRecords['Purchase Receipt'][0])
pr.get('items')[0].item_code = '_Test Serialized Item With Series'
pr.get('items')[0].qty = 3
pr.get('items')[0].rejected_qty = 2
pr.get('items')[0].received_qty = 5
pr.get('items')[0].rejected_warehouse = '_Test Rejected Warehouse - _TC'
pr.insert()
pr.submit()
pr.load_from_db()
accepted_serial_nos = get_serial_nos_from_bundle(pr.get('items')[0].serial_and_batch_bundle)
self.assertEqual(len(accepted_serial_nos), 3)
for serial_no in accepted_serial_nos:
    self.assertEqual(frappe.db.get_value('Serial No', serial_no, 'warehouse'), pr.get('items')[0].warehouse)
rejected_serial_nos = get_serial_nos_from_bundle(pr.get('items')[0].rejected_serial_and_batch_bundle)
self.assertEqual(len(rejected_serial_nos), 2)
for serial_no in rejected_serial_nos:
    self.assertEqual(frappe.db.get_value('Serial No', serial_no, 'warehouse'), pr.get('items')[0].rejected_warehouse)
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:378*

### test_purchase_return_full

**Category**: workflow  
**Description**: Workflow: test purchase return full  
**Expected**: self.assertEqual(pr.status, 'Return Issued')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1')
return_pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', is_return=1, return_against=pr.name, qty=-5, do_not_submit=1)
return_pr.items[0].purchase_receipt_item = pr.items[0].name
return_pr.submit()
returned = frappe.get_doc('Purchase Receipt', return_pr.name)
returned.update_prevdoc_status()
pr.load_from_db()
self.assertEqual(pr.items[0].returned_qty, 5)
self.assertEqual(pr.per_returned, 100)
self.assertEqual(pr.status, 'Return Issued')
return_pr.cancel()
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:494*

### test_purchase_return_for_rejected_qty

**Category**: workflow  
**Description**: Workflow: test purchase return for rejected qty  
**Expected**: self.assertEqual(actual_qty, -2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_single_value('Buying Settings', 'allow_multiple_items', 1)

from erpnext.stock.doctype.warehouse.test_warehouse import get_warehouse
rejected_warehouse = '_Test Rejected Warehouse - TCP1'
if not frappe.db.exists('Warehouse', rejected_warehouse):
    get_warehouse(company='_Test Company with perpetual inventory', abbr=' - TCP1', warehouse_name='_Test Rejected Warehouse').name
pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', qty=2, rejected_qty=2, rejected_warehouse=rejected_warehouse)
return_pr = make_purchase_receipt(company='_Test Company with perpetual inventory', warehouse='Stores - TCP1', supplier_warehouse='Work In Progress - TCP1', is_return=1, return_against=pr.name, qty=-2, rejected_qty=-2, rejected_warehouse=rejected_warehouse)
actual_qty = frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Purchase Receipt', 'voucher_no': return_pr.name, 'warehouse': return_pr.items[0].rejected_warehouse}, 'actual_qty')
self.assertEqual(actual_qty, -2)
return_pr.cancel()
pr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/purchase_receipt/test_purchase_receipt.py:526*

### test_concurrent_inserts

**Category**: workflow  
**Description**: Workflow: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Ensure no duplicates are possible in case of concurrent inserts'
item_code = '_TestConcurrentBin'
make_item(item_code)
warehouse = '_Test Warehouse - _TC'
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
bin1.insert()
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
with self.assertRaises(frappe.UniqueValidationError):
    bin2.insert()
bin = _create_bin(item_code, warehouse)
self.assertEqual(bin.item_code, item_code)
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:12*

### test_concurrent_inserts

**Category**: workflow  
**Description**: Workflow: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Ensure no duplicates are possible in case of concurrent inserts'
item_code = '_TestConcurrentBin'
make_item(item_code)
warehouse = '_Test Warehouse - _TC'
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
bin1.insert()
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
with self.assertRaises(frappe.UniqueValidationError):
    bin2.insert()
bin = _create_bin(item_code, warehouse)
self.assertEqual(bin.item_code, item_code)
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:12*

### test_putaway_rules_with_same_priority

**Category**: workflow  
**Description**: Workflow: Test if rule with more free space is applied,
among two rules with same priority and capacity.  
**Expected**: self.assertEqual(pr.items[1].warehouse, self.warehouse_1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test if rule with more free space is applied,\n\t\tamong two rules with same priority and capacity.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=500, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500, uom='Kg')
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=100, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=700, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 500)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 200)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:71*

### test_putaway_rules_multi_uom

**Category**: workflow  
**Description**: Workflow: Test rules applied on uom other than stock uom.  
**Expected**: self.assertEqual(pr.items[1].warehouse, self.warehouse_1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test rules applied on uom other than stock uom.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=3, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 3000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=4, uom='Bag')
self.assertEqual(rule_2.stock_capacity, 4000)
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=1000, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=6, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 4)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 2)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:111*

### test_putaway_rules_multi_uom_whole_uom

**Category**: workflow  
**Description**: Workflow: Test if whole UOMs are handled.  
**Expected**: self.assertUnchangedItemsOnResave(pr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test if whole UOMs are handled.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
frappe.db.set_value('UOM', 'Bag', 'must_be_whole_number', 1)
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=1, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 1000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500)
self.assertEqual(rule_2.stock_capacity, 500)
pr = make_purchase_receipt(item_code='_Rice', qty=2, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 1)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertUnchangedItemsOnResave(pr)
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:146*

### test_validate_over_receipt_in_warehouse

**Category**: workflow  
**Description**: Workflow: Test if overreceipt is blocked in the presence of putaway rules.  
**Expected**: self.assertRaises(frappe.ValidationError, pr.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test if overreceipt is blocked in the presence of putaway rules.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
pr = make_purchase_receipt(item_code='_Rice', qty=300, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 200)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertEqual(pr.items[0].putaway_rule, rule_1.name)
pr.items[0].qty = 300
pr.items[0].stock_qty = 300
pr.apply_putaway_rule = 0
self.assertRaises(frappe.ValidationError, pr.save)
pr.delete()
rule_1.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:220*

### test_putaway_rule_on_stock_entry_material_transfer

**Category**: workflow  
**Description**: Workflow: Test if source warehouse is considered while applying rules.  
**Expected**: self.assertUnchangedItemsOnResave(stock_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test if source warehouse is considered while applying rules.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=100, uom='Kg', priority=2)
stock_entry = make_stock_entry(item_code='_Rice', source=self.warehouse_1, qty=200, target='_Test Warehouse - _TC', purpose='Material Transfer', apply_putaway_rule=1, do_not_submit=1)
stock_entry_item = stock_entry.get('items')[0]
self.assertEqual(stock_entry_item.t_warehouse, self.warehouse_2)
self.assertEqual(stock_entry_item.qty, 100)
self.assertEqual(stock_entry_item.putaway_rule, rule_2.name)
self.assertUnchangedItemsOnResave(stock_entry)
stock_entry.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:239*

### test_putaway_rule_on_stock_entry_material_receipt

**Category**: workflow  
**Description**: Workflow: Test if rules are applied in Stock Entry of type Receipt.  
**Expected**: self.assertUnchangedItemsOnResave(stock_entry)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
if not frappe.db.exists('Item', '_Rice'):
    make_item('_Rice', {'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'stock_uom': 'Kg'})
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 1'}):
    create_warehouse('Rack 1')
if not frappe.db.exists('Warehouse', {'warehouse_name': 'Rack 2'}):
    create_warehouse('Rack 2')
self.warehouse_1 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 1'})
self.warehouse_2 = frappe.db.get_value('Warehouse', {'warehouse_name': 'Rack 2'})
if not frappe.db.exists('UOM', 'Bag'):
    new_uom = frappe.new_doc('UOM')
    new_uom.uom_name = 'Bag'
    new_uom.save()

'Test if rules are applied in Stock Entry of type Receipt.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=100, uom='Kg')
stock_entry = make_stock_entry(item_code='_Rice', qty=100, target='_Test Warehouse - _TC', purpose='Material Receipt', apply_putaway_rule=1, do_not_submit=1)
stock_entry_item = stock_entry.get('items')[0]
self.assertEqual(stock_entry_item.t_warehouse, self.warehouse_1)
self.assertEqual(stock_entry_item.qty, 100)
self.assertEqual(stock_entry_item.putaway_rule, rule_1.name)
self.assertUnchangedItemsOnResave(stock_entry)
stock_entry.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:417*

### test_putaway_rules_with_same_priority

**Category**: workflow  
**Description**: Workflow: Test if rule with more free space is applied,
among two rules with same priority and capacity.  
**Expected**: self.assertEqual(pr.items[1].warehouse, self.warehouse_1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test if rule with more free space is applied,\n\t\tamong two rules with same priority and capacity.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=500, uom='Kg')
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500, uom='Kg')
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=100, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=700, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 500)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 200)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:71*

### test_putaway_rules_multi_uom

**Category**: workflow  
**Description**: Workflow: Test rules applied on uom other than stock uom.  
**Expected**: self.assertEqual(pr.items[1].warehouse, self.warehouse_1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test rules applied on uom other than stock uom.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=3, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 3000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=4, uom='Bag')
self.assertEqual(rule_2.stock_capacity, 4000)
stock_receipt = make_stock_entry(item_code='_Rice', target=self.warehouse_1, qty=1000, basic_rate=50)
pr = make_purchase_receipt(item_code='_Rice', qty=6, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 2)
self.assertEqual(pr.items[0].qty, 4)
self.assertEqual(pr.items[0].warehouse, self.warehouse_2)
self.assertEqual(pr.items[1].qty, 2)
self.assertEqual(pr.items[1].warehouse, self.warehouse_1)
stock_receipt.cancel()
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:111*

### test_putaway_rules_multi_uom_whole_uom

**Category**: workflow  
**Description**: Workflow: Test if whole UOMs are handled.  
**Expected**: self.assertUnchangedItemsOnResave(pr)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test if whole UOMs are handled.'
item = frappe.get_doc('Item', '_Rice')
if not frappe.db.get_value('UOM Conversion Detail', {'parent': '_Rice', 'uom': 'Bag'}):
    item.append('uoms', {'uom': 'Bag', 'conversion_factor': 1000})
    item.save()
frappe.db.set_value('UOM', 'Bag', 'must_be_whole_number', 1)
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=1, uom='Bag')
self.assertEqual(rule_1.stock_capacity, 1000)
rule_2 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_2, capacity=500)
self.assertEqual(rule_2.stock_capacity, 500)
pr = make_purchase_receipt(item_code='_Rice', qty=2, uom='Bag', stock_uom='Kg', conversion_factor=1000, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 1)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertUnchangedItemsOnResave(pr)
pr.delete()
rule_1.delete()
rule_2.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:146*

### test_validate_over_receipt_in_warehouse

**Category**: workflow  
**Description**: Workflow: Test if overreceipt is blocked in the presence of putaway rules.  
**Expected**: self.assertRaises(frappe.ValidationError, pr.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test if overreceipt is blocked in the presence of putaway rules.'
rule_1 = create_putaway_rule(item_code='_Rice', warehouse=self.warehouse_1, capacity=200, uom='Kg')
pr = make_purchase_receipt(item_code='_Rice', qty=300, apply_putaway_rule=1, do_not_submit=1)
self.assertEqual(len(pr.items), 1)
self.assertEqual(pr.items[0].qty, 200)
self.assertEqual(pr.items[0].warehouse, self.warehouse_1)
self.assertEqual(pr.items[0].putaway_rule, rule_1.name)
pr.items[0].qty = 300
pr.items[0].stock_qty = 300
pr.apply_putaway_rule = 0
self.assertRaises(frappe.ValidationError, pr.save)
pr.delete()
rule_1.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/putaway_rule/test_putaway_rule.py:220*

### test_stock_reco_for_serialized_item

**Category**: workflow  
**Description**: Workflow: test stock reco for serialized item  
**Expected**: self.assertEqual(valuation_rate, 300)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
to_delete_records = []
serial_item_code = 'Stock-Reco-Serial-Item-1'
serial_warehouse = '_Test Warehouse for Stock Reco1 - _TC'
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=200)
serial_nos = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle).get_serial_nos()
self.assertEqual(len(serial_nos), 5)
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 200)
to_delete_records.append(sr.name)
sr = create_stock_reconciliation(item_code=serial_item_code, warehouse=serial_warehouse, qty=5, rate=300, serial_no=serial_nos)
sn_doc = frappe.get_doc('Serial and Batch Bundle', sr.items[0].serial_and_batch_bundle)
self.assertEqual(len(sn_doc.get_serial_nos()), 5)
args = {'item_code': serial_item_code, 'warehouse': serial_warehouse, 'qty': -5, 'posting_date': add_days(sr.posting_date, 1), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 300)
to_delete_records.append(sr.name)
to_delete_records.reverse()
for d in to_delete_records:
    stock_doc = frappe.get_doc('Stock Reconciliation', d)
    stock_doc.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:160*

### test_stock_reco_for_batch_item

**Category**: workflow  
**Description**: Workflow: test stock reco for batch item  
**Expected**: self.assertEqual(stock_value, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
to_delete_records = []
item_code = 'Stock-Reco-batch-Item-123'
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
self.make_item(item_code, frappe._dict({'is_stock_item': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'batch_number_series': 'SRBI123-.#####'}))
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=5, rate=200, do_not_save=1)
sr.save()
sr.submit()
sr.load_from_db()
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
self.assertTrue(batch_no)
to_delete_records.append(sr.name)
sr1 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=300, batch_no=batch_no)
args = {'item_code': item_code, 'warehouse': warehouse, 'posting_date': nowdate(), 'posting_time': nowtime(), 'serial_and_batch_bundle': sr1.items[0].serial_and_batch_bundle}
valuation_rate = get_incoming_rate(args)
self.assertEqual(valuation_rate, 300)
to_delete_records.append(sr1.name)
sr2 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=0, rate=0, batch_no=batch_no)
stock_value = get_stock_value_on(warehouse, nowdate(), item_code)
self.assertEqual(stock_value, 0)
to_delete_records.append(sr2.name)
to_delete_records.reverse()
for d in to_delete_records:
    stock_doc = frappe.get_doc('Stock Reconciliation', d)
    stock_doc.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:217*

### test_stock_reco_for_serial_and_batch_item

**Category**: workflow  
**Description**: Workflow: test stock reco for serial and batch item  
**Expected**: self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'warehouse'), None)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = create_item('_TestBatchSerialItemReco')
item.has_batch_no = 1
item.create_new_batch = 1
item.has_serial_no = 1
item.batch_number_series = 'TBS-BATCH-.##'
item.serial_no_series = 'TBS-.####'
item.save()
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
sr = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
batch_no = get_batch_from_bundle(sr.items[0].serial_and_batch_bundle)
serial_nos = get_serial_nos_from_bundle(sr.items[0].serial_and_batch_bundle)
self.assertEqual(len(serial_nos), 1)
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'batch_no'), batch_no)
sr.cancel()
self.assertEqual(frappe.db.get_value('Serial No', serial_nos[0], 'warehouse'), None)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:275*

### test_stock_reco_for_serial_and_batch_item_with_future_dependent_entry

**Category**: workflow  
**Description**: Workflow: Behaviour: 1) Create Stock Reconciliation, which will be the origin document
of a new batch having a serial no
2) Create a Stock Entry that adds a serial no to the same batch following this
Stock Reconciliation
3) Cancel Stock Entry
Expected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases  
**Expected**: self.assertFalse(frappe.db.get_value('Serial No', serial_no_2, 'warehouse'))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tBehaviour: 1) Create Stock Reconciliation, which will be the origin document\n\t\tof a new batch having a serial no\n\t\t2) Create a Stock Entry that adds a serial no to the same batch following this\n\t\tStock Reconciliation\n\t\t3) Cancel Stock Entry\n\t\tExpected Result: 3) Serial No only in the Stock Entry is Inactive and Batch qty decreases\n\t\t'
from erpnext.stock.doctype.batch.batch import get_batch_qty
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry
item = create_item('_TestBatchSerialItemDependentReco')
item.has_batch_no = 1
item.create_new_batch = 1
item.has_serial_no = 1
item.batch_number_series = 'TBSD-BATCH-.##'
item.serial_no_series = 'TBSD-.####'
item.save()
warehouse = '_Test Warehouse for Stock Reco2 - _TC'
stock_reco = create_stock_reconciliation(item_code=item.item_code, warehouse=warehouse, qty=1, rate=100)
batch_no = get_batch_from_bundle(stock_reco.items[0].serial_and_batch_bundle)
reco_serial_no = get_serial_nos_from_bundle(stock_reco.items[0].serial_and_batch_bundle)[0]
stock_entry = make_stock_entry(item_code=item.item_code, target=warehouse, qty=1, basic_rate=100, batch_no=batch_no)
serial_no_2 = get_serial_nos_from_bundle(stock_entry.items[0].serial_and_batch_bundle)[0]
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
self.assertEqual(batch_qty, 2)
stock_entry.cancel()
batch_qty = get_batch_qty(batch_no, warehouse, item.item_code)
self.assertEqual(batch_qty, 1)
self.assertEqual(frappe.db.get_value('Serial No', reco_serial_no, 'batch_no'), batch_no)
self.assertTrue(frappe.db.get_value('Serial No', reco_serial_no, 'warehouse'))
self.assertFalse(frappe.db.get_value('Serial No', serial_no_2, 'warehouse'))
stock_reco.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:298*

### test_backdated_stock_reco_qty_reposting

**Category**: workflow  
**Description**: Workflow: Test if a backdated stock reco recalculates future qty until next reco.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR5     | PR    |   10  |  10   (posting date: today-4) [backdated]
SR5             | Reco  |       0       |       8       (posting date: today-4) [backdated]
PR1             | PR    |       10      |       18      (posting date: today-3)
PR2             | PR    |       1       |       19      (posting date: today-2)
SR4             | Reco  |       0       |       6       (posting date: today-1) [backdated]
PR3             | PR    |       1       |       7       (posting date: today) # can't post future PR  
**Expected**: assertBalance(sr4, 6)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"\n\t\tTest if a backdated stock reco recalculates future qty until next reco.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR5     | PR    |   10  |  10   (posting date: today-4) [backdated]\n\t\tSR5\t\t| Reco\t|\t0\t|\t8\t(posting date: today-4) [backdated]\n\t\tPR1\t\t| PR\t|\t10\t|\t18\t(posting date: today-3)\n\t\tPR2\t\t| PR\t|\t1\t|\t19\t(posting date: today-2)\n\t\tSR4\t\t| Reco\t|\t0\t|\t6\t(posting date: today-1) [backdated]\n\t\tPR3\t\t| PR\t|\t1\t|\t7\t(posting date: today) # can't post future PR\n\t\t"
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
frappe.flags.dont_execute_stock_reposts = True

def assertBalance(doc, qty_after_transaction):
    sle_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': doc.name, 'is_cancelled': 0}, 'qty_after_transaction')
    self.assertEqual(sle_balance, qty_after_transaction)
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -3))
pr2 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -2))
pr3 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=nowdate())
assertBalance(pr1, 10)
assertBalance(pr3, 12)
sr4 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=6, rate=100, posting_date=add_days(nowdate(), -1))
assertBalance(pr3, 7)
sr5 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=8, rate=100, posting_date=add_days(nowdate(), -4))
assertBalance(pr1, 18)
assertBalance(pr2, 19)
assertBalance(sr4, 6)
pr5 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -5))
assertBalance(pr5, 10)
assertBalance(sr4, 6)
assertBalance(sr5, 8)
sr5.cancel()
assertBalance(pr1, 10)
assertBalance(pr2, 11)
assertBalance(sr4, 6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:361*

### test_backdated_stock_reco_future_negative_stock

**Category**: workflow  
**Description**: Workflow: Test if a backdated stock reco causes future negative stock and is blocked.
-------------------------------------------
Var             | Doc   |       Qty     | Balance
-------------------------------------------
PR1             | PR    |       10      |       10              (posting date: today-2)
SR3             | Reco  |       0       |       1               (posting date: today-1) [backdated & blocked]
DN2             | DN    |       -2      |       8(-1)   (posting date: today)  
**Expected**: self.assertRaises(NegativeStockError, sr3.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest if a backdated stock reco causes future negative stock and is blocked.\n\t\t-------------------------------------------\n\t\tVar\t\t| Doc\t|\tQty\t| Balance\n\t\t-------------------------------------------\n\t\tPR1\t\t| PR\t|\t10\t|\t10\t\t(posting date: today-2)\n\t\tSR3\t\t| Reco\t|\t0\t|\t1\t\t(posting date: today-1) [backdated & blocked]\n\t\tDN2\t\t| DN\t|\t-2\t|\t8(-1)\t(posting date: today)\n\t\t'
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.stock_ledger import NegativeStockError
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
pr1 = make_purchase_receipt(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), -2))
dn2 = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=2, rate=120, posting_date=nowdate())
pr1_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': pr1.name, 'is_cancelled': 0}, 'qty_after_transaction')
dn2_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn2.name, 'is_cancelled': 0}, 'qty_after_transaction')
self.assertEqual(pr1_balance, 10)
self.assertEqual(dn2_balance, 8)
sr3 = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=1, rate=100, posting_date=add_days(nowdate(), -1), do_not_submit=True)
self.assertRaises(NegativeStockError, sr3.submit)
sr3.cancel()
dn2.cancel()
pr1.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:427*

### test_backdated_stock_reco_cancellation_future_negative_stock

**Category**: workflow  
**Description**: Workflow: Test if a backdated stock reco cancellation that causes future negative stock is blocked.
-------------------------------------------
Var | Doc  | Qty | Balance
-------------------------------------------
SR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)
DN  | DN   | 100 |   0     (posting date: today)  
**Expected**: self.assertFalse(repost_exists, msg='Negative stock validation not working on reco cancellation')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"\n\t\tTest if a backdated stock reco cancellation that causes future negative stock is blocked.\n\t\t-------------------------------------------\n\t\tVar | Doc  | Qty | Balance\n\t\t-------------------------------------------\n\t\tSR  | Reco | 100 | 100     (posting date: today-1) (shouldn't be cancelled after DN)\n\t\tDN  | DN   | 100 |   0     (posting date: today)\n\t\t"
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
from erpnext.stock.stock_ledger import NegativeStockError
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
sr = create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=100, rate=100, posting_date=add_days(nowdate(), -1))
dn = create_delivery_note(item_code=item_code, warehouse=warehouse, qty=100, rate=120, posting_date=nowdate())
dn_balance = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': dn.name, 'is_cancelled': 0}, 'qty_after_transaction')
self.assertEqual(dn_balance, 0)
self.assertRaises(NegativeStockError, sr.cancel)
repost_exists = bool(frappe.db.exists('Repost Item Valuation', {'voucher_no': sr.name, 'status': 'Queued'}))
self.assertFalse(repost_exists, msg='Negative stock validation not working on reco cancellation')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:476*

### test_intermediate_sr_bin_update

**Category**: workflow  
**Description**: Workflow: Bin should show correct qty even for backdated entries.

-------------------------------------------
| creation | Var | Doc  | Qty | balance qty
-------------------------------------------
|  1       | SR  | Reco | 10  | 10     (posting date: today+10)
|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)
|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)  
**Expected**: self.assertEqual(old_bin_qty + 1, new_bin_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Bin should show correct qty even for backdated entries.\n\n\t\t-------------------------------------------\n\t\t| creation | Var | Doc  | Qty | balance qty\n\t\t-------------------------------------------\n\t\t|  1       | SR  | Reco | 10  | 10     (posting date: today+10)\n\t\t|  3       | SR2 | Reco | 11  | 11     (posting date: today+11)\n\t\t|  2       | DN  | DN   | 5   | 6 <-- assert in BIN  (posting date: today+12)\n\t\t'
from erpnext.stock.doctype.delivery_note.test_delivery_note import create_delivery_note
frappe.db.rollback()
frappe.flags.dont_execute_stock_reposts = True
item_code = self.make_item().name
warehouse = '_Test Warehouse - _TC'
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=10, rate=100, posting_date=add_days(nowdate(), 10))
create_delivery_note(item_code=item_code, warehouse=warehouse, qty=5, rate=120, posting_date=add_days(nowdate(), 12))
old_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
create_stock_reconciliation(item_code=item_code, warehouse=warehouse, qty=11, rate=100, posting_date=add_days(nowdate(), 11))
new_bin_qty = frappe.db.get_value('Bin', {'item_code': item_code, 'warehouse': warehouse}, 'actual_qty')
self.assertEqual(old_bin_qty + 1, new_bin_qty)
frappe.db.rollback()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:516*

### test_serial_no_cancellation

**Category**: workflow  
**Description**: Workflow: test serial no cancellation  
**Expected**: self.assertEqual(len(active_sr_no), 10)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_stock_entry
item = create_item('Stock-Reco-Serial-Item-9', is_stock_item=1)
if not item.has_serial_no:
    item.has_serial_no = 1
    item.serial_no_series = 'PSRS9.####'
    item.save()
item_code = item.name
warehouse = '_Test Warehouse - _TC'
se1 = make_stock_entry(item_code=item_code, target=warehouse, qty=10, basic_rate=700)
serial_nos = get_serial_nos_from_bundle(se1.items[0].serial_and_batch_bundle)
serial_nos.pop()
new_serial_nos = serial_nos
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=new_serial_nos, qty=9)
sr.cancel()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 10)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:579*

### test_serial_no_creation_and_inactivation

**Category**: workflow  
**Description**: Workflow: test serial no creation and inactivation  
**Expected**: self.assertEqual(len(active_sr_no), 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = create_item('_TestItemCreatedWithStockReco', is_stock_item=1)
if not item.has_serial_no:
    item.has_serial_no = 1
    item.save()
item_code = item.name
warehouse = '_Test Warehouse - _TC'
if not frappe.db.exists('Serial No', 'SR-CREATED-SR-NO'):
    frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': 'SR-CREATED-SR-NO'}).insert()
sr = create_stock_reconciliation(item_code=item.name, warehouse=warehouse, serial_no=['SR-CREATED-SR-NO'], qty=1, do_not_submit=True, rate=100)
sr.save()
self.assertEqual(cstr(sr.items[0].current_serial_no), '')
sr.submit()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 1)
sr.cancel()
active_sr_no = frappe.get_all('Serial No', filters={'item_code': item_code, 'warehouse': warehouse, 'status': 'Active'})
self.assertEqual(len(active_sr_no), 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_reconciliation/test_stock_reconciliation.py:608*

### test_stock_entry_qty

**Category**: workflow  
**Description**: Workflow: test stock entry qty  
**Expected**: self.assertEqual(se.items[0].qty, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_Test Item 2'
warehouse = '_Test Warehouse - _TC'
se = make_stock_entry(item_code=item_code, target=warehouse, qty=0, do_not_save=True)
with self.assertRaises(InvalidQtyError):
    se.save()
se.items[0].qty = 1
se.save()
self.assertEqual(se.items[0].qty, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:63*

### test_fifo

**Category**: workflow  
**Description**: Workflow: test fifo  
**Expected**: self.assertEqual([[1, 20], [1, 30]], frappe.safe_eval(sle.stock_queue))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
item_code = '_Test Item 2'
warehouse = '_Test Warehouse - _TC'
create_stock_reconciliation(item_code='_Test Item 2', warehouse='_Test Warehouse - _TC', qty=0, rate=100)
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=10)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, source=warehouse, qty=2, basic_rate=10)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[-1, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, source=warehouse, qty=1)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[-2, 10]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, target=warehouse, qty=3, basic_rate=20)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 20]], frappe.safe_eval(sle.stock_queue))
make_stock_entry(item_code=item_code, target=warehouse, qty=1, basic_rate=30)
sle = get_sle(item_code=item_code, warehouse=warehouse)[0]
self.assertEqual([[1, 20], [1, 30]], frappe.safe_eval(sle.stock_queue))
frappe.db.set_default('allow_negative_stock', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:75*

### test_add_to_transit_entry

**Category**: workflow  
**Description**: Workflow: test add to transit entry  
**Expected**: self.assertEqual(transit_entry.items[0].name, end_transit_entry.items[0].ste_detail)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.warehouse.test_warehouse import create_warehouse
item_code = '_Test Transit Item'
company = '_Test Company'
create_warehouse('Test From Warehouse')
create_warehouse('Test Transit Warehouse')
create_warehouse('Test To Warehouse')
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, company=company)
make_stock_entry(item_code=item_code, target='Test From Warehouse - _TC', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
transit_entry = make_stock_entry(item_code=item_code, source='Test From Warehouse - _TC', target='Test Transit Warehouse - _TC', add_to_transit=1, stock_entry_type='Material Transfer', purpose='Material Transfer', qty=10, basic_rate=100, expense_account='Stock Adjustment - _TC', cost_center='Main - _TC')
end_transit_entry = make_stock_in_entry(transit_entry.name)
self.assertEqual(end_transit_entry.stock_entry_type, 'Material Transfer')
self.assertEqual(end_transit_entry.purpose, 'Material Transfer')
self.assertEqual(transit_entry.name, end_transit_entry.outgoing_stock_entry)
self.assertEqual(transit_entry.name, end_transit_entry.items[0].against_stock_entry)
self.assertEqual(transit_entry.items[0].name, end_transit_entry.items[0].ste_detail)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:189*

### test_material_issue_gl_entry

**Category**: workflow  
**Description**: Workflow: test material issue gl entry  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', company=company, qty=50, basic_rate=100, expense_account='Stock Adjustment - TCP1')
mi = make_stock_entry(item_code='_Test Item', source='Stores - TCP1', company=company, qty=40, expense_account='Stock Adjustment - TCP1')
self.check_stock_ledger_entries('Stock Entry', mi.name, [['_Test Item', 'Stores - TCP1', -40.0]])
stock_in_hand_account = get_inventory_account(mi.company, 'Stores - TCP1')
stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mi.name}, 'stock_value_difference'))
self.check_gl_entries('Stock Entry', mi.name, sorted([[stock_in_hand_account, 0.0, stock_value_diff], ['Stock Adjustment - TCP1', stock_value_diff, 0.0]]))
mi.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:278*

### test_material_transfer_gl_entry

**Category**: workflow  
**Description**: Workflow: test material transfer gl entry  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
item_code = 'Hand Sanitizer - 001'
create_item(item_code=item_code, is_stock_item=1, is_purchase_item=1, opening_stock=1000, valuation_rate=10, company=company, warehouse='Stores - TCP1')
mtn = make_stock_entry(item_code=item_code, source='Stores - TCP1', target='Finished Goods - TCP1', qty=45, company=company)
self.check_stock_ledger_entries('Stock Entry', mtn.name, [[item_code, 'Stores - TCP1', -45.0], [item_code, 'Finished Goods - TCP1', 45.0]])
source_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].s_warehouse)
target_warehouse_account = get_inventory_account(mtn.company, mtn.get('items')[0].t_warehouse)
if source_warehouse_account == target_warehouse_account:
    self.assertFalse(frappe.db.sql("select * from `tabGL Entry`\n\t\t\t\twhere voucher_type='Stock Entry' and voucher_no=%s", mtn.name, as_dict=1))
else:
    stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': mtn.name, 'warehouse': 'Stores - TCP1'}, 'stock_value_difference'))
    self.check_gl_entries('Stock Entry', mtn.name, sorted([[source_warehouse_account, 0.0, stock_value_diff], [target_warehouse_account, stock_value_diff, 0.0]]))
mtn.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:320*

### test_repack_multiple_fg

**Category**: workflow  
**Description**: Workflow: Test `is_finished_item` for one item repacked into two items.  
**Expected**: self.assertRaises(FinishedGoodError, repack.validate_finished_goods)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test `is_finished_item` for one item repacked into two items.'
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=100, basic_rate=100)
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
repack.posting_date = nowdate()
repack.posting_time = nowtime()
repack.items[0].qty = 100.0
repack.items[0].transfer_qty = 100.0
repack.items[1].qty = 50.0
repack.append('items', {'conversion_factor': 1.0, 'cost_center': '_Test Cost Center - _TC', 'doctype': 'Stock Entry Detail', 'expense_account': 'Stock Adjustment - _TC', 'basic_rate': 150, 'item_code': '_Test Item 2', 'parentfield': 'items', 'qty': 50.0, 'stock_uom': '_Test UOM', 't_warehouse': '_Test Warehouse - _TC', 'transfer_qty': 50.0, 'uom': '_Test UOM'})
repack.set_stock_entry_type()
for row in repack.items:
    if row.t_warehouse:
        row.set_basic_rate_manually = 1
repack.insert()
self.assertEqual(repack.items[1].is_finished_item, 1)
self.assertEqual(repack.items[2].is_finished_item, 1)
repack.items[1].is_finished_item = 0
repack.items[2].is_finished_item = 0
self.assertRaises(FinishedGoodError, repack.validate_finished_goods)
repack.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:385*

### test_repack_no_change_in_valuation

**Category**: workflow  
**Description**: Workflow: test repack no change in valuation  
**Expected**: self.assertFalse(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=50, basic_rate=100)
repack = frappe.copy_doc(self.globalTestRecords['Stock Entry'][3])
repack.posting_date = nowdate()
repack.posting_time = nowtime()
repack.set_stock_entry_type()
repack.insert()
repack.submit()
self.check_stock_ledger_entries('Stock Entry', repack.name, [['_Test Item', '_Test Warehouse - _TC', -50.0], ['_Test Item Home Desktop 100', '_Test Warehouse - _TC', 1]])
gl_entries = frappe.db.sql("select account, debit, credit\n\t\t\tfrom `tabGL Entry` where voucher_type='Stock Entry' and voucher_no=%s\n\t\t\torder by account desc", repack.name, as_dict=1)
self.assertFalse(gl_entries)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:432*

### test_repack_with_additional_costs

**Category**: workflow  
**Description**: Workflow: test repack with additional costs  
**Expected**: self.assertEqual(stock_value_diff, 1200)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = frappe.db.get_value('Warehouse', 'Stores - TCP1', 'company')
make_stock_entry(item_code='_Test Item', target='Stores - TCP1', company=company, qty=50, basic_rate=100, expense_account='Stock Adjustment - TCP1')
repack = make_stock_entry(company=company, purpose='Repack', do_not_save=True)
repack.posting_date = nowdate()
repack.posting_time = nowtime()
default_expense_account = frappe.get_value('Company', company, 'default_expense_account')
items = get_multiple_items()
repack.items = []
for item in items:
    repack.append('items', item)
repack.set('additional_costs', [{'expense_account': default_expense_account, 'description': 'Actual Operating Cost', 'amount': 1000}, {'expense_account': default_expense_account, 'description': 'Additional Operating Cost', 'amount': 200}])
repack.set_stock_entry_type()
repack.insert()
repack.submit()
stock_in_hand_account = get_inventory_account(repack.company, repack.get('items')[1].t_warehouse)
rm_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item'}, 'stock_value_difference'))
fg_stock_value_diff = abs(frappe.db.get_value('Stock Ledger Entry', {'voucher_type': 'Stock Entry', 'voucher_no': repack.name, 'item_code': '_Test Item Home Desktop 100'}, 'stock_value_difference'))
stock_value_diff = flt(fg_stock_value_diff - rm_stock_value_diff, 2)
self.assertEqual(stock_value_diff, 1200)
self.check_gl_entries('Stock Entry', repack.name, sorted([[stock_in_hand_account, 1200, 0.0], ['Cost of Goods Sold - TCP1', 0.0, 1200.0]]))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:463*

### test_serial_no_reqd

**Category**: workflow  
**Description**: Workflow: test serial no reqd  
**Expected**: self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
se = frappe.copy_doc(self.globalTestRecords['Stock Entry'][0])
se.get('items')[0].item_code = '_Test Serialized Item'
se.get('items')[0].qty = 2
se.get('items')[0].transfer_qty = 2
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': se.get('items')[0].item_code, 'warehouse': se.get('items')[0].t_warehouse, 'company': se.company, 'qty': 2, 'voucher_type': 'Stock Entry', 'posting_date': se.posting_date, 'posting_time': se.posting_time, 'do_not_save': True}))
self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:596*

### test_serial_no_qty_less

**Category**: workflow  
**Description**: Workflow: test serial no qty less  
**Expected**: self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
se = frappe.copy_doc(self.globalTestRecords['Stock Entry'][0])
se.get('items')[0].item_code = '_Test Serialized Item'
se.get('items')[0].qty = 2
se.get('items')[0].serial_no = 'ABCD'
se.get('items')[0].transfer_qty = 2
bundle_id = make_serial_batch_bundle(frappe._dict({'item_code': se.get('items')[0].item_code, 'warehouse': se.get('items')[0].t_warehouse, 'company': se.company, 'qty': 2, 'serial_nos': ['ABCD'], 'voucher_type': 'Stock Entry', 'posting_date': se.posting_date, 'posting_time': se.posting_time, 'do_not_save': True}))
self.assertRaises(frappe.ValidationError, bundle_id.make_serial_and_batch_bundle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry/test_stock_entry.py:619*

### test_delivery_trip_status_completed

**Category**: workflow  
**Description**: Workflow: test delivery trip status completed  
**Expected**: self.assertEqual(self.delivery_trip.status, 'Completed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.delivery_trip.submit()
for stop in self.delivery_trip.delivery_stops:
    stop.visited = 1
self.delivery_trip.save()
self.assertEqual(self.delivery_trip.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:94*

### test_delivery_trip_status_completed

**Category**: workflow  
**Description**: Workflow: test delivery trip status completed  
**Expected**: self.assertEqual(self.delivery_trip.status, 'Completed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
self.delivery_trip.submit()
for stop in self.delivery_trip.delivery_stops:
    stop.visited = 1
self.delivery_trip.save()
self.assertEqual(self.delivery_trip.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:94*

### test_pick_list_shows_batch_no_for_batched_item

**Category**: workflow  
**Description**: Workflow: test pick list shows batch no for batched item  
**Expected**: self.assertEqual(pick_list.locations[0].batch_no, oldest_batch_no)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = frappe.db.exists('Item', {'item_name': 'Batched Item'})
if not item:
    item = create_item('Batched Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.batch_number_series = 'B-BATCH-.##'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched Item'})
pr1 = make_purchase_receipt(item_code='Batched Item', qty=1, rate=100.0)
pr1.load_from_db()
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
pr2 = make_purchase_receipt(item_code='Batched Item', qty=2, rate=100.0)
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}]})
pick_list.set_item_locations()
self.assertEqual(pick_list.locations[0].batch_no, oldest_batch_no)
pr1.cancel()
pr2.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:231*

### test_pick_list_for_batched_and_serialised_item

**Category**: workflow  
**Description**: Workflow: test pick list for batched and serialised item  
**Expected**: self.assertEqual(get_serial_nos_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_serial_nos)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item = frappe.db.exists('Item', {'item_name': 'Batched and Serialised Item'})
if not item:
    item = create_item('Batched and Serialised Item')
    item.has_batch_no = 1
    item.create_new_batch = 1
    item.has_serial_no = 1
    item.batch_number_series = 'B-BATCH-.##'
    item.serial_no_series = 'S-.####'
    item.save()
else:
    item = frappe.get_doc('Item', {'item_name': 'Batched and Serialised Item'})
pr1 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
pr1.load_from_db()
oldest_batch_no = get_batch_from_bundle(pr1.items[0].serial_and_batch_bundle)
oldest_serial_nos = get_serial_nos_from_bundle(pr1.items[0].serial_and_batch_bundle)
pr2 = make_purchase_receipt(item_code='Batched and Serialised Item', qty=2, rate=100.0)
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Material Transfer', 'locations': [{'item_code': 'Batched and Serialised Item', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
pick_list.set_item_locations()
pick_list.submit()
pick_list.reload()
self.assertEqual(get_batch_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_batch_no)
self.assertEqual(get_serial_nos_from_bundle(pick_list.locations[0].serial_and_batch_bundle), oldest_serial_nos)
pick_list.cancel()
pr1.cancel()
pr2.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:271*

### test_pick_list_for_items_with_multiple_UOM

**Category**: workflow  
**Description**: Workflow: test pick list for items with multiple UOM  
**Expected**: self.assertEqual(sales_order.items[0].conversion_factor, delivery_note.items[0].conversion_factor)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = make_item(uoms=[{'uom': 'Nos', 'conversion_factor': 1}, {'uom': 'Hand', 'conversion_factor': 5}, {'uom': 'Unit', 'conversion_factor': 0.5}]).name
purchase_receipt = make_purchase_receipt(item_code=item_code, qty=10)
purchase_receipt.submit()
sales_order = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': item_code, 'qty': 1, 'uom': 'Hand', 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}, {'item_code': item_code, 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today(), 'warehouse': '_Test Warehouse - _TC'}]}).insert()
sales_order.submit()
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'customer': '_Test Customer', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'locations': [{'item_code': item_code, 'qty': 2, 'stock_qty': 1, 'uom': 'Unit', 'conversion_factor': 0.5, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[0].name}, {'item_code': item_code, 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order.name, 'sales_order_item': sales_order.items[1].name}]})
pick_list.set_item_locations()
pick_list.submit()
delivery_note = create_delivery_note(pick_list.name)
pick_list.load_from_db()
self.assertEqual(pick_list.locations[0].picked_qty, delivery_note.items[0].qty * delivery_note.items[0].conversion_factor)
self.assertEqual(pick_list.locations[1].qty, delivery_note.items[1].qty)
self.assertEqual(sales_order.items[0].conversion_factor, delivery_note.items[0].conversion_factor)
pick_list.cancel()
sales_order.cancel()
purchase_receipt.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:401*

### test_pick_list_grouping_before_print

**Category**: workflow  
**Description**: Workflow: test pick list grouping before print  
**Expected**: self.assertEqual(len(pl.locations), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
def _compare_dicts(a, b):
    """compare dicts but ignore missing keys in `a`"""
    for key, value in a.items():
        self.assertEqual(b.get(key), value, msg=f"{key} doesn't match")
pl = frappe.get_doc(doctype='Pick List', group_same_items=True, locations=[_dict(item_code='A', warehouse='X', qty=1, picked_qty=2), _dict(item_code='B', warehouse='X', qty=1, picked_qty=2), _dict(item_code='A', warehouse='Y', qty=1, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=1, picked_qty=2)])
pl.before_print()
self.assertEqual(len(pl.locations), 4)
pl = frappe.get_doc(doctype='Pick List', group_same_items=False, locations=[_dict(item_code='A', warehouse='X', qty=5, picked_qty=1), _dict(item_code='B', warehouse='Y', qty=4, picked_qty=2), _dict(item_code='A', warehouse='X', qty=3, picked_qty=2), _dict(item_code='B', warehouse='Y', qty=2, picked_qty=2)])
pl.before_print()
self.assertEqual(len(pl.locations), 4)
pl.group_same_items = True
pl.before_print()
self.assertEqual(len(pl.locations), 2)
expected_items = [_dict(item_code='A', warehouse='X', qty=8, picked_qty=3), _dict(item_code='B', warehouse='Y', qty=6, picked_qty=4)]
for expected_item, created_item in zip(expected_items, pl.locations, strict=False):
    _compare_dicts(expected_item, created_item)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:484*

### test_multiple_dn_creation

**Category**: workflow  
**Description**: Workflow: test multiple dn creation  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
sales_order_1 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer', 'company': '_Test Company', 'items': [{'item_code': '_Test Item', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
sales_order_1.submit()
sales_order_2 = frappe.get_doc({'doctype': 'Sales Order', 'customer': '_Test Customer 1', 'company': '_Test Company', 'items': [{'item_code': '_Test Item 2', 'qty': 1, 'conversion_factor': 1, 'delivery_date': frappe.utils.today()}]}).insert()
sales_order_2.submit()
pick_list = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'items_based_on': 'Sales Order', 'purpose': 'Delivery', 'customer': '_Test Customer', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_1.name, 'sales_order_item': sales_order_1.items[0].name}, {'item_code': '_Test Item 2', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1, 'sales_order': sales_order_2.name, 'sales_order_item': sales_order_2.items[0].name}]})
pick_list.set_item_locations()
pick_list.submit()
create_delivery_note(pick_list.name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list.name, 'customer': '_Test Customer'}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        self.assertEqual(dn_item.item_code, '_Test Item')
        self.assertEqual(dn_item.against_sales_order, sales_order_1.name)
        self.assertEqual(dn_item.against_pick_list, pick_list.name)
        self.assertEqual(dn_item.pick_list_item, pick_list.locations[0].name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list.name, 'customer': '_Test Customer 1'}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        self.assertEqual(dn_item.item_code, '_Test Item 2')
        self.assertEqual(dn_item.against_sales_order, sales_order_2.name)
        self.assertEqual(dn_item.against_pick_list, pick_list.name)
        self.assertEqual(dn_item.pick_list_item, pick_list.locations[1].name)
pick_list_1 = frappe.get_doc({'doctype': 'Pick List', 'company': '_Test Company', 'purpose': 'Delivery', 'locations': [{'item_code': '_Test Item', 'qty': 1, 'stock_qty': 1, 'conversion_factor': 1}, {'item_code': '_Test Item 2', 'qty': 2, 'stock_qty': 2, 'conversion_factor': 1}]})
pick_list_1.set_item_locations()
pick_list_1.submit()
create_delivery_note(pick_list_1.name)
for dn in frappe.get_all('Delivery Note', filters={'against_pick_list': pick_list_1.name}, fields=['name']):
    for dn_item in frappe.get_doc('Delivery Note', dn.name).get('items'):
        if dn_item.item_code == '_Test Item':
            self.assertEqual(dn_item.qty, 1)
        if dn_item.item_code == '_Test Item 2':
            self.assertEqual(dn_item.qty, 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:530*

### test_picklist_reserved_qty_validation

**Category**: workflow  
**Description**: Workflow: test picklist reserved qty validation  
**Expected**: self.assertEqual(picklist_2.locations[0].qty, 5)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.selling.doctype.sales_order.test_sales_order import make_sales_order
warehouse = '_Test Warehouse - _TC'
test_stock_item = '_Test Stock Item'
if not frappe.db.exists('Item', test_stock_item):
    create_item(item_code=test_stock_item, is_stock_item=1)
make_stock_entry(item_code=test_stock_item, to_warehouse=warehouse, qty=15)
sales_order_1 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
picklist_1 = create_pick_list(sales_order_1.name)
picklist_1.submit()
dn = create_delivery_note(picklist_1.name)
dn.items[0].qty = 5
dn.save()
dn.submit()
picklist_1.reload()
self.assertEqual(picklist_1.status, 'Partly Delivered')
sales_order_2 = make_sales_order(item_code=test_stock_item, warehouse=warehouse, qty=10)
picklist_2 = create_pick_list(sales_order_2.name)
self.assertEqual(picklist_2.locations[0].qty, 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:648*

### test_picklist_with_multi_uom

**Category**: workflow  
**Description**: Workflow: test picklist with multi uom  
**Expected**: self.assertEqual(so.per_picked, 50)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'uoms': [dict(uom='Box', conversion_factor=24)]}).name
make_stock_entry(item=item, to_warehouse=warehouse, qty=1000)
so = make_sales_order(item_code=item, qty=10, rate=42, uom='Box')
pl = create_pick_list(so.name)
for loc in pl.locations:
    loc.picked_qty = loc.stock_qty / 2
pl.save()
pl.submit()
so.reload()
self.assertEqual(so.per_picked, 50)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:688*

### test_picklist_for_batch_item

**Category**: workflow  
**Description**: Workflow: test picklist for batch item  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'is_stock_item': 1, 'has_batch_no': 1, 'batch_number_series': 'PICKLT-.######'}).name
for batch_id in ['PICKLT-000001', 'PICKLT-000002']:
    if not frappe.db.exists('Batch', batch_id):
        frappe.get_doc({'doctype': 'Batch', 'batch_id': batch_id, 'item': item}).insert()
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100, batches=frappe._dict({'PICKLT-000001': 30, 'PICKLT-000002': 20}))
so = make_sales_order(item_code=item, qty=25.0, rate=100)
pl = create_pick_list(so.name)
pl.submit()
for loc in pl.locations:
    self.assertEqual(loc.qty, 25.0)
    self.assertTrue(loc.serial_and_batch_bundle)
pl.save()
pl.submit()
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
pl1 = create_pick_list(so1.name)
pl1.submit()
for loc in pl1.locations:
    self.assertEqual(loc.qty, 5.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
    for d in data:
        self.assertTrue(d.batch_no in ['PICKLT-000001', 'PICKLT-000002'])
        if d.batch_no == 'PICKLT-000001':
            self.assertEqual(d.qty, 5.0 * -1)
        elif d.batch_no == 'PICKLT-000002':
            self.assertEqual(d.qty, 5.0 * -1)
pl1.cancel()
pl.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:704*

### test_picklist_for_serial_item

**Category**: workflow  
**Description**: Workflow: test picklist for serial item  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = '_Test Warehouse - _TC'
item = make_item(properties={'is_stock_item': 1, 'has_serial_no': 1, 'serial_no_series': 'SN-PICKLT-.######'}).name
make_stock_entry(item=item, to_warehouse=warehouse, qty=50, basic_rate=100)
so = make_sales_order(item_code=item, qty=25.0, rate=100)
pl = create_pick_list(so.name)
pl.submit()
picked_serial_nos = []
for loc in pl.locations:
    self.assertEqual(loc.qty, 25.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['serial_no'], filters={'parent': loc.serial_and_batch_bundle})
    picked_serial_nos = [d.serial_no for d in data]
    self.assertEqual(len(picked_serial_nos), 25)
so1 = make_sales_order(item_code=item, qty=10.0, rate=100)
pl1 = create_pick_list(so1.name)
pl1.submit()
for loc in pl1.locations:
    self.assertEqual(loc.qty, 10.0)
    self.assertTrue(loc.serial_and_batch_bundle)
    data = frappe.get_all('Serial and Batch Entry', fields=['qty', 'batch_no'], filters={'parent': loc.serial_and_batch_bundle})
    self.assertEqual(len(data), 10)
    for d in data:
        self.assertTrue(d.serial_no not in picked_serial_nos)
pl1.cancel()
pl.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:765*

### test_picklist_with_bundles

**Category**: workflow  
**Description**: Workflow: test picklist with bundles  
**Expected**: self.assertEqual(so.per_delivered, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = '_Test Warehouse - _TC'
quantities = [5, 2]
bundle, components = create_product_bundle(quantities, warehouse=warehouse)
bundle_items = dict(zip(components, quantities, strict=False))
so = make_sales_order(item_code=bundle, qty=3, rate=42)
pl = create_pick_list(so.name)
pl.save()
self.assertEqual(len(pl.locations), 2)
for item in pl.locations:
    self.assertEqual(item.stock_qty, bundle_items[item.item_code] * 3)
pl.submit()
so.reload()
self.assertEqual(so.per_picked, 100)
dn = create_delivery_note(pl.name).submit()
self.assertEqual(dn.items[0].rate, 42)
self.assertEqual(dn.packed_items[0].warehouse, warehouse)
so.reload()
self.assertEqual(so.per_delivered, 100)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/pick_list/test_pick_list.py:812*

### test_cannot_create_direct

**Category**: workflow  
**Description**: Workflow: test cannot create direct  
**Expected**: self.assertTrue(SerialNoCannotCannotChangeError, sr.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.delete_doc_if_exists('Serial No', '_TCSER0001')
sr = frappe.new_doc('Serial No')
sr.item_code = '_Test Serialized Item'
sr.warehouse = '_Test Warehouse - _TC'
sr.serial_no = '_TCSER0001'
sr.purchase_rate = 10
self.assertRaises(SerialNoCannotCreateDirectError, sr.insert)
sr.warehouse = None
sr.insert()
self.assertTrue(sr.name)
sr.warehouse = '_Test Warehouse - _TC'
self.assertTrue(SerialNoCannotCannotChangeError, sr.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:31*

### test_inter_company_transfer

**Category**: workflow  
**Description**: Workflow: test inter company transfer  
**Expected**: self.assertEqual(serial_no.warehouse, wh)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
serial_no = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(serial_no.warehouse, None)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
serial_no.reload()
self.assertEqual(serial_no.warehouse, wh)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:48*

### test_inter_company_transfer_intermediate_cancellation

**Category**: workflow  
**Description**: Workflow: Receive into and Deliver Serial No from one company.
Then Receive into and Deliver from second company.
Try to cancel intermediate receipts/deliveries to test if it is blocked.  
**Expected**: self.assertRaises(frappe.ValidationError, pr.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tReceive into and Deliver Serial No from one company.\n\t\tThen Receive into and Deliver from second company.\n\t\tTry to cancel intermediate receipts/deliveries to test if it is blocked.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
self.assertRaises(frappe.ValidationError, dn.cancel)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
self.assertRaises(frappe.ValidationError, dn.cancel)
self.assertRaises(frappe.ValidationError, pr.cancel)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:73*

### test_inter_company_transfer_fallback_on_cancel

**Category**: workflow  
**Description**: Workflow: Test Serial No state changes on cancellation.
If Delivery cancelled, it should fall back on last Receipt in the same company.
If Receipt is cancelled, it should be Inactive in the same company.  
**Expected**: self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest Serial No state changes on cancellation.\n\t\tIf Delivery cancelled, it should fall back on last Receipt in the same company.\n\t\tIf Receipt is cancelled, it should be Inactive in the same company.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
dn_2 = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn_2.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
pr.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:133*

### test_correct_serial_no_incoming_rate

**Category**: workflow  
**Description**: Workflow: Check correct consumption rate based on serial no record.  
**Expected**: self.assertEqual(value_diff, -113)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Check correct consumption rate based on serial no record.'
item_code = '_Test Serialized Item'
warehouse = '_Test Warehouse - _TC'
serial_nos = ['LOWVALUATION', 'HIGHVALUATION']
for serial_no in serial_nos:
    if not frappe.db.exists('Serial No', serial_no):
        frappe.get_doc({'doctype': 'Serial No', 'item_code': item_code, 'serial_no': serial_no}).insert()
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=42, serial_no=[serial_nos[0]])
make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=1, rate=113, serial_no=[serial_nos[1]])
out = create_delivery_note(item_code=item_code, qty=1, serial_no=[serial_nos[0]], do_not_submit=True)
bundle = out.items[0].serial_and_batch_bundle
doc = frappe.get_doc('Serial and Batch Bundle', bundle)
doc.entries[0].serial_no = serial_nos[1]
doc.save()
out.save()
out.submit()
value_diff = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': out.name, 'voucher_type': 'Delivery Note'}, 'stock_value_difference')
self.assertEqual(value_diff, -113)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:189*

### test_auto_fetch

**Category**: workflow  
**Description**: Workflow: test auto fetch  
**Expected**: self.assertEqual(non_expired_serials, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = make_item(properties={'has_serial_no': 1, 'has_batch_no': 1, 'create_new_batch': 1, 'serial_no_series': 'TEST.#######'}).name
warehouse = '_Test Warehouse - _TC'
in1 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
in2 = make_stock_entry(item_code=item_code, to_warehouse=warehouse, qty=5)
in1.reload()
in2.reload()
batch1 = get_batch_from_bundle(in1.items[0].serial_and_batch_bundle)
batch2 = get_batch_from_bundle(in2.items[0].serial_and_batch_bundle)
batch_wise_serials = {batch1: get_serial_nos_from_bundle(in1.items[0].serial_and_batch_bundle), batch2: get_serial_nos_from_bundle(in2.items[0].serial_and_batch_bundle)}
first_fetch = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse}))
self.assertEqual(first_fetch, batch_wise_serials[batch1])
partial_fetch = get_auto_serial_nos(_dict({'qty': 2, 'item_code': item_code, 'warehouse': warehouse}))
self.assertTrue(set(partial_fetch).issubset(set(first_fetch)), msg=f'{partial_fetch} should be subset of {first_fetch}')
remaining = get_auto_serial_nos(_dict({'qty': 3, 'item_code': item_code, 'warehouse': warehouse, 'ignore_serial_nos': partial_fetch}))
self.assertEqual(sorted(remaining + partial_fetch), first_fetch)
for batch, expected_serials in batch_wise_serials.items():
    fetched_sr = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch]}))
    self.assertEqual(fetched_sr, sorted(expected_serials))
self.assertFalse(get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': 'Non Existing Warehouse'})))
all_serials = [sr for sr_list in batch_wise_serials.values() for sr in sr_list]
fetched_serials = get_auto_serial_nos(_dict({'qty': 10, 'item_code': item_code, 'warehouse': warehouse, 'batches': list(batch_wise_serials.keys())}))
self.assertEqual(sorted(all_serials), fetched_serials)
frappe.db.set_value('Batch', batch1, 'expiry_date', '1980-01-01')
non_expired_serials = get_auto_serial_nos(_dict({'qty': 5, 'item_code': item_code, 'warehouse': warehouse, 'batches': [batch1]}))
self.assertEqual(non_expired_serials, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:225*

### test_cannot_create_direct

**Category**: workflow  
**Description**: Workflow: test cannot create direct  
**Expected**: self.assertTrue(SerialNoCannotCannotChangeError, sr.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.delete_doc_if_exists('Serial No', '_TCSER0001')
sr = frappe.new_doc('Serial No')
sr.item_code = '_Test Serialized Item'
sr.warehouse = '_Test Warehouse - _TC'
sr.serial_no = '_TCSER0001'
sr.purchase_rate = 10
self.assertRaises(SerialNoCannotCreateDirectError, sr.insert)
sr.warehouse = None
sr.insert()
self.assertTrue(sr.name)
sr.warehouse = '_Test Warehouse - _TC'
self.assertTrue(SerialNoCannotCannotChangeError, sr.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:31*

### test_inter_company_transfer

**Category**: workflow  
**Description**: Workflow: test inter company transfer  
**Expected**: self.assertEqual(serial_no.warehouse, wh)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
serial_no = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(serial_no.warehouse, None)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
serial_no.reload()
self.assertEqual(serial_no.warehouse, wh)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:48*

### test_inter_company_transfer_intermediate_cancellation

**Category**: workflow  
**Description**: Workflow: Receive into and Deliver Serial No from one company.
Then Receive into and Deliver from second company.
Try to cancel intermediate receipts/deliveries to test if it is blocked.  
**Expected**: self.assertRaises(frappe.ValidationError, pr.cancel)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tReceive into and Deliver Serial No from one company.\n\t\tThen Receive into and Deliver from second company.\n\t\tTry to cancel intermediate receipts/deliveries to test if it is blocked.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh)
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
self.assertRaises(frappe.ValidationError, dn.cancel)
create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
self.assertRaises(frappe.ValidationError, se.cancel)
self.assertRaises(frappe.ValidationError, dn.cancel)
self.assertRaises(frappe.ValidationError, pr.cancel)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:73*

### test_inter_company_transfer_fallback_on_cancel

**Category**: workflow  
**Description**: Workflow: Test Serial No state changes on cancellation.
If Delivery cancelled, it should fall back on last Receipt in the same company.
If Receipt is cancelled, it should be Inactive in the same company.  
**Expected**: self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\tTest Serial No state changes on cancellation.\n\t\tIf Delivery cancelled, it should fall back on last Receipt in the same company.\n\t\tIf Receipt is cancelled, it should be Inactive in the same company.\n\t\t'
se = make_serialized_item(self, target_warehouse='_Test Warehouse - _TC')
serial_nos = get_serial_nos_from_bundle(se.get('items')[0].serial_and_batch_bundle)
sn_doc = frappe.get_doc('Serial No', serial_nos[0])
dn = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]])
wh = create_warehouse('_Test Warehouse', company='_Test Company 1')
pr = make_purchase_receipt(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
dn_2 = create_delivery_note(item_code='_Test Serialized Item With Series', qty=1, serial_no=[serial_nos[0]], company='_Test Company 1', warehouse=wh, cost_center='_Test Company 1 - _TC1')
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn_2.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, wh)
pr.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, None)
dn.cancel()
sn_doc.reload()
self.assertEqual(sn_doc.warehouse, '_Test Warehouse - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/serial_no/test_serial_no.py:133*

### test_make_subcontracted_purchase_order

**Category**: workflow  
**Description**: Workflow: test make subcontracted purchase order  
**Expected**: self.assertEqual(mr.items[0].ordered_qty, 54)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.manufacturing.doctype.production_plan.test_production_plan import make_bom
from erpnext.stock.doctype.item.test_item import create_item, make_item
from erpnext.subcontracting.doctype.subcontracting_bom.test_subcontracting_bom import create_subcontracting_bom
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
mr.material_request_type = 'Subcontracting'
mr.submit()
frappe.db.set_value('Item', mr.items[0].item_code, 'is_sub_contracted_item', 1)
raw_materials = ['Raw Material Item 1', 'Raw Material Item 2']
for item in raw_materials:
    create_item(item)
frappe.new_doc('UOM').update({'uom_name': 'Test UOM'}).save()
service_item = make_item(properties={'is_stock_item': 0}, uoms=[{'uom': 'Test UOM', 'conversion_factor': 3}])
mr.items[0].default_bom = make_bom(item=mr.items[0].item_code, raw_materials=raw_materials)
mr.reload()
create_subcontracting_bom(finished_good=mr.items[0].item_code, service_item=service_item.name, finished_good_qty=2, service_item_qty=1, service_item_uom='Test UOM')
po = make_purchase_order(mr.name)
po.supplier = '_Test Supplier'
po.items[0].schedule_date = today()
po.items.pop(1)
self.assertEqual(po.items[0].stock_qty, 81)
self.assertEqual(po.items[0].qty, 27)
self.assertEqual(po.items[0].fg_item_qty, 54)
po.submit()
mr.reload()
self.assertEqual(mr.items[0].ordered_qty, 54)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:50*

### test_make_stock_entry

**Category**: workflow  
**Description**: Workflow: test make stock entry  
**Expected**: self.assertEqual(len(se.get('items')), len(mr.get('items')))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
mr.submit()
se = make_stock_entry(mr.name)
self.assertEqual(se.stock_entry_type, 'Material Transfer')
self.assertEqual(se.purpose, 'Material Transfer')
self.assertEqual(se.doctype, 'Stock Entry')
self.assertEqual(len(se.get('items')), len(mr.get('items')))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:111*

### test_partial_make_stock_entry

**Category**: workflow  
**Description**: Workflow: test partial make stock entry  
**Expected**: self.assertEqual(mr.status, 'Partially Received')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.stock_entry_utils import make_stock_entry as _make_stock_entry
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
source_wh = create_warehouse(warehouse_name='_Test Source Warehouse', properties={'parent_warehouse': 'All Warehouses - _TC'}, company='_Test Company')
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
for row in mr.items:
    _make_stock_entry(item_code=row.item_code, qty=10, to_warehouse=source_wh, company='_Test Company', rate=100)
    row.from_warehouse = source_wh
    row.qty = 10
mr.save()
mr.submit()
se = make_stock_entry(mr.name)
se.get('items')[0].qty = 5
se.insert()
se.submit()
mr.reload()
self.assertEqual(mr.status, 'Partially Received')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:126*

### test_in_transit_make_stock_entry

**Category**: workflow  
**Description**: Workflow: test in transit make stock entry  
**Expected**: self.assertEqual(se.doctype, 'Stock Entry')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Transfer'
mr.submit()
in_transit_warehouse = get_in_transit_warehouse(mr.company)
se = make_in_transit_stock_entry(mr.name, in_transit_warehouse)
self.assertEqual(se.stock_entry_type, 'Material Transfer')
self.assertEqual(se.purpose, 'Material Transfer')
self.assertEqual(se.doctype, 'Stock Entry')
for row in se.get('items'):
    self.assertEqual(row.t_warehouse, in_transit_warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:163*

### test_over_transfer_qty_allowance

**Category**: workflow  
**Description**: Workflow: test over transfer qty allowance  
**Expected**: self.assertRaises(frappe.ValidationError)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.new_doc('Material Request')
mr.company = '_Test Company'
mr.scheduled_date = today()
mr.append('items', {'item_code': '_Test FG Item', 'item_name': '_Test FG Item', 'qty': 10, 'schedule_date': today(), 'uom': '_Test UOM 1', 'warehouse': '_Test Warehouse - _TC'})
mr.material_request_type = 'Material Transfer'
mr.insert()
mr.submit()
frappe.db.set_single_value('Stock Settings', 'mr_qty_allowance', 20)
se_doc = make_stock_entry(mr.name)
se_doc.update({'posting_date': today(), 'posting_time': '00:00'})
se_doc.get('items')[0].update({'qty': 13, 'transfer_qty': 12.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
sr = frappe.new_doc('Stock Reconciliation')
sr.company = '_Test Company'
sr.purpose = 'Opening Stock'
sr.append('items', {'item_code': '_Test FG Item', 'warehouse': '_Test Warehouse - _TC', 'qty': 20, 'valuation_rate': 0.01})
sr.insert()
sr.submit()
se = frappe.copy_doc(se_doc)
se.insert()
self.assertRaises(frappe.ValidationError)
se.items[0].qty = 12
se.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:484*

### test_incorrect_mapping_of_stock_entry

**Category**: workflow  
**Description**: Workflow: test incorrect mapping of stock entry  
**Expected**: self.assertEqual(se_doc.get('items')[0].s_warehouse, '_Test Warehouse - _TC')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Transfer'
mr.insert()
mr.submit()
se_doc = make_stock_entry(mr.name)
se_doc.update({'posting_date': '2013-03-01', 'posting_time': '00:00', 'fiscal_year': '_Test Fiscal Year 2013'})
se_doc.get('items')[0].update({'qty': 60.0, 'transfer_qty': 60.0, 's_warehouse': '_Test Warehouse - _TC', 't_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
se_doc.get('items')[1].update({'item_code': '_Test Item Home Desktop 100', 'qty': 3.0, 'transfer_qty': 3.0, 's_warehouse': '_Test Warehouse 1 - _TC', 'basic_rate': 1.0})
se = frappe.copy_doc(se_doc)
self.assertRaises(frappe.MappingMismatchError, se.insert)
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Issue'
mr.insert()
mr.submit()
se_doc = make_stock_entry(mr.name)
self.assertEqual(se_doc.get('items')[0].s_warehouse, '_Test Warehouse - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:628*

### test_make_stock_entry_for_material_issue

**Category**: workflow  
**Description**: Workflow: test make stock entry for material issue  
**Expected**: self.assertEqual(len(se.get('items')), len(mr.get('items')))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0]).insert()
self.assertRaises(frappe.ValidationError, make_stock_entry, mr.name)
mr = frappe.get_doc('Material Request', mr.name)
mr.material_request_type = 'Material Issue'
mr.submit()
se = make_stock_entry(mr.name)
self.assertEqual(se.doctype, 'Stock Entry')
self.assertEqual(len(se.get('items')), len(mr.get('items')))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:687*

### test_completed_qty_for_issue

**Category**: workflow  
**Description**: Workflow: test completed qty for issue  
**Expected**: self.assertEqual(_get_requested_qty(), existing_requested_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
def _get_requested_qty():
    return flt(frappe.db.get_value('Bin', {'item_code': '_Test Item Home Desktop 100', 'warehouse': '_Test Warehouse - _TC'}, 'indented_qty'))
existing_requested_qty = _get_requested_qty()
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][0])
mr.material_request_type = 'Material Issue'
mr.submit()
frappe.db.value_cache.clear()
self.assertEqual(_get_requested_qty(), existing_requested_qty - 54.0)
self._insert_stock_entry(60, 6, '_Test Warehouse - _TC')
se_doc = make_stock_entry(mr.name)
se_doc.fiscal_year = '_Test Fiscal Year 2014'
se_doc.get('items')[0].qty = 54.0
se_doc.insert()
se_doc.submit()
mr.load_from_db()
self.assertEqual(mr.get('items')[0].ordered_qty, 54.0)
self.assertEqual(mr.get('items')[1].ordered_qty, 3.0)
self.assertEqual(_get_requested_qty(), existing_requested_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:700*

### test_material_request_type_manufacture

**Category**: workflow  
**Description**: Workflow: test material request type manufacture  
**Expected**: self.assertEqual(requested_qty, new_requested_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
mr = frappe.copy_doc(self.globalTestRecords['Material Request'][1]).insert()
mr = frappe.get_doc('Material Request', mr.name)
mr.submit()
completed_qty = mr.items[0].ordered_qty
requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
prod_order = raise_work_orders(mr.name, mr.company)
po = frappe.get_doc('Work Order', prod_order[0])
po.wip_warehouse = '_Test Warehouse 1 - _TC'
po.submit()
mr = frappe.get_doc('Material Request', mr.name)
self.assertEqual(completed_qty + po.qty, mr.items[0].ordered_qty)
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
self.assertEqual(requested_qty - po.qty, new_requested_qty)
po.cancel()
mr = frappe.get_doc('Material Request', mr.name)
self.assertEqual(completed_qty, mr.items[0].ordered_qty)
new_requested_qty = frappe.db.sql('select indented_qty from `tabBin` where \t\t\titem_code= %s and warehouse= %s ', (mr.items[0].item_code, mr.items[0].warehouse))[0][0]
self.assertEqual(requested_qty, new_requested_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:739*

### test_requested_qty_multi_uom

**Category**: workflow  
**Description**: Workflow: test requested qty multi uom  
**Expected**: self.assertEqual(requested_qty, existing_requested_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
existing_requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
mr = make_material_request(item_code='_Test FG Item', material_request_type='Manufacture', uom='_Test UOM 1', conversion_factor=12)
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 120)
work_order = raise_work_orders(mr.name, mr.company)
wo = frappe.get_doc('Work Order', work_order[0])
wo.qty = 50
wo.wip_warehouse = '_Test Warehouse 1 - _TC'
wo.submit()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 70)
wo.cancel()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty + 120)
mr.reload()
mr.cancel()
requested_qty = self._get_requested_qty('_Test FG Item', '_Test Warehouse - _TC')
self.assertEqual(requested_qty, existing_requested_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/material_request/test_material_request.py:778*

### test_available_serial_no

**Category**: workflow  
**Description**: Workflow: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 5)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
item = create_item('_Test Item with Serial No', is_stock_item=1)
item.has_serial_no = 1
item.serial_no_series = 'TEST.###'
item.save(ignore_permissions=True)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='_Test Item With Serial No')

report = frappe.get_doc('Report', 'Available Serial No')
make_purchase_receipt(qty=10, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 10)
create_delivery_note(qty=5, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:30*

### test_available_serial_no

**Category**: workflow  
**Description**: Workflow: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 5)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
report = frappe.get_doc('Report', 'Available Serial No')
make_purchase_receipt(qty=10, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 10)
create_delivery_note(qty=5, item_code='_Test Item with Serial No')
data = report.get_data(filters=self.filters)
serial_nos = [item for item in data[-1][-1]['balance_serial_no'].split('\n')]
self.assertEqual(len(serial_nos), 5)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:30*

### test_fifo_qty_hypothesis

**Category**: workflow  
**Description**: Workflow: test fifo qty hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.queue = FIFOValuation([])

self.queue = FIFOValuation([])
total_qty = 0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
    self.assertTotalQty(total_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:127*

### test_fifo_qty_value_nonneg_hypothesis

**Category**: workflow  
**Description**: Workflow: test fifo qty value nonneg hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.queue = FIFOValuation([])

self.queue = FIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:147*

### test_fifo_qty_value_nonneg_hypothesis_with_outgoing_rate

**Category**: workflow  
**Description**: Workflow: test fifo qty value nonneg hypothesis with outgoing rate  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.queue = FIFOValuation([])

self.queue = FIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty, outgoing_rate)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:172*

### test_lifo_consumption_multiple

**Category**: workflow  
**Description**: Workflow: test lifo consumption multiple  
**Expected**: self.assertEqual(consumed, [[5, 5]])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.stack = LIFOValuation([])

self.stack.add_stock(1, 1)
self.stack.add_stock(2, 2)
consumed = self.stack.remove_stock(1)
self.assertEqual(consumed, [[1, 2]])
self.stack.add_stock(3, 3)
consumed = self.stack.remove_stock(4)
self.assertEqual(consumed, [[3, 3], [1, 2]])
self.stack.add_stock(4, 4)
consumed = self.stack.remove_stock(5)
self.assertEqual(consumed, [[4, 4], [1, 1]])
self.stack.add_stock(5, 5)
consumed = self.stack.remove_stock(5)
self.assertEqual(consumed, [[5, 5]])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:255*

### test_lifo_qty_hypothesis

**Category**: workflow  
**Description**: Workflow: test lifo qty hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.stack = LIFOValuation([])

self.stack = LIFOValuation([])
total_qty = 0
for qty, rate in stock_stack:
    if round_off_if_near_zero(qty) == 0:
        continue
    if qty > 0:
        self.stack.add_stock(qty, rate)
        total_qty += qty
    else:
        qty = abs(qty)
        consumed = self.stack.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
    self.assertTotalQty(total_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:274*

### test_lifo_qty_value_nonneg_hypothesis

**Category**: workflow  
**Description**: Workflow: test lifo qty value nonneg hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.stack = LIFOValuation([])

self.stack = LIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_stack:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.stack.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.stack.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:294*

### test_lifo_values

**Category**: workflow  
**Description**: Workflow: test lifo values  
**Expected**: self.assertStockQueue(out5, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
in1 = self._make_stock_entry(1, 1)
self.assertStockQueue(in1, [[1, 1]])
in2 = self._make_stock_entry(2, 2)
self.assertStockQueue(in2, [[1, 1], [2, 2]])
out1 = self._make_stock_entry(-1)
self.assertStockQueue(out1, [[1, 1], [1, 2]])
in3 = self._make_stock_entry(3, 3)
self.assertStockQueue(in3, [[1, 1], [1, 2], [3, 3]])
out2 = self._make_stock_entry(-4)
self.assertStockQueue(out2, [[1, 1]])
in4 = self._make_stock_entry(4, 4)
self.assertStockQueue(in4, [[1, 1], [4, 4]])
out3 = self._make_stock_entry(-5)
self.assertStockQueue(out3, [])
in5 = self._make_stock_entry(5, 5)
self.assertStockQueue(in5, [[5, 5]])
out5 = self._make_stock_entry(-5)
self.assertStockQueue(out5, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:352*

### test_fifo_qty_hypothesis

**Category**: workflow  
**Description**: Workflow: test fifo qty hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
# Fixtures: stock_queue

self.queue = FIFOValuation([])
total_qty = 0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
    self.assertTotalQty(total_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:127*

### test_fifo_qty_value_nonneg_hypothesis

**Category**: workflow  
**Description**: Workflow: test fifo qty value nonneg hypothesis  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
# Fixtures: stock_queue

self.queue = FIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:147*

### test_fifo_qty_value_nonneg_hypothesis_with_outgoing_rate

**Category**: workflow  
**Description**: Workflow: test fifo qty value nonneg hypothesis with outgoing rate  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
# Fixtures: stock_queue, outgoing_rate

self.queue = FIFOValuation([])
total_qty = 0.0
total_value = 0.0
for qty, rate in stock_queue:
    if round_off_if_near_zero(qty) == 0 or total_qty + qty < 0 or abs(qty) < 0.1:
        continue
    if qty > 0:
        self.queue.add_stock(qty, rate)
        total_qty += qty
        total_value += qty * rate
    else:
        qty = abs(qty)
        consumed = self.queue.remove_stock(qty, outgoing_rate)
        self.assertAlmostEqual(qty, sum((q for q, _ in consumed)), msg=f'incorrect consumption {consumed}')
        total_qty -= qty
        total_value -= sum((q * r for q, r in consumed))
    self.assertTotalQty(total_qty)
    self.assertTotalValue(total_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_valuation.py:172*

### test_newly_mapped_doc_packed_items

**Category**: workflow  
**Description**: Workflow: Test impact on packed items in newly mapped DN from SO.  
**Expected**: self.assertEqual(dn.packed_items[3].qty, 6)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact on packed items in newly mapped DN from SO.'
so_items = []
for qty in [2, 4]:
    so_items.append({'item_code': self.bundle, 'qty': qty, 'rate': 400, 'warehouse': '_Test Warehouse - _TC'})
so = make_sales_order(item_list=so_items)
dn = make_delivery_note(so.name)
dn.items[1].qty = 3
dn.save()
self.assertEqual(len(dn.packed_items), 4)
self.assertEqual(dn.packed_items[2].qty, 6)
self.assertEqual(dn.packed_items[3].qty, 6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:131*

### test_reposting_packed_items

**Category**: workflow  
**Description**: Workflow: test reposting packed items  
**Expected**: self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = 'Stores - TCP1'
company = '_Test Company with perpetual inventory'
today = nowdate()
yesterday = add_to_date(today, days=-1, as_string=True)
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=100, posting_date=today)
so = make_sales_order(item_code=self.bundle, qty=1, company=company, warehouse=warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
gles = get_gl_entries(dn.doctype, dn.name)
credit_before_repost = sum((gle.credit for gle in gles))
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=200, posting_date=yesterday)
gles = get_gl_entries(dn.doctype, dn.name)
credit_after_reposting = sum((gle.credit for gle in gles))
self.assertNotEqual(credit_before_repost, credit_after_reposting)
self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:150*

### test_returning_full_bundles

**Category**: workflow  
**Description**: Workflow: test returning full bundles  
**Expected**: self.assertReturns(dn.packed_items, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.save()
dn_ret.submit()
self.assertReturns(dn.packed_items, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:192*

### test_returning_partial_bundles

**Category**: workflow  
**Description**: Workflow: test returning partial bundles  
**Expected**: self.assertReturns(expected_returns, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.items.pop()
dn_ret.save()
dn_ret.submit()
dn_ret.reload()
self.assertTrue(all((d.parent_item == self.bundle for d in dn_ret.packed_items)))
expected_returns = [d for d in dn.packed_items if d.parent_item == self.bundle]
self.assertReturns(expected_returns, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:221*

### test_returning_partial_bundle_qty

**Category**: workflow  
**Description**: Workflow: test returning partial bundle qty  
**Expected**: self.assertReturns(expected_returns, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
so = make_sales_order(item_code=self.bundle, warehouse=self.warehouse, qty=2)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.items[0].qty = -1
dn_ret.save()
dn_ret.submit()
expected_returns = dn.packed_items
for d in expected_returns:
    d.qty /= 2
self.assertReturns(expected_returns, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:258*

### test_newly_mapped_doc_packed_items

**Category**: workflow  
**Description**: Workflow: Test impact on packed items in newly mapped DN from SO.  
**Expected**: self.assertEqual(dn.packed_items[3].qty, 6)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test impact on packed items in newly mapped DN from SO.'
so_items = []
for qty in [2, 4]:
    so_items.append({'item_code': self.bundle, 'qty': qty, 'rate': 400, 'warehouse': '_Test Warehouse - _TC'})
so = make_sales_order(item_list=so_items)
dn = make_delivery_note(so.name)
dn.items[1].qty = 3
dn.save()
self.assertEqual(len(dn.packed_items), 4)
self.assertEqual(dn.packed_items[2].qty, 6)
self.assertEqual(dn.packed_items[3].qty, 6)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:131*

### test_reposting_packed_items

**Category**: workflow  
**Description**: Workflow: test reposting packed items  
**Expected**: self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = 'Stores - TCP1'
company = '_Test Company with perpetual inventory'
today = nowdate()
yesterday = add_to_date(today, days=-1, as_string=True)
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=100, posting_date=today)
so = make_sales_order(item_code=self.bundle, qty=1, company=company, warehouse=warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
gles = get_gl_entries(dn.doctype, dn.name)
credit_before_repost = sum((gle.credit for gle in gles))
for item in self.bundle_items:
    make_stock_entry(item_code=item, to_warehouse=warehouse, qty=10, rate=200, posting_date=yesterday)
gles = get_gl_entries(dn.doctype, dn.name)
credit_after_reposting = sum((gle.credit for gle in gles))
self.assertNotEqual(credit_before_repost, credit_after_reposting)
self.assertAlmostEqual(credit_after_reposting, 2 * credit_before_repost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:150*

### test_returning_full_bundles

**Category**: workflow  
**Description**: Workflow: test returning full bundles  
**Expected**: self.assertReturns(dn.packed_items, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.save()
dn_ret.submit()
self.assertReturns(dn.packed_items, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:192*

### test_returning_partial_bundles

**Category**: workflow  
**Description**: Workflow: test returning partial bundles  
**Expected**: self.assertReturns(expected_returns, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
item_list = [{'item_code': self.bundle, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}, {'item_code': self.bundle2, 'warehouse': self.warehouse, 'qty': 1, 'rate': 100}]
so = make_sales_order(item_list=item_list, warehouse=self.warehouse)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.items.pop()
dn_ret.save()
dn_ret.submit()
dn_ret.reload()
self.assertTrue(all((d.parent_item == self.bundle for d in dn_ret.packed_items)))
expected_returns = [d for d in dn.packed_items if d.parent_item == self.bundle]
self.assertReturns(expected_returns, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:221*

### test_returning_partial_bundle_qty

**Category**: workflow  
**Description**: Workflow: test returning partial bundle qty  
**Expected**: self.assertReturns(expected_returns, dn_ret.packed_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.delivery_note.delivery_note import make_sales_return
so = make_sales_order(item_code=self.bundle, warehouse=self.warehouse, qty=2)
dn = make_delivery_note(so.name)
dn.save()
dn.submit()
dn_ret = make_sales_return(dn.name)
dn_ret.items[0].qty = -1
dn_ret.save()
dn_ret.submit()
expected_returns = dn.packed_items
for d in expected_returns:
    d.qty /= 2
self.assertReturns(expected_returns, dn_ret.packed_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packed_item/test_packed_item.py:258*

### test_inventory_dimension

**Category**: workflow  
**Description**: Workflow: test inventory dimension  
**Expected**: self.assertRaises(DoNotChangeError, inv_dim1.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
prepare_test_data()
create_store_dimension()

warehouse = 'Shelf Warehouse - _TC'
item_code = '_Test Item'
inv_dim1 = create_inventory_dimension(reference_document='Shelf', type_of_transaction='Outward', dimension_name='Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Issue'")
inv_dim1.reqd = 0
inv_dim1.save()
create_inventory_dimension(reference_document='Shelf', type_of_transaction='Inward', dimension_name='To Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Receipt'")
inward = make_stock_entry(item_code=item_code, target=warehouse, qty=5, basic_rate=10, do_not_save=True, purpose='Material Receipt')
inward.items[0].to_shelf = 'Shelf 1'
inward.save()
inward.submit()
inward.load_from_db()
sle_data = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': inward.name}, ['shelf', 'warehouse'], as_dict=1)
self.assertEqual(inward.items[0].to_shelf, 'Shelf 1')
self.assertEqual(sle_data.warehouse, warehouse)
self.assertEqual(sle_data.shelf, 'Shelf 1')
outward = make_stock_entry(item_code=item_code, source=warehouse, qty=3, basic_rate=10, do_not_save=True, purpose='Material Issue')
outward.items[0].shelf = 'Shelf 1'
outward.save()
outward.submit()
outward.load_from_db()
sle_shelf = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': outward.name}, 'shelf')
self.assertEqual(sle_shelf, 'Shelf 1')
inv_dim1.load_from_db()
inv_dim1.apply_to_all_doctypes = 1
self.assertTrue(inv_dim1.has_stock_ledger())
self.assertRaises(DoNotChangeError, inv_dim1.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:79*

### test_inventory_dimension_for_purchase_receipt_and_delivery_note

**Category**: workflow  
**Description**: Workflow: test inventory dimension for purchase receipt and delivery note  
**Expected**: self.assertEqual(sle_rack, 'Rack 1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
prepare_test_data()
create_store_dimension()

inv_dimension = create_inventory_dimension(reference_document='Rack', dimension_name='Rack', apply_to_all_doctypes=1)
inv_dimension.db_set('fetch_from_parent', 'Rack')
self.assertEqual(inv_dimension.type_of_transaction, 'Both')
self.assertEqual(inv_dimension.fetch_from_parent, 'Rack')
create_custom_field('Purchase Receipt', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
create_custom_field('Delivery Note', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
pr_doc = make_purchase_receipt(qty=2, do_not_submit=True)
pr_doc.rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc.load_from_db()
self.assertEqual(pr_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': pr_doc.items[0].name, 'voucher_type': pr_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
dn_doc = create_delivery_note(qty=2, do_not_submit=True)
dn_doc.rack = 'Rack 1'
dn_doc.save()
dn_doc.submit()
dn_doc.load_from_db()
self.assertEqual(dn_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': dn_doc.items[0].name, 'voucher_type': dn_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:149*

### test_validate_negative_stock_for_inventory_dimension

**Category**: workflow  
**Description**: Workflow: test validate negative stock for inventory dimension  
**Expected**: self.assertEqual(site_name, 'Site 1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
prepare_test_data()
create_store_dimension()

item_code = 'Test Negative Inventory Dimension Item'
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
create_item(item_code)
inv_dimension = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
warehouse = create_warehouse('Negative Stock Warehouse')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=10, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
doc.reload()
if doc.docstatus == 1:
    doc.cancel()
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=10, do_not_submit=True)
doc.items[0].to_inv_site = 'Site 1'
doc.submit()
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=100)
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
inv_dimension.reload()
inv_dimension.db_set('validate_negative_stock', 0)
frappe.clear_cache(doctype='Inventory Dimension')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
doc.submit()
self.assertEqual(doc.docstatus, 1)
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:435*

### test_validate_negative_stock_with_multiple_dimension

**Category**: workflow  
**Description**: Workflow: test validate negative stock with multiple dimension  
**Expected**: self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
prepare_test_data()
create_store_dimension()

item_code = 'Test Negative Multi Inventory Dimension Item'
create_item(item_code)
inv_dimension_1 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
inv_dimension_1.db_set('validate_negative_stock', 1)
inv_dimension_2 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Rack', reference_document='Rack', document_type='Rack', validate_negative_stock=1)
inv_dimension_2.db_set('validate_negative_stock', 1)
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=15, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=25, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
dn_doc = create_delivery_note(item_code=item_code, qty=35, do_not_submit=True)
dn_doc.items[0].inv_site = 'Site 2'
dn_doc.items[0].rack = 'Rack 1'
dn_doc.save()
self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:500*

### test_inventory_dimension

**Category**: workflow  
**Description**: Workflow: test inventory dimension  
**Expected**: self.assertRaises(DoNotChangeError, inv_dim1.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
warehouse = 'Shelf Warehouse - _TC'
item_code = '_Test Item'
inv_dim1 = create_inventory_dimension(reference_document='Shelf', type_of_transaction='Outward', dimension_name='Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Issue'")
inv_dim1.reqd = 0
inv_dim1.save()
create_inventory_dimension(reference_document='Shelf', type_of_transaction='Inward', dimension_name='To Shelf', apply_to_all_doctypes=0, document_type='Stock Entry Detail', condition="parent.purpose == 'Material Receipt'")
inward = make_stock_entry(item_code=item_code, target=warehouse, qty=5, basic_rate=10, do_not_save=True, purpose='Material Receipt')
inward.items[0].to_shelf = 'Shelf 1'
inward.save()
inward.submit()
inward.load_from_db()
sle_data = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': inward.name}, ['shelf', 'warehouse'], as_dict=1)
self.assertEqual(inward.items[0].to_shelf, 'Shelf 1')
self.assertEqual(sle_data.warehouse, warehouse)
self.assertEqual(sle_data.shelf, 'Shelf 1')
outward = make_stock_entry(item_code=item_code, source=warehouse, qty=3, basic_rate=10, do_not_save=True, purpose='Material Issue')
outward.items[0].shelf = 'Shelf 1'
outward.save()
outward.submit()
outward.load_from_db()
sle_shelf = frappe.db.get_value('Stock Ledger Entry', {'voucher_no': outward.name}, 'shelf')
self.assertEqual(sle_shelf, 'Shelf 1')
inv_dim1.load_from_db()
inv_dim1.apply_to_all_doctypes = 1
self.assertTrue(inv_dim1.has_stock_ledger())
self.assertRaises(DoNotChangeError, inv_dim1.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:79*

### test_inventory_dimension_for_purchase_receipt_and_delivery_note

**Category**: workflow  
**Description**: Workflow: test inventory dimension for purchase receipt and delivery note  
**Expected**: self.assertEqual(sle_rack, 'Rack 1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
inv_dimension = create_inventory_dimension(reference_document='Rack', dimension_name='Rack', apply_to_all_doctypes=1)
inv_dimension.db_set('fetch_from_parent', 'Rack')
self.assertEqual(inv_dimension.type_of_transaction, 'Both')
self.assertEqual(inv_dimension.fetch_from_parent, 'Rack')
create_custom_field('Purchase Receipt', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
create_custom_field('Delivery Note', dict(fieldname='rack', label='Rack', fieldtype='Link', options='Rack'))
pr_doc = make_purchase_receipt(qty=2, do_not_submit=True)
pr_doc.rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc.load_from_db()
self.assertEqual(pr_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': pr_doc.items[0].name, 'voucher_type': pr_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
dn_doc = create_delivery_note(qty=2, do_not_submit=True)
dn_doc.rack = 'Rack 1'
dn_doc.save()
dn_doc.submit()
dn_doc.load_from_db()
self.assertEqual(dn_doc.items[0].rack, 'Rack 1')
sle_rack = frappe.db.get_value('Stock Ledger Entry', {'voucher_detail_no': dn_doc.items[0].name, 'voucher_type': dn_doc.doctype}, 'rack')
self.assertEqual(sle_rack, 'Rack 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:149*

### test_validate_negative_stock_for_inventory_dimension

**Category**: workflow  
**Description**: Workflow: test validate negative stock for inventory dimension  
**Expected**: self.assertEqual(site_name, 'Site 1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = 'Test Negative Inventory Dimension Item'
frappe.db.set_single_value('Stock Settings', 'allow_negative_stock', 1)
create_item(item_code)
inv_dimension = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
warehouse = create_warehouse('Negative Stock Warehouse')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=10, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
doc.reload()
if doc.docstatus == 1:
    doc.cancel()
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=10, do_not_submit=True)
doc.items[0].to_inv_site = 'Site 1'
doc.submit()
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
doc = make_stock_entry(item_code=item_code, target=warehouse, qty=100)
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
self.assertRaises(InventoryDimensionNegativeStockError, doc.submit)
inv_dimension.reload()
inv_dimension.db_set('validate_negative_stock', 0)
frappe.clear_cache(doctype='Inventory Dimension')
doc = make_stock_entry(item_code=item_code, source=warehouse, qty=100, do_not_submit=True)
doc.items[0].inv_site = 'Site 1'
doc.submit()
self.assertEqual(doc.docstatus, 1)
site_name = frappe.get_all('Stock Ledger Entry', filters={'voucher_no': doc.name, 'is_cancelled': 0}, fields=['inv_site'])[0].inv_site
self.assertEqual(site_name, 'Site 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:435*

### test_validate_negative_stock_with_multiple_dimension

**Category**: workflow  
**Description**: Workflow: test validate negative stock with multiple dimension  
**Expected**: self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = 'Test Negative Multi Inventory Dimension Item'
create_item(item_code)
inv_dimension_1 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Inv Site', reference_document='Inv Site', document_type='Inv Site', validate_negative_stock=1)
inv_dimension_1.db_set('validate_negative_stock', 1)
inv_dimension_2 = create_inventory_dimension(apply_to_all_doctypes=1, dimension_name='Rack', reference_document='Rack', document_type='Rack', validate_negative_stock=1)
inv_dimension_2.db_set('validate_negative_stock', 1)
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=15, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 1'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=30, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 1'
pr_doc.save()
pr_doc.submit()
pr_doc = make_purchase_receipt(item_code=item_code, qty=25, do_not_submit=True)
pr_doc.items[0].inv_site = 'Site 2'
pr_doc.items[0].rack = 'Rack 2'
pr_doc.save()
pr_doc.submit()
dn_doc = create_delivery_note(item_code=item_code, qty=35, do_not_submit=True)
dn_doc.items[0].inv_site = 'Site 2'
dn_doc.items[0].rack = 'Rack 1'
dn_doc.save()
self.assertRaises(InventoryDimensionNegativeStockError, dn_doc.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:500*

### test_show_item_attr

**Category**: workflow  
**Description**: Workflow: test show item attr  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

from erpnext.controllers.item_variant import create_variant
self.item.has_variants = True
self.item.append('attributes', {'attribute': 'Test Size'})
self.item.save()
attributes = {'Test Size': 'Large'}
variant = create_variant(self.item.name, attributes)
variant.save()
self.generate_stock_ledger(variant.name, [_dict(qty=5, rate=10)])
rows = stock_balance(self.filters.update({'show_variant_attributes': 1, 'item_code': [variant.name]}))
self.assertPartialDictEq(attributes, rows[0])
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:156*

### test_show_item_attr

**Category**: workflow  
**Description**: Workflow: test show item attr  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.controllers.item_variant import create_variant
self.item.has_variants = True
self.item.append('attributes', {'attribute': 'Test Size'})
self.item.save()
attributes = {'Test Size': 'Large'}
variant = create_variant(self.item.name, attributes)
variant.save()
self.generate_stock_ledger(variant.name, [_dict(qty=5, rate=10)])
rows = stock_balance(self.filters.update({'show_variant_attributes': 1, 'item_code': [variant.name]}))
self.assertPartialDictEq(attributes, rows[0])
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:156*

### test_item_shortage_report

**Category**: method_call  
**Description**: test item shortage report  
**Expected**: self.assertEqual(projected_qty, -so.items[0].qty)  
**Confidence**: 0.85  

```python
self.assertEqual(reserved_qty, so.items[0].qty)
self.assertEqual(projected_qty, -so.items[0].qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:27*

### test_item_shortage_report

**Category**: method_call  
**Description**: test item shortage report  
**Expected**: self.assertEqual(projected_qty, -so.items[0].qty)  
**Confidence**: 0.85  

```python
self.assertEqual(reserved_qty, so.items[0].qty)
self.assertEqual(projected_qty, -so.items[0].qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:27*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertEqual(warehouse.is_group, 1)  
**Confidence**: 0.85  

```python
warehouse.reload()
self.assertEqual(warehouse.is_group, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:76*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertEqual(warehouse.is_group, 0)  
**Confidence**: 0.85  

```python
warehouse.reload()
self.assertEqual(warehouse.is_group, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:85*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertRaises(frappe.ValidationError, convert_to_group_or_ledger, warehouse.name)  
**Confidence**: 0.85  

```python
make_stock_entry(item_code='_Test Item', target=warehouse.name, qty=1)
self.assertRaises(frappe.ValidationError, convert_to_group_or_ledger, warehouse.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:88*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertEqual(warehouse.is_group, 1)  
**Confidence**: 0.85  

```python
warehouse.reload()
self.assertEqual(warehouse.is_group, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:76*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertEqual(warehouse.is_group, 0)  
**Confidence**: 0.85  

```python
warehouse.reload()
self.assertEqual(warehouse.is_group, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:85*

### test_group_non_group_conversion

**Category**: method_call  
**Description**: test group non group conversion  
**Expected**: self.assertRaises(frappe.ValidationError, convert_to_group_or_ledger, warehouse.name)  
**Confidence**: 0.85  

```python
make_stock_entry(item_code='_Test Item', target=warehouse.name, qty=1)
self.assertRaises(frappe.ValidationError, convert_to_group_or_ledger, warehouse.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/warehouse/test_warehouse.py:88*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(batch_scan['batch_no'], batch.name)  
**Confidence**: 0.85  

```python
self.assertEqual(batch_scan['item_code'], batch_item.name)
self.assertEqual(batch_scan['batch_no'], batch.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:82*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(batch_scan['has_batch_no'], 1)  
**Confidence**: 0.85  

```python
self.assertEqual(batch_scan['batch_no'], batch.name)
self.assertEqual(batch_scan['has_batch_no'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:83*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(batch_scan['has_serial_no'], 0)  
**Confidence**: 0.85  

```python
self.assertEqual(batch_scan['has_batch_no'], 1)
self.assertEqual(batch_scan['has_serial_no'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:84*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(serial_scan['serial_no'], serial.name)  
**Confidence**: 0.85  

```python
self.assertEqual(serial_scan['item_code'], serial_item.name)
self.assertEqual(serial_scan['serial_no'], serial.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:93*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(serial_scan['has_batch_no'], 0)  
**Confidence**: 0.85  

```python
self.assertEqual(serial_scan['serial_no'], serial.name)
self.assertEqual(serial_scan['has_batch_no'], 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:94*

### test_barcode_scanning

**Category**: method_call  
**Description**: test barcode scanning  
**Expected**: self.assertEqual(serial_scan['has_serial_no'], 1)  
**Confidence**: 0.85  

```python
self.assertEqual(serial_scan['has_batch_no'], 0)
self.assertEqual(serial_scan['has_serial_no'], 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_utils.py:95*

### test_qa_for_delivery

**Category**: method_call  
**Description**: test qa for delivery  
**Expected**: self.assertRaises(QualityInspectionRejectedError, dn.submit)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

dn.reload()
self.assertRaises(QualityInspectionRejectedError, dn.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:36*

### test_value_based_qi_readings

**Category**: method_call  
**Description**: test value based qi readings  
**Expected**: self.assertEqual(qa.readings[0].status, 'Accepted')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

qa.save()
self.assertEqual(qa.readings[0].status, 'Accepted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:81*

### test_value_based_qi_readings

**Category**: method_call  
**Description**: test value based qi readings  
**Expected**: self.assertEqual(qa.readings[1].status, 'Accepted')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

self.assertEqual(qa.readings[0].status, 'Accepted')
self.assertEqual(qa.readings[1].status, 'Accepted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:84*

### test_formula_based_qi_readings

**Category**: method_call  
**Description**: test formula based qi readings  
**Expected**: self.assertEqual(qa.readings[0].status, 'Accepted')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
create_item('_Test Item with QA')
frappe.db.set_value('Item', '_Test Item with QA', 'inspection_required_before_delivery', 1)

qa.save()
self.assertEqual(qa.readings[0].status, 'Accepted')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/quality_inspection/test_quality_inspection.py:126*

### test_shipment_from_delivery_note

**Category**: method_call  
**Description**: test shipment from delivery note  
**Expected**: self.assertEqual(len(second_shipment.shipment_delivery_note), 1)  
**Confidence**: 0.85  

```python
self.assertEqual(second_shipment.value_of_goods, delivery_note.grand_total)
self.assertEqual(len(second_shipment.shipment_delivery_note), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:19*

### test_shipment_from_delivery_note

**Category**: method_call  
**Description**: test shipment from delivery note  
**Expected**: self.assertEqual(second_shipment.shipment_delivery_note[0].delivery_note, delivery_note.name)  
**Confidence**: 0.85  

```python
self.assertEqual(len(second_shipment.shipment_delivery_note), 1)
self.assertEqual(second_shipment.shipment_delivery_note[0].delivery_note, delivery_note.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:20*

### test_get_total_weight

**Category**: method_call  
**Description**: test get total weight  
**Expected**: self.assertEqual(shipment.get_total_weight(), 35)  
**Confidence**: 0.85  

```python
shipment.extend('shipment_parcel', [{'length': 5, 'width': 5, 'height': 5, 'weight': 5, 'count': 5}, {'length': 5, 'width': 5, 'height': 5, 'weight': 10, 'count': 1}])
self.assertEqual(shipment.get_total_weight(), 35)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:25*

### test_shipment_from_delivery_note

**Category**: method_call  
**Description**: test shipment from delivery note  
**Expected**: self.assertEqual(len(second_shipment.shipment_delivery_note), 1)  
**Confidence**: 0.85  

```python
self.assertEqual(second_shipment.value_of_goods, delivery_note.grand_total)
self.assertEqual(len(second_shipment.shipment_delivery_note), 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:19*

### test_shipment_from_delivery_note

**Category**: method_call  
**Description**: test shipment from delivery note  
**Expected**: self.assertEqual(second_shipment.shipment_delivery_note[0].delivery_note, delivery_note.name)  
**Confidence**: 0.85  

```python
self.assertEqual(len(second_shipment.shipment_delivery_note), 1)
self.assertEqual(second_shipment.shipment_delivery_note[0].delivery_note, delivery_note.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:20*

### test_get_total_weight

**Category**: method_call  
**Description**: test get total weight  
**Expected**: self.assertEqual(shipment.get_total_weight(), 35)  
**Confidence**: 0.85  

```python
shipment.extend('shipment_parcel', [{'length': 5, 'width': 5, 'height': 5, 'weight': 5, 'count': 5}, {'length': 5, 'width': 5, 'height': 5, 'weight': 10, 'count': 1}])
self.assertEqual(shipment.get_total_weight(), 35)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:25*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].rate, 75)  
**Confidence**: 0.85  

```python
self.assertIsNone(dn.items[0].batch_no)
self.assertEqual(dn.items[0].rate, 75)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:87*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].batch_no, 'BATCH01')  
**Confidence**: 0.85  

```python
dn.save()
self.assertEqual(dn.items[0].batch_no, 'BATCH01')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:91*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].rate, 50)  
**Confidence**: 0.85  

```python
self.assertEqual(dn.items[0].batch_no, 'BATCH01')
self.assertEqual(dn.items[0].rate, 50)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:92*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].rate, 75)  
**Confidence**: 0.85  

```python
self.assertIsNone(dn.items[0].batch_no)
self.assertEqual(dn.items[0].rate, 75)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:87*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].batch_no, 'BATCH01')  
**Confidence**: 0.85  

```python
dn.save()
self.assertEqual(dn.items[0].batch_no, 'BATCH01')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:91*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: method_call  
**Description**: test fetch price from list rate on doc save  
**Expected**: self.assertEqual(dn.items[0].rate, 50)  
**Confidence**: 0.85  

```python
self.assertEqual(dn.items[0].batch_no, 'BATCH01')
self.assertEqual(dn.items[0].rate, 50)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:92*

### test_empty_duplicate_validation

**Category**: method_call  
**Description**: test empty duplicate validation  
**Expected**: self.assertEqual(price, 21)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

frappe.db.rollback()
self.assertEqual(price, 21)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:198*

### test_empty_duplicate_validation

**Category**: method_call  
**Description**: test empty duplicate validation  
**Expected**: self.assertEqual(price, 21)  
**Confidence**: 0.85  

```python
frappe.db.rollback()
self.assertEqual(price, 21)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:198*

### test_delivery_trip_notify_customers

**Category**: method_call  
**Description**: test delivery trip notify customers  
**Expected**: self.assertEqual(self.delivery_trip.email_notification_sent, 1)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.delivery_trip.load_from_db()
self.assertEqual(self.delivery_trip.email_notification_sent, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:37*

### test_unoptimized_route_list_without_locks

**Category**: method_call  
**Description**: test unoptimized route list without locks  
**Expected**: self.assertEqual(len(route_list[0]), 4)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.assertEqual(len(route_list), 1)
self.assertEqual(len(route_list[0]), 4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:44*

### test_unoptimized_route_list_with_locks

**Category**: method_call  
**Description**: test unoptimized route list with locks  
**Expected**: self.assertEqual(len(route_list[0]), 4)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.assertEqual(len(route_list), 1)
self.assertEqual(len(route_list[0]), 4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:55*

### test_optimized_route_list_without_locks

**Category**: method_call  
**Description**: test optimized route list without locks  
**Expected**: self.assertEqual(len(route_list[0]), 4)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.assertEqual(len(route_list), 1)
self.assertEqual(len(route_list[0]), 4)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:63*

### test_optimized_route_list_with_locks

**Category**: method_call  
**Description**: test optimized route list with locks  
**Expected**: self.assertEqual(len(route_list[0]), 2)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.assertEqual(len(route_list), 2)
self.assertEqual(len(route_list[0]), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:72*

### test_optimized_route_list_with_locks

**Category**: method_call  
**Description**: test optimized route list with locks  
**Expected**: self.assertEqual(len(route_list[1]), 3)  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.assertEqual(len(route_list[0]), 2)
self.assertEqual(len(route_list[1]), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:73*

### test_delivery_trip_status_scheduled

**Category**: method_call  
**Description**: test delivery trip status scheduled  
**Expected**: self.assertEqual(self.delivery_trip.status, 'Scheduled')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.delivery_trip.submit()
self.assertEqual(self.delivery_trip.status, 'Scheduled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:80*

### test_delivery_trip_status_cancelled

**Category**: method_call  
**Description**: test delivery trip status cancelled  
**Expected**: self.assertEqual(self.delivery_trip.status, 'Cancelled')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
driver = create_driver()
create_vehicle()
create_delivery_notification()
create_test_contact_and_address()
address = create_address(driver)
self.delivery_trip = create_delivery_trip(driver, address)

self.delivery_trip.cancel()
self.assertEqual(self.delivery_trip.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/delivery_trip/test_delivery_trip.py:85*

### test_packing_slip

**Category**: method_call  
**Description**: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, dn.submit)  
**Confidence**: 0.85  

```python
dn.load_from_db()
self.assertRaises(frappe.exceptions.ValidationError, dn.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:104*

### test_packing_slip

**Category**: method_call  
**Description**: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, dn.submit)  
**Confidence**: 0.85  

```python
dn.load_from_db()
self.assertRaises(frappe.exceptions.ValidationError, dn.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:104*

### test_settings

**Category**: method_call  
**Description**: test settings  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.85  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Stock Settings', 'clean_description_html', 0)

item.reload()
self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:26*

### test_settings

**Category**: method_call  
**Description**: test settings  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.85  

```python
item.reload()
self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:26*

### test_inventory_dimension

**Category**: method_call  
**Description**: test inventory dimension  
**Expected**: self.assertEqual(sle_data.warehouse, warehouse)  
**Confidence**: 0.85  

```python
# Setup
prepare_test_data()
create_store_dimension()

self.assertEqual(inward.items[0].to_shelf, 'Shelf 1')
self.assertEqual(sle_data.warehouse, warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:122*

### test_inventory_dimension

**Category**: method_call  
**Description**: test inventory dimension  
**Expected**: self.assertEqual(sle_data.shelf, 'Shelf 1')  
**Confidence**: 0.85  

```python
# Setup
prepare_test_data()
create_store_dimension()

self.assertEqual(sle_data.warehouse, warehouse)
self.assertEqual(sle_data.shelf, 'Shelf 1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/inventory_dimension/test_inventory_dimension.py:123*

### test_basic_stock_balance

**Category**: method_call  
**Description**: Check very basic functionality and item info  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.85  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

self.assertPartialDictEq({'item_code': self.item.name, 'item_name': self.item.item_name, 'item_group': self.item.item_group, 'stock_uom': self.item.stock_uom, 'in_qty': 5, 'in_val': 50, 'val_rate': 10}, rows[0])
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:95*

### test_opening_balance

**Category**: method_call  
**Description**: test opening balance  
**Expected**: self.assertPartialDictEq({'opening_qty': 1, 'in_qty': 5}, rows[0])  
**Confidence**: 0.85  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

self.assertInvariants(rows)
self.assertPartialDictEq({'opening_qty': 1, 'in_qty': 5}, rows[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:122*

### test_opening_balance

**Category**: method_call  
**Description**: test opening balance  
**Expected**: self.assertPartialDictEq({'opening_qty': 6, 'in_qty': 0}, rows[0])  
**Confidence**: 0.85  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

self.assertInvariants(rows)
self.assertPartialDictEq({'opening_qty': 6, 'in_qty': 0}, rows[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:126*

### test_uom_converted_info

**Category**: method_call  
**Description**: test uom converted info  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.85  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

self.assertEqual(rows[0].bal_qty_alt, 1)
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:136*

### test_show_item_attr

**Category**: method_call  
**Description**: test show item attr  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.85  

```python
# Setup
self.item = make_item()
self.filters = _dict({'company': '_Test Company', 'item_code': [self.item.name], 'from_date': '2020-01-01', 'to_date': str(today())})

self.assertPartialDictEq(attributes, rows[0])
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:169*

### test_basic_stock_balance

**Category**: method_call  
**Description**: Check very basic functionality and item info  
**Expected**: self.assertInvariants(rows)  
**Confidence**: 0.85  

```python
self.assertPartialDictEq({'item_code': self.item.name, 'item_name': self.item.item_name, 'item_group': self.item.item_group, 'stock_uom': self.item.stock_uom, 'in_qty': 5, 'in_val': 50, 'val_rate': 10}, rows[0])
self.assertInvariants(rows)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:95*

### test_opening_balance

**Category**: method_call  
**Description**: test opening balance  
**Expected**: self.assertPartialDictEq({'opening_qty': 1, 'in_qty': 5}, rows[0])  
**Confidence**: 0.85  

```python
self.assertInvariants(rows)
self.assertPartialDictEq({'opening_qty': 1, 'in_qty': 5}, rows[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:122*

### test_opening_balance

**Category**: method_call  
**Description**: test opening balance  
**Expected**: self.assertPartialDictEq({'opening_qty': 6, 'in_qty': 0}, rows[0])  
**Confidence**: 0.85  

```python
self.assertInvariants(rows)
self.assertPartialDictEq({'opening_qty': 6, 'in_qty': 0}, rows[0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_balance/test_stock_balance.py:126*

### test_item_shortage_report

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test item shortage report  
**Expected**: self.assertEqual(reserved_qty, so.items[0].qty)  
**Confidence**: 0.80  

```python
so = make_sales_order(item_code=item)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:17*

### test_item_shortage_report

**Category**: instantiation  
**Description**: Instantiate get_value: test item shortage report  
**Expected**: self.assertEqual(reserved_qty, so.items[0].qty)  
**Confidence**: 0.80  

```python
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:19*

### test_item_shortage_report

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test item shortage report  
**Expected**: self.assertEqual(reserved_qty, so.items[0].qty)  
**Confidence**: 0.80  

```python
so = make_sales_order(item_code=item)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:17*

### test_item_shortage_report

**Category**: instantiation  
**Description**: Instantiate get_value: test item shortage report  
**Expected**: self.assertEqual(reserved_qty, so.items[0].qty)  
**Confidence**: 0.80  

```python
reserved_qty, projected_qty = frappe.db.get_value('Bin', {'item_code': item, 'warehouse': so.items[0].warehouse}, ['reserved_qty', 'projected_qty'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:19*

### test_get_period_date_ranges

**Category**: instantiation  
**Description**: Instantiate _dict: test get period date ranges  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
# Setup
self.item = make_item().name
self.warehouse = '_Test Warehouse - _TC'

filters = _dict(range='Monthly', from_date='2020-12-28', to_date='2021-02-06')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:58*

### test_get_period_date_ranges

**Category**: instantiation  
**Description**: Instantiate get_period_date_ranges: test get period date ranges  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
# Setup
self.item = make_item().name
self.warehouse = '_Test Warehouse - _TC'

ranges = get_period_date_ranges(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:60*

### test_get_period_date_ranges_yearly

**Category**: instantiation  
**Description**: Instantiate _dict: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
# Setup
self.item = make_item().name
self.warehouse = '_Test Warehouse - _TC'

filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:71*

### test_get_period_date_ranges_yearly

**Category**: instantiation  
**Description**: Instantiate get_period_date_ranges: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
# Setup
self.item = make_item().name
self.warehouse = '_Test Warehouse - _TC'

ranges = get_period_date_ranges(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:73*

### test_get_period_date_ranges

**Category**: instantiation  
**Description**: Instantiate _dict: test get period date ranges  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
filters = _dict(range='Monthly', from_date='2020-12-28', to_date='2021-02-06')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:58*

### test_get_period_date_ranges

**Category**: instantiation  
**Description**: Instantiate get_period_date_ranges: test get period date ranges  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
ranges = get_period_date_ranges(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:60*

### test_get_period_date_ranges_yearly

**Category**: instantiation  
**Description**: Instantiate _dict: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
filters = _dict(range='Yearly', from_date='2021-01-28', to_date='2021-02-06')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:71*

### test_get_period_date_ranges_yearly

**Category**: instantiation  
**Description**: Instantiate get_period_date_ranges: test get period date ranges yearly  
**Expected**: self.assertEqual(ranges, expected_ranges)  
**Confidence**: 0.80  

```python
ranges = get_period_date_ranges(filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/stock_analytics/test_stock_analytics.py:73*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_subcontracting_order: test alternative item for subcontract rm  
**Expected**: self.assertEqual(after_transfer_reserved_qty_for_sub_contract, flt(reserved_qty_for_sub_contract - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

sco = get_subcontracting_order(service_items=service_items, supplier_warehouse=supplier_warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:57*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_value: test alternative item for subcontract rm  
**Expected**: self.assertEqual(after_transfer_reserved_qty_for_sub_contract, flt(reserved_qty_for_sub_contract - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

reserved_qty_for_sub_contract = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_sub_contract')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:81*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_doc: test alternative item for subcontract rm  
**Expected**: self.assertEqual(after_transfer_reserved_qty_for_sub_contract, flt(reserved_qty_for_sub_contract - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

se = frappe.get_doc(make_rm_stock_entry(sco.name, rm_items))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:87*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_doc: test alternative item for subcontract rm  
**Expected**: self.assertEqual(after_transfer_reserved_qty_for_sub_contract, flt(reserved_qty_for_sub_contract - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

doc = frappe.get_doc('Stock Entry', se.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:91*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_value: test alternative item for subcontract rm  
**Expected**: self.assertEqual(after_transfer_reserved_qty_for_sub_contract, flt(reserved_qty_for_sub_contract - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

after_transfer_reserved_qty_for_sub_contract = frappe.db.get_value('Bin', {'item_code': 'Test FG A RW 1', 'warehouse': '_Test Warehouse - _TC'}, 'reserved_qty_for_sub_contract')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:101*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate make_subcontracting_receipt: test alternative item for subcontract rm  
**Expected**: self.assertEqual(status, True)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

scr = make_subcontracting_receipt(sco.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:109*

### test_alternative_item_for_subcontract_rm

**Category**: instantiation  
**Description**: Instantiate get_doc: test alternative item for subcontract rm  
**Expected**: self.assertEqual(status, True)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

scr = frappe.get_doc('Subcontracting Receipt', scr.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:112*

### test_alternative_item_for_production_rm

**Category**: instantiation  
**Description**: Instantiate make_wo_order_test_record: test alternative item for production rm  
**Expected**: self.assertEqual(reserved_qty_for_production_after_transfer, flt(reserved_qty_for_production - 5))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
make_items()

pro_order = make_wo_order_test_record(production_item='Test Finished Goods - A', qty=5, source_warehouse='_Test Warehouse - _TC', wip_warehouse='Test Supplier Warehouse - _TC')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_alternative/test_item_alternative.py:128*

### test_shipment_from_delivery_note

**Category**: instantiation  
**Description**: Instantiate create_test_shipment: test shipment from delivery note  
**Expected**: self.assertEqual(second_shipment.value_of_goods, delivery_note.grand_total)  
**Confidence**: 0.80  

```python
shipment = create_test_shipment([delivery_note])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:16*

### test_shipment_from_delivery_note

**Category**: instantiation  
**Description**: Instantiate make_shipment: test shipment from delivery note  
**Expected**: self.assertEqual(second_shipment.value_of_goods, delivery_note.grand_total)  
**Confidence**: 0.80  

```python
second_shipment = make_shipment(delivery_note.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:18*

### test_get_total_weight

**Category**: instantiation  
**Description**: Instantiate new_doc: test get total weight  
**Expected**: self.assertEqual(shipment.get_total_weight(), 35)  
**Confidence**: 0.80  

```python
shipment = frappe.new_doc('Shipment')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:24*

### test_shipment_from_delivery_note

**Category**: instantiation  
**Description**: Instantiate create_test_shipment: test shipment from delivery note  
**Expected**: self.assertEqual(second_shipment.value_of_goods, delivery_note.grand_total)  
**Confidence**: 0.80  

```python
shipment = create_test_shipment([delivery_note])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/shipment/test_shipment.py:16*

### test_get_item_detail_purchase_order

**Category**: instantiation  
**Description**: Instantiate _dict: test get item detail purchase order  
**Expected**: self.assertEqual(details.get('price_list_rate'), 100)  
**Confidence**: 0.80  

```python
args = frappe._dict({'item_code': '_Test Item', 'company': '_Test Company', 'customer': '_Test Customer', 'conversion_rate': 1.0, 'price_list_currency': 'USD', 'plc_conversion_rate': 1.0, 'doctype': 'Purchase Order', 'name': None, 'supplier': '_Test Supplier', 'transaction_date': None, 'price_list': '_Test Buying Price List', 'is_subcontracted': 0, 'ignore_pricing_rule': 1, 'qty': 1})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:11*

### test_get_item_detail_purchase_order

**Category**: instantiation  
**Description**: Instantiate get_item_details: test get item detail purchase order  
**Expected**: self.assertEqual(details.get('price_list_rate'), 100)  
**Confidence**: 0.80  

```python
details = get_item_details(args)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:29*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test fetch price from list rate on doc save  
**Expected**: self.assertIsNone(dn.items[0].batch_no)  
**Confidence**: 0.80  

```python
so = make_sales_order(item_code=item.item_code, qty=2, rate=75)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:80*

### test_fetch_price_from_list_rate_on_doc_save

**Category**: instantiation  
**Description**: Instantiate make_delivery_note: test fetch price from list rate on doc save  
**Expected**: self.assertIsNone(dn.items[0].batch_no)  
**Confidence**: 0.80  

```python
dn = make_delivery_note(so.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/tests/test_get_item_details.py:84*

### test_template_item_price

**Category**: instantiation  
**Description**: Instantiate make_item: test template item price  
**Expected**: self.assertRaises(frappe.ValidationError, doc.save)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

item = make_item('Test Template Item 1', {'has_variants': 1, 'variant_based_on': 'Manufacturer'})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:22*

### test_template_item_price

**Category**: instantiation  
**Description**: Instantiate get_doc: test template item price  
**Expected**: self.assertRaises(frappe.ValidationError, doc.save)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

doc = frappe.get_doc({'doctype': 'Item Price', 'price_list': '_Test Price List', 'item_code': item.name, 'price_list_rate': 100})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:30*

### test_duplicate_item

**Category**: instantiation  
**Description**: Instantiate copy_doc: test duplicate item  
**Expected**: self.assertRaises(ItemPriceDuplicateItem, doc.save)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

doc = frappe.copy_doc(self.globalTestRecords['Item Price'][0])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:42*

### test_dates_validation_error

**Category**: instantiation  
**Description**: Instantiate copy_doc: test dates validation error  
**Expected**: self.assertRaises(frappe.ValidationError, doc.save)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

doc = frappe.copy_doc(self.globalTestRecords['Item Price'][1])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:63*

### test_price_in_a_qty

**Category**: instantiation  
**Description**: Instantiate copy_doc: test price in a qty  
**Expected**: self.assertEqual(price, 20.0)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

doc = frappe.copy_doc(self.globalTestRecords['Item Price'][2])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:72*

### test_price_in_a_qty

**Category**: instantiation  
**Description**: Instantiate ItemDetailsCtx: test price in a qty  
**Expected**: self.assertEqual(price, 20.0)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.sql('delete from `tabItem Price`')
make_test_records_for_doctype('Item Price', force=True)

ctx = ItemDetailsCtx({'price_list': doc.price_list, 'customer': doc.customer, 'uom': '_Test UOM', 'transaction_date': '2017-04-18', 'qty': 10})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_price/test_item_price.py:74*

### test_numeric_item_attribute

**Category**: instantiation  
**Description**: Instantiate get_doc: test numeric item attribute  
**Expected**: self.assertRaises(ItemAttributeIncrementError, item_attribute.save)  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
if frappe.db.exists('Item Attribute', '_Test_Length'):
    frappe.delete_doc('Item Attribute', '_Test_Length')

item_attribute = frappe.get_doc({'doctype': 'Item Attribute', 'attribute_name': '_Test_Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_attribute/test_item_attribute.py:18*

### test_numeric_item_attribute

**Category**: instantiation  
**Description**: Instantiate get_doc: test numeric item attribute  
**Expected**: self.assertRaises(ItemAttributeIncrementError, item_attribute.save)  
**Confidence**: 0.80  

```python
item_attribute = frappe.get_doc({'doctype': 'Item Attribute', 'attribute_name': '_Test_Length', 'numeric_values': 1, 'from_range': 0.0, 'to_range': 100.0, 'increment': 0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/item_attribute/test_item_attribute.py:18*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate get_doc: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:18*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate get_doc: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:21*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate _create_bin: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin = _create_bin(item_code, warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:26*

### test_index_exists

**Category**: instantiation  
**Description**: Instantiate sql: test index exists  
**Confidence**: 0.80  

```python
indexes = frappe.db.sql('show index from tabBin where Non_unique = 0', as_dict=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:32*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate get_doc: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin1 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:18*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate get_doc: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin2 = frappe.get_doc(doctype='Bin', item_code=item_code, warehouse=warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:21*

### test_concurrent_inserts

**Category**: instantiation  
**Description**: Instantiate _create_bin: Ensure no duplicates are possible in case of concurrent inserts  
**Expected**: self.assertEqual(bin.item_code, item_code)  
**Confidence**: 0.80  

```python
bin = _create_bin(item_code, warehouse)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:26*

### test_index_exists

**Category**: instantiation  
**Description**: Instantiate sql: test index exists  
**Confidence**: 0.80  

```python
indexes = frappe.db.sql('show index from tabBin where Non_unique = 0', as_dict=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/bin/test_bin.py:32*

### test_reserved_stock_report

**Category**: instantiation  
**Description**: Instantiate reserved_stock_report: test reserved stock report  
**Expected**: self.assertEqual(len(data), len(items_details))  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
self.stock_qty = 100
self.warehouse = '_Test Warehouse - _TC'

data = reserved_stock_report(filters={'company': so.company, 'from_date': today(), 'to_date': today()})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/reserved_stock/test_reserved_stock.py:46*

### test_reserved_stock_report

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test reserved stock report  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
self.stock_qty = 100
self.warehouse = '_Test Warehouse - _TC'

so = make_sales_order(item_code=item_code, qty=randint(11, 100), warehouse=self.warehouse, uom=properties.stock_uom)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/reserved_stock/test_reserved_stock.py:41*

### test_reserved_stock_report

**Category**: instantiation  
**Description**: Instantiate reserved_stock_report: test reserved stock report  
**Expected**: self.assertEqual(len(data), len(items_details))  
**Confidence**: 0.80  

```python
data = reserved_stock_report(filters={'company': so.company, 'from_date': today(), 'to_date': today()})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/reserved_stock/test_reserved_stock.py:46*

### test_reserved_stock_report

**Category**: instantiation  
**Description**: Instantiate make_sales_order: test reserved stock report  
**Confidence**: 0.80  

```python
so = make_sales_order(item_code=item_code, qty=randint(11, 100), warehouse=self.warehouse, uom=properties.stock_uom)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/reserved_stock/test_reserved_stock.py:41*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate create_delivery_note: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
dn = create_delivery_note(item_code=items[0], qty=2, do_not_save=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:21*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
ps1 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:37*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
ps2 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:53*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
ps3 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:91*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, dn.submit)  
**Confidence**: 0.80  

```python
ps4 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:98*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate create_delivery_note: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
dn = create_delivery_note(item_code=items[0], qty=2, do_not_save=True)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:21*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
ps1 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:37*

### test_packing_slip

**Category**: instantiation  
**Description**: Instantiate make_packing_slip: test packing slip  
**Expected**: self.assertRaises(frappe.exceptions.ValidationError, ps3.save)  
**Confidence**: 0.80  

```python
ps2 = make_packing_slip(dn.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/packing_slip/test_packing_slip.py:53*

### test_stock_entry_type_non_standard

**Category**: instantiation  
**Description**: Instantiate get_doc: test stock entry type non standard  
**Expected**: self.assertRaises(frappe.ValidationError, doc.insert)  
**Confidence**: 0.80  

```python
doc = frappe.get_doc({'doctype': 'Stock Entry Type', '__newname': stock_entry_type, 'purpose': 'Manufacture', 'is_standard': 1})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry_type/test_stock_entry_type.py:12*

### test_stock_entry_type_non_standard

**Category**: instantiation  
**Description**: Instantiate get_doc: test stock entry type non standard  
**Expected**: self.assertRaises(frappe.ValidationError, doc.insert)  
**Confidence**: 0.80  

```python
doc = frappe.get_doc({'doctype': 'Stock Entry Type', '__newname': stock_entry_type, 'purpose': 'Manufacture', 'is_standard': 1})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_entry_type/test_stock_entry_type.py:12*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_doc: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 10)  
**Confidence**: 0.80  

```python
# Setup
item = create_item('_Test Item with Serial No', is_stock_item=1)
item.has_serial_no = 1
item.serial_no_series = 'TEST.###'
item.save(ignore_permissions=True)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='_Test Item With Serial No')

report = frappe.get_doc('Report', 'Available Serial No')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:31*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_data: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 10)  
**Confidence**: 0.80  

```python
# Setup
item = create_item('_Test Item with Serial No', is_stock_item=1)
item.has_serial_no = 1
item.serial_no_series = 'TEST.###'
item.save(ignore_permissions=True)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='_Test Item With Serial No')

data = report.get_data(filters=self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:34*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_data: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 5)  
**Confidence**: 0.80  

```python
# Setup
item = create_item('_Test Item with Serial No', is_stock_item=1)
item.has_serial_no = 1
item.serial_no_series = 'TEST.###'
item.save(ignore_permissions=True)
self.filters = frappe._dict(company='_Test Company', from_date=today(), to_date=add_days(today(), 30), item_code='_Test Item With Serial No')

data = report.get_data(filters=self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:41*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_doc: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 10)  
**Confidence**: 0.80  

```python
report = frappe.get_doc('Report', 'Available Serial No')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:31*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_data: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 10)  
**Confidence**: 0.80  

```python
data = report.get_data(filters=self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:34*

### test_available_serial_no

**Category**: instantiation  
**Description**: Instantiate get_data: test available serial no  
**Expected**: self.assertEqual(len(serial_nos), 5)  
**Confidence**: 0.80  

```python
data = report.get_data(filters=self.filters)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/available_serial_no/test_available_serial_no.py:41*

### test_settings

**Category**: instantiation  
**Description**: Instantiate get_single: test settings  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Stock Settings', 'clean_description_html', 0)

settings = frappe.get_single('Stock Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:22*

### test_clean_html

**Category**: instantiation  
**Description**: Instantiate get_single: test clean html  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.80  

```python
# Setup
super().setUp()
frappe.db.set_single_value('Stock Settings', 'clean_description_html', 0)

settings = frappe.get_single('Stock Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:36*

### test_settings

**Category**: instantiation  
**Description**: Instantiate get_single: test settings  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.80  

```python
settings = frappe.get_single('Stock Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:22*

### test_clean_html

**Category**: instantiation  
**Description**: Instantiate get_single: test clean html  
**Expected**: self.assertEqual(item.description, '<p>Drawing No. 07-xxx-PO132<br>1800 x 1685 x 750<br>All parts made of Marine Ply<br>Top w/ Corian dd<br>CO, CS, VIP Day Cabin</p>')  
**Confidence**: 0.80  

```python
settings = frappe.get_single('Stock Settings')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/doctype/stock_settings/test_stock_settings.py:36*

### test_item_shortage_report

**Category**: config  
**Description**: Configuration example: test item shortage report  
**Expected**: self.assertIn(item, item_code_list)  
**Confidence**: 0.75  

```python
filters = {'company': so.company, 'warehouse': [so.items[0].warehouse]}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:37*

### test_item_shortage_report

**Category**: config  
**Description**: Configuration example: test item shortage report  
**Expected**: self.assertNotIn(item, item_code_list)  
**Confidence**: 0.75  

```python
filters = {'company': so.company, 'warehouse': ['Work In Progress - _TC']}
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/stock/report/item_shortage_report/test_item_shortage_report.py:45*

