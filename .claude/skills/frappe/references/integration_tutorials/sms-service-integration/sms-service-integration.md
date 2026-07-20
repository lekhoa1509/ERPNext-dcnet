# How To: SMS Service Integration

**Difficulty**: Intermediate
**Estimated Time**: 25 minutes
**Tags**: sms, twilio, nexmo, messaging, notifications

## Overview

Learn how to integrate SMS services (Twilio, Vonage/Nexmo, Plivo) with Frappe for sending transactional SMS messages and notifications.

## Prerequisites

- SMS provider account
- API credentials
- Verified phone number(s)

## Step-by-Step Guide

### Step 1: SMS Service Base Class

```python
import frappe
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class SMSService(ABC):
    """Abstract base class for SMS service integrations."""

    @abstractmethod
    def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send an SMS message."""
        pass

    @abstractmethod
    def check_balance(self) -> Dict[str, Any]:
        """Check account balance."""
        pass

    def log_sms(
        self,
        service: str,
        to: str,
        message: str,
        status: str,
        message_id: str = None,
        cost: float = None,
        error: str = None
    ):
        """Log SMS for tracking."""
        log = frappe.new_doc("SMS Log")  # Custom DocType
        log.service = service
        log.recipient = to
        log.message = message[:500]  # Truncate for storage
        log.status = status
        log.message_id = message_id
        log.cost = cost
        log.error = error
        log.insert(ignore_permissions=True)
        frappe.db.commit()

    def format_phone_number(self, phone: str, country_code: str = None) -> str:
        """Format phone number to E.164 format."""
        import re

        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)

        # Add country code if not present
        if not digits.startswith('+'):
            if country_code:
                country_code = country_code.lstrip('+')
                if not digits.startswith(country_code):
                    digits = country_code + digits
            digits = '+' + digits

        return digits
```

### Step 2: Twilio Integration

```python
import frappe
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from typing import Dict, Any

class TwilioService(SMSService):
    """Twilio SMS service integration."""

    def __init__(self):
        settings = frappe.get_single("Twilio Settings")
        self.account_sid = settings.account_sid
        self.auth_token = settings.get_password("auth_token")
        self.default_from = settings.default_from_number
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS via Twilio."""

        from_number = from_number or self.default_from
        to = self.format_phone_number(to)

        try:
            twilio_message = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to
            )

            self.log_sms(
                service="Twilio",
                to=to,
                message=message,
                status="Sent",
                message_id=twilio_message.sid,
                cost=float(twilio_message.price) if twilio_message.price else None
            )

            return {
                "success": True,
                "message_id": twilio_message.sid,
                "status": twilio_message.status
            }

        except TwilioRestException as e:
            self.log_sms(
                service="Twilio",
                to=to,
                message=message,
                status="Failed",
                error=str(e)
            )
            return {
                "success": False,
                "error": str(e),
                "code": e.code
            }

    def send_bulk_sms(
        self,
        recipients: list,
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS to multiple recipients."""

        from_number = from_number or self.default_from
        results = {"sent": 0, "failed": 0, "errors": []}

        for phone in recipients:
            result = self.send_sms(phone, message, from_number)
            if result["success"]:
                results["sent"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({
                    "phone": phone,
                    "error": result["error"]
                })

        return results

    def check_balance(self) -> Dict[str, Any]:
        """Check Twilio account balance."""

        try:
            balance = self.client.api.v2010.accounts(self.account_sid).balance.fetch()
            return {
                "success": True,
                "balance": balance.balance,
                "currency": balance.currency
            }
        except TwilioRestException as e:
            return {"success": False, "error": str(e)}

    def get_message_status(self, message_id: str) -> Dict[str, Any]:
        """Get status of a sent message."""

        try:
            message = self.client.messages(message_id).fetch()
            return {
                "success": True,
                "status": message.status,
                "date_sent": str(message.date_sent),
                "error_code": message.error_code,
                "error_message": message.error_message
            }
        except TwilioRestException as e:
            return {"success": False, "error": str(e)}

    def setup_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Configure webhook for status callbacks."""

        # This would typically be done in Twilio console
        # or via API for each message
        return {
            "message": "Configure status callback URL in Twilio console or pass as parameter when sending"
        }
```

### Step 3: Vonage (Nexmo) Integration

