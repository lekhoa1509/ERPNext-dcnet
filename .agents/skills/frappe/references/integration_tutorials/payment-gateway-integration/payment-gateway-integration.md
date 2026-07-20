# How To: Payment Gateway Integration Patterns

**Difficulty**: Advanced
**Estimated Time**: 40 minutes
**Tags**: payment, gateway, stripe, razorpay, paypal, checkout

## Overview

Learn patterns for integrating payment gateways with Frappe/ERPNext, including checkout flows, webhook handling, and payment reconciliation.

## Prerequisites

- Payment gateway API credentials
- Understanding of payment flows
- ERPNext payment entries

## Step-by-Step Guide

### Step 1: Payment Gateway Base Class

```python
import frappe
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PaymentGateway(ABC):
    """Abstract base class for payment gateway integrations."""

    @abstractmethod
    def create_payment_intent(
        self,
        amount: float,
        currency: str,
        reference: str,
        customer_email: str = None,
        metadata: dict = None
    ) -> Dict[str, Any]:
        """Create a payment intent/order with the gateway."""
        pass

    @abstractmethod
    def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """Verify payment status with the gateway."""
        pass

    @abstractmethod
    def process_webhook(self, payload: dict, signature: str) -> Dict[str, Any]:
        """Process webhook from payment gateway."""
        pass

    @abstractmethod
    def refund_payment(self, payment_id: str, amount: float = None) -> Dict[str, Any]:
        """Refund a payment."""
        pass

    def log_transaction(
        self,
        gateway: str,
        transaction_type: str,
        reference: str,
        status: str,
        amount: float,
        currency: str,
        gateway_response: dict
    ):
        """Log payment transaction for audit."""
        log = frappe.new_doc("Payment Gateway Log")  # Custom DocType
        log.gateway = gateway
        log.transaction_type = transaction_type
        log.reference = reference
        log.status = status
        log.amount = amount
        log.currency = currency
        log.gateway_response = frappe.as_json(gateway_response)
        log.insert(ignore_permissions=True)
        frappe.db.commit()
```

### Step 2: Stripe Integration

