# How To: Third-Party API Integration Examples

**Difficulty**: Intermediate
**Estimated Time**: 35 minutes
**Tags**: api, integration, external-services, examples, patterns

## Overview

Learn practical examples of integrating Frappe with various third-party APIs including shipping carriers, CRM systems, accounting software, and more.

## Prerequisites

- REST API knowledge
- Frappe development basics
- Understanding of OAuth/API Keys

## Step-by-Step Guide

### Example 1: Shipping Carrier Integration (Viettel Post)

```python
import frappe
import requests
import hashlib
from typing import Dict, Any

class ViettelPostAPI:
    """Integration with Viettel Post shipping API."""

    def __init__(self):
        settings = frappe.get_single("Viettel Post Settings")
        self.base_url = "https://partner.viettelpost.vn/v2"
        self.token = settings.get_password("api_token")
        self.partner_id = settings.partner_id

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Token": self.token
        }

    def create_order(self, shipment_data: dict) -> Dict[str, Any]:
        """Create shipping order with Viettel Post."""

        payload = {
            "ORDER_NUMBER": shipment_data["reference"],
            "SENDER_FULLNAME": shipment_data["sender_name"],
            "SENDER_ADDRESS": shipment_data["sender_address"],
            "SENDER_PHONE": shipment_data["sender_phone"],
            "SENDER_WARD": shipment_data["sender_ward_code"],
            "SENDER_DISTRICT": shipment_data["sender_district_code"],
            "SENDER_PROVINCE": shipment_data["sender_province_code"],
            "RECEIVER_FULLNAME": shipment_data["receiver_name"],
            "RECEIVER_ADDRESS": shipment_data["receiver_address"],
            "RECEIVER_PHONE": shipment_data["receiver_phone"],
            "RECEIVER_WARD": shipment_data["receiver_ward_code"],
            "RECEIVER_DISTRICT": shipment_data["receiver_district_code"],
            "RECEIVER_PROVINCE": shipment_data["receiver_province_code"],
            "PRODUCT_NAME": shipment_data["product_name"],
            "PRODUCT_WEIGHT": shipment_data["weight"],
            "ORDER_PAYMENT": shipment_data.get("payment_method", 1),  # 1=Sender pays
            "MONEY_COLLECTION": shipment_data.get("cod_amount", 0)
        }

        try:
            response = requests.post(
                f"{self.base_url}/order/createOrder",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if result.get("status") == 200:
                return {
                    "success": True,
                    "order_id": result["data"]["ORDER_NUMBER"],
                    "tracking_number": result["data"]["ORDER_NUMBER"],
                    "fee": result["data"].get("MONEY_TOTAL_FEE")
                }
            else:
                return {"success": False, "error": result.get("message")}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def track_order(self, tracking_number: str) -> Dict[str, Any]:
        """Track shipment status."""

        try:
            response = requests.get(
                f"{self.base_url}/order/getOrderTracking",
                headers=self._get_headers(),
                params={"ORDER_NUMBER": tracking_number},
                timeout=30
            )
            result = response.json()

            if result.get("status") == 200:
                tracking_data = result["data"]
                return {
                    "success": True,
                    "status": tracking_data.get("STATUS"),
                    "status_name": tracking_data.get("STATUS_NAME"),
                    "history": tracking_data.get("JOURNEY", [])
                }
            else:
                return {"success": False, "error": result.get("message")}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_fee(self, from_district: str, to_district: str, weight: int) -> Dict[str, Any]:
        """Calculate shipping fee."""

        payload = {
            "SENDER_DISTRICT": from_district,
            "RECEIVER_DISTRICT": to_district,
            "PRODUCT_WEIGHT": weight,
            "PRODUCT_TYPE": "HH"  # Hang hoa
        }

        try:
            response = requests.post(
                f"{self.base_url}/order/getPriceAll",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            result = response.json()

            if result.get("status") == 200:
                return {
                    "success": True,
                    "services": result["data"]  # List of service options with prices
                }
            else:
                return {"success": False, "error": result.get("message")}

        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Example 2: Accounting Software Integration (MISA)

```python
import frappe
import requests
from typing import Dict, Any, List

