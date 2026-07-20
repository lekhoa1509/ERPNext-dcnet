# API Reference: accounting_dimension.py

**Language**: Python

**Source**: `doctype/accounting_dimension/accounting_dimension.py`

---

## Classes

### AccountingDimension

**Inherits from**: Document

#### Methods

##### before_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_doctype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_document_type_change(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_dimension_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### after_insert(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_fieldname_and_label(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### make_dimension_in_accounting_doctypes(doc, doclist = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| doclist | None | None | - |

**Returns**: (none)



### add_dimension_to_budget_doctype(df, doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |
| doc | None | - | - |

**Returns**: (none)



### delete_accounting_dimension(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### disable_dimension(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### toggle_disabling(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### get_doctypes_with_dimensions()

**Returns**: (none)



### get_accounting_dimensions(as_list = True, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| as_list | None | True | - |
| filters | None | None | - |

**Returns**: (none)



### get_checks_for_pl_and_bs_accounts()

**Returns**: (none)



### get_dimension_with_children(doctype, dimensions)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| dimensions | None | - | - |

**Returns**: (none)



### get_dimensions(with_cost_center_and_project = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| with_cost_center_and_project | None | False | - |

**Returns**: (none)



### create_accounting_dimensions_for_doctype(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)


