# API Reference: authorization_control.py

**Language**: Python

**Source**: `doctype/authorization_control/authorization_control.py`

---

## Classes

### AuthorizationControl

**Inherits from**: TransactionBase

#### Methods

##### get_appr_user_role(self, det, doctype_name, total, based_on, condition, master_name, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| det | None | - | - |
| doctype_name | None | - | - |
| total | None | - | - |
| based_on | None | - | - |
| condition | None | - | - |
| master_name | None | - | - |
| company | None | - | - |


##### validate_auth_rule(self, doctype_name, total, based_on, cond, company, master_name = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| total | None | - | - |
| based_on | None | - | - |
| cond | None | - | - |
| company | None | - | - |
| master_name | None | '' | - |


##### bifurcate_based_on_type(self, doctype_name, total, av_dis, based_on, doc_obj, val, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| total | None | - | - |
| av_dis | None | - | - |
| based_on | None | - | - |
| doc_obj | None | - | - |
| val | None | - | - |
| company | None | - | - |


##### validate_approving_authority(self, doctype_name, company, total, doc_obj = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| company | None | - | - |
| total | None | - | - |
| doc_obj | None | '' | - |


##### get_value_based_rule(self, doctype_name, employee, total_claimed_amount, company)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype_name | None | - | - |
| employee | None | - | - |
| total_claimed_amount | None | - | - |
| company | None | - | - |



