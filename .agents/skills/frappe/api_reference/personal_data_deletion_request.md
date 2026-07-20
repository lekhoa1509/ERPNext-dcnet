# API Reference: personal_data_deletion_request.py

**Language**: Python

**Source**: `website/doctype/personal_data_deletion_request/personal_data_deletion_request.py`

---

## Classes

### PersonalDataDeletionRequest

**Inherits from**: Document

#### Methods

##### __init__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### autoname(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_url_for_confirmation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### disable_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### send_verification_mail(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### notify_system_managers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_data_anonymization(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### trigger_data_deletion(self)

Redact user data defined in current site's hooks under `user_data_fields`

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### anonymize_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### notify_user_after_deletion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_deletion_steps(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### redact_partial_match_data(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### rename_documents(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### redact_full_match_data(self, ref, email)

Replaces the entire field value by the values set in the anonymization_value_map

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ref | None | - | - |
| email | None | - | - |


##### generate_anonymization_dict(self, ref)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ref | None | - | - |


##### redact_doc(self, doc, ref)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| ref | None | - | - |


##### _anonymize_data(self, email = None, anon = None, set_data = True, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | None | None | - |
| anon | None | None | - |
| set_data | None | True | - |
| commit | None | False | - |


##### set_step_status(self, step, status = 'Deleted')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| step | None | - | - |
| status | None | 'Deleted' | - |


##### __set_anonymization_data(self, email, anon)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| email | None | - | - |
| anon | None | - | - |


##### __redact_partial_match_data(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### put_on_hold(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### process_data_deletion_request()

**Returns**: (none)



### remove_unverified_record()

**Returns**: (none)



### confirm_deletion(email, name, host_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |
| name | None | - | - |
| host_name | None | - | - |

**Returns**: (none)



### get_pattern(full_match)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| full_match | None | - | - |

**Returns**: (none)



### new_name(email, number)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email | None | - | - |
| number | None | - | - |

**Returns**: (none)


