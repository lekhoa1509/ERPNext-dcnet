# API Reference: deprecation_dumpster.py

**Language**: Python

**Source**: `deprecation_dumpster.py`

---

## Classes

### Color

**Inherits from**: (none)



### FrappeDeprecationError

Deprecated feature in current version.

Raises an error by default but can be configured via PYTHONWARNINGS in an emergency.

**Inherits from**: Warning



### FrappeDeprecationWarning

Deprecated feature in next version

**Inherits from**: Warning



### PendingFrappeDeprecationWarning

Deprecated feature in develop beyond next version.

Warning ignored by default.

The deprecation decision may still be reverted or deferred at this stage.
Regardless, using the new variant is encouraged and stable.

**Inherits from**: FrappeDeprecationWarning



### V15FrappeDeprecationWarning

**Inherits from**: FrappeDeprecationError



### V16FrappeDeprecationWarning

**Inherits from**: FrappeDeprecationWarning



### V17FrappeDeprecationWarning

**Inherits from**: PendingFrappeDeprecationWarning



### FrappeTestCase

Base test class for Frappe tests.


If you specify `setUpClass` then make sure to call `super().setUpClass`
otherwise this class will become ineffective.

**Inherits from**: unittest.TestCase

#### Methods

##### __new__(cls)

**Decorators**: `@deprecated('frappe.tests.utils.FrappeTestCase', '2024-20-08', 'v17', 'Import `frappe.tests.UnitTestCase` or `frappe.tests.IntegrationTestCase` respectively instead of `frappe.tests.utils.FrappeTestCase` - also see wiki for more info: https://github.com/frappe/frappe/wiki#testing-guide')`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### setUpClass(cls) → None

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### _apply_debug_decorator(self, exceptions = ())

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| exceptions | None | () | - |


##### assertSequenceSubset(self, larger: Sequence, smaller: Sequence, msg = None)

Assert that `expected` is a subset of `actual`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| larger | Sequence | - | - |
| smaller | Sequence | - | - |
| msg | None | None | - |


##### assertDocumentEqual(self, expected, actual)

Compare a (partial) expected document with actual Document.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expected | None | - | - |
| actual | None | - | - |


##### _compare_field(self, expected, actual, doc: BaseDocument, field: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| expected | None | - | - |
| actual | None | - | - |
| doc | BaseDocument | - | - |
| field | str | - | - |


##### normalize_html(self, code: str) → str

Formats HTML consistently so simple string comparisons can work on them.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| code | str | - | - |

**Returns**: `str`


##### normalize_sql(self, query: str) → str

Formats SQL consistently so simple string comparisons can work on them.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| query | str | - | - |

**Returns**: `str`


##### primary_connection(self)

Switch to primary DB connection

This is used for simulating multiple users performing actions by simulating two DB connections

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### secondary_connection(self)

Switch to secondary DB connection.

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### _rollback_connections(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### assertQueryEqual(self, first: str, second: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| first | str | - | - |
| second | str | - | - |


##### assertQueryCount(self, count)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | None | - | - |


##### assertRedisCallCounts(self, count)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | None | - | - |


##### assertRowsRead(self, count)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| count | None | - | - |


##### enable_safe_exec(cls) → None

Enable safe exec and disable them after test case is completed.

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |

**Returns**: `None`


##### set_user(self, user: str)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| user | str | - | - |


##### switch_site(self, site: str)

Switch connection to different site.
Note: Drops current site connection completely.

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| site | str | - | - |


##### freeze_time(self, time_to_freeze, is_utc = False)

**Decorators**: `@contextmanager`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| time_to_freeze | None | - | - |
| is_utc | None | False | - |




### FrappeTestCasePreparation

**Inherits from**: IntegrationTestPreparation

#### Methods

##### __call__(self, suite: unittest.TestSuite, app: str, category: str) → None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| suite | unittest.TestSuite | - | - |
| app | str | - | - |
| category | str | - | - |

**Returns**: `None`




## Functions

### colorize(text, color_code)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| text | None | - | - |
| color_code | None | - | - |

**Returns**: (none)



### __get_deprecation_class(graduation: str | None = None, class_name: str | None = None) → type

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| graduation | str | None | None | - |
| class_name | str | None | None | - |

**Returns**: `type`



### deprecated(original: str, marked: str, graduation: str, msg: str, stacklevel: int = 1)

Decorator to wrap a function/method as deprecated.

