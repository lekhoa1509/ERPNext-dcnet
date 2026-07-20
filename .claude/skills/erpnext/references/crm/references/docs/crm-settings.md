# CRM Settings Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/crm_settings

## Overview

CRM Settings is a Single DocType that controls global CRM behavior including lead duplicate handling, opportunity auto-close, quotation defaults, and communication settings.

## Field Reference

### Campaign Section

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `campaign_naming_by` | Select | Campaign Name / Naming Series | Campaign Name |

### Lead Section

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `allow_lead_duplication_based_on_emails` | Check | Allow duplicate email leads | 0 |
| `auto_creation_of_contact` | Check | Auto-create contact on conversion | 0 |

### Opportunity Section

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `close_opportunity_after_days` | Int | Auto-close replied opportunities after N days | 15 |

### Quotation Section

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `default_valid_till` | Data | Default quotation validity (days) | - |

### Activity Section

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `carry_forward_communication_and_comments` | Check | Copy comments/emails to new docs | 0 |
| `update_timestamp_on_new_communication` | Check | Update modified timestamp on new comm | 0 |

## API Reference

### Get CRM Settings

```python
# Get single value
allow_duplicates = frappe.db.get_single_value(
    "CRM Settings",
    "allow_lead_duplication_based_on_emails"
)

# Get multiple values
settings = frappe.get_cached_doc("CRM Settings")
close_after = settings.close_opportunity_after_days
auto_contact = settings.auto_creation_of_contact
```

### Update CRM Settings

```python
settings = frappe.get_doc("CRM Settings")
settings.close_opportunity_after_days = 30
settings.allow_lead_duplication_based_on_emails = 1
settings.save()
```

## Settings Explained

### 1. Campaign Naming By

Controls how Campaign documents are named:

```python
# "Campaign Name" - Uses campaign_name as document name
# "Naming Series" - Uses SAL-CAM-.YYYY.-
```

### 2. Allow Lead Duplication Based on Emails

When **disabled** (default):
```python
# This will fail if email already exists
lead = frappe.new_doc("Lead")
lead.email_id = "existing@email.com"  # Error: duplicate
lead.insert()
```

When **enabled**:
```python
# Multiple leads with same email allowed
lead = frappe.new_doc("Lead")
lead.email_id = "existing@email.com"  # OK
lead.insert()
```

### 3. Auto Creation of Contact

When **enabled**:
- Converting Lead to Customer auto-creates Contact
- Links contact to customer

```python
from erpnext.crm.doctype.lead.lead import make_customer

customer = make_customer("LEAD-00001")
customer.insert()
# Contact is auto-created with lead's contact info
```

### 4. Close Opportunity After Days

Scheduler job auto-closes "Replied" opportunities:

```python
# Runs daily via scheduler
from erpnext.crm.doctype.opportunity.opportunity import auto_close_opportunity

# Closes opportunities where:
# - status == "Replied"
# - days since modified > close_opportunity_after_days
```

### 5. Default Valid Till

Sets default quotation validity:

```python
# In Quotation creation
from frappe.utils import add_days, today

valid_till = frappe.db.get_single_value("CRM Settings", "default_valid_till")
if valid_till:
    quotation.valid_till = add_days(today(), int(valid_till))
```

### 6. Carry Forward Communication

When **enabled**:
- Converting Lead to Opportunity copies all Communication docs
- Converting Lead to Customer copies all Communication docs

```python
# In conversion process
if frappe.db.get_single_value("CRM Settings", "carry_forward_communication_and_comments"):
    # Copy communications from source to target
    communications = frappe.get_all(
        "Communication",
        filters={"reference_doctype": "Lead", "reference_name": lead.name}
    )
    for comm in communications:
        # Link to new document
        ...
```

### 7. Update Timestamp on New Communication

When **enabled**:
- New email/communication updates Lead/Opportunity `modified` timestamp
- Helps with activity tracking and sorting by recent activity

## Recommended Settings for DCNET

```python
# Golf business CRM settings
settings = frappe.get_doc("CRM Settings")

# Allow sales team flexibility with leads
settings.allow_lead_duplication_based_on_emails = 0  # Prevent duplicates

# Auto-create contacts for better relationship tracking
settings.auto_creation_of_contact = 1

# Give sales team time to follow up
settings.close_opportunity_after_days = 30

# Standard quotation validity
settings.default_valid_till = "30"

# Keep communication history
settings.carry_forward_communication_and_comments = 1

# Track activity timestamps
settings.update_timestamp_on_new_communication = 1

settings.save()
```

## Related DocTypes

- **Lead** - Affected by duplicate settings
- **Opportunity** - Affected by auto-close
- **Quotation** - Affected by validity settings
- **Campaign** - Affected by naming settings
- **Customer** - Contact auto-creation
