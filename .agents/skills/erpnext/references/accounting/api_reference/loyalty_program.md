# API Reference: loyalty_program.py

**Language**: Python

**Source**: `doctype/loyalty_program/loyalty_program.py`

---

## Classes

### LoyaltyProgram

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_lowest_tier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_loyalty_details(customer, loyalty_program, expiry_date = None, company = None, include_expired_entry = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| loyalty_program | None | - | - |
| expiry_date | None | None | - |
| company | None | None | - |
| include_expired_entry | None | False | - |

**Returns**: (none)



### get_loyalty_program_details_with_points(customer, loyalty_program = None, expiry_date = None, company = None, silent = False, include_expired_entry = False, current_transaction_amount = 0)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| loyalty_program | None | None | - |
| expiry_date | None | None | - |
| company | None | None | - |
| silent | None | False | - |
| include_expired_entry | None | False | - |
| current_transaction_amount | None | 0 | - |

**Returns**: (none)



### get_loyalty_program_details(customer, loyalty_program = None, expiry_date = None, company = None, silent = False, include_expired_entry = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| loyalty_program | None | None | - |
| expiry_date | None | None | - |
| company | None | None | - |
| silent | None | False | - |
| include_expired_entry | None | False | - |

**Returns**: (none)



### get_redeemption_factor(loyalty_program = None, customer = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| loyalty_program | None | None | - |
| customer | None | None | - |

**Returns**: (none)



### validate_loyalty_points(ref_doc, points_to_redeem)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| ref_doc | None | - | - |
| points_to_redeem | None | - | - |

**Returns**: (none)


