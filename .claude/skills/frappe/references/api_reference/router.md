# API Reference: router.py

**Language**: Python

**Source**: `website/router.py`

---

## Functions

### get_page_info_from_web_page_with_dynamic_routes(path)

Query Web Page with dynamic_route = 1 and evaluate if any of the routes match

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_page_info_from_web_form(path)

Query published web forms and evaluate if the route matches

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### evaluate_dynamic_routes(rules, path)

Use Werkzeug routing to evaluate dynamic routes like /project/<name>
https://werkzeug.palletsprojects.com/en/1.0.x/routing/

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| rules | None | - | - |
| path | None | - | - |

**Returns**: (none)



### get_pages(app = None)

Get all pages. Called for docs / sitemap

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | None | - |

**Returns**: (none)



### get_pages_from_path(start, app, app_path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| start | None | - | - |
| app | None | - | - |
| app_path | None | - | - |

**Returns**: (none)



### get_page_info(path, app, start, basepath = None, app_path = None, fname = None)

Load page info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| app | None | - | - |
| start | None | - | - |
| basepath | None | None | - |
| app_path | None | None | - |
| fname | None | None | - |

**Returns**: (none)



### setup_source(page_info)

Get the HTML source of the template

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| page_info | None | - | - |

**Returns**: (none)



### get_base_template(path = None)

Return the `base_template` for given `path`.

The default `base_template` for any web route is `templates/web.html` defined in `hooks.py`.
This can be overridden for certain routes in `custom_app/hooks.py` based on regex pattern.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |

**Returns**: (none)



### setup_index(page_info)

Build page sequence from index.txt

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| page_info | None | - | - |

**Returns**: (none)



### load_properties_from_controller(page_info)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| page_info | None | - | - |

**Returns**: (none)



### get_doctypes_with_web_view()

Return doctypes with Has Web View or set via hooks

**Returns**: (none)



### get_start_folders()

**Returns**: (none)



### clear_routing_cache()

**Returns**: (none)



### _build(app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### _get()

**Returns**: (none)


