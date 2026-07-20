"""
Tờ khai khấu trừ thuế thu nhập cá nhân mẫu 05/KK-TNCN (TT80/2021, XSD v2.0.7).

Kỳ kê khai: hàng tháng.

Cấu trúc chỉ tiêu theo XSD 05_KK_TNCN_TT80_283.xsd:
─────────────────────────────────────────────────────────────
 THÔNG TIN CHUNG
 ct15  Phân bổ thuế do có đơn vị phụ thuộc tại địa bàn khác
 ct16  Tổng số người lao động
 ct17  Trong đó: Cá nhân cư trú có hợp đồng lao động
─────────────────────────────────────────────────────────────
 I. SỐ CÁ NHÂN ĐÃ KHẤU TRỪ THUẾ
 ct18  Tổng số cá nhân đã khấu trừ thuế [18]=[19]+[20]
 ct19  Cá nhân cư trú
 ct20  Cá nhân không cư trú
─────────────────────────────────────────────────────────────
 II. THU NHẬP CHỊU THUẾ TRẢ CHO CÁ NHÂN
 ct21  Tổng thu nhập chịu thuế [21]=[22]+[23]
 ct22  Cá nhân cư trú
 ct23  Cá nhân không cư trú
 ct24  Trong đó: Từ bảo hiểm nhân thọ nước ngoài
 ct25  Trong đó: Thu nhập miễn theo Hợp đồng dầu khí
─────────────────────────────────────────────────────────────
 III. THU NHẬP THUỘC DIỆN KHẤU TRỪ THUẾ
 ct26  Tổng TNCT thuộc diện khấu trừ [26]=[27]+[28]
 ct27  Cá nhân cư trú
 ct28  Cá nhân không cư trú
─────────────────────────────────────────────────────────────
 IV. THUẾ TNCN ĐÃ KHẤU TRỪ
 ct29  Tổng số thuế đã khấu trừ [29]=[30]+[31]
 ct30  Cá nhân cư trú
 ct31  Cá nhân không cư trú
 ct32  Trong đó: Thuế trên bảo hiểm nhân thọ nước ngoài
─────────────────────────────────────────────────────────────

Nguồn dữ liệu từ ERPNext:
  - ct16: COUNT(DISTINCT employee) FROM Salary Slip
  - ct17: COUNT(employee có HĐLĐ) — cần xác định bằng employment_type
  - ct21, ct22: SUM(gross_pay) FROM Salary Slip theo cư trú/không cư trú
  - ct29, ct30: SUM(income_tax_deducted) FROM Salary Slip
"""

import frappe
from frappe.utils import flt

from dcnet_apps.htkk.declarations.base import DeclarationConfig, register


# ---------------------------------------------------------------------------
# Nhãn mô tả cho từng chỉ tiêu (hiển thị trong ct_values table)
# ---------------------------------------------------------------------------

CT_LABELS = {
    "ct15": "Phân bổ thuế do có đơn vị phụ thuộc tại địa bàn khác",
    "ct16": "Tổng số người lao động",
    "ct17": "Trong đó: Cá nhân cư trú có hợp đồng lao động",

    "ct18": "Tổng số cá nhân đã khấu trừ thuế [18]=[19]+[20]",
    "ct19": "Cá nhân cư trú",
    "ct20": "Cá nhân không cư trú",

    "ct21": "Tổng thu nhập chịu thuế trả cho cá nhân [21]=[22]+[23]",
    "ct22": "Cá nhân cư trú",
    "ct23": "Cá nhân không cư trú",
    "ct24": "Trong đó: Thu nhập từ bảo hiểm nhân thọ nước ngoài",
    "ct25": "Trong đó: Thu nhập miễn theo Hợp đồng dầu khí",

    "ct26": "Tổng TNCT thuộc diện khấu trừ [26]=[27]+[28]",
    "ct27": "Cá nhân cư trú",
    "ct28": "Cá nhân không cư trú",

    "ct29": "Tổng số thuế TNCN đã khấu trừ [29]=[30]+[31]",
    "ct30": "Cá nhân cư trú",
    "ct31": "Cá nhân không cư trú",
    "ct32": "Trong đó: Thuế trên bảo hiểm nhân thọ nước ngoài",
}


# ---------------------------------------------------------------------------
# Declaration Config
# ---------------------------------------------------------------------------


