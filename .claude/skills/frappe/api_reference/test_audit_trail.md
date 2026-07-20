# API Reference: test_audit_trail.py

**Language**: Python

**Source**: `core/doctype/audit_trail/test_audit_trail.py`

---

## Classes

### TestAuditTrail

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_compare_changed_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_compare_rows(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_rows_updated(self, row_changed)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| row_changed | None | - | - |


##### check_rows_added(self, rows_added)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| rows_added | None | - | - |


##### check_expected_values(self, values_to_check, expected_values)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| values_to_check | None | - | - |
| expected_values | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### create_custom_child_doctype()

**Returns**: (none)



### create_custom_doctype()

**Returns**: (none)



### amend_document(amend_from, changed_fields, rows_updated, submit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| amend_from | None | - | - |
| changed_fields | None | - | - |
| rows_updated | None | - | - |
| submit | None | False | - |

**Returns**: (none)



### create_comparator_doc(doctype_name, document)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_name | None | - | - |
| document | None | - | - |

**Returns**: (none)


