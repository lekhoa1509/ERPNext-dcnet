"""HTKK Declaration — lưu lịch sử tờ khai và giá trị nhập tay."""

import json

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, get_first_day, get_last_day, getdate


class HTKKDeclaration(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        from dcnet_apps.htkk.doctype.htkk_declaration_adjustment.htkk_declaration_adjustment import (
            HTKKDeclarationAdjustment,
        )
        from dcnet_apps.htkk.doctype.htkk_declaration_ct_value.htkk_declaration_ct_value import (
            HTKKDeclarationCtValue,
        )

        adjustments: DF.Table[HTKKDeclarationAdjustment]
        company: DF.Link
        ct_values: DF.Table[HTKKDeclarationCtValue]
        declaration_type: DF.Literal["01/GTGT", "03/TNDN", "BCTC"]
        finance_book: DF.Link | None
        from_date: DF.Date | None
        generated_at: DF.Datetime | None
        generated_xml: DF.Attach | None
        import_goods_value: DF.Currency
        import_vat_account: DF.Link | None
        import_vat_amount: DF.Currency
        investment_vat_offset: DF.Currency
        notes: DF.SmallText | None
        period: DF.Int
        period_type: DF.Literal["Tháng", "Quý", "Năm"]
        received_vat_credit: DF.Currency
        result_summary: DF.Code | None
        status: DF.Literal["Nháp", "Đã xuất", "Đã nộp"]
        to_date: DF.Date | None
        vat_carried_forward: DF.Currency
        vat_refund_requested: DF.Currency
        year: DF.Int
    # end: auto-generated types

    def validate(self):
        self._validate_period()
        self._compute_dates()
        self._auto_fill_carried_forward()

    def _validate_period(self):
        """Kiểm tra kỳ kê khai hợp lệ."""
        if self.period_type == "Tháng" and not (1 <= self.period <= 12):
            frappe.throw(_("Kỳ tháng phải từ 1 đến 12"))
        elif self.period_type == "Quý" and not (1 <= self.period <= 4):
            frappe.throw(_("Kỳ quý phải từ 1 đến 4"))
        elif self.period_type == "Năm":
            self.period = 0

    def _compute_dates(self):
        """Tự tính from_date, to_date từ period_type + period + year."""
        if self.period_type == "Tháng":
            self.from_date = get_first_day(f"{self.year}-{self.period:02d}-01")
            self.to_date = get_last_day(f"{self.year}-{self.period:02d}-01")
        elif self.period_type == "Quý":
            start_month = (self.period - 1) * 3 + 1
            end_month = start_month + 2
            self.from_date = get_first_day(f"{self.year}-{start_month:02d}-01")
            self.to_date = get_last_day(f"{self.year}-{end_month:02d}-01")
        elif self.period_type == "Năm":
            self.from_date = getdate(f"{self.year}-01-01")
            self.to_date = getdate(f"{self.year}-12-31")

    def _auto_fill_carried_forward(self):
        """Tự động lấy CT43 từ HTKK Declaration kỳ liền trước (nếu chưa nhập tay)."""
        if self.declaration_type != "01/GTGT":
            return
        if self.vat_carried_forward:
            return
        if self.is_new():
            prev = self._get_previous_declaration()
            if prev:
                ct43 = self._get_ct43_from_declaration(prev)
                if ct43:
                    self.vat_carried_forward = ct43

    def _get_ct43_from_declaration(self, declaration_doc):
        """Đọc CT43 từ ct_values table hoặc result_summary."""
        # Ưu tiên ct_values (có manual overrides)
        if declaration_doc.ct_values:
            for row in declaration_doc.ct_values:
                if row.ct_name == "ct43":
                    return flt(row.manual_value) if row.is_manual else flt(row.auto_value)
        # Fallback: result_summary JSON
        if declaration_doc.result_summary:
            try:
                summary = json.loads(declaration_doc.result_summary)
                return flt(summary.get("ct43", 0))
            except (json.JSONDecodeError, TypeError):
                pass
        return 0

    def _get_previous_declaration(self):
        """Tìm HTKK Declaration kỳ liền trước cùng company + loại."""
        filters = {
            "company": self.company,
            "declaration_type": self.declaration_type,
            "status": ("in", ["Đã xuất", "Đã nộp"]),
            "name": ("!=", self.name or ""),
        }

        if self.period_type == "Tháng":
            if self.period == 1:
                filters["period"] = 12
                filters["year"] = self.year - 1
            else:
                filters["period"] = self.period - 1
                filters["year"] = self.year
            filters["period_type"] = "Tháng"
        elif self.period_type == "Quý":
            if self.period == 1:
                filters["period"] = 4
                filters["year"] = self.year - 1
            else:
                filters["period"] = self.period - 1
                filters["year"] = self.year
            filters["period_type"] = "Quý"

        prev_name = frappe.db.get_value("HTKK Declaration", filters, "name")
        if prev_name:
            return frappe.get_doc("HTKK Declaration", prev_name)
        return None

    def get_finance_book(self):
        """Lấy finance_book: ưu tiên field trên declaration, fallback HTKK Settings."""
        if self.finance_book:
            return self.finance_book
        settings = frappe.get_single("HTKK Settings")
        return settings.default_finance_book

    @frappe.whitelist()
    def calculate(self):
        """
        Tính toán các chỉ tiêu từ chứng từ và cập nhật ct_values table.
        Sử dụng Declaration Registry để tìm generator tương ứng.
        """
        from dcnet_apps.htkk.api import _get_generator

        if not self.from_date or not self.to_date:
            frappe.throw(_("Vui lòng chọn kỳ kê khai trước khi tính toán."))

        # Lấy generator cho loại tờ khai này
        generator = _get_generator(self.declaration_type)

        if not hasattr(generator, "compute_chi_tieu"):
            frappe.throw(_("Loại tờ khai {0} chưa hỗ trợ tính toán tự động.").format(self.declaration_type))

        # Tính toán
        all_data = generator.compute_chi_tieu(self)

        # Lưu lại manual overrides hiện có
        existing = {row.ct_name: row for row in self.ct_values}

        self.set("ct_values", [])
        for ct_name, info in all_data.items():
            auto_value = info.get("auto_value", 0)
            label = info.get("label", ct_name)
            source = info.get("source", "")

            existing_row = existing.get(ct_name)
            is_manual = int(existing_row.is_manual) if existing_row else 0
            manual_value = flt(existing_row.manual_value) if (existing_row and existing_row.is_manual) else 0

            self.append("ct_values", {
                "ct_name": ct_name,
                "label": label,
                "auto_value": auto_value,
                "is_manual": is_manual,
                "manual_value": manual_value,
                "data_source": source,
            })

        # Cập nhật result_summary với giá trị cuối cùng (backward compat)
        final_ct = {}
        for row in self.ct_values:
            val = flt(row.manual_value) if row.is_manual else flt(row.auto_value)
            final_ct[row.ct_name] = val
        self.result_summary = json.dumps(final_ct, ensure_ascii=False)

        self.save(ignore_permissions=True)

        count_manual = sum(1 for row in self.ct_values if row.is_manual)
        count_total = len(self.ct_values)
        msg = f"Đã tính toán {count_total} chỉ tiêu."
        if count_manual:
            msg += f" {count_manual} chỉ tiêu đang được ghi đè thủ công."
        frappe.msgprint(msg, alert=True, indicator="green")

        return final_ct

    @frappe.whitelist()
    def preview(self):
        """Gọi từ nút 'Xem trước' trên form."""
        from dcnet_apps.htkk.api import preview_declaration

        return preview_declaration(self.name)

    @frappe.whitelist()
    def export_xml(self):
        """Gọi từ nút 'Xuất XML' trên form."""
        from dcnet_apps.htkk.api import export_declaration

        return export_declaration(self.name)
