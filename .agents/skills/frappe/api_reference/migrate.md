# API Reference: migrate.py

**Language**: Python

**Source**: `migrate.py`

---

## Classes

### SiteMigration

Migrate all apps to the current version, will:
- run before migrate hooks
- run patches
- sync doctypes (schema)
- sync dashboards
- sync jobs
- sync fixtures
- sync customizations
- sync languages
- sync web pages (from /www)
- run after migrate hooks

**Inherits from**: (none)

#### Methods

##### __init__(self, skip_failing: bool = False, skip_search_index: bool = False, skip_fixtures: bool = False) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| skip_failing | bool | False | - |
| skip_search_index | bool | False | - |
| skip_fixtures | bool | False | - |

**Returns**: `None`


##### setUp(self)

Complete setup required for site migration

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

Run operations that should be run post schema updation processes
This should be executed irrespective of outcome

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### pre_schema_updates(self)

Executes `before_migrate` hooks

**Decorators**: `@atomic`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run_schema_updates(self)

Run patches as defined in patches.txt, sync schema changes as defined in the {doctype}.json files

**Decorators**: `@atomic`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### post_schema_updates(self)

Execute pending migration tasks post patches execution & schema sync
This includes:
* Sync `Scheduled Job Type` and scheduler events defined in hooks
* Sync fixtures & custom scripts
* Sync in-Desk Module Dashboards
* Sync customizations: Custom Fields, Property Setters, Custom Permissions
* Sync Frappe's internal language master
* Flush deferred inserts made during maintenance mode.
* Sync Portal Menu Items
* Sync Installed Applications Version History
* Execute `after_migrate` hooks

**Decorators**: `@atomic`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### required_services_running(self) → bool

Return True if all required services are running. Return False and print
instructions to stdout when required services are not available.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `bool`


##### lower_lock_timeout(self)

Lower timeout for table metadata locks, default is 1 day, reduce it to 5 minutes.

This is required to avoid indefinitely waiting for metadata lock.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### kill_idle_connections(self, idle_limit = 30)

Assuming migrate has highest priority, kill everything else.

If someone has connected to mariadb using DB console or ipython console and then acquired
certain locks we won't be able to migrate.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| idle_limit | None | 30 | - |


##### run(self, site: str)

Run Migrate operation on site specified. This method initializes
and destroys connections to the site database.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| site | str | - | - |




### DBQueryProgressMonitor

**Inherits from**: threading.Thread

#### Methods

##### __init__(self) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: `None`


##### run(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### stop(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




## Functions

### atomic(method)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| method | None | - | - |

**Returns**: (none)



### wrapper()

**Returns**: (none)


