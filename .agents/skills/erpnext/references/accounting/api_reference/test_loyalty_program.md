# API Reference: test_loyalty_program.py

**Language**: Python

**Source**: `doctype/loyalty_program/test_loyalty_program.py`

---

## Classes

### TestLoyaltyProgram

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_loyalty_points_earned_single_tier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_loyalty_points_earned_multiple_tier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cancel_sales_invoice(self)

cancelling the sales invoice should cancel the earned points

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sales_invoice_return(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_loyalty_points_for_dashboard(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_tier_selection(self, mock_get_loyalty_details)

**Decorators**: `@unittest.mock.patch('erpnext.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_details')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| mock_get_loyalty_details | None | - | - |




## Functions

### get_points_earned(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### create_sales_invoice_record(qty = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| qty | None | 1 | - |

**Returns**: (none)



### create_records()

**Returns**: (none)



### get_returned_amount()

**Returns**: (none)



### side_effect()

**Returns**: (none)


