# How To: Email Service Integration

**Difficulty**: Intermediate
**Estimated Time**: 30 minutes
**Tags**: email, sendgrid, mailgun, ses, transactional

## Overview

Learn how to integrate external email services (SendGrid, Mailgun, Amazon SES) with Frappe for reliable transactional email delivery.

## Prerequisites

- Email service provider account
- API credentials
- Understanding of email authentication (SPF, DKIM)

## Step-by-Step Guide

### Step 1: Email Service Base Class

```python
import frappe
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class EmailService(ABC):
    """Abstract base class for email service integrations."""

    @abstractmethod
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_email: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[Dict] = None,
        reply_to: str = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Send an email."""
        pass

    @abstractmethod
    def send_template_email(
        self,
        to: List[str],
        template_id: str,
        template_data: Dict[str, Any],
        from_email: str = None
    ) -> Dict[str, Any]:
        """Send email using a template."""
        pass

    def log_email(
        self,
        service: str,
        to: List[str],
        subject: str,
        status: str,
        message_id: str = None,
        error: str = None
    ):
        """Log email for tracking."""
        log = frappe.new_doc("Email Log")  # Custom DocType
        log.service = service
        log.recipients = ", ".join(to)
        log.subject = subject
        log.status = status
        log.message_id = message_id
        log.error = error
        log.insert(ignore_permissions=True)
        frappe.db.commit()
```

### Step 2: SendGrid Integration

```python
import frappe
import requests
from typing import Dict, Any, List

class SendGridService(EmailService):
    """SendGrid email service integration."""

    def __init__(self):
        settings = frappe.get_single("SendGrid Settings")
        self.api_key = settings.get_password("api_key")
        self.default_from = settings.default_from_email
        self.api_url = "https://api.sendgrid.com/v3"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_email: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[Dict] = None,
        reply_to: str = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Send email via SendGrid."""

        from_email = from_email or self.default_from

        # Build personalizations
        personalizations = [{
            "to": [{"email": email} for email in to]
        }]

        if cc:
            personalizations[0]["cc"] = [{"email": email} for email in cc]
        if bcc:
            personalizations[0]["bcc"] = [{"email": email} for email in bcc]

        # Build request data
        data = {
            "personalizations": personalizations,
            "from": {"email": from_email},
            "subject": subject,
            "content": [
                {"type": "text/html", "value": body}
            ]
        }

        if reply_to:
            data["reply_to"] = {"email": reply_to}

        if headers:
            data["headers"] = headers

        # Handle attachments
        if attachments:
            data["attachments"] = []
            for att in attachments:
                import base64
                data["attachments"].append({
                    "content": base64.b64encode(att["content"]).decode(),
                    "filename": att["filename"],
                    "type": att.get("content_type", "application/octet-stream"),
                    "disposition": "attachment"
                })

        try:
            response = requests.post(
                f"{self.api_url}/mail/send",
                headers=self._get_headers(),
                json=data,
                timeout=30
            )

            if response.status_code in [200, 202]:
                message_id = response.headers.get("X-Message-Id")
                self.log_email("SendGrid", to, subject, "Sent", message_id)
                return {
                    "success": True,
                    "message_id": message_id
                }
            else:
                error = response.text
                self.log_email("SendGrid", to, subject, "Failed", error=error)
                return {
                    "success": False,
                    "error": error
                }

        except Exception as e:
            self.log_email("SendGrid", to, subject, "Failed", error=str(e))
            return {"success": False, "error": str(e)}

    def send_template_email(
        self,
        to: List[str],
        template_id: str,
        template_data: Dict[str, Any],
        from_email: str = None
    ) -> Dict[str, Any]:
        """Send email using SendGrid dynamic template."""

        from_email = from_email or self.default_from

        data = {
            "personalizations": [{
                "to": [{"email": email} for email in to],
                "dynamic_template_data": template_data
            }],
            "from": {"email": from_email},
            "template_id": template_id
        }

        try:
            response = requests.post(
                f"{self.api_url}/mail/send",
                headers=self._get_headers(),
                json=data,
                timeout=30
            )

            if response.status_code in [200, 202]:
                return {"success": True}
            else:
                return {"success": False, "error": response.text}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_email_stats(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get email statistics from SendGrid."""

        try:
            response = requests.get(
                f"{self.api_url}/stats",
                headers=self._get_headers(),
                params={
                    "start_date": start_date,
                    "end_date": end_date
                },
                timeout=30
            )

            if response.status_code == 200:
                return {"success": True, "stats": response.json()}
            else:
                return {"success": False, "error": response.text}

        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Step 3: Mailgun Integration

```python
import frappe
import requests
from typing import Dict, Any, List

