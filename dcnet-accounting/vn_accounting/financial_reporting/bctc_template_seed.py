from __future__ import annotations

import frappe

# B01-DN large enterprise mapping — key lines per TT99/2025 Phụ lục IV
# Full 50+ line set; mã 270 = Tổng tài sản = mã 440 = Tổng nguồn vốn (equation check)
_B01_LARGE = [
    # ── TÀI SẢN NGẮN HẠN ──
    {"code": "100", "label": "TÀI SẢN NGẮN HẠN", "section": "TÀI SẢN", "value_type": "formula", "line_formula": "=110+120+130+140+150", "is_subtotal": 1, "display_indent": 0},
    {"code": "110", "label": "Tiền và các khoản tương đương tiền", "value_type": "closing_debit", "account_formula": "+111,+112,+113", "display_indent": 1},
    {"code": "120", "label": "Đầu tư tài chính ngắn hạn", "value_type": "formula", "line_formula": "=121+122+123", "display_indent": 1},
    {"code": "121", "label": "Chứng khoán kinh doanh", "value_type": "closing_debit", "account_formula": "+121", "display_indent": 2},
    {"code": "122", "label": "Dự phòng giảm giá chứng khoán KD", "value_type": "closing_credit", "account_formula": "+2291", "sign_multiplier": "-1", "display_indent": 2},
    {"code": "123", "label": "Đầu tư nắm giữ đến ngày đáo hạn", "value_type": "closing_debit", "account_formula": "+1281", "display_indent": 2},
    {"code": "130", "label": "Các khoản phải thu ngắn hạn", "value_type": "formula", "line_formula": "=131+132+133+134+135+136+137+139", "display_indent": 1},
    {"code": "131", "label": "Phải thu ngắn hạn của khách hàng", "value_type": "closing_debit", "account_formula": "+131", "display_indent": 2},
    {"code": "132", "label": "Trả trước cho người bán ngắn hạn", "value_type": "closing_debit", "account_formula": "+331%", "display_indent": 2},
    {"code": "133", "label": "Phải thu nội bộ ngắn hạn", "value_type": "closing_debit", "account_formula": "+136", "display_indent": 2},
    {"code": "134", "label": "Phải thu theo tiến độ HĐXD", "value_type": "closing_debit", "account_formula": "+337", "display_indent": 2},
    {"code": "135", "label": "Phải thu về cho vay ngắn hạn", "value_type": "closing_debit", "account_formula": "+1283", "display_indent": 2},
    {"code": "136", "label": "Phải thu ngắn hạn khác", "value_type": "closing_debit", "account_formula": "+1385,+1388,+141", "display_indent": 2, "note": "Per TT99/2025: gồm 1385 (phải thu cổ phần hoá), 1388 (phải thu khác), 141 (Tạm ứng nhân viên). Loại bỏ +334,+338 vì đó là liability — không vào mã 136."},
    {"code": "137", "label": "Dự phòng phải thu ngắn hạn khó đòi", "value_type": "closing_credit", "account_formula": "+2293", "sign_multiplier": "-1", "display_indent": 2},
    {"code": "139", "label": "Tài sản thiếu chờ xử lý", "value_type": "closing_debit", "account_formula": "+1381", "display_indent": 2},
    {"code": "140", "label": "Hàng tồn kho", "value_type": "formula", "line_formula": "=141+149", "display_indent": 1},
    {"code": "141", "label": "Hàng tồn kho", "value_type": "closing_debit", "account_formula": "+151,+152,+153,+154,+155,+156,+157,+158", "display_indent": 2},
    {"code": "149", "label": "Dự phòng giảm giá hàng tồn kho", "value_type": "closing_credit", "account_formula": "+2294", "sign_multiplier": "-1", "display_indent": 2},
    {"code": "150", "label": "Tài sản ngắn hạn khác", "value_type": "formula", "line_formula": "=151+152+153+154+155", "display_indent": 1},
    {"code": "151", "label": "Chi phí trả trước ngắn hạn", "value_type": "closing_debit", "account_formula": "+242,+2421", "display_indent": 2, "note": "+242 match TK 242 (chưa split); +2421 match khi đã có sub-account NH/DH."},
    {"code": "152", "label": "Thuế GTGT được khấu trừ", "value_type": "closing_debit", "account_formula": "+1331,+1332,+1333,+1334", "display_indent": 2},
    {"code": "153", "label": "Thuế và các khoản khác phải thu NN", "value_type": "closing_debit", "account_formula": "+333%", "display_indent": 2},
    {"code": "154", "label": "Giao dịch mua bán lại TPCP", "value_type": "closing_debit", "account_formula": "+171", "display_indent": 2},
    {"code": "155", "label": "Tài sản ngắn hạn khác", "value_type": "closing_debit", "account_formula": "+1388", "display_indent": 2},
    # ── TÀI SẢN DÀI HẠN ──
    {"code": "200", "label": "TÀI SẢN DÀI HẠN", "section": "TÀI SẢN", "value_type": "formula", "line_formula": "=210+220+230+240+250+260", "is_subtotal": 1, "display_indent": 0},
    {"code": "210", "label": "Các khoản phải thu dài hạn", "value_type": "closing_debit", "account_formula": "+1362,+1368,+1388,+2281", "display_indent": 1},
    {"code": "220", "label": "Tài sản cố định", "value_type": "formula", "line_formula": "=221+222+223", "display_indent": 1},
    {"code": "221", "label": "TSCĐ hữu hình", "value_type": "formula", "line_formula": "=221a+221b", "display_indent": 2},
    {"code": "221a", "label": "Nguyên giá", "value_type": "closing_debit", "account_formula": "+211", "display_indent": 3},
    {"code": "221b", "label": "Hao mòn lũy kế", "value_type": "closing_credit", "account_formula": "+2141", "sign_multiplier": "-1", "display_indent": 3},
    {"code": "222", "label": "TSCĐ thuê tài chính", "value_type": "formula", "line_formula": "=222a+222b", "display_indent": 2},
    {"code": "222a", "label": "Nguyên giá", "value_type": "closing_debit", "account_formula": "+212", "display_indent": 3},
    {"code": "222b", "label": "Hao mòn lũy kế", "value_type": "closing_credit", "account_formula": "+2142", "sign_multiplier": "-1", "display_indent": 3},
    {"code": "223", "label": "TSCĐ vô hình", "value_type": "formula", "line_formula": "=223a+223b", "display_indent": 2},
    {"code": "223a", "label": "Nguyên giá", "value_type": "closing_debit", "account_formula": "+213", "display_indent": 3},
    {"code": "223b", "label": "Hao mòn lũy kế", "value_type": "closing_credit", "account_formula": "+2143", "sign_multiplier": "-1", "display_indent": 3},
    {"code": "230", "label": "Bất động sản đầu tư", "value_type": "closing_debit", "account_formula": "+217", "display_indent": 1},
    {"code": "240", "label": "Tài sản dở dang dài hạn", "value_type": "closing_debit", "account_formula": "+2411,+2412,+241%", "display_indent": 1},
    {"code": "250", "label": "Đầu tư tài chính dài hạn", "value_type": "closing_debit", "account_formula": "+221,+222,+228,+2292", "display_indent": 1},
    {"code": "260", "label": "Tài sản dài hạn khác", "value_type": "closing_debit", "account_formula": "+2422,+243,+244,+33311", "display_indent": 1},
    # ── TỔNG TÀI SẢN (mã 270 phải = mã 440) ──
    {"code": "270", "label": "TỔNG CỘNG TÀI SẢN", "section": "TỔNG", "value_type": "formula", "line_formula": "=100+200", "is_subtotal": 1, "display_indent": 0},
    # ── NỢ PHẢI TRẢ ──
    {"code": "300", "label": "NỢ PHẢI TRẢ", "section": "NGUỒN VỐN", "value_type": "formula", "line_formula": "=310+330", "is_subtotal": 1, "display_indent": 0},
    {"code": "310", "label": "Nợ ngắn hạn", "value_type": "formula", "line_formula": "=311+312+313+314+315+316+317+318+319+320+321+322+323+324", "display_indent": 1},
    {"code": "311", "label": "Phải trả người bán ngắn hạn", "value_type": "closing_credit", "account_formula": "+331", "display_indent": 2},
    {"code": "312", "label": "Người mua trả tiền trước ngắn hạn", "value_type": "closing_credit", "account_formula": "+131%", "display_indent": 2},
    {"code": "313", "label": "Thuế và các khoản phải nộp NN", "value_type": "closing_credit", "account_formula": "+333%", "display_indent": 2},
    {"code": "314", "label": "Phải trả người lao động", "value_type": "closing_credit", "account_formula": "+334", "display_indent": 2},
    {"code": "315", "label": "Chi phí phải trả ngắn hạn", "value_type": "closing_credit", "account_formula": "+335", "display_indent": 2},
    {"code": "316", "label": "Phải trả nội bộ ngắn hạn", "value_type": "closing_credit", "account_formula": "+336", "display_indent": 2},
    {"code": "317", "label": "Phải trả theo tiến độ HĐXD", "value_type": "closing_credit", "account_formula": "+337", "display_indent": 2},
    {"code": "318", "label": "Doanh thu chưa thực hiện ngắn hạn", "value_type": "closing_credit", "account_formula": "+3387", "display_indent": 2},
    {"code": "319", "label": "Phải trả ngắn hạn khác", "value_type": "closing_credit", "account_formula": "+3381,+3382,+3383,+3384,+3385,+3386,+3388", "display_indent": 2, "note": "Loại trừ 3387 (đã ở mã 318) — nếu để +338 sẽ double-count 3387."},
    {"code": "320", "label": "Vay và nợ thuê tài chính ngắn hạn", "value_type": "closing_credit", "account_formula": "+3411,+3412", "display_indent": 2, "note": "Chỉ 3411 (vay NH) + 3412 (thuê TC NH). Loại bỏ +341 prefix (sẽ match cả 3413-3415 dài hạn và double-count với mã 338)."},
    {"code": "321", "label": "Dự phòng phải trả ngắn hạn", "value_type": "closing_credit", "account_formula": "+352%", "display_indent": 2, "note": "+352% match all 352* (3521 bảo hành, 3522 tái cơ cấu, 3523 phải trả khác, 3524...). DN không tách NH/DH thì gộp hết vào ngắn hạn."},
    {"code": "322", "label": "Quỹ khen thưởng, phúc lợi", "value_type": "closing_credit", "account_formula": "+353,+3531,+3532", "display_indent": 2},
    {"code": "323", "label": "Quỹ bình ổn giá", "value_type": "closing_credit", "account_formula": "+357", "display_indent": 2},
    {"code": "324", "label": "Giao dịch mua bán lại TPCP", "value_type": "closing_credit", "account_formula": "+171", "display_indent": 2},
    {"code": "330", "label": "Nợ dài hạn", "value_type": "formula", "line_formula": "=331+332+333+334+335+336+337+338+339+340+341+342+343", "display_indent": 1},
    {"code": "331", "label": "Phải trả người bán dài hạn", "value_type": "closing_credit", "account_formula": "", "display_indent": 2, "note": "Để trống: TK 331 đã map vào line 311 (ngắn hạn). KTT tự fill nếu DN có khoản phải trả NB dài hạn riêng."},
    {"code": "332", "label": "Người mua trả tiền trước dài hạn", "value_type": "closing_credit", "account_formula": "", "display_indent": 2, "note": "Để trống: TK 131% đã map vào line 312 (ngắn hạn). KTT tự fill nếu DN có khoản nhận trước dài hạn riêng."},
    {"code": "333", "label": "Chi phí phải trả dài hạn", "value_type": "closing_credit", "account_formula": "+335", "display_indent": 2},
    {"code": "334", "label": "Phải trả nội bộ về vốn kinh doanh", "value_type": "closing_credit", "account_formula": "+3361", "display_indent": 2},
    {"code": "335", "label": "Phải trả nội bộ dài hạn khác", "value_type": "closing_credit", "account_formula": "+3368", "display_indent": 2},
    {"code": "336", "label": "Doanh thu chưa thực hiện dài hạn", "value_type": "closing_credit", "account_formula": "", "display_indent": 2, "note": "Để trống: TK 3387 mặc định ngắn hạn (đã ở mã 318). KTT tự fill nếu DN có khoản DT chưa thực hiện > 12 tháng riêng (vd 3387 split thành 2 sub-TK)."},
    {"code": "337", "label": "Phải trả dài hạn khác", "value_type": "closing_credit", "account_formula": "", "display_indent": 2, "note": "Để trống: TK 338 mặc định ngắn hạn (đã ở mã 319). KTT tự fill nếu DN có khoản phải trả khác > 12 tháng."},
    {"code": "338", "label": "Vay và nợ thuê tài chính dài hạn", "value_type": "closing_credit", "account_formula": "+3413,+3414,+3415", "display_indent": 2, "note": "Chỉ 3413+3414+3415 (vay/nợ dài hạn). Loại bỏ 3411+3412 (đã ở mã 320 ngắn hạn) tránh double-count."},
    {"code": "339", "label": "Trái phiếu chuyển đổi", "value_type": "closing_credit", "account_formula": "+3431,+3432", "display_indent": 2},
    {"code": "340", "label": "Cổ phiếu ưu đãi", "value_type": "closing_credit", "account_formula": "", "display_indent": 2, "note": "Để trống cho DN nhỏ-vừa không có cổ phiếu ưu đãi. KTT fill TK riêng nếu có."},
    {"code": "341", "label": "Thuế thu nhập hoãn lại phải trả", "value_type": "closing_credit", "account_formula": "+347", "display_indent": 2},
    {"code": "342", "label": "Dự phòng phải trả dài hạn", "value_type": "closing_credit", "account_formula": "+3522", "display_indent": 2},
    {"code": "343", "label": "Quỹ phát triển khoa học công nghệ", "value_type": "closing_credit", "account_formula": "+356", "display_indent": 2},
    # ── VỐN CHỦ SỞ HỮU ──
    {"code": "400", "label": "VỐN CHỦ SỞ HỮU", "section": "NGUỒN VỐN", "value_type": "formula", "line_formula": "=410+430", "is_subtotal": 1, "display_indent": 0},
    {"code": "410", "label": "Vốn chủ sở hữu", "value_type": "formula", "line_formula": "=411+412+413+414+415+416+417+418+419+420", "display_indent": 1, "note": "Sum lines 411-419 + subtotal 420. KHÔNG cộng riêng 421/422 (đã có trong 420 = 421+422)."},
    {"code": "411", "label": "Vốn góp của chủ sở hữu", "value_type": "closing_credit", "account_formula": "+4111", "display_indent": 2},
    {"code": "412", "label": "Thặng dư vốn cổ phần", "value_type": "closing_credit", "account_formula": "+4112", "display_indent": 2},
    {"code": "413", "label": "Vốn khác của chủ sở hữu", "value_type": "closing_credit", "account_formula": "+4113,+4118", "display_indent": 2},
    {"code": "414", "label": "Cổ phiếu quỹ", "value_type": "closing_debit", "account_formula": "+419", "sign_multiplier": "-1", "display_indent": 2},
    {"code": "415", "label": "Chênh lệch đánh giá lại tài sản", "value_type": "closing_credit", "account_formula": "+412", "display_indent": 2},
    {"code": "416", "label": "Chênh lệch tỷ giá hối đoái", "value_type": "closing_credit", "account_formula": "+413", "display_indent": 2},
    {"code": "417", "label": "Quỹ đầu tư phát triển", "value_type": "closing_credit", "account_formula": "+414", "display_indent": 2},
    {"code": "418", "label": "Quỹ hỗ trợ sắp xếp doanh nghiệp", "value_type": "closing_credit", "account_formula": "+417", "display_indent": 2},
    {"code": "419", "label": "Quỹ khác thuộc vốn chủ sở hữu", "value_type": "closing_credit", "account_formula": "+418", "display_indent": 2},
    {"code": "420", "label": "Lợi nhuận sau thuế chưa phân phối", "value_type": "formula", "line_formula": "=421+422", "display_indent": 2},
    {"code": "421", "label": "Lợi nhuận chưa phân phối năm trước", "value_type": "net_credit", "account_formula": "+4211", "display_indent": 3, "note": "net_credit: âm khi TK 4211 có số dư Dr (lỗ năm trước)"},
    {"code": "422", "label": "Lợi nhuận chưa phân phối năm nay", "value_type": "net_credit", "account_formula": "+4212", "display_indent": 3, "note": "net_credit: âm khi TK 4212 có số dư Dr (lỗ năm nay)"},
    {"code": "430", "label": "Nguồn kinh phí và quỹ khác", "value_type": "closing_credit", "account_formula": "+461,+462,+466", "display_indent": 1},
    # ── TỔNG NGUỒN VỐN (phải = mã 270) ──
    {"code": "440", "label": "TỔNG CỘNG NGUỒN VỐN", "section": "TỔNG", "value_type": "formula", "line_formula": "=300+400", "is_subtotal": 1, "display_indent": 0},
]

