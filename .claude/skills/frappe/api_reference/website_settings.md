# API Reference: website_settings.py

**Language**: Python

**Source**: `website/doctype/website_settings/website_settings.py`

---

## Classes

### WebsiteSettings

**Inherits from**: Document

#### Methods

##### validate(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_home_page(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_top_bar_items(self)

validate url in top bar items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_footer_items(self)

validate url in top bar items

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_google_settings(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### validate_redirects(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### on_update(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### clear_cache(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_access_token(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### get_website_settings(context = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | None | None | - |

**Returns**: (none)



### get_items(parentfield: str) → list[dict]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parentfield | str | - | - |

**Returns**: `list[dict]`



### modify_header_footer_items(items: list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | list | - | - |

**Returns**: (none)



### get_auto_account_deletion()

**Returns**: (none)


