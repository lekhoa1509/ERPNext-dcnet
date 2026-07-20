# Frappe REST API

Complete reference for building and consuming Frappe REST APIs, including authentication, resource endpoints, whitelisted methods, and client-side integration.

---

## API Architecture Overview

Frappe exposes two categories of REST endpoints:

| Endpoint | Pattern | Purpose |
|----------|---------|---------|
| **Resource API** | `/api/resource/{DocType}` | CRUD operations on documents |
| **Method API** | `/api/method/{dotted.path}` | Custom server-side functions |

---

## @frappe.whitelist() -- Custom API Methods

### Basic Whitelisted Method

```python
# dcnet_apps/fitting/api.py

import frappe
from frappe import _


@frappe.whitelist()
def get_fitting_summary(session_name):
    """Get a summary of a fitting session.

    Accessible at: /api/method/dcnet_apps.fitting.api.get_fitting_summary
    Requires: Logged in user with permission to read Fitting Session
    """
    session = frappe.get_doc("Fitting Session", session_name)
    session.check_permission("read")

    return {
        "name": session.name,
        "customer": session.customer,
        "status": session.workflow_state,
        "measurements_count": len(session.measurements),
        "services": [s.service_type for s in session.services]
    }
```

### Allow Guest Access

```python
@frappe.whitelist(allow_guest=True)
def get_public_fitting_slots(date):
    """Public endpoint -- no login required.

    Accessible at: /api/method/dcnet_apps.fitting.api.get_public_fitting_slots
    """
    slots = frappe.get_all(
        "Fitting Session",
        filters={
            "fitting_date": date,
            "workflow_state": "Scheduled"
        },
        fields=["name", "fitting_date", "time_slot"],
        order_by="time_slot asc"
    )
    return slots
```

### Restrict HTTP Methods

```python
@frappe.whitelist(methods=["POST"])
def book_fitting(customer, date, service_type):
    """Only accepts POST requests."""
    session = frappe.get_doc({
        "doctype": "Fitting Session",
        "customer": customer,
        "fitting_date": date,
        "services": [{"service_type": service_type}]
    })
    session.insert()
    return {"name": session.name, "status": "booked"}


@frappe.whitelist(methods=["GET"])
def check_availability(date):
    """Only accepts GET requests."""
    count = frappe.db.count("Fitting Session", {"fitting_date": date})
    max_slots = 10
    return {"date": date, "available": max_slots - count, "total": max_slots}


@frappe.whitelist(methods=["DELETE"])
def cancel_fitting(session_name):
    """Only accepts DELETE requests."""
    session = frappe.get_doc("Fitting Session", session_name)
    session.check_permission("cancel")
    session.cancel()
    return {"status": "cancelled"}
```

### Handling Request Parameters

```python
@frappe.whitelist()
def search_fittings(customer=None, status=None, from_date=None, to_date=None):
    """Parameters come from query string (GET) or form body (POST).

    GET:  /api/method/dcnet_apps.fitting.api.search_fittings?customer=CUST-001&status=Completed
    POST: {"customer": "CUST-001", "status": "Completed"}
    """
    filters = {}
    if customer:
        filters["customer"] = customer
    if status:
        filters["workflow_state"] = status
    if from_date and to_date:
        filters["fitting_date"] = ["between", [from_date, to_date]]

    return frappe.get_all(
        "Fitting Session",
        filters=filters,
        fields=["name", "customer", "fitting_date", "workflow_state"],
        order_by="fitting_date desc",
        limit_page_length=20
    )


@frappe.whitelist()
def bulk_update(session_names, new_status):
    """Accept JSON arrays/objects.

    POST body: {"session_names": "[\"FS-001\", \"FS-002\"]", "new_status": "Completed"}
    Note: Arrays arrive as JSON strings -- must parse.
    """
    import json
    if isinstance(session_names, str):
        session_names = json.loads(session_names)

    updated = []
    for name in session_names:
        doc = frappe.get_doc("Fitting Session", name)
        doc.custom_status = new_status
        doc.save()
        updated.append(name)

    return {"updated": updated, "count": len(updated)}
```

