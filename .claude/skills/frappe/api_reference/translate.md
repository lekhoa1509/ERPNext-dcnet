# API Reference: translate.py

**Language**: Python

**Source**: `translate.py`

---

## Functions

### get_language(lang_list: list | None = None) → str

Set `frappe.local.lang` from HTTP headers at beginning of request

Order of priority for setting language:
1. Form Dict => _lang
2. Cookie => preferred_language (Non authorized user)
3. Request Header => Accept-Language (Non authorized user)
4. User document => language
5. System Settings => language

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang_list | list | None | None | - |

**Returns**: `str`



### get_parent_language(lang: str) → str

If the passed language is a variant, return its parent

Eg:
        1. zh-TW -> zh
        2. sr-BA -> sr

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | str | - | - |

**Returns**: `str`



### get_user_lang(user: str | None = None) → str

Set frappe.local.lang from user preferences on session beginning or resumption

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| user | str | None | None | - |

**Returns**: `str`



### get_lang_code(lang: str) → str | None

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | str | - | - |

**Returns**: `str | None`



### set_default_language(lang)

Set Global default language

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |

**Returns**: (none)



### get_lang_dict()

Return all languages in dict format, full name is the key e.g. `{"english":"en"}`.

**Returns**: (none)



### get_messages_for_boot()

Return all message translations that are required on boot.

**Returns**: (none)



### get_all_translations(lang: str) → dict[str, str]

Load and return the entire translations dictionary for a language from apps + user translations.

:param lang: Language Code, e.g. `hi` or `es-CO`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | str | - | - |

**Returns**: `dict[str, str]`



### get_translations_from_apps(lang, apps = None)

Combine all translations from `.csv` files in all `apps`.
For derivative languages (es-GT), take translations from the
base language (es) and then update translations from the child (es-GT)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |
| apps | None | None | - |

**Returns**: (none)



### get_translations_from_csv(lang, app)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |
| app | None | - | - |

**Returns**: (none)



### get_translation_dict_from_file(path, lang, app, throw = False) → dict[str, str]

Return translation dict from given CSV file at path

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| lang | None | - | - |
| app | None | - | - |
| throw | None | False | - |

**Returns**: `dict[str, str]`



### get_user_translations(lang)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |

**Returns**: (none)



### clear_cache()

Clear all translation assets from :meth:`frappe.cache`

**Returns**: (none)



### get_messages_for_app(app, deduplicate = True)

Return all messages (list) for a specified `app`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| deduplicate | None | True | - |

**Returns**: (none)



### get_messages_from_navbar()

Return all labels from Navbar Items, as specified in Navbar Settings.

**Returns**: (none)



### get_messages_from_doctype(name)

