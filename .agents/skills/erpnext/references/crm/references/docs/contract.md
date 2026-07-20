# Contract DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/contract

## Overview

Contract manages agreements with Customers, Suppliers, or Employees. It supports digital signatures, fulfilment tracking, and links to related documents like Quotations, Sales Orders, etc.

## Field Reference

### Party Information

| Field | Type | Description |
|-------|------|-------------|
| `party_type` | Select | Customer, Supplier, Employee |
| `party_name` | Dynamic Link | Party reference |
| `party_user` | Link (User) | Party's user account |
| `party_full_name` | Data | Full name for display |

### Contract Status

| Field | Type | Description |
|-------|------|-------------|
| `status` | Select | Unsigned, Active, Inactive, Cancelled |
| `is_signed` | Check | Whether contract is signed |
| `fulfilment_status` | Select | N/A, Unfulfilled, Partially Fulfilled, Fulfilled, Lapsed |

### Contract Period

| Field | Type | Description |
|-------|------|-------------|
| `start_date` | Date | Contract start |
| `end_date` | Date | Contract end |

### Signature Details

| Field | Type | Description |
|-------|------|-------------|
| `signee` | Data | Name of person who signed |
| `signed_on` | Datetime | Signature timestamp |
| `ip_address` | Data | IP address at signing |
| `signee_company` | Signature | Company representative signature |
| `signed_by_company` | Link (User) | Who signed for company |

### Contract Content

| Field | Type | Description |
|-------|------|-------------|
| `contract_template` | Link | Contract Template |
| `contract_terms` | Text Editor | Full contract terms |

### Fulfilment

| Field | Type | Description |
|-------|------|-------------|
| `requires_fulfilment` | Check | Whether fulfilment tracking needed |
| `fulfilment_deadline` | Date | Deadline for fulfilment |
| `fulfilment_terms` | Table | Checklist items |

### Document References

| Field | Type | Description |
|-------|------|-------------|
| `document_type` | Select | Quotation, Project, Sales Order, Purchase Order, Sales Invoice, Purchase Invoice |
| `document_name` | Dynamic Link | Reference document |

## Status Values

```python
status: Literal[
    "Unsigned",   # Not yet signed
    "Active",     # Currently active
    "Inactive",   # Expired or paused
    "Cancelled"   # Terminated
]

fulfilment_status: Literal[
    "N/A",                # No fulfilment required
    "Unfulfilled",        # Not yet fulfilled
    "Partially Fulfilled", # Some items fulfilled
    "Fulfilled",          # All items fulfilled
    "Lapsed"              # Deadline passed unfulfilled
]
```

## API Reference

### Create Contract

```python
contract = frappe.new_doc("Contract")
contract.party_type = "Customer"
contract.party_name = "CUST-00001"
contract.start_date = "2026-01-01"
contract.end_date = "2026-12-31"
contract.contract_terms = """
<h3>Service Agreement</h3>
<p>Terms and conditions...</p>
"""
contract.insert()
```

### Create Contract from Template

```python
# First, create a Contract Template
template = frappe.new_doc("Contract Template")
template.title = "Standard Service Agreement"
template.contract_terms = """
<h3>Service Agreement</h3>
<p>This agreement is between {party_name} and {company}...</p>
"""
template.insert()

# Then use in contract
contract = frappe.new_doc("Contract")
contract.party_type = "Customer"
contract.party_name = "CUST-00001"
contract.contract_template = "Standard Service Agreement"
# Terms are auto-populated from template
contract.insert()
```

### Create Contract with Fulfilment

```python
contract = frappe.new_doc("Contract")
contract.party_type = "Customer"
contract.party_name = "CUST-00001"
contract.start_date = "2026-01-01"
contract.end_date = "2026-12-31"
contract.requires_fulfilment = 1
contract.fulfilment_deadline = "2026-06-30"

# Add fulfilment checklist
contract.append("fulfilment_terms", {
    "requirement": "Deliver initial batch",
    "fulfilled": 0
})
contract.append("fulfilment_terms", {
    "requirement": "Complete training",
    "fulfilled": 0
})
contract.append("fulfilment_terms", {
    "requirement": "Sign-off on acceptance",
    "fulfilled": 0
})

contract.insert()
```

### Link Contract to Sales Order

```python
contract = frappe.new_doc("Contract")
contract.party_type = "Customer"
contract.party_name = "CUST-00001"
contract.document_type = "Sales Order"
contract.document_name = "SAL-ORD-2026-00001"
contract.start_date = "2026-01-01"
contract.end_date = "2026-12-31"
contract.insert()
```

### Record Signature

```python
contract = frappe.get_doc("Contract", "CTR-00001")
contract.is_signed = 1
contract.signee = "John Doe"
contract.signed_on = frappe.utils.now_datetime()
contract.ip_address = frappe.local.request_ip
contract.save()
```

### Update Fulfilment Status

```python
contract = frappe.get_doc("Contract", "CTR-00001")

# Mark item as fulfilled
for item in contract.fulfilment_terms:
    if item.requirement == "Deliver initial batch":
        item.fulfilled = 1

contract.save()
# fulfilment_status is auto-calculated based on fulfilled items
```

### Get Active Contracts for Customer

```python
contracts = frappe.get_all(
    "Contract",
    filters={
        "party_type": "Customer",
        "party_name": "CUST-00001",
        "status": "Active"
    },
    fields=["name", "start_date", "end_date", "fulfilment_status"]
)
```

### Check Expiring Contracts

```python
from frappe.utils import add_days, today

# Contracts expiring in next 30 days
expiring = frappe.get_all(
    "Contract",
    filters={
        "status": "Active",
        "end_date": ["between", [today(), add_days(today(), 30)]]
    },
    fields=["name", "party_name", "end_date"]
)
```

## Contract Fulfilment Checklist (Child Table)

| Field | Type | Description |
|-------|------|-------------|
| `requirement` | Data | Fulfilment requirement |
| `notes` | Small Text | Additional notes |
| `fulfilled` | Check | Whether fulfilled |

## Contract Template

Pre-defined templates for common contract types:

```python
template = frappe.new_doc("Contract Template")
template.title = "Annual Service Agreement"
template.contract_terms = """
<h2>Service Agreement</h2>

<p>This Service Agreement ("Agreement") is entered into as of {start_date}
between {company} ("Provider") and {party_name} ("Client").</p>

<h3>1. Services</h3>
<p>Provider agrees to provide the following services...</p>

<h3>2. Term</h3>
<p>This Agreement shall commence on {start_date} and continue until {end_date}.</p>

<h3>3. Payment</h3>
<p>Client agrees to pay Provider...</p>
"""
template.insert()
```

## Jinja Variables in Templates

Available variables in contract templates:
- `{party_name}` - Customer/Supplier name
- `{party_full_name}` - Full name
- `{company}` - Your company name
- `{start_date}` - Contract start
- `{end_date}` - Contract end
- Any custom field on Contract

## Related DocTypes

- **Contract Template** - Reusable contract templates
- **Contract Fulfilment Checklist** - Fulfilment items
- **Customer** - Customer contracts
- **Supplier** - Supplier contracts
- **Employee** - Employment contracts
- **Quotation/Sales Order** - Linked documents
