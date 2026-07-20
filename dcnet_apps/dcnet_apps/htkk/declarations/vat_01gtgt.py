"""
Tờ khai thuế GTGT mẫu 01/GTGT — Phương pháp khấu trừ (TT80/2021, XSD v2.1.2).

Kỳ kê khai: hàng tháng hoặc hàng quý.

Cấu trúc chỉ tiêu theo XSD 01_GTGT_TT80_283.xsd:
─────────────────────────────────────────────────────────────
 CT22  Thuế GTGT còn khấu trừ kỳ trước (nhập tay)
 CT23  Giá trị HHDV mua vào (chưa thuế) — từ Purchase Invoices
 CT24  Thuế GTGT của HHDV mua vào = PI trong nước + CT24a
 CT23a Trong đó: hàng hóa, dịch vụ nhập khẩu (giá trị) — nhập tay
 CT24a Trong đó: thuế GTGT hàng nhập khẩu — từ TK chọn hoặc nhập tay
 CT25  Thuế GTGT mua vào được khấu trừ kỳ này (mặc định = CT24)
 CT26  Doanh thu HHDV bán ra không chịu thuế GTGT (KCT)
 ─── Nhóm HHDVBRaChiuThueGTGT ─────────────────────────────
 CT27  Tổng giá trị HHDV bán ra chịu thuế = [29]+[30]+[32]+[32a]
 CT28  Tổng thuế GTGT của HHDV bán ra chịu thuế = [31]+[33]
 ───────────────────────────────────────────────────────────
 CT29  Doanh thu thuế suất 0% (hàng xuất khẩu)
 ─── Nhóm HHDVBRaChiuTSuat5 ────────────────────────────────
 CT30  Doanh thu 5%
 CT31  Thuế GTGT 5%
 ─── Nhóm HHDVBRaChiuTSuat10 ───────────────────────────────
 CT32  Doanh thu 10%
 CT33  Thuế GTGT 10%
 ───────────────────────────────────────────────────────────
 CT32a Doanh thu hàng hóa "không tính thuế" (VD: 8% NĐ44/NĐ15)
       Lưu ý: VAT của ct32a KHÔNG nằm trong ct28/ct35 theo XSD.
       Cần khai thêm phụ lục PL01-3 cho hàng 8% (chưa implement).
 ─── Nhóm TongDThuVaThueGTGT ────────────────────────────────
 CT34  Tổng doanh thu = [26]+[27]
 CT35  Tổng thuế GTGT bán ra = [28]
 ───────────────────────────────────────────────────────────
 CT36  Thuế GTGT phát sinh trong kỳ = [35]−[25]
 CT37  Điều chỉnh GIẢM thuế GTGT còn được khấu trừ kỳ trước
 CT38  Điều chỉnh TĂNG thuế GTGT còn được khấu trừ kỳ trước
 CT39a Thuế GTGT nhận bàn giao được khấu trừ kỳ này (nhập tay)
 CT40a Thuế phải nộp của HĐSXKD = max(0, [36]−[22]+[37]−[38]−[39a])
 CT40b Bù trừ thuế GTGT dự án đầu tư (nhập tay, ≤ CT40a)
 CT40  Thuế GTGT còn phải nộp = [40a]−[40b]
 CT41  Thuế GTGT chưa khấu trừ hết = abs(net) nếu net < 0
 CT42  Tổng số thuế GTGT đề nghị hoàn (nhập tay)
 CT43  Thuế GTGT còn được khấu trừ chuyển kỳ sau = [41]−[42]
─────────────────────────────────────────────────────────────

Nguồn dữ liệu:
  - Output VAT: Sales Invoices (item-level, 2-layer fallback)
  - Input VAT domestic: Purchase Invoices (item-level, phân biệt TSCĐ vs HHDV)
  - Input VAT import (CT24a): GL JE trên TK do user chọn, hoặc nhập tay
  - Các giá trị nhập tay: vat_carried_forward, import_goods_value,
    import_vat_amount, received_vat_credit, investment_vat_offset,
    vat_refund_requested, adjustments table
"""

from frappe.utils import flt, formatdate

from dcnet_apps.htkk.declarations.base import DeclarationConfig, register
from dcnet_apps.htkk.data_queries import (
    VAT_EXEMPT,
    get_import_vat_from_account,
    get_purchase_invoices,
    get_sales_invoices,
)

