# Jinja Templating in ERPNext

Jinja templating patterns for Print Formats, Email Templates, Letter Heads, Portal Pages, and dynamic content rendering in ERPNext/Frappe.

---

## When to Use

USE for: Print Formats, Email Templates, Portal Pages (www/*.html), Letter Heads, Custom jenv methods

DO NOT USE for: Report Print Formats (they use JavaScript `{%= %}`), Client Scripts, Server Scripts

---

## Context Objects per Template Type

### Print Formats

| Object | Description |
|--------|-------------|
| `doc` | The document being printed |
| `frappe` | Frappe module with utility methods |
| `_()` | Translation function |

### Email Templates

| Object | Description |
|--------|-------------|
| `doc` | The linked document |
| `frappe` | Frappe module (limited) |

### Portal Pages

| Object | Description |
|--------|-------------|
| `frappe.session.user` | Current user |
| `frappe.form_dict` | Query parameters |
| `frappe.lang` | Current language |
| Custom context | Via Python controller |

---

## Accessing Document Fields

```jinja
{# Direct field access #}
{{ doc.name }}
{{ doc.customer_name }}
{{ doc.posting_date }}
{{ doc.docstatus }}          {# 0=Draft, 1=Submitted, 2=Cancelled #}

{# RECOMMENDED: get_formatted() respects field settings #}
{{ doc.get_formatted("posting_date") }}
{{ doc.get_formatted("grand_total") }}

{# Child table rows - pass parent doc #}
{% for row in doc.items %}
    {{ row.get_formatted("rate", doc) }}
    {{ row.get_formatted("amount", doc) }}
{% endfor %}

{# Linked document field (single query) #}
{{ frappe.db.get_value("Customer", doc.customer, "customer_group") }}

{# Get full linked document #}
{% set customer = frappe.get_doc("Customer", doc.customer) %}
{{ customer.customer_name }}

{# Multiple fields from linked doc #}
{% set cust_info = frappe.db.get_value("Customer", doc.customer, ["territory", "customer_group"], as_dict=True) %}
{{ cust_info.territory }} / {{ cust_info.customer_group }}
```

---

## Print Format Templates

### Basic Structure

```html
{% raw %}
<style>
    .header { background: #f5f5f5; padding: 15px; }
    .table { width: 100%; border-collapse: collapse; }
    .table th, .table td { border: 1px solid #ddd; padding: 8px; }
    .text-right { text-align: right; }
</style>

<div class="print-format">
    <h1>{{ doc.select_print_heading or _("Invoice") }}</h1>
    <p>{{ doc.name }}</p>
    <p>{{ _("Date") }}: {{ doc.get_formatted("posting_date") }}</p>
    <p>Customer: {{ doc.customer_name }}</p>

    <table class="table">
        <thead>
            <tr>
                <th>#</th>
                <th>{{ _("Item") }}</th>
                <th>{{ _("Qty") }}</th>
                <th class="text-right">{{ _("Rate") }}</th>
                <th class="text-right">{{ _("Amount") }}</th>
            </tr>
        </thead>
        <tbody>
            {% for item in doc.items %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ item.item_code }}<br><small>{{ item.description | striptags | truncate(80) }}</small></td>
                <td>{{ item.qty }} {{ item.uom }}</td>
                <td class="text-right">{{ item.get_formatted("rate", doc) }}</td>
                <td class="text-right">{{ item.get_formatted("amount", doc) }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <p><strong>{{ _("Grand Total") }}:</strong> {{ doc.get_formatted("grand_total") }}</p>
    <p><em>{{ frappe.utils.money_in_words(doc.grand_total, doc.currency) }}</em></p>
</div>
{% endraw %}
```

---

## Conditional Blocks

```jinja
{# If / elif / else #}
{% if doc.status == "Paid" %}
    <span class="label-success">{{ _("Paid") }}</span>
{% elif doc.status == "Overdue" %}
    <span class="label-danger">{{ _("Overdue") }}</span>
{% else %}
    <span>{{ doc.status }}</span>
{% endif %}

{# Check if field has value #}
{% if doc.customer_address %}
    <p>{{ doc.customer_address }}</p>
{% endif %}

{# Check child table not empty #}
{% if doc.items | length > 0 %}
    {# render items table #}
{% endif %}

{# Ternary-style inline #}
<td>{{ "Yes" if item.is_stock_item else "No" }}</td>
```

---

## Formatting Functions

### Money and Number

| Expression | Description | Output Example |
|------------|-------------|----------------|
| `frappe.utils.fmt_money(val, currency="VND")` | Format with currency symbol | `1,234,567 VND` |
| `frappe.utils.money_in_words(val, currency)` | Amount in words | `VND One Million...` |
| `frappe.utils.flt(val, 2)` | Float with precision | `100.46` |
| `frappe.utils.cint(val)` | Integer conversion | `10` |
| `frappe.utils.rounded(val, 2)` | Rounded float | `100.46` |
| `frappe.format(val, {"fieldtype": "Currency"})` | Format by fieldtype | varies |

### Date

| Expression | Description | Output Example |
|------------|-------------|----------------|
| `frappe.utils.formatdate(date, "dd-MM-yyyy")` | Custom date format | `14-02-2026` |
| `frappe.utils.formatdate(date)` | System default format | varies |
| `frappe.utils.format_datetime(datetime)` | Datetime format | `14-02-2026 10:30:00` |
| `frappe.format_date(doc.posting_date)` | Short format date | varies |
| `frappe.utils.today()` | Current date string | `2026-02-14` |

### String Filters (Standard Jinja)

```jinja
{{ doc.customer_name | upper }}              {# CUSTOMER NAME #}
{{ doc.customer_name | lower }}              {# customer name #}
{{ doc.customer_name | title }}              {# Customer Name #}
{{ doc.description | truncate(100) }}        {# First 100 chars... #}
{{ doc.description | striptags }}            {# Remove HTML tags #}
{{ doc.description | escape }}               {# HTML-escape #}
{{ doc.notes | default("No notes", true) }}  {# Default if falsy #}
{{ doc.name | replace("SO-", "Order-") }}    {# String replace #}
{{ html_content | safe }}                    {# Trusted content only! #}
```

### List/Collection Filters

```jinja
{# Join list to string #}
{{ doc.items | map(attribute='item_code') | join(", ") }}

{# Sum attribute #}
Total qty: {{ doc.items | sum(attribute='qty') }}

{# Sort #}
{% for item in doc.items | sort(attribute='item_code') %}
    {{ item.item_code }}
{% endfor %}

{# Groupby #}
{% for group_name, items in doc.items | groupby('item_group') %}
    <h3>{{ group_name }}</h3>
    {% for item in items %}
        {{ item.item_code }}: {{ item.qty }}
    {% endfor %}
{% endfor %}

{# Select specific items #}
{% for item in doc.items | selectattr('qty', 'gt', 0) %}
    {{ item.item_code }}
{% endfor %}
```

---

## Loop Variables

```jinja
{% for item in doc.items %}
    {{ loop.index }}       {# 1-based counter #}
    {{ loop.index0 }}      {# 0-based counter #}
    {{ loop.first }}        {# True if first iteration #}
    {{ loop.last }}         {# True if last iteration #}
    {{ loop.length }}       {# Total number of items #}
{% else %}
    <p>{{ _("No items") }}</p>
{% endfor %}
```

### Namespace for Mutable Variables in Loops

```jinja
{% set ns = namespace(total_qty=0, total_amount=0) %}

{% for item in doc.items %}
    {% set ns.total_qty = ns.total_qty + item.qty %}
    {% set ns.total_amount = ns.total_amount + item.amount %}
{% endfor %}

<p>Total Qty: {{ ns.total_qty }}, Total: {{ frappe.utils.fmt_money(ns.total_amount, currency=doc.currency) }}</p>
```

---

## Email Templates

```jinja
<p>{{ _("Dear") }} {{ doc.customer_name }},</p>

<p>{{ _("Invoice") }} <strong>{{ doc.name }}</strong> {{ _("for") }}
{{ doc.get_formatted("grand_total") }} {{ _("is due.") }}</p>

<p>{{ _("Due Date") }}: {{ frappe.format_date(doc.due_date) }}</p>

{% if doc.items %}
<ul>
{% for item in doc.items %}
    <li>{{ item.item_name }} - {{ item.qty }} x {{ item.get_formatted("rate", doc) }}</li>
{% endfor %}
</ul>
{% endif %}

<p>{{ _("Best regards") }},<br>
{{ frappe.db.get_value("Company", doc.company, "company_name") }}</p>
```

### Notification Template Variables

```jinja
{{ doc }}                                                    {# Document object #}
{{ frappe.utils.get_url_to_form(doc.doctype, doc.name) }}    {# URL to document #}
{{ frappe.utils.get_url() }}/app/{{ frappe.scrub(doc.doctype) }}/{{ doc.name }}
```

---

## Letter Head

```html
<div class="letter-head">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <img src="{{ frappe.db.get_value('Company', doc.company, 'company_logo') }}"
                 style="max-height: 80px;">
        </div>
        <div style="text-align: right;">
            <h2 style="margin: 0;">{{ frappe.db.get_value('Company', doc.company, 'company_name') }}</h2>
            <p style="margin: 4px 0;">MST: {{ frappe.db.get_value('Company', doc.company, 'tax_id') }}</p>
            <p style="margin: 4px 0;">{{ frappe.db.get_value('Company', doc.company, 'phone_no') }}</p>
        </div>
    </div>
    <hr style="border-top: 2px solid #333; margin-top: 10px;">
</div>
```

---

## Portal Page with Controller

### www/projects/index.html

```jinja
{% extends "templates/web.html" %}

{% block title %}{{ _("Projects") }}{% endblock %}

{% block page_content %}
<h1>{{ _("Projects") }}</h1>

{% if frappe.session.user != 'Guest' %}
    <p>{{ _("Welcome") }}, {{ frappe.get_fullname() }}</p>
{% endif %}

{% for project in projects %}
    <div class="project">
        <h3>{{ project.title }}</h3>
        <p>{{ project.description | truncate(150) }}</p>
    </div>
{% else %}
    <p>{{ _("No projects found.") }}</p>
{% endfor %}
{% endblock %}
```

### www/projects/index.py

```python
import frappe

def get_context(context):
    context.title = "Projects"
    context.projects = frappe.get_all(
        "Project",
        filters={"is_public": 1},
        fields=["name", "title", "description"],
        order_by="creation desc"
    )
    return context
```

---

## Advanced Patterns

### Reusable Macros

```jinja
{% macro render_address(address_name) %}
    {% if address_name %}
        {% set addr = frappe.get_doc("Address", address_name) %}
        <p>
            {{ addr.address_line1 }}<br>
            {% if addr.address_line2 %}{{ addr.address_line2 }}<br>{% endif %}
            {{ addr.city }}{% if addr.state %}, {{ addr.state }}{% endif %} {{ addr.pincode }}<br>
            {{ addr.country }}
        </p>
    {% endif %}
{% endmacro %}

{{ render_address(doc.customer_address) }}
{{ render_address(doc.shipping_address_name) }}
```

### Custom Queries in Templates

```jinja
{% set outstanding = frappe.db.sql("""
    SELECT SUM(outstanding_amount) as total
    FROM `tabSales Invoice`
    WHERE customer = %s AND docstatus = 1
""", doc.customer, as_dict=True) %}

{% if outstanding and outstanding[0].total %}
    <p class="text-danger">
        Outstanding: {{ frappe.utils.fmt_money(outstanding[0].total, currency=doc.currency) }}
    </p>
{% endif %}
```

### QR Code

```jinja
{% set qr_url = frappe.utils.get_url_to_form(doc.doctype, doc.name) %}
<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={{ qr_url | urlencode }}">
```

### Multi-Page Print (Page Breaks)

```html
<style>
    .page-break { break-before: page; }  /* v16 Chrome PDF */
    @media print { .no-print { display: none; } }
</style>

<div class="page-1">
    {# Page 1: Header and items #}
</div>
<div class="page-break"></div>
<div class="page-2">
    {# Page 2: Terms and signatures #}
</div>
```

---

## Custom Jinja Methods via jenv Hook

### hooks.py

```python
jenv = {
    "methods": ["myapp.jinja.methods"],
    "filters": ["myapp.jinja.filters"]
}
```

### myapp/jinja/methods.py

```python
import frappe

def get_company_logo(company):
    return frappe.db.get_value("Company", company, "company_logo") or ""
```

### Usage

```jinja
<img src="{{ get_company_logo(doc.company) }}">
```

---

## Report Print Formats (NOT Jinja!)

**WARNING**: Report Print Formats use JavaScript templating, NOT Jinja.

| Aspect | Jinja (Print Formats) | JS (Report Print Formats) |
|--------|----------------------|---------------------------|
| Output | `{{ }}` | `{%= %}` |
| Code | `{% %}` | `{% %}` |
| Language | Python | JavaScript |

```html
<!-- JS Template for Reports -->
{% for(var i=0; i<data.length; i++) { %}
<tr><td>{%= data[i].name %}</td></tr>
{% } %}
```

---

## V16: Chrome PDF Rendering

v16 uses Chrome-based PDF instead of wkhtmltopdf.

| Aspect | v14/v15 (wkhtmltopdf) | v16 (Chrome) |
|--------|----------------------|---------------|
| CSS Support | Limited CSS3 | Full modern CSS |
| Flexbox/Grid | Partial | Full support |
| Page breaks | `page-break-*` | `break-*` preferred |
| Fonts | System fonts | Web fonts supported |

```python
# site_config.json
{
    "pdf_engine": "chrome",  # or "wkhtmltopdf" for legacy
    "chrome_path": "/usr/bin/chromium"
}
```

---

## Critical Rules

### ALWAYS
1. Use `_()` for all user-facing strings
2. Use `get_formatted()` for currency/date fields in print formats
3. Use default values: `{{ value | default('') }}`
4. Child table rows: `row.get_formatted("field", doc)` (pass parent doc)

### NEVER
1. Execute queries in loops (N+1 problem) - use `frappe.get_cached_doc()`
2. Use `| safe` for user input (XSS risk)
3. Heavy calculations in templates (do in Python)
4. Jinja syntax in Report Print Formats (they use JS `{%= %}`)
