# API Reference: website_theme.py

**Language**: Python

**Source**: `website/doctype/website_theme/website_theme.py`

---

## Classes

### WebsiteTheme

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### is_standard_and_not_valid_user(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_trash(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_if_customizable(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### export_doc(self)

Export to standard folder `[module]/website_theme/[name]/[name].json`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache_if_current_theme(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### generate_bootstrap_theme(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### delete_old_theme_files(self, folder_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| folder_path | None | - | - |


##### set_as_default(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_apps(self)

**Decorators**: `@frappe.whitelist()`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_active_theme() → 'WebsiteTheme' | None

**Returns**: `'WebsiteTheme' | None`



### get_scss(website_theme)

Render `website_theme_template.scss` with the values defined in Website Theme.

params:
website_theme - instance of a Website Theme

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| website_theme | None | - | - |

**Returns**: (none)



### get_scss_paths()

Return a set of SCSS import paths from all apps that provide `website.scss`.

If `$BENCH_PATH/apps/frappe/frappe/public/scss/website[.bundle].scss` exists, the
returned set will contain 'frappe/public/scss/website[.bundle]'.

**Returns**: (none)



### after_migrate()

Regenerate Active Theme CSS file after migration.

Necessary to reflect possible changes in the imported SCSS files. Called at
the end of every `bench migrate`.

**Returns**: (none)