class MailgunService(EmailService):
    """Mailgun email service integration."""

    def __init__(self):
        settings = frappe.get_single("Mailgun Settings")
        self.api_key = settings.get_password("api_key")
        self.domain = settings.domain
        self.default_from = settings.default_from_email
        self.region = settings.region or "us"  # "us" or "eu"

        if self.region == "eu":
            self.api_url = f"https://api.eu.mailgun.net/v3/{self.domain}"
        else:
            self.api_url = f"https://api.mailgun.net/v3/{self.domain}"

    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_email: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[Dict] = None,
        reply_to: str = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Send email via Mailgun."""

        from_email = from_email or self.default_from

        data = {
            "from": from_email,
            "to": to,
            "subject": subject,
            "html": body
        }

        if cc:
            data["cc"] = cc
        if bcc:
            data["bcc"] = bcc
        if reply_to:
            data["h:Reply-To"] = reply_to

        # Add custom headers
        if headers:
            for key, value in headers.items():
                data[f"h:{key}"] = value

        # Handle attachments
        files = []
        if attachments:
            for att in attachments:
                files.append(
                    ("attachment", (att["filename"], att["content"], att.get("content_type")))
                )

        try:
            response = requests.post(
                f"{self.api_url}/messages",
                auth=("api", self.api_key),
                data=data,
                files=files if files else None,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                message_id = result.get("id")
                self.log_email("Mailgun", to, subject, "Sent", message_id)
                return {
                    "success": True,
                    "message_id": message_id
                }
            else:
                error = response.text
                self.log_email("Mailgun", to, subject, "Failed", error=error)
                return {"success": False, "error": error}

        except Exception as e:
            self.log_email("Mailgun", to, subject, "Failed", error=str(e))
            return {"success": False, "error": str(e)}

    def send_template_email(
        self,
        to: List[str],
        template_id: str,
        template_data: Dict[str, Any],
        from_email: str = None
    ) -> Dict[str, Any]:
        """Send email using Mailgun template."""

        from_email = from_email or self.default_from

        data = {
            "from": from_email,
            "to": to,
            "template": template_id,
            "h:X-Mailgun-Variables": frappe.as_json(template_data)
        }

        try:
            response = requests.post(
                f"{self.api_url}/messages",
                auth=("api", self.api_key),
                data=data,
                timeout=30
            )

            if response.status_code == 200:
                return {"success": True}
            else:
                return {"success": False, "error": response.text}

        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Step 4: Amazon SES Integration

```python
import frappe
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any, List

class AmazonSESService(EmailService):
    """Amazon SES email service integration."""

    def __init__(self):
        settings = frappe.get_single("Amazon SES Settings")
        self.client = boto3.client(
            'ses',
            region_name=settings.region,
            aws_access_key_id=settings.access_key_id,
            aws_secret_access_key=settings.get_password("secret_access_key")
        )
        self.default_from = settings.default_from_email

    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_email: str = None,
        cc: List[str] = None,
        bcc: List[str] = None,
        attachments: List[Dict] = None,
        reply_to: str = None,
        headers: Dict[str, str] = None
    ) -> Dict[str, Any]:
        """Send email via Amazon SES."""

        from_email = from_email or self.default_from

        # Build destination
        destination = {"ToAddresses": to}
        if cc:
            destination["CcAddresses"] = cc
        if bcc:
            destination["BccAddresses"] = bcc

        # If no attachments, use simple email
        if not attachments:
            try:
                response = self.client.send_email(
                    Source=from_email,
                    Destination=destination,
                    Message={
                        "Subject": {"Data": subject, "Charset": "UTF-8"},
                        "Body": {"Html": {"Data": body, "Charset": "UTF-8"}}
                    },
                    ReplyToAddresses=[reply_to] if reply_to else []
                )

                message_id = response.get("MessageId")
                self.log_email("Amazon SES", to, subject, "Sent", message_id)
                return {
                    "success": True,
                    "message_id": message_id
                }

            except ClientError as e:
                error = e.response["Error"]["Message"]
                self.log_email("Amazon SES", to, subject, "Failed", error=error)
                return {"success": False, "error": error}

        # With attachments, use raw email
        else:
            return self._send_raw_email(
                to, subject, body, from_email, cc, bcc, attachments, reply_to
            )

    def _send_raw_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_email: str,
        cc: List[str],
        bcc: List[str],
        attachments: List[Dict],
        reply_to: str
    ) -> Dict[str, Any]:
        """Send raw email with attachments."""

        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = ", ".join(to)

        if cc:
            msg["Cc"] = ", ".join(cc)
        if reply_to:
            msg["Reply-To"] = reply_to

        # HTML body
        msg_body = MIMEMultipart("alternative")
        html_part = MIMEText(body, "html", "utf-8")
        msg_body.attach(html_part)
        msg.attach(msg_body)

        # Attachments
        for att in attachments:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(att["content"])
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={att['filename']}"
            )
            msg.attach(part)

        try:
            destinations = to + (cc or []) + (bcc or [])
            response = self.client.send_raw_email(
                Source=from_email,
                Destinations=destinations,
                RawMessage={"Data": msg.as_string()}
            )

            message_id = response.get("MessageId")
            self.log_email("Amazon SES", to, subject, "Sent", message_id)
            return {"success": True, "message_id": message_id}

        except ClientError as e:
            error = e.response["Error"]["Message"]
            self.log_email("Amazon SES", to, subject, "Failed", error=error)
            return {"success": False, "error": error}

    def send_template_email(
        self,
        to: List[str],
        template_id: str,
        template_data: Dict[str, Any],
        from_email: str = None
    ) -> Dict[str, Any]:
        """Send email using SES template."""

        from_email = from_email or self.default_from

        try:
            response = self.client.send_templated_email(
                Source=from_email,
                Destination={"ToAddresses": to},
                Template=template_id,
                TemplateData=frappe.as_json(template_data)
            )

            return {"success": True, "message_id": response.get("MessageId")}

        except ClientError as e:
            return {"success": False, "error": e.response["Error"]["Message"]}
```

### Step 5: Email Manager

```python
import frappe
from typing import Dict, Any, List

class EmailManager:
    """Unified email manager supporting multiple services."""

    SERVICES = {
        "sendgrid": SendGridService,
        "mailgun": MailgunService,
        "ses": AmazonSESService
    }

    @classmethod
    def get_service(cls, service_name: str = None) -> EmailService:
        """Get email service instance."""
        if not service_name:
            # Get default from settings
            service_name = frappe.db.get_single_value("Email Settings", "default_email_service")

        service_class = cls.SERVICES.get(service_name.lower())
        if not service_class:
            frappe.throw(f"Unknown email service: {service_name}")

        return service_class()

    @classmethod
    def send(
        cls,
        to: List[str],
        subject: str,
        body: str,
        service: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send email through specified or default service."""

        email_service = cls.get_service(service)
        return email_service.send_email(to, subject, body, **kwargs)

    @classmethod
    def send_template(
        cls,
        to: List[str],
        template_id: str,
        template_data: Dict[str, Any],
        service: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send template email."""

        email_service = cls.get_service(service)
        return email_service.send_template_email(to, template_id, template_data, **kwargs)

# API Endpoints
@frappe.whitelist()
def send_email(to: str, subject: str, body: str, service: str = None):
    """Send email API endpoint."""
    recipients = [email.strip() for email in to.split(",")]
    return EmailManager.send(recipients, subject, body, service=service)

@frappe.whitelist()
def send_notification_email(doctype: str, docname: str, template: str):
    """Send notification email for a document."""
    doc = frappe.get_doc(doctype, docname)

    # Get email template
    email_template = frappe.get_doc("Email Template", template)
    subject = frappe.render_template(email_template.subject, {"doc": doc})
    body = frappe.render_template(email_template.response, {"doc": doc})

    # Get recipients based on doctype
    recipients = get_notification_recipients(doc)

    return EmailManager.send(recipients, subject, body)
```

## Usage Examples

```python
# Send simple email
result = EmailManager.send(
    to=["customer@example.com"],
    subject="Order Confirmation",
    body="<h1>Thank you for your order!</h1>"
)

# Send with attachments
with open("invoice.pdf", "rb") as f:
    pdf_content = f.read()

result = EmailManager.send(
    to=["customer@example.com"],
    subject="Your Invoice",
    body="Please find your invoice attached.",
    attachments=[{
        "filename": "invoice.pdf",
        "content": pdf_content,
        "content_type": "application/pdf"
    }]
)

# Send template email (SendGrid)
result = EmailManager.send_template(
    to=["customer@example.com"],
    template_id="d-xxxxxxxxxxxxx",
    template_data={
        "customer_name": "John Doe",
        "order_id": "ORD-001",
        "total": "$99.99"
    },
    service="sendgrid"
)
```

## Troubleshooting

### Emails Not Delivered
- Check SPF/DKIM configuration
- Verify sender domain is authenticated
- Review bounce/complaint reports

### Rate Limiting
- Implement queuing for bulk emails
- Use warmup strategy for new domains
- Monitor sending reputation

## Next Steps

- [SMS Service Integration](../sms-service-integration/sms-service-integration.md)
- [Webhook Event Handling](../webhook-event-handling/webhook-event-handling.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
