# API Reference: parallel_test_runner.py

**Language**: Python

**Source**: `parallel_test_runner.py`

---

## Classes

### ParallelTestRunner

**Inherits from**: (none)

#### Methods

##### __init__(self, app, site, build_number = 1, total_builds = 1, dry_run = False, lightmode = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| app | None | - | - |
| site | None | - | - |
| build_number | None | 1 | - |
| total_builds | None | 1 | - |
| dry_run | None | False | - |
| lightmode | None | False | - |


##### setup_and_run(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_test_site(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### before_test_setup(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### setup_test_file_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run_tests(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### run_tests_for_file(self, file_info)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| file_info | None | - | - |


##### get_module(self, path, filename)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| path | None | - | - |
| filename | None | - | - |


##### print_result(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_test_file_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_test_weight(test)

Get approximate count of tests inside a file

**Decorators**: `@staticmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| test | None | - | - |




### ParallelTestWithOrchestrator

This can be used to balance-out test time across multiple instances
This is dependent on external orchestrator which returns next test to run

orchestrator endpoints
- register-instance (<build_id>, <instance_id>, test_spec_list)
- get-next-test-spec (<build_id>, <instance_id>)
- test-completed (<build_id>, <instance_id>)

**Inherits from**: ParallelTestRunner

#### Methods

##### __init__(self, app, site)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| app | None | - | - |
| site | None | - | - |


##### run_tests(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_test_file_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### register_instance(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### get_next_test(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### print_result(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### call_orchestrator(self, endpoint, data = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| endpoint | None | - | - |
| data | None | None | - |




## Functions

### split_by_weight(work, weights, chunk_count)

Roughly split work by respective weight while keep ordering.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| work | None | - | - |
| weights | None | - | - |
| chunk_count | None | - | - |

**Returns**: (none)



### get_all_tests(app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)


