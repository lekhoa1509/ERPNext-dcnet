# API Reference: change_log.py

**Language**: Python

**Source**: `utils/change_log.py`

---

## Functions

### get_change_log(user = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | None | None | - |

**Returns**: (none)



### get_change_log_for_app(app, from_version, to_version)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| from_version | None | - | - |
| to_version | None | - | - |

**Returns**: (none)



### update_last_known_versions()

**Returns**: (none)



### get_versions()

Get versions of all installed apps.

Example:

        {
                "frappe": {
                        "title": "Frappe Framework",
                        "version": "5.0.0"
                }
        }

**Returns**: (none)



### get_app_branch(app)

Return branch of an app.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### get_app_last_commit_ref(app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### check_for_update()

**Returns**: (none)



### has_app_update_notifications() → bool

**Returns**: `bool`



### parse_latest_non_beta_release(response: list, current_version: Version) → list | None

Parse the response JSON for all the releases and return the latest non prerelease.

Args:

response (list): response object returned by github

Return a json object pertaining to the latest non-beta release

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| response | list | - | - |
| current_version | Version | - | - |

**Returns**: `list | None`



### check_release_on_github(owner: str, repo: str, current_version: Version) → tuple[Version, str] | tuple[None, None]

Check the latest release for a repo URL on GitHub.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| owner | str | - | - |
| repo | str | - | - |
| current_version | Version | - | - |

**Returns**: `tuple[Version, str] | tuple[None, None]`



### security_issues_count(owner: str, repo: str, current_version: Version, target_version: Version) → int

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| owner | str | - | - |
| repo | str | - | - |
| current_version | Version | - | - |
| target_version | Version | - | - |

**Returns**: `int`



### _get_latest_releases(owner, repo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| owner | None | - | - |
| repo | None | - | - |

**Returns**: (none)



### _get_security_issues(owner, repo)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| owner | None | - | - |
| repo | None | - | - |

**Returns**: (none)



### parse_github_url(remote_url: str) → tuple[str, str] | tuple[None, None]

Parse the remote URL to get the owner and repo name.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| remote_url | str | - | - |

**Returns**: `tuple[str, str] | tuple[None, None]`



### get_source_url(app: str) → str | None

Get the remote URL of the app.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `str | None`



### add_message_to_redis(update_json)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| update_json | None | - | - |

**Returns**: (none)



### show_update_popup()

**Returns**: (none)



### get_pyproject(app: str) → dict | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | str | - | - |

**Returns**: `dict | None`



### set_in_change_log(app, opts, change_log)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| opts | None | - | - |
| change_log | None | - | - |

**Returns**: (none)



### prioritize_minor_update(v: str) → Version

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| v | str | - | - |

**Returns**: `Version`



### applicable(advisory) → bool

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| advisory | None | - | - |

**Returns**: `bool`


