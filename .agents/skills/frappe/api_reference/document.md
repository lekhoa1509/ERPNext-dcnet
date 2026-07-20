# API Reference: document.py

**Language**: Python

**Source**: `model/document.py`

---

## Classes

### Document

All controllers inherit from `Document`.

**Inherits from**: BaseDocument

#### Methods

##### __init__(self)

Constructor.

:param arg1: DocType name as string, document **dict**, or DocRef object
:param arg2: Document name, if `arg1` is DocType name.

If DocType name and document name are passed, the object will load
all values (including child documents) from the database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_locked(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_from_db(self) → 'Self'

Load document and children from database and create properties
from fields

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'Self'`


##### mask_fields(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_children_from_db(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _load_child_table_from_db(self, fieldname, child_doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| child_doctype | None | - | - |


##### reload(self) → 'Self'

Reload document from database

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'Self'`


##### get_latest(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_permission(self, permtype = 'read', permlevel = None)

Raise `frappe.PermissionError` if not permitted

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| permtype | None | 'read' | - |
| permlevel | None | None | - |


##### has_permission(self, permtype = 'read') → bool

Call `frappe.permissions.has_permission` if `ignore_permissions` flag isn't truthy

:param permtype: `read`, `write`, `submit`, `cancel`, `delete`, etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| permtype | None | 'read' | - |

**Returns**: `bool`


##### _handle_permission_failure(self, perm_type)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| perm_type | None | - | - |


##### raise_no_permission_to(self, perm_type)

Raise `frappe.PermissionError`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| perm_type | None | - | - |


##### insert(self, ignore_permissions = None, ignore_links = None, ignore_if_duplicate = False, ignore_mandatory = None, set_name = None, set_child_names = True) → 'Self'

Insert the document in the database (as a new document).
This will check for user permissions and execute `before_insert`,
`validate`, `on_update`, `after_insert` methods if they are written.

:param ignore_permissions: Do not check permissions if True.
:param ignore_links: Do not check validity of links if True.
:param ignore_if_duplicate: Do not raise error if a duplicate entry exists.
:param ignore_mandatory: Do not check missing mandatory fields if True.
:param set_name: Name to set for the document, if valid.
:param set_child_names: Whether to set names for the child documents.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_permissions | None | None | - |
| ignore_links | None | None | - |
| ignore_if_duplicate | None | False | - |
| ignore_mandatory | None | None | - |
| set_name | None | None | - |
| set_child_names | None | True | - |

**Returns**: `'Self'`


##### check_if_locked(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### save(self) → 'Self'

Wrapper for _save

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'Self'`


##### _save(self, ignore_permissions = None, ignore_version = None) → 'Self'

Save the current document in the database in the **DocType**'s table or
`tabSingles` (for single types).

This will check for user permissions and execute
`validate` before updating, `on_update` after updating triggers.

:param ignore_permissions: Do not check permissions if True.
:param ignore_version: Do not save version if True.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_permissions | None | None | - |
| ignore_version | None | None | - |

**Returns**: `'Self'`


##### validate_amended_from(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### copy_attachments_from_amended_from(self)

Copy attachments from `amended_from`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_children(self)

update child tables

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_child_table(self, fieldname: str, df: 'DocField' | None = None)

sync child table for given fieldname

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | str | - | - |
| df | 'DocField' | None | None | - |


##### reset_computed_child_tables(self)

Reset computed child tables so that they are reloaded next time

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_doc_before_save(self) → 'Self'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `'Self'`


##### has_value_changed(self, fieldname)

Return True if value has changed before and after saving.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### get_value_before_save(self, fieldname)

Returns value of a field before saving

Note: This function only works in save context like doc.save, doc.submit.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### set_new_name(self, force = False, set_name = None, set_child_names = True)

Calls `frappe.naming.set_new_name` for parent and child docs.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| force | None | False | - |
| set_name | None | None | - |
| set_child_names | None | True | - |


##### get_title(self)

Get the document title based on title_field or `title` or `name`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_title_field(self)

Set title field based on template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### update_single(self, d)

Updates values for Single type Document in `tabSingles`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| d | None | - | - |


##### set_user_and_timestamp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_docstatus(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_non_negative(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _fix_rating_value(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_workflow(self)

Validate if the workflow transition is valid

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_set_only_once(self)

Validate that fields are not changed if not in insert

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_child_table_same(self, fieldname)

Validate child table is same as original table before saving

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### apply_fieldlevel_read_permissions(self)

Remove values the user is not allowed to read.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_higher_perm_levels(self)

If the user does not have permissions at permlevel > 0, then reset the values to original / default

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_permlevel_access(self, permission_type = 'write')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| permission_type | None | 'write' | - |


##### has_permlevel_access_to(self, fieldname, df = None, permission_type = 'read')

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| df | None | None | - |
| permission_type | None | 'read' | - |


##### get_permissions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _set_defaults(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_if_latest(self)

Checks if `modified` timestamp provided by document being updated is same as the
`modified` timestamp in the database. If there is a different, the document has been
updated in the database after the current copy was read. Will throw an error if
timestamps don't match.

Will also validate document transitions (Save > Submit > Cancel) calling
`self.check_docstatus_transition`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### check_docstatus_transition(self, to_docstatus)

Ensures valid `docstatus` transition.
Valid transitions are (number in brackets is `docstatus`):

- Save (0) > Save (0)
- Save (0) > Submit (1)
- Submit (1) > Submit (1)
- Submit (1) > Cancel (2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| to_docstatus | None | - | - |


##### set_parent_in_children(self)

Updates `parent` and `parenttype` property in all children.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_name_in_children(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_update_after_submit(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_mandatory(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _validate_links(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_all_children(self, parenttype = None) → list['Document']

Return all child documents from **Table** type fields in a list.
Excludes computed tables by default, unless `include_computed` is set to True.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parenttype | None | None | - |

**Returns**: `list['Document']`


##### run_method(self, method)

run standard triggers, plus those in hooks

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |


##### run_trigger(self, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |


##### run_notifications(self, method)

Run notifications for this method

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |


##### _submit(self)

Submit the document. Sets `docstatus` = 1, then saves.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _cancel(self)

Cancel the document. Sets `docstatus` = 2, then saves.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _rename(self, name: str | int, merge: bool = False, force: bool = False, validate_rename: bool = True)

Rename the document. Triggers frappe.rename_doc, then reloads.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | int | - | - |
| merge | bool | False | - |
| force | bool | False | - |
| validate_rename | bool | True | - |


##### submit(self)

Submit the document. Sets `docstatus` = 1, then saves.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### cancel(self)

Cancel the document. Sets `docstatus` = 2, then saves.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### discard(self)

Discard the draft document. Sets `docstatus` = 2 with db_set.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### rename(self, name: str | int, merge = False, force = False, validate_rename = True)

Rename the document to `name`. This transforms the current object.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | str | int | - | - |
| merge | None | False | - |
| force | None | False | - |
| validate_rename | None | True | - |


##### delete(self, ignore_permissions = False, force = False)

Delete document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| ignore_permissions | None | False | - |
| force | None | False | - |


##### run_before_save_methods(self)

Run standard methods before     `INSERT` or `UPDATE`. Standard Methods are:

- `validate`, `before_save` for **Save**.
- `validate`, `before_submit` for **Submit**.
- `before_cancel` for **Cancel**
- `before_update_after_submit` for **Update after Submit**

Will also update title_field if set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### load_doc_before_save(self)

load existing document from db before saving

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run_post_save_methods(self)

Run standard methods after `INSERT` or `UPDATE`. Standard Methods are:

- `on_update` for **Save**.
- `on_update`, `on_submit` for **Submit**.
- `on_cancel` for **Cancel**
- `update_after_submit` for **Update after Submit**

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reset_seen(self)

Clear _seen property and set current user as seen

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### notify_update(self)

Publish realtime that the current document is modified

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### db_set(self, fieldname, value = None, update_modified = True, notify = False, commit = False)

Set a value in the document object, update the timestamp and update the database.

WARNING: This method does not trigger controller validations and should
be used very carefully.

:param fieldname: fieldname of the property to be updated, or a {"field":"value"} dictionary
:param value: value of the property to be updated
:param update_modified: default True. updates the `modified` and `modified_by` properties
:param notify: default False. run doc.notify_update() to send updates via socketio
:param commit: default False. run frappe.db.commit()

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| value | None | None | - |
| update_modified | None | True | - |
| notify | None | False | - |
| commit | None | False | - |


##### db_get(self, fieldname)

get database value for this fieldname

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |


##### check_no_back_links_exist(self)

Check if document links to any active document before Cancel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### save_version(self)

Save version info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### hook(f)

Decorator: Make method `hookable` (i.e. extensible by another app).

Note: If each hooked method returns a value (dict), then all returns are
collated in one dict and returned. Ideally, don't return values in hookable
methods, set properties in the document.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| f | None | - | - |


##### is_whitelisted(self, method_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method_name | None | - | - |


##### validate_value(self, fieldname, condition, val2, doc = None, raise_exception = None)

Check that value of fieldname should be 'condition' val2
else throw Exception.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | None | - | - |
| condition | None | - | - |
| val2 | None | - | - |
| doc | None | None | - |
| raise_exception | None | None | - |


##### validate_table_has_rows(self, parentfield, raise_exception = None)

Raise exception if Table field is empty.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| parentfield | None | - | - |
| raise_exception | None | None | - |


##### round_floats_in(self, doc, fieldnames = None)

Round floats for all `Currency`, `Float`, `Percent` fields for the given doc.

:param doc: Document whose numeric properties are to be rounded.
:param fieldnames: [Optional] List of fields to be rounded.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |
| fieldnames | None | None | - |


##### get_url(self)

Return Desk URL for this document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_comment(self, comment_type = 'Comment', text = None, comment_email = None, comment_by = None)

Add a comment to this document.

:param comment_type: e.g. `Comment`. See Communication for more info.

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| comment_type | None | 'Comment' | - |
| text | None | None | - |
| comment_email | None | None | - |
| comment_by | None | None | - |


##### add_seen(self, user = None)

add the given/current user to list of users who have seen this document (_seen)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |


##### add_viewed(self, user = None, force = False, unique_views = False)

Add a view log for the current document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | None | None | - |
| force | None | False | - |
| unique_views | None | False | - |


##### log_error(self, title = None, message = None)

Helper function to create an Error Log

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| title | None | None | - |
| message | None | None | - |


##### get_signature(self)

Return signature (hash) for private URL.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_document_share_key(self, expires_on = None, no_expiry = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expires_on | None | None | - |
| no_expiry | None | False | - |


##### get_liked_by(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __onload(self)

**Decorators**: `@property`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_onload(self, key, value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | - | - |
| value | None | - | - |


##### get_onload(self, key = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | None | None | - |


##### queue_action(self, action)

Run an action in background. If the action has an inner function,
like _submit for submit, it will call that instead

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| action | None | - | - |


##### lock(self, timeout = None)

Creates a lock file for the given document. If timeout is set,
it will retry every 1 second for acquiring the lock again

:param timeout: Timeout in seconds, default 0

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| timeout | None | None | - |


##### unlock(self)

Delete the lock file for this document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_from_to_dates(self, from_date_field: str, to_date_field: str) → None

Validate that the value of `from_date_field` is not later than the value of `to_date_field`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| from_date_field | str | - | - |
| to_date_field | str | - | - |

**Returns**: `None`


##### get_assigned_users(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_tag(self, tag)

Add a Tag to this document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tag | None | - | - |


##### remove_tag(self, tag)

Remove a Tag to this document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| tag | None | - | - |


##### get_tags(self)

Return a list of Tags attached to this document

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### deferred_insert(self) → None

Push the document to redis temporarily and insert later.

WARN: This doesn't guarantee insertion as redis can be restarted
before data is flushed to database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### __str__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __repr__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### LazyDocument

Mixin for Document class that implments lazy loading for child tables.

**Inherits from**: (none)

#### Methods

##### load_children_from_db(self: Document)

Override Document which eagerly loads child tables

**Decorators**: `@override`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | Document | - | - |


##### get(self: Document, key, filters = None, limit = None, default = None)

**Decorators**: `@override`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | Document | - | - |
| key | None | - | - |
| filters | None | None | - |
| limit | None | None | - |
| default | None | None | - |


##### append(self, key: str, value: D | dict | None = None, position: int = -1) → D

**Decorators**: `@override`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| key | str | - | - |
| value | D | dict | None | None | - |
| position | int | -1 | - |

**Returns**: `D`


##### db_update_all(self)

**Decorators**: `@override`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### init_child_tables(self)

**Decorators**: `@override`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### LazyChildTable

**Inherits from**: (none)

#### Methods

##### __init__(self, fieldname: str, doctype: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| fieldname | str | - | - |
| doctype | str | - | - |

**Returns**: `None`


##### __get__(self, doc: Document, objtype = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | Document | - | - |
| objtype | None | None | - |




## Functions

### get_doc() → 'Document'

**Returns**: `'Document'`



### get_doc() → _SingleDocument

Retrieve Single DocType from DB, doctype must be positional argument.

**Returns**: `_SingleDocument`



### get_doc() → 'Document'

Retrieve DocType from DB, doctype and name must be positional argument.

**Returns**: `'Document'`



### get_doc() → '_NewDocument'

Initialize document from kwargs.
Not recommended. Use `frappe.new_doc` instead.

**Returns**: `'_NewDocument'`



### get_doc(documentdict: dict) → '_NewDocument'

Create document from dict.
Not recommended. Use `frappe.new_doc` instead.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| documentdict | dict | - | - |

**Returns**: `'_NewDocument'`



### get_doc() → 'Document'

Return a `frappe.model.Document` object.

:param arg1: Document dict or DocType name.
:param arg2: [optional] document name.
:param for_update: [optional] select document for update.

There are multiple ways to call `get_doc`

        # will fetch the latest user object (with child table) from the database
        user = get_doc("User", "test@example.com")

        # create a new object
        user = get_doc({
                "doctype":"User"
                "email_id": "test@example.com",
                "roles: [
                        {"role": "System Manager"}
                ]
        })

        # create new object with keyword arguments
        user = get_doc(doctype='User', email_id='test@example.com')

        # select a document for update
        user = get_doc("User", "test@example.com", for_update=True)

**Returns**: `'Document'`



### _basedoc(doc: BaseDocument) → 'Document'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | BaseDocument | - | - |

**Returns**: `'Document'`



### get_doc_str(doctype: str, name: str | None = None) → 'Document'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | None | None | - |

**Returns**: `'Document'`



### get_doc_from_mapping_proxy(data: MappingProxyType) → 'Document'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | MappingProxyType | - | - |

**Returns**: `'Document'`



### get_doc_from_dict(data: dict[str, Any]) → 'Document'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | dict[str, Any] | - | - |

**Returns**: `'Document'`



### get_lazy_doc(doctype: str, name: str) → 'Document'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: `'Document'`



### get_doc_permission_check(doc: 'Document', check_permission: str | bool | None = None) → 'Document'

Checks permissions for the given document, if specified.

:param doc: The document to check permissions for.
:param check_permission: The permission to check for, default is "read" if truthy.
:return: The document with permissions checked.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| check_permission | str | bool | None | None | - |

**Returns**: `'Document'`



### execute_action(__doctype, __name, __action)

Execute an action on a document (called by background worker)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| __doctype | None | - | - |
| __name | None | - | - |
| __action | None | - | - |

**Returns**: (none)



### bulk_insert(doctype: str, documents: Iterable['Document'], ignore_duplicates: bool = False, chunk_size = 1000, commit_chunks = False)

Insert simple Documents objects to database in bulk.

Warning/Info:
        - All documents are inserted without triggering ANY hooks.
        - This function assumes you've done the due dilligence and inserts in similar fashion as db_insert
        - Documents can be any iterable / generator containing Document objects

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| documents | Iterable['Document'] | - | - |
| ignore_duplicates | bool | False | - |
| chunk_size | None | 1000 | - |
| commit_chunks | None | False | - |

**Returns**: (none)



### _document_values_generator(documents: Iterable['Document'], columns: list[str]) → Generator[tuple[Any]]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| documents | Iterable['Document'] | - | - |
| columns | list[str] | - | - |

**Returns**: `Generator[tuple[Any]]`



### unlock_document(doctype: str, name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: (none)



### get_lazy_controller(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### copy_doc(doc: 'Document', ignore_no_copy: bool = True) → 'Document'

No_copy fields also get copied.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | 'Document' | - | - |
| ignore_no_copy | bool | True | - |

**Returns**: `'Document'`



### new_doc(doctype: str) → 'Document'

Return a new document of the given DocType with defaults set.

:param doctype: DocType of the new document.
:param parent_doc: [optional] add to parent document.
:param parentfield: [optional] add against this `parentfield`.
:param as_dict: [optional] return as dictionary instead of Document.
:param kwargs: [optional] You can specify fields as field=value pairs in function call.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |

**Returns**: `'Document'`



### get_cached_doc() → 'Document'

Identical to `frappe.get_doc`, but return from cache if available.

**Returns**: `'Document'`



### _set_document_in_cache(key: str, doc: 'Document') → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | str | - | - |
| doc | 'Document' | - | - |

**Returns**: `None`



### can_cache_doc(args) → str | None

Determine if document should be cached based on get_doc params.
Return cache key if doc can be cached, None otherwise.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |

**Returns**: `str | None`



### get_document_cache_key(doctype: str, name: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | - | - |

**Returns**: (none)



### clear_document_cache(doctype: str, name: str | None = None) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | None | None | - |

**Returns**: `None`



### get_cached_value(doctype: str, name: str | dict, fieldname: str | Iterable[str] = 'name', as_dict: bool = False) → Any

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | str | - | - |
| name | str | dict | - | - |
| fieldname | str | Iterable[str] | 'name' | - |
| as_dict | bool | False | - |

**Returns**: `Any`



### get_single_value()

Return the cached value associated with the given fieldname from single DocType.

Usage:
        telemetry_enabled = frappe.get_single_value("System Settings", "telemetry_enabled")

**Returns**: (none)



### get_last_doc(doctype, filters: FilterSignature | None = None, order_by = 'creation desc')

Get last created document of this type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| filters | FilterSignature | None | None | - |
| order_by | None | 'creation desc' | - |

**Returns**: (none)



### get_single(doctype)

Return a `frappe.model.document.Document` object of the given Single doctype.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### remove_no_copy_fields(d)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| d | None | - | - |

**Returns**: (none)



### clear_in_redis()

**Returns**: (none)



### get_values()

**Returns**: (none)



### get_msg(df)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| df | None | - | - |

**Returns**: (none)



### fn(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### _get_notifications()

Return enabled notifications for the current doctype.

**Returns**: (none)



### _evaluate_alert(alert)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| alert | None | - | - |

**Returns**: (none)



### add_to_return_value(self, new_return_value)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| new_return_value | None | - | - |

**Returns**: (none)



### compose(fn)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| fn | None | - | - |

**Returns**: (none)



### composer(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### runner(self, method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |

**Returns**: (none)


