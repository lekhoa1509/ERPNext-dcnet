# API Reference: test_quotation.py

**Language**: Python

**Source**: `doctype/quotation/test_quotation.py`

---

## Classes

### TestQuotation

**Inherits from**: IntegrationTestCase

#### Methods

##### test_update_child_quotation_add_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disallow_due_date_before_transaction_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_disallow_rate_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_child_removing_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quotation_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quotation_zero_qty(self)

Test if Quote with zero qty (Unit Price Item) is conditionally allowed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_quotation_without_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_order_terms_copied(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_do_not_add_ordered_items_in_new_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_gross_profit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_maintain_rate_in_sales_cycle_is_enforced(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_order_with_different_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_order(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_sales_order_with_terms(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'add_taxes_from_item_tax_template': 0, 'add_taxes_from_taxes_and_charges_template': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_till_before_transaction_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_from_expired_quotation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_quotation_with_margin(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_create_two_quotations(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_quotation_expiry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_product_bundle_mapping_on_creating_so(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_product_bundle_price_calculation_when_calculate_bundle_price_is_unchecked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_product_bundle_price_calculation_when_calculate_bundle_price_is_checked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_product_bundle_price_calculation_for_multiple_product_bundles_when_calculate_bundle_price_is_checked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_packed_items_indices_are_reset_when_product_bundle_is_deleted_from_items_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_alternative_items_with_stock_items(self)

Check if taxes & totals considers only non-alternative items with:
- One set of non-alternative & alternative items [first 3 rows]
- One simple stock item

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_alternative_items_with_service_items(self)

Check if taxes & totals considers only non-alternative items with:
- One set of non-alternative & alternative service items [first 3 rows]
- One simple non-alternative service item
All having the same item code and unique item name/description due to
dynamic services

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_amount_calculation_for_alternative_items(self)

Make sure that the amount is calculated correctly for alternative items when the qty is changed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_alternative_items_sales_order_mapping_with_stock_items(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_uom_validation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_item_tax_template_for_quotation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Accounts Settings', {'add_taxes_from_item_tax_template': 1, 'add_taxes_from_taxes_and_charges_template': 0})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_grand_total_and_rounded_total_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_so_from_zero_qty_quotation(self)

**Decorators**: `@IntegrationTestCase.change_settings('Selling Settings', {'allow_zero_qty_in_quotation': 1})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_items_in_quotation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_make_quotation_qar_to_inr(self)

**Decorators**: `@change_settings('Accounts Settings', {'allow_pegged_currencies_exchange_rates': True})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_over_order_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### enable_calculate_bundle_price(enable = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| enable | None | 1 | - |

**Returns**: (none)



### get_quotation_dict(party_name = None, item_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| party_name | None | None | - |
| item_code | None | None | - |

**Returns**: (none)



### make_quotation()

**Returns**: (none)


