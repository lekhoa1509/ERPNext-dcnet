# API Reference: test_utils.py

**Language**: Python

**Source**: `tests/test_utils.py`

---

## Classes

### Capturing

**Inherits from**: list

#### Methods

##### __enter__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### __exit__(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestFilters

**Inherits from**: IntegrationTestCase

#### Methods

##### test_simple_dict(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_multiple_dict(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_list_filters(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_list_filters_as_list(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_lt_gt(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_date_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_filter_evaluation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timespan(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_operator(self)

Test 'is' operator for checking if values are set or not set.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_in_operators(self)

Test 'in' and 'not in' operators with and without fieldtype casting.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_operator_case_insensitive(self)

Test that 'is' operator patterns are case insensitive.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_link_to_report_with_between_filter(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestMoney

**Inherits from**: IntegrationTestCase

#### Methods

##### test_money_in_words(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_money_in_words_without_fraction(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDataManipulation

**Inherits from**: IntegrationTestCase

#### Methods

##### test_scrub_urls(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestFieldCasting

**Inherits from**: IntegrationTestCase

#### Methods

##### test_str_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_float_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_int_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_datetime_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_date_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_time_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestMathUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_floor(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_ceil(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestHTMLUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_clean_email_html(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_sanitize_html(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestValidationUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_valid_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_email(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_valid_phone(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_name(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_iban(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestImage

**Inherits from**: IntegrationTestCase

#### Methods

##### test_strip_exif_data(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_optimize_image(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestPythonExpressions

**Inherits from**: IntegrationTestCase

#### Methods

##### test_validation_for_good_python_expression(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validation_for_bad_python_expression(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDiffUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### setUpClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### tearDownClass(cls)

**Decorators**: `@classmethod`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| cls | None | - | - |


##### test_version_query(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_field_value_from_version(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_version_diff(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDateUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_first_day_of_week(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_last_day_of_week(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_is_last_day_of_the_month(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_time(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_timedelta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_to_timedelta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_add_date_utils(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_duration_to_sec(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_format_duration(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_timespan_date_range(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_timesmap_utils(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_datetime(self, original)

**Decorators**: `@given(st.datetimes())`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| original | None | - | - |


##### test_get_datetime_tz_aware(self, original)

**Decorators**: `@given(st.datetimes(timezones=st.timezones()))`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| original | None | - | - |


##### test_pretty_date(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_date_from_timegrain(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestResponse

**Inherits from**: IntegrationTestCase

#### Methods

##### test_json_handler(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestTimeDeltaUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_format_timedelta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_timedelta(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestXlsxUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_unescape(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestLinkTitle

**Inherits from**: IntegrationTestCase

#### Methods

##### test_link_title_doctypes_in_boot_info(self)

Test that doctypes are added to link_title_map in boot_info

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_link_titles_on_getdoc(self)

Test that link titles are added to the doctype on getdoc

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestAppParser

**Inherits from**: MockedRequestTestCase

#### Methods

##### test_app_name_parser(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestIntrospectionMagic

Test utils that inspect live objects

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_newargs(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_strip_off_kwargs_when_not_supported(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestMakeRandom

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_random(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_can_make(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_how_many(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestLazyLoader

**Inherits from**: IntegrationTestCase

#### Methods

##### test_lazy_import_module(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestIdenticon

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_gravatar(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_generate_identicon(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestContainerUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_dict_to_str(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_remove_blanks(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestLocks

**Inherits from**: IntegrationTestCase

#### Methods

##### test_locktimeout(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_global_lock(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestMiscUtils

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_file_timestamp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_execute_in_shell(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_all_sites(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_site_info(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_get_url_to_form(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_safe_json_load(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_url_expansion(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestTypingValidations

**Inherits from**: IntegrationTestCase

#### Methods

##### test_validate_whitelisted_api(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_validate_whitelisted_doc_method(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestTBSanitization

**Inherits from**: IntegrationTestCase

#### Methods

##### test_traceback_sanitzation(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestRounding

**Inherits from**: IntegrationTestCase

#### Methods

##### test_normal_rounding(self)

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'rounding_method': 'Commercial Rounding'})`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_normal_rounding_as_argument(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_normal_rounding_property(self, number, precision)

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'rounding_method': 'Commercial Rounding'})`, `@given(st.decimals(min_value=-100000000.0, max_value=100000000.0), st.integers(min_value=-2, max_value=4))`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| number | None | - | - |
| precision | None | - | - |


##### test_bankers_rounding(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_bankers_rounding_property(self, number, precision)

**Decorators**: `@IntegrationTestCase.change_settings('System Settings', {'rounding_method': "Banker's Rounding"})`, `@given(st.decimals(min_value=-100000000.0, max_value=100000000.0), st.integers(min_value=-2, max_value=4))`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| number | None | - | - |
| precision | None | - | - |


##### test_default_rounding(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_cint(self, floating_point, integer)

**Decorators**: `@given(st.floats(min_value=-2 ** 32 - 1, max_value=2 ** 32 + 1), st.integers(min_value=-2 ** 63 - 1, max_value=2 ** 63 + 1))`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |
| floating_point | None | - | - |
| integer | None | - | - |




### TestArgumentTypingValidations

**Inherits from**: IntegrationTestCase

#### Methods

##### test_validate_argument_types(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestChangeLog

**Inherits from**: IntegrationTestCase

#### Methods

##### test_get_remote_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_github_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestCrypto

**Inherits from**: IntegrationTestCase

#### Methods

##### test_hashing(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestURLTrackers

**Inherits from**: IntegrationTestCase

#### Methods

##### test_add_trackers_to_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_parse_and_map_trackers_from_url(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_map_trackers(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TestDataUtils

**Inherits from**: UnitTestCase

#### Methods

##### setUp(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### tearDown(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_comma_and(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |


##### test_comma_or(self)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| self | None | - | - |




### TEST

**Inherits from**: Enum



## Functions

### f(a, b = 2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | None | - | - |
| b | None | 2 | - |

**Returns**: (none)



### f(a, b = 2)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | None | - | - |
| b | None | 2 | - |

**Returns**: (none)



### simple(string: str, number: int)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | str | - | - |
| number | int | - | - |

**Returns**: (none)



### varkw(string: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| string | str | - | - |

**Returns**: (none)



### test_simple_types(a: int, b: float, c: bool)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | int | - | - |
| b | float | - | - |
| c | bool | - | - |

**Returns**: (none)



### test_sequence(a: str, b: list[dict] | None = None, c: dict[str, int] | None = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | str | - | - |
| b | list[dict] | None | None | - |
| c | dict[str, int] | None | None | - |

**Returns**: (none)



### test_doctypes(a: DocType | dict)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | DocType | dict | - | - |

**Returns**: (none)



### test_mocks(a: str)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| a | str | - | - |

**Returns**: (none)


