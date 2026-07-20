"""
Tờ khai thuế TNDN mẫu 03/TNDN — Quyết toán năm (TT80/2021, XSD v2.0.7).

Kỳ kê khai: quyết toán năm tài chính.

Cấu trúc chỉ tiêu theo XSD 03_TNDN_TT80_292.xsd:
─────────────────────────────────────────────────────────────
 A. LỢI NHUẬN KẾ TOÁN TRƯỚC THUẾ
 A1   Tổng lợi nhuận kế toán trước thuế TNDN
─────────────────────────────────────────────────────────────
 B. ĐIỀU CHỈNH TĂNG/GIẢM TỔNG LỢI NHUẬN
 B1   Điều chỉnh tăng (B1 = B2+B3+B4+B5+B6+B7)
 B2   Các khoản điều chỉnh tăng doanh thu
 B3   Chi phí của phần doanh thu điều chỉnh giảm
 B4   Các khoản chi không được trừ
 B5   Thuế thu nhập đã nộp ở nước ngoài
 B6   Điều chỉnh tăng do giao dịch liên kết
 B7   Các khoản điều chỉnh tăng khác
 B8   Điều chỉnh giảm (B8 = B9+B10+B11+B12)
 B9   Giảm trừ doanh thu đã tính thuế năm trước
 B10  Chi phí của phần doanh thu điều chỉnh tăng
 B11  Chi phí lãi vay kỳ trước chuyển sang (GDLK)
 B12  Các khoản điều chỉnh giảm khác
 B13  Tổng thu nhập chịu thuế (B13 = A1+B1-B8)
 B14  Thu nhập chịu thuế từ SXKD
 B15  Thu nhập chịu thuế từ chuyển nhượng BĐS
─────────────────────────────────────────────────────────────
 C. THUẾ TNDN TỪ HOẠT ĐỘNG SXKD
 C1   Thu nhập chịu thuế (C1 = B14)
 C2   Thu nhập miễn thuế
 C3   Chuyển lỗ và bù trừ (C3 = C3a+C3b)
 C3a  Lỗ từ SXKD được chuyển trong kỳ
 C3b  Lỗ từ BĐS bù trừ với lãi SXKD
 C4   Thu nhập tính thuế (C4 = C1-C2-C3)
 C5   Trích lập quỹ KHCN
 C6   TNTT sau trích quỹ KHCN (C6 = C4-C5 = C7+C8)
 C7   TNTT áp dụng thuế suất 15%/17%/20%
 C8   TNTT thuế suất không ưu đãi khác
 C8a  Thuế suất không ưu đãi khác (%)
 C9   Thuế TNDN từ SXKD (C9 = C7×20% + C8×C8a)
 C10  Thuế TNDN được ưu đãi (C10 = C11+C12+C13)
 C11  Thuế chênh lệch do thuế suất ưu đãi
 C12  Thuế TNDN được miễn trong kỳ
 C13  Thuế TNDN được giảm trong kỳ
 C14  Thuế miễn/giảm theo Hiệp định thuế
 C15  Thuế miễn/giảm theo từng thời kỳ
 C16  Thuế thu nhập đã nộp ở nước ngoài được trừ
 C17  Thuế TNDN phải nộp của SXKD (C17 = C9-C10-C14-C15-C16)
─────────────────────────────────────────────────────────────
 D. THUẾ TNDN TỪ CHUYỂN NHƯỢNG BĐS (nếu có)
 D1-D8: Tính toán riêng cho hoạt động BĐS
─────────────────────────────────────────────────────────────
 E. TỔNG THUẾ TNDN PHẢI NỘP
 E    Tổng thuế phải nộp (E = E1+E2+E5)
 E1   Thuế TNDN từ SXKD
 E2   Thuế từ chuyển nhượng BĐS (E2 = E3+E4)
 E3-E4, E5-E6: Chi tiết
─────────────────────────────────────────────────────────────
 G. THUẾ TNDN ĐÃ TẠM NỘP
 G    Tổng đã tạm nộp (G = G1+G2+G3+G4+G5)
 G1   Thuế nộp thừa kỳ trước chuyển sang
 G2   Thuế đã tạm nộp trong năm
 G3-G5: Chi tiết BĐS
─────────────────────────────────────────────────────────────
 H. CHÊNH LỆCH
 H1   Chênh lệch SXKD (H1 = E1+E5-G2)
 H2   Chênh lệch BĐS (H2 = E3-G4)
 H3   Chênh lệch CSHT (H3 = E4-G5)
─────────────────────────────────────────────────────────────
 I. THUẾ CÒN PHẢI NỘP
 I    Tổng còn phải nộp (I = E-G = I1+I2)
 I1   Thuế còn phải nộp từ SXKD
 I2   Thuế còn phải nộp từ BĐS
─────────────────────────────────────────────────────────────

Nguồn dữ liệu:
  - Lợi nhuận kế toán (A1): từ báo cáo P&L hoặc GL Entry TK 4212
  - Các khoản điều chỉnh (B2-B12): nhập tay
  - Lỗ chuyển kỳ (C3a): nhập tay từ declaration.prior_year_loss
  - Thuế suất: từ declaration.cit_rate (mặc định 20%)
  - Thuế đã tạm nộp (G2): từ declaration.cit_prepaid
"""

