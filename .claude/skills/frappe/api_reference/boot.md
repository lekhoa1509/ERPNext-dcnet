# API Reference: boot.py

**Language**: Python

**Source**: `boot.py`

---

## Functions

### get_bootinfo()

build and return boot info

**Returns**: (none)



### get_icon_style()

**Returns**: (none)



### get_letter_heads()

**Returns**: (none)



### load_conf_settings(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### load_desktop_data(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### get_allowed_pages(cache = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cache | None | False | - |

**Returns**: (none)



### get_allowed_reports(cache = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cache | None | False | - |

**Returns**: (none)



### get_allowed_report_names(cache = False) → set[str]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cache | None | False | - |

**Returns**: `set[str]`



### get_user_pages_or_reports(parent, cache = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent | None | - | - |
| cache | None | False | - |

**Returns**: (none)



### load_translations(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### get_user_info()

**Returns**: (none)



### get_user(bootinfo)

get user info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### add_home_page(bootinfo, docs)

load home page

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |
| docs | None | - | - |

**Returns**: (none)



### add_timezone_info(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### load_print(bootinfo, doclist)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |
| doclist | None | - | - |

**Returns**: (none)



### load_print_css(bootinfo, print_settings)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |
| print_settings | None | - | - |

**Returns**: (none)



### get_success_action()

**Returns**: (none)



### get_link_preview_doctypes()

**Returns**: (none)



### get_additional_filters_from_hooks()

**Returns**: (none)



### add_layouts(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### get_desk_settings()

**Returns**: (none)



### get_notification_settings()

**Returns**: (none)



### get_link_title_doctypes()

**Returns**: (none)



### set_time_zone(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### load_country_doc(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### load_currency_docs(bootinfo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| bootinfo | None | - | - |

**Returns**: (none)



### get_marketplace_apps()

**Returns**: (none)



### add_subscription_conf()

**Returns**: (none)



### get_sentry_dsn()

**Returns**: (none)



### get_sidebar_items()

**Returns**: (none)



### get_desktop_icon_urls()

**Returns**: (none)



### add_user_specific_sidebar(sidebar_items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sidebar_items | None | - | - |

**Returns**: (none)



### get_apps_from_fc()

**Returns**: (none)


