"""
Whitelisted API endpoints cho DCNet Ecommerce.

Tất cả endpoints đều check Frappe permission trước khi thực thi.
"""

import frappe
from dcnet_apps.dcnet_ecommerce.connectors import CONNECTOR_MAP


# ------------------------------------------------------------------
# Permission helpers
# ------------------------------------------------------------------

def _require_permission(doctype: str, ptype: str = "read") -> None:
    """Kiểm tra quyền Frappe, throw 403 nếu không đủ quyền."""
    if not frappe.has_permission(doctype, ptype):
        frappe.throw(
            f"Bạn không có quyền '{ptype}' trên {doctype}.",
            frappe.PermissionError
        )


def _get_connection_doc(connection_name: str):
    """Load và validate connection document."""
    _require_permission("DCNet Marketplace Connection", "read")
    return frappe.get_doc("DCNet Marketplace Connection", connection_name)


def _build_connector(connection_doc):
    """Khởi tạo connector từ connection document."""
    from dcnet_apps.dcnet_ecommerce.connectors import get_connector
    return get_connector(connection_doc)


# ------------------------------------------------------------------
# Platform & Connection management
# ------------------------------------------------------------------

@frappe.whitelist()
def get_supported_platforms() -> list[str]:
    """
    Trả về danh sách các sàn TMĐT đang được hỗ trợ.
    """
    return list(CONNECTOR_MAP.keys())


@frappe.whitelist()
def get_connections(platform: str = None, enabled: int = 1) -> list[dict]:
    """
    Lấy danh sách kết nối marketplace.

    Args:
        platform: Lọc theo sàn (optional).
        enabled:  1 = chỉ lấy kết nối đang bật (mặc định), 0 = tất cả.
    """
    _require_permission("DCNet Marketplace Connection", "read")

    filters = {}
    if int(enabled):
        filters["enabled"] = 1
    if platform:
        filters["platform"] = platform

    return frappe.get_all(
        "DCNet Marketplace Connection",
        filters=filters,
        fields=[
            "name", "connection_name", "platform", "shop_name",
            "shop_id", "enabled", "is_sandbox"
        ],
    )





@frappe.whitelist()
def disconnect(connection_name: str) -> dict:
    """
    Ngắt kết nối và xóa token cache.
    """
    _require_permission("DCNet Marketplace Connection", "write")

    connection_doc = _get_connection_doc(connection_name)

    try:
        connector = _build_connector(connection_doc)
        connector.disconnect()

        return {
            "success": True,
            "message": f"Đã ngắt kết nối {connection_doc.platform}.",
        }

    except Exception as e:
        frappe.throw(f"Không thể ngắt kết nối: {e}")


@frappe.whitelist()
def get_rate_limit_info(connection_name: str) -> dict:
    """
    Lấy thông tin rate limit từ connector.
    """
    connection_doc = _get_connection_doc(connection_name)

    try:
        connector = _build_connector(connection_doc)
        connector.authenticate()
        return connector.get_rate_limit_info()
    except Exception as e:
        frappe.throw(f"Không thể lấy rate limit info: {e}")


@frappe.whitelist(allow_guest=True)
def oauth_callback(code: str = None, state: str = None, **kwargs) -> None:
    """
    Điểm tiếp nhận callback từ Marketplace sau khi người dùng cấp quyền.
    """
    # WooCommerce không gửi code, nên ta nới lỏng kiểm tra cho phương thức POST
    if frappe.request.method != "POST" and (not code or not state):
        frappe.throw("Thiếu thông số callback (code hoặc state).")
 
    # Nếu không có state trực tiếp (WooCommerce callback), thử lấy từ user_id hoặc payload
    if not state:
        try:
             payload = frappe.request.get_json() or {}
             state = payload.get("user_id") or frappe.form_dict.get("user_id")
        except Exception:
             state = frappe.form_dict.get("user_id")

    # Tìm connection record dựa trên state
    frappe.logger().debug(f"Handling OAuth callback for state: {state}")
    connection = frappe.db.get_value(
        "DCNet Marketplace Connection", 
        {"state": state}, 
        "name"
    )
    if not connection:
        frappe.msgprint(__("Không tìm thấy kết nối ứng với state: {0}. Có thể state đã hết hạn hoặc nhầm lẫn.", [state]))
        frappe.throw("Yêu cầu không hợp lệ hoặc đã hết hạn (state mismatch).")

    doc = frappe.get_doc("DCNet Marketplace Connection", connection)
    
    try:
        connector = _build_connector(doc)
        callback_url = frappe.utils.get_url(
            "/api/method/dcnet_apps.dcnet_ecommerce.api.oauth_callback"
        )
        
        # 1. Đổi code lấy token
        if frappe.request.method == "POST":
            # WooCommerce POST callback case
            try:
                # Try JSON first, then form data
                token_data = frappe.request.get_json() or frappe.form_dict
                if not token_data.get("consumer_key"):
                     # Có thể là callback trống hoặc không hợp lệ
                     return
            except Exception:
                token_data = frappe.form_dict
        else:
            # Standard GET callback (Shopee, Lazada, TikTok)
            token_data = connector.handle_oauth_callback(code, callback_url)
        
        # 2. Lưu token & thông tin shop vào doc
        if token_data.get("consumer_key"):
            # WooCommerce case
            doc.consumer_key = token_data.get("consumer_key")
            doc.consumer_secret = token_data.get("consumer_secret")
            if token_data.get("user_id"):
                doc.shop_id = token_data.get("user_id")
        else:
            # Common case (access_token based)
            doc.access_token = token_data.get("access_token")
            doc.refresh_token = token_data.get("refresh_token")
            
            expires_in = token_data.get("expires_in")
            if expires_in:
                from frappe.utils import add_to_date, now_datetime
                doc.token_expires_at = add_to_date(now_datetime(), seconds=int(expires_in))
        
        if token_data.get("shop_id") and not doc.shop_id:
            doc.shop_id = token_data.get("shop_id")
        if token_data.get("shop_name"):
            doc.shop_name = token_data.get("shop_name")
            
        # Clear state sau khi dùng
        doc.state = None
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        # Redirect về trang view của connection
        redirect_url = frappe.utils.get_url(f"/app/dcnet-marketplace-connection/{doc.name}")
        frappe.local.response.type = "redirect"
        frappe.local.response.location = redirect_url

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Marketplace OAuth Callback Error")
        frappe.msgprint(
            __("Đã có lỗi xảy ra trong quá trình xử lý callback: {0}. Vui lòng kiểm tra Error Log.", [str(e)]), 
            title=__("Lỗi kết nối"),
            indicator="red"
        )
        # Chuyển hướng thay vì ném exception 417
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/app"


# ------------------------------------------------------------------
# Internal background job processors (Disabled for current version)
# ------------------------------------------------------------------

def _process_order_sync(connection_name: str, from_date: str, to_date: str) -> None:
    pass


def _process_product_sync(connection_name: str) -> None:
    pass