Arguments:
        - original: frappe.utils.make_esc  (fully qualified)
        - marked: 2024-09-13  (the date it has been marked)
        - graduation: v17  (generally: current version + 2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| original | str | - | - |
| marked | str | - | - |
| graduation | str | - | - |
| msg | str | - | - |
| stacklevel | int | 1 | - |

**Returns**: (none)



### deprecation_warning(marked: str, graduation: str, msg: str)

Warn in-place from a deprecated code path, for objects use `@deprecated` decorator from the deprectation_dumpster"

Arguments:
        - marked: 2024-09-13  (the date it has been marked)
        - graduation: v17  (generally: current version + 2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| marked | str | - | - |
| graduation | str | - | - |
| msg | str | - | - |

**Returns**: (none)



### _old_deprecated(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### _old_deprecation_warning(msg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| msg | None | - | - |

**Returns**: (none)



### make_esc(esc_chars)

Function generator for Escaping special characters

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| esc_chars | None | - | - |

**Returns**: (none)



### is_column_missing(e)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| e | None | - | - |

**Returns**: (none)



### show_progress(docnames, message, i, description)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| docnames | None | - | - |
| message | None | - | - |
| i | None | - | - |
| description | None | - | - |

**Returns**: (none)



### get_js(items)

Load JS code files.  Will also append translations
and extend `frappe._messages`

:param items: JSON list of paths of the js files to be loaded.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| items | None | - | - |

**Returns**: (none)



### read_multi_pdf(output) → bytes

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| output | None | - | - |

**Returns**: `bytes`



### gzip_compress(data, compresslevel = 5)

Compress data in one shot and return the compressed string.
Optional argument is the compression level, in range of 0-9.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |
| compresslevel | None | 5 | - |

**Returns**: (none)



### gzip_decompress(data)

Decompress a gzip compressed string in one shot.
Return the decompressed string.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| data | None | - | - |

**Returns**: (none)



### send_mail(email_queue_name, smtp_server_instance = None)

This is equivalent to EmailQueue.send.

This provides a way to make sending mail as a background job.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| email_queue_name | None | - | - |
| smtp_server_instance | None | None | - |

**Returns**: (none)



### get_translated_dict()

**Returns**: (none)



### validate_roles(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |

**Returns**: (none)



### test_runner_get_modules(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### test_runner_make_test_records()

**Returns**: (none)



### test_runner_make_test_objects()

**Returns**: (none)



### test_runner_make_test_records_for_doctype()

**Returns**: (none)



### test_runner_print_mandatory_fields()

**Returns**: (none)



### test_runner_get_test_record_log(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### test_runner_add_to_test_record_log(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### test_runner_main()

**Returns**: (none)



### test_xmlrunner_wrapper(output)

Convenience wrapper to keep method signature unchanged for XMLTestRunner and TextTestRunner

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| output | None | - | - |

**Returns**: (none)



### tests_update_system_settings(args, commit = False)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| args | None | - | - |
| commit | None | False | - |

**Returns**: (none)



### tests_get_system_setting(key)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| key | None | - | - |

**Returns**: (none)



### tests_change_settings()

**Returns**: (none)



### tests_patch_hooks()

**Returns**: (none)



### tests_debug_on()

**Returns**: (none)



### tests_timeout()

**Returns**: (none)



### get_tests_CompatFrappeTestCase()

Unfortunately, due to circular imports, we just have to copy the entire old implementation here, even though IntegrationTestCase is overwhelmingly api-compatible.

**Returns**: (none)



### get_compat_frappe_test_case_preparation(cfg)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cfg | None | - | - |

**Returns**: (none)



### model_trace_traced_field_context()

**Returns**: (none)



### tests_utils_get_dependencies(doctype)

Get the dependencies for the specified doctype

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### test_runner_get_dependencies(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### frappe_get_test_records(doctype)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |

**Returns**: (none)



### compat_preload_test_records_upfront(candidates: list)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| candidates | list | - | - |

**Returns**: (none)



### get_number_format_info(format: str) → tuple[str, str, int]

DEPRECATED: use `NumberFormat.from_string()` from `frappe.utils.number_format` instead.

Return the decimal separator, thousands separator and precision for the given number `format` string.

e.g. get_number_format_info('#,##,###.##') -> ('.', ',', 2)

Will return ('.', ',', 2) for format strings which can't be guessed.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| format | str | - | - |

**Returns**: `tuple[str, str, int]`



### boilerplate_modules_txt(dest, app_name, app_title)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| dest | None | - | - |
| app_name | None | - | - |
| app_title | None | - | - |

**Returns**: (none)



### decorator(func)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | None | - | - |

**Returns**: (none)



### deprecation_warning(message, category = DeprecationWarning, stacklevel = 1)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | None | - | - |
| category | None | DeprecationWarning | - |
| stacklevel | None | 1 | - |

**Returns**: (none)



### _runner()

**Returns**: (none)



### _commit_watcher()

**Returns**: (none)



### _rollback_db()

**Returns**: (none)



### _restore_thread_locals(flags)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| flags | None | - | - |

**Returns**: (none)



### _deprecated(message: str, category = FrappeDeprecationWarning, stacklevel = 1) → Callable[[T], T]

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| message | str | - | - |
| category | None | FrappeDeprecationWarning | - |
| stacklevel | None | 1 | - |

**Returns**: `Callable[[T], T]`



### decorator(func: T) → T

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| func | T | - | - |

**Returns**: `T`



### _sql_with_count()

**Returns**: (none)



### execute_command_and_count()

**Returns**: (none)



### _sql_with_count()

**Returns**: (none)



### wrapper()

**Returns**: (none)