# B02-DN large enterprise mapping (KQHĐKD — ~18 lines)
# Note: All P&L lines use value_type=period_net (Cr-Dr) — auto handles sign.
# Revenue accounts Cr>Dr give positive value; expense accounts Cr<Dr give negative.
# Giảm trừ DT line 02 uses sign -1 because Dr 521 reduces revenue.
_B02_LARGE = [
    {"code": "01", "label": "Doanh thu bán hàng và cung cấp dịch vụ", "section": "KẾT QUẢ HOẠT ĐỘNG KINH DOANH", "value_type": "period_net", "account_formula": "+511,+512", "display_indent": 0},
    {"code": "02", "label": "Các khoản giảm trừ doanh thu", "value_type": "period_net", "account_formula": "+521", "sign_multiplier": "-1", "display_indent": 1, "note": "TK 521 period_net = Cr-Dr (âm khi có Dr returns). Sign -1 đảo về dương để hiển thị giảm trừ."},
    {"code": "10", "label": "Doanh thu thuần về bán hàng và CCDV", "value_type": "formula", "line_formula": "=01+02", "is_subtotal": 1, "display_indent": 0},
    {"code": "11", "label": "Giá vốn hàng bán", "value_type": "period_net", "account_formula": "+632", "display_indent": 0, "note": "period_net = Cr 632 - Dr 632 (âm). Đã net với sales returns Cr 632."},
    {"code": "20", "label": "Lợi nhuận gộp về bán hàng và CCDV", "value_type": "formula", "line_formula": "=10+11", "is_subtotal": 1, "display_indent": 0},
    {"code": "21", "label": "Doanh thu hoạt động tài chính", "value_type": "period_net", "account_formula": "+515", "display_indent": 0},
    {"code": "22", "label": "Chi phí tài chính", "value_type": "period_net", "account_formula": "+635", "display_indent": 0},
    {"code": "23", "label": "Trong đó: Chi phí lãi vay", "value_type": "period_net", "account_formula": "+6351", "display_indent": 1},
    {"code": "24", "label": "Phần lãi lỗ trong công ty liên doanh", "value_type": "period_net", "account_formula": "+515%", "display_indent": 0},
    {"code": "25", "label": "Chi phí bán hàng", "value_type": "period_net", "account_formula": "+641", "display_indent": 0},
    {"code": "26", "label": "Chi phí quản lý doanh nghiệp", "value_type": "period_net", "account_formula": "+642", "display_indent": 0},
    {"code": "30", "label": "Lợi nhuận thuần từ HĐKD", "value_type": "formula", "line_formula": "=20+21+22+23+24+25+26", "is_subtotal": 1, "display_indent": 0},
    {"code": "31", "label": "Thu nhập khác", "value_type": "period_net", "account_formula": "+711", "display_indent": 0},
    {"code": "32", "label": "Chi phí khác", "value_type": "period_net", "account_formula": "+811", "display_indent": 0},
    {"code": "40", "label": "Lợi nhuận khác", "value_type": "formula", "line_formula": "=31+32", "display_indent": 0},
    {"code": "50", "label": "Tổng LN kế toán trước thuế TNDN", "value_type": "formula", "line_formula": "=30+40", "is_subtotal": 1, "display_indent": 0},
    {"code": "51", "label": "Chi phí thuế TNDN hiện hành", "value_type": "period_net", "account_formula": "+821", "display_indent": 0},
    {"code": "60", "label": "Lợi nhuận sau thuế TNDN", "value_type": "formula", "line_formula": "=50+51", "is_subtotal": 1, "display_indent": 0},
    {"code": "70", "label": "Lãi cơ bản trên cổ phiếu", "value_type": "formula", "line_formula": "=60", "display_indent": 0},
]