@register
class PIT05KKTNCN(DeclarationConfig):
    """Tờ khai khấu trừ thuế thu nhập cá nhân (05/KK-TNCN)."""

    # === METADATA ===
    code = "05/KK-TNCN"
    name = "Tờ khai khấu trừ thuế thu nhập cá nhân"
    short_name = "KK-TNCN"
    xsd_file = "05_KK_TNCN_TT80_283.xsd"
    period = "monthly"
    circular = "TT80/2021/TT-BTC"
    has_appendices = True

    # === FRONTEND CONFIG ===
    title = "Tờ khai khấu trừ thuế thu nhập cá nhân"
    subtitle = "(Áp dụng đối với tổ chức, cá nhân trả thu nhập khấu trừ thuế theo tháng/quý)"

    appendices = [
        {
            "key": "PL05_1_TNCN",
            "label": "PL 05-1/KK-TNCN",
            "type": "PL 05-1/KK-TNCN",
        },
    ]

    sections = [
        {
            "id": "header",
            "title": "Thông tin chung",
            "indicators": ["ct15", "ct16", "ct17"],
        },
        {
            "id": "deducted_count",
            "title": "I. Số cá nhân đã khấu trừ thuế",
            "indicators": ["ct18", "ct19", "ct20"],
        },
        {
            "id": "taxable_income",
            "title": "II. Thu nhập chịu thuế trả cho cá nhân",
            "indicators": ["ct21", "ct22", "ct23", "ct24", "ct25"],
        },
        {
            "id": "income_deductible",
            "title": "III. Thu nhập thuộc diện khấu trừ thuế",
            "indicators": ["ct26", "ct27", "ct28"],
        },
        {
            "id": "tax_deducted",
            "title": "IV. Thuế TNCN đã khấu trừ",
            "indicators": ["ct29", "ct30", "ct31", "ct32"],
        },
    ]

    # -------------------------------------------------------------------------
    # compute_chi_tieu
    # -------------------------------------------------------------------------

    def compute_chi_tieu(self, doc):
        """
        Tính toán chỉ tiêu từ dữ liệu Salary Slip trong ERPNext.

        Ưu tiên dùng Salary Slip vì:
        - gross_pay = thu nhập chịu thuế
        - income_tax_deducted = thuế đã khấu trừ (component type = Deduction, is_income_tax = 1)
        """
        r = {}

        def _ct(name, auto_value, source):
            r[name] = {
                "auto_value": flt(auto_value),
                "label": CT_LABELS.get(name, name),
                "source": source,
            }

        company = doc.company
        from_date = doc.from_date
        to_date = doc.to_date

        # --- Query Salary Slip ---
        salary_data = self._query_salary_slip_summary(company, from_date, to_date)

        total_employees = salary_data.get("total_employees", 0)
        resident_employees = salary_data.get("resident_employees", 0)
        resident_with_contract = salary_data.get("resident_with_contract", 0)
        non_resident_employees = salary_data.get("non_resident_employees", 0)

        total_income = salary_data.get("total_income", 0)
        resident_income = salary_data.get("resident_income", 0)
        non_resident_income = salary_data.get("non_resident_income", 0)

        total_tax = salary_data.get("total_tax", 0)
        resident_tax = salary_data.get("resident_tax", 0)
        non_resident_tax = salary_data.get("non_resident_tax", 0)

        # --- Thông tin chung ---
        _ct("ct15", 0, "Mặc định: Không phân bổ (0=False)")
        _ct("ct16", total_employees, f"COUNT(DISTINCT employee) = {total_employees}")
        _ct("ct17", resident_with_contract, f"Cá nhân cư trú có HĐLĐ = {resident_with_contract}")

        # --- I. Số cá nhân đã khấu trừ ---
        deducted_count = resident_employees + non_resident_employees
        _ct("ct18", deducted_count, f"Tổng = {resident_employees} + {non_resident_employees}")
        _ct("ct19", resident_employees, f"Cư trú = {resident_employees}")
        _ct("ct20", non_resident_employees, f"Không cư trú = {non_resident_employees}")

        # --- II. Thu nhập chịu thuế ---
        _ct("ct21", total_income, f"Tổng = {_fmt(resident_income)} + {_fmt(non_resident_income)}")
        _ct("ct22", resident_income, f"Cư trú = {_fmt(resident_income)}")
        _ct("ct23", non_resident_income, f"Không cư trú = {_fmt(non_resident_income)}")
        _ct("ct24", 0, "Bảo hiểm nhân thọ nước ngoài (nhập tay)")
        _ct("ct25", 0, "Miễn theo Hợp đồng dầu khí (nhập tay)")

        # --- III. Thu nhập thuộc diện khấu trừ ---
        # Giả định: toàn bộ thu nhập đều thuộc diện khấu trừ
        _ct("ct26", total_income, f"[26] = [21] = {_fmt(total_income)}")
        _ct("ct27", resident_income, f"Cư trú = {_fmt(resident_income)}")
        _ct("ct28", non_resident_income, f"Không cư trú = {_fmt(non_resident_income)}")

        # --- IV. Thuế đã khấu trừ ---
        _ct("ct29", total_tax, f"Tổng = {_fmt(resident_tax)} + {_fmt(non_resident_tax)}")
        _ct("ct30", resident_tax, f"Cư trú = {_fmt(resident_tax)}")
        _ct("ct31", non_resident_tax, f"Không cư trú = {_fmt(non_resident_tax)}")
        _ct("ct32", 0, "Thuế trên bảo hiểm nhân thọ nước ngoài (nhập tay)")

        return r

    def _query_salary_slip_summary(self, company, from_date, to_date):
        """
        Query Salary Slip để lấy tổng hợp nhân viên, thu nhập, thuế.

        Returns dict với các key:
        - total_employees, resident_employees, non_resident_employees
        - resident_with_contract
        - total_income, resident_income, non_resident_income
        - total_tax, resident_tax, non_resident_tax
        """
        # Check if Salary Slip exists
        if not frappe.db.table_exists("tabSalary Slip"):
            return self._empty_salary_data()

        # Main query
        result = frappe.db.sql(
            """
            SELECT
                COUNT(DISTINCT ss.employee) as total_employees,
                SUM(ss.gross_pay) as total_income,
                SUM(COALESCE(
                    (SELECT SUM(sd.amount)
                     FROM `tabSalary Detail` sd
                     WHERE sd.parent = ss.name
                       AND sd.parentfield = 'deductions'
                       AND sd.is_income_tax_component = 1),
                    0
                )) as total_tax
            FROM `tabSalary Slip` ss
            WHERE ss.company = %s
              AND ss.posting_date BETWEEN %s AND %s
              AND ss.docstatus = 1
            """,
            (company, from_date, to_date),
            as_dict=True,
        )

        if not result or not result[0].get("total_employees"):
            return self._empty_salary_data()

        row = result[0]

        # For simplicity, assume all are residents with contracts
        # In production, you'd query Employee.is_resident and Employment Type
        return {
            "total_employees": int(row.get("total_employees") or 0),
            "resident_employees": int(row.get("total_employees") or 0),
            "non_resident_employees": 0,
            "resident_with_contract": int(row.get("total_employees") or 0),
            "total_income": flt(row.get("total_income") or 0),
            "resident_income": flt(row.get("total_income") or 0),
            "non_resident_income": 0,
            "total_tax": flt(row.get("total_tax") or 0),
            "resident_tax": flt(row.get("total_tax") or 0),
            "non_resident_tax": 0,
        }

    def _empty_salary_data(self):
        return {
            "total_employees": 0,
            "resident_employees": 0,
            "non_resident_employees": 0,
            "resident_with_contract": 0,
            "total_income": 0,
            "resident_income": 0,
            "non_resident_income": 0,
            "total_tax": 0,
            "resident_tax": 0,
            "non_resident_tax": 0,
        }

    # -------------------------------------------------------------------------
    # generate
    # -------------------------------------------------------------------------

    def generate(self, doc):
        """
        Generate full declaration data for preview/export.

        Returns:
            {
                "chi_tieu": {element_name: value, ...},
                "sources": {element_name: source_text, ...},
                "phu_luc": {
                    "PL05_1_TNCN": [...],  # Phân bổ thuế theo địa bàn
                }
            }
        """
        chi_tieu, sources = self._get_final_ct_values(doc)

        # Phụ lục: Phân bổ thuế theo địa bàn
        # Hiện tại trả về empty vì chưa implement logic phân bổ
        phu_luc = {
            "PL05_1_TNCN": [],
        }

        return {
            "chi_tieu": chi_tieu,
            "sources": sources,
            "phu_luc": phu_luc,
        }

    def _get_final_ct_values(self, doc):
        """
        Lấy giá trị chỉ tiêu cuối cùng, ưu tiên manual_value nếu có.
        """
        ct = {}
        sources = {}

        if doc.get("ct_values"):
            for row in doc.ct_values:
                val = flt(row.manual_value) if row.is_manual else flt(row.auto_value)
                ct[row.ct_name] = val
                sources[row.ct_name] = row.data_source or ""
        else:
            # Hot computation if not saved
            all_data = self.compute_chi_tieu(doc)
            for name, info in all_data.items():
                ct[name] = info["auto_value"]
                sources[name] = info["source"]

        return ct, sources


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _fmt(n):
    """Format số nguyên với dấu phân cách nghìn cho source notes."""
    return f"{flt(n):,.0f}"
