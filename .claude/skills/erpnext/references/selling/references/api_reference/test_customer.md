# API Reference: test_customer.py

**Language**: Python

**Source**: `doctype/customer/test_customer.py`

---

## Classes

### TestCustomer

**Inherits from**: IntegrationTestCase

#### Methods

##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_customer_group_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_party_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_party_details_tax_category(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rename(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_freezed_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_delete_customer_contact(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_disabled_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duplicate_customer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_customer_outstanding_amount(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_credit_limit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_credit_limit_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_credit_limit_on_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_customer_payment_terms(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_full_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_customer_dict(customer_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |

**Returns**: (none)



### set_credit_limit(customer, company, credit_limit)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer | None | - | - |
| company | None | - | - |
| credit_limit | None | - | - |

**Returns**: (none)



### create_internal_customer(customer_name = None, represents_company = None, allowed_to_interact_with = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | None | - |
| represents_company | None | None | - |
| allowed_to_interact_with | None | None | - |

**Returns**: (none)



### make_customer(customer_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| customer_name | None | - | - |

**Returns**: (none)


