# API Reference: material_requirements_planning_report.py

**Language**: Python

**Source**: `report/material_requirements_planning_report/material_requirements_planning_report.py`

---

## Classes

### MaterialRequirementsPlanningReport

**Inherits from**: (none)

#### Methods

##### __init__(self, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| filters | None | - | - |


##### generate_mrp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_non_planned_orders(self, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | - | - |


##### get_orders_to_skip(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_item_wise_bin_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_mps_data_with_bin_details(self, bin_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bin_details | None | - | - |


##### update_sales_forecast_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_mrp_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### filter_based_on_type_of_materials(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_chart_data(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_detailed_view_chart_data(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_bucket_view_chart_data(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_bucket_view_data(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### get_detailed_view_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_lead_time_from_raw_materials(self, raw_materials)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| raw_materials | None | - | - |


##### add_non_planned_so(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### add_bin_details(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### add_po_details(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### add_wo_details(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### update_required_qty(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### add_safety_stock(self, row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |


##### get_work_order_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_purchase_order_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_sales_order_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_packed_items_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_subcontracted_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_rm_details(self, raw_materials, delivery_date, planned_qty, bom_no, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| raw_materials | None | - | - |
| delivery_date | None | - | - |
| planned_qty | None | - | - |
| bom_no | None | - | - |
| data | None | - | - |


##### get_mps_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_items_from_mps(self, mps_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mps_data | None | - | - |


##### get_raw_materials_data(self, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| items | None | - | - |


##### get_raw_materials(self, bom_no, indent = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bom_no | None | - | - |
| indent | None | 0 | - |


##### get_columns(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_first_date_of_week(self, input_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| input_date | None | - | - |


##### get_last_date_of_week(self, input_date)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| input_date | None | - | - |


##### get_sales_forecast_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### execute(filters: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| filters | dict | None | None | - |

**Returns**: (none)



### get_item_details(item_code, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_item_lead_time(item_code, type_of_material)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| type_of_material | None | - | - |

**Returns**: (none)



### convert_to_daily_bucket_data(data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_item_capacity(item_code, bucket_size)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| bucket_size | None | - | - |

**Returns**: (none)



### make_order(selected_rows, company, warehouse = None, mps = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| selected_rows | None | - | - |
| company | None | - | - |
| warehouse | None | None | - |
| mps | None | None | - |

**Returns**: (none)



### make_purchase_orders(purchase_orders, company, warehouse = None, mps = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| purchase_orders | None | - | - |
| company | None | - | - |
| warehouse | None | None | - |
| mps | None | None | - |

**Returns**: (none)



### make_work_orders(work_orders, company, warehouse = None, mps = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work_orders | None | - | - |
| company | None | - | - |
| warehouse | None | None | - |
| mps | None | None | - |

**Returns**: (none)



### get_item_uom(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### is_whole_number(uom)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| uom | None | - | - |

**Returns**: (none)


