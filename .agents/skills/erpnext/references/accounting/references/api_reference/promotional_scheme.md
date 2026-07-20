# API Reference: promotional_scheme.py

**Language**: Python

**Source**: `doctype/promotional_scheme/promotional_scheme.py`

---

## Classes

### TransactionExists

**Inherits from**: frappe.ValidationError



### PromotionalScheme

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_applicable_for(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_pricing_rules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_invalid_pricing_rules(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mixed_with_recursion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_pricing_rules(self, pricing_rules)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| pricing_rules | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### raise_for_transaction_exists(name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_pricing_rules(doc, rules = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| rules | None | None | - |

**Returns**: (none)



### _get_pricing_rules(doc, child_doc, discount_fields, rules = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| child_doc | None | - | - |
| discount_fields | None | - | - |
| rules | None | None | - |

**Returns**: (none)



### get_pricing_rule_docname(row: dict, applicable_for: str | None = None, applicable_for_value: str | None = None) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| row | dict | - | - |
| applicable_for | str | None | None | - |
| applicable_for_value | str | None | None | - |

**Returns**: `str`



### prepare_pricing_rule(args, doc, child_doc, discount_fields, d, docname = None, applicable_for = None, value = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| doc | None | - | - |
| child_doc | None | - | - |
| discount_fields | None | - | - |
| d | None | - | - |
| docname | None | None | - |
| applicable_for | None | None | - |
| value | None | None | - |

**Returns**: (none)



### set_args(args, pr, doc, child_doc, discount_fields, child_doc_fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| pr | None | - | - |
| doc | None | - | - |
| child_doc | None | - | - |
| discount_fields | None | - | - |
| child_doc_fields | None | - | - |

**Returns**: (none)



### get_args_for_pricing_rule(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)