# B03-DN large enterprise mapping (LCTT gián tiếp — ~30 lines)
# Indirect-method = LN trước thuế + non-cash adjustments + working-capital delta.
# Lines 07-11 use delta_debit/delta_credit (signed period change in balance).
_B03_LARGE = [
    {"code": "01", "label": "LN trước thuế", "section": "LƯU CHUYỂN TIỀN TỪ HĐKD", "value_type": "period_net", "account_formula": "+511,+512,+515,+711,+632,+641,+642,+635,+811", "display_indent": 0, "note": "period_net: doanh thu Cr-Dr + chi phí Cr-Dr (loại trừ PCV closing entries) = LN trước thuế."},
    {"code": "02", "label": "Khấu hao TSCĐ và BĐSĐT (add back)", "value_type": "period_debit", "account_formula": "+6141,+6142,+6424,+627%", "display_indent": 1, "note": "Add back khấu hao (non-cash). TK 6141 trong giá vốn, 6142 trong CPBH, 6424 trong CPQLDN, 627% trong CP SX chung."},
    {"code": "03", "label": "Các khoản dự phòng (add back)", "value_type": "delta_credit", "account_formula": "+159%,+229%,+352%", "display_indent": 1, "note": "Delta dự phòng phải thu khó đòi (159), giảm giá HTK/CK (229), dự phòng phải trả (352)."},
    {"code": "04", "label": "Lãi/lỗ chênh lệch tỷ giá chưa thực hiện", "value_type": "delta_credit", "account_formula": "+4131", "sign_multiplier": "-1", "display_indent": 1, "note": "TK 4131 (CLTG chưa thực hiện) — delta Cr trừ ra vì chưa cash."},
    {"code": "05", "label": "Lãi/lỗ từ HĐ đầu tư", "value_type": "period_net", "account_formula": "+515,+635", "sign_multiplier": "-1", "display_indent": 1, "note": "Trừ ra phần LN từ đầu tư (đã tính ở LN trước thuế nhưng cash ở HĐĐT line 21-27)."},
    {"code": "06", "label": "Chi phí lãi vay (add back)", "value_type": "period_debit", "account_formula": "+6351", "display_indent": 1, "note": "Add back lãi vay (chuyển sang HĐ tài chính)."},
    {"code": "07", "label": "LN từ HĐKD trước thay đổi vốn lưu động", "value_type": "formula", "line_formula": "=01+02+03+04+05+06", "is_subtotal": 1, "display_indent": 1},
    {"code": "08", "label": "(+/-) Tăng/giảm các khoản phải thu", "value_type": "delta_debit", "account_formula": "+131,+138%", "sign_multiplier": "-1", "display_indent": 1, "note": "Delta Dr AR. Tăng AR (số dương) → trừ khỏi cash (sign -1)."},
    {"code": "09", "label": "(+/-) Tăng/giảm hàng tồn kho", "value_type": "delta_debit", "account_formula": "+151,+152,+153,+154,+155,+156,+157,+158", "sign_multiplier": "-1", "display_indent": 1, "note": "Delta Dr HTK. Tồn kho tăng = cash tied up."},
    {"code": "10", "label": "(+/-) Tăng/giảm các khoản phải trả", "value_type": "delta_credit", "account_formula": "+331,+333%,+334,+335,+336,+337,+338%", "display_indent": 1, "note": "Delta Cr AP + Thuế phải nộp + lương + chi phí phải trả. KHÔNG bao gồm vay 341 (đã ở HĐ tài chính)."},
    {"code": "11", "label": "(+/-) Tăng/giảm CP trả trước", "value_type": "delta_debit", "account_formula": "+142,+242", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "12", "label": "Tiền lãi vay đã trả", "value_type": "period_debit", "account_formula": "+6351", "sign_multiplier": "-1", "display_indent": 1, "note": "Subtract lãi vay đã trả (đã add back ở line 06, trừ phần thực trả)."},
    {"code": "13", "label": "Thuế TNDN đã nộp", "value_type": "period_debit", "account_formula": "+3334", "sign_multiplier": "-1", "display_indent": 1, "note": "Dr 3334 trong kỳ = đã nộp thuế TNDN."},
    {"code": "14", "label": "Tiền thu khác từ HĐKD", "value_type": "period_credit", "account_formula": "+711%", "display_indent": 1},
    {"code": "15", "label": "Tiền chi khác cho HĐKD", "value_type": "period_debit", "account_formula": "+811%", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "20", "label": "LC THUẦN TỪ HĐKD", "value_type": "formula", "line_formula": "=07+08+09+10+11+12+13+14+15", "is_subtotal": 1, "display_indent": 0},
    {"code": "21", "label": "Mua sắm TSCĐ, BĐSĐT", "section": "LƯU CHUYỂN TIỀN TỪ HĐĐT", "value_type": "period_debit", "account_formula": "+211,+213", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "22", "label": "Tiền thu từ thanh lý TSCĐ", "value_type": "period_credit", "account_formula": "+711%", "display_indent": 1},
    {"code": "23", "label": "Cho vay, mua công cụ nợ", "value_type": "period_debit", "account_formula": "+1281,+2281", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "24", "label": "Thu hồi cho vay, bán công cụ nợ", "value_type": "period_credit", "account_formula": "+1281,+2281", "display_indent": 1},
    {"code": "25", "label": "Đầu tư CTLK, CTTK", "value_type": "period_debit", "account_formula": "+221,+222,+228", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "26", "label": "Thu hồi vốn CTLK, CTTK", "value_type": "period_credit", "account_formula": "+221,+222,+228", "display_indent": 1},
    {"code": "27", "label": "Tiền lãi cho vay, cổ tức, LN nhận được", "value_type": "period_credit", "account_formula": "+515", "display_indent": 1},
    {"code": "30", "label": "LC THUẦN TỪ HĐĐT", "value_type": "formula", "line_formula": "=21+22+23+24+25+26+27", "is_subtotal": 1, "display_indent": 0},
    {"code": "31", "label": "Tiền vay nhận được", "section": "LƯU CHUYỂN TIỀN TỪ HĐTC", "value_type": "period_credit", "account_formula": "+3411,+3412,+3413", "display_indent": 1},
    {"code": "32", "label": "Hoàn trả nợ vay", "value_type": "period_debit", "account_formula": "+3411,+3412,+3413", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "33", "label": "Tiền thu từ phát hành cổ phiếu", "value_type": "period_credit", "account_formula": "+4111,+4112", "display_indent": 1},
    {"code": "34", "label": "Cổ tức, LN đã trả cho chủ sở hữu", "value_type": "period_debit", "account_formula": "+414,+421", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "40", "label": "LC THUẦN TỪ HĐTC", "value_type": "formula", "line_formula": "=31+32+33+34", "is_subtotal": 1, "display_indent": 0},
    {"code": "50", "label": "LC THUẦN TRONG KỲ", "value_type": "formula", "line_formula": "=20+30+40", "is_subtotal": 1, "display_indent": 0},
    {"code": "60", "label": "Tiền và TĐTT đầu kỳ", "value_type": "closing_debit", "account_formula": "+111,+112,+113", "display_indent": 0},
    {"code": "61", "label": "Ảnh hưởng thay đổi tỷ giá hối đoái", "value_type": "formula", "line_formula": "=61", "display_indent": 0},
    {"code": "70", "label": "TIỀN VÀ TĐTT CUỐI KỲ", "value_type": "formula", "line_formula": "=50+60+61", "is_subtotal": 1, "display_indent": 0},
]


