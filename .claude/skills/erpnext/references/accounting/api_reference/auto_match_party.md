# API Reference: auto_match_party.py

**Language**: Python

**Source**: `doctype/bank_transaction/auto_match_party.py`

---

## Classes

### AutoMatchParty

Matches by Account/IBAN and then by Party Name/Description sequentially.
Returns when a result is obtained.

Result (if present) is of the form: (Party Type, Party,)

**Inherits from**: (none)

#### Methods

##### __init__(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### match(self) → tuple | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple | None`




### AutoMatchbyAccountIBAN

**Inherits from**: (none)

#### Methods

##### __init__(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### match(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### match_account_in_party(self) → tuple | None

Returns (Party Type, Party) if a matching account is found in Bank Account or Employee:
1. Get party from a matching (iban/account no) Bank Account
2. If not found, get party from Employee with matching bank account details (iban/account no)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple | None`


##### get_or_filters(self, party: str | None = None) → dict

Return OR filters for Bank Account and IBAN

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| party | str | None | None | - |

**Returns**: `dict`




### AutoMatchbyPartyNameDescription

**Inherits from**: (none)

#### Methods

##### __init__(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### get(self, key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |


##### match(self) → tuple | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple | None`


##### match_party_name_desc_in_party(self) → tuple | None

Fuzzy search party name and/or description against parties in the system

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `tuple | None`


##### fuzzy_search_and_return_result(self, party, names, field) → tuple | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| party | None | - | - |
| names | None | - | - |
| field | None | - | - |

**Returns**: `tuple | None`


##### process_fuzzy_result(self, result: list | None)

If there are multiple valid close matches return None as result may be faulty.
Return the result only if one accurate match stands out.

Returns: Result, Skip (whether or not to discontinue matching)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| result | list | None | - | - |




## Functions

### get_parties_in_order(deposit: float) → list

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| deposit | float | - | - |

**Returns**: `list`