from frappe.utils import flt

from dcnet_apps.htkk.declarations.base import DeclarationConfig, register
from dcnet_apps.htkk.data_queries import get_income_expense_by_account


# ---------------------------------------------------------------------------
# Nhãn mô tả cho từng chỉ tiêu (hiển thị trong ct_values table)
# ---------------------------------------------------------------------------

CT_LABELS = {
    "ctA1": "Tổng lợi nhuận kế toán trước thuế TNDN",

    "ctB1": "Điều chỉnh tăng tổng lợi nhuận (B1=B2+B3+B4+B5+B6+B7)",
    "ctB2": "Các khoản điều chỉnh tăng doanh thu",
    "ctB3": "Chi phí của phần doanh thu điều chỉnh giảm",
    "ctB4": "Các khoản chi không được trừ khi xác định TNCT",
    "ctB5": "Thuế thu nhập đã nộp cho phần thu nhập ở nước ngoài",
    "ctB6": "Điều chỉnh tăng lợi nhuận do giao dịch liên kết",
    "ctB7": "Các khoản điều chỉnh làm tăng lợi nhuận trước thuế khác",
    "ctB8": "Điều chỉnh giảm tổng lợi nhuận (B8=B9+B10+B11+B12)",
    "ctB9": "Giảm trừ các khoản doanh thu đã tính thuế năm trước",
    "ctB10": "Chi phí của phần doanh thu điều chỉnh tăng",
    "ctB11": "Chi phí lãi vay không được trừ kỳ trước chuyển sang (GDLK)",
    "ctB12": "Các khoản điều chỉnh làm giảm lợi nhuận trước thuế khác",
    "ctB13": "Tổng thu nhập chịu thuế (B13=A1+B1-B8)",
    "ctB14": "Thu nhập chịu thuế từ hoạt động SXKD",
    "ctB15": "Thu nhập chịu thuế từ hoạt động chuyển nhượng BĐS",

    "ctC1": "Thu nhập chịu thuế (C1=B14)",
    "ctC2": "Thu nhập miễn thuế",
    "ctC3": "Chuyển lỗ và bù trừ lãi, lỗ (C3=C3a+C3b)",
    "ctC3a": "Lỗ từ hoạt động SXKD được chuyển trong kỳ",
    "ctC3b": "Lỗ từ BĐS được bù trừ với lãi SXKD",
    "ctC4": "Thu nhập tính thuế (C4=C1-C2-C3)",
    "ctC5": "Trích lập quỹ khoa học công nghệ",
    "ctC6": "TNTT sau khi đã trích lập quỹ KHCN (C6=C4-C5)",
    "ctC7": "Thu nhập tính thuế áp dụng thuế suất phổ thông",
    "ctC7_thueSuat": "Thuế suất áp dụng (%)",
    "ctC8": "TNTT thuế suất không ưu đãi khác",
    "ctC8a": "Thuế suất không ưu đãi khác (%)",
    "ctC9": "Thuế TNDN từ SXKD tính theo thuế suất không ưu đãi",
    "ctC10": "Thuế TNDN được ưu đãi (C10=C11+C12+C13)",
    "ctC11": "Thuế chênh lệch do áp dụng thuế suất ưu đãi",
    "ctC12": "Thuế TNDN được miễn trong kỳ",
    "ctC13": "Thuế TNDN được giảm trong kỳ",
    "ctC14": "Thuế miễn, giảm theo Hiệp định thuế",
    "ctC15": "Thuế miễn, giảm theo từng thời kỳ",
    "ctC16": "Thuế thu nhập đã nộp ở nước ngoài được trừ",
    "ctC17": "Thuế TNDN phải nộp của hoạt động SXKD (C17=C9-C10-C14-C15-C16)",

    "ctD1": "Thu nhập chịu thuế từ BĐS (D1=B15)",
    "ctD2": "Lỗ từ BĐS được chuyển trong kỳ",
    "ctD3": "Thu nhập tính thuế BĐS (D3=D1-D2)",
    "ctD4": "Trích lập quỹ KHCN (BĐS)",
    "ctD5": "TNTT sau trích quỹ KHCN (D5=D3-D4)",
    "ctD6": "Thuế TNDN phải nộp của BĐS trong kỳ",
    "ctD7": "Thuế chênh lệch do thuế suất ưu đãi nhà ở xã hội",
    "ctD8": "Thuế TNDN của BĐS còn phải nộp (D8=D6-D7)",

    "ctE": "Số thuế TNDN phải nộp quyết toán (E=E1+E2+E5)",
    "ctE1": "Thuế TNDN của hoạt động SXKD",
    "ctE2": "Thuế TNDN từ chuyển nhượng BĐS (E2=E3+E4)",
    "ctE3": "Thuế TNDN từ chuyển nhượng BĐS",
    "ctE4": "Thuế TNDN từ chuyển nhượng CSHT/nhà theo tiến độ",
    "ctE5": "Thuế TNDN phải nộp khác",
    "ctE6": "Trong đó thuế từ xử lý Quỹ phát triển KHCN",

    "ctG": "Số thuế TNDN đã tạm nộp (G=G1+G2+G3+G4+G5)",
    "ctG1": "Thuế nộp thừa kỳ trước chuyển sang kỳ này",
    "ctG2": "Thuế TNDN đã tạm nộp trong năm",
    "ctG3": "Thuế nộp thừa kỳ trước chuyển sang (BĐS)",
    "ctG4": "Thuế đã tạm nộp trong năm (BĐS)",
    "ctG5": "Thuế đã tạm nộp (CSHT/nhà theo tiến độ)",

    "ctH1": "Chênh lệch thuế phải nộp và đã tạm nộp của SXKD (H1=E1+E5-G2)",
    "ctH2": "Chênh lệch thuế phải nộp và đã tạm nộp của BĐS (H2=E3-G4)",
    "ctH3": "Chênh lệch thuế phải nộp và đã tạm nộp CSHT (H3=E4-G5)",

    "ctI": "Thuế TNDN còn phải nộp (I=E-G)",
    "ctI1": "Thuế TNDN còn phải nộp của hoạt động SXKD",
    "ctI2": "Thuế TNDN còn phải nộp của hoạt động BĐS",
}