# ─────────────────────────────────────────────────────────────────────────────
# vn_small_trade — DN nhỏ-vừa thương mại + dịch vụ (no manufacturing)
# ~40 lines total (vs 87 for large enterprise). Drops TK 154/155/621/622/627.
# B01: drop TSCĐ thuê tài chính sub-lines, TSCĐ vô hình sub-lines, đầu tư DH.
# B02: drop tiêu thụ đặc biệt, drop lãi/lỗ liên doanh.
# B03: keep indirect simplified (no production-cost lines).
# ─────────────────────────────────────────────────────────────────────────────

_B01_SMALL_TRADE = [
    {"code": "100", "label": "TÀI SẢN NGẮN HẠN", "section": "TÀI SẢN", "value_type": "formula", "line_formula": "=110+130+140+150", "is_subtotal": 1, "display_indent": 0},
    {"code": "110", "label": "Tiền và các khoản tương đương tiền", "value_type": "closing_debit", "account_formula": "+111,+112,+113", "display_indent": 1},
    {"code": "130", "label": "Các khoản phải thu ngắn hạn", "value_type": "formula", "line_formula": "=131+132+138", "display_indent": 1},
    {"code": "131", "label": "Phải thu khách hàng", "value_type": "closing_debit", "account_formula": "+131", "display_indent": 2},
    {"code": "132", "label": "Trả trước cho người bán", "value_type": "closing_debit", "account_formula": "+331%", "display_indent": 2},
    {"code": "138", "label": "Phải thu khác", "value_type": "closing_debit", "account_formula": "+138%", "display_indent": 2},
    {"code": "140", "label": "Hàng tồn kho", "value_type": "closing_debit", "account_formula": "+151,+152,+153,+154,+155,+156,+157,+158", "display_indent": 1, "note": "Per TT99/2025: 140 = toàn bộ TK 151-158 (gồm 154 SXKD dở dang). DN thương mại chủ yếu TK 156. Nếu có sản xuất, TK 154 chứa WIP."},
    {"code": "150", "label": "Tài sản ngắn hạn khác", "value_type": "formula", "line_formula": "=151+152s", "display_indent": 1},
    {"code": "151", "label": "Chi phí trả trước ngắn hạn", "value_type": "closing_debit", "account_formula": "+242", "display_indent": 2, "note": "TT99/2025: TK 142 đã bỏ, hợp nhất vào TK 242 Chi phí chờ phân bổ."},
    {"code": "152s", "label": "Thuế GTGT được khấu trừ", "value_type": "closing_debit", "account_formula": "+1331,+1332,+1333,+1334", "display_indent": 2},
    {"code": "200", "label": "TÀI SẢN DÀI HẠN", "section": "TÀI SẢN", "value_type": "formula", "line_formula": "=220+240", "is_subtotal": 1, "display_indent": 0},
    {"code": "220", "label": "Tài sản cố định (net)", "value_type": "formula", "line_formula": "=221a+221b", "display_indent": 1},
    {"code": "221a", "label": "Nguyên giá TSCĐ", "value_type": "closing_debit", "account_formula": "+211,+213", "display_indent": 2},
    {"code": "221b", "label": "Hao mòn lũy kế (-)", "value_type": "closing_credit", "account_formula": "+2141,+2143", "sign_multiplier": "-1", "display_indent": 2},
    {"code": "240", "label": "Tài sản dở dang dài hạn (XDCB)", "value_type": "closing_debit", "account_formula": "+241%", "display_indent": 1},
    {"code": "270", "label": "TỔNG CỘNG TÀI SẢN", "section": "TỔNG", "value_type": "formula", "line_formula": "=100+200", "is_subtotal": 1, "display_indent": 0},
    {"code": "300", "label": "NỢ PHẢI TRẢ", "section": "NGUỒN VỐN", "value_type": "formula", "line_formula": "=311+312+313+314+315+319+320", "is_subtotal": 1, "display_indent": 0},
    {"code": "311", "label": "Phải trả người bán", "value_type": "closing_credit", "account_formula": "+331", "display_indent": 1},
    {"code": "312", "label": "Người mua trả tiền trước", "value_type": "closing_credit", "account_formula": "+131%", "display_indent": 1},
    {"code": "313", "label": "Thuế và các khoản phải nộp NN", "value_type": "closing_credit", "account_formula": "+333%", "display_indent": 1},
    {"code": "314", "label": "Phải trả người lao động", "value_type": "closing_credit", "account_formula": "+334", "display_indent": 1},
    {"code": "315", "label": "Chi phí phải trả", "value_type": "closing_credit", "account_formula": "+335", "display_indent": 1},
    {"code": "319", "label": "Phải trả ngắn hạn khác", "value_type": "closing_credit", "account_formula": "+338%", "display_indent": 1},
    {"code": "320", "label": "Vay và nợ ngắn hạn", "value_type": "closing_credit", "account_formula": "+3411,+3412", "display_indent": 1},
    {"code": "400", "label": "VỐN CHỦ SỞ HỮU", "section": "NGUỒN VỐN", "value_type": "formula", "line_formula": "=411+420", "is_subtotal": 1, "display_indent": 0},
    {"code": "411", "label": "Vốn góp của chủ sở hữu", "value_type": "closing_credit", "account_formula": "+4111,+4112,+4113,+4118", "display_indent": 1},
    {"code": "420", "label": "Lợi nhuận sau thuế chưa phân phối", "value_type": "net_credit", "account_formula": "+421%", "display_indent": 1, "note": "net_credit: âm khi TK 421 có số dư Dr (lỗ)."},
    {"code": "440", "label": "TỔNG CỘNG NGUỒN VỐN", "section": "TỔNG", "value_type": "formula", "line_formula": "=300+400", "is_subtotal": 1, "display_indent": 0},
]