```python
import frappe
import vonage
from typing import Dict, Any

class VonageService(SMSService):
    """Vonage/Nexmo SMS service integration."""

    def __init__(self):
        settings = frappe.get_single("Vonage Settings")
        self.api_key = settings.api_key
        self.api_secret = settings.get_password("api_secret")
        self.default_from = settings.default_from_name
        self.client = vonage.Client(key=self.api_key, secret=self.api_secret)
        self.sms = vonage.Sms(self.client)

    def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS via Vonage."""

        from_number = from_number or self.default_from
        to = self.format_phone_number(to).lstrip('+')  # Vonage doesn't want +

        try:
            response = self.sms.send_message({
                "from": from_number,
                "to": to,
                "text": message
            })

            message_data = response["messages"][0]

            if message_data["status"] == "0":
                self.log_sms(
                    service="Vonage",
                    to=to,
                    message=message,
                    status="Sent",
                    message_id=message_data.get("message-id"),
                    cost=float(message_data.get("message-price", 0))
                )
                return {
                    "success": True,
                    "message_id": message_data.get("message-id"),
                    "remaining_balance": message_data.get("remaining-balance")
                }
            else:
                error = message_data.get("error-text", "Unknown error")
                self.log_sms(
                    service="Vonage",
                    to=to,
                    message=message,
                    status="Failed",
                    error=error
                )
                return {
                    "success": False,
                    "error": error,
                    "status_code": message_data["status"]
                }

        except Exception as e:
            self.log_sms(
                service="Vonage",
                to=to,
                message=message,
                status="Failed",
                error=str(e)
            )
            return {"success": False, "error": str(e)}

    def check_balance(self) -> Dict[str, Any]:
        """Check Vonage account balance."""

        try:
            response = self.client.account.get_balance()
            return {
                "success": True,
                "balance": response["value"],
                "auto_reload": response.get("autoReload", False)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_template_sms(
        self,
        to: str,
        template_name: str,
        template_data: Dict[str, Any],
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS using template from Frappe."""

        # Get template from Frappe
        template = frappe.get_doc("SMS Template", template_name)
        message = frappe.render_template(template.message, template_data)

        return self.send_sms(to, message, from_number)
```

### Step 4: Plivo Integration

```python
import frappe
import plivo
from typing import Dict, Any, List

class PlivoService(SMSService):
    """Plivo SMS service integration."""

    def __init__(self):
        settings = frappe.get_single("Plivo Settings")
        self.auth_id = settings.auth_id
        self.auth_token = settings.get_password("auth_token")
        self.default_from = settings.default_from_number
        self.client = plivo.RestClient(self.auth_id, self.auth_token)

    def send_sms(
        self,
        to: str,
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS via Plivo."""

        from_number = from_number or self.default_from
        to = self.format_phone_number(to).lstrip('+')

        try:
            response = self.client.messages.create(
                src=from_number,
                dst=to,
                text=message
            )

            self.log_sms(
                service="Plivo",
                to=to,
                message=message,
                status="Sent",
                message_id=response.message_uuid[0]
            )

            return {
                "success": True,
                "message_id": response.message_uuid[0],
                "api_id": response.api_id
            }

        except plivo.exceptions.PlivoRestError as e:
            self.log_sms(
                service="Plivo",
                to=to,
                message=message,
                status="Failed",
                error=str(e)
            )
            return {"success": False, "error": str(e)}

    def send_bulk_sms(
        self,
        recipients: List[str],
        message: str,
        from_number: str = None
    ) -> Dict[str, Any]:
        """Send SMS to multiple recipients (Plivo bulk API)."""

        from_number = from_number or self.default_from
        # Plivo accepts comma-separated numbers
        dst = "<".join([self.format_phone_number(r).lstrip('+') for r in recipients])

        try:
            response = self.client.messages.create(
                src=from_number,
                dst=dst,
                text=message
            )

            return {
                "success": True,
                "message_count": len(response.message_uuid),
                "message_ids": response.message_uuid
            }

        except plivo.exceptions.PlivoRestError as e:
            return {"success": False, "error": str(e)}

    def check_balance(self) -> Dict[str, Any]:
        """Check Plivo account balance."""

        try:
            response = self.client.account.get()
            return {
                "success": True,
                "balance": response.cash_credits,
                "account_type": response.account_type
            }
        except plivo.exceptions.PlivoRestError as e:
            return {"success": False, "error": str(e)}
```

