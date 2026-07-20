# API Reference: installed_applications.py

**Language**: Python

**Source**: `core/doctype/installed_applications/installed_applications.py`

---

## Classes

### InvalidAppOrder

**Inherits from**: frappe.ValidationError



### InstalledApplications

**Inherits from**: Document

#### Methods

##### update_versions(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_app_wise_setup_details(self)

Get app wise setup details from the Installed Application doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### reload_doc_if_required(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### has_non_admin_user()

**Returns**: (none)



### has_company()

**Returns**: (none)



### update_installed_apps_order(new_order: list[str] | str)

Change the ordering of `installed_apps` global

This list is used to resolve hooks and by default it's order of installation on site.

Sometimes it might not be the ordering you want, so thie function is provided to override it.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| new_order | list[str] | str | - | - |

**Returns**: (none)



### _create_version_log_for_change(old, new)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| old | None | - | - |
| new | None | - | - |

**Returns**: (none)



### get_installed_app_order() → list[str]

**Returns**: `list[str]`



### get_setup_wizard_completed_apps()

Get list of apps that have completed setup wizard

**Returns**: (none)



### get_setup_wizard_not_required_apps()

Get list of apps that do not require setup wizard

**Returns**: (none)



### get_apps_with_incomplete_dependencies(current_app)

Get apps with incomplete dependencies.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| current_app | None | - | - |

**Returns**: (none)



### get_setup_wizard_pending_apps(apps = None)

Get list of apps that have completed setup wizard

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| apps | None | None | - |

**Returns**: (none)


