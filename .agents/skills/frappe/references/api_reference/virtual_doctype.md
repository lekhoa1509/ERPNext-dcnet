# API Reference: virtual_doctype.py

**Language**: Python

**Source**: `model/virtual_doctype.py`

---

## Classes

### VirtualDoctype

This class documents requirements that must be met by a doctype controller to function as virtual doctype


Additional requirements:
- DocType controller has to inherit from `frappe.model.document.Document` class

Note:
- "Backend" here means any storage service, it can be a database, flat file or network call to API.

**Inherits from**: Protocol

#### Methods

##### get_list() → list[frappe._dict]

Similar to reportview.get_list

**Decorators**: `@staticmethod`

**Returns**: `list[frappe._dict]`


##### get_count() → int

Similar to reportview.get_count, return total count of documents on listview.

**Decorators**: `@staticmethod`

**Returns**: `int`


##### get_stats()

Similar to reportview.get_stats, return sidebar stats.

**Decorators**: `@staticmethod`


##### db_insert(self) → None

Serialize the `Document` object and insert it in backend.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### load_from_db(self) → None

Using self.name initialize current document from backend data.

This is responsible for updatinng __dict__ of class with all the fields on doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### db_update(self) → None

Serialize the `Document` object and update existing document in backend.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### delete(self) → None

Delete the current document from backend

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`




## Functions

### validate_controller(doctype: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `None`



### _as_str(method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |

**Returns**: (none)