_B02_SMALL_TRADE = [
    {"code": "01", "label": "Doanh thu bán hàng và CCDV", "section": "KẾT QUẢ HĐKD", "value_type": "period_net", "account_formula": "+511,+512", "display_indent": 0},
    {"code": "02", "label": "Các khoản giảm trừ doanh thu", "value_type": "period_net", "account_formula": "+521", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "10", "label": "Doanh thu thuần", "value_type": "formula", "line_formula": "=01+02", "is_subtotal": 1, "display_indent": 0},
    {"code": "11", "label": "Giá vốn hàng bán", "value_type": "period_net", "account_formula": "+632", "display_indent": 0},
    {"code": "20", "label": "Lợi nhuận gộp", "value_type": "formula", "line_formula": "=10+11", "is_subtotal": 1, "display_indent": 0},
    {"code": "21", "label": "Doanh thu HĐ tài chính", "value_type": "period_net", "account_formula": "+515", "display_indent": 0},
    {"code": "22", "label": "Chi phí tài chính", "value_type": "period_net", "account_formula": "+635", "display_indent": 0},
    {"code": "25", "label": "Chi phí bán hàng", "value_type": "period_net", "account_formula": "+641", "display_indent": 0},
    {"code": "26", "label": "Chi phí quản lý doanh nghiệp", "value_type": "period_net", "account_formula": "+642", "display_indent": 0},
    {"code": "30", "label": "Lợi nhuận thuần từ HĐKD", "value_type": "formula", "line_formula": "=20+21+22+25+26", "is_subtotal": 1, "display_indent": 0},
    {"code": "31", "label": "Thu nhập khác", "value_type": "period_net", "account_formula": "+711", "display_indent": 0},
    {"code": "32", "label": "Chi phí khác", "value_type": "period_net", "account_formula": "+811", "display_indent": 0},
    {"code": "40", "label": "Lợi nhuận khác", "value_type": "formula", "line_formula": "=31+32", "display_indent": 0},
    {"code": "50", "label": "Tổng LN kế toán trước thuế", "value_type": "formula", "line_formula": "=30+40", "is_subtotal": 1, "display_indent": 0},
    {"code": "51", "label": "Chi phí thuế TNDN hiện hành", "value_type": "period_net", "account_formula": "+821", "display_indent": 0},
    {"code": "60", "label": "Lợi nhuận sau thuế TNDN", "value_type": "formula", "line_formula": "=50+51", "is_subtotal": 1, "display_indent": 0},
]