### Step 5: SMS Manager

```python
import frappe
from typing import Dict, Any, List

class SMSManager:
    """Unified SMS manager supporting multiple services."""

    SERVICES = {
        "twilio": TwilioService,
        "vonage": VonageService,
        "plivo": PlivoService
    }

    @classmethod
    def get_service(cls, service_name: str = None) -> SMSService:
        """Get SMS service instance."""
        if not service_name:
            service_name = frappe.db.get_single_value("SMS Settings", "default_sms_service")

        service_class = cls.SERVICES.get(service_name.lower())
        if not service_class:
            frappe.throw(f"Unknown SMS service: {service_name}")

        return service_class()

    @classmethod
    def send(
        cls,
        to: str,
        message: str,
        service: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send SMS through specified or default service."""
        sms_service = cls.get_service(service)
        return sms_service.send_sms(to, message, **kwargs)

    @classmethod
    def send_bulk(
        cls,
        recipients: List[str],
        message: str,
        service: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send SMS to multiple recipients."""
        sms_service = cls.get_service(service)

        if hasattr(sms_service, 'send_bulk_sms'):
            return sms_service.send_bulk_sms(recipients, message, **kwargs)

        # Fallback to individual sends
        results = {"sent": 0, "failed": 0, "errors": []}
        for phone in recipients:
            result = sms_service.send_sms(phone, message, **kwargs)
            if result["success"]:
                results["sent"] += 1
            else:
                results["failed"] += 1
                results["errors"].append({"phone": phone, "error": result["error"]})

        return results

    @classmethod
    def send_template(
        cls,
        to: str,
        template_name: str,
        context: Dict[str, Any],
        service: str = None
    ) -> Dict[str, Any]:
        """Send SMS using a Frappe SMS Template."""
        template = frappe.get_doc("SMS Template", template_name)
        message = frappe.render_template(template.message, context)
        return cls.send(to, message, service)

# API Endpoints
@frappe.whitelist()
def send_sms(to: str, message: str, service: str = None):
    """Send SMS API endpoint."""
    return SMSManager.send(to, message, service)

@frappe.whitelist()
def send_notification_sms(doctype: str, docname: str, template: str, recipient_field: str):
    """Send notification SMS for a document."""
    doc = frappe.get_doc(doctype, docname)
    phone = doc.get(recipient_field)

    if not phone:
        return {"success": False, "error": f"No phone number in field {recipient_field}"}

    return SMSManager.send_template(phone, template, {"doc": doc})
```

## Usage Examples

```python
# Send simple SMS
result = SMSManager.send(
    to="+1234567890",
    message="Your verification code is 123456"
)

# Send using template
result = SMSManager.send_template(
    to="+1234567890",
    template_name="Order Confirmation",
    context={
        "order_id": "ORD-001",
        "delivery_date": "2024-01-15"
    }
)

# Send bulk SMS
result = SMSManager.send_bulk(
    recipients=["+1234567890", "+0987654321"],
    message="Flash sale! 50% off all items today only."
)

# Integration with document events
def after_submit(doc, method):
    """Send SMS notification after Sales Order submission."""
    if doc.customer_mobile:
        SMSManager.send_template(
            to=doc.customer_mobile,
            template_name="Order Submitted",
            context={"doc": doc}
        )
```

## SMS Template DocType

Create a simple SMS Template DocType:

```python
{
    "doctype": "SMS Template",
    "fields": [
        {"fieldname": "template_name", "fieldtype": "Data", "label": "Template Name", "reqd": 1},
        {"fieldname": "message", "fieldtype": "Small Text", "label": "Message", "reqd": 1},
        {"fieldname": "character_count", "fieldtype": "Int", "label": "Character Count", "read_only": 1},
        {"fieldname": "description", "fieldtype": "Text", "label": "Description"}
    ]
}
```

## Troubleshooting

### Message Not Delivered
- Verify phone number format (E.164)
- Check sender ID is approved
- Review carrier filtering rules

### Cost Management
- Set up balance alerts
- Implement rate limiting
- Monitor usage via logs

## Next Steps

- [Email Service Integration](../email-service-integration/email-service-integration.md)
- [Webhook Event Handling](../webhook-event-handling/webhook-event-handling.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
