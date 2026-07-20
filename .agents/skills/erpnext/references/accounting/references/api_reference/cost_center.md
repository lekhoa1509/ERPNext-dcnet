# API Reference: cost_center.py

**Language**: Python

**Source**: `doctype/cost_center/cost_center.py`

---

## Classes

### CostCenter

**Inherits from**: NestedSet

#### Methods

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


##### validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_parent_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


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


##### if_allocation_exists_against_cost_center(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_part_of_cost_center_allocation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |


##### after_rename(self, olddn, newdn, merge = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| olddn | None | - | - |
| newdn | None | - | - |
| merge | None | False | - |




## Functions

### on_doctype_update()

**Returns**: (none)



### get_name_with_number(new_account, account_number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_account | None | - | - |
| account_number | None | - | - |

**Returns**: (none)


