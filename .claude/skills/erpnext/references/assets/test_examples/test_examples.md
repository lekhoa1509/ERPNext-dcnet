# Test Example Extraction Report

**Total Examples**: 84  
**High Value Examples** (confidence > 0.7): 84  
**Average Complexity**: 0.74  

## Examples by Category

- **instantiation**: 14
- **method_call**: 16
- **workflow**: 54

## Examples by Language

- **Python**: 84

## Extracted Examples

### test_capitalization_with_wip_composite_asset

**Category**: workflow  
**Description**: Workflow: test capitalization with wip composite asset  
**Expected**: self.assertFalse(get_actual_sle_dict(asset_capitalization.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
stock_rate = 1000
stock_qty = 2
stock_amount = 2000
total_amount = 2000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', stock_qty=stock_qty, stock_rate=stock_rate, service_expense_account='Expenses Included In Asset Valuation - TCP1', company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
self.assertEqual(asset_capitalization.total_value, total_amount)
self.assertEqual(asset_capitalization.target_incoming_rate, total_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
self.assertEqual(target_asset.status, 'Work In Progress')
expected_gle = {'_Test Fixed Asset - TCP1': 2000, '_Test Warehouse - TCP1': -2000}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
expected_sle = {('Capitalization Source Stock Item', '_Test Warehouse - TCP1'): {'actual_qty': -stock_qty, 'stock_value_difference': -stock_amount}}
actual_sle = get_actual_sle_dict(asset_capitalization.name)
self.assertEqual(actual_sle, expected_sle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:226*

### test_capitalize_only_service_item

**Category**: workflow  
**Description**: Workflow: test capitalize only service item  
**Expected**: self.assertFalse(get_actual_sle_dict(asset_capitalization.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

company = '_Test Company'
service_rate = 500
service_qty = 2
service_amount = 1000
total_amount = 1000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', service_qty=service_qty, service_rate=service_rate, service_expense_account='Expenses Included In Asset Valuation - _TC', company=company, submit=1)
self.assertEqual(asset_capitalization.service_items[0].amount, service_amount)
self.assertEqual(asset_capitalization.service_items_total, service_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
expected_gle = {'CWIP Account - _TC': 1000.0, 'Expenses Included In Asset Valuation - _TC': -1000.0}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:300*

### test_capitalize_composite_component

**Category**: workflow  
**Description**: Workflow: test capitalize composite component  
**Expected**: self.assertEqual(actual_gle, {})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
consumed_asset_value = 100000
consumed_asset = create_asset(asset_name='Asset Capitalization Consumable Asset', asset_value=consumed_asset_value, submit=1, warehouse='Stores - _TC', is_composite_component=1, company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', consumed_asset=consumed_asset.name, company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, {})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:348*

### test_capitalization_with_wip_composite_asset

**Category**: workflow  
**Description**: Workflow: test capitalization with wip composite asset  
**Expected**: self.assertFalse(get_actual_sle_dict(asset_capitalization.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
stock_rate = 1000
stock_qty = 2
stock_amount = 2000
total_amount = 2000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', stock_qty=stock_qty, stock_rate=stock_rate, service_expense_account='Expenses Included In Asset Valuation - TCP1', company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
self.assertEqual(asset_capitalization.total_value, total_amount)
self.assertEqual(asset_capitalization.target_incoming_rate, total_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
self.assertEqual(target_asset.status, 'Work In Progress')
expected_gle = {'_Test Fixed Asset - TCP1': 2000, '_Test Warehouse - TCP1': -2000}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
expected_sle = {('Capitalization Source Stock Item', '_Test Warehouse - TCP1'): {'actual_qty': -stock_qty, 'stock_value_difference': -stock_amount}}
actual_sle = get_actual_sle_dict(asset_capitalization.name)
self.assertEqual(actual_sle, expected_sle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:226*

### test_capitalize_only_service_item

**Category**: workflow  
**Description**: Workflow: test capitalize only service item  
**Expected**: self.assertFalse(get_actual_sle_dict(asset_capitalization.name))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company'
service_rate = 500
service_qty = 2
service_amount = 1000
total_amount = 1000
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', service_qty=service_qty, service_rate=service_rate, service_expense_account='Expenses Included In Asset Valuation - _TC', company=company, submit=1)
self.assertEqual(asset_capitalization.service_items[0].amount, service_amount)
self.assertEqual(asset_capitalization.service_items_total, service_amount)
target_asset = frappe.get_doc('Asset', asset_capitalization.target_asset)
self.assertEqual(target_asset.net_purchase_amount, total_amount)
self.assertEqual(target_asset.purchase_amount, total_amount)
expected_gle = {'CWIP Account - _TC': 1000.0, 'Expenses Included In Asset Valuation - _TC': -1000.0}
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, expected_gle)
asset_capitalization.cancel()
self.assertFalse(get_actual_gle_dict(asset_capitalization.name))
self.assertFalse(get_actual_sle_dict(asset_capitalization.name))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:300*

### test_capitalize_composite_component

**Category**: workflow  
**Description**: Workflow: test capitalize composite component  
**Expected**: self.assertEqual(actual_gle, {})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
company = '_Test Company with perpetual inventory'
set_depreciation_settings_in_company(company=company)
name = frappe.db.get_value('Asset Category Account', filters={'parent': 'Computers', 'company_name': company}, fieldname=['name'])
frappe.db.set_value('Asset Category Account', name, 'capital_work_in_progress_account', '')
wip_composite_asset = create_asset(asset_name='Asset Capitalization WIP Composite Asset', is_composite_asset=1, warehouse='Stores - TCP1', company=company)
consumed_asset_value = 100000
consumed_asset = create_asset(asset_name='Asset Capitalization Consumable Asset', asset_value=consumed_asset_value, submit=1, warehouse='Stores - _TC', is_composite_component=1, company=company)
asset_capitalization = create_asset_capitalization(target_asset=wip_composite_asset.name, target_asset_location='Test Location', consumed_asset=consumed_asset.name, company=company, submit=1)
self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)
actual_gle = get_actual_gle_dict(asset_capitalization.name)
self.assertEqual(actual_gle, {})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:348*

### test_available_for_use_date_is_after_purchase_date

**Category**: workflow  
**Description**: Workflow: test available for use date is after purchase date  
**Expected**: self.assertRaises(frappe.ValidationError, asset.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, do_not_save=1)
asset.is_existing_asset = 0
asset.purchase_date = getdate('2021-10-10')
asset.available_for_use_date = getdate('2021-10-1')
self.assertRaises(frappe.ValidationError, asset.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:80*

### test_validate_item

**Category**: workflow  
**Description**: Workflow: test validate item  
**Expected**: self.assertRaises(frappe.ValidationError, asset.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(item_code='MacBook Pro', do_not_save=1)
item = frappe.get_doc('Item', 'MacBook Pro')
item.disabled = 1
item.save()
self.assertRaises(frappe.ValidationError, asset.save)
item.disabled = 0
item.is_fixed_asset = 0
self.assertRaises(frappe.ValidationError, asset.save)
item.is_fixed_asset = 1
item.is_stock_item = 1
self.assertRaises(frappe.ValidationError, asset.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:93*

### test_purchase_asset

**Category**: workflow  
**Description**: Workflow: test purchase asset  
**Expected**: self.assertEqual(asset.docstatus, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset.available_for_use_date = purchase_date
asset.purchase_date = purchase_date
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset.submit()
pi = make_invoice(pr.name)
pi.supplier = '_Test Supplier'
pi.insert()
pi.submit()
asset.load_from_db()
self.assertEqual(asset.supplier, '_Test Supplier')
self.assertEqual(asset.purchase_date, getdate(purchase_date))
self.assertEqual(asset.purchase_receipt, pr.name)
expected_gle = (('Asset Received But Not Billed - _TC', 100000.0, 0.0), ('Creditors - _TC', 0.0, 100000.0))
gle = get_gl_entries('Purchase Invoice', pi.name)
self.assertSequenceEqual(gle, expected_gle)
pi.cancel()
asset.cancel()
asset.load_from_db()
pr.load_from_db()
pr.cancel()
self.assertEqual(asset.docstatus, 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:109*

### test_purchase_of_grouped_asset

**Category**: workflow  
**Description**: Workflow: test purchase of grouped asset  
**Expected**: asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
create_fixed_asset_item('Rack', is_grouped_asset=1)
pr = make_purchase_receipt(item_code='Rack', qty=3, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
self.assertEqual(asset.asset_quantity, 3)
asset.calculate_depreciation = 1
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset.available_for_use_date = purchase_date
asset.purchase_date = purchase_date
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:158*

### test_is_fixed_asset_set

**Category**: workflow  
**Description**: Workflow: test is fixed asset set  
**Expected**: self.assertEqual(doc.items[0].is_fixed_asset, 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(is_existing_asset=1)
doc = frappe.new_doc('Purchase Invoice')
doc.company = '_Test Company'
doc.supplier = '_Test Supplier'
doc.append('items', {'item_code': 'Macbook Pro', 'qty': 1, 'asset': asset.name})
doc.set_missing_values()
self.assertEqual(doc.items[0].is_fixed_asset, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:184*

### test_gle_made_by_asset_sale

**Category**: workflow  
**Description**: Workflow: test gle made by asset sale  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
post_depreciation_entries(date=add_months(purchase_date, 2))
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
asset.load_from_db()
accumulated_depr_amount = flt(asset.net_purchase_amount - asset.finance_books[0].value_after_depreciation, asset.precision('net_purchase_amount'))
pro_rata_amount = flt(accumulated_depr_amount - 18000)
expected_gle = (('_Test Accumulated Depreciations - _TC', flt(accumulated_depr_amount, asset.precision('net_purchase_amount')), 0.0), ('_Test Fixed Asset - _TC', 0.0, 100000.0), ('_Test Gain/Loss on Asset Disposal - _TC', flt(57000.0 - pro_rata_amount, asset.precision('net_purchase_amount')), 0.0), ('Debtors - _TC', 25000.0, 0.0))
gle = get_gl_entries('Sales Invoice', si.name)
self.assertSequenceEqual(gle, expected_gle)
si.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:313*

### test_gle_made_by_asset_sale_for_existing_asset

**Category**: workflow  
**Description**: Workflow: test gle made by asset sale for existing asset  
**Expected**: self.assertSequenceEqual(gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.accounts.doctype.sales_invoice.test_sales_invoice import create_sales_invoice
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-04-01', purchase_date='2020-04-01', expected_value_after_useful_life=0, total_number_of_depreciations=5, opening_number_of_booked_depreciations=2, frequency_of_depreciation=12, depreciation_start_date='2023-03-31', opening_accumulated_depreciation=24000, net_purchase_amount=60000, submit=1)
expected_depr_values = [['2023-03-31', 12000, 36000], ['2024-03-31', 12000, 48000], ['2025-03-31', 12000, 60000]]
first_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
for i, schedule in enumerate(first_asset_depr_schedule):
    self.assertEqual(getdate(expected_depr_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_depr_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_depr_values[i][2], schedule.accumulated_depreciation_amount)
post_depreciation_entries(date='2023-03-31')
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=40000, posting_date=getdate('2023-05-23'))
asset.load_from_db()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
expected_values = [['2023-03-31', 12000, 36000], ['2023-05-23', 1737.7, 37737.7]]
second_asset_depr_schedule = get_depr_schedule(asset.name, 'Active')
for i, schedule in enumerate(second_asset_depr_schedule):
    self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
    self.assertTrue(schedule.journal_entry)
expected_gle = (('_Test Accumulated Depreciations - _TC', 37737.7, 0.0), ('_Test Fixed Asset - _TC', 0.0, 60000.0), ('_Test Gain/Loss on Asset Disposal - _TC', 0.0, 17737.7), ('Debtors - _TC', 40000.0, 0.0))
gle = get_gl_entries('Sales Invoice', si.name)
self.assertSequenceEqual(gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:376*

### test_asset_with_maintenance_required_status_after_sale

**Category**: workflow  
**Description**: Workflow: test asset with maintenance required status after sale  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2020-06-06', purchase_date='2020-01-01', expected_value_after_useful_life=10000, total_number_of_depreciations=3, frequency_of_depreciation=10, maintenance_required=1, depreciation_start_date='2020-12-31', submit=1)
post_depreciation_entries(date='2021-01-01')
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = nowdate()
si.get('items')[0].rate = 25000
si.insert()
si.submit()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
update_maintenance_status()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:447*

### test_cwip_accounting

**Category**: workflow  
**Description**: Workflow: test cwip accounting  
**Expected**: self.assertSequenceEqual(gle, expected_gle)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=5000, do_not_submit=True, location='Test Location')
pr.set('taxes', [{'category': 'Total', 'add_deduct_tax': 'Add', 'charge_type': 'On Net Total', 'account_head': '_Test Account Service Tax - _TC', 'description': '_Test Account Service Tax', 'cost_center': 'Main - _TC', 'rate': 5.0}, {'category': 'Valuation and Total', 'add_deduct_tax': 'Add', 'charge_type': 'On Net Total', 'account_head': '_Test Account Shipping Charges - _TC', 'description': '_Test Account Shipping Charges', 'cost_center': 'Main - _TC', 'rate': 5.0}])
pr.submit()
expected_gle = (('_Test Account Shipping Charges - _TC', 0.0, 250.0), ('Asset Received But Not Billed - _TC', 0.0, 5000.0), ('CWIP Account - _TC', 5250.0, 0.0))
pr_gle = get_gl_entries('Purchase Receipt', pr.name)
self.assertSequenceEqual(pr_gle, expected_gle)
pi = make_invoice(pr.name)
pi.submit()
expected_gle = (('_Test Account Service Tax - _TC', 250.0, 0.0), ('_Test Account Shipping Charges - _TC', 250.0, 0.0), ('Asset Received But Not Billed - _TC', 5000.0, 0.0), ('Creditors - _TC', 0.0, 5500.0))
pi_gle = get_gl_entries('Purchase Invoice', pi.name)
self.assertSequenceEqual(pi_gle, expected_gle)
asset = frappe.db.get_value('Asset', {'purchase_receipt': pr.name, 'docstatus': 0}, 'name')
asset_doc = frappe.get_doc('Asset', asset)
month_end_date = get_last_day(nowdate())
asset_doc.available_for_use_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
self.assertEqual(asset_doc.net_purchase_amount, 5250.0)
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset_doc.submit()
expected_gle = (('_Test Fixed Asset - _TC', 5250.0, 0.0), ('CWIP Account - _TC', 0.0, 5250.0))
gle = get_gl_entries('Asset', asset_doc.name)
self.assertSequenceEqual(gle, expected_gle)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:548*

### test_partial_asset_sale

**Category**: workflow  
**Description**: Workflow: test partial asset sale  
**Expected**: self.assertEqual(asset_depr_schedule_after_sale.depreciation_schedule[0].get('depreciation_amount'), 41666.66)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
depreciation_start_date = add_months(get_last_day(date), -2)
asset = create_asset(item_code='Macbook Pro', is_existing_asset=1, calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, depreciation_start_date=depreciation_start_date, net_purchase_amount=1000000.0, purchase_amount=1000000.0, asset_quantity=10, total_number_of_depreciations=12, frequency_of_depreciation=1, submit=1)
asset_depr_schedule_before_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
post_depreciation_entries(date)
asset.reload()
self.assertEqual(asset.asset_quantity, 10)
self.assertEqual(asset.net_purchase_amount, 1000000)
self.assertEqual(asset.status, 'Partially Depreciated')
self.assertEqual(asset_depr_schedule_before_sale.depreciation_schedule[0].get('depreciation_amount'), 83333.33)
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=5)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
asset.reload()
asset_depr_schedule_after_sale = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(asset.asset_quantity, 5)
self.assertEqual(asset.net_purchase_amount, 500000)
self.assertEqual(asset.status, 'Sold')
self.assertEqual(asset_depr_schedule_after_sale.depreciation_schedule[0].get('depreciation_amount'), 41666.66)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset/test_asset.py:704*

### test_movement

**Category**: workflow  
**Description**: Workflow: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
asset.available_for_use_date = '2020-06-06'
asset.purchase_date = '2020-06-06'
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
if asset.docstatus == 0:
    asset.submit()
if not frappe.db.exists('Location', 'Test Location 2'):
    frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
employee = make_employee('testassetmovemp@example.com', company='_Test Company')
create_asset_movement(purpose='Issue', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'to_employee': employee}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)
create_asset_movement(purpose='Receipt', company=asset.company, assets=[{'asset': asset.name, 'from_employee': employee, 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:21*

### test_last_movement_cancellation

**Category**: workflow  
**Description**: Workflow: test last movement cancellation  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
asset.available_for_use_date = '2020-06-06'
asset.purchase_date = '2020-06-06'
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
if asset.docstatus == 0:
    asset.submit()
if not frappe.db.exists('Location', 'Test Location 2'):
    frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
movement = frappe.get_doc({'doctype': 'Asset Movement', 'reference_name': pr.name})
self.assertRaises(frappe.ValidationError, movement.cancel)
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:104*

### test_movement

**Category**: workflow  
**Description**: Workflow: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
asset.available_for_use_date = '2020-06-06'
asset.purchase_date = '2020-06-06'
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
if asset.docstatus == 0:
    asset.submit()
if not frappe.db.exists('Location', 'Test Location 2'):
    frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
employee = make_employee('testassetmovemp@example.com', company='_Test Company')
create_asset_movement(purpose='Issue', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'to_employee': employee}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)
create_asset_movement(purpose='Receipt', company=asset.company, assets=[{'asset': asset.name, 'from_employee': employee, 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:21*

### test_last_movement_cancellation

**Category**: workflow  
**Description**: Workflow: test last movement cancellation  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset = frappe.get_doc('Asset', asset_name)
asset.calculate_depreciation = 1
asset.available_for_use_date = '2020-06-06'
asset.purchase_date = '2020-06-06'
asset.append('finance_books', {'expected_value_after_useful_life': 10000, 'next_depreciation_date': '2020-12-31', 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10})
if asset.docstatus == 0:
    asset.submit()
if not frappe.db.exists('Location', 'Test Location 2'):
    frappe.get_doc({'doctype': 'Location', 'location_name': 'Test Location 2'}).insert()
movement = frappe.get_doc({'doctype': 'Asset Movement', 'reference_name': pr.name})
self.assertRaises(frappe.ValidationError, movement.cancel)
movement1 = create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:104*

### test_current_asset_value

**Category**: workflow  
**Description**: Workflow: test current asset value  
**Expected**: self.assertEqual(current_value, 100000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset_doc.available_for_use_date = purchase_date
asset_doc.purchase_date = purchase_date
asset_doc.calculate_depreciation = 1
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset_doc.submit()
current_value = get_asset_value_after_depreciation(asset_doc.name)
self.assertEqual(current_value, 100000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:25*

### test_asset_depreciation_value_adjustment

**Category**: workflow  
**Description**: Workflow: test asset depreciation value adjustment  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=120000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
post_depreciation_entries(getdate('2023-08-21'))
current_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_value, new_asset_value=50000.0, date='2023-08-21')
adj_doc.submit()
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
expected_gle = (('_Test Difference Account - _TC', 4625.29, 0.0), ('_Test Fixed Asset - _TC', 0.0, 4625.29))
gle = frappe.db.sql("select account, debit, credit from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\torder by account", adj_doc.journal_entry)
self.assertSequenceEqual(gle, expected_gle)
expected_schedules = [['2023-01-31', 5474.73, 5474.73], ['2023-02-28', 9983.33, 15458.06], ['2023-03-31', 9983.33, 25441.39], ['2023-04-30', 9983.33, 35424.72], ['2023-05-31', 9983.33, 45408.05], ['2023-06-30', 9983.33, 55391.38], ['2023-07-31', 9983.33, 65374.71], ['2023-08-31', 9070.36, 74445.07], ['2023-09-30', 9070.36, 83515.43], ['2023-10-31', 9070.36, 92585.79], ['2023-11-30', 9070.36, 101656.15], ['2023-12-31', 9070.36, 110726.51], ['2024-01-15', 4448.2, 115174.71]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in second_asset_depr_schedule.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:52*

### test_difference_amount

**Category**: workflow  
**Description**: Workflow: test difference amount  
**Expected**: self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
adj_doc.submit()
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
self.assertEqual(difference_amount, -60000)
asset_doc.load_from_db()
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:267*

### test_expected_value_after_useful_life

**Category**: workflow  
**Description**: Workflow: test expected value after useful life  
**Expected**: self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 2000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 5000, 'salvage_value_percentage': 5, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 5000.0)
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
adj_doc.submit()
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
self.assertEqual(difference_amount, -60000)
asset_doc.load_from_db()
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 2000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:301*

### test_current_asset_value

**Category**: workflow  
**Description**: Workflow: test current asset value  
**Expected**: self.assertEqual(current_value, 100000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
asset_doc.available_for_use_date = purchase_date
asset_doc.purchase_date = purchase_date
asset_doc.calculate_depreciation = 1
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
asset_doc.submit()
current_value = get_asset_value_after_depreciation(asset_doc.name)
self.assertEqual(current_value, 100000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:25*

### test_asset_depreciation_value_adjustment

**Category**: workflow  
**Description**: Workflow: test asset depreciation value adjustment  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=120000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
post_depreciation_entries(getdate('2023-08-21'))
current_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_value, new_asset_value=50000.0, date='2023-08-21')
adj_doc.submit()
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset_doc.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
expected_gle = (('_Test Difference Account - _TC', 4625.29, 0.0), ('_Test Fixed Asset - _TC', 0.0, 4625.29))
gle = frappe.db.sql("select account, debit, credit from `tabGL Entry`\n\t\t\twhere voucher_type='Journal Entry' and voucher_no = %s\n\t\t\torder by account", adj_doc.journal_entry)
self.assertSequenceEqual(gle, expected_gle)
expected_schedules = [['2023-01-31', 5474.73, 5474.73], ['2023-02-28', 9983.33, 15458.06], ['2023-03-31', 9983.33, 25441.39], ['2023-04-30', 9983.33, 35424.72], ['2023-05-31', 9983.33, 45408.05], ['2023-06-30', 9983.33, 55391.38], ['2023-07-31', 9983.33, 65374.71], ['2023-08-31', 9070.36, 74445.07], ['2023-09-30', 9070.36, 83515.43], ['2023-10-31', 9070.36, 92585.79], ['2023-11-30', 9070.36, 101656.15], ['2023-12-31', 9070.36, 110726.51], ['2024-01-15', 4448.2, 115174.71]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in second_asset_depr_schedule.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:52*

### test_difference_amount

**Category**: workflow  
**Description**: Workflow: test difference amount  
**Expected**: self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
adj_doc.submit()
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
self.assertEqual(difference_amount, -60000)
asset_doc.load_from_db()
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:267*

### test_expected_value_after_useful_life

**Category**: workflow  
**Description**: Workflow: test expected value after useful life  
**Expected**: self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 2000.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
pr = make_purchase_receipt(item_code='Macbook Pro', qty=1, rate=100000.0, location='Test Location')
asset_name = frappe.db.get_value('Asset', {'purchase_receipt': pr.name}, 'name')
asset_doc = frappe.get_doc('Asset', asset_name)
asset_doc.calculate_depreciation = 1
asset_doc.available_for_use_date = '2023-01-15'
asset_doc.purchase_date = '2023-01-15'
asset_doc.append('finance_books', {'expected_value_after_useful_life': 5000, 'salvage_value_percentage': 5, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 12, 'frequency_of_depreciation': 1, 'depreciation_start_date': '2023-01-31'})
asset_doc.submit()
self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 5000.0)
current_asset_value = get_asset_value_after_depreciation(asset_doc.name)
adj_doc = make_asset_value_adjustment(asset=asset_doc.name, current_asset_value=current_asset_value, new_asset_value=40000, date='2023-08-21')
adj_doc.submit()
difference_amount = adj_doc.new_asset_value - adj_doc.current_asset_value
self.assertEqual(difference_amount, -60000)
asset_doc.load_from_db()
self.assertEqual(asset_doc.finance_books[0].value_after_depreciation, 40000.0)
self.assertEqual(asset_doc.finance_books[0].expected_value_after_useful_life, 2000.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:301*

### test_asset_shift_allocation

**Category**: workflow  
**Description**: Workflow: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 10000.0, 50000.0, 'Single'], ['2023-06-30', 10000.0, 60000.0, 'Single'], ['2023-07-31', 10000.0, 70000.0, 'Single'], ['2023-08-31', 10000.0, 80000.0, 'Single'], ['2023-09-30', 10000.0, 90000.0, 'Single'], ['2023-10-31', 10000.0, 100000.0, 'Single'], ['2023-11-30', 10000.0, 110000.0, 'Single'], ['2023-12-31', 10000.0, 120000.0, 'Single']]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc({'doctype': 'Asset Shift Allocation', 'asset': asset.name}).insert()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
asset_shift_allocation.depreciation_schedule[4].shift = 'Triple'
asset_shift_allocation.save()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 20000.0, 60000.0, 'Triple'], ['2023-06-30', 10000.0, 70000.0, 'Single'], ['2023-07-31', 10000.0, 80000.0, 'Single'], ['2023-08-31', 10000.0, 90000.0, 'Single'], ['2023-09-30', 10000.0, 100000.0, 'Single'], ['2023-10-31', 10000.0, 110000.0, 'Single'], ['2023-11-30', 10000.0, 120000.0, 'Single']]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation.submit()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:24*

### test_asset_shift_allocation

**Category**: workflow  
**Description**: Workflow: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 10000.0, 50000.0, 'Single'], ['2023-06-30', 10000.0, 60000.0, 'Single'], ['2023-07-31', 10000.0, 70000.0, 'Single'], ['2023-08-31', 10000.0, 80000.0, 'Single'], ['2023-09-30', 10000.0, 90000.0, 'Single'], ['2023-10-31', 10000.0, 100000.0, 'Single'], ['2023-11-30', 10000.0, 110000.0, 'Single'], ['2023-12-31', 10000.0, 120000.0, 'Single']]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc({'doctype': 'Asset Shift Allocation', 'asset': asset.name}).insert()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
asset_shift_allocation.depreciation_schedule[4].shift = 'Triple'
asset_shift_allocation.save()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in asset_shift_allocation.get('depreciation_schedule')]
expected_schedules = [['2023-01-31', 10000.0, 10000.0, 'Single'], ['2023-02-28', 10000.0, 20000.0, 'Single'], ['2023-03-31', 10000.0, 30000.0, 'Single'], ['2023-04-30', 10000.0, 40000.0, 'Single'], ['2023-05-31', 20000.0, 60000.0, 'Triple'], ['2023-06-30', 10000.0, 70000.0, 'Single'], ['2023-07-31', 10000.0, 80000.0, 'Single'], ['2023-08-31', 10000.0, 90000.0, 'Single'], ['2023-09-30', 10000.0, 100000.0, 'Single'], ['2023-10-31', 10000.0, 110000.0, 'Single'], ['2023-11-30', 10000.0, 120000.0, 'Single']]
self.assertEqual(schedules, expected_schedules)
asset_shift_allocation.submit()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount, d.shift] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_schedules)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:24*

### test_create_asset_maintenance_with_log

**Category**: workflow  
**Description**: Workflow: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
self.asset_doc.available_for_use_date = purchase_date
self.asset_doc.purchase_date = purchase_date
self.asset_doc.calculate_depreciation = 1
self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
self.asset_doc.save()
asset_maintenance = frappe.get_doc({'doctype': 'Asset Maintenance', 'asset_name': self.asset_name, 'maintenance_team': 'Team Awesome', 'company': '_Test Company', 'asset_maintenance_tasks': get_maintenance_tasks()}).insert()
next_due_date = calculate_next_due_date(nowdate(), 'Monthly')
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
asset_maintenance_log = frappe.db.get_value('Asset Maintenance Log', {'asset_maintenance': asset_maintenance.name, 'task_name': 'Change Oil'}, 'name')
asset_maintenance_log_doc = frappe.get_doc('Asset Maintenance Log', asset_maintenance_log)
asset_maintenance_log_doc.update({'completion_date': add_days(nowdate(), 2), 'maintenance_status': 'Completed'})
asset_maintenance_log_doc.save()
next_due_date = calculate_next_due_date(asset_maintenance_log_doc.completion_date, 'Monthly')
asset_maintenance.reload()
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:21*

### test_create_asset_maintenance_with_log

**Category**: workflow  
**Description**: Workflow: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
month_end_date = get_last_day(nowdate())
purchase_date = nowdate() if nowdate() != month_end_date else add_days(nowdate(), -15)
self.asset_doc.available_for_use_date = purchase_date
self.asset_doc.purchase_date = purchase_date
self.asset_doc.calculate_depreciation = 1
self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})
self.asset_doc.save()
asset_maintenance = frappe.get_doc({'doctype': 'Asset Maintenance', 'asset_name': self.asset_name, 'maintenance_team': 'Team Awesome', 'company': '_Test Company', 'asset_maintenance_tasks': get_maintenance_tasks()}).insert()
next_due_date = calculate_next_due_date(nowdate(), 'Monthly')
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
asset_maintenance_log = frappe.db.get_value('Asset Maintenance Log', {'asset_maintenance': asset_maintenance.name, 'task_name': 'Change Oil'}, 'name')
asset_maintenance_log_doc = frappe.get_doc('Asset Maintenance Log', asset_maintenance_log)
asset_maintenance_log_doc.update({'completion_date': add_days(nowdate(), 2), 'maintenance_status': 'Completed'})
asset_maintenance_log_doc.save()
next_due_date = calculate_next_due_date(asset_maintenance_log_doc.completion_date, 'Monthly')
asset_maintenance.reload()
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:21*

### test_depreciation_schedule_after_cancelling_asset_repair

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after cancelling asset repair  
**Expected**: self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
expected_depreciation_before_repair = [['2023-01-31', 41.67, 41.67], ['2023-02-28', 41.67, 83.34], ['2023-03-31', 41.67, 125.01], ['2023-04-30', 41.67, 166.68], ['2023-05-31', 41.67, 208.35], ['2023-06-30', 41.67, 250.02], ['2023-07-31', 41.67, 291.69], ['2023-08-31', 41.67, 333.36], ['2023-09-30', 41.67, 375.03], ['2023-10-31', 41.67, 416.7], ['2023-11-30', 41.67, 458.37], ['2023-12-31', 41.63, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-01-31', 50.0, 50.0], ['2023-02-28', 50.0, 100.0], ['2023-03-31', 50.0, 150.0], ['2023-04-30', 50.0, 200.0], ['2023-05-31', 50.0, 250.0], ['2023-06-30', 50.0, 300.0], ['2023-07-31', 50.0, 350.0], ['2023-08-31', 50.0, 400.0], ['2023-09-30', 50.0, 450.0], ['2023-10-31', 50.0, 500.0], ['2023-11-30', 50.0, 550.0], ['2023-12-31', 50.0, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 600)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:377*

### test_depreciation_schedule_after_cancelling_asset_repair_for_6_months_frequency

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after cancelling asset repair for 6 months frequency  
**Expected**: self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-06-30', frequency_of_depreciation=6, total_number_of_depreciations=4, submit=1)
expected_depreciation_before_repair = [['2023-06-30', 125.0, 125.0], ['2023-12-31', 125.0, 250.0], ['2024-06-30', 125.0, 375.0], ['2024-12-31', 125.0, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-06-30', 150.0, 150.0], ['2023-12-31', 150.0, 300.0], ['2024-06-30', 150.0, 450.0], ['2024-12-31', 150.0, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 600)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:457*

### test_depreciation_schedule_after_cancelling_asset_repair_for_existing_asset

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after cancelling asset repair for existing asset  
**Expected**: self.assertEqual(asset.finance_books[0].value_after_depreciation, 435.48)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-15', depreciation_start_date='2023-03-31', frequency_of_depreciation=1, total_number_of_depreciations=12, is_existing_asset=1, opening_accumulated_depreciation=64.52, opening_number_of_booked_depreciations=2, submit=1)
expected_depreciation_before_repair = [['2023-03-31', 41.39, 105.91], ['2023-04-30', 41.39, 147.3], ['2023-05-31', 41.39, 188.69], ['2023-06-30', 41.39, 230.08], ['2023-07-31', 41.39, 271.47], ['2023-08-31', 41.39, 312.86], ['2023-09-30', 41.39, 354.25], ['2023-10-31', 41.39, 395.64], ['2023-11-30', 41.39, 437.03], ['2023-12-31', 41.39, 478.42], ['2024-01-15', 21.58, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-03-31', 50.9, 115.42], ['2023-04-30', 50.9, 166.32], ['2023-05-31', 50.9, 217.22], ['2023-06-30', 50.9, 268.12], ['2023-07-31', 50.9, 319.02], ['2023-08-31', 50.9, 369.92], ['2023-09-30', 50.9, 420.82], ['2023-10-31', 50.9, 471.72], ['2023-11-30', 50.9, 522.62], ['2023-12-31', 50.9, 573.52], ['2024-01-15', 26.48, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 435.48)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:522*

### test_wdv_depreciation_schedule_after_cancelling_asset_repair

**Category**: workflow  
**Description**: Workflow: test wdv depreciation schedule after cancelling asset repair  
**Expected**: self.assertEqual(schedules, expected_depreciation_before_repair)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Written Down Value', available_for_use_date='2023-04-01', depreciation_start_date='2023-12-31', frequency_of_depreciation=12, total_number_of_depreciations=4, rate_of_depreciation=40, submit=1)
expected_depreciation_before_repair = [['2023-12-31', 150.68, 150.68], ['2024-12-31', 139.73, 290.41], ['2025-12-31', 83.84, 374.25], ['2026-12-31', 50.3, 424.55], ['2027-04-01', 75.45, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2024-01-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
expected_depreciation_after_repair = [['2023-12-31', 180.82, 180.82], ['2024-12-31', 167.67, 348.49], ['2025-12-31', 100.6, 449.09], ['2026-12-31', 60.36, 509.45], ['2027-04-01', 90.55, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:601*

### test_daily_prorata_based_depreciation_schedule_after_cancelling_asset_repair

**Category**: workflow  
**Description**: Workflow: test daily prorata based depreciation schedule after cancelling asset repair  
**Expected**: self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', daily_prorata_based=1, frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
expected_depreciation_before_repair = [['2023-01-31', 42.47, 42.47], ['2023-02-28', 38.36, 80.83], ['2023-03-31', 42.47, 123.3], ['2023-04-30', 41.1, 164.4], ['2023-05-31', 42.47, 206.87], ['2023-06-30', 41.1, 247.97], ['2023-07-31', 42.47, 290.44], ['2023-08-31', 42.47, 332.91], ['2023-09-30', 41.1, 374.01], ['2023-10-31', 42.47, 416.48], ['2023-11-30', 41.1, 457.58], ['2023-12-31', 42.42, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2023-04-01', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2023-01-31', 50.96, 50.96], ['2023-02-28', 46.03, 96.99], ['2023-03-31', 50.96, 147.95], ['2023-04-30', 49.32, 197.27], ['2023-05-31', 50.96, 248.23], ['2023-06-30', 49.32, 297.55], ['2023-07-31', 50.96, 348.51], ['2023-08-31', 50.96, 399.47], ['2023-09-30', 49.32, 448.79], ['2023-10-31', 50.96, 499.75], ['2023-11-30', 49.32, 549.07], ['2023-12-31', 50.93, 600.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 600)
asset_repair.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_repair)
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 500)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:662*

### test_depreciation_schedule_after_cancelling_asset_value_adjustent

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after cancelling asset value adjustent  
**Expected**: self.assertEqual(schedules, expected_depreciation_before_adjustment)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=1000, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-01', depreciation_start_date='2023-01-31', frequency_of_depreciation=1, total_number_of_depreciations=12, submit=1)
expected_depreciation_before_adjustment = [['2023-01-31', 83.33, 83.33], ['2023-02-28', 83.33, 166.66], ['2023-03-31', 83.33, 249.99], ['2023-04-30', 83.33, 333.32], ['2023-05-31', 83.33, 416.65], ['2023-06-30', 83.33, 499.98], ['2023-07-31', 83.33, 583.31], ['2023-08-31', 83.33, 666.64], ['2023-09-30', 83.33, 749.97], ['2023-10-31', 83.33, 833.3], ['2023-11-30', 83.33, 916.63], ['2023-12-31', 83.37, 1000.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=1200)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2023-01-31', 100.0, 100.0], ['2023-02-28', 100.0, 200.0], ['2023-03-31', 100.0, 300.0], ['2023-04-30', 100.0, 400.0], ['2023-05-31', 100.0, 500.0], ['2023-06-30', 100.0, 600.0], ['2023-07-31', 100.0, 700.0], ['2023-08-31', 100.0, 800.0], ['2023-09-30', 100.0, 900.0], ['2023-10-31', 100.0, 1000.0], ['2023-11-30', 100.0, 1100.0], ['2023-12-31', 100.0, 1200.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_value_adjustment.cancel()
asset.reload()
self.assertEqual(asset.finance_books[0].value_after_depreciation, 1000)
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:742*

### test_depreciation_on_return_of_sold_asset

**Category**: workflow  
**Description**: Workflow: test depreciation on return of sold asset  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

from erpnext.controllers.sales_and_purchase_return import make_return_doc
create_asset_data()
asset = create_asset(item_code='Macbook Pro', calculate_depreciation=1, submit=1)
post_depreciation_entries(getdate('2021-09-30'))
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=90000, posting_date=getdate('2021-09-30'))
return_si = make_return_doc('Sales Invoice', si.name)
return_si.submit()
asset.load_from_db()
expected_values = [['2020-06-30', 1366.12, 1366.12, True], ['2021-06-30', 20000.0, 21366.12, True], ['2022-06-30', 20000.95, 41367.07, False], ['2023-06-30', 20000.95, 61368.02, False], ['2024-06-30', 20000.95, 81368.97, False], ['2025-06-06', 18631.03, 100000.0, False]]
for i, schedule in enumerate(get_depr_schedule(asset.name, 'Active')):
    self.assertEqual(getdate(expected_values[i][0]), schedule.schedule_date)
    self.assertEqual(expected_values[i][1], schedule.depreciation_amount)
    self.assertEqual(expected_values[i][2], schedule.accumulated_depreciation_amount)
    self.assertEqual(schedule.journal_entry, schedule.journal_entry)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:815*

### test_depreciation_schedule_after_cancelling_asset_value_adjustent_for_existing_asset

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after cancelling asset value adjustent for existing asset  
**Expected**: self.assertEqual(schedules, expected_depreciation_before_adjustment)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=500, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2023-01-15', depreciation_start_date='2023-03-31', frequency_of_depreciation=1, total_number_of_depreciations=12, is_existing_asset=1, opening_accumulated_depreciation=64.52, opening_number_of_booked_depreciations=2, submit=1)
expected_depreciation_before_adjustment = [['2023-03-31', 41.39, 105.91], ['2023-04-30', 41.39, 147.3], ['2023-05-31', 41.39, 188.69], ['2023-06-30', 41.39, 230.08], ['2023-07-31', 41.39, 271.47], ['2023-08-31', 41.39, 312.86], ['2023-09-30', 41.39, 354.25], ['2023-10-31', 41.39, 395.64], ['2023-11-30', 41.39, 437.03], ['2023-12-31', 41.39, 478.42], ['2024-01-15', 21.58, 500.0]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2023-04-01', current_asset_value=current_asset_value, new_asset_value=600)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2023-03-31', 57.03, 121.55], ['2023-04-30', 57.03, 178.58], ['2023-05-31', 57.03, 235.61], ['2023-06-30', 57.03, 292.64], ['2023-07-31', 57.03, 349.67], ['2023-08-31', 57.03, 406.7], ['2023-09-30', 57.03, 463.73], ['2023-10-31', 57.03, 520.76], ['2023-11-30', 57.03, 577.79], ['2023-12-31', 57.03, 634.82], ['2024-01-15', 29.7, 664.52]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_value_adjustment.cancel()
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:844*

### test_depreciation_schedule_for_parallel_adjustment_and_repair

**Category**: workflow  
**Description**: Workflow: test depreciation schedule for parallel adjustment and repair  
**Expected**: self.assertEqual(schedules, expected_depreciation_after_cancelling_adjustment)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=600, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2021-01-01', depreciation_start_date='2021-12-31', frequency_of_depreciation=12, total_number_of_depreciations=3, is_existing_asset=1, submit=1)
post_depreciation_entries(date='2021-12-31')
asset.reload()
expected_depreciation_before_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 200, 400], ['2023-12-31', 200, 600]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2022-01-15', current_asset_value=current_asset_value, new_asset_value=500)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', failure_date='2022-01-20', pi_repair_cost1=60, pi_repair_cost2=40, increase_in_asset_life=0, submit=1)
self.assertEqual(asset_repair.total_repair_cost, 100)
expected_depreciation_after_repair = [['2021-12-31', 200, 200], ['2022-12-31', 300, 500], ['2023-12-31', 300, 800]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_repair)
asset.reload()
asset_value_adjustment.cancel()
expected_depreciation_after_cancelling_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_cancelling_adjustment)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:918*

### test_depreciation_schedule_after_sale_of_asset

**Category**: workflow  
**Description**: Workflow: test depreciation schedule after sale of asset  
**Expected**: self.assertEqual(schedules, expected_depreciation_after_adjustment)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_asset_data()

asset = create_asset(item_code='Macbook Pro', net_purchase_amount=600, calculate_depreciation=1, depreciation_method='Straight Line', available_for_use_date='2021-01-01', depreciation_start_date='2021-12-31', frequency_of_depreciation=12, total_number_of_depreciations=3, is_existing_asset=1, submit=1)
post_depreciation_entries(date='2021-12-31')
asset.reload()
expected_depreciation_before_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 200, 400], ['2023-12-31', 200, 600]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_before_adjustment)
current_asset_value = asset.finance_books[0].value_after_depreciation
asset_value_adjustment = make_asset_value_adjustment(asset=asset.name, date='2022-01-15', current_asset_value=current_asset_value, new_asset_value=500)
asset_value_adjustment.submit()
expected_depreciation_after_adjustment = [['2021-12-31', 200, 200], ['2022-12-31', 250, 450], ['2023-12-31', 250, 700]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
si = create_sales_invoice(item_code='Macbook Pro', asset=asset.name, qty=1, rate=300, posting_date=getdate('2022-04-01'))
asset.load_from_db()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
expected_depreciation_after_sale = [['2021-12-31', 200.0, 200.0], ['2022-04-01', 62.33, 262.33]]
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_sale)
si.cancel()
asset.reload()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Partially Depreciated')
schedules = [[cstr(d.schedule_date), d.depreciation_amount, d.accumulated_depreciation_amount] for d in get_depr_schedule(asset.name, 'Active')]
self.assertEqual(schedules, expected_depreciation_after_adjustment)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_depreciation_schedule/test_asset_depreciation_schedule.py:1007*

### test_cwip_accounting

**Category**: workflow  
**Description**: Workflow: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.get_value('Company', '_Test Company', 'capital_work_in_progress_account')
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', '')
asset_category = frappe.new_doc('Asset Category')
asset_category.asset_category_name = 'Computers'
asset_category.enable_cwip_accounting = 1
asset_category.total_number_of_depreciations = 3
asset_category.frequency_of_depreciation = 3
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
self.assertRaises(frappe.ValidationError, asset_category.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:32*

### test_cwip_accounting

**Category**: workflow  
**Description**: Workflow: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.get_value('Company', '_Test Company', 'capital_work_in_progress_account')
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', '')
asset_category = frappe.new_doc('Asset Category')
asset_category.asset_category_name = 'Computers'
asset_category.enable_cwip_accounting = 1
asset_category.total_number_of_depreciations = 3
asset_category.frequency_of_depreciation = 3
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
self.assertRaises(frappe.ValidationError, asset_category.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:32*

### test_asset_status

**Category**: workflow  
**Description**: Workflow: test asset status  
**Expected**: self.assertRaises(frappe.ValidationError, asset_repair.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
asset.reload()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
asset_repair = frappe.new_doc('Asset Repair')
asset_repair.update({'company': '_Test Company', 'asset': asset.name, 'asset_name': asset.asset_name})
self.assertRaises(frappe.ValidationError, asset_repair.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:39*

### test_update_status

**Category**: workflow  
**Description**: Workflow: test update status  
**Expected**: self.assertEqual(asset_status, initial_status)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(submit=1)
initial_status = asset.status
asset_repair = create_asset_repair(asset=asset)
if asset_repair.repair_status == 'Pending':
    asset.reload()
    self.assertEqual(asset.status, 'Out of Order')
asset_repair.repair_status = 'Completed'
asset_repair.save()
asset_status = frappe.db.get_value('Asset', asset_repair.asset, 'status')
self.assertEqual(asset_status, initial_status)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:68*

### test_serialized_item_consumption

**Category**: workflow  
**Description**: Workflow: test serialized item consumption  
**Expected**: self.assertRaises(frappe.ValidationError, asset_repair.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.stock.doctype.stock_entry.test_stock_entry import make_serialized_item
stock_entry = make_serialized_item(self)
bundle_id = stock_entry.get('items')[0].serial_and_batch_bundle
serial_nos = get_serial_nos_from_bundle(bundle_id)
serial_no = serial_nos[0]
create_asset_repair(stock_consumption=1, item_code=stock_entry.get('items')[0].item_code, warehouse='_Test Warehouse - _TC', serial_no=[serial_no], submit=1)
asset_repair = create_asset_repair(stock_consumption=1, warehouse='_Test Warehouse - _TC', item_code=stock_entry.get('items')[0].item_code)
asset_repair.repair_status = 'Completed'
self.assertRaises(frappe.ValidationError, asset_repair.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:122*

### test_increase_in_asset_value_due_to_repair_cost_capitalisation

**Category**: workflow  
**Description**: Workflow: test increase in asset value due to repair cost capitalisation  
**Expected**: self.assertEqual(asset_repair.repair_cost, increase_in_asset_value)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(calculate_depreciation=1, submit=1)
initial_asset_value = get_asset_value_after_depreciation(asset.name)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_value=1)
asset.reload()
increase_in_asset_value = get_asset_value_after_depreciation(asset.name) - initial_asset_value
self.assertEqual(asset_repair.repair_cost, increase_in_asset_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:158*

### test_repair_cost_exceeds_available_amount

**Category**: workflow  
**Description**: Workflow: Test that repair cost cannot exceed available amount from Purchase Invoice.  
**Expected**: self.assertRaises(frappe.ValidationError, asset_repair2.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'Test that repair cost cannot exceed available amount from Purchase Invoice.'
asset_repair1 = create_asset_repair(capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
pi_name = asset_repair1.invoices[0].purchase_invoice
expense_account = asset_repair1.invoices[0].expense_account
asset_repair2 = frappe.new_doc('Asset Repair')
asset_repair2.update({'asset': asset_repair1.asset, 'asset_name': asset_repair1.asset_name, 'failure_date': nowdate(), 'description': 'Second Repair', 'company': asset_repair1.company, 'capitalize_repair_cost': 1})
asset_repair2.append('invoices', {'purchase_invoice': pi_name, 'expense_account': expense_account, 'repair_cost': 10})
self.assertRaises(frappe.ValidationError, asset_repair2.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:179*

### test_gl_entries_with_perpetual_inventory

**Category**: workflow  
**Description**: Workflow: test gl entries with perpetual inventory  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
set_depreciation_settings_in_company(company='_Test Company with perpetual inventory')
asset_category = frappe.get_doc('Asset Category', 'Computers')
asset_category.append('accounts', {'company_name': '_Test Company with perpetual inventory', 'fixed_asset_account': '_Test Fixed Asset - TCP1', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - TCP1', 'depreciation_expense_account': '_Test Depreciations - TCP1', 'capital_work_in_progress_account': 'CWIP Account - TCP1'})
asset_category.save()
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, warehouse='Stores - TCP1', company='_Test Company with perpetual inventory', pi_expense_account1='Administrative Expenses - TCP1', pi_expense_account2='Legal Expenses - TCP1', item='_Test Non Stock Item', increase_in_asset_life=1, submit=1)
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
self.assertTrue(gl_entries)
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
pi_repair_costs = [pi.repair_cost for pi in asset_repair.invoices]
stock_entry_expense_account = frappe.get_doc('Stock Entry', {'asset_repair': asset_repair.name}).get('items')[0].expense_account
expected_values = {fixed_asset_account: [asset_repair.total_repair_cost, 0], pi_expense_accounts[0]: [0, pi_repair_costs[0]], pi_expense_accounts[1]: [0, pi_repair_costs[1]], stock_entry_expense_account: [0, 100]}
for d in gl_entries:
    self.assertEqual(expected_values[d.account][0], d.debit)
    self.assertEqual(expected_values[d.account][1], d.credit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:212*

### test_gl_entries_with_periodical_inventory

**Category**: workflow  
**Description**: Workflow: test gl entries with periodical inventory  
**Expected**: self.assertTrue(gl_entries)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Company', '_Test Company', 'default_expense_account', 'Cost of Goods Sold - _TC')
asset_repair = create_asset_repair(capitalize_repair_cost=1, stock_consumption=1, increase_in_asset_life=1, item='_Test Non Stock Item', submit=1)
gl_entries = frappe.db.sql("\n\t\t\tselect\n\t\t\t\taccount,\n\t\t\t\tsum(debit) as debit,\n\t\t\t\tsum(credit) as credit\n\t\t\tfrom `tabGL Entry`\n\t\t\twhere\n\t\t\t\tvoucher_type='Asset Repair'\n\t\t\t\tand voucher_no=%s\n\t\t\tgroup by\n\t\t\t\taccount\n\t\t", asset_repair.name, as_dict=1)
self.assertTrue(gl_entries)
fixed_asset_account = get_asset_account('fixed_asset_account', asset=asset_repair.asset, company=asset_repair.company)
default_expense_account = frappe.get_cached_value('Company', asset_repair.company, 'default_expense_account')
pi_expense_accounts = [pi.expense_account for pi in asset_repair.invoices]
expected_values = {fixed_asset_account: [650, 0], pi_expense_accounts[0]: [0, 250], default_expense_account: [0, 100], pi_expense_accounts[1]: [0, 300]}
for d in gl_entries:
    self.assertEqual(expected_values[d.account][0], d.debit)
    self.assertEqual(expected_values[d.account][1], d.credit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:279*

### test_increase_in_asset_life

**Category**: workflow  
**Description**: Workflow: test increase in asset life  
**Expected**: self.assertEqual(second_asset_depr_schedule.get('depreciation_schedule')[-1].accumulated_depreciation_amount, asset.finance_books[0].value_after_depreciation)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(calculate_depreciation=1, submit=1)
first_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Active')
initial_num_of_depreciations = num_of_depreciations(asset)
create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1, increase_in_asset_life=1)
asset.reload()
first_asset_depr_schedule.load_from_db()
second_asset_depr_schedule = get_asset_depr_schedule_doc(asset.name, 'Active')
self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
self.assertEqual(initial_num_of_depreciations + 1, num_of_depreciations(asset))
self.assertEqual(second_asset_depr_schedule.get('depreciation_schedule')[-1].accumulated_depreciation_amount, asset.finance_books[0].value_after_depreciation)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:327*

### test_gl_entries_with_capitalized_asset_repair

**Category**: workflow  
**Description**: Workflow: test gl entries with capitalized asset repair  
**Expected**: self.assertEqual(booked_value, asset_repair.repair_cost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
asset = create_asset(is_existing_asset=1, calculate_depreciation=1, submit=1)
asset_repair = create_asset_repair(asset=asset, capitalize_repair_cost=1, item='_Test Non Stock Item', submit=1)
asset.reload()
GLEntry = qb.DocType('GL Entry')
res = qb.from_(GLEntry).select(Sum(GLEntry.debit_in_account_currency).as_('total_debit')).where((GLEntry.voucher_type == 'Asset Repair') & (GLEntry.voucher_no == asset_repair.name) & (GLEntry.against_voucher_type == 'Asset') & (GLEntry.against_voucher == asset.name) & (GLEntry.company == asset.company) & (GLEntry.is_cancelled == 0)).run(as_dict=True)
booked_value = res[0].total_debit if res else 0
self.assertEqual(asset.additional_asset_cost, asset_repair.repair_cost)
self.assertEqual(booked_value, asset_repair.repair_cost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:361*

### test_asset_status

**Category**: workflow  
**Description**: Workflow: test asset status  
**Expected**: self.assertRaises(frappe.ValidationError, asset_repair.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
date = nowdate()
purchase_date = add_months(get_first_day(date), -2)
asset = create_asset(calculate_depreciation=1, available_for_use_date=purchase_date, purchase_date=purchase_date, expected_value_after_useful_life=10000, total_number_of_depreciations=10, frequency_of_depreciation=1, submit=1)
si = make_sales_invoice(asset=asset.name, item_code='Macbook Pro', company='_Test Company', sell_qty=asset.asset_quantity)
si.customer = '_Test Customer'
si.due_date = date
si.get('items')[0].rate = 25000
si.insert()
si.submit()
asset.reload()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'status'), 'Sold')
asset_repair = frappe.new_doc('Asset Repair')
asset_repair.update({'company': '_Test Company', 'asset': asset.name, 'asset_name': asset.asset_name})
self.assertRaises(frappe.ValidationError, asset_repair.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_repair/test_asset_repair.py:39*

### test_capitalization_with_perpetual_inventory

**Category**: method_call  
**Description**: test capitalization with perpetual inventory  
**Expected**: self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)  
**Confidence**: 0.85  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

self.assertEqual(asset_capitalization.target_qty, 1)
self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:80*

### test_capitalization_with_perpetual_inventory

**Category**: method_call  
**Description**: test capitalization with perpetual inventory  
**Expected**: self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)  
**Confidence**: 0.85  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

self.assertEqual(asset_capitalization.stock_items[0].valuation_rate, stock_rate)
self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:82*

### test_capitalization_with_perpetual_inventory

**Category**: method_call  
**Description**: test capitalization with perpetual inventory  
**Expected**: self.assertEqual(asset_capitalization.stock_items_total, stock_amount)  
**Confidence**: 0.85  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

self.assertEqual(asset_capitalization.stock_items[0].amount, stock_amount)
self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:83*

### test_capitalization_with_perpetual_inventory

**Category**: method_call  
**Description**: test capitalization with perpetual inventory  
**Expected**: self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)  
**Confidence**: 0.85  

```python
# Setup
set_depreciation_settings_in_company()
create_asset_data()
create_asset_capitalization_data()
frappe.db.sql('delete from `tabTax Rule`')

self.assertEqual(asset_capitalization.stock_items_total, stock_amount)
self.assertEqual(asset_capitalization.asset_items[0].asset_value, consumed_asset_value)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_capitalization/test_asset_capitalization.py:84*

### test_movement

**Category**: method_call  
**Description**: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

create_asset_movement(purpose='Transfer', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location', 'target_location': 'Test Location 2'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:47*

### test_movement

**Category**: method_call  
**Description**: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:77*

### test_movement

**Category**: method_call  
**Description**: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

create_asset_movement(purpose='Issue', company=asset.company, assets=[{'asset': asset.name, 'source_location': 'Test Location 2', 'to_employee': employee}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:81*

### test_movement

**Category**: method_call  
**Description**: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location 2')
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'custodian'), employee)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:90*

### test_movement

**Category**: method_call  
**Description**: test movement  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

create_asset_movement(purpose='Receipt', company=asset.company, assets=[{'asset': asset.name, 'from_employee': employee, 'target_location': 'Test Location'}], reference_doctype='Purchase Receipt', reference_name=pr.name)
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:93*

### test_last_movement_cancellation

**Category**: method_call  
**Description**: test last movement cancellation  
**Expected**: self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')  
**Confidence**: 0.85  

```python
# Setup
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')
create_asset_data()
make_location()

movement1.cancel()
self.assertEqual(frappe.db.get_value('Asset', asset.name, 'location'), 'Test Location')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_movement/test_asset_movement.py:146*

### test_asset_depreciation_value_adjustment

**Category**: method_call  
**Description**: test asset depreciation value adjustment  
**Expected**: self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')  
**Confidence**: 0.85  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:91*

### test_depreciation_after_cancelling_asset_repair

**Category**: method_call  
**Description**: test depreciation after cancelling asset repair  
**Expected**: self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')  
**Confidence**: 0.85  

```python
# Setup
create_asset_data()
frappe.db.set_value('Company', '_Test Company', 'capital_work_in_progress_account', 'CWIP Account - _TC')

self.assertEqual(second_asset_depr_schedule.status, 'Active')
self.assertEqual(first_asset_depr_schedule.status, 'Cancelled')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_value_adjustment/test_asset_value_adjustment.py:180*

### test_create_asset_maintenance_with_log

**Category**: method_call  
**Description**: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.85  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

asset_maintenance.reload()
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:73*

### test_create_asset_maintenance_with_log

**Category**: method_call  
**Description**: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.85  

```python
asset_maintenance.reload()
self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:73*

### test_cwip_accounting

**Category**: method_call  
**Description**: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.85  

```python
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
self.assertRaises(frappe.ValidationError, asset_category.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:42*

### test_cwip_accounting

**Category**: method_call  
**Description**: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.85  

```python
asset_category.append('accounts', {'company_name': '_Test Company', 'fixed_asset_account': '_Test Fixed Asset - _TC', 'accumulated_depreciation_account': '_Test Accumulated Depreciations - _TC', 'depreciation_expense_account': '_Test Depreciations - _TC'})
self.assertRaises(frappe.ValidationError, asset_category.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:42*

### test_asset_shift_allocation

**Category**: instantiation  
**Description**: Instantiate create_asset: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.80  

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:25*

### test_asset_shift_allocation

**Category**: instantiation  
**Description**: Instantiate get_doc: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.80  

```python
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:70*

### test_asset_shift_allocation

**Category**: instantiation  
**Description**: Instantiate create_asset: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.80  

```python
asset = create_asset(calculate_depreciation=1, available_for_use_date='2023-01-01', purchase_date='2023-01-01', net_purchase_amount=120000, depreciation_start_date='2023-01-31', total_number_of_depreciations=12, frequency_of_depreciation=1, shift_based=1, submit=1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:25*

### test_asset_shift_allocation

**Category**: instantiation  
**Description**: Instantiate get_doc: test asset shift allocation  
**Expected**: self.assertEqual(schedules, expected_schedules)  
**Confidence**: 0.80  

```python
asset_shift_allocation = frappe.get_doc('Asset Shift Allocation', asset_shift_allocation.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_shift_allocation/test_asset_shift_allocation.py:70*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate get_last_day: test create asset maintenance with log  
**Expected**: self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})  
**Confidence**: 0.80  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

month_end_date = get_last_day(nowdate())
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:22*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate calculate_next_due_date: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.80  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

next_due_date = calculate_next_due_date(nowdate(), 'Monthly')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:53*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate get_value: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.80  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

asset_maintenance_log = frappe.db.get_value('Asset Maintenance Log', {'asset_maintenance': asset_maintenance.name, 'task_name': 'Change Oil'}, 'name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:56*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate get_doc: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.80  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

asset_maintenance_log_doc = frappe.get_doc('Asset Maintenance Log', asset_maintenance_log)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:62*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate calculate_next_due_date: test create asset maintenance with log  
**Expected**: self.assertEqual(asset_maintenance.asset_maintenance_tasks[0].next_due_date, next_due_date)  
**Confidence**: 0.80  

```python
# Setup
set_depreciation_settings_in_company()
self.pr = make_purchase_receipt(item_code='Photocopier', qty=1, rate=100000.0, location='Test Location')
self.asset_name = frappe.db.get_value('Asset', {'purchase_receipt': self.pr.name}, 'name')
self.asset_doc = frappe.get_doc('Asset', self.asset_name)

next_due_date = calculate_next_due_date(asset_maintenance_log_doc.completion_date, 'Monthly')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:71*

### test_create_asset_maintenance_with_log

**Category**: instantiation  
**Description**: Instantiate get_last_day: test create asset maintenance with log  
**Expected**: self.asset_doc.append('finance_books', {'expected_value_after_useful_life': 200, 'depreciation_method': 'Straight Line', 'total_number_of_depreciations': 3, 'frequency_of_depreciation': 10, 'depreciation_start_date': month_end_date})  
**Confidence**: 0.80  

```python
month_end_date = get_last_day(nowdate())
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_maintenance/test_asset_maintenance.py:22*

### test_mandatory_fields

**Category**: instantiation  
**Description**: Instantiate new_doc: test mandatory fields  
**Expected**: self.assertRaises(frappe.MandatoryError, asset_category.insert)  
**Confidence**: 0.80  

```python
asset_category = frappe.new_doc('Asset Category')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:10*

### test_cwip_accounting

**Category**: instantiation  
**Description**: Instantiate new_doc: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.80  

```python
asset_category = frappe.new_doc('Asset Category')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:36*

### test_mandatory_fields

**Category**: instantiation  
**Description**: Instantiate new_doc: test mandatory fields  
**Expected**: self.assertRaises(frappe.MandatoryError, asset_category.insert)  
**Confidence**: 0.80  

```python
asset_category = frappe.new_doc('Asset Category')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:10*

### test_cwip_accounting

**Category**: instantiation  
**Description**: Instantiate new_doc: test cwip accounting  
**Expected**: self.assertRaises(frappe.ValidationError, asset_category.insert)  
**Confidence**: 0.80  

```python
asset_category = frappe.new_doc('Asset Category')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/assets/doctype/asset_category/test_asset_category.py:36*

