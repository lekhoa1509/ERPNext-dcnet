# API Reference: account.py

**Language**: Python

**Source**: `doctype/account/account.py`

---

## Classes

### RootNotEditable

**Inherits from**: frappe.ValidationError



### BalanceMismatchError

**Inherits from**: frappe.ValidationError



### InvalidAccountMergeError

**Inherits from**: frappe.ValidationError



### Account

**Inherits from**: NestedSet

#### Methods

##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_child_account_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent(self)

Fetch Parent Details and validate parent account

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_root_and_report_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_receivable_payable_account_type(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_root_details(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_root_company_and_sync_account_to_children(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_disabled(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_group_or_ledger(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_default_accounts_in_company(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_frozen_accounts_modifier(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_balance_must_be_debit_or_credit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account_currency(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_account_number(self, account_number = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| account_number | None | None | - |


##### create_account_for_child_company(self, parent_acc_name_map, descendants, parent_acc_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent_acc_name_map | None | - | - |
| descendants | None | - | - |
| parent_acc_name | None | - | - |


##### convert_group_to_ledger(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### convert_ledger_to_group(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_gle_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_child_exists(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_parent_account(doctype, txt, searchfield, start, page_len, filters)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| txt | None | - | - |
| searchfield | None | - | - |
| start | None | - | - |
| page_len | None | - | - |
| filters | None | - | - |

**Returns**: (none)



### get_account_currency(account)

Helper function to get account currency

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account | None | - | - |

**Returns**: (none)



### on_doctype_update()

**Returns**: (none)



### get_account_autoname(account_number, account_name, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| account_number | None | - | - |
| account_name | None | - | - |
| company | None | - | - |

**Returns**: (none)



### update_account_number(name, account_name, account_number = None, from_descendant = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |
| account_name | None | - | - |
| account_number | None | None | - |
| from_descendant | None | False | - |

**Returns**: (none)



### merge_account(old, new)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| old | None | - | - |
| new | None | - | - |

**Returns**: (none)



### get_root_company(company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| company | None | - | - |

**Returns**: (none)



### sync_update_account_number_in_child(descendants, old_acc_name, account_name, account_number = None, old_acc_number = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| descendants | None | - | - |
| old_acc_name | None | - | - |
| account_name | None | - | - |
| account_number | None | None | - |
| old_acc_number | None | None | - |

**Returns**: (none)



### _ensure_idle_system()

**Returns**: (none)



### get_company_default_account_fields()

**Returns**: (none)



### generator()

**Returns**: (none)


