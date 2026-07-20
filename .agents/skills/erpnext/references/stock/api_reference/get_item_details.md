# API Reference: get_item_details.py

**Language**: Python

**Source**: `get_item_details.py`

---

## Functions

### _preprocess_ctx(ctx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |

**Returns**: (none)



### get_item_details(ctx, doc = None, for_validate = False, overwrite_warehouse = True) → ItemDetails

ctx = {
        "item_code": "",
        "warehouse": None,
        "customer": "",
        "conversion_rate": 1.0,
        "selling_price_list": None,
        "price_list_currency": None,
        "plc_conversion_rate": 1.0,
        "doctype": "",
        "name": "",
        "supplier": None,
        "transaction_date": None,
        "conversion_rate": 1.0,
        "buying_price_list": None,
        "is_subcontracted": 0/1,
        "ignore_pricing_rule": 0/1
        "project": ""
        "set_warehouse": ""
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| doc | None | None | - |
| for_validate | None | False | - |
| overwrite_warehouse | None | True | - |

**Returns**: `ItemDetails`



### remove_standard_fields(out: ItemDetails)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | ItemDetails | - | - |

**Returns**: (none)



### set_valuation_rate(out: ItemDetails | dict, ctx: ItemDetailsCtx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | ItemDetails | dict | - | - |
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### update_stock(ctx, out, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| out | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### has_incorrect_serial_nos(ctx, out)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| out | None | - | - |

**Returns**: (none)



### filter_batches(batches, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batches | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_filtered_serial_nos(serial_nos, doc, table = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| serial_nos | None | - | - |
| doc | None | - | - |
| table | None | None | - |

**Returns**: (none)



### update_bin_details(ctx: ItemDetailsCtx, out: ItemDetails, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| out | ItemDetails | - | - |
| doc | None | - | - |

**Returns**: (none)



### get_item_code(barcode = None, serial_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| barcode | None | None | - |
| serial_no | None | None | - |

**Returns**: (none)



### validate_item_details(ctx: ItemDetailsCtx, item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |

**Returns**: (none)



### get_basic_details(ctx: ItemDetailsCtx, item, overwrite_warehouse = True) → ItemDetails

:param ctx: {
                "item_code": "",
                "warehouse": None,
                "customer": "",
                "conversion_rate": 1.0,
                "selling_price_list": None,
                "price_list_currency": None,
                "price_list_uom_dependant": None,
                "plc_conversion_rate": 1.0,
                "doctype": "",
                "name": "",
                "supplier": None,
                "transaction_date": None,
                "conversion_rate": 1.0,
                "buying_price_list": None,
                "is_subcontracted": 0/1,
                "ignore_pricing_rule": 0/1
                "project": "",
                barcode: "",
                serial_no: "",
                currency: "",
                update_stock: "",
                price_list: "",
                company: "",
                order_type: "",
                is_pos: "",
                project: "",
                qty: "",
                stock_qty: "",
                conversion_factor: "",
                against_blanket_order: 0/1
        }
:param item: `item_code` of Item object
:return: frappe._dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| overwrite_warehouse | None | True | - |

**Returns**: `ItemDetails`



### get_item_warehouse_(ctx: ItemDetailsCtx, item, overwrite_warehouse, defaults = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| overwrite_warehouse | None | - | - |
| defaults | None | None | - |

**Returns**: (none)



### update_barcode_value(out)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | None | - | - |

**Returns**: (none)



### get_barcode_data(items_list = None, item_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items_list | None | None | - |
| item_code | None | None | - |

**Returns**: (none)



### get_item_tax_info(doc, tax_category, item_codes, item_rates = None, item_tax_templates = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| tax_category | None | - | - |
| item_codes | None | - | - |
| item_rates | None | None | - |
| item_tax_templates | None | None | - |

**Returns**: (none)



### get_item_tax_template(ctx, item = None, out: ItemDetails | None = None)

Determines item_tax template from item or parent item groups.

Accesses:
        ctx = {
        "child_doctype": str
        }
Passes:
        ctx = {
                "company": str
                "bill_date": str
                "transaction_date": str
        "tax_category": None
        "item_tax_template": None
        "base_net_rate": float
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| item | None | None | - |
| out | ItemDetails | None | None | - |

**Returns**: (none)



### _get_item_tax_template(ctx: ItemDetailsCtx, taxes, out: ItemDetails | None = None, for_validate = False) → None | str | list[str]

Accesses:
        ctx = {
                "company": str
                "bill_date": str
                "transaction_date": str
        "tax_category": None
        "item_tax_template": None
        }
Passes:
        ctx = {
        "base_net_rate": float
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| taxes | None | - | - |
| out | ItemDetails | None | None | - |
| for_validate | None | False | - |

**Returns**: `None | str | list[str]`



### is_within_valid_range(ctx: ItemDetailsCtx, tax) → bool

Accesses:
        ctx = {
        "base_net_rate": float
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| tax | None | - | - |

**Returns**: `bool`



### get_item_tax_map()

**Returns**: (none)



### calculate_service_end_date(ctx: ItemDetailsCtx, item = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | None | - |

**Returns**: (none)



### get_default_income_account(ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_default_inventory_account(ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_default_expense_account(ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_provisional_account(ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_default_discount_account(ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_default_deferred_account(ctx: ItemDetailsCtx, item, fieldname = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| fieldname | None | None | - |

**Returns**: (none)



### get_default_cost_center(ctx: ItemDetailsCtx, item = None, item_group = None, brand = None, company = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item | None | None | - |
| item_group | None | None | - |
| brand | None | None | - |
| company | None | None | - |

**Returns**: (none)



### get_default_supplier(_ctx: ItemDetailsCtx, item, item_group, brand)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _ctx | ItemDetailsCtx | - | - |
| item | None | - | - |
| item_group | None | - | - |
| brand | None | - | - |

**Returns**: (none)



### get_price_list_rate(ctx: ItemDetailsCtx, item_doc, out: ItemDetails = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item_doc | None | - | - |
| out | ItemDetails | None | - |

**Returns**: (none)



### insert_item_price(ctx: ItemDetailsCtx)

Insert Item Price if Price List and Price List Rate are specified and currency is the same

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### _get_stock_uom_rate(rate: float, ctx: ItemDetailsCtx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rate | float | - | - |
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### get_item_price(pctx: ItemPriceCtx | dict, item_code, ignore_party = False, force_batch_no = False) → list[dict]

Get name, price_list_rate from Item Price based on conditions
        Check if the desired qty is within the increment of the packing list.
:param pctx: dict (or frappe._dict) with mandatory fields price_list, uom
        optional fields transaction_date, customer, supplier
:param item_code: str, Item Doctype field item_code

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pctx | ItemPriceCtx | dict | - | - |
| item_code | None | - | - |
| ignore_party | None | False | - |
| force_batch_no | None | False | - |

**Returns**: `list[dict]`



### get_batch_based_item_price(pctx: ItemPriceCtx | dict | str, item_code) → float

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pctx | ItemPriceCtx | dict | str | - | - |
| item_code | None | - | - |

**Returns**: `float`



### get_price_list_rate_for(ctx: ItemDetailsCtx, item_code)

:param customer: link to Customer DocType
:param supplier: link to Supplier DocType
:param price_list: str (Standard Buying or Standard Selling)
:param item_code: str, Item Doctype field item_code
:param qty: Desired Qty
:param transaction_date: Date of the price

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item_code | None | - | - |

**Returns**: (none)



### check_packing_list(price_list_rate_name, desired_qty, item_code)

Check if the desired qty is within the increment of the packing list.
:param price_list_rate_name: Name of Item Price
:param desired_qty: Desired Qt
:param item_code: str, Item Doctype field item_code
:param qty: Desired Qt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| price_list_rate_name | None | - | - |
| desired_qty | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### validate_conversion_rate(ctx: ItemDetailsCtx, meta)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| meta | None | - | - |

**Returns**: (none)



### get_party_item_code(ctx: ItemDetailsCtx, item_doc, out: ItemDetails)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item_doc | None | - | - |
| out | ItemDetails | - | - |

**Returns**: (none)



### get_tax_withholding_category(ctx: ItemDetailsCtx, item_doc, out: ItemDetails)

Get tax withholding category for the item based on the transaction type and party.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| item_doc | None | - | - |
| out | ItemDetails | - | - |

**Returns**: (none)



### get_pos_profile_item_details_(ctx: ItemDetailsCtx, company, pos_profile = None, update_data = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| company | None | - | - |
| pos_profile | None | None | - |
| update_data | None | False | - |

**Returns**: (none)



### get_pos_profile(company, pos_profile = None, user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| pos_profile | None | None | - |
| user | None | None | - |

**Returns**: (none)



### get_conversion_factor(item_code, uom)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| uom | None | - | - |

**Returns**: (none)



### get_projected_qty(item_code, warehouse)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |

**Returns**: (none)



### get_bin_details(item_code, warehouse, company = None, include_child_warehouses = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| warehouse | None | - | - |
| company | None | None | - |
| include_child_warehouses | None | False | - |

**Returns**: (none)



### get_company_total_stock(item_code, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |

**Returns**: (none)



### get_batch_qty(batch_no, warehouse, item_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| batch_no | None | - | - |
| warehouse | None | - | - |
| item_code | None | - | - |

**Returns**: (none)



### apply_price_list(ctx, as_doc = False, doc = None)

Apply pricelist on a document-like dict object and return as
{'parent': dict, 'children': list}

:param ctx: See below
:param as_doc: Updates value in the passed dict

        ctx = {
                "doctype": "",
                "name": "",
                "items": [{"doctype": "", "name": "", "item_code": "", "brand": "", "item_group": ""}, ...],
                "conversion_rate": 1.0,
                "selling_price_list": None,
                "price_list_currency": None,
                "price_list_uom_dependant": None,
                "plc_conversion_rate": 1.0,
                "doctype": "",
                "name": "",
                "supplier": None,
                "transaction_date": None,
                "conversion_rate": 1.0,
                "buying_price_list": None,
                "ignore_pricing_rule": 0/1
        }

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| as_doc | None | False | - |
| doc | None | None | - |

**Returns**: (none)



### apply_price_list_on_item(ctx, doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### get_price_list_currency_and_exchange_rate(ctx: ItemDetailsCtx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### get_default_bom(item_code = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | None | - |

**Returns**: (none)



### get_valuation_rate(item_code, company, warehouse = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_code | None | - | - |
| company | None | - | - |
| warehouse | None | None | - |

**Returns**: (none)



### get_gross_profit(out: ItemDetails)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| out | ItemDetails | - | - |

**Returns**: (none)



### get_serial_no(_args, serial_nos = None, sales_order = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| _args | None | - | - |
| serial_nos | None | None | - |
| sales_order | None | None | - |

**Returns**: (none)



### update_party_blanket_order(ctx: ItemDetailsCtx, out: ItemDetails | dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |
| out | ItemDetails | dict | - | - |

**Returns**: (none)



### get_blanket_order_details(ctx: ItemDetailsCtx)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ctx | ItemDetailsCtx | - | - |

**Returns**: (none)



### _get_bom(item)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item | None | - | - |

**Returns**: (none)


