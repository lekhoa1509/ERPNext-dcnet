# API Reference: testing.py

**Language**: Python

**Source**: `commands/testing.py`

---

## Functions

### main(site: str | None = None, app: str | None = None, module: str | None = None, doctype: str | None = None, module_def: str | None = None, verbose: bool = False, tests: tuple = (), force: bool = False, profile: bool = False, junit_xml_output: str | None = None, doctype_list_path: str | None = None, failfast: bool = False, case: str | None = None, skip_before_tests: bool = False, debug: bool = False, debug_exceptions: tuple[Exception] | None = None, selected_categories: list[str] | None = None, lightmode: bool = False) → None

Main function to run tests

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| site | str | None | None | - |
| app | str | None | None | - |
| module | str | None | None | - |
| doctype | str | None | None | - |
| module_def | str | None | None | - |
| verbose | bool | False | - |
| tests | tuple | () | - |
| force | bool | False | - |
| profile | bool | False | - |
| junit_xml_output | str | None | None | - |
| doctype_list_path | str | None | None | - |
| failfast | bool | False | - |
| case | str | None | None | - |
| skip_before_tests | bool | False | - |
| debug | bool | False | - |
| debug_exceptions | tuple[Exception] | None | None | - |
| selected_categories | list[str] | None | None | - |
| lightmode | bool | False | - |

**Returns**: `None`



### run_tests_in_light_mode(test_params)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| test_params | None | - | - |

**Returns**: (none)



### _setup_xml_output(junit_xml_output)

Setup XML output for test results if specified

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| junit_xml_output | None | - | - |

**Returns**: (none)



### _load_doctype_list(doctype_list_path)

Load the list of doctypes from the specified file

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype_list_path | None | - | - |

**Returns**: (none)



### _run_module_def_tests(app, module_def, runner: 'TestRunner', force) → 'TestRunner'

Run tests for the specified module definition

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| module_def | None | - | - |
| runner | 'TestRunner' | - | - |
| force | None | - | - |

**Returns**: `'TestRunner'`



### _get_doctypes_for_module_def(app, module_def)

Get the list of doctypes for the specified module definition

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| module_def | None | - | - |

**Returns**: (none)



### run_tests(context: CliCtxObj, app = None, module = None, doctype = None, module_def = None, test = (), profile = False, coverage = False, junit_xml_output = False, doctype_list_path = None, skip_test_records = False, skip_before_tests = False, failfast = False, case = None, test_category = 'all', lightmode = False, debug = False)

Run python unit-tests

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | None | None | - |
| module | None | None | - |
| doctype | None | None | - |
| module_def | None | None | - |
| test | None | () | - |
| profile | None | False | - |
| coverage | None | False | - |
| junit_xml_output | None | False | - |
| doctype_list_path | None | None | - |
| skip_test_records | None | False | - |
| skip_before_tests | None | False | - |
| failfast | None | False | - |
| case | None | None | - |
| test_category | None | 'all' | - |
| lightmode | None | False | - |
| debug | None | False | - |

**Returns**: (none)



### run_parallel_tests(context: CliCtxObj, app, build_number, total_builds, with_coverage = False, use_orchestrator = False, dry_run = False, lightmode = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | None | - | - |
| build_number | None | - | - |
| total_builds | None | - | - |
| with_coverage | None | False | - |
| use_orchestrator | None | False | - |
| dry_run | None | False | - |
| lightmode | None | False | - |

**Returns**: (none)



### run_ui_tests(context: CliCtxObj, app, headless = False, parallel = True, with_coverage = False, browser = 'chrome', ci_build_id = None, cypressargs = None, spec = None)

Run UI tests

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| context | CliCtxObj | - | - |
| app | None | - | - |
| headless | None | False | - |
| parallel | None | True | - |
| with_coverage | None | False | - |
| browser | None | 'chrome' | - |
| ci_build_id | None | None | - |
| cypressargs | None | None | - |
| spec | None | None | - |

**Returns**: (none)