_B03_SMALL_TRADE = [
    {"code": "01", "label": "LN trước thuế", "section": "HĐKD", "value_type": "period_net", "account_formula": "+511,+512,+515,+711,+632,+641,+642,+635,+811", "display_indent": 0},
    {"code": "02", "label": "Khấu hao TSCĐ (add back)", "value_type": "period_debit", "account_formula": "+6424", "display_indent": 1, "note": "DN thương mại/dịch vụ: khấu hao chủ yếu ở TK 6424 (CPQLDN). Không có 6141/6142/627x."},
    {"code": "03", "label": "Các khoản dự phòng (add back)", "value_type": "delta_credit", "account_formula": "+159%,+229%,+352%", "display_indent": 1},
    {"code": "07", "label": "LN từ HĐKD trước thay đổi VLĐ", "value_type": "formula", "line_formula": "=01+02+03", "is_subtotal": 1, "display_indent": 1},
    {"code": "08", "label": "Tăng/giảm phải thu KH", "value_type": "delta_debit", "account_formula": "+131,+138%", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "09", "label": "Tăng/giảm hàng tồn kho", "value_type": "delta_debit", "account_formula": "+151,+152,+153,+154,+155,+156,+157,+158", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "10", "label": "Tăng/giảm phải trả NCC, thuế, lương", "value_type": "delta_credit", "account_formula": "+331,+333%,+334,+335,+338%", "display_indent": 1},
    {"code": "11", "label": "Tăng/giảm CP trả trước", "value_type": "delta_debit", "account_formula": "+142,+242", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "13", "label": "Thuế TNDN đã nộp", "value_type": "period_debit", "account_formula": "+3334", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "20", "label": "LC THUẦN TỪ HĐKD", "value_type": "formula", "line_formula": "=07+08+09+10+11+13", "is_subtotal": 1, "display_indent": 0},
    {"code": "21", "label": "Mua sắm TSCĐ", "section": "HĐ ĐẦU TƯ", "value_type": "delta_debit", "account_formula": "+211,+213", "sign_multiplier": "-1", "display_indent": 1},
    {"code": "30", "label": "LC THUẦN TỪ HĐĐT", "value_type": "formula", "line_formula": "=21", "is_subtotal": 1, "display_indent": 0},
    {"code": "31", "label": "Tiền vay nhận / trả nợ vay", "section": "HĐ TÀI CHÍNH", "value_type": "delta_credit", "account_formula": "+3411,+3412", "display_indent": 1},
    {"code": "33", "label": "Phát hành cổ phiếu", "value_type": "delta_credit", "account_formula": "+4111,+4112", "display_indent": 1},
    {"code": "40", "label": "LC THUẦN TỪ HĐTC", "value_type": "formula", "line_formula": "=31+33", "is_subtotal": 1, "display_indent": 0},
    {"code": "50", "label": "LC THUẦN TRONG KỲ", "value_type": "formula", "line_formula": "=20+30+40", "is_subtotal": 1, "display_indent": 0},
    {"code": "60", "label": "Tiền và TĐTT đầu kỳ", "value_type": "closing_debit", "account_formula": "+111,+112,+113", "display_indent": 0, "note": "Số dư trước period_start. Resolver sẽ tính tại (period_start - 1 day) khi line này được report dùng đầu kỳ — hiện hardcode dùng closing tại period_end, cần override manual."},
    {"code": "70", "label": "TIỀN VÀ TĐTT CUỐI KỲ", "value_type": "formula", "line_formula": "=50+60", "is_subtotal": 1, "display_indent": 0},
]


