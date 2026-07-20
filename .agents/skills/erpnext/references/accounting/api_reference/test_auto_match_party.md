# API Reference: test_auto_match_party.py

**Language**: Python

**Source**: `doctype/bank_transaction/test_auto_match_party.py`

---

## Classes

### TestAutoMatchParty

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


##### test_match_by_account_number(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_match_by_iban(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_match_by_party_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_match_by_description(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_skip_match_if_multiple_close_results(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_supplier_for_match(supplier_name = 'John Doe & Co.', iban = None, account_no = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| supplier_name | None | 'John Doe & Co.' | - |
| iban | None | None | - |
| account_no | None | None | - |

**Returns**: (none)



### create_bank_transaction(description = None, withdrawal = 0, deposit = 0, transaction_id = None, party_name = None, account_no = None, iban = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| description | None | None | - |
| withdrawal | None | 0 | - |
| deposit | None | 0 | - |
| transaction_id | None | None | - |
| party_name | None | None | - |
| account_no | None | None | - |
| iban | None | None | - |

**Returns**: (none)