---

## Resource API -- /api/resource/{DocType}

### CRUD Operations

```
# List documents
GET /api/resource/Fitting Session
GET /api/resource/Fitting Session?filters=[["status","=","Draft"]]&fields=["name","customer"]&limit_page_length=20&order_by=creation desc

# Get single document
GET /api/resource/Fitting Session/FS-00001

# Create document
POST /api/resource/Fitting Session
Body: {"customer": "CUST-001", "fitting_date": "2026-03-15"}

# Update document
PUT /api/resource/Fitting Session/FS-00001
Body: {"workflow_state": "Scheduled"}

# Delete document
DELETE /api/resource/Fitting Session/FS-00001
```

### Filter Syntax

```
# Exact match
?filters=[["customer","=","CUST-001"]]

# Multiple conditions (AND)
?filters=[["customer","=","CUST-001"],["status","=","Draft"]]

# Operators
?filters=[["creation",">=","2026-01-01"]]
?filters=[["status","in",["Draft","Scheduled"]]]
?filters=[["status","not in",["Cancelled"]]]
?filters=[["customer_name","like","%Golf%"]]
?filters=[["fitting_date","between",["2026-01-01","2026-03-31"]]]
?filters=[["custom_field","is","set"]]
?filters=[["custom_field","is","not set"]]

# Simple dict filters (shorthand)
?filters={"customer":"CUST-001","status":"Draft"}
```

### Pagination and Sorting

```
# Pagination
?limit_page_length=20&limit_start=0    # Page 1
?limit_page_length=20&limit_start=20   # Page 2

# No pagination (get all -- use carefully)
?limit_page_length=0

# Sorting
?order_by=creation desc
?order_by=fitting_date asc, name desc
```

### Field Selection

```
# Specific fields
?fields=["name","customer","fitting_date","workflow_state"]

# All fields (including standard)
?fields=["*"]

# Child table fields
?fields=["name","customer","services.service_type","services.amount"]
```

---

## Authentication

### Session Cookie (Default -- Browser)

Frappe's default auth uses session cookies set after login:

```
POST /api/method/login
Content-Type: application/json

{"usr": "user@example.com", "pwd": "password"}
```

Response sets `sid` cookie. Subsequent requests use this cookie automatically.

### API Key + Secret

```python
# Generate via: User > API Access > Generate Keys
# Header format:
# Authorization: token api_key:api_secret
```

```bash
# curl example
curl -H "Authorization: token abc123:xyz789" \
     https://flow.local/api/resource/Fitting%20Session
```

### Token Auth (Bearer)

```python
# OAuth2 bearer token or Frappe token
# Authorization: Bearer <token>
```

### API Key Authentication in Python

```python
import requests

API_KEY = "abc123def456"
API_SECRET = "xyz789uvw012"

session = requests.Session()
session.headers.update({
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json"
})

# List fitting sessions
response = session.get(
    "https://flow.local/api/resource/Fitting Session",
    params={
        "filters": '[["status","=","Draft"]]',
        "fields": '["name","customer","fitting_date"]',
        "limit_page_length": 20
    }
)
data = response.json()
print(data["data"])  # List of documents

# Create a document
response = session.post(
    "https://flow.local/api/resource/Fitting Session",
    json={
        "customer": "CUST-001",
        "fitting_date": "2026-03-15",
        "services": [
            {"service_type": "Club Fitting"}
        ]
    }
)
new_doc = response.json()
print(new_doc["data"]["name"])
```

### OAuth2 Setup

```python
# 1. Create OAuth Client in Frappe
# Setup > OAuth Client > New
# Set: redirect URIs, default redirect URI, grant type

# 2. Authorization flow
# GET /api/method/frappe.integrations.oauth2.authorize?client_id=...&redirect_uri=...&response_type=code
# POST /api/method/frappe.integrations.oauth2.get_token (exchange code for token)
# Use token: Authorization: Bearer <access_token>
```

