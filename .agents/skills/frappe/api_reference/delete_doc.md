# API Reference: delete_doc.py

**Language**: Python

**Source**: `model/delete_doc.py`

---

## Functions

### delete_doc(doctype: str | None = None, name: str | int | list[str | int] | None = None, force: int | bool = 0, ignore_doctypes: list[str] | None = None, for_reload: bool = False, ignore_permissions: bool = False, flags: dict[str, Any] | None = None, ignore_on_trash: bool = False, ignore_missing: bool = True, delete_permanently: bool = False) → bool | None

Deletes a document and validates if it is not submitted and not linked in a live record.

Args:
        doctype (str, optional): The document type to delete. If not provided,
                retrieved from frappe.form_dict.get("dt"). Defaults to None.
        name (str | int | list, optional): The name/ID of the document(s) to delete.
                Can be a single name or a list of names. If not provided,
                retrieved from frappe.form_dict.get("dn"). Defaults to None.
        force (bool, optional): When True, bypasses link existence checks and allows
                deletion of documents that are linked to other records. Also allows
                deletion of standard DocTypes. Defaults to 0 (False).
        ignore_doctypes (list, optional): A list of child doctypes to ignore when
                deleting child table records associated with the document. Defaults to None.
        for_reload (bool, optional): When True, indicates the deletion is for reloading
                purposes (like during doctype updates). Skips certain validations like
                permissions and on_trash methods, and automatically sets delete_permanently=True.
                Defaults to False.
        ignore_permissions (bool, optional): When True, bypasses permission checks
                during deletion. Useful for system operations. Defaults to False.
        flags (dict, optional): Additional flags to set on the document during the
                deletion process. These flags affect document behavior during deletion.
                Defaults to None.
        ignore_on_trash (bool, optional): When True, skips calling the document's
                on_trash method, which typically contains cleanup logic. Defaults to False.
        ignore_missing (bool, optional): When True, doesn't raise an error if the
                document doesn't exist and returns False. When False, raises
                frappe.DoesNotExistError if document is missing. Defaults to True.
        delete_permanently (bool, optional): When True, permanently deletes the document
                without adding it to the "Deleted Document" table for recovery purposes.
                When False, the document is soft-deleted and can be recovered. Defaults to False.

Raises:
        frappe.DoesNotExistError: When document doesn't exist and ignore_missing=False.
        frappe.LinkExistsError: When document is linked to other records and force=False.
        frappe.PermissionError: When user doesn't have delete permissions and ignore_permissions=False.
        frappe.ValidationError: When trying to delete a submitted document.
        frappe.QueryTimeoutError: When document is locked by another user.

Returns:
        bool: False if document doesn't exist and ignore_missing=True, otherwise None.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | None | None | - |
| name | str | int | list[str | int] | None | None | - |
| force | int | bool | 0 | - |
| ignore_doctypes | list[str] | None | None | - |
| for_reload | bool | False | - |
| ignore_permissions | bool | False | - |
| flags | dict[str, Any] | None | None | - |
| ignore_on_trash | bool | False | - |
| ignore_missing | bool | True | - |
| delete_permanently | bool | False | - |

**Returns**: `bool | None`



### add_to_deleted_document(doc)

Add this document to Deleted Document table. Called after delete

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### update_naming_series(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### delete_from_table(doctype: str, name: str, ignore_doctypes: list[str], doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |
| ignore_doctypes | list[str] | - | - |
| doc | None | - | - |

**Returns**: (none)



### update_flags(doc, flags = None, ignore_permissions = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| flags | None | None | - |
| ignore_permissions | None | False | - |

**Returns**: (none)



### check_permission_and_not_submitted(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### check_if_doc_is_linked(doc, method = 'Delete')

Raises exception if the given document is linked in another record.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | 'Delete' | - |

**Returns**: (none)



### check_if_doc_is_dynamically_linked(doc, method = 'Delete')

Raise `frappe.LinkExistsError` if the document is dynamically linked

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| method | None | 'Delete' | - |

**Returns**: (none)



### raise_link_exists_exception(doc, reference_doctype, reference_docname, row = '')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| reference_doctype | None | - | - |
| reference_docname | None | - | - |
| row | None | '' | - |

**Returns**: (none)



### delete_dynamic_links(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### delete_references(doctype, reference_doctype, reference_name, reference_doctype_field = 'reference_doctype', reference_name_field = 'reference_name')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| reference_doctype_field | None | 'reference_doctype' | - |
| reference_name_field | None | 'reference_name' | - |

**Returns**: (none)



### clear_references(doctype, reference_doctype, reference_name, reference_doctype_field = 'reference_doctype', reference_name_field = 'reference_name')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| reference_doctype | None | - | - |
| reference_name | None | - | - |
| reference_doctype_field | None | 'reference_doctype' | - |
| reference_name_field | None | 'reference_name' | - |

**Returns**: (none)



### clear_timeline_references(link_doctype, link_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| link_doctype | None | - | - |
| link_name | None | - | - |

**Returns**: (none)



### insert_feed(doc)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |

**Returns**: (none)



### delete_controllers(doctype, module)

Delete controller code in the doctype folder

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| module | None | - | - |

**Returns**: (none)


