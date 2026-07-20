"""
DCNet Marketplace Connection — Python controller.

Xử lý business logic cho form kết nối sàn TMĐT:
- Validate credentials trước khi save
- Clean token khi platform thay đổi
"""

import frappe
from frappe.model.document import Document


class DCNetMarketplaceConnection(Document):
    """Controller for DCNet Marketplace Connection doctype."""

    def validate(self):
        """Validate connection config trước khi save."""
        self._validate_required_credentials()

    def _validate_required_credentials(self):
        """Kiểm tra credentials cần thiết dựa trên nền tảng (Platform)."""
        platform = self.platform

        if platform == "Shopee":
            if not self.api_key or not self.api_secret:
                frappe.throw("Shopee yêu cầu API Key và API Secret.")
            if not self.shop_id or not self.partner_id:
                frappe.throw("Shopee yêu cầu Shop ID và Partner ID.")

        elif platform == "Lazada":
            if not self.api_key_lazada or not self.api_secret_lazada:
                frappe.throw("Lazada yêu cầu API Key và API Secret.")

        elif platform == "TikTok Shop":
            if not self.api_key_tiktok or not self.api_secret_tiktok:
                frappe.throw("TikTok Shop yêu cầu API Key và API Secret.")
            if not self.service_id:
                frappe.throw("TikTok Shop yêu cầu Service ID.")

        elif platform == "Woocommerce":
            if not self.consumer_key or not self.consumer_secret:
                frappe.throw("Woocommerce yêu cầu Consumer Key và Consumer Secret.")
            if not self.store_url:
                frappe.throw("Woocommerce yêu cầu Store URL.")

    @frappe.whitelist()
    def get_auth_url(self):
        """
        Khởi tạo luồng OAuth:
        1. Tạo state ngẫu nhiên và lưu trực tiếp vào DB.
        2. Lấy callback URL.
        3. Gọi connector để tạo Auth URL.
        """
        from dcnet_apps.dcnet_ecommerce.api import _build_connector

        # Tạo state để chống CSRF và lưu trực tiếp vào DB để tránh chạy lại hooks
        state = frappe.generate_hash(length=24)
        frappe.db.set_value(self.doctype, self.name, "state", state, update_modified=False)
        self.state = state  # Cập nhật state cho object trong bộ nhớ

        # Callback URL trỏ về endpoint api.py
        callback_url = frappe.utils.get_url(
            "/api/method/dcnet_apps.dcnet_ecommerce.api.oauth_callback"
        )

        connector = _build_connector(self)
        try:
            url = connector.get_auth_url(callback_url, self.state)
            frappe.msgprint(f"Generated URL: {url}", alert=True)
            return url
        except NotImplementedError:
            frappe.throw(f"Platform {self.platform} chưa hỗ trợ OAuth flow.")

    def on_update(self):
        """On update hook."""
        pass


@frappe.whitelist()
def get_auth_url(docname):
    """Module-level wrapper for get_auth_url."""
    doc = frappe.get_doc("DCNet Marketplace Connection", docname)
    return doc.get_auth_url()
