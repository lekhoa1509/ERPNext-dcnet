# API Reference: html_template.py

**Language**: Python

**Source**: `gettext/extractors/html_template.py`

---

## Functions

### extract()

Extract messages from Jinja and JS microtemplates.

Reuse the babel_extract function from jinja2.ext, but handle our own implementation of `_()`.
To handle JS microtemplates, parse all code again using regex.

**Returns**: (none)


