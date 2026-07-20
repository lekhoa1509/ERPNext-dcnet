# API Reference: item.py

**Language**: Python

**Source**: `doctype/item/item.py`

---

## Classes

### DuplicateReorderRows

**Inherits from**: frappe.ValidationError



### StockExistsForTemplate

**Inherits from**: frappe.ValidationError



### InvalidBarcode

**Inherits from**: frappe.ValidationError



### DataValidationError

**Inherits from**: frappe.ValidationError



### Item

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

set opening stock and item price

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


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


##### validate_description(self)

Clean HTML description if set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_customer_provided_part(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_price(self, price_list = None)

Add a new price

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| price_list | None | None | - |


##### set_opening_stock(self)

set opening stock

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_fixed_asset(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_retain_sample(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_retain_sample(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_default_uom_in_conversion_factor_table(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_tax_net_rate_range(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_template_tables(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_conversion_factor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_naming_series(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_for_active_boms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fill_customer_code(self)

Append all the customer codes and insert into "customer_code" field of item table.
Used to search Item by customer code.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_item_tax(self)

Check whether Tax Rate is not entered twice for same Tax Type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_barcode(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_warehouse_for_reorder(self)

Validate Reorder level table for duplicate and conditional mandatory

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### stock_ledger_created(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_submitted_assets(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_item_price(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, old_name, new_name, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |
| merge | None | False | - |


##### after_rename(self, old_name, new_name, merge)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |
| merge | None | - | - |


##### delete_old_bins(self, old_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |


##### validate_duplicate_item_in_stock_reconciliation(self, old_name, new_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |


##### validate_properties_before_merge(self, new_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_name | None | - | - |


##### validate_duplicate_product_bundles_before_merge(self, old_name, new_name)

Block merge if both old and new items have product bundles.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |


##### set_last_purchase_rate(self, new_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_name | None | - | - |


##### recalculate_bin_qty(self, new_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_name | None | - | - |


##### update_bom_item_desc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_item_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_defaults_from_item_group(self)

Get defaults from Item Group

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_variants(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_has_variants(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_attributes_in_variants(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_stock_exists_for_template_item(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_variant_based_on_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_uom(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_uom_conversion_factor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_attributes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_variant_attributes(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cant_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _get_linked_submitted_documents(self, changed_fields: list[str]) → dict[str, str] | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| changed_fields | list[str] | - | - |

**Returns**: `dict[str, str] | None`


##### validate_auto_reorder_enabled_in_stock_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### convert_erpnext_to_barcodenumber(erpnext_number, barcode)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| erpnext_number | None | - | - |
| barcode | None | - | - |

**Returns**: (none)



### make_item_price(item, price_list_name, item_price)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| price_list_name | None | - | - |
| item_price | None | - | - |

**Returns**: (none)



### get_timeline_data(doctype: str, name: str) → dict[int, int]

get timeline data based on Stock Ledger Entry. This is displayed as heatmap on the item page.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `dict[int, int]`



### validate_end_of_life(item_code, end_of_life = None, disabled = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| end_of_life | None | None | - |
| disabled | None | None | - |

**Returns**: (none)



### validate_is_stock_item(item_code, is_stock_item = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| is_stock_item | None | None | - |

**Returns**: (none)



### validate_cancelled_item(item_code, docstatus = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| docstatus | None | None | - |

**Returns**: (none)



### get_last_purchase_details(item_code, doc_name = None, conversion_rate = 1.0)

returns last purchase details in stock uom

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| doc_name | None | None | - |
| conversion_rate | None | 1.0 | - |

**Returns**: (none)



### get_purchase_voucher_details(doctype, item_code, document_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| item_code | None | - | - |
| document_name | None | None | - |

**Returns**: (none)



### check_stock_uom_with_bin(item, stock_uom)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| stock_uom | None | - | - |

**Returns**: (none)



### get_item_defaults(item_code, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |

**Returns**: (none)



### set_item_default(item_code, company, fieldname, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |
| fieldname | None | - | - |
| value | None | - | - |

**Returns**: (none)



### get_item_details(item_code, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | None | - |

**Returns**: (none)



### get_uom_conv_factor(uom, stock_uom)

Get UOM conversion factor from uom to stock_uom
e.g. uom = "Kg", stock_uom = "Gram" then returns 1000.0

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| uom | None | - | - |
| stock_uom | None | - | - |

**Returns**: (none)



### get_item_attribute(parent, attribute_value = '')

Used for providing auto-completions in child table.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| attribute_value | None | '' | - |

**Returns**: (none)



### update_variants(variants, template, publish_progress = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| variants | None | - | - |
| template | None | - | - |
| publish_progress | None | True | - |

**Returns**: (none)



### validate_item_default_company_links(item_defaults: list[ItemDefault]) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_defaults | list[ItemDefault] | - | - |

**Returns**: `None`



### get_asset_naming_series()

**Returns**: (none)



### get_child_warehouses(warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| warehouse | None | - | - |

**Returns**: (none)



### body(docnames)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docnames | None | - | - |

**Returns**: (none)



### table_row(title, body)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | None | - | - |
| body | None | - | - |

**Returns**: (none)


