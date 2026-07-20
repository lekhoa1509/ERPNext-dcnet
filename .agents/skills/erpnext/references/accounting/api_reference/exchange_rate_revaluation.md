# API Reference: exchange_rate_revaluation.py

**Language**: Python

**Source**: `doctype/exchange_rate_revaluation/exchange_rate_revaluation.py`

---

## Classes

### ExchangeRateRevaluation

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_rounding_loss_allowance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_total_gain_loss(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_accounts_without_gain_loss(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_cancel(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_journal_entry_condition(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### fetch_and_calculate_accounts_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_accounts_data(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_account_balance_from_gle(company, posting_date, account, party_type, party, rounding_loss_allowance)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| posting_date | None | - | - |
| account | None | - | - |
| party_type | None | - | - |
| party | None | - | - |
| rounding_loss_allowance | None | - | - |


##### calculate_new_account_balance(company, posting_date, account_details)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| posting_date | None | - | - |
| account_details | None | - | - |


##### throw_invalid_response_message(self, account_details)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_details | None | - | - |


##### get_for_unrealized_gain_loss_account(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_jv_entries(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_jv_for_zero_balance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### make_jv_for_revaluation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### calculate_exchange_rate_using_last_gle(company, account, party_type, party)

Use last GL entry to calculate exchange rate

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| account | None | - | - |
| party_type | None | - | - |
| party | None | - | - |

**Returns**: (none)



### get_account_details(company, posting_date, account, party_type = None, party = None, rounding_loss_allowance: float | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |
| posting_date | None | - | - |
| account | None | - | - |
| party_type | None | None | - |
| party | None | None | - |
| rounding_loss_allowance | float | None | None | - |

**Returns**: (none)


