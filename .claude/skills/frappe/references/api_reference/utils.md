# API Reference: utils.py

**Language**: Python

**Source**: `website/utils.py`

---

## Functions

### delete_page_cache(path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |

**Returns**: (none)



### find_first_image(html)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| html | None | - | - |

**Returns**: (none)



### can_cache(no_cache = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| no_cache | None | False | - |

**Returns**: (none)



### get_comment_list(doctype, name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |

**Returns**: (none)



### get_home_page()

**Returns**: (none)



### get_home_page_via_hooks()

**Returns**: (none)



### get_boot_data()

**Returns**: (none)



### is_signup_disabled()

**Returns**: (none)



### cleanup_page_name(title: str) → str

make page name from title

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| title | str | - | - |

**Returns**: `str`



### abs_url(path)

Deconstructs and Reconstructs a URL into an absolute URL or a URL relative from root '/'

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### get_toc(route, url_prefix = None, app = None)

Insert full index (table of contents) for {index} tag

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | None | - | - |
| url_prefix | None | None | - |
| app | None | None | - |

**Returns**: (none)



### get_next_link(route, url_prefix = None, app = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | None | - | - |
| url_prefix | None | None | - |
| app | None | None | - |

**Returns**: (none)



### get_full_index(route = None, app = None)

Return full index of the website for www upto the n-th level.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | None | None | - |
| app | None | None | - |

**Returns**: (none)



### extract_title(source, path)

Return title from `&lt;!-- title --&gt;` or &lt;h1&gt; or path.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| path | None | - | - |

**Returns**: (none)



### extract_comment_tag(source: str, tag: str)

Extract custom tags in comments from source.

:param source: raw template source in HTML
:param title: tag to search, example "title"

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | str | - | - |
| tag | str | - | - |

**Returns**: (none)



### get_html_content_based_on_type(doc, fieldname, content_type)

Set content based on content_type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doc | None | - | - |
| fieldname | None | - | - |
| content_type | None | - | - |

**Returns**: (none)



### clear_cache(path = None)

Clear website caches
:param path: (optional) for the given path

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |

**Returns**: (none)



### clear_website_cache(path = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | None | - |

**Returns**: (none)



### get_frontmatter(string)

Reference: https://github.com/jonbeebe/frontmatter

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | None | - | - |

**Returns**: (none)



### get_sidebar_items(parent_sidebar, basepath = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| parent_sidebar | None | - | - |
| basepath | None | None | - |

**Returns**: (none)



### get_portal_sidebar_items()

**Returns**: (none)



### get_sidebar_items_from_sidebar_file(basepath, look_for_sidebar_json)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| basepath | None | - | - |
| look_for_sidebar_json | None | - | - |

**Returns**: (none)



### get_sidebar_json_path(path, look_for = False)

Get _sidebar.json path from directory path
:param path: path of the current diretory
:param look_for: if True, look for _sidebar.json going upwards from given path
:return: _sidebar.json path

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| look_for | None | False | - |

**Returns**: (none)



### cache_html(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### build_response(path, data, http_status_code, headers: dict | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| data | None | - | - |
| http_status_code | None | - | - |
| headers | dict | None | None | - |

**Returns**: (none)



### set_content_type(response, data, path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | None | - | - |
| data | None | - | - |
| path | None | - | - |

**Returns**: (none)



### add_preload_for_bundled_assets(response)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | None | - | - |

**Returns**: (none)



### is_binary_file(path)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### check_if_webform_exists(route)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| route | None | - | - |

**Returns**: (none)



### _get_home_page()

**Returns**: (none)



### cache_html_decorator()

**Returns**: (none)



### _build()

**Returns**: (none)



### add_items(sidebar_items, items)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| sidebar_items | None | - | - |
| items | None | - | - |

**Returns**: (none)


