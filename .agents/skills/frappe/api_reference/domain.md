# API Reference: domain.py

**Language**: Python

**Source**: `core/doctype/domain/domain.py`

---

## Classes

### Domain

**Inherits from**: Document

#### Methods

##### setup_domain(self)

Setup domain icons, permissions, custom fields etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_domain(self)

Unset domain settings

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### remove_custom_field(self)

Remove custom_fields when disabling domain

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_roles(self)

Enable roles that are restricted to this domain

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_data(self, domain = None)

Load domain info via hooks

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domain | None | None | - |


##### get_domain_data(self, module)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| module | None | - | - |


##### set_default_portal_role(self)

Set default portal role based on domain

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_properties(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### set_values(self)

set values based on `data.set_value`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_sidebar_items(self)

Enable / disable sidebar items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |



