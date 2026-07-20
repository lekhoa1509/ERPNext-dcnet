# API Reference: test_project_meta.py

**Language**: Python

**Source**: `tests/test_project_meta.py`

---

## Classes

### TestProjectMeta

**Inherits from**: IntegrationTestCase

#### Methods

##### test_init_py_tax_paid(self)

Impose the __init__.py tax.

frappe/__init__.py has grown crazy big and keeps getting bigger. Plot the LOC over time and
you'll see the madness and laziness in action.

Don't try to delete or bypass this test.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



