# Test Example Extraction Report

**Total Examples**: 118  
**High Value Examples** (confidence > 0.7): 118  
**Average Complexity**: 0.70  

## Examples by Category

- **instantiation**: 20
- **method_call**: 26
- **workflow**: 72

## Examples by Language

- **Python**: 118

## Extracted Examples

### test_production_plan_mr_creation

**Category**: workflow  
**Description**: Workflow: Test if MRs are created for unavailable raw materials.  
**Expected**: self.assertTrue(len(work_orders), len(pln.po_items))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

'Test if MRs are created for unavailable raw materials.'
pln = create_production_plan(item_code='Test Production Item 1')
self.assertTrue(len(pln.mr_items), 2)
for row in pln.mr_items:
    row.schedule_date = add_to_date(nowdate(), days=10)
pln.make_material_request()
pln.reload()
self.assertTrue(pln.status, 'Material Requested')
material_requests = frappe.get_all('Material Request Item', fields=['parent'], filters={'production_plan': pln.name}, as_list=1, distinct=True)
self.assertTrue(len(material_requests), 2)
for row in material_requests:
    mr_schedule_date = getdate(frappe.db.get_value('Material Request', row[0], 'schedule_date'))
    expected_date = getdate(add_to_date(nowdate(), days=10))
    self.assertEqual(mr_schedule_date, expected_date)
pln.make_work_order()
work_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
pln.make_work_order()
nwork_orders = frappe.get_all('Work Order', fields=['name'], filters={'production_plan': pln.name}, as_list=1)
self.assertTrue(len(work_orders), len(nwork_orders))
self.assertTrue(len(work_orders), len(pln.po_items))
for name in material_requests:
    mr = frappe.get_doc('Material Request', name[0])
    if mr.docstatus != 0:
        mr.cancel()
for name in work_orders:
    mr = frappe.delete_doc('Work Order', name[0])
pln = frappe.get_doc('Production Plan', pln.name)
pln.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:62*

### test_projected_qty_cascading_across_multiple_sales_orders

**Category**: workflow  
**Description**: Workflow: test projected qty cascading across multiple sales orders  
**Expected**: self.assertEqual(quantities, [0, 1], 'Cascading failed: first item should consume stock (qty=0), second should need procurement (qty=1)')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

rm_item = make_item('_Test RM For Cascading', {'is_stock_item': 1, 'valuation_rate': 100}).name
fg_item_a = make_item('_Test FG A For Cascading', {'is_stock_item': 1, 'valuation_rate': 200}).name
if not frappe.db.exists('BOM', {'item': fg_item_a, 'docstatus': 1}):
    make_bom(item=fg_item_a, raw_materials=[rm_item], rm_qty=1)
sr = create_stock_reconciliation(item_code=rm_item, target='_Test Warehouse - _TC', qty=1, rate=100)
so1 = make_sales_order(item_code=fg_item_a, qty=1)
so2 = make_sales_order(item_code=fg_item_a, qty=1)
pln = frappe.get_doc({'doctype': 'Production Plan', 'company': '_Test Company', 'posting_date': nowdate(), 'get_items_from': 'Sales Order', 'ignore_existing_ordered_qty': 1})
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln.get_items()
pln.insert()
mr_items = get_items_for_material_requests(pln.as_dict())
quantities = [d['quantity'] for d in mr_items]
rm_qty = sum(quantities)
self.assertEqual(len(mr_items), 2)
self.assertEqual(rm_qty, 1, 'Cascading failed: total MR qty should be 1 (2 needed - 1 in stock)')
self.assertEqual(quantities, [0, 1], 'Cascading failed: first item should consume stock (qty=0), second should need procurement (qty=1)')
sr.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:154*

### test_production_plan_without_multi_level_for_existing_ordered_qty

**Category**: workflow  
**Description**: Workflow: - Disable 'ignore_existing_ordered_qty'.
- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for
non exploded BOM.  
**Expected**: self.assertFalse(len(items))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

"\n\t\t- Disable 'ignore_existing_ordered_qty'.\n\t\t- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for\n\t\tnon exploded BOM.\n\t\t"
sr1 = create_stock_reconciliation(item_code='Raw Material Item 1', target='_Test Warehouse - _TC', qty=1, rate=130)
sr2 = create_stock_reconciliation(item_code='Subassembly Item 1', target='_Test Warehouse - _TC', qty=1, rate=140)
pln = create_production_plan(item_code='Test Production Item 1', use_multi_level_bom=0, ignore_existing_ordered_qty=1)
items = []
for row in pln.mr_items:
    if row.quantity > 0:
        items.append(row.item_code)
self.assertFalse(len(items))
pln.cancel()
sr1.cancel()
sr2.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:233*

### test_production_plan_sales_orders

**Category**: workflow  
**Description**: Workflow: Test if previously fulfilled SO (with WO) is pulled into Prod Plan.  
**Expected**: self.assertEqual(sales_orders, [])  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

'Test if previously fulfilled SO (with WO) is pulled into Prod Plan.'
item = 'Test Production Item 1'
so = make_sales_order(item_code=item, qty=1)
sales_order = so.name
sales_order_item = so.items[0].name
pln = frappe.new_doc('Production Plan')
pln.company = so.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln.get_so_items()
pln.submit()
pln.make_work_order()
work_order = frappe.db.get_value('Work Order', {'sales_order': sales_order, 'production_plan': pln.name, 'sales_order_item': sales_order_item}, 'name')
wo_doc = frappe.get_doc('Work Order', work_order)
wo_doc.update({'wip_warehouse': 'Work In Progress - _TC', 'fg_warehouse': 'Finished Goods - _TC'})
wo_doc.submit()
so_wo_qty = frappe.db.get_value('Sales Order Item', sales_order_item, 'work_order_qty')
self.assertTrue(so_wo_qty, 5)
pln = frappe.new_doc('Production Plan')
pln.update({'from_date': so.transaction_date, 'to_date': so.transaction_date, 'customer': so.customer, 'item_code': item, 'sales_order_status': so.status})
sales_orders = get_sales_orders(pln) or {}
sales_orders = [d.get('name') for d in sales_orders if d.get('name') == sales_order]
self.assertEqual(sales_orders, [])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:261*

### test_donot_allow_to_make_multiple_pp_against_same_so

