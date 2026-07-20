# API Reference: test_rename_doc.py

**Language**: Python

**Source**: `tests/test_rename_doc.py`

---

## Classes

### TestRenameDoc

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(self)

Setting Up data for the tests defined under TestRenameDoc

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDownClass(self)

Deleting data generated for the tests defined under TestRenameDoc

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### test_rename_doc(self)

Rename an existing document via frappe.rename_doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_merging_docs(self)

Merge two documents via frappe.rename_doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rename_controllers(self)

Rename doctypes with controller code paths

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rename_doctype(self)

Rename DocType via frappe.rename_doc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_update_document_title_api(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bulk_rename(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doc_rename_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parenttype(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_rename_autoincrement_doc(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### patch_db(endpoints: list[str] | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| endpoints | list[str] | None | None | - |

**Returns**: (none)


