# API Reference: test_domainification.py

**Language**: Python

**Source**: `tests/test_domainification.py`

---

## Classes

### TestDomainification

**Inherits from**: IntegrationTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### add_active_domain(self, domain)

add domain in active domain

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | None | - | - |


##### remove_from_active_domains(self, domain = None, remove_all = False)

remove domain from domain settings

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | None | None | - |
| remove_all | None | False | - |


##### new_domain(self, domain)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | None | - | - |


##### new_doctype(self, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| name | None | - | - |


##### test_active_domains(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_doctype_and_role_domainification(self)

test if doctype is hidden if the doctype's restrict to domain is not included
in active domains

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