def seed_bctc_mapping_templates() -> None:
    """Seed BCTC Mapping Template records with TT99/2025 defaults.
    Idempotent: checks existence before inserting.
    Two templates: vn_large_enterprise (87+19+30 lines, full BCTC), and
    vn_small_trade (~30 lines, DN nhỏ-vừa thương mại+dịch vụ).
    """
    templates = [
        ("vn_large_enterprise_b01", "b01_lines", _B01_LARGE),
        ("vn_large_enterprise_b02", "b02_lines", _B02_LARGE),
        ("vn_large_enterprise_b03", "b03_lines", _B03_LARGE),
        ("vn_small_trade_b01", "b01_lines", _B01_SMALL_TRADE),
        ("vn_small_trade_b02", "b02_lines", _B02_SMALL_TRADE),
        ("vn_small_trade_b03", "b03_lines", _B03_SMALL_TRADE),
    ]

    for template_name, table_field, lines in templates:
        if frappe.db.exists("BCTC Mapping Template", template_name):
            continue

        doc = frappe.new_doc("BCTC Mapping Template")
        doc.name = template_name
        for line in lines:
            row = {
                "code": line.get("code", ""),
                "label": line.get("label", ""),
                "section": line.get("section", ""),
                "value_type": line.get("value_type", "formula"),
                "account_formula": line.get("account_formula", ""),
                "line_formula": line.get("line_formula", ""),
                "display_indent": line.get("display_indent", 0),
                "is_subtotal": line.get("is_subtotal", 0),
                "sign_multiplier": line.get("sign_multiplier", "+1"),
                "note": line.get("note", ""),
            }
            doc.append(table_field, row)

        doc.flags.ignore_permissions = True
        doc.insert()
        frappe.db.commit()
        print(f"  ✓ BCTC Mapping Template: {template_name} ({len(lines)} lines)")
