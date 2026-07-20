# API Reference: frappeclient.py

**Language**: Python

**Source**: `frappeclient.py`

---

## Classes

### AuthError

**Inherits from**: Exception



### SiteExpiredError

**Inherits from**: Exception



### SiteUnreachableError

**Inherits from**: Exception



### FrappeException

**Inherits from**: Exception



### FrappeClient

**Inherits from**: (none)

#### Methods

##### __init__(self, url, username = None, password = None, verify = True, api_key = None, api_secret = None, frappe_authorization_source = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| url | None | - | - |
| username | None | None | - |
| password | None | None | - |
| verify | None | True | - |
| api_key | None | None | - |
| api_secret | None | None | - |
| frappe_authorization_source | None | None | - |


##### __enter__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __exit__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _login(self, username, password)

Login/start a session. Called internally on init

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| username | None | - | - |
| password | None | - | - |


##### setup_key_authentication_headers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### logout(self)

Logout session

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_list(self, doctype: str, fields = '["name"]', filters = None, limit_start: int = 0, limit_page_length: int | None = None, order_by = None, group_by = None)

Return list of records of a particular type.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | str | - | - |
| fields | None | '["name"]' | - |
| filters | None | None | - |
| limit_start | int | 0 | - |
| limit_page_length | int | None | None | - |
| order_by | None | None | - |
| group_by | None | None | - |


##### insert(self, doc)

Insert a document to the remote server

:param doc: A dict or Document object to be inserted remotely

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### insert_many(self, docs)

Insert multiple documents to the remote server

:param docs: List of dict or Document objects to be inserted in one request

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docs | None | - | - |


##### update(self, doc)

Update a remote document

:param doc: dict or Document object to be updated remotely. `name` is mandatory for this

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### bulk_update(self, docs)

Bulk update documents remotely

:param docs: List of dict or Document objects to be updated remotely (by `name`)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| docs | None | - | - |


##### delete(self, doctype, name)

Delete remote document by name

:param doctype: `doctype` to be deleted
:param name: `name` of document to be deleted

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| name | None | - | - |


##### submit(self, doc)

Submit remote document

:param doc: dict or Document object to be submitted remotely

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doc | None | - | - |


##### get_value(self, doctype, fieldname = None, filters = None)

Return a value from a document.

:param doctype: DocType to be queried
:param fieldname: Field to be returned (default `name`)
:param filters: dict or string for identifying the record

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| fieldname | None | None | - |
| filters | None | None | - |


##### set_value(self, doctype, docname, fieldname, value)

Set a value in a remote document

:param doctype: DocType of the document to be updated
:param docname: name of the document to be updated
:param fieldname: fieldname of the document to be updated
:param value: value to be updated

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| docname | None | - | - |
| fieldname | None | - | - |
| value | None | - | - |


##### cancel(self, doctype, name)

Cancel a remote document

:param doctype: DocType of the document to be cancelled
:param name: name of the document to be cancelled

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| name | None | - | - |


##### get_doc(self, doctype, name = '', filters = None, fields = None)

Return a single remote document.

:param doctype: DocType of the document to be returned
:param name: (optional) `name` of the document to be returned
:param filters: (optional) Filter by this dict if name is not set
:param fields: (optional) Fields to be returned, will return everything if not set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| name | None | '' | - |
| filters | None | None | - |
| fields | None | None | - |


##### rename_doc(self, doctype, old_name, new_name)

Rename remote document

:param doctype: DocType of the document to be renamed
:param old_name: Current `name` of the document to be renamed
:param new_name: New `name` to be set

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| old_name | None | - | - |
| new_name | None | - | - |


##### migrate_doctype(self, doctype, filters = None, update = None, verbose = 1, exclude = None, preprocess = None)

Migrate records from another doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |
| filters | None | None | - |
| update | None | None | - |
| verbose | None | 1 | - |
| exclude | None | None | - |
| preprocess | None | None | - |


##### migrate_single(self, doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| doctype | None | - | - |


##### get_api(self, method, params = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| params | None | None | - |


##### post_api(self, method, params = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| method | None | - | - |
| params | None | None | - |


##### get_request(self, params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| params | None | - | - |


##### post_request(self, data)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| data | None | - | - |


##### preprocess(self, params)

convert dicts, lists to json

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| params | None | - | - |


##### post_process(self, response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| response | None | - | - |




### FrappeOAuth2Client

**Inherits from**: FrappeClient

#### Methods

##### __init__(self, url, access_token, verify = True)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| url | None | - | - |
| access_token | None | - | - |
| verify | None | True | - |



