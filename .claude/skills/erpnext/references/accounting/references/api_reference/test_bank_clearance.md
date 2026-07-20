# API Reference: test_bank_clearance.py

**Language**: Python

**Source**: `doctype/bank_clearance/test_bank_clearance.py`

---

## Classes

### TestBankClearance

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_bank_clearance(self)

**Decorators**: `@if_lending_app_not_installed`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bank_clearance_with_loan(self)

**Decorators**: `@if_lending_app_installed`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_clearance_date_on_si(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_bank_account()

**Returns**: (none)



### add_transactions()

**Returns**: (none)



### make_payment_entry()

**Returns**: (none)



### make_pos_sales_invoice()

**Returns**: (none)



### create_loan_masters()

**Returns**: (none)



### make_loan()

**Returns**: (none)


