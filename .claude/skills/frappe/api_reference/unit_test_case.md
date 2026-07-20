# API Reference: unit_test_case.py

**Language**: Python

**Source**: `tests/classes/unit_test_case.py`

---

## Classes

### BaseTestCase

**Inherits from**: (none)

#### Methods

##### registerAs(cls, _as)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |
| _as | None | - | - |




### UnitTestCase

Unit test class for Frappe tests.

This class extends unittest.TestCase and provides additional utilities
specific to Frappe framework. It's designed for testing individual
components or functions in isolation.

Key features:
- Custom assertions for Frappe-specific comparisons
- Utilities for HTML and SQL normalization
- Context managers for user switching and time freezing

Note: If you override `setUpClass`, make sure to call `super().setUpClass()`
to maintain the functionality of this base class.

**Inherits from**: unittest.TestCase, BaseTestCase

#### Methods

##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### assertQueryEqual(self, first: str, second: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| first | str | - | - |
| second | str | - | - |

**Returns**: `None`


##### assertSequenceSubset(self, larger: Sequence, smaller: Sequence, msg: str | None = None) → None

Assert that `expected` is a subset of `actual`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| larger | Sequence | - | - |
| smaller | Sequence | - | - |
| msg | str | None | None | - |

**Returns**: `None`


##### assertDocumentEqual(self, expected: dict | BaseDocument, actual: BaseDocument) → None

Compare a (partial) expected document with actual Document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expected | dict | BaseDocument | - | - |
| actual | BaseDocument | - | - |

**Returns**: `None`


##### _compare_field(self, expected: Any, actual: Any, doc: BaseDocument, field: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expected | Any | - | - |
| actual | Any | - | - |
| doc | BaseDocument | - | - |
| field | str | - | - |

**Returns**: `None`


##### normalize_html(code: str) → str

Formats HTML consistently so simple string comparisons can work on them.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |

**Returns**: `str`


##### normalize_sql(query: str) → str

Formats SQL consistently so simple string comparisons can work on them.

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| query | str | - | - |

**Returns**: `str`




## Functions

### _get_doctype_from_module(cls)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: (none)



### decorator(cm_func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cm_func | None | - | - |

**Returns**: (none)


