# API Reference: domain_settings.py

**Language**: Python

**Source**: `core/doctype/domain_settings/domain_settings.py`

---

## Classes

### DomainSettings

**Inherits from**: Document

#### Methods

##### set_active_domains(self, domains)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| domains | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### restrict_roles_and_modules(self)

Disable all restricted roles and set `restrict_to_domain` property in Module Def

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_active_domains()

get the domains set in the Domain Settings as active domain

**Returns**: (none)



### get_active_modules()

get the active modules from Module Def

**Returns**: (none)



### _get_active_domains()

**Returns**: (none)



### _get_active_modules()

**Returns**: (none)



### remove_role(role)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| role | None | - | - |

**Returns**: (none)


