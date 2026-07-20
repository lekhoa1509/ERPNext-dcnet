# API Reference: test_item.py

**Language**: Python

**Source**: `doctype/item/test_item.py`

---

## Classes

### TestItem

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_item(self, idx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| idx | None | - | - |


##### test_get_item_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_asset_item_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_tax_template(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_default_validations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_attribute_change_after_variant(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_item_variant(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_copy_fields_from_template_to_variants(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_item_variant_with_numeric_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_merging(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_merging_with_product_bundle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_conversion_factor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_conv_intermediate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_conv_base_case(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_variant_by_manufacturer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_stock_exists_against_template_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_add_item_barcode(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_heatmap_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_index_creation(self)

check if index is getting created in db

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_attribute_completions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_stock_uom_with_bin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_check_stock_uom_with_bin_no_sle(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_erasure_of_old_conversions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_autoname_series(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'item_naming_by': 'Naming Series'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_wise_negative_stock(self)

When global settings are disabled check that item that allows
negative stock can still consume material in all known stock
transactions that consume inventory.

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_backdated_negative_stock(self)

same as test above but backdated entries

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'allow_negative_stock': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_retain_sample(self)

**Decorators**: `@IntegrationTestCase.change_settings('Stock Settings', {'sample_retention_warehouse': '_Test Warehouse - _TC'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### consume_item_code_with_differet_stock_transactions(self, item_code, warehouse = '_Test Warehouse - _TC')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| item_code | None | - | - |
| warehouse | None | '_Test Warehouse - _TC' | - |


##### test_item_dashboard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_type_field_change(self)

Check if critical fields like `is_stock_item`, `has_batch_no` are not changed if transactions exist.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_codes_length(self)

Check if item code with special characters are allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_is_stock_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_serach_fields_for_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_group_warehouse_for_reorder_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_variant_uom_mismatch_throws_error(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_opening_stock_for_serial_batch(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_item(item_code = None, properties = None, uoms = None, barcode = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |
| properties | None | None | - |
| uoms | None | None | - |
| barcode | None | None | - |

**Returns**: (none)



### set_item_variant_settings(fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fields | None | - | - |

**Returns**: (none)



### make_item_variant()

**Returns**: (none)



### create_item(item_code, is_stock_item = 1, valuation_rate = 0, stock_uom = 'Nos', warehouse = '_Test Warehouse - _TC', is_customer_provided_item = None, customer = None, is_purchase_item = None, opening_stock = 0, is_fixed_asset = 0, asset_category = None, buying_cost_center = None, selling_cost_center = None, company = '_Test Company')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| is_stock_item | None | 1 | - |
| valuation_rate | None | 0 | - |
| stock_uom | None | 'Nos' | - |
| warehouse | None | '_Test Warehouse - _TC' | - |
| is_customer_provided_item | None | None | - |
| customer | None | None | - |
| is_purchase_item | None | None | - |
| opening_stock | None | 0 | - |
| is_fixed_asset | None | 0 | - |
| asset_category | None | None | - |
| buying_cost_center | None | None | - |
| selling_cost_center | None | None | - |
| company | None | '_Test Company' | - |

**Returns**: (none)


