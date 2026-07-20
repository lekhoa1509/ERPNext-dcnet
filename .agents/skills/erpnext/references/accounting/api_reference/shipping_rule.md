# API Reference: shipping_rule.py

**Language**: Python

**Source**: `doctype/shipping_rule/shipping_rule.py`

---

## Classes

### OverlappingConditionError

**Inherits from**: frappe.ValidationError



### FromGreaterThanToError

**Inherits from**: frappe.ValidationError



### ManyBlankToValuesError

**Inherits from**: frappe.ValidationError



### ShippingRule

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_from_to_values(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### apply(self, doc)

Apply shipping rule on given doc. Called from accounts controller

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_shipping_amount_from_rules(self, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| value | None | - | - |


##### validate_countries(self, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### add_shipping_rule_to_tax_table(self, doc, shipping_amount)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| shipping_amount | None | - | - |


##### sort_shipping_rule_conditions(self)

Sort Shipping Rule Conditions based on increasing From Value

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_overlapping_shipping_rule_conditions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### overlap_exists_between(num_range1, num_range2)

num_range1 and num_range2 are two ranges
ranges are represented as a tuple e.g. range 100 to 300 is represented as (100, 300)
if condition num_range1 = 100 to 300
then condition num_range2 can only be like 50 to 99 or 301 to 400
hence, non-overlapping condition = (x1 <= x2 < y1 <= y2) or (y1 <= y2 < x1 <= x2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| num_range1 | None | - | - |
| num_range2 | None | - | - |

**Returns**: (none)


