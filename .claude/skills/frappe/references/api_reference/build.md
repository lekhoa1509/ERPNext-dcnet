# API Reference: build.py

**Language**: Python

**Source**: `build.py`

---

## Classes

### AssetsNotDownloadedError

**Inherits from**: Exception



### AssetsDontExistError

**Inherits from**: Exception



## Functions

### download_file(url, prefix)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |
| prefix | None | - | - |

**Returns**: (none)



### build_missing_files()

Check which files dont exist yet from the assets.json and run build for those files

**Returns**: (none)



### get_assets_link(frappe_head) → str

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| frappe_head | None | - | - |

**Returns**: `str`



### fetch_assets(url, frappe_head)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| url | None | - | - |
| frappe_head | None | - | - |

**Returns**: (none)



### setup_assets(assets_archive)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| assets_archive | None | - | - |

**Returns**: (none)



### download_frappe_assets(verbose = True) → bool

Download and set up Frappe assets if they exist based on the current commit HEAD.
Return True if correctly setup else return False.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| verbose | None | True | - |

**Returns**: `bool`



### symlink(target, link_name, overwrite = False)

Create a symbolic link named link_name pointing to target.
If link_name exists then FileExistsError is raised, unless overwrite=True.
When trying to overwrite a directory, IsADirectoryError is raised.

Source: https://stackoverflow.com/a/55742015/10309266

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| target | None | - | - |
| link_name | None | - | - |
| overwrite | None | False | - |

**Returns**: (none)



### setup()

**Returns**: (none)



### bundle(mode, apps = None, hard_link = False, verbose = False, skip_frappe = False, files = None, save_metafiles = False, using_cached = False, esbuild_target = None)

concat / minify js files

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| mode | None | - | - |
| apps | None | None | - |
| hard_link | None | False | - |
| verbose | None | False | - |
| skip_frappe | None | False | - |
| files | None | None | - |
| save_metafiles | None | False | - |
| using_cached | None | False | - |
| esbuild_target | None | None | - |

**Returns**: (none)



### watch(apps = None)

watch and rebuild if necessary

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| apps | None | None | - |

**Returns**: (none)



### check_node_executable()

**Returns**: (none)



### get_node_env()

**Returns**: (none)



### get_safe_max_old_space_size()

**Returns**: (none)



### generate_assets_map()

**Returns**: (none)



### setup_assets_dirs()

**Returns**: (none)



### clear_broken_symlinks()

**Returns**: (none)



### unstrip(message: str) → str

Pads input string on the right side until the last available column in the terminal

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | str | - | - |

**Returns**: `str`



### make_asset_dirs(hard_link = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| hard_link | None | False | - |

**Returns**: (none)



### link_assets_dir(source, target, hard_link = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | - | - |
| target | None | - | - |
| hard_link | None | False | - |

**Returns**: (none)



### scrub_html_template(content)

Return HTML content with removed whitespace and comments.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| content | None | - | - |

**Returns**: (none)



### html_to_js_template(path, content)

Return HTML template content as Javascript code, by adding it to `frappe.templates`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| content | None | - | - |

**Returns**: (none)


