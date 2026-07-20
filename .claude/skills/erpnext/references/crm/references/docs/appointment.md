# Appointment DocType Reference

> Source: https://github.com/frappe/erpnext/tree/develop/erpnext/crm/doctype/appointment

## Overview

Appointment manages scheduled meetings with customers or leads. It integrates with the Calendar for visual scheduling and can be linked to various party types.

## Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `scheduled_time` | Datetime | **Required** - Appointment date/time |
| `status` | Select | Open, Unverified, Closed |
| `customer_name` | Data | **Required** - Contact name |
| `customer_phone_number` | Data | Phone number |
| `customer_skype` | Data | Skype ID |
| `customer_email` | Data | **Required** - Email address |
| `customer_details` | Long Text | Additional details |
| `appointment_with` | Link (DocType) | Lead, Customer, etc. |
| `party` | Dynamic Link | Party reference |
| `calendar_event` | Link (Event) | Linked calendar event |

## Naming

Auto-name format: `APMT-{customer_name}-{####}`

## Status Values

```python
status: Literal[
    "Open",       # Scheduled, not yet occurred
    "Unverified", # Pending verification
    "Closed"      # Completed or cancelled
]
```

## API Reference

### Create Appointment

```python
appointment = frappe.new_doc("Appointment")
appointment.scheduled_time = "2026-02-15 10:00:00"
appointment.customer_name = "John Doe"
appointment.customer_email = "john@example.com"
appointment.customer_phone_number = "0901234567"
appointment.customer_details = "Discuss golf equipment fitting"
appointment.status = "Open"
appointment.insert()
```

### Create Appointment Linked to Lead

```python
appointment = frappe.new_doc("Appointment")
appointment.scheduled_time = "2026-02-15 14:00:00"
appointment.customer_name = "Jane Smith"
appointment.customer_email = "jane@abc.com"
appointment.customer_phone_number = "0912345678"
appointment.appointment_with = "Lead"
appointment.party = "LEAD-00001"
appointment.status = "Open"
appointment.insert()
```

### Create Appointment Linked to Customer

```python
appointment = frappe.new_doc("Appointment")
appointment.scheduled_time = "2026-02-16 09:00:00"
appointment.customer_name = "ABC Corporation"
appointment.customer_email = "contact@abc.com"
appointment.appointment_with = "Customer"
appointment.party = "CUST-00001"
appointment.customer_details = "Annual contract review meeting"
appointment.status = "Open"
appointment.insert()
```

### Get Today's Appointments

```python
from frappe.utils import today, add_days

appointments = frappe.get_all(
    "Appointment",
    filters={
        "scheduled_time": ["between", [today(), add_days(today(), 1)]],
        "status": "Open"
    },
    fields=["name", "customer_name", "scheduled_time", "customer_email"]
)
```

### Get Appointments for Lead/Customer

```python
# For Lead
lead_appointments = frappe.get_all(
    "Appointment",
    filters={
        "appointment_with": "Lead",
        "party": "LEAD-00001"
    },
    fields=["name", "scheduled_time", "status"]
)

# For Customer
customer_appointments = frappe.get_all(
    "Appointment",
    filters={
        "appointment_with": "Customer",
        "party": "CUST-00001"
    },
    fields=["name", "scheduled_time", "status"]
)
```

### Close Appointment

```python
appointment = frappe.get_doc("Appointment", "APMT-John Doe-0001")
appointment.status = "Closed"
appointment.save()
```

### Reschedule Appointment

```python
appointment = frappe.get_doc("Appointment", "APMT-John Doe-0001")
appointment.scheduled_time = "2026-02-20 15:00:00"
appointment.save()
# Calendar event will be updated automatically if linked
```

## Calendar Integration

Appointments can create calendar events automatically:

```python
# Create appointment with calendar event
appointment = frappe.new_doc("Appointment")
appointment.scheduled_time = "2026-02-15 10:00:00"
appointment.customer_name = "John Doe"
appointment.customer_email = "john@example.com"
appointment.insert()

# Create linked calendar event
event = frappe.new_doc("Event")
event.subject = f"Appointment with {appointment.customer_name}"
event.starts_on = appointment.scheduled_time
event.event_type = "Private"
event.insert()

# Link to appointment
appointment.calendar_event = event.name
appointment.save()
```

## Appointment Booking (Web Form)

ERPNext supports public appointment booking via Web Forms:

```python
# Check if appointment booking is enabled
from erpnext.crm.doctype.appointment_booking_settings.appointment_booking_settings import (
    get_appointment_settings
)

settings = get_appointment_settings()
```

## Workflow Example

```
Customer Request → Unverified Appointment
                        │
                        ▼
              Verify Details (call/email)
                        │
                        ▼
              Open Appointment (confirmed)
                        │
                        ▼
              Meeting Occurs
                        │
                        ▼
              Closed Appointment
                        │
                        ▼
        Create Follow-up (Lead/Opportunity)
```

## Related DocTypes

- **Event** - Calendar events
- **Appointment Booking Settings** - Booking configuration
- **Lead** - Link to lead
- **Customer** - Link to customer