---

## Client-Side API Calls (frappe.call)

### Basic frappe.call()

```javascript
// Call a whitelisted method
frappe.call({
    method: "dcnet_apps.fitting.api.get_fitting_summary",
    args: {
        session_name: "FS-00001"
    },
    callback: function(r) {
        if (r.message) {
            console.log(r.message);  // Server return value is in r.message
        }
    },
    error: function(r) {
        frappe.msgprint(__("Error fetching fitting summary"));
    }
});
```

### Async/Await Pattern

```javascript
// Modern async pattern
async function getFittingSummary(sessionName) {
    try {
        const response = await frappe.call({
            method: "dcnet_apps.fitting.api.get_fitting_summary",
            args: { session_name: sessionName },
            async: true
        });
        return response.message;
    } catch (error) {
        frappe.msgprint(__("Failed to load summary"));
        throw error;
    }
}
```

### frappe.xcall() -- Promise-Based

```javascript
// Cleaner promise-based API (v14+)
const result = await frappe.xcall(
    "dcnet_apps.fitting.api.get_fitting_summary",
    { session_name: "FS-00001" }
);
console.log(result);  // Direct return value (no .message wrapper)
```

### Resource API from Client

```javascript
// Get a document
frappe.db.get_doc("Fitting Session", "FS-00001").then(doc => {
    console.log(doc.customer);
});

// Get specific field value
frappe.db.get_value("Fitting Session", "FS-00001", "workflow_state").then(r => {
    console.log(r.message.workflow_state);
});

// Get list of documents
frappe.db.get_list("Fitting Session", {
    filters: { workflow_state: "Draft" },
    fields: ["name", "customer", "fitting_date"],
    limit_page_length: 20,
    order_by: "fitting_date desc"
}).then(data => {
    console.log(data);
});

// Get count
frappe.db.count("Fitting Session", {
    workflow_state: "Scheduled"
}).then(count => {
    console.log(`${count} sessions scheduled`);
});

// Insert a document
frappe.db.insert({
    doctype: "Fitting Session",
    customer: "CUST-001",
    fitting_date: "2026-03-15"
}).then(doc => {
    console.log("Created:", doc.name);
});

// Set a value (single field update)
frappe.db.set_value("Fitting Session", "FS-00001", "custom_notes", "Updated via API");
```

---

## File Upload API

### Upload via /api/method/upload_file

```javascript
// Client-side file upload
let fileInput = document.querySelector('input[type="file"]');
let file = fileInput.files[0];

let formData = new FormData();
formData.append("file", file);
formData.append("doctype", "Fitting Session");
formData.append("docname", "FS-00001");
formData.append("fieldname", "attachment");
formData.append("is_private", 1);

fetch("/api/method/upload_file", {
    method: "POST",
    body: formData,
    headers: {
        "X-Frappe-CSRF-Token": frappe.csrf_token
    }
})
.then(r => r.json())
.then(data => {
    console.log("File URL:", data.message.file_url);
});
```

### Python File Upload

```python
import requests

files = {"file": open("report.pdf", "rb")}
data = {
    "doctype": "Fitting Session",
    "docname": "FS-00001",
    "fieldname": "attachment",
    "is_private": 1
}

response = session.post(
    "https://flow.local/api/method/upload_file",
    files=files,
    data=data
)
file_url = response.json()["message"]["file_url"]
```

---

## Error Responses

### Standard Error Format

```json
{
    "exc_type": "ValidationError",
    "exception": "frappe.exceptions.ValidationError: Customer is required",
    "_server_messages": "[{\"message\": \"Customer is required\", \"indicator\": \"red\"}]",
    "exc": "Traceback (most recent call last):\n  ..."
}
```

### Common HTTP Status Codes