# ---------------------------------------------------------------------------
# Nhãn mô tả cho từng chỉ tiêu (hiển thị trong ct_values table)
# ---------------------------------------------------------------------------

CT_LABELS = {
    "ct21":  "Không phát sinh hoạt động MHHDV trong kỳ",
    "ct22":  "Thuế GTGT còn khấu trừ kỳ trước chuyển sang",
    "ct23":  "Giá trị HHDV mua vào phát sinh trong kỳ",
    "ct23a": "Trong đó: HHDV nhập khẩu (giá trị, chưa thuế)",
    "ct24":  "Thuế GTGT HHDV mua vào phát sinh trong kỳ",
    "ct24a": "Trong đó: thuế GTGT hàng nhập khẩu",
    "ct25":  "Thuế GTGT được khấu trừ kỳ này",
    "ct26":  "Doanh thu HHDV bán ra không chịu thuế GTGT (KCT)",
    "ct27":  "Tổng giá trị HHDV bán ra chịu thuế ([29]+[30]+[32]+[32a])",
    "ct28":  "Tổng thuế GTGT HHDV bán ra chịu thuế ([31]+[33])",
    "ct29":  "Hàng hoá, dịch vụ xuất khẩu — thuế suất 0%",
    "ct30":  "Hàng hoá, dịch vụ chịu thuế suất 5% — giá trị",
    "ct31":  "Hàng hoá, dịch vụ chịu thuế suất 5% — thuế GTGT",
    "ct32":  "Hàng hoá, dịch vụ chịu thuế suất 10% — giá trị",
    "ct33":  "Hàng hoá, dịch vụ chịu thuế suất 10% — thuế GTGT",
    "ct32a": "HHDV bán ra không tính thuế (8% NĐ44/NĐ15) — giá trị",
    "ct34":  "Tổng doanh thu HHDV bán ra ([26]+[27])",
    "ct35":  "Tổng thuế GTGT bán ra ([28])",
    "ct36":  "Thuế GTGT phát sinh trong kỳ ([35]−[25])",
    "ct37":  "Điều chỉnh GIẢM thuế còn khấu trừ kỳ trước",
    "ct38":  "Điều chỉnh TĂNG thuế còn khấu trừ kỳ trước",
    "ct39a": "Thuế GTGT nhận bàn giao được khấu trừ kỳ này",
    "ct40a": "Thuế phải nộp của HĐSXKD (trước bù trừ đầu tư)",
    "ct40b": "Bù trừ thuế GTGT dự án đầu tư (≤ CT40a)",
    "ct40":  "Thuế GTGT còn phải nộp của HĐSXKD ([40a]−[40b])",
    "ct41":  "Thuế GTGT chưa khấu trừ hết kỳ này",
    "ct42":  "Tổng số thuế GTGT đề nghị hoàn kỳ này",
    "ct43":  "Thuế GTGT còn được khấu trừ chuyển kỳ sau ([41]−[42])",
}


