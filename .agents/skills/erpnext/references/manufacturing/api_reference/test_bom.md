# API Reference: test_bom.py

**Language**: Python

**Source**: `doctype/bom/test_bom.py`

---

## Classes

### TestBOM

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_items(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_items_exploded(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_items_list(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_default_bom(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_bom_cost_in_all_boms(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost_with_batch_size(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost_multi_uom_multi_currency_based_on_price_list(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost_multi_uom_based_on_valuation_rate(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost_with_fg_based_operating_cost(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_subcontractor_sourced_item(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_tree_representation(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_generated_variant_bom(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_recursion_1st_level(self)

BOM should not allow BOM item again in child

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_recursion_transitive(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_with_process_loss_item(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_item_query(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_exclude_exploded_items_from_bom(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_transfer_defaults(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_name_length(self)

test >140 char names

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_version_index(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_versioning(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_clear_inpection_quality(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_pricing_based_on_lpp(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_set_default_bom_for_item_having_single_bom(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_exploded_items_rate(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_cost_update_flag(self)

**Decorators**: `@timeout`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_with_service_item_cost(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_include_manufacturing_and_fixed_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bom_raw_materials_stock_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_default_bom(item_code = '_Test FG Item 2')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | '_Test FG Item 2' | - |

**Returns**: (none)



### level_order_traversal(node)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| node | None | - | - |

**Returns**: (none)



### create_nested_bom(tree, prefix = '_Test bom ', submit = True, phantom_items = None)

Helper function to create a simple nested bom from tree describing item names. (along with required items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tree | None | - | - |
| prefix | None | '_Test bom ' | - |
| submit | None | True | - |
| phantom_items | None | None | - |

**Returns**: (none)



### reset_item_valuation_rate(item_code, warehouse_list = None, qty = None, rate = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse_list | None | None | - |
| qty | None | None | - |
| rate | None | None | - |

**Returns**: (none)



### create_bom_with_process_loss_item(fg_item, bom_item, scrap_qty = 0, scrap_rate = 0, fg_qty = 2, process_loss_percentage = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fg_item | None | - | - |
| bom_item | None | - | - |
| scrap_qty | None | 0 | - |
| scrap_rate | None | 0 | - |
| fg_qty | None | 2 | - |
| process_loss_percentage | None | 0 | - |

**Returns**: (none)



### create_process_loss_bom_items()

**Returns**: (none)



### create_process_loss_bom_item(item_tuple)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_tuple | None | - | - |

**Returns**: (none)



### create_tree_for_phantom_bom_tests()

**Returns**: (none)



### create_items(bom_tree)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bom_tree | None | - | - |

**Returns**: (none)



### dfs(tree, node)

naive implementation for searching right subtree

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| tree | None | - | - |
| node | None | - | - |

**Returns**: (none)



### _get_default_bom_in_item()

**Returns**: (none)