class MISAIntegration:
    """Integration with MISA accounting software."""

    def __init__(self):
        settings = frappe.get_single("MISA Settings")
        self.base_url = settings.api_url
        self.app_id = settings.app_id
        self.access_code = settings.get_password("access_code")
        self.company_code = settings.company_code

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-MISA-AppID": self.app_id,
            "X-MISA-AccessCode": self.access_code,
            "X-MISA-CompanyCode": self.company_code
        }

    def sync_customer(self, customer: dict) -> Dict[str, Any]:
        """Sync customer to MISA."""

        payload = {
            "CustomerCode": customer["name"],
            "CustomerName": customer["customer_name"],
            "Address": customer.get("address"),
            "TaxCode": customer.get("tax_id"),
            "Mobile": customer.get("mobile_no"),
            "Email": customer.get("email_id")
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/customers",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_invoice(self, invoice_data: dict) -> Dict[str, Any]:
        """Create sales invoice in MISA."""

        payload = {
            "RefNo": invoice_data["name"],
            "RefDate": invoice_data["posting_date"],
            "CustomerCode": invoice_data["customer"],
            "CustomerName": invoice_data["customer_name"],
            "Address": invoice_data.get("customer_address"),
            "TaxCode": invoice_data.get("tax_id"),
            "TotalAmount": invoice_data["grand_total"],
            "VATAmount": invoice_data["total_taxes_and_charges"],
            "Items": []
        }

        for item in invoice_data["items"]:
            payload["Items"].append({
                "ItemCode": item["item_code"],
                "ItemName": item["item_name"],
                "Quantity": item["qty"],
                "UnitPrice": item["rate"],
                "Amount": item["amount"]
            })

        try:
            response = requests.post(
                f"{self.base_url}/api/invoices",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return {
                "success": True,
                "misa_invoice_id": result.get("InvoiceID"),
                "invoice_no": result.get("InvoiceNo")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_gl_accounts(self) -> Dict[str, Any]:
        """Get chart of accounts from MISA."""

        try:
            response = requests.get(
                f"{self.base_url}/api/accounts",
                headers=self._get_headers(),
                timeout=30
            )
            response.raise_for_status()
            return {"success": True, "accounts": response.json()}
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Example 3: CRM Integration (HubSpot)

```python
import frappe
import requests
from typing import Dict, Any, List

class HubSpotIntegration:
    """Integration with HubSpot CRM."""

    def __init__(self):
        settings = frappe.get_single("HubSpot Settings")
        self.api_key = settings.get_password("api_key")
        self.base_url = "https://api.hubapi.com"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_contact(self, contact_data: dict) -> Dict[str, Any]:
        """Create contact in HubSpot."""

        payload = {
            "properties": {
                "email": contact_data["email"],
                "firstname": contact_data.get("first_name"),
                "lastname": contact_data.get("last_name"),
                "phone": contact_data.get("phone"),
                "company": contact_data.get("company"),
                "erpnext_id": contact_data.get("erpnext_id")
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/contacts",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return {
                "success": True,
                "hubspot_id": result["id"]
            }
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                # Contact exists, get existing
                return self.get_contact_by_email(contact_data["email"])
            return {"success": False, "error": str(e)}

    def get_contact_by_email(self, email: str) -> Dict[str, Any]:
        """Get contact by email."""

        try:
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/contacts/search",
                headers=self._get_headers(),
                json={
                    "filterGroups": [{
                        "filters": [{
                            "propertyName": "email",
                            "operator": "EQ",
                            "value": email
                        }]
                    }]
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if result["total"] > 0:
                return {
                    "success": True,
                    "hubspot_id": result["results"][0]["id"],
                    "properties": result["results"][0]["properties"]
                }
            return {"success": False, "error": "Contact not found"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_deal(self, deal_data: dict) -> Dict[str, Any]:
        """Create deal in HubSpot."""

        payload = {
            "properties": {
                "dealname": deal_data["name"],
                "amount": deal_data["amount"],
                "pipeline": deal_data.get("pipeline", "default"),
                "dealstage": deal_data.get("stage", "appointmentscheduled"),
                "closedate": deal_data.get("expected_closing"),
                "erpnext_id": deal_data.get("erpnext_id")
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/crm/v3/objects/deals",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            # Associate with contact if provided
            if deal_data.get("contact_id"):
                self._associate_deal_contact(result["id"], deal_data["contact_id"])

            return {
                "success": True,
                "hubspot_deal_id": result["id"]
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _associate_deal_contact(self, deal_id: str, contact_id: str):
        """Associate deal with contact."""
        requests.put(
            f"{self.base_url}/crm/v3/objects/deals/{deal_id}/associations/contacts/{contact_id}/3",
            headers=self._get_headers(),
            timeout=30
        )
```

### Example 4: E-Invoice Integration (Vietnam)

```python
import frappe
import requests
import hashlib
import base64
from typing import Dict, Any

class EInvoiceVietnam:
    """Integration with Vietnam E-Invoice providers."""

    def __init__(self, provider: str = "VNPT"):
        settings = frappe.get_single(f"{provider} E-Invoice Settings")
        self.base_url = settings.api_url
        self.username = settings.username
        self.password = settings.get_password("password")
        self.tax_code = settings.tax_code
        self.provider = provider

    def _get_auth_token(self) -> str:
        """Get authentication token."""
        auth_string = f"{self.username}:{self.password}"
        return base64.b64encode(auth_string.encode()).decode()

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self._get_auth_token()}"
        }

    def create_invoice(self, invoice_data: dict) -> Dict[str, Any]:
        """Create e-invoice."""

        # Format invoice data according to Vietnam e-invoice standard
        payload = {
            "generalInvoiceInfo": {
                "invoiceType": "01GTKT",
                "templateCode": invoice_data.get("template_code", "01GTKT0/001"),
                "invoiceSeries": invoice_data.get("series", "AA/24E"),
                "currencyCode": invoice_data.get("currency", "VND"),
                "adjustmentType": "1",  # 1: Original
                "paymentStatus": "1" if invoice_data.get("paid") else "0",
                "paymentMethodName": invoice_data.get("payment_method", "TM/CK")
            },
            "sellerInfo": {
                "sellerLegalName": invoice_data["seller_name"],
                "sellerTaxCode": self.tax_code,
                "sellerAddressLine": invoice_data["seller_address"],
                "sellerPhoneNumber": invoice_data.get("seller_phone"),
                "sellerBankName": invoice_data.get("seller_bank"),
                "sellerBankAccount": invoice_data.get("seller_bank_account")
            },
            "buyerInfo": {
                "buyerName": invoice_data["buyer_name"],
                "buyerLegalName": invoice_data.get("buyer_company_name"),
                "buyerTaxCode": invoice_data.get("buyer_tax_code"),
                "buyerAddressLine": invoice_data.get("buyer_address"),
                "buyerPhoneNumber": invoice_data.get("buyer_phone"),
                "buyerEmail": invoice_data.get("buyer_email")
            },
            "itemInfo": []
        }

        # Add line items
        for idx, item in enumerate(invoice_data["items"], 1):
            payload["itemInfo"].append({
                "lineNumber": idx,
                "itemCode": item["item_code"],
                "itemName": item["item_name"],
                "unitName": item.get("uom", "Cái"),
                "quantity": item["qty"],
                "unitPrice": item["rate"],
                "itemTotalAmountWithoutTax": item["amount"],
                "taxPercentage": item.get("tax_rate", 10),
                "taxAmount": item.get("tax_amount", item["amount"] * 0.1)
            })

        try:
            response = requests.post(
                f"{self.base_url}/api/invoice/create",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            if result.get("errorCode") == "0":
                return {
                    "success": True,
                    "invoice_no": result.get("invoiceNo"),
                    "lookup_code": result.get("lookupCode"),
                    "pdf_url": result.get("pdfUrl")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("description")
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_invoice_pdf(self, invoice_no: str) -> Dict[str, Any]:
        """Get invoice PDF."""

        try:
            response = requests.get(
                f"{self.base_url}/api/invoice/pdf",
                headers=self._get_headers(),
                params={"invoiceNo": invoice_no},
                timeout=30
            )
            response.raise_for_status()

            return {
                "success": True,
                "pdf_content": response.content
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cancel_invoice(self, invoice_no: str, reason: str) -> Dict[str, Any]:
        """Cancel e-invoice."""

        payload = {
            "invoiceNo": invoice_no,
            "cancelReason": reason
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/invoice/cancel",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()

            return {
                "success": result.get("errorCode") == "0",
                "message": result.get("description")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
```

### Example 5: Google Maps/Geolocation API

```python
import frappe
import requests
from typing import Dict, Any, List

class GoogleMapsAPI:
    """Integration with Google Maps API."""

    def __init__(self):
        settings = frappe.get_single("Google Maps Settings")
        self.api_key = settings.get_password("api_key")
        self.base_url = "https://maps.googleapis.com/maps/api"

    def geocode_address(self, address: str) -> Dict[str, Any]:
        """Convert address to coordinates."""

        try:
            response = requests.get(
                f"{self.base_url}/geocode/json",
                params={
                    "address": address,
                    "key": self.api_key
                },
                timeout=10
            )
            result = response.json()

            if result["status"] == "OK":
                location = result["results"][0]["geometry"]["location"]
                return {
                    "success": True,
                    "latitude": location["lat"],
                    "longitude": location["lng"],
                    "formatted_address": result["results"][0]["formatted_address"]
                }
            else:
                return {"success": False, "error": result["status"]}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def calculate_distance(
        self,
        origin: str,
        destination: str,
        mode: str = "driving"
    ) -> Dict[str, Any]:
        """Calculate distance and duration between two points."""

        try:
            response = requests.get(
                f"{self.base_url}/distancematrix/json",
                params={
                    "origins": origin,
                    "destinations": destination,
                    "mode": mode,
                    "key": self.api_key
                },
                timeout=10
            )
            result = response.json()

            if result["status"] == "OK":
                element = result["rows"][0]["elements"][0]
                if element["status"] == "OK":
                    return {
                        "success": True,
                        "distance": element["distance"]["value"],  # meters
                        "distance_text": element["distance"]["text"],
                        "duration": element["duration"]["value"],  # seconds
                        "duration_text": element["duration"]["text"]
                    }

            return {"success": False, "error": result.get("status")}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_nearby_places(
        self,
        latitude: float,
        longitude: float,
        radius: int = 1000,
        place_type: str = None
    ) -> Dict[str, Any]:
        """Find nearby places."""

        params = {
            "location": f"{latitude},{longitude}",
            "radius": radius,
            "key": self.api_key
        }
        if place_type:
            params["type"] = place_type

        try:
            response = requests.get(
                f"{self.base_url}/place/nearbysearch/json",
                params=params,
                timeout=10
            )
            result = response.json()

            if result["status"] == "OK":
                places = []
                for place in result["results"]:
                    places.append({
                        "name": place["name"],
                        "address": place.get("vicinity"),
                        "latitude": place["geometry"]["location"]["lat"],
                        "longitude": place["geometry"]["location"]["lng"],
                        "rating": place.get("rating"),
                        "types": place.get("types", [])
                    })
                return {"success": True, "places": places}

            return {"success": False, "error": result.get("status")}

        except Exception as e:
            return {"success": False, "error": str(e)}
```

## Usage Examples

```python
# Shipping
viettel = ViettelPostAPI()
result = viettel.create_order({
    "reference": "SO-001",
    "sender_name": "ABC Company",
    # ... other fields
})

# CRM Sync
hubspot = HubSpotIntegration()
result = hubspot.create_contact({
    "email": "customer@example.com",
    "first_name": "John",
    "last_name": "Doe"
})

# E-Invoice
einvoice = EInvoiceVietnam("VNPT")
result = einvoice.create_invoice({
    "seller_name": "ABC Company",
    "buyer_name": "XYZ Customer",
    "items": [...]
})

# Geolocation
maps = GoogleMapsAPI()
distance = maps.calculate_distance(
    "Ho Chi Minh City, Vietnam",
    "Hanoi, Vietnam"
)
```

## Troubleshooting

### API Rate Limits
- Implement caching for frequent requests
- Use batch APIs where available
- Add retry logic with backoff

### Authentication Failures
- Verify credentials are current
- Check IP whitelist settings
- Review API documentation for auth changes

## Next Steps

- [REST API Integration Patterns](../rest-api-integration-patterns/rest-api-integration-patterns.md)
- [Error Handling in Integrations](../error-handling-integrations/error-handling-integrations.md)

---

*Source: Frappe Integration Documentation | Difficulty: Intermediate | Last updated: 2026-02-04*
