# API Reference: inventory_dimension.py

**Language**: Python

**Source**: `doctype/inventory_dimension/inventory_dimension.py`

---

## Classes

### DoNotChangeError

**Inherits from**: frappe.ValidationError



### CanNotBeChildDoc

**Inherits from**: frappe.ValidationError



### CanNotBeDefaultDimension

**Inherits from**: frappe.ValidationError



### InventoryDimension

**Inherits from**: Document

#### Methods

##### onload(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### has_stock_ledger(self) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `str`


##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_save(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_type_of_transaction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### do_not_update_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_reference_document(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_source_and_target_fieldname(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_insert_after_fieldname(doctype)

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |


##### get_dimension_fields(self, doctype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | None | - |


##### add_custom_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_transfer_field(self, doctype, dimension_fields)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| dimension_fields | None | - | - |




## Functions

### field_exists(doctype, fieldname) → str or None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| fieldname | None | - | - |

**Returns**: `str or None`



### get_inventory_documents(doctype = None, txt = None, searchfield = None, start = None, page_len = None, filters = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| txt | None | None | - |
| searchfield | None | None | - |
| start | None | None | - |
| page_len | None | None | - |
| filters | None | None | - |

**Returns**: (none)



### get_evaluated_inventory_dimension(doc, sl_dict, parent_doc = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| sl_dict | None | - | - |
| parent_doc | None | None | - |

**Returns**: (none)



### get_document_wise_inventory_dimensions(doctype) → dict

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: `dict`



### get_inventory_dimensions()

**Returns**: (none)



### delete_dimension(dimension)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dimension | None | - | - |

**Returns**: (none)



### get_parent_fields(child_doctype, dimension_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| child_doctype | None | - | - |
| dimension_name | None | - | - |

**Returns**: (none)