```python
import frappe
import stripe
from typing import Dict, Any

class StripeGateway(PaymentGateway):
    """Stripe payment gateway integration."""

    def __init__(self):
        settings = frappe.get_single("Stripe Settings")
        self.secret_key = settings.get_password("secret_key")
        self.publishable_key = settings.publishable_key
        self.webhook_secret = settings.get_password("webhook_secret")
        stripe.api_key = self.secret_key

    def create_payment_intent(
        self,
        amount: float,
        currency: str,
        reference: str,
        customer_email: str = None,
        metadata: dict = None
    ) -> Dict[str, Any]:
        """Create Stripe PaymentIntent."""

        try:
            # Convert to smallest currency unit (cents)
            amount_cents = int(amount * 100)

            intent_data = {
                "amount": amount_cents,
                "currency": currency.lower(),
                "metadata": {
                    "reference": reference,
                    **(metadata or {})
                }
            }

            if customer_email:
                intent_data["receipt_email"] = customer_email

            intent = stripe.PaymentIntent.create(**intent_data)

            self.log_transaction(
                gateway="Stripe",
                transaction_type="Payment Intent Created",
                reference=reference,
                status="Pending",
                amount=amount,
                currency=currency,
                gateway_response={"intent_id": intent.id}
            )

            return {
                "success": True,
                "payment_intent_id": intent.id,
                "client_secret": intent.client_secret,
                "publishable_key": self.publishable_key
            }

        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "code": e.code if hasattr(e, 'code') else None
            }

    def verify_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Verify Stripe payment status."""

        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            return {
                "success": True,
                "status": intent.status,
                "paid": intent.status == "succeeded",
                "amount": intent.amount / 100,
                "currency": intent.currency.upper(),
                "metadata": intent.metadata
            }

        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    def process_webhook(self, payload: str, signature: str) -> Dict[str, Any]:
        """Process Stripe webhook."""

        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )

            # Handle different event types
            if event.type == "payment_intent.succeeded":
                return self._handle_payment_success(event.data.object)
            elif event.type == "payment_intent.payment_failed":
                return self._handle_payment_failure(event.data.object)
            elif event.type == "charge.refunded":
                return self._handle_refund(event.data.object)

            return {"success": True, "action": "ignored"}

        except stripe.error.SignatureVerificationError:
            return {"success": False, "error": "Invalid signature"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _handle_payment_success(self, payment_intent) -> Dict[str, Any]:
        """Handle successful payment."""
        reference = payment_intent.metadata.get("reference")

        if reference:
            # Create Payment Entry in ERPNext
            self._create_payment_entry(
                reference=reference,
                amount=payment_intent.amount / 100,
                currency=payment_intent.currency.upper(),
                gateway_reference=payment_intent.id
            )

        self.log_transaction(
            gateway="Stripe",
            transaction_type="Payment Succeeded",
            reference=reference or payment_intent.id,
            status="Completed",
            amount=payment_intent.amount / 100,
            currency=payment_intent.currency.upper(),
            gateway_response={"intent_id": payment_intent.id}
        )

        return {"success": True, "action": "payment_recorded"}

    def _handle_payment_failure(self, payment_intent) -> Dict[str, Any]:
        """Handle failed payment."""
        reference = payment_intent.metadata.get("reference")

        self.log_transaction(
            gateway="Stripe",
            transaction_type="Payment Failed",
            reference=reference or payment_intent.id,
            status="Failed",
            amount=payment_intent.amount / 100,
            currency=payment_intent.currency.upper(),
            gateway_response={
                "intent_id": payment_intent.id,
                "error": payment_intent.last_payment_error
            }
        )

        return {"success": True, "action": "failure_logged"}

    def _handle_refund(self, charge) -> Dict[str, Any]:
        """Handle refund."""
        self.log_transaction(
            gateway="Stripe",
            transaction_type="Refund",
            reference=charge.payment_intent,
            status="Refunded",
            amount=charge.amount_refunded / 100,
            currency=charge.currency.upper(),
            gateway_response={"charge_id": charge.id}
        )

        return {"success": True, "action": "refund_logged"}

    def refund_payment(self, payment_intent_id: str, amount: float = None) -> Dict[str, Any]:
        """Refund a Stripe payment."""

        try:
            refund_data = {"payment_intent": payment_intent_id}
            if amount:
                refund_data["amount"] = int(amount * 100)

            refund = stripe.Refund.create(**refund_data)

            return {
                "success": True,
                "refund_id": refund.id,
                "status": refund.status,
                "amount": refund.amount / 100
            }

        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}

    def _create_payment_entry(
        self,
        reference: str,
        amount: float,
        currency: str,
        gateway_reference: str
    ):
        """Create Payment Entry in ERPNext."""

        # Determine if reference is Sales Invoice or Sales Order
        if frappe.db.exists("Sales Invoice", reference):
            doc = frappe.get_doc("Sales Invoice", reference)
            payment_type = "Receive"
            party_type = "Customer"
            party = doc.customer
        elif frappe.db.exists("Sales Order", reference):
            doc = frappe.get_doc("Sales Order", reference)
            payment_type = "Receive"
            party_type = "Customer"
            party = doc.customer
        else:
            frappe.log_error(f"Unknown reference for payment: {reference}")
            return

        # Get payment account
        payment_account = frappe.db.get_value(
            "Mode of Payment Account",
            {"parent": "Stripe", "company": doc.company},
            "default_account"
        )

        pe = frappe.new_doc("Payment Entry")
        pe.payment_type = payment_type
        pe.party_type = party_type
        pe.party = party
        pe.company = doc.company
        pe.paid_amount = amount
        pe.received_amount = amount
        pe.paid_to = payment_account
        pe.paid_to_account_currency = currency
        pe.reference_no = gateway_reference
        pe.reference_date = frappe.utils.today()
        pe.remarks = f"Payment via Stripe - {gateway_reference}"

        pe.append("references", {
            "reference_doctype": doc.doctype,
            "reference_name": doc.name,
            "allocated_amount": amount
        })

        pe.insert(ignore_permissions=True)
        pe.submit()
        frappe.db.commit()
```

### Step 3: Razorpay Integration