Extract all translatable messages for a doctype. Includes labels, Python code,
Javascript code, html templates

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_messages_from_workflow(doctype = None, app_name = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | None | - |
| app_name | None | None | - |

**Returns**: (none)



### get_messages_from_custom_fields(app_name)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | - | - |

**Returns**: (none)



### get_messages_from_page(name)

Return all translatable strings from a :class:`frappe.core.doctype.Page`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### get_messages_from_report(name)

Return all translatable strings from a :class:`frappe.core.doctype.Report`.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| name | None | - | - |

**Returns**: (none)



### _get_messages_from_page_or_report(doctype, name, module = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| doctype | None | - | - |
| name | None | - | - |
| module | None | None | - |

**Returns**: (none)



### get_server_messages(app)

Extracts all translatable strings (tagged with :func:`frappe._`) from Python modules
inside an app

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |

**Returns**: (none)



### get_messages_from_include_files(app_name = None)

Return messages from js files included at time of boot like desk.min.js for desk and web.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | None | - |

**Returns**: (none)



### get_all_messages_from_js_files(app_name = None)

Extracts all translatable strings from app `.js` files

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app_name | None | None | - |

**Returns**: (none)



### get_messages_from_file(path: str) → list[tuple[str, str, str | None, int]]

Return a list of transatable strings from a code file.

:param path: path of the code file

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | str | - | - |

**Returns**: `list[tuple[str, str, str | None, int]]`



### extract_messages_from_python_code(code: str) → list[tuple[int, str, str | None]]

Extracts translatable strings from Python code using babel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |

**Returns**: `list[tuple[int, str, str | None]]`



### extract_messages_from_javascript_code(code: str) → list[tuple[int, str, str | None]]

Extracts translatable strings from JavaScript code using babel.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| code | str | - | - |

**Returns**: `list[tuple[int, str, str | None]]`



### read_csv_file(path)

Read CSV file and return as list of list

:param path: File path

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |

**Returns**: (none)



### write_csv_file(path, app_messages, lang_dict)

Write translation CSV file.

:param path: File path, usually `[app]/translations`.
:param app_messages: Translatable strings for this app.
:param lang_dict: Full translated dict.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| path | None | - | - |
| app_messages | None | - | - |
| lang_dict | None | - | - |

**Returns**: (none)



### get_untranslated(lang, untranslated_file, get_all = False, app = '_ALL_APPS')

Return all untranslated strings for a language and write in a file.

:param lang: Language code.
:param untranslated_file: Output file path.
:param get_all: Return all strings, translated or not.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |
| untranslated_file | None | - | - |
| get_all | None | False | - |
| app | None | '_ALL_APPS' | - |

**Returns**: (none)



### update_translations(lang, untranslated_file, translated_file, app = '_ALL_APPS')

Update translations from a source and target file for a given language.

:param lang: Language code (e.g. `en`).
:param untranslated_file: File path with the messages in English.
:param translated_file: File path with messages in language to be updated.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |
| untranslated_file | None | - | - |
| translated_file | None | - | - |
| app | None | '_ALL_APPS' | - |

**Returns**: (none)



### import_translations(lang, path)

Import translations from file in standard format

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| lang | None | - | - |
| path | None | - | - |

**Returns**: (none)



### migrate_translations(source_app, target_app)

Migrate target-app-specific translations from source-app to target-app

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source_app | None | - | - |
| target_app | None | - | - |

**Returns**: (none)



### rebuild_all_translation_files()

Rebuild all translation files: `[app]/translations/[lang].csv`.

**Returns**: (none)



### write_translations_file(app, lang, full_dict = None, app_messages = None)

Write a translation file for a given language.

:param app: `app` for which translations are to be written.
:param lang: Language code.
:param full_dict: Full translated language dict (optional).
:param app_messages: Source strings (optional).

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| app | None | - | - |
| lang | None | - | - |
| full_dict | None | None | - |
| app_messages | None | None | - |

**Returns**: (none)



### send_translations(translation_dict)

Append translated dict in `frappe.local.response`

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| translation_dict | None | - | - |

**Returns**: (none)



### deduplicate_messages(messages)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| messages | None | - | - |

**Returns**: (none)



### update_translations_for_source(source = None, translation_dict = None)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| source | None | None | - |
| translation_dict | None | None | - |

**Returns**: (none)



### get_all_languages(with_language_name: bool = False) → list

Return all enabled language codes ar, ch etc.

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| with_language_name | bool | False | - |

**Returns**: `list`



### get_preferred_language_cookie()

**Returns**: (none)



### get_translated_doctypes()

**Returns**: (none)



### print_language(language: str)

Ensure correct globals for printing in a specific language.

Usage:

```
with print_language("de"):
    html = frappe.get_print(...)
```

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| language | str | - | - |

**Returns**: (none)



### _merge_translations()

**Returns**: (none)



### _read_from_db()

**Returns**: (none)



### escape_newlines(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |

**Returns**: (none)



### restore_newlines(s)

**Parameters**:

| Name | Type | Default | Description |
|------|------|---------|-------------|
| s | None | - | - |

**Returns**: (none)



### get_all_language_with_name()

**Returns**: (none)


