import frappe
from frappe.core.doctype.user.user import sha256_hash
from frappe.utils import get_url, now_datetime


class DCNETPermissionUserMixin:
    def _reset_password(self, send_email=False, password_expired=False):
        key = frappe.generate_hash()
        hashed_key = sha256_hash(key)
        self.db_set("reset_password_key", hashed_key)
        self.db_set("last_reset_password_key_generated_on", now_datetime())

        url = "/update-password?key=" + key
        if password_expired:
            url += "&password_expired=true"

        if send_email:
            link = get_url(url, allow_header_override=False)
            self.password_reset_mail(link)
            return link

        return url