```python
import frappe
import razorpay
import hmac
import hashlib
from typing import Dict, Any

class RazorpayGateway(PaymentGateway):
    """Razorpay payment gateway integration."""

    def __init__(self):
        settings = frappe.get_single("Razorpay Settings")
        self.key_id = settings.key_id
        self.key_secret = settings.get_password("key_secret")
        self.client = razorpay.Client(auth=(self.key_id, self.key_secret))

    def create_payment_intent(
        self,
        amount: float,
        currency: str,
        reference: str,
        customer_email: str = None,
        metadata: dict = None
    ) -> Dict[str, Any]:
        """Create Razorpay Order."""

        try:
            # Convert to paise for INR
            amount_paise = int(amount * 100)

            order_data = {
                "amount": amount_paise,
                "currency": currency.upper(),
                "receipt": reference,
                "notes": metadata or {}
            }

            order = self.client.order.create(data=order_data)

            self.log_transaction(
                gateway="Razorpay",
                transaction_type="Order Created",
                reference=reference,
                status="Pending",
                amount=amount,
                currency=currency,
                gateway_response={"order_id": order["id"]}
            )

            return {
                "success": True,
                "order_id": order["id"],
                "key_id": self.key_id,
                "amount": amount_paise,
                "currency": currency.upper()
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_payment(self, payment_id: str) -> Dict[str, Any]:
        """Verify Razorpay payment."""

        try:
            payment = self.client.payment.fetch(payment_id)

            return {
                "success": True,
                "status": payment["status"],
                "paid": payment["status"] == "captured",
                "amount": payment["amount"] / 100,
                "currency": payment["currency"],
                "order_id": payment["order_id"]
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def verify_payment_signature(
        self,
        order_id: str,
        payment_id: str,
        signature: str
    ) -> bool:
        """Verify Razorpay payment signature."""

        message = f"{order_id}|{payment_id}"
        expected_signature = hmac.new(
            self.key_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    def process_webhook(self, payload: dict, signature: str) -> Dict[str, Any]:
        """Process Razorpay webhook."""

        try:
            # Verify webhook signature
            expected_signature = hmac.new(
                self.key_secret.encode(),
                frappe.as_json(payload).encode(),
                hashlib.sha256
            ).hexdigest()

            if not hmac.compare_digest(signature, expected_signature):
                return {"success": False, "error": "Invalid signature"}

            event = payload.get("event")

            if event == "payment.captured":
                return self._handle_payment_captured(payload["payload"]["payment"]["entity"])
            elif event == "payment.failed":
                return self._handle_payment_failed(payload["payload"]["payment"]["entity"])
            elif event == "refund.created":
                return self._handle_refund_created(payload["payload"]["refund"]["entity"])

            return {"success": True, "action": "ignored"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _handle_payment_captured(self, payment) -> Dict[str, Any]:
        """Handle captured payment."""

        # Get order to find reference
        order = self.client.order.fetch(payment["order_id"])
        reference = order.get("receipt")

        if reference:
            self._create_payment_entry(
                reference=reference,
                amount=payment["amount"] / 100,
                currency=payment["currency"],
                gateway_reference=payment["id"]
            )

        self.log_transaction(
            gateway="Razorpay",
            transaction_type="Payment Captured",
            reference=reference or payment["id"],
            status="Completed",
            amount=payment["amount"] / 100,
            currency=payment["currency"],
            gateway_response=payment
        )

        return {"success": True, "action": "payment_recorded"}

    def refund_payment(self, payment_id: str, amount: float = None) -> Dict[str, Any]:
        """Refund a Razorpay payment."""

        try:
            refund_data = {}
            if amount:
                refund_data["amount"] = int(amount * 100)

            refund = self.client.payment.refund(payment_id, refund_data)

            return {
                "success": True,
                "refund_id": refund["id"],
                "status": refund["status"],
                "amount": refund["amount"] / 100
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Step 4: Payment Controller

```python
import frappe
from frappe import _

