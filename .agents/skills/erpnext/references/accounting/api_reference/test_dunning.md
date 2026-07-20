# API Reference: test_dunning.py

**Language**: Python

**Source**: `doctype/dunning/test_dunning.py`

---

## Classes

### TestDunning

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_dunning_without_fees(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dunning_with_fees_and_interest(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dunning_with_payment_entry(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_fetch_overdue_payments(self)

Create SI with overdue payment. Check if overdue payment is fetched in Dunning.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dunning_and_payment_against_partially_due_invoice(self)

Create SI with first installment overdue. Check impact of Dunning and Payment Entry.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dunning_resolution_from_credit_note(self)

Test that dunning is resolved when a credit note is issued against the original invoice.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_dunning_not_affected_by_standalone_credit_note(self)

Test that dunning is NOT resolved when a credit note has update_outstanding_for_self checked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_dunning(overdue_days, dunning_type_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| overdue_days | None | - | - |
| dunning_type_name | None | None | - |

**Returns**: (none)



### create_dunning_type(title, fee, interest, is_default)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | None | - | - |
| fee | None | - | - |
| interest | None | - | - |
| is_default | None | - | - |

**Returns**: (none)



### get_income_account(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### create_payment_terms_template_for_dunning()

**Returns**: (none)


