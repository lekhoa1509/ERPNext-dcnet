# API Reference: linked_with.py

**Language**: Python

**Source**: `form/linked_with.py`

---

## Classes

### SubmittableDocumentTree

**Inherits from**: (none)

#### Methods

##### __init__(self, doctype: str, name: str)

Construct a tree for the submitable linked documents.

* Node has properties like doctype and docnames. Represented as Node(doctype, docnames).
* Nodes are linked by doctype relationships like table, link and dynamic links.
* Node is referenced(linked) by many other documents and those are the child nodes.

NOTE: child document is a property of child node (not same as Frappe child docs of a table field).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| name | str | - | - |


##### get_all_children(self, ignore_doctypes_on_cancel_all)

Get all nodes of a tree except the root node (all the nested submitted
documents those are present in referencing tables dependent tables).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_doctypes_on_cancel_all | None | - | - |


##### get_next_level_children(self, parent_dt, parent_names)

Get immediate children of a Node(parent_dt, parent_names)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parent_dt | None | - | - |
| parent_names | None | - | - |


##### get_doctype_references(self, doctype)

Get references for a given document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### get_document_sources(self)

Return list of doctypes from where we access submittable documents.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_link_sources(self)

limit doctype links to these doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_submittable_doctypes(self) → list[str]

Return list of submittable doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `list[str]`




## Functions

### get_submitted_linked_docs(doctype: str, name: str, ignore_doctypes_on_cancel_all = None) → list[tuple]

Get all the nested submitted documents those are present in referencing tables (dependent tables).

:param doctype: Document type
:param name: Name of the document

Use-case:
* User should be able to cancel the linked documents along with the one user trying to cancel.

Case1: If document sd1-n1 (document name n1 from submittable doctype sd1) is linked to sd2-n2 and sd2-n2 is linked to sd3-n3,
        Getting submittable linked docs of `sd1-n1`should give both sd2-n2 and sd3-n3.
Case2: If document sd1-n1 (document name n1 from submittable doctype sd1) is linked to d2-n2 and d2-n2 is linked to sd3-n3,
        Getting submittable linked docs of `sd1-n1`should give None. (because d2-n2 is not a submittable doctype)
Case3: If document sd1-n1 (document name n1 from submittable doctype sd1) is linked to d2-n2 & sd2-n2. d2-n2 is linked to sd3-n3.
        Getting submittable linked docs of `sd1-n1`should give sd2-n2.

Logic:
-----
1. We can find linked documents only if we know how the doctypes are related.
2. As we need only submittable documents, we can limit doctype relations search to submittable doctypes by
        finding the relationships(Foreign key references) across submittable doctypes.
3. Searching for links is going to be a tree like structure where at every level,
        you will be finding documents using parent document and parent document links.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| ignore_doctypes_on_cancel_all | None | None | - |

**Returns**: `list[tuple]`



### get_child_tables_of_doctypes(doctypes: list[str] | None = None)

Return child tables by doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctypes | list[str] | None | None | - |

**Returns**: (none)



### get_references_across_doctypes(to_doctypes: list[str] | None = None, limit_link_doctypes: list[str] | None = None) → list

Find doctype wise foreign key references.

:param to_doctypes: Get links of these doctypes.
:param limit_link_doctypes: limit links to these doctypes.

* Include child table, link and dynamic link references.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| to_doctypes | list[str] | None | None | - |
| limit_link_doctypes | list[str] | None | None | - |

**Returns**: `list`



### get_references_across_doctypes_by_link_field(to_doctypes: list[str] | None = None, limit_link_doctypes: list[str] | None = None)

Find doctype wise foreign key references based on link fields.

:param to_doctypes: Get links to these doctypes.
:param limit_link_doctypes: limit links to these doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| to_doctypes | list[str] | None | None | - |
| limit_link_doctypes | list[str] | None | None | - |

**Returns**: (none)



### get_references_across_doctypes_by_dynamic_link_field(to_doctypes: list[str] | None = None, limit_link_doctypes: list[str] | None = None)

Find doctype wise foreign key references based on dynamic link fields.

:param to_doctypes: Get links to these doctypes.
:param limit_link_doctypes: limit links to these doctypes.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| to_doctypes | list[str] | None | None | - |
| limit_link_doctypes | list[str] | None | None | - |

**Returns**: (none)



### get_referencing_documents(reference_doctype: str, reference_names: list[str], link_info: dict, get_parent_if_child_table_doc: bool = True, parent_filters: list[list] | None = None, child_filters = None, allowed_parents = None)

Get linked documents based on link_info.

:param reference_doctype: reference doctype to find links
:param reference_names: reference document names to find links for
:param link_info: linking details to get the linked documents
        Ex: {'doctype': 'Purchase Invoice Advance', 'fieldname': 'reference_name',
                'doctype_fieldname': 'reference_type', 'is_child': True}
:param get_parent_if_child_table_doc: Get parent record incase linked document is a child table record.
:param parent_filters: filters to apply on if not a child table.
:param child_filters: apply filters if it is a child table.
:param allowed_parents: list of parents allowed in case of get_parent_if_child_table_doc
        is enabled.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| reference_doctype | str | - | - |
| reference_names | list[str] | - | - |
| link_info | dict | - | - |
| get_parent_if_child_table_doc | bool | True | - |
| parent_filters | list[list] | None | None | - |
| child_filters | None | None | - |
| allowed_parents | None | None | - |

**Returns**: (none)



### cancel_all_linked_docs(docs, ignore_doctypes_on_cancel_all = None)

Cancel all linked doctype, optionally ignore doctypes specified in a list.

Arguments:
        docs (json str) - It contains list of dictionaries of a linked documents.
        ignore_doctypes_on_cancel_all (list) - List of doctypes to ignore while cancelling.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docs | None | - | - |
| ignore_doctypes_on_cancel_all | None | None | - |

**Returns**: (none)



### validate_linked_doc(docinfo, ignore_doctypes_on_cancel_all = None)

Validate a document to be submitted and non-exempted from auto-cancel.

Arguments:
        docinfo (dict): The document to check for submitted and non-exempt from auto-cancel
        ignore_doctypes_on_cancel_all (list) - List of doctypes to ignore while cancelling.

Return:
        bool: True if linked document passes all validations, else False

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docinfo | None | - | - |
| ignore_doctypes_on_cancel_all | None | None | - |

**Returns**: (none)



### get_exempted_doctypes()

Get list of doctypes exempted from being auto-cancelled

**Returns**: (none)



### get_linked_docs(doctype: str, name: str, linkinfo: dict | None = None) → dict[str, list]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| linkinfo | dict | None | None | - |

**Returns**: `dict[str, list]`



### get(doctype, docname)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| docname | None | - | - |

**Returns**: (none)



### get_linked_doctypes(doctype, without_ignore_user_permissions_enabled = False)

add list of doctypes this doctype is 'linked' with.

Example, for Customer:

        {"Address": {"fieldname": "customer"}..}

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| without_ignore_user_permissions_enabled | None | False | - |

**Returns**: (none)



### _get_linked_doctypes(doctype, without_ignore_user_permissions_enabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| without_ignore_user_permissions_enabled | None | False | - |

**Returns**: (none)



### get_linked_fields(doctype, without_ignore_user_permissions_enabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| without_ignore_user_permissions_enabled | None | False | - |

**Returns**: (none)



### get_dynamic_linked_fields(doctype, without_ignore_user_permissions_enabled = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| without_ignore_user_permissions_enabled | None | False | - |

**Returns**: (none)