class PaymentController:
    """Controller for payment operations."""

    GATEWAYS = {
        "stripe": StripeGateway,
        "razorpay": RazorpayGateway
    }

    @classmethod
    def get_gateway(cls, gateway_name: str) -> PaymentGateway:
        """Get payment gateway instance."""
        gateway_class = cls.GATEWAYS.get(gateway_name.lower())
        if not gateway_class:
            frappe.throw(_("Unknown payment gateway: {0}").format(gateway_name))
        return gateway_class()

    @classmethod
    def initiate_payment(
        cls,
        gateway_name: str,
        reference: str,
        amount: float,
        currency: str,
        customer_email: str = None
    ) -> Dict[str, Any]:
        """Initiate payment with specified gateway."""

        gateway = cls.get_gateway(gateway_name)
        return gateway.create_payment_intent(
            amount=amount,
            currency=currency,
            reference=reference,
            customer_email=customer_email,
            metadata={"source": "ERPNext"}
        )

    @classmethod
    def verify_and_record_payment(
        cls,
        gateway_name: str,
        payment_id: str,
        reference: str = None
    ) -> Dict[str, Any]:
        """Verify payment and record if successful."""

        gateway = cls.get_gateway(gateway_name)
        result = gateway.verify_payment(payment_id)

        if result.get("paid"):
            # Record in ERPNext
            gateway._create_payment_entry(
                reference=reference or result.get("metadata", {}).get("reference"),
                amount=result["amount"],
                currency=result["currency"],
                gateway_reference=payment_id
            )
            result["recorded"] = True

        return result

# API Endpoints
@frappe.whitelist(allow_guest=True)
def initiate_payment(gateway: str, reference: str, amount: float, currency: str = "USD"):
    """Initiate payment - called from frontend."""
    # Get customer email from reference
    if frappe.db.exists("Sales Invoice", reference):
        customer_email = frappe.db.get_value("Sales Invoice", reference, "contact_email")
    else:
        customer_email = None

    return PaymentController.initiate_payment(
        gateway_name=gateway,
        reference=reference,
        amount=float(amount),
        currency=currency,
        customer_email=customer_email
    )

@frappe.whitelist(allow_guest=True)
def stripe_webhook():
    """Handle Stripe webhook."""
    gateway = StripeGateway()
    payload = frappe.request.get_data(as_text=True)
    signature = frappe.request.headers.get("Stripe-Signature")

    result = gateway.process_webhook(payload, signature)
    return result

@frappe.whitelist(allow_guest=True)
def razorpay_webhook():
    """Handle Razorpay webhook."""
    gateway = RazorpayGateway()
    payload = frappe.request.json
    signature = frappe.request.headers.get("X-Razorpay-Signature")

    result = gateway.process_webhook(payload, signature)
    return result
```

## Complete Checkout Flow Example

```javascript
// Frontend checkout with Stripe
async function initiateStripePayment(invoiceId, amount) {
    // 1. Create payment intent
    const response = await frappe.call({
        method: 'your_app.payment.initiate_payment',
        args: {
            gateway: 'stripe',
            reference: invoiceId,
            amount: amount,
            currency: 'USD'
        }
    });

    if (!response.message.success) {
        frappe.msgprint(response.message.error);
        return;
    }

    const { client_secret, publishable_key } = response.message;

    // 2. Initialize Stripe
    const stripe = Stripe(publishable_key);
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    // 3. Handle payment submission
    document.getElementById('payment-form').addEventListener('submit', async (e) => {
        e.preventDefault();

        const { error, paymentIntent } = await stripe.confirmCardPayment(client_secret, {
            payment_method: {
                card: card
            }
        });

        if (error) {
            frappe.msgprint(error.message);
        } else if (paymentIntent.status === 'succeeded') {
            frappe.msgprint('Payment successful!');
            // Redirect to success page
            window.location.href = '/payment-success?reference=' + invoiceId;
        }
    });
}
```

## Troubleshooting

### Webhook Not Received
- Verify webhook URL is accessible
- Check webhook signature configuration
- Review gateway dashboard for delivery status

### Payment Not Recorded
- Check webhook processing logs
- Verify reference format matches
- Review Payment Entry creation

## Next Steps

- [Webhook Event Handling](../webhook-event-handling/webhook-event-handling.md)
- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)

---

*Source: Frappe Integration Documentation | Difficulty: Advanced | Last updated: 2026-02-04*