@register
class VAT01GTGT(DeclarationConfig):
    """
    Tờ khai thuế GTGT mẫu 01/GTGT — Phương pháp khấu trừ.
    """

    # === METADATA ===
    code = "01/GTGT"
    name = "Tờ khai thuế giá trị gia tăng"
    short_name = "GTGT khấu trừ"
    xsd_file = "01_GTGT_TT80_283.xsd"
    period = "quarterly"  # monthly hoặc quarterly
    circular = "TT80/2021/TT-BTC"
    has_appendices = True

    # === FRONTEND CONFIG ===
    title = "Tờ khai thuế giá trị gia tăng"
    subtitle = "(Dành cho người nộp thuế tính thuế theo phương pháp khấu trừ)"

    appendices = [
        {"key": "PL01_1_GTGT", "label": "PL 01-1/GTGT", "type": "PL 01-1/GTGT"},
        {"key": "PL01_2_GTGT", "label": "PL 01-2/GTGT", "type": "PL 01-2/GTGT"},
    ]

    sections = [
        {
            "id": "header",
            "title": "Thông tin chung",
            "indicators": ["ct09", "ct10", "ct11a", "ct11b", "ct11c"],
        },
        {
            "id": "no_activity",
            "title": "Không phát sinh hoạt động",
            "indicators": ["ct21"],
        },
        {
            "id": "input_vat",
            "title": "A. THUẾ GTGT CÒN ĐƯỢC KHẤU TRỪ KỲ TRƯỚC CHUYỂN SANG",
            "indicators": ["ct22"],
        },
        {
            "id": "purchases",
            "title": "B. KÊ KHAI THUẾ GTGT MUA VÀO, BÁN RA TRONG KỲ",
            "subsections": [
                {
                    "id": "purchases_total",
                    "title": "I. Hàng hóa, dịch vụ mua vào trong kỳ",
                    "indicators": ["ct23", "ct24"],
                },
                {
                    "id": "purchases_import",
                    "title": "Trong đó: Hàng nhập khẩu",
                    "indicators": ["ct23a", "ct24a"],
                    "indent": 1,
                },
                {
                    "id": "deductible",
                    "title": "II. Thuế GTGT được khấu trừ kỳ này",
                    "indicators": ["ct25"],
                },
            ],
        },
        {
            "id": "sales",
            "title": "III. Hàng hóa, dịch vụ bán ra trong kỳ",
            "subsections": [
                {
                    "id": "sales_exempt",
                    "title": "1. Không chịu thuế GTGT",
                    "indicators": ["ct26"],
                },
                {
                    "id": "sales_taxable",
                    "title": "2. Chịu thuế GTGT",
                    "indicators": ["ct27", "ct28"],
                    "computed": True,
                },
                {
                    "id": "sales_0pct",
                    "title": "a) Thuế suất 0%",
                    "indicators": ["ct29"],
                    "indent": 1,
                },
                {
                    "id": "sales_5pct",
                    "title": "b) Thuế suất 5%",
                    "indicators": ["ct30", "ct31"],
                    "indent": 1,
                },
                {
                    "id": "sales_10pct",
                    "title": "c) Thuế suất 10%",
                    "indicators": ["ct32", "ct33"],
                    "indent": 1,
                },
                {
                    "id": "sales_notax",
                    "title": "d) Không tính thuế",
                    "indicators": ["ct32a"],
                    "indent": 1,
                },
            ],
        },
        {
            "id": "totals",
            "title": "IV. Tổng doanh thu và thuế GTGT",
            "indicators": ["ct34", "ct35"],
            "computed": True,
        },
        {
            "id": "settlement",
            "title": "C. XÁC ĐỊNH NGHĨA VỤ THUẾ GTGT PHẢI NỘP TRONG KỲ",
            "subsections": [
                {
                    "id": "vat_period",
                    "title": "Thuế GTGT phát sinh trong kỳ",
                    "indicators": ["ct36"],
                    "computed": True,
                },
                {
                    "id": "adjustments",
                    "title": "Điều chỉnh",
                    "indicators": ["ct37", "ct38", "ct39a"],
                },
                {
                    "id": "payable",
                    "title": "Thuế GTGT phải nộp",
                    "indicators": ["ct40a", "ct40b", "ct40"],
                    "computed": True,
                    "highlight": True,
                },
                {
                    "id": "carryforward",
                    "title": "Thuế GTGT chưa khấu trừ hết / Chuyển kỳ sau",
                    "indicators": ["ct41", "ct42", "ct43"],
                },
            ],
        },
    ]

    # === DRIVER METHODS ===

    def compute_chi_tieu(self, doc):
        """
        Tính toán tất cả chỉ tiêu cho tờ khai 01/GTGT theo TT80.

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

        sales_lines = get_sales_invoices(company, from_date, to_date)
        purchase_lines = get_purchase_invoices(company, from_date, to_date)

        sales_by_rate = _aggregate_by_rate(sales_lines)
        purchase_totals = _aggregate_purchase(purchase_lines)

        # ── Import VAT (CT24a) ──────────────────────────────────────────────
        import_vat_account = getattr(doc, "import_vat_account", None) or ""
        import_vat_manual = flt(getattr(doc, "import_vat_amount", 0))
        import_goods_value = flt(getattr(doc, "import_goods_value", 0))

        if import_vat_account:
            ct24a_val = get_import_vat_from_account(
                company, from_date, to_date, import_vat_account, finance_book
            )
            ct24a_src = (
                f"Đọc Nợ phát sinh từ JE trên TK '{import_vat_account}' "
                f"trong kỳ = {_fmt(ct24a_val)}đ"
            )
        elif import_vat_manual:
            ct24a_val = import_vat_manual
            ct24a_src = f"Nhập tay = {_fmt(ct24a_val)}đ"
        else:
            ct24a_val = 0
            ct24a_src = "Chưa thiết lập TK hoặc nhập tay (để trống = 0)"

        # ── Tổng hợp mua vào ────────────────────────────────────────────────
        pi_count = purchase_totals["invoice_count"]
        domestic_net = purchase_totals["net_total"]
        domestic_vat = purchase_totals["vat_total"]
        goods_vat = purchase_totals["goods_vat"]
        fa_vat = purchase_totals["fa_vat"]

        # ── Tổng hợp bán ra ─────────────────────────────────────────────────
        si_count = len(set(l["invoice"] for l in sales_lines))
        kct_net = sales_by_rate.get("KCT", {}).get("net", 0)
        _0_net = sales_by_rate.get("0", {}).get("net", 0)
        _5_net = sales_by_rate.get("5", {}).get("net", 0)
        _5_vat = sales_by_rate.get("5", {}).get("vat", 0)
        _8_net = sales_by_rate.get("8", {}).get("net", 0)
        _8_vat = sales_by_rate.get("8", {}).get("vat", 0)
        _10_net = sales_by_rate.get("10", {}).get("net", 0)
        _10_vat = sales_by_rate.get("10", {}).get("vat", 0)

        # ── Helper ghi kết quả ──────────────────────────────────────────────
        r = {}

        def _ct(name, auto_value, source):
            r[name] = {
                "auto_value": flt(auto_value),
                "label": CT_LABELS.get(name, name),
                "source": source,
            }

        # ── CT21 ────────────────────────────────────────────────────────────
        has_activity = bool(sales_lines or purchase_lines)
        _ct("ct21",
            0.0 if has_activity else 1.0,
            f"{'Có' if has_activity else 'Không có'} phát sinh mua/bán. "
            f"{si_count} HĐ bán ra, {pi_count} HĐ mua vào.")

        # ── CT22 ────────────────────────────────────────────────────────────
        _ct("ct22", flt(doc.vat_carried_forward),
            "Lấy từ CT43 kỳ liền trước (auto-fill khi tạo) hoặc nhập tay.")

        # ── Mua vào ─────────────────────────────────────────────────────────
        _ct("ct23", domestic_net + import_goods_value,
            f"PI trong nước: {_fmt(domestic_net)}đ từ {pi_count} HĐ mua vào"
            f" + nhập khẩu CT23a: {_fmt(import_goods_value)}đ.")

        _ct("ct23a", import_goods_value,
            "Nhập tay tại trường 'Giá trị hàng nhập khẩu'. Thường lấy từ tờ khai hải quan.")

        ct24_val = domestic_vat + ct24a_val
        _ct("ct24", ct24_val,
            f"PI trong nước: {_fmt(domestic_vat)}đ "
            f"(HHDV: {_fmt(goods_vat)}đ, TSCĐ: {_fmt(fa_vat)}đ) "
            f"+ nhập khẩu CT24a: {_fmt(ct24a_val)}đ = {_fmt(ct24_val)}đ.")

        _ct("ct24a", ct24a_val, ct24a_src)

        _ct("ct25", ct24_val,
            f"Mặc định = CT24 = {_fmt(ct24_val)}đ. "
            "Ghi đè nếu có HHDV không đủ điều kiện khấu trừ.")

        # ── Bán ra ──────────────────────────────────────────────────────────
        kct_lines = [l for l in sales_lines if l["vat_rate"] == VAT_EXEMPT]
        _ct("ct26", kct_net,
            f"{len(kct_lines)} dòng KCT từ {len(set(l['invoice'] for l in kct_lines))} HĐ: "
            f"{_fmt(kct_net)}đ.")

        _ct("ct29", _0_net,
            f"{_fmt(_0_net)}đ doanh thu 0% (xuất khẩu).")

        _5_invs = len(set(l["invoice"] for l in sales_lines if _rate_to_key(l["vat_rate"]) == "5"))
        _ct("ct30", _5_net, f"{_5_invs} HĐ 5%: doanh thu {_fmt(_5_net)}đ.")
        _ct("ct31", _5_vat, f"{_5_invs} HĐ 5%: thuế {_fmt(_5_vat)}đ.")

        _10_invs = len(set(l["invoice"] for l in sales_lines if _rate_to_key(l["vat_rate"]) == "10"))
        _ct("ct32", _10_net, f"{_10_invs} HĐ 10%: doanh thu {_fmt(_10_net)}đ.")
        _ct("ct33", _10_vat, f"{_10_invs} HĐ 10%: thuế {_fmt(_10_vat)}đ.")

        _8_invs = len(set(l["invoice"] for l in sales_lines if _rate_to_key(l["vat_rate"]) == "8"))
        _ct("ct32a", _8_net,
            f"{_8_invs} HĐ 8% NĐ44/NĐ15: doanh thu {_fmt(_8_net)}đ, thuế {_fmt(_8_vat)}đ. "
            "VAT 8% KHÔNG nằm trong CT28 theo XSD — cần khai PL01-3 (chưa triển khai).")

        # ── Subtotals ────────────────────────────────────────────────────────
        ct27_val = _0_net + _5_net + _10_net + _8_net
        ct28_val = _5_vat + _10_vat  # KHÔNG bao gồm VAT ct32a theo XSD

        _ct("ct27", ct27_val, f"[29]+[30]+[32]+[32a] = {_fmt(_0_net)}+{_fmt(_5_net)}+{_fmt(_10_net)}+{_fmt(_8_net)} = {_fmt(ct27_val)}đ.")
        _ct("ct28", ct28_val, f"[31]+[33] = {_fmt(_5_vat)}+{_fmt(_10_vat)} = {_fmt(ct28_val)}đ. (Không cộng VAT 8% của CT32a)")

        ct34_val = kct_net + ct27_val
        ct35_val = ct28_val

        _ct("ct34", ct34_val, f"[26]+[27] = {_fmt(kct_net)}+{_fmt(ct27_val)} = {_fmt(ct34_val)}đ.")
        _ct("ct35", ct35_val, f"= [28] = {_fmt(ct35_val)}đ.")

        # ── CT36 ────────────────────────────────────────────────────────────
        ct36_val = ct35_val - ct24_val  # ct25 default = ct24
        _ct("ct36", ct36_val,
            f"[35]−[25] = {_fmt(ct35_val)}−{_fmt(ct24_val)} = {_fmt(ct36_val)}đ. "
            "Nếu ghi đè CT25, cần ghi đè CT36 tương ứng.")

        # ── Điều chỉnh ───────────────────────────────────────────────────────
        adj_tang = 0
        adj_giam = 0
        for adj in doc.adjustments:
            if adj.adjustment_type == "Tăng":
                adj_tang += flt(adj.amount)
            elif adj.adjustment_type == "Giảm":
                adj_giam += flt(adj.amount)

        _ct("ct37", adj_giam, f"Tổng {_fmt(adj_giam)}đ từ bảng điều chỉnh GIẢM.")
        _ct("ct38", adj_tang, f"Tổng {_fmt(adj_tang)}đ từ bảng điều chỉnh TĂNG.")

        # ── CT39a ────────────────────────────────────────────────────────────
        ct39a_val = flt(doc.received_vat_credit)
        _ct("ct39a", ct39a_val,
            "Nhập tay — thuế GTGT nhận bàn giao từ dự án/đơn vị khác.")

        # ── Phải nộp / Còn khấu trừ ──────────────────────────────────────────
        ct22_val = flt(doc.vat_carried_forward)
        net_position = ct36_val - ct22_val + adj_giam - adj_tang - ct39a_val

        ct40a_val = max(0.0, net_position)
        _ct("ct40a", ct40a_val,
            f"max(0, [36]−[22]+[37]−[38]−[39a]) = "
            f"max(0, {_fmt(ct36_val)}−{_fmt(ct22_val)}+{_fmt(adj_giam)}−{_fmt(adj_tang)}−{_fmt(ct39a_val)}) "
            f"= {_fmt(ct40a_val)}đ.")

        ct40b_val = min(flt(doc.investment_vat_offset), ct40a_val)
        _ct("ct40b", ct40b_val,
            f"Nhập tay (tối đa CT40a={_fmt(ct40a_val)}đ). Bù trừ thuế GTGT dự án đầu tư.")

        ct40_val = ct40a_val - ct40b_val
        _ct("ct40", ct40_val, f"[40a]−[40b] = {_fmt(ct40a_val)}−{_fmt(ct40b_val)} = {_fmt(ct40_val)}đ.")

        ct41_val = abs(net_position) if net_position < 0 else 0
        _ct("ct41", ct41_val,
            f"net_position = {_fmt(net_position)}đ → "
            f"{'chưa khấu trừ hết' if net_position < 0 else 'không có số dư âm'}.")

        ct42_val = flt(doc.vat_refund_requested)
        _ct("ct42", ct42_val,
            "Nhập tay — tổng số thuế GTGT đề nghị hoàn kỳ này.")

        ct43_val = max(0.0, ct41_val - ct42_val)
        _ct("ct43", ct43_val,
            f"[41]−[42] = {_fmt(ct41_val)}−{_fmt(ct42_val)} = {_fmt(ct43_val)}đ. "
            "Chuyển sang CT22 kỳ sau.")

        return r

    def generate(self, doc):
        """
        Tạo toàn bộ dữ liệu cho tờ khai 01/GTGT (chỉ tiêu + phụ lục).

        Ưu tiên đọc từ ct_values child table (có manual override).
        Nếu ct_values chưa có, tính toán tự động.

        Returns:
            dict: {
                "chi_tieu": {element_name: value, ...},
                "sources": {element_name: source_text, ...},
                "phu_luc": {
                    "PL01_1_GTGT": [rows],
                    "PL01_2_GTGT": [rows],
                }
            }
        """
        chi_tieu, sources = self._get_final_ct_values(doc)

        phu_luc = {
            "PL01_1_GTGT": get_bang_ke_ban_ra(
                doc.company, doc.from_date, doc.to_date
            ),
            "PL01_2_GTGT": get_bang_ke_mua_vao(
                doc.company, doc.from_date, doc.to_date
            ),
            "PL_NQ142_GTGT": get_nq142_appendix(
                doc.company, doc.from_date, doc.to_date
            ),
        }

        return {"chi_tieu": chi_tieu, "sources": sources, "phu_luc": phu_luc}

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

        # Post-process ct21: 1.0 → "True", 0.0 → "False"
        if "ct21" in ct:
            ct["ct21"] = "True" if flt(ct["ct21"]) >= 1 else "False"

        return ct, sources


# ---------------------------------------------------------------------------
# Phụ lục PL 01-1/GTGT (bảng kê bán ra)
# ---------------------------------------------------------------------------

def get_bang_ke_ban_ra(company, from_date, to_date):
    """
    Phụ lục PL 01-1/GTGT — Bảng kê hóa đơn bán ra.

    Một hóa đơn nhiều mức thuế → nhiều dòng (mỗi dòng = 1 mức thuế suất).
    Hóa đơn trả hàng (is_return=1) xuất hiện với số âm.

    Returns:
        list[dict]: mỗi dict chứa các field theo cột XML của PL 01-1
    """
    lines = get_sales_invoices(company, from_date, to_date)

    rows = []
    for line in lines:
        tsuat = _format_thue_suat(line["vat_rate"])

        rows.append({
            "KHMSHDon": "",  # TODO: parse từ einvoice_pattern (Phase 2.13)
            "KHHDon": "",    # TODO: parse từ einvoice_serial
            "SHDon": line.get("einvoice_number") or "",
            "NLap": _format_date(line["posting_date"]),
            "NMua": line.get("customer_name") or "",
            "MST": line.get("customer_tax_id") or "",
            "DThuaKCT": flt(line["base_net_amount"]),
            "TSuat": tsuat,
            "TienThue": flt(line["vat_amount"]),
            "doctype": "Sales Invoice",
            "doc_name": line["invoice"]
        })

    return rows


# ---------------------------------------------------------------------------
# Phụ lục PL 01-2/GTGT (bảng kê mua vào)
# ---------------------------------------------------------------------------

def get_bang_ke_mua_vao(company, from_date, to_date):
    """
    Phụ lục PL 01-2/GTGT — Bảng kê hóa đơn mua vào.

    Hóa đơn trả hàng (is_return=1) xuất hiện với số âm.

    Returns:
        list[dict]: mỗi dict chứa các field theo cột XML của PL 01-2
    """
    lines = get_purchase_invoices(company, from_date, to_date)

    rows = []
    for line in lines:
        tsuat = _format_thue_suat(line["vat_rate"])

        # Ưu tiên Inward Invoice info cho số HĐ
        shdon = (
            line.get("inward_invoice_number")
            or line.get("bill_no")
            or ""
        )
        nlap = (
            _format_date(line.get("inward_invoice_date"))
            or _format_date(line.get("bill_date"))
            or _format_date(line["posting_date"])
        )
        mst = (
            line.get("inward_supplier_tax_code")
            or line.get("supplier_tax_id")
            or ""
        )

        rows.append({
            "KHMSHDon": line.get("inward_invoice_pattern") or "",
            "KHHDon": line.get("inward_invoice_serial") or "",
            "SHDon": shdon,
            "NLap": nlap,
            "NBan": line.get("supplier_name") or "",
            "MST": mst,
            "DThuaKCT": flt(line["base_net_amount"]),
            "TSuat": tsuat,
            "TienThue": flt(line["vat_amount"]),
            "doctype": "Purchase Invoice",
            "doc_name": line["invoice"]
        })

    return rows


# ---------------------------------------------------------------------------
# Phụ lục Giảm thuế NQ142 (8%)
# ---------------------------------------------------------------------------

def get_nq142_appendix(company, from_date, to_date):
    """
    Phụ lục NQ142/2024 về giảm thuế 2% (8% VAT).
    """
    lines = get_sales_invoices(company, from_date, to_date)
    reduced_lines = [l for l in lines if _rate_to_key(l["vat_rate"]) == "8"]

    if not reduced_lines:
        return None

    rows = []
    total_net = 0
    total_reduced = 0

    for line in reduced_lines:
        net = flt(line["base_net_amount"])
        # Giảm 2% so với mức 10%
        reduced_amount = round(net * 0.02)

        rows.append({
            "tenHHDV": f"Hàng hóa, dịch vụ theo HĐ {line['einvoice_number'] or line['invoice']}",
            "giaTriHHDV": net,
            "thueSuatTheoQuyDinh": 10,
            "thueSuatSauGiam": 8,
            "thueGTGTDuocGiam": reduced_amount
        })
        total_net += net
        total_reduced += reduced_amount

    return {
        "HH_DV_BanRaTrongKy": {
            "BangKeTenHHDV": rows,
            "tongCongGiaTriHHDV": total_net,
            "tongCongThueGTGTDuocGiam": total_reduced
        }
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _aggregate_by_rate(sales_lines):
    """
    Gom doanh thu & thuế bán ra theo thuế suất.

    Returns:
        dict: {rate_key: {"net": amount, "vat": amount}}
        rate_key: "KCT", "0", "5", "8", "10"
    """
    result = {}
    for line in sales_lines:
        rate = line["vat_rate"]
        key = _rate_to_key(rate)
        if key not in result:
            result[key] = {"net": 0, "vat": 0}
        result[key]["net"] += flt(line["base_net_amount"])
        result[key]["vat"] += flt(line["vat_amount"])

    return result


def _aggregate_purchase(purchase_lines):
    """
    Tổng hợp giá trị và thuế mua vào, phân biệt HHDV vs TSCĐ.

    Returns:
        dict: {
            "net_total": amount,
            "vat_total": amount,
            "goods_vat": amount,   # thuế HHDV thông thường
            "fa_vat": amount,      # thuế TSCĐ (is_fixed_asset)
            "invoice_count": int,
        }
    """
    result = {
        "net_total": 0, "vat_total": 0,
        "goods_vat": 0, "fa_vat": 0,
        "invoice_count": 0,
    }
    invoices = set()
    for line in purchase_lines:
        result["net_total"] += flt(line["base_net_amount"])
        vat = flt(line["vat_amount"])
        result["vat_total"] += vat
        result["goods_vat"] += flt(line.get("goods_vat", vat))
        result["fa_vat"] += flt(line.get("fa_vat", 0))
        invoices.add(line["invoice"])

    result["invoice_count"] = len(invoices)
    return result


def _rate_to_key(rate):
    """Chuyển VAT rate thành key string."""
    if rate == VAT_EXEMPT:
        return "KCT"
    r = flt(rate)
    if r == int(r):
        return str(int(r))
    return str(r)


def _fmt(n):
    """Format số nguyên với dấu phân cách nghìn cho source notes."""
    return f"{flt(n):,.0f}"


def _format_thue_suat(rate):
    """Format thuế suất cho XML output."""
    if rate == VAT_EXEMPT:
        return "KCT"
    r = flt(rate)
    if r == int(r):
        return f"{int(r)}%"
    return f"{r}%"


def _format_date(date_val):
    """Format date cho XML: dd/MM/yyyy."""
    if not date_val:
        return ""
    return formatdate(str(date_val), "dd/MM/yyyy")