| Status | Frappe Exception | When |
|--------|------------------|------|
| `200` | -- | Success |
| `400` | `ValidationError` | Invalid data / business rule violation |
| `403` | `PermissionError` | User lacks permission |
| `404` | `DoesNotExistError` | Document not found |
| `409` | `DuplicateEntryError` | Unique constraint violation |
| `417` | `ValidationError` | frappe.throw() called |
| `500` | `Exception` | Unhandled server error |
| `501` | `MethodNotAllowedError` | Whitelisted method doesn't allow this HTTP method |

### Raising API Errors

```python
@frappe.whitelist()
def validate_and_process(session_name):
    if not frappe.db.exists("Fitting Session", session_name):
        frappe.throw(
            _("Fitting Session {0} not found").format(session_name),
            frappe.DoesNotExistError
        )

    session = frappe.get_doc("Fitting Session", session_name)

    if session.workflow_state == "Cancelled":
        frappe.throw(
            _("Cannot process cancelled session"),
            frappe.ValidationError
        )

    if not frappe.has_permission("Fitting Session", "write", doc=session.name):
        frappe.throw(
            _("You do not have permission to process this session"),
            frappe.PermissionError
        )

    # Process...
    return {"status": "processed"}
```

---

## Rate Limiting and Security

### CSRF Protection

All POST/PUT/DELETE requests from browser require CSRF token:

```javascript
// Automatically included by frappe.call()
// For manual fetch:
headers: {
    "X-Frappe-CSRF-Token": frappe.csrf_token
}
```

API key/token auth requests are exempt from CSRF.

### Rate Limiting (v15+)

```python
# In site_config.json
{
    "rate_limit": {
        "limit": 100,         # requests
        "window": 60          # seconds
    }
}
```

### Protecting Sensitive Endpoints

```python
@frappe.whitelist()
def sensitive_operation(session_name):
    # Always verify permissions explicitly
    frappe.only_for(["Fitting Manager", "System Manager"])

    # Or check specific permission
    if not frappe.has_permission("Fitting Session", "write"):
        frappe.throw(_("Insufficient permissions"), frappe.PermissionError)

    # Proceed with operation...
```

---

## Response Formatting

### Standard Response Structure

```python
@frappe.whitelist()
def get_data():
    # Return value is wrapped in {"message": <return_value>}
    return {"items": [...], "total": 42}
    # Client receives: {"message": {"items": [...], "total": 42}}
```

### Frappe Response Flags

```python
@frappe.whitelist()
def custom_response():
    # Set HTTP status
    frappe.response["http_status_code"] = 201

    # Add custom headers
    frappe.response["headers"] = {"X-Custom-Header": "value"}

    # Return data
    return {"created": True}
```

### Streaming Response (Large Files)

```python
@frappe.whitelist()
def download_report(session_name):
    """Generate and return a file download."""
    content = generate_pdf_report(session_name)

    frappe.response["filename"] = f"fitting_report_{session_name}.pdf"
    frappe.response["filecontent"] = content
    frappe.response["type"] = "download"
```

---

## Practical Patterns

### Pagination Helper

```python
@frappe.whitelist()
def get_fittings_paginated(page=1, page_size=20, filters=None):
    """Paginated fitting list with total count."""
    import json

    page = int(page)
    page_size = int(page_size)
    if isinstance(filters, str):
        filters = json.loads(filters)

    total = frappe.db.count("Fitting Session", filters or {})

    data = frappe.get_all(
        "Fitting Session",
        filters=filters or {},
        fields=["name", "customer", "fitting_date", "workflow_state"],
        order_by="fitting_date desc",
        limit_start=(page - 1) * page_size,
        limit_page_length=page_size
    )

    return {
        "data": data,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": -(-total // page_size)  # Ceiling division
    }
```

### Batch API Pattern

```python
@frappe.whitelist()
def batch_get(doctype, names):
    """Get multiple documents in a single request."""
    import json

    if isinstance(names, str):
        names = json.loads(names)

    results = []
    for name in names:
        if frappe.has_permission(doctype, "read", name):
            doc = frappe.get_doc(doctype, name)
            results.append(doc.as_dict())

    return results
```
