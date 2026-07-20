# WooCommerce Integration Pattern

Example for DCNET Flow WooCommerce integration.

## Incoming Webhook (WooCommerce → ERPNext)

```python
# In custom app
@frappe.whitelist(allow_guest=True)
def woocommerce_webhook():
    """Handle incoming WooCommerce webhooks"""
    data = frappe.request.json

    # Verify signature
    signature = frappe.request.headers.get("X-WC-Webhook-Signature")
    if not verify_wc_signature(data, signature):
        frappe.throw("Invalid signature", frappe.AuthenticationError)

    topic = frappe.request.headers.get("X-WC-Webhook-Topic")

    if topic == "order.created":
        create_sales_order(data)
    elif topic == "order.updated":
        update_sales_order(data)
    elif topic == "product.updated":
        sync_item(data)

    return {"status": "success"}
```

## Outgoing Sync (ERPNext → WooCommerce)

```python
# Webhook on Sales Invoice submit
webhook = frappe.new_doc("Webhook")
webhook.webhook_doctype = "Sales Invoice"
webhook.webhook_docevent = "on_submit"
webhook.request_url = "https://your-store.com/wp-json/wc/v3/orders/{{ doc.woocommerce_order_id }}"
webhook.request_method = "PUT"
webhook.webhook_json = '''
{
    "status": "completed",
    "meta_data": [
        {"key": "erpnext_invoice", "value": "{{ doc.name }}"}
    ]
}
'''
# Add WooCommerce auth header
webhook.append("webhook_headers", {
    "key": "Authorization",
    "value": "Basic {{ frappe.utils.base64_encode('ck_xxx:cs_xxx') }}"
})
webhook.insert()
```

## Verify WooCommerce Signature

```python
import hmac
import hashlib
import base64

def verify_wc_signature(payload, signature, secret):
    """Verify WooCommerce webhook signature"""
    if not signature or not secret:
        return False

    # WooCommerce uses base64(hmac-sha256(secret, payload))
    expected = base64.b64encode(
        hmac.new(
            secret.encode(),
            payload.encode() if isinstance(payload, str) else payload,
            hashlib.sha256
        ).digest()
    ).decode()

    return hmac.compare_digest(signature, expected)
```

## Sync Product from WooCommerce

```python
def sync_item_from_woocommerce(wc_product):
    """Create or update Item from WooCommerce product"""
    item_code = f"WC-{wc_product['id']}"

    if frappe.db.exists("Item", item_code):
        item = frappe.get_doc("Item", item_code)
    else:
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_group = "Products"

    item.item_name = wc_product['name']
    item.description = wc_product.get('description', '')
    item.standard_rate = float(wc_product.get('price', 0))
    item.woocommerce_id = wc_product['id']

    item.save(ignore_permissions=True)
    frappe.db.commit()

    return item.name
```

## Create Sales Order from WooCommerce

```python
def create_sales_order_from_woocommerce(wc_order):
    """Create Sales Order from WooCommerce order"""
    # Find or create customer
    customer = get_or_create_customer(wc_order['billing'])

    so = frappe.new_doc("Sales Order")
    so.customer = customer
    so.woocommerce_order_id = wc_order['id']
    so.delivery_date = frappe.utils.add_days(frappe.utils.today(), 7)

    for line in wc_order['line_items']:
        item_code = f"WC-{line['product_id']}"
        if not frappe.db.exists("Item", item_code):
            sync_item_from_woocommerce({"id": line['product_id'], "name": line['name']})

        so.append("items", {
            "item_code": item_code,
            "qty": line['quantity'],
            "rate": float(line['price']),
            "delivery_date": so.delivery_date
        })

    so.insert(ignore_permissions=True)
    so.submit()
    frappe.db.commit()

    return so.name
```
