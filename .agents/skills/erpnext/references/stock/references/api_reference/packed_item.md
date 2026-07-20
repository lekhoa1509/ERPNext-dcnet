# API Reference: packed_item.py

**Language**: Python

**Source**: `doctype/packed_item/packed_item.py`

---

## Classes

### PackedItem

**Inherits from**: Document

#### Methods

##### set_actual_and_projected_qty(self)

Set actual and projected qty based on warehouse and item_code

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_packing_list(doc)

Make/Update packing list for Product Bundle Item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### is_product_bundle(item_code: str) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | str | - | - |

**Returns**: `bool`



### get_indexed_packed_items_table(doc)

Create dict from stale packed items table like:
{(Parent Item 1, Bundle Item 1, ae4b5678): {...}, (key): {value}}

Use: to quickly retrieve/check if row existed in table instead of looping n times

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### reset_packing_list(doc)

Conditionally reset the table and return if it was reset or not.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_product_bundle_items(item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |

**Returns**: (none)



### add_packed_item_row(doc, packing_item, main_item_row, packed_items_table, reset)

Add and return packed item row.
doc: Transaction document
packing_item (dict): Packed Item details
main_item_row (dict): Items table row corresponding to packed item
packed_items_table (dict): Packed Items table before save (indexed)
reset (bool): State if table is reset or preserved as is

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| packing_item | None | - | - |
| main_item_row | None | - | - |
| packed_items_table | None | - | - |
| reset | None | - | - |

**Returns**: (none)



### get_packed_item_details(item_code, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |

**Returns**: (none)



### update_packed_item_basic_data(main_item_row, pi_row, packing_item, item_data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| main_item_row | None | - | - |
| pi_row | None | - | - |
| packing_item | None | - | - |
| item_data | None | - | - |

**Returns**: (none)



### update_packed_item_stock_data(main_item_row, pi_row, packing_item, item_data, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| main_item_row | None | - | - |
| pi_row | None | - | - |
| packing_item | None | - | - |
| item_data | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### update_packed_item_with_pick_list_info(main_item_row, pi_row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| main_item_row | None | - | - |
| pi_row | None | - | - |

**Returns**: (none)



### update_packed_item_price_data(pi_row, item_data, doc)

Set price as per price list or from the Item master.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pi_row | None | - | - |
| item_data | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### update_packed_item_from_cancelled_doc(main_item_row, packing_item, pi_row, doc)

Update packed item row details from cancelled doc into amended doc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| main_item_row | None | - | - |
| packing_item | None | - | - |
| pi_row | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_packed_item_bin_qty(item, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_cancelled_doc_packed_item_details(old_packed_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| old_packed_items | None | - | - |

**Returns**: (none)



### update_product_bundle_rate(parent_items_price, pi_row, item_row)

Update the price dict of Product Bundles based on the rates of the Items in the bundle.

Structure:
{(Bundle Item 1, ae56fgji): 150.0, (Bundle Item 2, bc78fkjo): 200.0}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_items_price | None | - | - |
| pi_row | None | - | - |
| item_row | None | - | - |

**Returns**: (none)



### set_product_bundle_rate_amount(doc, parent_items_price)

Set cumulative rate and amount in bundle item.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| parent_items_price | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### get_items_from_product_bundle(row)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | None | - | - |

**Returns**: (none)


