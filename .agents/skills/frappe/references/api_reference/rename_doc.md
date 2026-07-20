# API Reference: rename_doc.py

**Language**: Python

**Source**: `model/utils/rename_doc.py`

---

## Functions

### update_linked_doctypes(doctype: str, docname: str, linked_to: str, value: str, ignore_doctypes: list | None = None)

linked_doctype_info_list = list formed by get_fetch_fields() function
docname = Master DocType's name in which modification are made
value = Value for the field thats set in other DocType's by fetching from Master DocType

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| docname | str | - | - |
| linked_to | str | - | - |
| value | str | - | - |
| ignore_doctypes | list | None | None | - |

**Returns**: (none)



### get_fetch_fields(doctype: str, linked_to: str, ignore_doctypes: list | None = None) → list[dict]

doctype = Master DocType in which the changes are being made
linked_to = DocType name of the field thats being updated in Master
This function fetches list of all DocType where both doctype and linked_to is found
as link fields.
Forms a list of dict in the form -
        [{doctype: , master_fieldname: , linked_to_fieldname: ]
where
        doctype = DocType where changes need to be made
        master_fieldname = Fieldname where options = doctype
        linked_to_fieldname = Fieldname where options = linked_to

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| linked_to | str | - | - |
| ignore_doctypes | list | None | None | - |

**Returns**: `list[dict]`


