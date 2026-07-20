# API Reference: test_error_log.py

**Language**: Python

**Source**: `core/doctype/error_log/test_error_log.py`

---

## Classes

### TestErrorLog

**Inherits from**: IntegrationTestCase

#### Methods

##### test_error_log(self)

let's do an error log on error log?

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ldap_exceptions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestExceptionSourceGuessing

**Inherits from**: IntegrationTestCase

#### Methods

##### test_exc_source_guessing(self, _installed_apps)

**Decorators**: `@patch.object(frappe, 'get_installed_apps', return_value=['frappe', 'erpnext', '3pa'])`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| _installed_apps | None | - | - |



