# API Reference: asset_capitalization.py

**Language**: Python

**Source**: `doctype/asset_capitalization/asset_capitalization.py`

---

## Classes

### AssetCapitalization

**Inherits from**: StockController

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

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


##### set_title(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_missing_values(self, for_validate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| for_validate | None | False | - |


##### validate_target_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_target_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_consumed_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_consumed_asset_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_service_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_source_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### get_asset_for_validation(self, asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| asset | None | - | - |


##### set_warehouse_details(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_asset_values(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_args_for_incoming_rate(self, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item | None | - | - |


##### calculate_totals(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_stock_ledger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_gl_entries(self, gl_entries = None, from_repost = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | None | - |
| from_repost | None | False | - |


##### get_gl_entries(self, inventory_account_map = None, default_expense_account = None, default_cost_center = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| inventory_account_map | None | None | - |
| default_expense_account | None | None | - |
| default_cost_center | None | None | - |


##### get_target_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gl_entries_for_consumed_stock_items(self, gl_entries, target_account, target_against, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| target_account | None | - | - |
| target_against | None | - | - |
| precision | None | - | - |


##### get_gl_entries_for_consumed_asset_items(self, gl_entries, target_account, target_against, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| target_account | None | - | - |
| target_against | None | - | - |
| precision | None | - | - |


##### get_gl_entries_for_consumed_service_items(self, gl_entries, target_account, target_against, precision)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| target_account | None | - | - |
| target_against | None | - | - |
| precision | None | - | - |


##### get_composite_component_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_gl_entries_for_target_item(self, gl_entries, target_account, target_against, precision, composite_component_value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| gl_entries | None | - | - |
| target_account | None | - | - |
| target_against | None | - | - |
| precision | None | - | - |
| composite_component_value | None | - | - |


##### update_target_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### restore_consumed_asset_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_consumed_asset_status(self, asset)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| asset | None | - | - |




## Functions

### get_target_item_details(item_code = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_target_asset_details(asset = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| asset | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_consumed_stock_item_details(ctx: ItemDetailsCtx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### get_warehouse_details(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_consumed_asset_details(ctx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |

**Returns**: (none)



### get_service_item_details(ctx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |

**Returns**: (none)



### get_items_tagged_to_wip_composite_asset(params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| params | None | - | - |

**Returns**: (none)



### process_stock_item(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### process_fixed_asset(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)


