# API Reference: test_production_plan.py

**Language**: Python

**Source**: `doctype/production_plan/test_production_plan.py`

---

## Classes

### TestProductionPlan

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_production_plan_mr_creation(self)

Test if MRs are created for unavailable raw materials.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_start_date(self)

Test if Work Order has same Planned Start Date as Prod Plan.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_for_existing_ordered_qty(self)

- Enable 'ignore_existing_ordered_qty'.
- Test if MR Planning table pulls Raw Material Qty even if it is in stock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_projected_qty_cascading_across_multiple_sales_orders(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_with_non_stock_item(self)

Test if MR Planning table includes Non Stock RM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_without_multi_level(self)

Test MR Planning table for non exploded BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_without_multi_level_for_existing_ordered_qty(self)

- Disable 'ignore_existing_ordered_qty'.
- Test if MR Planning table avoids pulling Raw Material Qty as it is in stock for
non exploded BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_sales_orders(self)

Test if previously fulfilled SO (with WO) is pulled into Prod Plan.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_donot_allow_to_make_multiple_pp_against_same_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_based_bill_of_material(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_with_non_active_bom_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_combine_items(self)

Test combining FG items in Production Plan.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_subassembly_default_supplier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_for_subcontracting_po(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_for_mr_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_combine_subassembly(self)

Test combining Sub assembly items belonging to the same BOM in Prod Plan.
1) Red-Car -> Wheel (sub assembly) > BOM-WHEEL-001
2) Green-Car -> Wheel (sub assembly) > BOM-WHEEL-001

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_pp_to_mr_customer_provided(self)

Test Material Request from Production Plan for Customer Provided Item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_with_multi_level_bom(self)

Item Code       |       Qty     |
|Test BOM 1     |       1       |
|Test BOM 2     |       2       |
|Test BOM 3     |       3       |

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_warehouse_list_group(self)

Check if required child warehouses are returned.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_warehouse_list_single(self)

Check if same warehouse is returned in absence of child warehouses.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_sales_order_with_variant(self)

Check if Template BOM is fetched in absence of Variant BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_sales_order_items_for_product_bundle(self)

Testing the Planned Qty for Product Bundle Item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_work_order_for_production_plan_item(self)

Test producing Prod Plan (making WO) in parts.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_pending_qty_with_sales_order(self)

Test Prod Plan impact via: SO -> Prod Plan -> WO -> SE -> SE (cancel)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_pending_qty_independent_items(self)

Test Prod Plan impact if items are added independently (no from SO or MR).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_qty_based_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_planned_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_temporary_name_relinking(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_produced_qty_for_multi_level_bom_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_request_item_for_purchase_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_request_for_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_plan_for_material_requests(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_plan_for_work_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_plan_for_less_rm_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserved_qty_for_production_plan_for_material_requests_with_multi_UOM(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_from_warehouse_for_purchase_material_request(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_skip_available_qty_for_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sub_assembly_and_their_raw_materials_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_transfer_and_purchase_mrp_for_purchase_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mr_qty_for_complex_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_mr_qty_for_same_rm_with_different_sub_assemblies(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_reserve_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_material_request_qty_purchase_and_material_transfer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_unreserve_qty_on_closing_of_pp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_min_order_qty_in_pp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fg_item_quantity(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parent_warehouse_for_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_calculation_of_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reservation_against_production_plan(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reservation_of_serial_nos_against_production_plan(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_reservation_of_batch_nos_against_production_plan(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_production_plan_for_partial_sub_assembly_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_phantom_bom_explosion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_production_plan()

sales_order (obj): Sales Order Doc Object
get_items_from (str): Sales Order/Material Request
skip_getting_mr_items (bool): Whether or not to plan for new MRs

**Returns**: (none)



### make_bom()

**Returns**: (none)



### make_purchase_receipt_from_po(po_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| po_doc | None | - | - |

**Returns**: (none)



### setup_item(fg_item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fg_item | None | - | - |

**Returns**: (none)



### create_work_order(item, pln, qty)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| pln | None | - | - |
| qty | None | - | - |

**Returns**: (none)



### set_bom_qty(item_code, qtys)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| qtys | None | - | - |

**Returns**: (none)