@register
class CIT03TNDN(DeclarationConfig):
    """
    Tờ khai thuế TNDN mẫu 03/TNDN — Quyết toán năm.
    """

    # === METADATA ===
    code = "03/TNDN"
    name = "Tờ khai thuế thu nhập doanh nghiệp tạm tính"
    short_name = "TNDN tạm tính"
    xsd_file = "03_TNDN_TT80_292.xsd"
    period = "yearly"  # quyết toán năm
    circular = "TT80/2021/TT-BTC"
    has_appendices = False

    # === FRONTEND CONFIG ===
    title = "Tờ khai thuế thu nhập doanh nghiệp tạm tính"
    subtitle = "(Dành cho doanh nghiệp kê khai thuế TNDN tạm tính theo quý)"

    appendices = []  # 03/TNDN không có phụ lục

    sections = [
        {
            "id": "header",
            "title": "Thông tin chung",
            "indicators": ["ct04_ma", "ct04_ten", "ct05"],
        },
        {
            "id": "profit",
            "title": "A. LỢI NHUẬN KẾ TOÁN TRƯỚC THUẾ TNDN",
            "indicators": ["ctA1"],
        },
        {
            "id": "adjustments",
            "title": "B. ĐIỀU CHỈNH TĂNG GIẢM LỢI NHUẬN",
            "subsections": [
                {
                    "id": "increase",
                    "title": "Điều chỉnh tăng",
                    "indicators": ["ctB1", "ctB2", "ctB3", "ctB4", "ctB5", "ctB6", "ctB7"],
                    "computed_first": True,
                },
                {
                    "id": "decrease",
                    "title": "Điều chỉnh giảm",
                    "indicators": ["ctB8", "ctB9", "ctB10", "ctB11", "ctB12"],
                    "computed_first": True,
                },
                {
                    "id": "taxable_income",
                    "title": "Tổng thu nhập chịu thuế",
                    "indicators": ["ctB13", "ctB14", "ctB15"],
                    "computed": True,
                },
            ],
        },
        {
            "id": "cit_sxkd",
            "title": "C. XÁC ĐỊNH THUẾ TNDN TỪ HOẠT ĐỘNG SXKD",
            "subsections": [
                {
                    "id": "taxable",
                    "title": "Thu nhập chịu thuế và miễn thuế",
                    "indicators": ["ctC1", "ctC2", "ctC3", "ctC3a", "ctC3b", "ctC4"],
                },
                {
                    "id": "deductions",
                    "title": "Trích lập quỹ KH&CN",
                    "indicators": ["ctC5", "ctC6", "ctC7_thuNhap", "ctC8", "ctC8a"],
                },
                {
                    "id": "tax_calc",
                    "title": "Tính thuế TNDN",
                    "indicators": ["ctC9", "ctC10", "ctC11", "ctC12", "ctC13", "ctC14", "ctC15", "ctC16", "ctC17"],
                    "highlight": True,
                },
            ],
        },
        {
            "id": "cit_bds",
            "title": "D. XÁC ĐỊNH THUẾ TNDN TỪ CHUYỂN NHƯỢNG BĐS",
            "indicators": ["ctD1", "ctD2", "ctD3", "ctD4", "ctD5", "ctD6", "ctD7", "ctD8"],
        },
        {
            "id": "total_tax",
            "title": "E. TỔNG SỐ THUẾ TNDN PHẢI NỘP",
            "indicators": ["ctE", "ctE1", "ctE2", "ctE3", "ctE4", "ctE5"],
            "computed": True,
            "highlight": True,
        },
        {
            "id": "prepaid",
            "title": "G. SỐ THUẾ TNDN ĐÃ TẠM NỘP TRONG NĂM",
            "indicators": ["ctG", "ctG1", "ctG2", "ctG3", "ctG4", "ctG5"],
        },
        {
            "id": "payable",
            "title": "H. SỐ THUẾ TNDN CÒN PHẢI NỘP / NỘP THỪA",
            "indicators": ["ctH1", "ctH2", "ctH3"],
            "computed": True,
            "highlight": True,
        },
    ]

    # === DRIVER METHODS ===

    def compute_chi_tieu(self, doc):
        """
        Tính toán tất cả chỉ tiêu cho tờ khai 03/TNDN theo TT80.

        Mỗi chỉ tiêu có:
          - auto_value: giá trị tính toán tự động từ chứng từ
          - label: tên mô tả hiển thị
          - source: giải thích nguồn dữ liệu và cách tính

        Args:
            doc: HTKK Declaration document

        Returns:
            dict: {ct_name: {"auto_value": float, "label": str, "source": str}}
        """
        company = doc.company
        from_date = doc.from_date
        to_date = doc.to_date
        finance_book = getattr(doc, "finance_book", None)

        # ── Helper ghi kết quả ──────────────────────────────────────────────
        r = {}

        def _ct(name, auto_value, source):
            r[name] = {
                "auto_value": flt(auto_value),
                "label": CT_LABELS.get(name, name),
                "source": source,
            }

        # ══════════════════════════════════════════════════════════════════
        # A. LỢI NHUẬN KẾ TOÁN TRƯỚC THUẾ
        # ══════════════════════════════════════════════════════════════════

        # A1: Lấy từ P&L hoặc nhập tay
        accounting_profit = flt(getattr(doc, "accounting_profit", 0))

        if accounting_profit != 0:
            ctA1_val = accounting_profit
            ctA1_src = f"Nhập tay = {_fmt(ctA1_val)}đ"
        else:
            # Tính từ GL: Revenue (5xx, 7xx) - Expense (6xx, 8xx except 821)
            pnl = _calculate_profit_from_gl(company, from_date, to_date, finance_book)
            ctA1_val = pnl["profit_before_tax"]
            ctA1_src = (
                f"Từ GL Entry: Doanh thu {_fmt(pnl['revenue'])}đ - "
                f"Chi phí {_fmt(pnl['expense'])}đ = {_fmt(ctA1_val)}đ"
            )

        _ct("ctA1", ctA1_val, ctA1_src)

        # ══════════════════════════════════════════════════════════════════
        # B. ĐIỀU CHỈNH TĂNG/GIẢM
        # ══════════════════════════════════════════════════════════════════

        # B2-B7: Điều chỉnh tăng (nhập tay, mặc định 0)
        ctB2 = 0  # Các khoản điều chỉnh tăng doanh thu
        ctB3 = 0  # Chi phí của phần doanh thu điều chỉnh giảm
        ctB4 = 0  # Các khoản chi không được trừ
        ctB5 = 0  # Thuế thu nhập đã nộp ở nước ngoài
        ctB6 = 0  # Điều chỉnh tăng do giao dịch liên kết
        ctB7 = 0  # Các khoản điều chỉnh tăng khác

        _ct("ctB2", ctB2, "Nhập tay. Mặc định 0.")
        _ct("ctB3", ctB3, "Nhập tay. Mặc định 0.")
        _ct("ctB4", ctB4, "Nhập tay. Mặc định 0.")
        _ct("ctB5", ctB5, "Nhập tay. Mặc định 0.")
        _ct("ctB6", ctB6, "Nhập tay. Mặc định 0.")
        _ct("ctB7", ctB7, "Nhập tay. Mặc định 0.")

        # B1 = B2+B3+B4+B5+B6+B7
        ctB1_val = ctB2 + ctB3 + ctB4 + ctB5 + ctB6 + ctB7
        _ct("ctB1", ctB1_val, f"[B2]+[B3]+[B4]+[B5]+[B6]+[B7] = {_fmt(ctB1_val)}đ")

        # B9-B12: Điều chỉnh giảm (nhập tay, mặc định 0)
        ctB9 = 0   # Giảm trừ doanh thu đã tính thuế năm trước
        ctB10 = 0  # Chi phí của phần doanh thu điều chỉnh tăng
        ctB11 = 0  # Chi phí lãi vay kỳ trước chuyển sang
        ctB12 = 0  # Các khoản điều chỉnh giảm khác

        _ct("ctB9", ctB9, "Nhập tay. Mặc định 0.")
        _ct("ctB10", ctB10, "Nhập tay. Mặc định 0.")
        _ct("ctB11", ctB11, "Nhập tay. Mặc định 0.")
        _ct("ctB12", ctB12, "Nhập tay. Mặc định 0.")

        # B8 = B9+B10+B11+B12
        ctB8_val = ctB9 + ctB10 + ctB11 + ctB12
        _ct("ctB8", ctB8_val, f"[B9]+[B10]+[B11]+[B12] = {_fmt(ctB8_val)}đ")

        # B13 = A1 + B1 - B8
        ctB13_val = ctA1_val + ctB1_val - ctB8_val
        _ct("ctB13", ctB13_val,
            f"[A1]+[B1]-[B8] = {_fmt(ctA1_val)}+{_fmt(ctB1_val)}-{_fmt(ctB8_val)} = {_fmt(ctB13_val)}đ")

        # B14 = B13 (giả định toàn bộ là SXKD, không có BĐS)
        ctB14_val = max(0, ctB13_val)
        _ct("ctB14", ctB14_val,
            f"Thu nhập chịu thuế từ SXKD = {_fmt(ctB14_val)}đ (giả định không có hoạt động BĐS)")

        # B15 = 0 (mặc định không có BĐS)
        ctB15_val = 0
        _ct("ctB15", ctB15_val, "Thu nhập từ BĐS = 0 (nhập tay nếu có)")

        # ══════════════════════════════════════════════════════════════════
        # C. THUẾ TNDN TỪ HOẠT ĐỘNG SXKD
        # ══════════════════════════════════════════════════════════════════

        # C1 = B14
        ctC1_val = ctB14_val
        _ct("ctC1", ctC1_val, f"[C1] = [B14] = {_fmt(ctC1_val)}đ")

        # C2: Thu nhập miễn thuế (nhập tay)
        ctC2_val = 0
        _ct("ctC2", ctC2_val, "Thu nhập miễn thuế = 0 (nhập tay nếu có)")

        # C3a: Lỗ từ SXKD được chuyển trong kỳ
        ctC3a_val = flt(getattr(doc, "prior_year_loss", 0))
        _ct("ctC3a", ctC3a_val,
            f"Lỗ các năm trước chuyển sang = {_fmt(ctC3a_val)}đ (từ trường nhập tay)")

        # C3b: Lỗ từ BĐS bù trừ
        ctC3b_val = 0
        _ct("ctC3b", ctC3b_val, "Lỗ từ BĐS bù trừ với lãi SXKD = 0 (nhập tay nếu có)")

        # C3 = C3a + C3b
        ctC3_val = ctC3a_val + ctC3b_val
        _ct("ctC3", ctC3_val, f"[C3a]+[C3b] = {_fmt(ctC3a_val)}+{_fmt(ctC3b_val)} = {_fmt(ctC3_val)}đ")

        # C4 = C1 - C2 - C3
        ctC4_val = ctC1_val - ctC2_val - ctC3_val
        _ct("ctC4", ctC4_val,
            f"[C1]-[C2]-[C3] = {_fmt(ctC1_val)}-{_fmt(ctC2_val)}-{_fmt(ctC3_val)} = {_fmt(ctC4_val)}đ")

        # C5: Trích lập quỹ KHCN
        ctC5_val = 0
        _ct("ctC5", ctC5_val, "Trích lập quỹ KHCN = 0 (nhập tay nếu có)")

        # C6 = C4 - C5
        ctC6_val = max(0, ctC4_val - ctC5_val)
        _ct("ctC6", ctC6_val, f"[C4]-[C5] = {_fmt(ctC4_val)}-{_fmt(ctC5_val)} = {_fmt(ctC6_val)}đ")

        # C7: TNTT áp dụng thuế suất phổ thông (20%)
        ctC7_val = ctC6_val
        _ct("ctC7", ctC7_val, f"TNTT thuế suất 20% = {_fmt(ctC7_val)}đ")

        # Thuế suất áp dụng
        cit_rate = flt(getattr(doc, "cit_rate", 20))
        _ct("ctC7_thueSuat", cit_rate, f"Thuế suất = {cit_rate}%")

        # C8: TNTT thuế suất không ưu đãi khác
        ctC8_val = 0
        _ct("ctC8", ctC8_val, "TNTT thuế suất khác = 0 (nhập tay nếu có)")

        # C8a: Thuế suất không ưu đãi khác
        ctC8a_val = 0
        _ct("ctC8a", ctC8a_val, "Thuế suất khác = 0%")

        # C9 = C7 × thuế suất + C8 × C8a
        ctC9_val = ctC7_val * cit_rate / 100 + ctC8_val * ctC8a_val / 100
        _ct("ctC9", ctC9_val,
            f"[C7]×{cit_rate}% + [C8]×{ctC8a_val}% = "
            f"{_fmt(ctC7_val)}×{cit_rate}% + {_fmt(ctC8_val)}×{ctC8a_val}% = {_fmt(ctC9_val)}đ")

        # C10-C16: Các khoản ưu đãi/miễn/giảm (mặc định 0)
        ctC11_val = 0
        ctC12_val = 0
        ctC13_val = 0
        ctC10_val = ctC11_val + ctC12_val + ctC13_val
        ctC14_val = 0
        ctC15_val = 0
        ctC16_val = 0

        _ct("ctC11", ctC11_val, "Thuế chênh lệch do thuế suất ưu đãi = 0")
        _ct("ctC12", ctC12_val, "Thuế TNDN được miễn trong kỳ = 0")
        _ct("ctC13", ctC13_val, "Thuế TNDN được giảm trong kỳ = 0")
        _ct("ctC10", ctC10_val, f"[C11]+[C12]+[C13] = {_fmt(ctC10_val)}đ")
        _ct("ctC14", ctC14_val, "Thuế miễn/giảm theo Hiệp định thuế = 0")
        _ct("ctC15", ctC15_val, "Thuế miễn/giảm theo từng thời kỳ = 0")
        _ct("ctC16", ctC16_val, "Thuế đã nộp ở nước ngoài được trừ = 0")

        # C17 = C9 - C10 - C14 - C15 - C16
        ctC17_val = max(0, ctC9_val - ctC10_val - ctC14_val - ctC15_val - ctC16_val)
        _ct("ctC17", ctC17_val,
            f"[C9]-[C10]-[C14]-[C15]-[C16] = "
            f"{_fmt(ctC9_val)}-{_fmt(ctC10_val)}-{_fmt(ctC14_val)}-{_fmt(ctC15_val)}-{_fmt(ctC16_val)} "
            f"= {_fmt(ctC17_val)}đ")

        # ══════════════════════════════════════════════════════════════════
        # D. THUẾ TNDN TỪ CHUYỂN NHƯỢNG BĐS (mặc định 0)
        # ══════════════════════════════════════════════════════════════════

        ctD1_val = ctB15_val
        _ct("ctD1", ctD1_val, f"[D1] = [B15] = {_fmt(ctD1_val)}đ")

        ctD2_val = 0
        _ct("ctD2", ctD2_val, "Lỗ từ BĐS được chuyển trong kỳ = 0")

        ctD3_val = ctD1_val - ctD2_val
        _ct("ctD3", ctD3_val, f"[D1]-[D2] = {_fmt(ctD1_val)}-{_fmt(ctD2_val)} = {_fmt(ctD3_val)}đ")

        ctD4_val = 0
        _ct("ctD4", ctD4_val, "Trích lập quỹ KHCN (BĐS) = 0")

        ctD5_val = ctD3_val - ctD4_val
        _ct("ctD5", ctD5_val, f"[D3]-[D4] = {_fmt(ctD3_val)}-{_fmt(ctD4_val)} = {_fmt(ctD5_val)}đ")

        ctD6_val = max(0, ctD5_val * 20 / 100)  # Thuế suất BĐS = 20%
        _ct("ctD6", ctD6_val, f"[D5]×20% = {_fmt(ctD5_val)}×20% = {_fmt(ctD6_val)}đ")

        ctD7_val = 0
        _ct("ctD7", ctD7_val, "Thuế chênh lệch ưu đãi nhà ở xã hội = 0")

        ctD8_val = ctD6_val - ctD7_val
        _ct("ctD8", ctD8_val, f"[D6]-[D7] = {_fmt(ctD6_val)}-{_fmt(ctD7_val)} = {_fmt(ctD8_val)}đ")

        # ══════════════════════════════════════════════════════════════════
        # E. TỔNG THUẾ TNDN PHẢI NỘP
        # ══════════════════════════════════════════════════════════════════

        ctE1_val = ctC17_val
        _ct("ctE1", ctE1_val, f"Thuế TNDN từ SXKD = [C17] = {_fmt(ctE1_val)}đ")

        ctE3_val = ctD8_val
        _ct("ctE3", ctE3_val, f"Thuế TNDN từ BĐS = [D8] = {_fmt(ctE3_val)}đ")

        ctE4_val = 0
        _ct("ctE4", ctE4_val, "Thuế từ CSHT/nhà theo tiến độ = 0")

        ctE2_val = ctE3_val + ctE4_val
        _ct("ctE2", ctE2_val, f"[E3]+[E4] = {_fmt(ctE3_val)}+{_fmt(ctE4_val)} = {_fmt(ctE2_val)}đ")

        ctE5_val = 0
        _ct("ctE5", ctE5_val, "Thuế TNDN phải nộp khác = 0")

        ctE6_val = 0
        _ct("ctE6", ctE6_val, "Thuế từ xử lý Quỹ KHCN = 0")

        ctE_val = ctE1_val + ctE2_val + ctE5_val
        _ct("ctE", ctE_val,
            f"[E1]+[E2]+[E5] = {_fmt(ctE1_val)}+{_fmt(ctE2_val)}+{_fmt(ctE5_val)} = {_fmt(ctE_val)}đ")

        # ══════════════════════════════════════════════════════════════════
        # G. THUẾ TNDN ĐÃ TẠM NỘP
        # ══════════════════════════════════════════════════════════════════

        ctG1_val = 0
        _ct("ctG1", ctG1_val, "Thuế nộp thừa kỳ trước chuyển sang = 0 (nhập tay nếu có)")

        ctG2_val = flt(getattr(doc, "cit_prepaid", 0))
        _ct("ctG2", ctG2_val, f"Thuế đã tạm nộp trong năm = {_fmt(ctG2_val)}đ (từ trường nhập tay)")

        ctG3_val = 0
        _ct("ctG3", ctG3_val, "Thuế nộp thừa kỳ trước (BĐS) = 0")

        ctG4_val = 0
        _ct("ctG4", ctG4_val, "Thuế đã tạm nộp (BĐS) = 0")

        ctG5_val = 0
        _ct("ctG5", ctG5_val, "Thuế đã tạm nộp (CSHT) = 0")

        ctG_val = ctG1_val + ctG2_val + ctG3_val + ctG4_val + ctG5_val
        _ct("ctG", ctG_val,
            f"[G1]+[G2]+[G3]+[G4]+[G5] = {_fmt(ctG_val)}đ")

        # ══════════════════════════════════════════════════════════════════
        # H. CHÊNH LỆCH
        # ══════════════════════════════════════════════════════════════════

        ctH1_val = ctE1_val + ctE5_val - ctG2_val
        _ct("ctH1", ctH1_val,
            f"[E1]+[E5]-[G2] = {_fmt(ctE1_val)}+{_fmt(ctE5_val)}-{_fmt(ctG2_val)} = {_fmt(ctH1_val)}đ")

        ctH2_val = ctE3_val - ctG4_val
        _ct("ctH2", ctH2_val, f"[E3]-[G4] = {_fmt(ctE3_val)}-{_fmt(ctG4_val)} = {_fmt(ctH2_val)}đ")

        ctH3_val = ctE4_val - ctG5_val
        _ct("ctH3", ctH3_val, f"[E4]-[G5] = {_fmt(ctE4_val)}-{_fmt(ctG5_val)} = {_fmt(ctH3_val)}đ")

        # ══════════════════════════════════════════════════════════════════
        # I. THUẾ CÒN PHẢI NỘP
        # ══════════════════════════════════════════════════════════════════

        ctI_val = ctE_val - ctG_val
        _ct("ctI", ctI_val, f"[E]-[G] = {_fmt(ctE_val)}-{_fmt(ctG_val)} = {_fmt(ctI_val)}đ")

        # I1: Thuế còn phải nộp SXKD (= E1 + E5 - G1 - G2)
        ctI1_val = ctE1_val + ctE5_val - ctG1_val - ctG2_val
        _ct("ctI1", ctI1_val,
            f"[E1]+[E5]-[G1]-[G2] = {_fmt(ctE1_val)}+{_fmt(ctE5_val)}-{_fmt(ctG1_val)}-{_fmt(ctG2_val)} "
            f"= {_fmt(ctI1_val)}đ")

        # I2: Thuế còn phải nộp BĐS
        ctI2_val = ctE2_val - ctG3_val - ctG4_val - ctG5_val
        _ct("ctI2", ctI2_val,
            f"[E2]-[G3]-[G4]-[G5] = {_fmt(ctE2_val)}-{_fmt(ctG3_val)}-{_fmt(ctG4_val)}-{_fmt(ctG5_val)} "
            f"= {_fmt(ctI2_val)}đ")

        return r

    def generate(self, doc):
        """
        Tạo toàn bộ dữ liệu cho tờ khai 03/TNDN (chỉ tiêu).

        Ưu tiên đọc từ ct_values child table (có manual override).
        Nếu ct_values chưa có, tính toán tự động.

        Returns:
            dict: {
                "chi_tieu": {element_name: value, ...},
                "sources": {element_name: source_text, ...},
            }
        """
        chi_tieu, sources = self._get_final_ct_values(doc)

        return {"chi_tieu": chi_tieu, "sources": sources, "phu_luc": {}}

    def _get_final_ct_values(self, doc):
        """
        Lấy giá trị cuối cùng và nguồn mô tả của từng CT.
        Ưu tiên manual_value nếu is_manual.

        Nếu ct_values chưa có, tính toán tự động từ chứng từ.
        """
        ct = {}
        sources = {}

        if doc.get("ct_values"):
            for row in doc.ct_values:
                val = flt(row.manual_value) if row.is_manual else flt(row.auto_value)
                ct[row.ct_name] = val
                sources[row.ct_name] = row.data_source or ""
        else:
            # Tính toán nóng nếu chưa được lưu
            all_data = self.compute_chi_tieu(doc)
            for name, info in all_data.items():
                ct[name] = info["auto_value"]
                sources[name] = info["source"]

        return ct, sources


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _calculate_profit_from_gl(company, from_date, to_date, finance_book=None):
    """
    Tính lợi nhuận kế toán trước thuế từ GL Entry.

    Công thức: Revenue (5xx, 7xx) - Expense (6xx, 8xx trừ 821)

    Returns:
        dict: {"revenue": x, "expense": y, "profit_before_tax": x - y}
    """
    balances = get_income_expense_by_account(company, from_date, to_date, finance_book)

    revenue = 0
    expense = 0

    for acc_num, amount in balances.items():
        if not acc_num:
            continue

        prefix = acc_num[0] if len(acc_num) >= 1 else ""

        if prefix in ("5", "7"):
            # Revenue: 511, 515, 521, 711, etc.
            revenue += amount
        elif prefix in ("6", "8"):
            # Expense: 632, 641, 642, 811, etc.
            # Exclude 821 (thuế TNDN) - không tính vào chi phí trước thuế
            if not acc_num.startswith("821"):
                expense += amount

    return {
        "revenue": revenue,
        "expense": expense,
        "profit_before_tax": revenue - expense,
    }


def _fmt(n):
    """Format số nguyên với dấu phân cách nghìn cho source notes."""
    return f"{flt(n):,.0f}"


