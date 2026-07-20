# API Reference: pricing_rule.py

**Language**: Python

**Source**: `doctype/pricing_rule/pricing_rule.py`

---

## Classes

### PricingRule

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_duplicate_apply_on(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_applicable_for_selling_or_buying(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_min_max_qty(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_min_max_amt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_recursion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cleanup_fields_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_rate_or_discount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_max_discount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_price_list_with_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dates(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_condition(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mixed_with_recursion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### apply_pricing_rule(args, doc = None)

args = {
        "items": [{"doctype": "", "name": "", "item_code": "", "brand": "", "item_group": ""}, ...],
        "customer": "something",
        "customer_group": "something",
        "territory": "something",
        "supplier": "something",
        "supplier_group": "something",
        "currency": "something",
        "conversion_rate": "something",
        "price_list": "something",
        "plc_conversion_rate": "something",
        "company": "something",
        "transaction_date": "something",
        "campaign": "something",
        "sales_partner": "something",
        "ignore_pricing_rule": "something"
}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| doc | None | None | - |

**Returns**: (none)



### update_pricing_rule_uom(pricing_rule, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pricing_rule | None | - | - |
| args | None | - | - |

**Returns**: (none)



### get_pricing_rule_for_item(args, doc = None, for_validate = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| doc | None | None | - |
| for_validate | None | False | - |

**Returns**: (none)



### update_args_for_pricing_rule(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_pricing_rule_details(args, pricing_rule)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| pricing_rule | None | - | - |

**Returns**: (none)



### apply_price_discount_rule(pricing_rule, item_details, args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pricing_rule | None | - | - |
| item_details | None | - | - |
| args | None | - | - |

**Returns**: (none)



### remove_pricing_rule_for_item(pricing_rules, item_details, item_code = None, rate = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| pricing_rules | None | - | - |
| item_details | None | - | - |
| item_code | None | None | - |
| rate | None | None | - |

**Returns**: (none)



### remove_pricing_rules(item_list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| item_list | None | - | - |

**Returns**: (none)



### set_transaction_type(args)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: (none)



### get_item_uoms(doctype, txt, searchfield, start, page_len, filters)

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