**Category**: workflow  
**Description**: Workflow: test donot allow to make multiple pp against same so  
**Expected**: self.assertRaises(frappe.ValidationError, pln.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

item = 'Test SO Production Item 1'
create_item(item)
raw_material = 'Test SO RM Production Item 1'
create_item(raw_material)
if not frappe.db.get_value('BOM', {'item': item}):
    make_bom(item=item, raw_materials=[raw_material])
so = make_sales_order(item_code=item, qty=4)
pln = frappe.new_doc('Production Plan')
pln.company = so.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln.get_so_items()
pln.submit()
pln = frappe.new_doc('Production Plan')
pln.company = so.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln.get_so_items()
self.assertRaises(frappe.ValidationError, pln.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:314*

### test_so_based_bill_of_material

**Category**: workflow  
**Description**: Workflow: test so based bill of material  
**Expected**: self.assertEqual(pln2.po_items[0].bom_no, bom2.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

item = 'Test SO Production Item 1'
create_item(item)
raw_material = 'Test SO RM Production Item 1'
create_item(raw_material)
bom1 = make_bom(item=item, raw_materials=[raw_material])
so = make_sales_order(item_code=item, qty=4)
bom2 = make_bom(item=item, raw_materials=[raw_material])
so2 = make_sales_order(item_code=item, qty=4)
pln1 = frappe.new_doc('Production Plan')
pln1.company = so.company
pln1.get_items_from = 'Sales Order'
pln1.append('sales_orders', {'sales_order': so.name, 'sales_order_date': so.transaction_date, 'customer': so.customer, 'grand_total': so.grand_total})
pln1.get_so_items()
self.assertEqual(pln1.po_items[0].bom_no, bom1.name)
pln2 = frappe.new_doc('Production Plan')
pln2.company = so2.company
pln2.get_items_from = 'Sales Order'
pln2.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln2.get_so_items()
self.assertEqual(pln2.po_items[0].bom_no, bom2.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:359*

### test_production_plan_with_non_active_bom_item

**Category**: workflow  
**Description**: Workflow: test production plan with non active bom item  
**Expected**: self.assertFalse(pln.po_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

item = make_item('Test Production Item 1 for Non Active BOM', {'is_stock_item': 1}).name
so1 = make_sales_order(item_code=item, qty=1)
pln = frappe.new_doc('Production Plan')
pln.company = so1.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
pln.get_items()
self.assertFalse(pln.po_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:410*

### test_production_plan_combine_items

**Category**: workflow  
**Description**: Workflow: Test combining FG items in Production Plan.  
**Expected**: self.assertTrue(pln.po_items[0].planned_qty, 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

'Test combining FG items in Production Plan.'
item = 'Test Production Item 1'
so1 = make_sales_order(item_code=item, qty=1)
pln = frappe.new_doc('Production Plan')
pln.company = so1.company
pln.get_items_from = 'Sales Order'
pln.append('sales_orders', {'sales_order': so1.name, 'sales_order_date': so1.transaction_date, 'customer': so1.customer, 'grand_total': so1.grand_total})
so2 = make_sales_order(item_code=item, qty=2)
pln.append('sales_orders', {'sales_order': so2.name, 'sales_order_date': so2.transaction_date, 'customer': so2.customer, 'grand_total': so2.grand_total})
pln.combine_items = 1
pln.get_items()
pln.submit()
self.assertTrue(pln.po_items[0].planned_qty, 3)
pln.make_work_order()
work_order = frappe.db.get_value('Work Order', {'production_plan_item': pln.po_items[0].name, 'production_plan': pln.name}, 'name')
wo_doc = frappe.get_doc('Work Order', work_order)
wo_doc.update({'wip_warehouse': 'Work In Progress - _TC'})
wo_doc.submit()
so_items = []
for plan_reference in pln.prod_plan_references:
    so_items.append(plan_reference.sales_order_item)
    so_wo_qty = frappe.db.get_value('Sales Order Item', plan_reference.sales_order_item, 'work_order_qty')
    self.assertEqual(so_wo_qty, plan_reference.qty)
wo_doc.cancel()
for so_item in so_items:
    so_wo_qty = frappe.db.get_value('Sales Order Item', so_item, 'work_order_qty')
    self.assertEqual(so_wo_qty, 0.0)
pln.reload()
pln.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:432*

### test_production_plan_subassembly_default_supplier

**Category**: workflow  
**Description**: Workflow: test production plan subassembly default supplier  
**Expected**: self.assertEqual(plan.sub_assembly_items[0].supplier, '_Test Supplier')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
bom_tree_1 = {'Test Laptop': {'Test Motherboard': {'Test Motherboard Wires': {}}}}
create_nested_bom(bom_tree_1, prefix='')
item_doc = frappe.get_doc('Item', 'Test Motherboard')
company = '_Test Company'
item_doc.is_sub_contracted_item = 1
for row in item_doc.item_defaults:
    if row.company == company and (not row.default_supplier):
        row.default_supplier = '_Test Supplier'
if not item_doc.item_defaults:
    item_doc.append('item_defaults', {'company': company, 'default_supplier': '_Test Supplier'})
item_doc.save()
plan = create_production_plan(item_code='Test Laptop', use_multi_level_bom=1, do_not_submit=True)
plan.get_sub_assembly_items()
plan.set_default_supplier_for_subcontracting_order()
self.assertEqual(plan.sub_assembly_items[0].supplier, '_Test Supplier')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:496*

### test_production_plan_combine_subassembly

**Category**: workflow  
**Description**: Workflow: Test combining Sub assembly items belonging to the same BOM in Prod Plan.
1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001
2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001  
**Expected**: self.assertTrue(len(plan.sub_assembly_items), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
for item in ['Test Production Item 1', 'Subassembly Item 1', 'Raw Material Item 1', 'Raw Material Item 2']:
    create_item(item, valuation_rate=100)
    sr = frappe.db.get_value('Stock Reconciliation Item', {'item_code': item, 'docstatus': 1}, 'parent')
    if sr:
        sr_doc = frappe.get_doc('Stock Reconciliation', sr)
        sr_doc.cancel()
create_item('Test Non Stock Raw Material', is_stock_item=0)
for item, raw_materials in {'Subassembly Item 1': ['Raw Material Item 1', 'Raw Material Item 2'], 'Test Production Item 1': ['Raw Material Item 1', 'Subassembly Item 1', 'Test Non Stock Raw Material']}.items():
    if not frappe.db.get_value('BOM', {'item': item}):
        make_bom(item=item, raw_materials=raw_materials)

'\n\t\tTest combining Sub assembly items belonging to the same BOM in Prod Plan.\n\t\t1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001\n\t\t'
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
bom_tree_1 = {'Red-Car': {'Wheel': {'Rubber': {}}}}
bom_tree_2 = {'Green-Car': {'Wheel': {'Rubber': {}}}}
parent_bom_1 = create_nested_bom(bom_tree_1, prefix='')
parent_bom_2 = create_nested_bom(bom_tree_2, prefix='')
subassembly_bom = parent_bom_1.items[0].bom_no
frappe.db.set_value('BOM Item', parent_bom_2.items[0].name, 'bom_no', subassembly_bom)
plan = create_production_plan(item_code='Red-Car', use_multi_level_bom=1, do_not_save=True)
plan.append('po_items', {'use_multi_level_bom': 1, 'item_code': 'Green-Car', 'bom_no': frappe.db.get_value('Item', 'Green-Car', 'default_bom'), 'planned_qty': 1, 'planned_start_date': now_datetime()})
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 2)
plan.combine_sub_items = 1
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 1)
self.assertEqual(plan.sub_assembly_items[0].qty, 2.0)
self.assertEqual(plan.sub_assembly_items[0].stock_qty, 2.0)
plan.po_items[0].warehouse = 'Finished Goods - _TC'
plan.get_sub_assembly_items()
self.assertTrue(len(plan.sub_assembly_items), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/production_plan/test_production_plan.py:700*

### test_job_card_with_different_work_station

**Category**: workflow  
**Description**: Workflow: test job card with different work station  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

job_cards = frappe.get_all('Job Card', filters={'work_order': self.work_order.name}, fields=['operation_id', 'workstation', 'name', 'for_quantity'])
job_card = job_cards[0]
if job_card:
    workstation = frappe.db.get_value('Workstation', {'name': ('not in', [job_card.workstation])}, 'name')
    if not workstation or job_card.workstation == workstation:
        workstation = make_workstation(workstation_name=random_string(5)).name
    doc = frappe.get_doc('Job Card', job_card.name)
    doc.workstation = workstation
    doc.append('time_logs', {'from_time': '2009-01-01 12:06:25', 'to_time': '2009-01-01 12:37:25', 'time_in_mins': '31.00002', 'completed_qty': job_card.for_quantity})
    doc.submit()
    completed_qty = frappe.db.get_value('Work Order Operation', job_card.operation_id, 'completed_qty')
    self.assertEqual(completed_qty, job_card.for_quantity)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:89*

### test_job_card_overlap

**Category**: workflow  
**Description**: Workflow: test job card overlap  
**Expected**: self.assertRaises(OverlapError, jc2.save)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

wo2 = make_wo_order_test_record(item='_Test FG Item 2', qty=2)
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
employee = self.employees[0].name
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1, 'employee': employee})
jc1.save()
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1, 'employee': employee})
self.assertRaises(OverlapError, jc2.save)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:124*

### test_job_card_overlap_with_capacity

**Category**: workflow  
**Description**: Workflow: test job card overlap with capacity  
**Expected**: self.assertTrue(jc2.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

wo2 = make_wo_order_test_record(item='_Test FG Item 2', qty=2)
workstation = make_workstation(workstation_name=random_string(5)).name
frappe.db.set_value('Workstation', workstation, 'production_capacity', 1)
jc1 = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
jc2 = frappe.get_last_doc('Job Card', {'work_order': wo2.name})
jc1.workstation = workstation
jc1.append('time_logs', {'from_time': '2021-01-01 00:00:00', 'to_time': '2021-01-01 08:00:00', 'completed_qty': 1})
jc1.save()
jc2.workstation = workstation
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
self.assertRaises(OverlapError, jc2.save)
frappe.db.set_value('Workstation', workstation, 'production_capacity', 2)
jc2.load_from_db()
jc2.workstation = workstation
jc2.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 1})
jc2.save()
self.assertTrue(jc2.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:155*

### test_job_card_multiple_materials_transfer

**Category**: workflow  
**Description**: Workflow: Test transferring RMs separately against Job Card with multiple RMs.  
**Expected**: self.assertEqual(transfer_entry_2.fg_completed_qty, 0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

'Test transferring RMs separately against Job Card with multiple RMs.'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
job_card = frappe.get_doc('Job Card', job_card_name)
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
del transfer_entry_1.items[1]
transfer_entry_1.insert()
transfer_entry_1.submit()
job_card.reload()
self.assertEqual(transfer_entry_1.fg_completed_qty, 2)
self.assertEqual(job_card.transferred_qty, 2)
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
del transfer_entry_2.items[0]
transfer_entry_2.insert()
transfer_entry_2.submit()
self.assertEqual(transfer_entry_2.fg_completed_qty, 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:194*

### test_job_card_excess_material_transfer

**Category**: workflow  
**Description**: Workflow: Test transferring more than required RM against Job Card.  
**Expected**: self.assertEqual(job_card.status, 'Completed')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

'Test transferring more than required RM against Job Card.'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
self.assertEqual(job_card.status, 'Open')
transfer_entry_1 = make_stock_entry_from_jc(job_card.name)
transfer_entry_1.insert()
transfer_entry_1.submit()
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
transfer_entry_2.fg_completed_qty = 1
transfer_entry_2.items[0].qty = 5
transfer_entry_2.items[1].qty = 3
transfer_entry_2.insert()
transfer_entry_2.submit()
job_card.reload()
self.assertGreater(job_card.transferred_qty, job_card.for_quantity)
transfer_entry_3 = make_stock_entry_from_jc(job_card.name)
self.assertEqual(transfer_entry_3.fg_completed_qty, 0)
job_card.append('time_logs', {'from_time': '2021-01-01 00:01:00', 'to_time': '2021-01-01 06:00:00', 'completed_qty': 2})
job_card.save()
job_card.submit()
self.assertEqual(job_card.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:225*

### test_job_card_excess_material_transfer_block

**Category**: workflow  
**Description**: Workflow: test job card excess material transfer block  
**Expected**: self.assertRaises(JobCardOverTransferError, transfer_entry_2.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
transfer_entry_1.insert()
transfer_entry_1.submit()
transfer_entry_2 = make_stock_entry_from_jc(job_card_name)
transfer_entry_2.fg_completed_qty = 1
transfer_entry_2.items[0].qty = 5
transfer_entry_2.items[1].qty = 3
transfer_entry_2.insert()
self.assertRaises(JobCardOverTransferError, transfer_entry_2.submit)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:268*

### test_job_card_excess_material_transfer_with_no_reference

**Category**: workflow  
**Description**: Workflow: test job card excess material transfer with no reference  
**Expected**: self.assertRaises(frappe.ValidationError, transfer_entry_1.insert)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card_name = frappe.db.get_value('Job Card', {'work_order': self.work_order.name})
transfer_entry_1 = make_stock_entry_from_jc(job_card_name)
row = transfer_entry_1.items[0]
transfer_entry_1.append('items', {'item_code': row.item_code, 'item_name': row.item_name, 'item_group': row.item_group, 'qty': row.qty, 'uom': row.uom, 'conversion_factor': row.conversion_factor, 'stock_uom': row.stock_uom, 'basic_rate': row.basic_rate, 'basic_amount': row.basic_amount, 'expense_account': row.expense_account, 'cost_center': row.cost_center, 's_warehouse': row.s_warehouse, 't_warehouse': row.t_warehouse})
self.assertRaises(frappe.ValidationError, transfer_entry_1.insert)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:291*

### test_job_card_partial_material_transfer

**Category**: workflow  
**Description**: Workflow: Test partial material transfer against Job Card  
**Expected**: self.assertEqual(job_card.transferred_qty, 0.0)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

'Test partial material transfer against Job Card'
self.transfer_material_against = 'Job Card'
self.source_warehouse = 'Stores - _TC'
self.generate_required_stock(self.work_order)
job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
transfer_entry = make_stock_entry_from_jc(job_card.name)
transfer_entry.fg_completed_qty = 1
transfer_entry.get_items()
transfer_entry.insert()
transfer_entry.submit()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 1)
self.assertEqual(transfer_entry.items[0].qty, 5)
self.assertEqual(transfer_entry.items[1].qty, 3)
transfer_entry_2 = make_stock_entry_from_jc(job_card.name)
self.assertEqual(transfer_entry_2.fg_completed_qty, 1)
self.assertEqual(transfer_entry_2.items[0].qty, 5)
self.assertEqual(transfer_entry_2.items[1].qty, 3)
transfer_entry_2.insert()
transfer_entry_2.submit()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 2)
transfer_entry_2.cancel()
transfer_entry.cancel()
job_card.reload()
self.assertEqual(job_card.transferred_qty, 0.0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:325*

### test_job_card_material_transfer_correctness

**Category**: workflow  
**Description**: Workflow: 1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card
2. Test impact of changing 'For Qty' in such a Stock Entry  
**Expected**: self.assertEqual(transfer_entry.items[0].qty, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

"\n\t\t1. Test if only current Job Card Items are pulled in a Stock Entry against a Job Card\n\t\t2. Test impact of changing 'For Qty' in such a Stock Entry\n\t\t"
create_bom_with_multiple_operations()
work_order = make_wo_with_transfer_against_jc()
job_card_name = frappe.db.get_value('Job Card', {'work_order': work_order.name, 'operation': 'Test Operation A'})
job_card = frappe.get_doc('Job Card', job_card_name)
self.assertEqual(len(job_card.items), 1)
self.assertEqual(job_card.items[0].item_code, '_Test Item')
transfer_entry = make_stock_entry_from_jc(job_card_name)
transfer_entry.insert()
self.assertEqual(len(transfer_entry.items), 1)
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
self.assertEqual(transfer_entry.items[0].qty, 4)
transfer_entry.fg_completed_qty = 2
transfer_entry.get_items()
self.assertEqual(len(transfer_entry.items), 1)
self.assertEqual(transfer_entry.items[0].item_code, '_Test Item')
self.assertEqual(transfer_entry.items[0].qty, 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:365*

### test_corrective_costing

**Category**: workflow  
**Description**: Workflow: test corrective costing  
**Expected**: self.assertEqual(cost_after_cancel, original_cost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.make_employees()
self.make_bom_for_jc_tests()
self.transfer_material_against: Literal['Work Order', 'Job Card'] = 'Work Order'
self.source_warehouse = None
self._work_order = None

job_card = frappe.get_last_doc('Job Card', {'work_order': self.work_order.name})
job_card.append('time_logs', {'from_time': now(), 'to_time': add_to_date(now(), hours=1), 'completed_qty': 2})
job_card.submit()
self.work_order.reload()
original_cost = self.work_order.total_operating_cost
corrective_action = frappe.get_doc(doctype='Operation', is_corrective_operation=1, name=frappe.generate_hash()).insert()
corrective_job_card = make_corrective_job_card(job_card.name, operation=corrective_action.name, for_operation=job_card.operation)
corrective_job_card.hour_rate = 100
corrective_job_card.insert()
corrective_job_card.append('time_logs', {'from_time': add_to_date(now(), hours=2), 'to_time': add_to_date(now(), hours=2, minutes=30), 'completed_qty': 2})
corrective_job_card.submit()
self.work_order.reload()
cost_after_correction = self.work_order.total_operating_cost
self.assertGreater(cost_after_correction, original_cost)
corrective_job_card.cancel()
self.work_order.reload()
cost_after_cancel = self.work_order.total_operating_cost
self.assertEqual(cost_after_cancel, original_cost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/job_card/test_job_card.py:401*

### test_bom_stock_report

**Category**: workflow  
**Description**: Workflow: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
self.assertRaises(ValidationError, bom_stock_report, filters)
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': self.warehouse, 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, self.warehouse, 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:26*

### test_bom_stock_report

**Category**: workflow  
**Description**: Workflow: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
self.assertRaises(ValidationError, bom_stock_report, filters)
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': self.warehouse, 'qty_to_produce': 1}))
expected_data = get_expected_data(self.bom, self.warehouse, 1)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:26*

### test_sequence_id

**Category**: workflow  
**Description**: Workflow: test sequence id  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
operations = [{'operation': 'Test Operation A', 'workstation': 'Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': 'Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Testing Route', operations=operations)
bom_doc = setup_bom(item_code=self.item_code, routing=routing_doc.name)
wo_doc = make_wo_order_test_record(production_item=self.item_code, bom_no=bom_doc.name)
for row in routing_doc.operations:
    self.assertEqual(row.sequence_id, row.idx)
for data in frappe.get_all('Job Card', filters={'work_order': wo_doc.name}, order_by='sequence_id desc'):
    job_card_doc = frappe.get_doc('Job Card', data.name)
    for row in job_card_doc.scheduled_time_logs:
        job_card_doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins})
    job_card_doc.time_logs[0].completed_qty = 10
    if job_card_doc.sequence_id != 1:
        self.assertRaises(OperationSequenceError, job_card_doc.save)
    else:
        job_card_doc.save()
        self.assertEqual(job_card_doc.total_completed_qty, 10)
wo_doc.cancel()
wo_doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:23*

### test_update_bom_operation_time

**Category**: workflow  
**Description**: Workflow: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"Update cost shouldn't update routing times."
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'hour_rate_labour': 750, 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_labour': 200, 'hour_rate_rent': 1000, 'time_in_mins': 20}]
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
routing_doc.operations[0].time_in_mins = 90
routing_doc.operations[1].time_in_mins = 42.2
routing_doc.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:61*

### test_sequence_id

**Category**: workflow  
**Description**: Workflow: test sequence id  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
operations = [{'operation': 'Test Operation A', 'workstation': 'Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': 'Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Testing Route', operations=operations)
bom_doc = setup_bom(item_code=self.item_code, routing=routing_doc.name)
wo_doc = make_wo_order_test_record(production_item=self.item_code, bom_no=bom_doc.name)
for row in routing_doc.operations:
    self.assertEqual(row.sequence_id, row.idx)
for data in frappe.get_all('Job Card', filters={'work_order': wo_doc.name}, order_by='sequence_id desc'):
    job_card_doc = frappe.get_doc('Job Card', data.name)
    for row in job_card_doc.scheduled_time_logs:
        job_card_doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins})
    job_card_doc.time_logs[0].completed_qty = 10
    if job_card_doc.sequence_id != 1:
        self.assertRaises(OperationSequenceError, job_card_doc.save)
    else:
        job_card_doc.save()
        self.assertEqual(job_card_doc.total_completed_qty, 10)
wo_doc.cancel()
wo_doc.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:23*

### test_update_bom_operation_time

**Category**: workflow  
**Description**: Workflow: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
"Update cost shouldn't update routing times."
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'hour_rate_labour': 750, 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_labour': 200, 'hour_rate_rent': 1000, 'time_in_mins': 20}]
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 30}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 20}]
setup_operations(operations)
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
routing_doc.operations[0].time_in_mins = 90
routing_doc.operations[1].time_in_mins = 42.2
routing_doc.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:61*

### test_default_bom

**Category**: workflow  
**Description**: Workflow: test default bom  
**Expected**: self.assertTrue(_get_default_bom_in_item(), bom.name)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
def _get_default_bom_in_item():
    return cstr(frappe.db.get_value('Item', '_Test FG Item 2', 'default_bom'))
bom = frappe.get_doc('BOM', {'item': '_Test FG Item 2', 'is_default': 1})
self.assertEqual(_get_default_bom_in_item(), bom.name)
bom.is_active = 0
bom.save()
self.assertEqual(_get_default_bom_in_item(), '')
bom.is_active = 1
bom.is_default = 1
bom.save()
self.assertTrue(_get_default_bom_in_item(), bom.name)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:59*

### test_bom_cost

**Category**: workflow  
**Description**: Workflow: test bom cost  
**Expected**: self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.insert()
raw_material_cost = 0.0
op_cost = 0.0
for op_row in bom.operations:
    op_cost += op_row.operating_cost
for row in bom.items:
    raw_material_cost += row.amount
base_raw_material_cost = raw_material_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
base_op_cost = op_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
self.assertAlmostEqual(bom.operating_cost, op_cost)
self.assertAlmostEqual(bom.raw_material_cost, raw_material_cost)
self.assertAlmostEqual(bom.total_cost, raw_material_cost + op_cost)
self.assertAlmostEqual(bom.base_operating_cost, base_op_cost)
self.assertAlmostEqual(bom.base_raw_material_cost, base_raw_material_cost)
self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:106*

### test_bom_cost_with_batch_size

**Category**: workflow  
**Description**: Workflow: test bom cost with batch size  
**Expected**: self.assertAlmostEqual(bom.operating_cost, op_cost / 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.docstatus = 0
op_cost = 0.0
for op_row in bom.operations:
    op_row.docstatus = 0
    op_row.batch_size = 2
    op_row.set_cost_based_on_bom_qty = 1
    op_cost += op_row.operating_cost
bom.save()
for op_row in bom.operations:
    self.assertAlmostEqual(op_row.cost_per_unit, op_row.operating_cost / 2)
self.assertAlmostEqual(bom.operating_cost, op_cost / 2)
bom.delete()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:135*

### test_bom_cost_multi_uom_multi_currency_based_on_price_list

**Category**: workflow  
**Description**: Workflow: test bom cost multi uom multi currency based on price list  
**Expected**: self.assertEqual(bom.base_total_cost, 33000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
frappe.db.set_value('Price List', '_Test Price List', 'price_not_uom_dependent', 1)
for item_code, rate in (('_Test Item', 3600), ('_Test Item Home Desktop Manufactured', 3000)):
    frappe.db.sql("delete from `tabItem Price` where price_list='_Test Price List' and item_code=%s", item_code)
    item_price = frappe.new_doc('Item Price')
    item_price.price_list = '_Test Price List'
    item_price.item_code = item_code
    item_price.price_list_rate = rate
    item_price.insert()
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
bom.rm_cost_as_per = 'Price List'
bom.buying_price_list = '_Test Price List'
bom.items[0].uom = '_Test UOM 1'
bom.items[0].conversion_factor = 5
bom.insert()
bom.update_cost(update_hour_rate=False)
self.assertEqual(bom.items[0].rate, 300)
self.assertEqual(bom.items[1].rate, 50)
self.assertEqual(bom.operating_cost, 100)
self.assertEqual(bom.raw_material_cost, 450)
self.assertEqual(bom.total_cost, 550)
self.assertEqual(bom.items[0].base_rate, 18000)
self.assertEqual(bom.items[1].base_rate, 3000)
self.assertEqual(bom.base_operating_cost, 6000)
self.assertEqual(bom.base_raw_material_cost, 27000)
self.assertEqual(bom.base_total_cost, 33000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:154*

### test_bom_cost_multi_uom_based_on_valuation_rate

**Category**: workflow  
**Description**: Workflow: test bom cost multi uom based on valuation rate  
**Expected**: self.assertEqual(bom.items[0].rate, 20)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][2])
bom.set_rate_of_sub_assembly_item_based_on_bom = 0
bom.rm_cost_as_per = 'Valuation Rate'
bom.items[0].uom = '_Test UOM 1'
bom.items[0].conversion_factor = 6
bom.insert()
reset_item_valuation_rate(item_code='_Test Item', warehouse_list=frappe.get_all('Warehouse', {'is_group': 0, 'company': bom.company}, pluck='name'), qty=200, rate=200)
bom.update_cost()
self.assertEqual(bom.items[0].rate, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:191*

### test_bom_cost_with_fg_based_operating_cost

**Category**: workflow  
**Description**: Workflow: test bom cost with fg based operating cost  
**Expected**: self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bom = frappe.copy_doc(self.globalTestRecords['BOM'][4])
bom.insert()
raw_material_cost = 0.0
op_cost = 0.0
op_cost = bom.quantity * bom.operating_cost_per_bom_quantity
for row in bom.items:
    raw_material_cost += row.amount
base_raw_material_cost = raw_material_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
base_op_cost = op_cost * flt(bom.conversion_rate, bom.precision('conversion_rate'))
self.assertAlmostEqual(bom.operating_cost, op_cost)
self.assertAlmostEqual(bom.raw_material_cost, raw_material_cost)
self.assertAlmostEqual(bom.total_cost, raw_material_cost + op_cost)
self.assertAlmostEqual(bom.base_operating_cost, base_op_cost)
self.assertAlmostEqual(bom.base_raw_material_cost, base_raw_material_cost)
self.assertAlmostEqual(bom.base_total_cost, base_raw_material_cost + base_op_cost)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:211*

### test_subcontractor_sourced_item

**Category**: workflow  
**Description**: Workflow: test subcontractor sourced item  
**Expected**: self.assertEqual(bom_items, supplied_items)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_code = '_Test Subcontracted FG Item 1'
set_backflush_based_on('Material Transferred for Subcontract')
if not frappe.db.exists('Item', item_code):
    make_item(item_code, {'is_stock_item': 1, 'is_sub_contracted_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 1'):
    make_item('Test Extra Item 1', {'is_stock_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 2'):
    make_item('Test Extra Item 2', {'is_stock_item': 1, 'stock_uom': 'Nos'})
if not frappe.db.exists('Item', 'Test Extra Item 3'):
    make_item('Test Extra Item 3', {'is_stock_item': 1, 'stock_uom': 'Nos'})
bom = frappe.get_doc({'doctype': 'BOM', 'is_default': 1, 'item': item_code, 'currency': 'USD', 'quantity': 1, 'company': '_Test Company'})
for item in ['Test Extra Item 1', 'Test Extra Item 2']:
    item_doc = frappe.get_doc('Item', item)
    bom.append('items', {'item_code': item, 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': item_doc.valuation_rate})
bom.append('items', {'item_code': 'Test Extra Item 3', 'qty': 1, 'uom': item_doc.stock_uom, 'stock_uom': item_doc.stock_uom, 'rate': 0, 'sourced_by_supplier': 1})
bom.insert(ignore_permissions=True)
bom.update_cost()
bom.submit()
self.assertEqual(bom.items[2].rate, 0)
from erpnext.controllers.tests.test_subcontracting_controller import get_subcontracting_order, make_service_item
make_service_item('Subcontracted Service Item 1')
service_items = [{'warehouse': '_Test Warehouse - _TC', 'item_code': 'Subcontracted Service Item 1', 'qty': 1, 'rate': 100, 'fg_item': item_code, 'fg_item_qty': 1}]
sco = get_subcontracting_order(service_items=service_items, supplier_warehouse='_Test Warehouse 1 - _TC')
bom_items = sorted([d.item_code for d in bom.items if d.sourced_by_supplier != 1])
supplied_items = sorted([d.rm_item_code for d in sco.supplied_items])
self.assertEqual(bom_items, supplied_items)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:239*

### test_bom_tree_representation

**Category**: workflow  
**Description**: Workflow: test bom tree representation  
**Expected**: self.assertEqual(len(reqd_order), len(created_order))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bom_tree = {'Assembly': {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'SubAssembly2': {'ChildPart3': {}}, 'SubAssembly3': {'SubSubAssy1': {'ChildPart4': {}}}, 'ChildPart5': {}, 'ChildPart6': {}, 'SubAssembly4': {'SubSubAssy2': {'ChildPart7': {}}}}}
parent_bom = create_nested_bom(bom_tree, prefix='')
created_tree = parent_bom.get_tree_representation()
reqd_order = level_order_traversal(bom_tree)[1:]
created_order = created_tree.level_order_traversal()
self.assertEqual(len(reqd_order), len(created_order))
for reqd_item, created_item in zip(reqd_order, created_order, strict=False):
    self.assertEqual(reqd_item, created_item.item_code)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:321*

### test_generated_variant_bom

**Category**: workflow  
**Description**: Workflow: test generated variant bom  
**Expected**: self.assertEqual(len(reqd_order), len(created_order))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
from erpnext.controllers.item_variant import create_variant
template_item = make_item('_TestTemplateItem', {'has_variants': 1, 'attributes': [{'attribute': 'Test Size'}]})
variant = create_variant(template_item.item_code, {'Test Size': 'Large'})
variant.insert(ignore_if_duplicate=True)
bom_tree = {template_item.item_code: {'SubAssembly1': {'ChildPart1': {}, 'ChildPart2': {}}, 'ChildPart5': {}}}
template_bom = create_nested_bom(bom_tree, prefix='')
variant_bom = make_variant_bom(template_bom.name, template_bom.name, variant.item_code, variant_items=[])
variant_bom.save()
reqd_order = template_bom.get_tree_representation().level_order_traversal()
created_order = variant_bom.get_tree_representation().level_order_traversal()
self.assertEqual(len(reqd_order), len(created_order))
for reqd_item, created_item in zip(reqd_order, created_order, strict=False):
    self.assertEqual(reqd_item.item_code, created_item.item_code)
    self.assertEqual(reqd_item.qty, created_item.qty)
    self.assertEqual(reqd_item.exploded_qty, created_item.exploded_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:347*

### test_bom_recursion_1st_level

**Category**: workflow  
**Description**: Workflow: BOM should not allow BOM item again in child  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'BOM should not allow BOM item again in child'
item_code = make_item(properties={'is_stock_item': 1}).name
bom = frappe.new_doc('BOM')
bom.item = item_code
bom.append('items', frappe._dict(item_code=item_code))
bom.save()
with self.assertRaises(BOMRecursionError):
    bom.items[0].bom_no = bom.name
    bom.save()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom/test_bom.py:388*

### test_bom_sub_assembly

**Category**: workflow  
**Description**: Workflow: test bom sub assembly  
**Expected**: self.assertEqual(doc.items[0].amount, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_items()

final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM with Sub Assembly', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_sub_assembly(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, bom_item={'item_code': 'Frame Assembly', 'qty': 1, 'items': [{'item_code': 'Frame', 'qty': 1}, {'item_code': 'Fork', 'qty': 1}]})
doc.reload()
self.assertEqual(doc.items[0].item_code, 'Frame Assembly')
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Frame Assembly')
        self.assertEqual(row.fg_reference_id, doc.items[0].name)
self.assertEqual(doc.items[0].amount, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:20*

### test_bom_raw_material

**Category**: workflow  
**Description**: Workflow: test bom raw material  
**Expected**: self.assertEqual(doc.raw_material_cost, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_items()

final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM with Raw Material', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')
self.assertEqual(doc.items[0].qty, 2)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Bicycle')
        self.assertEqual(row.fg_reference_id, doc.name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:75*

### test_convert_to_sub_assembly

**Category**: workflow  
**Description**: Workflow: test convert to sub assembly  
**Expected**: self.assertEqual(doc.raw_material_cost, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_items()

final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Pedal Assembly')
        self.assertEqual(row.qty, 2.0)
        self.assertEqual(row.fg_reference_id, doc.items[0].name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:119*

### test_make_boms_from_bom_creator

**Category**: workflow  
**Description**: Workflow: test make boms from bom creator  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
create_items()

final_product = 'Bicycle Test'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM Test', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
doc.submit()
doc.create_boms()
doc.reload()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
doc.create_boms()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:187*

### test_bom_sub_assembly

**Category**: workflow  
**Description**: Workflow: test bom sub assembly  
**Expected**: self.assertEqual(doc.items[0].amount, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM with Sub Assembly', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_sub_assembly(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, bom_item={'item_code': 'Frame Assembly', 'qty': 1, 'items': [{'item_code': 'Frame', 'qty': 1}, {'item_code': 'Fork', 'qty': 1}]})
doc.reload()
self.assertEqual(doc.items[0].item_code, 'Frame Assembly')
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Frame Assembly')
        self.assertEqual(row.fg_reference_id, doc.items[0].name)
self.assertEqual(doc.items[0].amount, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:20*

### test_bom_raw_material

**Category**: workflow  
**Description**: Workflow: test bom raw material  
**Expected**: self.assertEqual(doc.raw_material_cost, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM with Raw Material', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')
self.assertEqual(doc.items[0].qty, 2)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Bicycle')
        self.assertEqual(row.fg_reference_id, doc.name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:75*

### test_convert_to_sub_assembly

**Category**: workflow  
**Description**: Workflow: test convert to sub assembly  
**Expected**: self.assertEqual(doc.raw_material_cost, fg_valuation_rate)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
final_product = 'Bicycle'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
fg_valuation_rate = 0
for row in doc.items:
    if row.fg_item == final_product:
        fg_valuation_rate += row.amount
    if not row.is_expandable:
        self.assertEqual(row.fg_item, 'Pedal Assembly')
        self.assertEqual(row.qty, 2.0)
        self.assertEqual(row.fg_reference_id, doc.items[0].name)
self.assertEqual(doc.raw_material_cost, fg_valuation_rate)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:119*

### test_make_boms_from_bom_creator

**Category**: workflow  
**Description**: Workflow: test make boms from bom creator  
**Expected**: self.assertEqual(len(data), 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
final_product = 'Bicycle Test'
make_item(final_product, {'item_group': 'Raw Material', 'stock_uom': 'Nos'})
doc = make_bom_creator(name='Bicycle BOM Test', company='_Test Company', item_code=final_product, qty=1, rm_cosy_as_per='Valuation Rate', currency='INR', plc_conversion_rate=1, conversion_rate=1)
add_item(parent=doc.name, fg_item=final_product, fg_reference_id=doc.name, item_code='Pedal Assembly', qty=2)
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 0)
add_sub_assembly(convert_to_sub_assembly=1, parent=doc.name, fg_item=final_product, fg_reference_id=doc.items[0].name, bom_item={'item_code': 'Pedal Assembly', 'qty': 2, 'items': [{'item_code': 'Pedal Body', 'qty': 2}, {'item_code': 'Pedal Axle', 'qty': 2}]})
doc.reload()
self.assertEqual(doc.items[0].is_expandable, 1)
doc.submit()
doc.create_boms()
doc.reload()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
doc.create_boms()
data = frappe.get_all('BOM', filters={'bom_creator': doc.name, 'docstatus': 1})
self.assertEqual(len(data), 2)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:187*

### test_bom_replace_for_root_bom

**Category**: workflow  
**Description**: Workflow: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

'\n\t\t- B-Item A (Root Item)\n\t\t        - B-Item B\n\t\t                - B-Item C\n\t\t        - B-Item D\n\t\t                - B-Item E\n\t\t                        - B-Item F\n\n\t\tCreate New BOM for B-Item E with B-Item G and replace it in the above BOM.\n\t\t'
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
from erpnext.stock.doctype.item.test_item import make_item
items = ['B-Item A', 'B-Item B', 'B-Item C', 'B-Item D', 'B-Item E', 'B-Item F', 'B-Item G']
for item_code in items:
    if not frappe.db.exists('Item', item_code):
        make_item(item_code)
for item_code in items:
    remove_bom(item_code)
bom_tree = {'B-Item A': {'B-Item B': {'B-Item C': {}}, 'B-Item D': {'B-Item E': {'B-Item F': {}}}}}
root_bom = create_nested_bom(bom_tree, prefix='')
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item F']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
old_bom = frappe.db.get_value('BOM', {'item': 'B-Item E'}, 'name')
bom_tree = {'B-Item E': {'B-Item G': {}}}
new_bom = create_nested_bom(bom_tree, prefix='')
enqueue_replace_bom(boms=frappe._dict(current_bom=old_bom, new_bom=new_bom.name))
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item G']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:60*

### test_bom_replace_for_root_bom

**Category**: workflow  
**Description**: Workflow: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
'\n\t\t- B-Item A (Root Item)\n\t\t        - B-Item B\n\t\t                - B-Item C\n\t\t        - B-Item D\n\t\t                - B-Item E\n\t\t                        - B-Item F\n\n\t\tCreate New BOM for B-Item E with B-Item G and replace it in the above BOM.\n\t\t'
from erpnext.manufacturing.doctype.bom.test_bom import create_nested_bom
from erpnext.stock.doctype.item.test_item import make_item
items = ['B-Item A', 'B-Item B', 'B-Item C', 'B-Item D', 'B-Item E', 'B-Item F', 'B-Item G']
for item_code in items:
    if not frappe.db.exists('Item', item_code):
        make_item(item_code)
for item_code in items:
    remove_bom(item_code)
bom_tree = {'B-Item A': {'B-Item B': {'B-Item C': {}}, 'B-Item D': {'B-Item E': {'B-Item F': {}}}}}
root_bom = create_nested_bom(bom_tree, prefix='')
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item F']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
old_bom = frappe.db.get_value('BOM', {'item': 'B-Item E'}, 'name')
bom_tree = {'B-Item E': {'B-Item G': {}}}
new_bom = create_nested_bom(bom_tree, prefix='')
enqueue_replace_bom(boms=frappe._dict(current_bom=old_bom, new_bom=new_bom.name))
exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
exploded_items = [item.item_code for item in exploded_items]
expected_exploded_items = ['B-Item C', 'B-Item G']
self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:60*

### test_replace_bom

**Category**: workflow  
**Description**: Workflow: test replace bom  
**Expected**: self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
current_bom = 'BOM-_Test Item Home Desktop Manufactured-001'
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
boms = frappe._dict(current_bom=current_bom, new_bom=bom_doc.name)
enqueue_replace_bom(boms=boms)
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:24*

### test_bom_cost

**Category**: workflow  
**Description**: Workflow: test bom cost  
**Expected**: self.assertEqual(doc.total_cost, 200)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for item in ['BOM Cost Test Item 1', 'BOM Cost Test Item 2', 'BOM Cost Test Item 3']:
    item_doc = create_item(item, valuation_rate=100)
    if item_doc.valuation_rate != 100.0:
        frappe.db.set_value('Item', item_doc.name, 'valuation_rate', 100)
bom_no = frappe.db.get_value('BOM', {'item': 'BOM Cost Test Item 1'}, 'name')
if not bom_no:
    doc = make_bom(item='BOM Cost Test Item 1', raw_materials=['BOM Cost Test Item 2', 'BOM Cost Test Item 3'], currency='INR')
else:
    doc = frappe.get_doc('BOM', bom_no)
self.assertEqual(doc.total_cost, 200)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 200)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 300)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 100)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 200)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:38*

### test_replace_bom

**Category**: workflow  
**Description**: Workflow: test replace bom  
**Expected**: self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
current_bom = 'BOM-_Test Item Home Desktop Manufactured-001'
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
boms = frappe._dict(current_bom=current_bom, new_bom=bom_doc.name)
enqueue_replace_bom(boms=boms)
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:24*

### test_bom_cost

**Category**: workflow  
**Description**: Workflow: test bom cost  
**Expected**: self.assertEqual(doc.total_cost, 200)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
for item in ['BOM Cost Test Item 1', 'BOM Cost Test Item 2', 'BOM Cost Test Item 3']:
    item_doc = create_item(item, valuation_rate=100)
    if item_doc.valuation_rate != 100.0:
        frappe.db.set_value('Item', item_doc.name, 'valuation_rate', 100)
bom_no = frappe.db.get_value('BOM', {'item': 'BOM Cost Test Item 1'}, 'name')
if not bom_no:
    doc = make_bom(item='BOM Cost Test Item 1', raw_materials=['BOM Cost Test Item 2', 'BOM Cost Test Item 3'], currency='INR')
else:
    doc = frappe.get_doc('BOM', bom_no)
self.assertEqual(doc.total_cost, 200)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 200)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 300)
frappe.db.set_value('Item', 'BOM Cost Test Item 2', 'valuation_rate', 100)
update_cost_in_all_boms_in_test()
doc.load_from_db()
self.assertEqual(doc.total_cost, 200)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:38*

### test_bom_stock_calculated

**Category**: workflow  
**Description**: Workflow: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.fg_item, self.rm_items = create_items()
self.boms = create_boms(self.fg_item, self.rm_items)

qty_to_make = 10
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[0].name})[1]
expected_data = get_expected_data(self.boms[0], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[1].name})[1]
expected_data = get_expected_data(self.boms[1], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[2].name})[1]
expected_data = get_expected_data(self.boms[2], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:18*

### test_bom_stock_calculated

**Category**: workflow  
**Description**: Workflow: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
qty_to_make = 10
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[0].name})[1]
expected_data = get_expected_data(self.boms[0], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[1].name})[1]
expected_data = get_expected_data(self.boms[1], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
data = bom_stock_calculated_report(filters={'qty_to_make': qty_to_make, 'bom': self.boms[2].name})[1]
expected_data = get_expected_data(self.boms[2], qty_to_make)
self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:18*

### test_sales_order_creation

**Category**: workflow  
**Description**: Workflow: test sales order creation  
**Expected**: self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.flags.args = frappe._dict()

bo = make_blanket_order(blanket_order_type='Selling')
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 10
so.submit()
self.assertEqual(so.doctype, 'Sales Order')
self.assertEqual(len(so.get('items')), len(bo.get('items')))
self.assertEqual(so.items[0].rate, bo.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(so.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Sales Order'
so1 = make_order(bo.name)
so1.currency = get_company_currency(so1.company)
self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:17*

### test_purchase_order_creation

**Category**: workflow  
**Description**: Workflow: test purchase order creation  
**Expected**: self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.flags.args = frappe._dict()

bo = make_blanket_order(blanket_order_type='Purchasing')
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 10
po.submit()
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(bo.get('items')))
self.assertEqual(po.items[0].rate, po.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(po.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Purchase Order'
po1 = make_order(bo.name)
po1.currency = get_company_currency(po1.company)
self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:42*

### test_blanket_order_allowance

**Category**: workflow  
**Description**: Workflow: test blanket order allowance  
**Expected**: self.assertRaises(frappe.ValidationError, po.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.flags.args = frappe._dict()

bo = make_blanket_order(blanket_order_type='Selling', quantity=100)
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 110
self.assertRaises(frappe.ValidationError, so.submit)
frappe.db.set_single_value('Selling Settings', 'blanket_order_allowance', 10)
so.submit()
bo = make_blanket_order(blanket_order_type='Purchasing', quantity=100)
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 110
self.assertRaises(frappe.ValidationError, po.submit)
frappe.db.set_single_value('Buying Settings', 'blanket_order_allowance', 10)
po.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:67*

### test_party_item_code

**Category**: workflow  
**Description**: Workflow: test party item code  
**Expected**: self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
frappe.flags.args = frappe._dict()

item_doc = make_item('_Test Item 1 for Blanket Order')
item_code = item_doc.name
customer = '_Test Customer'
supplier = '_Test Supplier'
if not frappe.db.exists('Item Customer Detail', {'customer_name': customer, 'parent': item_code}):
    item_doc.append('customer_items', {'customer_name': customer, 'ref_code': 'CUST-REF-1'})
    item_doc.save()
if not frappe.db.exists('Item Supplier', {'supplier': supplier, 'parent': item_code}):
    item_doc.append('supplier_items', {'supplier': supplier, 'supplier_part_no': 'SUPP-PART-1'})
    item_doc.save()
bo = make_blanket_order(blanket_order_type='Selling', customer=customer, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'CUST-REF-1')
bo = make_blanket_order(blanket_order_type='Purchasing', supplier=supplier, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:94*

### test_sales_order_creation

**Category**: workflow  
**Description**: Workflow: test sales order creation  
**Expected**: self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bo = make_blanket_order(blanket_order_type='Selling')
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 10
so.submit()
self.assertEqual(so.doctype, 'Sales Order')
self.assertEqual(len(so.get('items')), len(bo.get('items')))
self.assertEqual(so.items[0].rate, bo.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(so.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Sales Order'
so1 = make_order(bo.name)
so1.currency = get_company_currency(so1.company)
self.assertEqual(so1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:17*

### test_purchase_order_creation

**Category**: workflow  
**Description**: Workflow: test purchase order creation  
**Expected**: self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bo = make_blanket_order(blanket_order_type='Purchasing')
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 10
po.submit()
self.assertEqual(po.doctype, 'Purchase Order')
self.assertEqual(len(po.get('items')), len(bo.get('items')))
self.assertEqual(po.items[0].rate, po.items[0].rate)
bo = frappe.get_doc('Blanket Order', bo.name)
self.assertEqual(po.items[0].qty, bo.items[0].ordered_qty)
frappe.flags.args.doctype = 'Purchase Order'
po1 = make_order(bo.name)
po1.currency = get_company_currency(po1.company)
self.assertEqual(po1.items[0].qty, bo.items[0].qty - bo.items[0].ordered_qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:42*

### test_blanket_order_allowance

**Category**: workflow  
**Description**: Workflow: test blanket order allowance  
**Expected**: self.assertRaises(frappe.ValidationError, po.submit)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
bo = make_blanket_order(blanket_order_type='Selling', quantity=100)
frappe.flags.args.doctype = 'Sales Order'
so = make_order(bo.name)
so.currency = get_company_currency(so.company)
so.delivery_date = today()
so.items[0].qty = 110
self.assertRaises(frappe.ValidationError, so.submit)
frappe.db.set_single_value('Selling Settings', 'blanket_order_allowance', 10)
so.submit()
bo = make_blanket_order(blanket_order_type='Purchasing', quantity=100)
frappe.flags.args.doctype = 'Purchase Order'
po = make_order(bo.name)
po.currency = get_company_currency(po.company)
po.schedule_date = today()
po.items[0].qty = 110
self.assertRaises(frappe.ValidationError, po.submit)
frappe.db.set_single_value('Buying Settings', 'blanket_order_allowance', 10)
po.submit()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:67*

### test_party_item_code

**Category**: workflow  
**Description**: Workflow: test party item code  
**Expected**: self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
item_doc = make_item('_Test Item 1 for Blanket Order')
item_code = item_doc.name
customer = '_Test Customer'
supplier = '_Test Supplier'
if not frappe.db.exists('Item Customer Detail', {'customer_name': customer, 'parent': item_code}):
    item_doc.append('customer_items', {'customer_name': customer, 'ref_code': 'CUST-REF-1'})
    item_doc.save()
if not frappe.db.exists('Item Supplier', {'supplier': supplier, 'parent': item_code}):
    item_doc.append('supplier_items', {'supplier': supplier, 'supplier_part_no': 'SUPP-PART-1'})
    item_doc.save()
bo = make_blanket_order(blanket_order_type='Selling', customer=customer, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'CUST-REF-1')
bo = make_blanket_order(blanket_order_type='Purchasing', supplier=supplier, item_code=item_code)
self.assertEqual(bo.items[0].party_item_code, 'SUPP-PART-1')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:94*

### test_reserved_qty_for_partial_completion

**Category**: workflow  
**Description**: Workflow: test reserved qty for partial completion  
**Expected**: self.assertEqual(cint(bin1_at_completion.reserved_qty_for_production), reserved_qty_on_submission - 1)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

item = '_Test Item'
warehouse = '_Test Warehouse - _TC'
bin1_at_start = get_bin(item, warehouse)
bin1_at_start.update_reserved_qty_for_production()
wo_order = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=warehouse, skip_transfer=1)
reserved_qty_on_submission = cint(get_bin(item, warehouse).reserved_qty_for_production)
self.assertEqual(cint(bin1_at_start.reserved_qty_for_production) + 2, reserved_qty_on_submission)
test_stock_entry.make_stock_entry(item_code='_Test Item', target=warehouse, qty=100, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=warehouse, qty=100, basic_rate=100)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 1))
s.submit()
bin1_at_completion = get_bin(item, warehouse)
self.assertEqual(cint(bin1_at_completion.reserved_qty_for_production), reserved_qty_on_submission - 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:121*

### test_reserved_qty_for_production_on_stock_entry

**Category**: workflow  
**Description**: Workflow: test reserved qty for production on stock entry  
**Expected**: self.assertEqual(cint(bin1_on_end_production.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

test_stock_entry.make_stock_entry(item_code='_Test Item', target=self.warehouse, qty=100, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target=self.warehouse, qty=100, basic_rate=100)
self.test_reserved_qty_for_production_submit()
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Material Transfer for Manufacture', 2))
s.submit()
bin1_on_start_production = get_bin(self.item, self.warehouse)
self.assertEqual(cint(self.bin1_at_start.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
self.assertEqual(cint(self.bin1_at_start.projected_qty), cint(bin1_on_start_production.projected_qty) + 2)
s = frappe.get_doc(make_stock_entry(self.wo_order.name, 'Manufacture', 2))
bin1_on_end_production = get_bin(self.item, self.warehouse)
self.assertEqual(cint(bin1_on_end_production.reserved_qty_for_production), cint(bin1_on_start_production.reserved_qty_for_production))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:200*

### test_reserved_qty_for_production_closed

**Category**: workflow  
**Description**: Workflow: test reserved qty for production closed  
**Expected**: self.assertEqual(bin_before.reserved_qty_for_production, bin_after.reserved_qty_for_production)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

wo1 = make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
item = wo1.required_items[0].item_code
bin_before = get_bin(item, self.warehouse)
bin_before.update_reserved_qty_for_production()
make_wo_order_test_record(item='_Test FG Item', qty=2, source_warehouse=self.warehouse)
close_work_order(wo1.name, 'Closed')
bin_after = get_bin(item, self.warehouse)
self.assertEqual(bin_before.reserved_qty_for_production, bin_after.reserved_qty_for_production)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:237*

### test_backflush_qty_for_overpduction_manufacture

**Category**: workflow  
**Description**: Workflow: test backflush qty for overpduction manufacture  
**Expected**: self.assertEqual(s1.items[1].qty, 100)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

cancel_stock_entry = []
allow_overproduction('overproduction_percentage_for_work_order', 30)
wo_order = make_wo_order_test_record(planned_start_date=now(), qty=100)
ste1 = test_stock_entry.make_stock_entry(item_code='_Test Item', target='_Test Warehouse - _TC', qty=120, basic_rate=5000.0)
ste2 = test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='_Test Warehouse - _TC', qty=240, basic_rate=1000.0)
cancel_stock_entry.extend([ste1.name, ste2.name])
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 60))
s.submit()
cancel_stock_entry.append(s.name)
s1 = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 50))
s1.submit()
cancel_stock_entry.append(s1.name)
self.assertEqual(s1.items[0].qty, 50)
self.assertEqual(s1.items[1].qty, 100)
cancel_stock_entry.reverse()
for ste in cancel_stock_entry:
    doc = frappe.get_doc('Stock Entry', ste)
    doc.cancel()
allow_overproduction('overproduction_percentage_for_work_order', 0)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:249*

### test_scrap_material_qty

**Category**: workflow  
**Description**: Workflow: test scrap material qty  
**Expected**: self.assertEqual(wo_order_details.produced_qty, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

wo_order = make_wo_order_test_record(planned_start_date=now(), qty=2)
test_stock_entry.make_stock_entry(item_code='_Test Item', target='Stores - _TC', qty=10, basic_rate=5000.0)
test_stock_entry.make_stock_entry(item_code='_Test Item Home Desktop 100', target='Stores - _TC', qty=10, basic_rate=1000.0)
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Material Transfer for Manufacture', 2))
for d in s.get('items'):
    d.s_warehouse = 'Stores - _TC'
s.insert()
s.submit()
s = frappe.get_doc(make_stock_entry(wo_order.name, 'Manufacture', 2))
s.insert()
s.submit()
wo_order_details = frappe.db.get_value('Work Order', wo_order.name, ['scrap_warehouse', 'qty', 'produced_qty', 'bom_no'], as_dict=1)
scrap_item_details = get_scrap_item_details(wo_order_details.bom_no)
self.assertEqual(wo_order_details.produced_qty, 2)
for item in s.items:
    if item.bom_no and item.item_code in scrap_item_details:
        self.assertEqual(wo_order_details.scrap_warehouse, item.t_warehouse)
        self.assertEqual(flt(wo_order_details.qty) * flt(scrap_item_details[item.item_code]), item.qty)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:337*

### test_work_order_with_non_stock_item

**Category**: workflow  
**Description**: Workflow: test work order with non stock item  
**Expected**: self.assertEqual(ste.total_additional_costs, 1000)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

items = {'Finished Good Test Item For non stock': 1, '_Test FG Item': 1, '_Test FG Non Stock Item': 0}
for item, is_stock_item in items.items():
    make_item(item, {'is_stock_item': is_stock_item})
if not frappe.db.get_value('Item Price', {'item_code': '_Test FG Non Stock Item'}):
    frappe.get_doc({'doctype': 'Item Price', 'item_code': '_Test FG Non Stock Item', 'price_list_rate': 1000, 'price_list': '_Test Price List India'}).insert(ignore_permissions=True)
fg_item = 'Finished Good Test Item For non stock'
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
if not frappe.db.get_value('BOM', {'item': fg_item, 'docstatus': 1}):
    bom = make_bom(item=fg_item, rate=1000, raw_materials=['_Test FG Item', '_Test FG Non Stock Item'], do_not_save=True)
    bom.rm_cost_as_per = 'Price List'
    bom.buying_price_list = '_Test Price List India'
    bom.currency = 'INR'
    bom.save()
wo = make_wo_order_test_record(production_item=fg_item)
se = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
se.insert()
se.submit()
ste = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
ste.insert()
self.assertEqual(len(ste.additional_costs), 1)
self.assertEqual(ste.total_additional_costs, 1000)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:414*

### test_job_card

**Category**: workflow  
**Description**: Workflow: test job card  
**Expected**: self.assertEqual(len(job_cards), len(bom.operations))  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

stock_entries = []
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
work_order = make_wo_order_test_record(item=bom.item, qty=1, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC')
for row in work_order.required_items:
    stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
    stock_entries.append(stock_entry_doc)
ste = frappe.get_doc(make_stock_entry(work_order.name, 'Material Transfer for Manufacture', 1))
ste.submit()
stock_entries.append(ste)
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
self.assertEqual(len(job_cards), len(bom.operations))
for _i, job_card in enumerate(job_cards):
    doc = frappe.get_doc('Job Card', job_card)
    for row in doc.scheduled_time_logs:
        doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 0})
    doc.time_logs[0].completed_qty = 1
    doc.submit()
ste1 = frappe.get_doc(make_stock_entry(work_order.name, 'Manufacture', 1))
ste1.submit()
stock_entries.append(ste1)
for job_card in job_cards:
    doc = frappe.get_doc('Job Card', job_card)
    self.assertRaises(JobCardCancelError, doc.cancel)
stock_entries.reverse()
for stock_entry in stock_entries:
    stock_entry.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:462*

### test_work_order_material_transferred_qty_with_process_loss

**Category**: workflow  
**Description**: Workflow: test work order material transferred qty with process loss  
**Expected**: self.assertEqual(work_order.material_transferred_for_manufacturing, 2)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

stock_entries = []
bom = frappe.get_doc('BOM', {'docstatus': 1, 'with_operations': 1, 'company': '_Test Company'})
work_order = make_wo_order_test_record(item=bom.item, qty=2, bom_no=bom.name, source_warehouse='_Test Warehouse - _TC', transfer_material_against='Job Card')
self.assertEqual(work_order.qty, 2)
for row in work_order.required_items:
    stock_entry_doc = test_stock_entry.make_stock_entry(item_code=row.item_code, target='_Test Warehouse - _TC', qty=row.required_qty, basic_rate=100)
    stock_entries.append(stock_entry_doc)
job_cards = frappe.get_all('Job Card', filters={'work_order': work_order.name}, order_by='creation asc')
for row in job_cards:
    transfer_entry_1 = make_stock_entry_from_jc(row.name)
    transfer_entry_1.submit()
    doc = frappe.get_doc('Job Card', row.name)
    for row in doc.scheduled_time_logs:
        doc.append('time_logs', {'from_time': row.from_time, 'to_time': row.to_time, 'time_in_mins': row.time_in_mins, 'completed_qty': 1})
    doc.save()
    doc.submit()
    self.assertEqual(doc.total_completed_qty, 1)
    self.assertEqual(doc.process_loss_qty, 1)
work_order.reload()
self.assertEqual(work_order.material_transferred_for_manufacturing, 2)
for row in work_order.operations:
    self.assertEqual(row.completed_qty, 1)
    self.assertEqual(row.process_loss_qty, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:513*

### test_capcity_planning

**Category**: workflow  
**Description**: Workflow: test capcity planning  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

frappe.db.set_single_value('Manufacturing Settings', {'disable_capacity_planning': 0, 'capacity_planning_for_days': 1})
data = frappe.get_cached_value('BOM', {'docstatus': 1, 'item': '_Test FG Item 2', 'with_operations': 1, 'company': '_Test Company'}, ['name', 'item'])
if data:
    bom, bom_item = data
    planned_start_date = add_months(today(), months=-1)
    work_order = make_wo_order_test_record(item=bom_item, qty=10, bom_no=bom, planned_start_date=planned_start_date)
    work_order1 = make_wo_order_test_record(item=bom_item, qty=30, bom_no=bom, planned_start_date=planned_start_date, do_not_submit=1)
    self.assertRaises(CapacityError, work_order1.submit)
    frappe.db.set_single_value('Manufacturing Settings', {'capacity_planning_for_days': 30})
    work_order1.reload()
    work_order1.submit()
    self.assertTrue(work_order1.docstatus, 1)
    work_order1.cancel()
    work_order.cancel()
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:567*

### test_work_order_with_non_transfer_item

**Category**: workflow  
**Description**: Workflow: test work order with non transfer item  
**Expected**: self.assertEqual(len(ste1.items), 3)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
# Setup
self.warehouse = '_Test Warehouse 2 - _TC'
self.item = '_Test Item'
prepare_data_for_backflush_based_on_materials_transferred()

frappe.db.set_single_value('Manufacturing Settings', 'backflush_raw_materials_based_on', 'BOM')
items = {'Finished Good Transfer Item': 1, '_Test FG Item': 1, '_Test FG Item 1': 0}
for item, allow_transfer in items.items():
    make_item(item, {'include_item_in_manufacturing': allow_transfer})
fg_item = 'Finished Good Transfer Item'
test_stock_entry.make_stock_entry(item_code='_Test FG Item', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
test_stock_entry.make_stock_entry(item_code='_Test FG Item 1', target='_Test Warehouse - _TC', qty=1, basic_rate=100)
if not frappe.db.get_value('BOM', {'item': fg_item}):
    make_bom(item=fg_item, raw_materials=['_Test FG Item', '_Test FG Item 1'])
wo = make_wo_order_test_record(production_item=fg_item)
ste = frappe.get_doc(make_stock_entry(wo.name, 'Material Transfer for Manufacture', 1))
ste.insert()
ste.submit()
self.assertEqual(len(ste.items), 1)
ste1 = frappe.get_doc(make_stock_entry(wo.name, 'Manufacture', 1))
self.assertEqual(len(ste1.items), 3)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/work_order/test_work_order.py:601*

### test_update_bom_operation_rate

**Category**: workflow  
**Description**: Workflow: test update bom operation rate  
**Expected**: self.assertEqual(bom_doc.operations[1].hour_rate, 250)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_rent': 1000, 'time_in_mins': 60}]
for row in operations:
    make_workstation(row)
    make_operation(row)
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 60}]
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
w1 = frappe.get_doc('Workstation', '_Test Workstation A')
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 300
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 300)
self.assertEqual(bom_doc.operations[0].hour_rate, 300)
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 250
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 250)
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
self.assertEqual(bom_doc.operations[1].hour_rate, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:51*

### test_update_bom_operation_rate

**Category**: workflow  
**Description**: Workflow: test update bom operation rate  
**Expected**: self.assertEqual(bom_doc.operations[1].hour_rate, 250)  
**Confidence**: 0.90  
**Tags**: workflow, integration  

```python
operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'hour_rate_rent': 300, 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation B', 'hour_rate_rent': 1000, 'time_in_mins': 60}]
for row in operations:
    make_workstation(row)
    make_operation(row)
test_routing_operations = [{'operation': 'Test Operation A', 'workstation': '_Test Workstation A', 'time_in_mins': 60}, {'operation': 'Test Operation B', 'workstation': '_Test Workstation A', 'time_in_mins': 60}]
routing_doc = create_routing(routing_name='Routing Test', operations=test_routing_operations)
bom_doc = setup_bom(item_code='_Testing Item', routing=routing_doc.name, currency='INR')
w1 = frappe.get_doc('Workstation', '_Test Workstation A')
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 300
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 300)
self.assertEqual(bom_doc.operations[0].hour_rate, 300)
for row in w1.workstation_costs:
    if row.operating_component == _('Rent'):
        row.operating_cost = 250
        break
w1.save()
bom_doc.update_cost()
bom_doc.reload()
self.assertEqual(w1.hour_rate, 250)
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
self.assertEqual(bom_doc.operations[1].hour_rate, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:51*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(routing_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.85  

```python
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:87*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[0].time_in_mins, 30)  
**Confidence**: 0.85  

```python
bom_doc.reload()
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:93*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.85  

```python
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:94*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(routing_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.85  

```python
self.assertEqual(routing_doc.operations[0].time_in_mins, 30)
self.assertEqual(routing_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:87*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[0].time_in_mins, 30)  
**Confidence**: 0.85  

```python
bom_doc.reload()
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:93*

### test_update_bom_operation_time

**Category**: method_call  
**Description**: Update cost shouldn't update routing times.  
**Expected**: self.assertEqual(bom_doc.operations[1].time_in_mins, 20)  
**Confidence**: 0.85  

```python
self.assertEqual(bom_doc.operations[0].time_in_mins, 30)
self.assertEqual(bom_doc.operations[1].time_in_mins, 20)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/routing/test_routing.py:94*

### test_bom_sub_assembly

**Category**: method_call  
**Description**: test bom sub assembly  
**Expected**: self.assertEqual(doc.items[0].item_code, 'Frame Assembly')  
**Confidence**: 0.85  

```python
# Setup
create_items()

doc.reload()
self.assertEqual(doc.items[0].item_code, 'Frame Assembly')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:61*

### test_bom_raw_material

**Category**: method_call  
**Description**: test bom raw material  
**Expected**: self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')  
**Confidence**: 0.85  

```python
# Setup
create_items()

doc.reload()
self.assertEqual(doc.items[0].item_code, 'Pedal Assembly')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_creator/test_bom_creator.py:104*

### test_bom_update_log_completion

**Category**: method_call  
**Description**: Test if BOM Update Log handles job completion correctly.  
**Expected**: self.assertEqual(log.status, 'Completed')  
**Confidence**: 0.85  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

log.reload()
self.assertEqual(log.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:57*

### test_bom_update_log_completion

**Category**: method_call  
**Description**: Test if BOM Update Log handles job completion correctly.  
**Expected**: self.assertEqual(log.status, 'Completed')  
**Confidence**: 0.85  

```python
log.reload()
self.assertEqual(log.status, 'Completed')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:57*

### test_replace_bom

**Category**: method_call  
**Description**: test replace bom  
**Expected**: self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))  
**Confidence**: 0.85  

```python
enqueue_replace_bom(boms=boms)
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:32*

### test_replace_bom

**Category**: method_call  
**Description**: test replace bom  
**Expected**: self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))  
**Confidence**: 0.85  

```python
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:34*

### test_bom_cost

**Category**: method_call  
**Description**: test bom cost  
**Expected**: self.assertEqual(doc.total_cost, 300)  
**Confidence**: 0.85  

```python
doc.load_from_db()
self.assertEqual(doc.total_cost, 300)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:59*

### test_bom_cost

**Category**: method_call  
**Description**: test bom cost  
**Expected**: self.assertEqual(doc.total_cost, 200)  
**Confidence**: 0.85  

```python
doc.load_from_db()
self.assertEqual(doc.total_cost, 200)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:65*

### test_replace_bom

**Category**: method_call  
**Description**: test replace bom  
**Expected**: self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))  
**Confidence**: 0.85  

```python
enqueue_replace_bom(boms=boms)
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:32*

### test_replace_bom

**Category**: method_call  
**Description**: test replace bom  
**Expected**: self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))  
**Confidence**: 0.85  

```python
self.assertFalse(frappe.db.exists('BOM Item', {'bom_no': current_bom, 'docstatus': 1}))
self.assertTrue(frappe.db.exists('BOM Item', {'bom_no': bom_doc.name, 'docstatus': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_tool/test_bom_update_tool.py:34*

### test_sales_order_creation

**Category**: method_call  
**Description**: test sales order creation  
**Expected**: self.assertEqual(so.doctype, 'Sales Order')  
**Confidence**: 0.85  

```python
# Setup
frappe.flags.args = frappe._dict()

so.submit()
self.assertEqual(so.doctype, 'Sales Order')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:25*

### test_sales_order_creation

**Category**: method_call  
**Description**: test sales order creation  
**Expected**: self.assertEqual(len(so.get('items')), len(bo.get('items')))  
**Confidence**: 0.85  

```python
# Setup
frappe.flags.args = frappe._dict()

self.assertEqual(so.doctype, 'Sales Order')
self.assertEqual(len(so.get('items')), len(bo.get('items')))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/blanket_order/test_blanket_order.py:27*

### test_validate_timings

**Category**: method_call  
**Description**: test validate timings  
**Expected**: self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')  
**Confidence**: 0.85  

```python
check_if_within_operating_hours('_Test Workstation 1', 'Operation 1', '2013-02-02 10:00:00', '2013-02-02 20:00:00')
self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:23*

### test_validate_timings

**Category**: method_call  
**Description**: test validate timings  
**Expected**: self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')  
**Confidence**: 0.85  

```python
self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')
self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:26*

### test_validate_timings

**Category**: method_call  
**Description**: test validate timings  
**Expected**: self.assertRaises(WorkstationHolidayError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-01 10:00:00', '2013-02-02 20:00:00')  
**Confidence**: 0.85  

```python
self.assertRaises(NotInWorkingHoursError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-02 05:00:00', '2013-02-02 20:00:00')
self.assertRaises(WorkstationHolidayError, check_if_within_operating_hours, '_Test Workstation 1', 'Operation 1', '2013-02-01 10:00:00', '2013-02-02 20:00:00')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:34*

### test_update_bom_operation_rate

**Category**: method_call  
**Description**: test update bom operation rate  
**Expected**: self.assertEqual(w1.hour_rate, 300)  
**Confidence**: 0.85  

```python
bom_doc.reload()
self.assertEqual(w1.hour_rate, 300)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:86*

### test_update_bom_operation_rate

**Category**: method_call  
**Description**: test update bom operation rate  
**Expected**: self.assertEqual(bom_doc.operations[0].hour_rate, 300)  
**Confidence**: 0.85  

```python
self.assertEqual(w1.hour_rate, 300)
self.assertEqual(bom_doc.operations[0].hour_rate, 300)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:87*

### test_update_bom_operation_rate

**Category**: method_call  
**Description**: test update bom operation rate  
**Expected**: self.assertEqual(w1.hour_rate, 250)  
**Confidence**: 0.85  

```python
bom_doc.reload()
self.assertEqual(w1.hour_rate, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:98*

### test_update_bom_operation_rate

**Category**: method_call  
**Description**: test update bom operation rate  
**Expected**: self.assertEqual(bom_doc.operations[0].hour_rate, 250)  
**Confidence**: 0.85  

```python
self.assertEqual(w1.hour_rate, 250)
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:99*

### test_update_bom_operation_rate

**Category**: method_call  
**Description**: test update bom operation rate  
**Expected**: self.assertEqual(bom_doc.operations[1].hour_rate, 250)  
**Confidence**: 0.85  

```python
self.assertEqual(bom_doc.operations[0].hour_rate, 250)
self.assertEqual(bom_doc.operations[1].hour_rate, 250)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/workstation/test_workstation.py:100*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate _dict: test bom stock report  
**Expected**: self.assertRaises(ValidationError, bom_stock_report, filters)  
**Confidence**: 0.80  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:28*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate bom_stock_report: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:38*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:47*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate bom_stock_report: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': self.warehouse, 'qty_to_produce': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:51*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.warehouse = '_Test Warehouse - _TC'
self.fg_item, self.rm_items = create_items()
make_stock_entry(target=self.warehouse, item_code=self.rm_items[0], qty=20, basic_rate=100)
make_stock_entry(target=self.warehouse, item_code=self.rm_items[1], qty=40, basic_rate=200)
self.bom = make_bom(item=self.fg_item, quantity=1, raw_materials=self.rm_items, rm_qty=10)

expected_data = get_expected_data(self.bom, self.warehouse, 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:60*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate _dict: test bom stock report  
**Expected**: self.assertRaises(ValidationError, bom_stock_report, filters)  
**Confidence**: 0.80  

```python
filters = frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 0})
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:28*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate bom_stock_report: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
data = bom_stock_report(frappe._dict({'bom': self.bom.name, 'warehouse': 'Stores - _TC', 'qty_to_produce': 1}))
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:38*

### test_bom_stock_report

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock report  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
expected_data = get_expected_data(self.bom, 'Stores - _TC', 1)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_report/test_bom_stock_report.py:47*

### test_bom_update_log_completion

**Category**: instantiation  
**Description**: Instantiate enqueue_replace_bom: Test if BOM Update Log handles job completion correctly.  
**Expected**: self.assertEqual(log.status, 'Completed')  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

log = enqueue_replace_bom(boms=self.boms)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:56*

### test_bom_replace_for_root_bom

**Category**: instantiation  
**Description**: Instantiate create_nested_bom: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

root_bom = create_nested_bom(bom_tree, prefix='')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:86*

### test_bom_replace_for_root_bom

**Category**: instantiation  
**Description**: Instantiate get_all: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:88*

### test_bom_replace_for_root_bom

**Category**: instantiation  
**Description**: Instantiate get_value: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

old_bom = frappe.db.get_value('BOM', {'item': 'B-Item E'}, 'name')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:96*

### test_bom_replace_for_root_bom

**Category**: instantiation  
**Description**: Instantiate create_nested_bom: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

new_bom = create_nested_bom(bom_tree, prefix='')
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:99*

### test_bom_replace_for_root_bom

**Category**: instantiation  
**Description**: Instantiate get_all: - B-Item A (Root Item)
        - B-Item B
                - B-Item C
        - B-Item D
                - B-Item E
                        - B-Item F

Create New BOM for B-Item E with B-Item G and replace it in the above BOM.  
**Expected**: self.assertEqual(sorted(exploded_items), sorted(expected_exploded_items))  
**Confidence**: 0.80  

```python
# Setup
bom_doc = frappe.copy_doc(self.globalTestRecords['BOM'][0])
bom_doc.items[1].item_code = '_Test Item'
bom_doc.insert()
self.boms = frappe._dict(current_bom='BOM-_Test Item Home Desktop Manufactured-001', new_bom=bom_doc.name)
self.new_bom_doc = bom_doc

exploded_items = frappe.get_all('BOM Explosion Item', filters={'parent': root_bom.name}, fields=['item_code'])
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/doctype/bom_update_log/test_bom_update_log.py:102*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.fg_item, self.rm_items = create_items()
self.boms = create_boms(self.fg_item, self.rm_items)

expected_data = get_expected_data(self.boms[0], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:28*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.fg_item, self.rm_items = create_items()
self.boms = create_boms(self.fg_item, self.rm_items)

expected_data = get_expected_data(self.boms[1], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:38*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
# Setup
self.fg_item, self.rm_items = create_items()
self.boms = create_boms(self.fg_item, self.rm_items)

expected_data = get_expected_data(self.boms[2], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:48*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
expected_data = get_expected_data(self.boms[0], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:28*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
expected_data = get_expected_data(self.boms[1], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:38*

### test_bom_stock_calculated

**Category**: instantiation  
**Description**: Instantiate get_expected_data: test bom stock calculated  
**Expected**: self.assertSetEqual(set((tuple(x) for x in data)), set((tuple(x) for x in expected_data)))  
**Confidence**: 0.80  

```python
expected_data = get_expected_data(self.boms[2], qty_to_make)
```

*Source: /Users/vovanduc/Code/dcnet/erpnext/erpnext/manufacturing/report/bom_stock_calculated/test_bom_stock_calculated.py:48*

