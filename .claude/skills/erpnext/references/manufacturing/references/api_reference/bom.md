# API Reference: bom.py

**Language**: Python

**Source**: `doctype/bom/bom.py`

---

## Classes

### BOMRecursionError

**Inherits from**: frappe.ValidationError



### BOMTree

Full tree representation of a BOM

**Inherits from**: (none)

#### Methods

##### __init__(self, name: str, is_bom: bool = True, exploded_qty: float = 1.0, qty: float = 1) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | - | - |
| is_bom | bool | True | - |
| exploded_qty | float | 1.0 | - |
| qty | float | 1 | - |

**Returns**: `None`


##### __create_tree(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### level_order_traversal(self) → list['BOMTree']

Get level order traversal of tree.
E.g. for following tree the traversal will return list of nodes in order from top to bottom.
BOM:
        - SubAssy1
                - item1
                - item2
        - SubAssy2
                - item3
        - item4

returns = [SubAssy1, item1, item2, SubAssy2, item3, item4]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list['BOMTree']`


##### __str__(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### __repr__(self, level: int = 0) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| level | int | 0 | - |

**Returns**: `str`




### BOM

**Inherits from**: WebsiteGenerator

#### Methods

##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_index_for_bom(self, existing_boms)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| existing_boms | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_onload_for_multi_level_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_next_version_index(existing_boms: list[str]) → int

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| existing_boms | list[str] | - | - |

**Returns**: `int`


##### before_validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_default_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_context(self, context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| context | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_bom_creator_status(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_item_det(self, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |


##### get_routing(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_bom_material_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_bom_scrap_items_detail(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_bom_material_detail(self, args = None)

Get raw material details like uom, desc and rate

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | None | - |


##### validate_bom_currency(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### get_rm_rate(self, arg, notify = True)

Get raw material rate as per selected method, if bom exists takes bom cost

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| arg | None | - | - |
| notify | None | True | - |


##### update_cost(self, update_parent = True, from_child_bom = False, update_hour_rate = True, save = True)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| update_parent | None | True | - |
| from_child_bom | None | False | - |
| update_hour_rate | None | True | - |
| save | None | True | - |


##### update_parent_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_bom_unitcost(self, bom_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bom_no | None | - | - |


##### manage_default_bom(self)

Uncheck others if current one is selected as default or
check the current one as default if it the only bom for the selected item,
update default bom in item master

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_inspection(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_main_item(self)

Validate main FG item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_stock_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_uom_is_interger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_conversion_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_plc_conversion_rate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_materials(self)

Validate raw material entries

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_recursion(self, bom_list = None)

Check whether recursion occurs in any bom

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bom_list | None | None | - |


##### set_materials_based_on_operation_bom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_raw_materials(self, operation_row_id, items)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| operation_row_id | None | - | - |
| items | None | - | - |


##### is_sub_assembly_item(self, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |


##### get_item_data(self, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### add_materials_from_bom(self, finished_good, bom_no, operation_row_id, qty = None)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| finished_good | None | - | - |
| bom_no | None | - | - |
| operation_row_id | None | - | - |
| qty | None | None | - |


##### traverse_tree(self, bom_list = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bom_list | None | None | - |


##### calculate_cost(self, save_updates = False, update_hour_rate = False)

Calculate bom totals

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save_updates | None | False | - |
| update_hour_rate | None | False | - |


##### calculate_op_cost(self, update_hour_rate = False)

Update workstation rate and calculates totals

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| update_hour_rate | None | False | - |


##### update_rate_and_time(self, row, update_hour_rate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row | None | - | - |
| update_hour_rate | None | False | - |


##### calculate_rm_cost(self, save = False)

Fetch RM rate as per today's valuation rate and calculate totals

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | False | - |


##### calculate_sm_cost(self, save = False)

Fetch RM rate as per today's valuation rate and calculate totals

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | False | - |


##### calculate_exploded_cost(self)

Set exploded row cost from it's parent BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_rm_rate_map(self) → dict[str, float]

Create Raw Material-Rate map for Exploded Items. Fetch rate from Items table or Subassembly BOM.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `dict[str, float]`


##### update_exploded_items(self, save = True)

Update Flat BOM, following will be correct data

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | True | - |


##### get_exploded_items(self)

Get all raw materials including items from child bom

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### company_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_to_cur_exploded_items(self, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| args | None | - | - |


##### get_child_exploded_items(self, bom_no, stock_qty, operation = None)

Add all items from Flat BOM of child BOM

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| bom_no | None | - | - |
| stock_qty | None | - | - |
| operation | None | None | - |


##### add_exploded_items(self, save = True)

Add items to Flat BOM table

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| save | None | True | - |


##### validate_bom_links(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_transfer_against(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_routing_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_operations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_tree_representation(self) → BOMTree

Get a complete tree representation preserving order of child items.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `BOMTree`


##### set_process_loss_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_scrap_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_bom_item_rate(args, bom_doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| bom_doc | None | - | - |

**Returns**: (none)



### get_valuation_rate(data)

1) Get average valuation rate from all warehouses
2) If no value, get last valuation rate from SLE
3) If no value, get valuation rate from Item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### get_list_context(context)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | - | - |

**Returns**: (none)



### get_bom_items_as_dict(bom, company, qty = 1, fetch_exploded = 1, fetch_scrap_items = 0, include_non_stock_items = False, fetch_qty_in_stock_uom = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom | None | - | - |
| company | None | - | - |
| qty | None | 1 | - |
| fetch_exploded | None | 1 | - |
| fetch_scrap_items | None | 0 | - |
| include_non_stock_items | None | False | - |
| fetch_qty_in_stock_uom | None | True | - |

**Returns**: (none)



### get_bom_items(bom, company, qty = 1, fetch_exploded = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom | None | - | - |
| company | None | - | - |
| qty | None | 1 | - |
| fetch_exploded | None | 1 | - |

**Returns**: (none)



### validate_bom_no(item, bom_no)

Validate BOM No of sub-contracted items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| bom_no | None | - | - |

**Returns**: (none)



### get_children(parent = None, is_root = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | None | - |
| is_root | None | False | - |

**Returns**: (none)



### add_additional_cost(stock_entry, work_order, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry | None | - | - |
| work_order | None | - | - |
| job_card | None | None | - |

**Returns**: (none)



### add_non_stock_items_cost(stock_entry, work_order, expense_account, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry | None | - | - |
| work_order | None | - | - |
| expense_account | None | - | - |
| job_card | None | None | - |

**Returns**: (none)



### add_operating_cost_component_wise(stock_entry, work_order = None, consumed_operating_cost = None, op_expense_account = None, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry | None | - | - |
| work_order | None | None | - |
| consumed_operating_cost | None | None | - |
| op_expense_account | None | None | - |
| job_card | None | None | - |

**Returns**: (none)



### get_component_account(parent, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| company | None | - | - |

**Returns**: (none)



### add_operations_cost(stock_entry, work_order = None, expense_account = None, job_card = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| stock_entry | None | - | - |
| work_order | None | None | - |
| expense_account | None | None | - |
| job_card | None | None | - |

**Returns**: (none)



### get_bom_diff(bom1, bom2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom1 | None | - | - |
| bom2 | None | - | - |

**Returns**: (none)



### item_query(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### make_variant_bom(source_name, bom_no, item, variant_items, target_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_name | None | - | - |
| bom_no | None | - | - |
| item | None | - | - |
| variant_items | None | - | - |
| target_doc | None | None | - |

**Returns**: (none)



### get_op_cost_from_sub_assemblies(bom_no, op_cost = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |
| op_cost | None | 0 | - |

**Returns**: (none)



### get_scrap_items_from_sub_assemblies(bom_no, company, qty, scrap_items = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |
| company | None | - | - |
| qty | None | - | - |
| scrap_items | None | None | - |

**Returns**: (none)



### get_max_operation_quantity()

**Returns**: (none)



### get_utilised_corrective_cost()

**Returns**: (none)



### postprocess(source, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### _throw_error(bom_name, production_item = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_name | None | - | - |
| production_item | None | None | - |

**Returns**: (none)



### _get_children(bom_no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_no | None | - | - |

**Returns**: (none)


