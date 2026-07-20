# Kế hoạch triển khai VN Accounting

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Mục tiêu:** Xây dựng app bản địa hoá kế toán Việt Nam cho ERPNext v16 với hệ thống tài khoản (TT99/2025), thiết lập mặc định công ty, workspace dashboard, và thanh điều hướng sidebar.

**Kiến trúc:** App Frappe độc lập (`vn_accounting`), không tạo DocType mới. Tất cả tính năng dùng DocType sẵn có của ERPNext. Hệ thống tài khoản đăng ký qua hook `override_whitelisted_methods`. Sidebar + workspace dạng file JSON fixture. 4 báo cáo Script Report theo mẫu Việt Nam.

**Tech Stack:** Frappe v16, ERPNext v16, Python, JSON fixtures, Script Reports (Python + JS)

**Spec:** `docs/specs/2026-04-02-vn-accounting-design.md`

**Lưu ý:** TT99/2025/TT-BTC (hiệu lực 01/01/2026) thay thế cả TT200 và TT133. Design spec ghi "TT99/2024" nhưng đúng là TT99/2025.

---

## Kết quả /autoplan Review

> Review ngày 02/04/2026. 3 pha: CEO → Design → Eng. 4 lỗi critical đã sửa trong plan này.

| # | Lỗi critical | Cách sửa |
|---|---|---|
| 1 | `regional_overrides` không hoạt động — `get_charts_for_country` thiếu decorator `@erpnext.allow_regional` | Dùng `override_whitelisted_methods` thay thế |
| 2 | `after_insert` sai thời điểm — tài khoản được tạo trong `on_update`, không phải `after_insert` | Đổi hook sang `on_update` + guard chống chạy lặp |
| 3 | Number Card logic sai — Doanh thu (TK 511) ghi Có, plan cộng Nợ | Dùng Number Card kiểu `method` với hàm Python |
| 4 | Sidebar links không lọc — "Thu tiền mặt" và "Chi tiền mặt" cùng trỏ Payment Entry | Thêm query params hoặc dùng URL filtered list view |

---

## Cấu trúc file

```
vn_accounting/
├── vn_accounting/
│   ├── __init__.py                          (có sẵn)
│   ├── hooks.py                             (có sẵn, sửa)
│   ├── modules.txt                          (có sẵn)
│   ├── install.py                           (có sẵn, sửa)
│   │
│   ├── chart_of_accounts/
│   │   ├── __init__.py                      (có sẵn)
│   │   ├── coa_registry.py                  (có sẵn, sửa)
│   │   ├── vn_large_enterprise.json         (tạo mới — COA JSON cho Company creation)
│   │   ├── vn_small_enterprise.json         (tạo mới — COA JSON cho Company creation)
│   │   ├── vn_large_enterprise.csv          (tạo mới — COA CSV cho COA Importer)
│   │   └── vn_small_enterprise.csv          (tạo mới — COA CSV cho COA Importer)
│   │
│   ├── setup/
│   │   ├── __init__.py                      (có sẵn)
│   │   └── company_defaults.py              (có sẵn, sửa)
│   │
│   ├── vn_accounting/                       (module "VN Accounting")
│   │   ├── __init__.py                      (có sẵn)
│   │   ├── number_card_methods.py           (tạo mới — hàm Python cho Number Cards)
│   │   ├── workspace/
│   │   │   └── ke_toan_vn/
│   │   │       └── ke_toan_vn.json          (tạo mới — workspace dashboard)
│   │   ├── dashboard_chart/                 (có sẵn)
│   │   │   ├── doanh_thu_chi_phi_thang/
│   │   │   │   └── doanh_thu_chi_phi_thang.json  (tạo mới)
│   │   │   ├── cong_no_phai_thu/
│   │   │   │   └── cong_no_phai_thu.json          (tạo mới)
│   │   │   ├── cong_no_phai_tra/
│   │   │   │   └── cong_no_phai_tra.json          (tạo mới)
│   │   │   └── bien_dong_tien/
│   │   │       └── bien_dong_tien.json            (tạo mới)
│   │   ├── number_card/                     (có sẵn)
│   │   │   ├── tong_doanh_thu/
│   │   │   │   └── tong_doanh_thu.json            (tạo mới — method type)
│   │   │   ├── tong_chi_phi/
│   │   │   │   └── tong_chi_phi.json              (tạo mới — method type)
│   │   │   ├── cong_no_phai_thu/
│   │   │   │   └── cong_no_phai_thu.json          (tạo mới — method type)
│   │   │   ├── cong_no_phai_tra/
│   │   │   │   └── cong_no_phai_tra.json          (tạo mới — method type)
│   │   │   └── ton_quy/
│   │   │       └── ton_quy.json                   (tạo mới — method type)
│   │   └── report/
│   │       ├── so_quy_tien_mat/
│   │       │   ├── so_quy_tien_mat.py             (tạo mới — Script Report)
│   │       │   ├── so_quy_tien_mat.js             (tạo mới — bộ lọc)
│   │       │   └── so_quy_tien_mat.json           (tạo mới — định nghĩa báo cáo)
│   │       ├── so_tien_gui_ngan_hang/
│   │       │   ├── so_tien_gui_ngan_hang.py
│   │       │   ├── so_tien_gui_ngan_hang.js
│   │       │   └── so_tien_gui_ngan_hang.json
│   │       ├── so_chi_tiet_tai_khoan/
│   │       │   ├── so_chi_tiet_tai_khoan.py
│   │       │   ├── so_chi_tiet_tai_khoan.js
│   │       │   └── so_chi_tiet_tai_khoan.json
│   │       └── bang_can_doi_so_phat_sinh/
│   │           ├── bang_can_doi_so_phat_sinh.py
│   │           ├── bang_can_doi_so_phat_sinh.js
│   │           └── bang_can_doi_so_phat_sinh.json
│   │
│   └── workspace_sidebar/
│       └── ke_toan_vn.json                  (tạo mới — sidebar 14 phân hành)
│
├── tests/
│   └── test_coa.py                          (tạo mới — kiểm tra cấu trúc COA)
│
├── pyproject.toml                           (có sẵn, sửa mô tả)
└── docs/
    └── specs/
        └── 2026-04-02-vn-accounting-design.md (có sẵn)
```

---

## Task 1: COA JSON — Doanh nghiệp lớn (TT99/2025)

**Files:**
- Tạo mới: `vn_accounting/chart_of_accounts/vn_large_enterprise.json`

File lớn nhất. Chứa toàn bộ Hệ thống tài khoản kế toán doanh nghiệp lớn theo TT99/2025/TT-BTC: 71 tài khoản cấp 1, ~101 cấp 2, và một số cấp 3.

- [ ] **Bước 1: Tạo file COA JSON**

JSON theo format COA của ERPNext: cây lồng nhau với `root_type` trên node gốc, `account_number` trên mọi node, và `account_type` trên node lá ánh xạ sang ERPNext.

```json
{
    "country_code": "vn",
    "name": "Việt Nam - Doanh nghiệp lớn (TT99/2025)",
    "tree": {
        "Tài sản": {
            "root_type": "Asset",
            "Tiền mặt": {
                "account_number": "111",
                "account_type": "Cash"
            },
            "Tiền gửi không kỳ hạn": {
                "account_number": "112",
                "account_type": "Bank"
            }
        }
    }
}
```

**Bảng ánh xạ account_type (giá trị ERPNext):**

| Tài khoản VN | ERPNext account_type |
|---|---|
| 111 Tiền mặt | Cash |
| 112 Tiền gửi không kỳ hạn | Bank |
| 131 Phải thu khách hàng | Receivable |
| 133 Thuế GTGT được khấu trừ | Tax |
| 151 Hàng mua đang đi đường | Stock Received But Not Billed |
| 152-158 Hàng tồn kho | Stock |
| 211 TSCĐ hữu hình | Fixed Asset |
| 214 Hao mòn TSCĐ | Accumulated Depreciation |
| 241 XDCB dở dang | Capital Work in Progress |
| 331 Phải trả người bán | Payable |
| 333 Thuế và các khoản phải nộp | Tax |
| 33311 Thuế GTGT đầu ra | Tax |
| 421 Lợi nhuận sau thuế CPP | Equity |
| 511 Doanh thu bán hàng | Income Account |
| 515 Doanh thu tài chính | Income Account |
| 521 Giảm trừ doanh thu | Income Account |
| 632 Giá vốn hàng bán | Cost of Goods Sold |
| 635 Chi phí tài chính | Expense Account |
| 641 Chi phí bán hàng | Expense Account |
| 642 Chi phí QLDN | Expense Account |
| 711 Thu nhập khác | Income Account |
| 811 Chi phí khác | Expense Account |
| 821 Chi phí thuế TNDN | Tax |
| 911 Xác định KQKD | Expense Account |

**Danh mục tài khoản đầy đủ cho doanh nghiệp lớn (TT99/2025):**

Loại 1 - Tài sản ngắn hạn:
- 111 Tiền mặt
- 112 Tiền gửi không kỳ hạn
- 113 Tiền đang chuyển
- 121 Chứng khoán kinh doanh
- 128 Đầu tư nắm giữ đến ngày đáo hạn (1281, 1282, 1283, 1288)
- 131 Phải thu của khách hàng
- 133 Thuế GTGT được khấu trừ (1331, 1332)
- 136 Phải thu nội bộ (1361, 1362, 1363, 1368)
- 138 Phải thu khác (1381, 1383, 1388)
- 141 Tạm ứng
- 151 Hàng mua đang đi đường
- 152 Nguyên liệu, vật liệu
- 153 Công cụ, dụng cụ
- 154 Chi phí SXKD dở dang
- 155 Sản phẩm
- 156 Hàng hoá
- 157 Hàng gửi đi bán
- 158 Nguyên liệu, vật tư tại kho bảo thuế
- 171 Giao dịch mua bán lại TPCP

Loại 2 - Tài sản dài hạn:
- 211 TSCĐ hữu hình
- 212 TSCĐ thuê tài chính
- 213 TSCĐ vô hình
- 214 Hao mòn TSCĐ (2141, 2142, 2143, 2147)
- 215 Tài sản sinh học (2151, 2152, 2153)
- 217 Bất động sản đầu tư
- 221 Đầu tư vào công ty con
- 222 Đầu tư vào công ty liên doanh, liên kết
- 228 Đầu tư khác (2281, 2288)
- 229 Dự phòng tổn thất tài sản (2291, 2292, 2293, 2294, 2295)
- 241 XDCB dở dang (2411, 2412, 2413, 2414)
- 242 Chi phí chờ phân bổ
- 243 Tài sản thuế TNDN hoãn lại
- 244 Ký quỹ, ký cược

Loại 3 - Nợ phải trả:
- 331 Phải trả cho người bán
- 332 Phải trả cổ tức, lợi nhuận
- 333 Thuế và các khoản phải nộp NN (3331 gồm 33311/33312, 3332, 3333, 3334, 3335, 3336, 3337, 3338 gồm 33381/33382, 3339)
- 334 Phải trả người lao động
- 335 Chi phí phải trả
- 336 Phải trả nội bộ (3361, 3362, 3363, 3368)
- 337 Thanh toán theo tiến độ hợp đồng XD
- 338 Phải trả, phải nộp khác (3381, 3382, 3383, 3384, 3386, 3387, 3388)
- 341 Vay và nợ thuê tài chính (3411, 3412)
- 343 Trái phiếu phát hành (3431, 3432)
- 344 Nhận ký quỹ, ký cược
- 347 Thuế TNDN hoãn lại phải trả
- 352 Dự phòng phải trả (3521, 3522, 3523, 3525)
- 353 Quỹ khen thưởng, phúc lợi (3531, 3532, 3533, 3534)
- 356 Quỹ phát triển KHCN (3561, 3562)
- 357 Quỹ bình ổn giá

Loại 4 - Vốn chủ sở hữu:
- 411 Vốn đầu tư của CSH (4111 gồm 41111/41112, 4112, 4113, 4118)
- 412 Chênh lệch đánh giá lại tài sản
- 413 Chênh lệch tỷ giá hối đoái
- 414 Quỹ đầu tư phát triển
- 418 Các quỹ khác thuộc VCSH
- 419 Cổ phiếu mua lại của chính mình
- 421 Lợi nhuận sau thuế CPP (4211, 4212)

Loại 5 - Doanh thu:
- 511 Doanh thu bán hàng và cung cấp dịch vụ
- 515 Doanh thu hoạt động tài chính
- 521 Các khoản giảm trừ doanh thu

Loại 6 - Chi phí SXKD:
- 621 Chi phí nguyên vật liệu trực tiếp
- 622 Chi phí nhân công trực tiếp
- 623 Chi phí sử dụng máy thi công (6231-6238)
- 627 Chi phí sản xuất chung (6271-6278)
- 632 Giá vốn hàng bán
- 635 Chi phí tài chính
- 641 Chi phí bán hàng (6411-6418)
- 642 Chi phí quản lý doanh nghiệp (6421-6428)

Loại 7 - Thu nhập khác:
- 711 Thu nhập khác

Loại 8 - Chi phí khác:
- 811 Chi phí khác
- 821 Chi phí thuế TNDN (8211 gồm 82111/82112, 8212)

Loại 9 - Xác định KQKD:
- 911 Xác định kết quả kinh doanh

Viết file JSON đầy đủ với TẤT CẢ tài khoản ở trên, lồng nhau đúng cách với `root_type`, `account_number`, và `account_type` trên mỗi node lá. Tài khoản nhóm dùng `is_group: 1`. Tên tài khoản dùng **tiếng Việt có dấu đầy đủ**.

- [ ] **Bước 2: Kiểm tra JSON hợp lệ**

Chạy: `python3 -c "import json; json.load(open('vn_accounting/chart_of_accounts/vn_large_enterprise.json')); print('Valid JSON')"` từ thư mục gốc app.

Kết quả mong đợi: `Valid JSON`

- [ ] **Bước 3: Commit**

```bash
git add vn_accounting/chart_of_accounts/vn_large_enterprise.json
git commit -m "feat: thêm COA JSON doanh nghiệp lớn (TT99/2025)"
```

---

## Task 2: COA JSON — Doanh nghiệp nhỏ (TT99/2025)

**Files:**
- Tạo mới: `vn_accounting/chart_of_accounts/vn_small_enterprise.json`

COA doanh nghiệp nhỏ là tập con của doanh nghiệp lớn. Khác biệt chính:
- Không có TK 621, 622, 623, 627 (chi phí SXKD chi tiết) — DN nhỏ dùng TK 154 trực tiếp
- Không có TK 136/336 (nội bộ)
- Không có TK 151 (hàng mua đang đi đường)
- Không có TK 158 (kho bảo thuế)
- Không có TK 171 (TPCP)
- Không có TK 215 (tài sản sinh học)
- Không có TK 217 (BĐS đầu tư)
- Không có TK 221, 222 (đầu tư công ty con/liên kết)
- Không có TK 337 (tiến độ XD)
- Không có TK 343 (trái phiếu)
- Không có TK 357 (quỹ bình ổn giá)
- Tổng ~100 tài khoản

- [ ] **Bước 1: Tạo file COA JSON doanh nghiệp nhỏ**

Cùng format Task 1 nhưng với danh sách tài khoản rút gọn. Dùng `country_code: "vn"`, name: `"Việt Nam - Doanh nghiệp nhỏ (TT99/2025)"`. Tên tài khoản **tiếng Việt có dấu đầy đủ**.

- [ ] **Bước 2: Kiểm tra JSON hợp lệ**

Chạy: `python3 -c "import json; json.load(open('vn_accounting/chart_of_accounts/vn_small_enterprise.json')); print('Valid JSON')"` từ thư mục gốc app.

- [ ] **Bước 3: Commit**

```bash
git add vn_accounting/chart_of_accounts/vn_small_enterprise.json
git commit -m "feat: thêm COA JSON doanh nghiệp nhỏ (TT99/2025)"
```

---

## Task 3: COA CSV (cho COA Importer)

**Files:**
- Tạo mới: `vn_accounting/chart_of_accounts/vn_large_enterprise.csv`
- Tạo mới: `vn_accounting/chart_of_accounts/vn_small_enterprise.csv`

Format CSV (8 cột): `Account Name,Parent Account,Account Number,Is Group,Account Type,Account Category,Root Type,Tax Rate`

- [ ] **Bước 1: Tạo CSV doanh nghiệp lớn**

Chuyển đổi từ dữ liệu JSON. Mỗi tài khoản một dòng. Parent Account tham chiếu tên tài khoản cha. Tên tiếng Việt có dấu.

Ví dụ:
```csv
Account Name,Parent Account,Account Number,Is Group,Account Type,Account Category,Root Type,Tax Rate
Tài sản,,,,1,,Asset,
Tiền mặt,Tài sản,111,0,Cash,,Asset,
Tiền gửi không kỳ hạn,Tài sản,112,0,Bank,,Asset,
Phải thu của khách hàng,Tài sản,131,0,Receivable,,Asset,
```

- [ ] **Bước 2: Tạo CSV doanh nghiệp nhỏ**

Cùng format, danh sách tài khoản rút gọn theo Task 2.

- [ ] **Bước 3: Kiểm tra CSV parse đúng**

```bash
python3 -c "
import csv
for f in ['vn_large_enterprise.csv', 'vn_small_enterprise.csv']:
    with open(f'vn_accounting/chart_of_accounts/{f}') as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        print(f'{f}: {len(rows)} tài khoản, cột: {reader.fieldnames}')
"
```

Kết quả: ~180 tài khoản cho DN lớn, ~100 cho DN nhỏ.

- [ ] **Bước 4: Commit**

```bash
git add vn_accounting/chart_of_accounts/vn_large_enterprise.csv
git add vn_accounting/chart_of_accounts/vn_small_enterprise.csv
git commit -m "feat: thêm COA CSV cho COA Importer"
```

---

## Task 4: Kiểm tra cấu trúc COA (tests)

**Files:**
- Tạo mới: `tests/test_coa.py`

> ⚠️ Task mới từ autoplan review — đảm bảo COA JSON không bị lỗi cấu trúc.

- [ ] **Bước 1: Tạo file test**

```python
import json
import os
import pytest

COA_DIR = os.path.join(os.path.dirname(__file__), "..", "vn_accounting", "chart_of_accounts")


def _collect_account_numbers(tree, numbers=None):
    if numbers is None:
        numbers = []
    for key, value in tree.items():
        if isinstance(value, dict):
            if "account_number" in value:
                numbers.append(value["account_number"])
            _collect_account_numbers(value, numbers)
    return numbers


@pytest.mark.parametrize("filename", ["vn_large_enterprise.json", "vn_small_enterprise.json"])
def test_coa_structure(filename):
    filepath = os.path.join(COA_DIR, filename)
    with open(filepath) as f:
        coa = json.load(f)

    assert "tree" in coa, "Thiếu key 'tree'"
    assert "country_code" in coa, "Thiếu key 'country_code'"
    assert coa["country_code"] == "vn"

    # Mọi node gốc phải có root_type
    for name, node in coa["tree"].items():
        assert "root_type" in node, f"Node gốc '{name}' thiếu root_type"
        assert node["root_type"] in ("Asset", "Liability", "Equity", "Income", "Expense")

    # account_number không được trùng
    numbers = _collect_account_numbers(coa["tree"])
    duplicates = [n for n in numbers if numbers.count(n) > 1]
    assert len(duplicates) == 0, f"Trùng account_number: {set(duplicates)}"


def test_large_has_more_accounts_than_small():
    with open(os.path.join(COA_DIR, "vn_large_enterprise.json")) as f:
        large = json.load(f)
    with open(os.path.join(COA_DIR, "vn_small_enterprise.json")) as f:
        small = json.load(f)

    large_nums = _collect_account_numbers(large["tree"])
    small_nums = _collect_account_numbers(small["tree"])
    assert len(large_nums) > len(small_nums), "DN lớn phải có nhiều TK hơn DN nhỏ"


def test_large_has_manufacturing_accounts():
    """DN lớn phải có TK 621, 622, 627 (chi phí sản xuất chi tiết)."""
    with open(os.path.join(COA_DIR, "vn_large_enterprise.json")) as f:
        coa = json.load(f)
    numbers = _collect_account_numbers(coa["tree"])
    for tk in ["621", "622", "627"]:
        assert tk in numbers, f"DN lớn thiếu TK {tk}"


def test_small_no_manufacturing_accounts():
    """DN nhỏ không có TK 621, 622, 627."""
    with open(os.path.join(COA_DIR, "vn_small_enterprise.json")) as f:
        coa = json.load(f)
    numbers = _collect_account_numbers(coa["tree"])
    for tk in ["621", "622", "627"]:
        assert tk not in numbers, f"DN nhỏ không nên có TK {tk}"
```

- [ ] **Bước 2: Chạy test**

```bash
cd /home/long/long/frappe-bench-dcnet/apps/vn_accounting
python3 -m pytest tests/test_coa.py -v
```

Kết quả mong đợi: tất cả PASS.

- [ ] **Bước 3: Commit**

```bash
git add tests/test_coa.py
git commit -m "test: thêm kiểm tra cấu trúc COA JSON"
```

---

## Task 5: Sửa COA Registry (`coa_registry.py`)

**Files:**
- Sửa: `vn_accounting/chart_of_accounts/coa_registry.py`

> ⚠️ FIX CRITICAL #1 từ autoplan: dùng `override_whitelisted_methods` thay vì `regional_overrides`.

Hàm mới phải gọi hàm gốc `get_charts_for_country` trước, rồi thêm templates Việt Nam.

- [ ] **Bước 1: Sửa coa_registry.py**

```python
import json
import os

from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
    get_charts_for_country as _original_get_charts,
)


def get_charts_for_country(country, with_standard=False):
    """Trả về danh sách COA templates cho Company creation flow.

    Gọi hàm gốc của ERPNext trước, sau đó thêm templates Việt Nam
    nếu country = 'Vietnam'.
    """
    charts = _original_get_charts(country, with_standard)

    if country == "Vietnam":
        charts_dir = os.path.dirname(__file__)
        for fname in sorted(os.listdir(charts_dir)):
            if fname.endswith(".json"):
                with open(os.path.join(charts_dir, fname)) as f:
                    content = json.load(f)
                    name = content.get("name")
                    if name and name not in charts:
                        charts.insert(0, name)

    return charts
```

- [ ] **Bước 2: Kiểm tra hàm hoạt động**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute 'vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country' --args '\"Vietnam\"'"
```

Kết quả cần có: `Việt Nam - Doanh nghiệp lớn (TT99/2025)`, `Việt Nam - Doanh nghiệp nhỏ (TT99/2025)`, `Standard`, `Standard with Numbers`

- [ ] **Bước 3: Commit**

```bash
git add vn_accounting/chart_of_accounts/coa_registry.py
git commit -m "fix: dùng override_whitelisted_methods, gọi hàm gốc ERPNext"
```

---

## Task 6: Sửa hooks.py

**Files:**
- Sửa: `vn_accounting/hooks.py`

> ⚠️ FIX CRITICAL #1 + #2 từ autoplan.

- [ ] **Bước 1: Cập nhật hooks.py**

```python
app_name = "vn_accounting"
app_title = "VN Accounting"
app_publisher = "DCNET"
app_description = "Kế toán Việt Nam cho ERPNext v16 — Hệ thống tài khoản TT99/2025, thiết lập mặc định, workspace, sidebar, dashboard"
app_email = "info@dcnet.vn"
app_license = "mit"

required_apps = ["frappe", "erpnext"]

# Đăng ký COA — thêm templates Việt Nam khi chọn country = Vietnam
# Dùng override_whitelisted_methods vì get_charts_for_country không có @erpnext.allow_regional
override_whitelisted_methods = {
    "erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country":
        "vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country"
}

# Thiết lập mặc định công ty sau khi tạo COA
# Dùng on_update vì tài khoản được tạo trong on_update, không phải after_insert
doc_events = {
    "Company": {
        "on_update": "vn_accounting.setup.company_defaults.set_vn_defaults"
    }
}

# Đảm bảo COA templates đã đăng ký sau migrate
after_migrate = ["vn_accounting.install.after_migrate"]
```

- [ ] **Bước 2: Commit**

```bash
git add vn_accounting/hooks.py
git commit -m "fix: đổi regional_overrides sang override_whitelisted_methods, after_insert sang on_update"
```

---

## Task 7: Sửa Company Defaults (`company_defaults.py`)

**Files:**
- Sửa: `vn_accounting/setup/company_defaults.py`

> ⚠️ FIX CRITICAL #2 từ autoplan: thêm guard chống chạy lặp khi on_update.

- [ ] **Bước 1: Cập nhật company_defaults.py**

```python
import frappe


def set_vn_defaults(doc, method=None):
    """Thiết lập mặc định công ty Việt Nam sau khi tạo COA.

    Ánh xạ số hiệu tài khoản Việt Nam (TT99/2025) sang company defaults ERPNext.
    Chỉ chạy khi: country = Vietnam, COA dùng số hiệu VN, và chưa thiết lập.
    """
    if doc.country != "Vietnam":
        return

    # Guard chống chạy lặp — nếu đã thiết lập rồi thì bỏ qua
    if doc.default_cash_account:
        return

    # Kiểm tra COA có dùng số hiệu VN không (TK 111 = Tiền mặt)
    cash_account = frappe.db.get_value(
        "Account",
        {"account_number": "111", "company": doc.name},
        "name",
    )
    if not cash_account:
        return

    # Nhận dạng loại template: DN lớn có TK 621 (Chi phí NVL trực tiếp)
    is_large = frappe.db.exists(
        "Account",
        {"account_number": "621", "company": doc.name},
    )

    defaults = _get_defaults_large() if is_large else _get_defaults_small()

    for field, account_number in defaults.items():
        account_name = frappe.db.get_value(
            "Account",
            {"account_number": account_number, "company": doc.name},
            "name",
        )
        if account_name:
            doc.db_set(field, account_name)


def _get_defaults_large():
    """Ánh xạ tài khoản mặc định cho doanh nghiệp lớn (TT99/2025)."""
    return {
        "default_cash_account": "111",
        "default_bank_account": "112",
        "default_receivable_account": "131",
        "default_payable_account": "331",
        "default_income_account": "511",
        "default_expense_account": "632",
        "stock_received_but_not_billed": "151",
        "default_inventory_account": "156",
        "accumulated_depreciation_account": "214",
        "depreciation_expense_account": "6274",
        "capital_work_in_progress_account": "241",
        "round_off_account": "711",
    }


def _get_defaults_small():
    """Ánh xạ tài khoản mặc định cho doanh nghiệp nhỏ (TT99/2025)."""
    return {
        "default_cash_account": "111",
        "default_bank_account": "112",
        "default_receivable_account": "131",
        "default_payable_account": "331",
        "default_income_account": "511",
        "default_expense_account": "632",
        "default_inventory_account": "156",
        "accumulated_depreciation_account": "214",
        "depreciation_expense_account": "6424",
        "round_off_account": "711",
    }
```

- [ ] **Bước 2: Commit**

```bash
git add vn_accounting/setup/company_defaults.py
git commit -m "fix: thêm guard chống chạy lặp, cập nhật TT99/2025"
```

---

## Task 8: Workspace Sidebar (14 phân hành)

**Files:**
- Tạo mới: `vn_accounting/workspace_sidebar/ke_toan_vn.json`

> ⚠️ FIX CRITICAL #4 từ autoplan: thêm query params cho các link dùng chung DocType.
> ⚠️ FIX từ autoplan: loại bỏ links placeholder chưa có tính năng, đúng 14 phân hành (không phải 13).

Sidebar điều hướng chính với 14 phân hành kế toán Việt Nam. Mỗi phân hành chứa links tới DocType, Report, hoặc Page của ERPNext.

- [ ] **Bước 1: Tạo file sidebar JSON**

Format `Workspace Sidebar` của Frappe v16. Lưu ý:
- Links dùng chung DocType (Payment Entry, Stock Entry) phải có **route URL có filter** thay vì link trực tiếp
- Loại bỏ links placeholder (Tờ khai thuế GTGT, Thuế TNDN, Tình hình sử dụng hoá đơn, Thuyết minh BCTC B09-DN)
- Section Giá thành: giữ nhưng `keep_closed: 1`

**Ánh xạ đầy đủ phân hành → link (đã sửa theo autoplan):**

Phân hành 1: Quỹ tiền mặt
- Thu tiền mặt → `/app/payment-entry?payment_type=Receive&mode_of_payment=Cash` (link_type: URL)
- Chi tiền mặt → `/app/payment-entry?payment_type=Pay&mode_of_payment=Cash` (link_type: URL)
- Sổ quỹ tiền mặt → Sổ Quỹ Tiền Mặt (Report)

Phân hành 2: Ngân hàng
- Thu tiền ngân hàng → `/app/payment-entry?payment_type=Receive&mode_of_payment=Bank Draft` (URL)
- Chi tiền ngân hàng → `/app/payment-entry?payment_type=Pay&mode_of_payment=Bank Draft` (URL)
- Sổ tiền gửi ngân hàng → Sổ Tiền Gửi Ngân Hàng (Report)
- Đối chiếu ngân hàng → Bank Reconciliation Tool (Page)
- Chuyển tiền nội bộ → Journal Entry (DocType)

Phân hành 3: Mua hàng
- Đơn mua hàng → Purchase Order (DocType)
- Hoá đơn mua hàng → Purchase Invoice (DocType)
- Mua hàng nhập kho → Purchase Receipt (DocType)
- Hàng mua trả lại → `/app/purchase-invoice?is_return=1` (URL)
- Công nợ phải trả → Accounts Payable (Report)
- Bảng tổng hợp công nợ NCC → Accounts Payable Summary (Report)
- Báo cáo mua hàng → Purchase Analytics (Report)

Phân hành 4: Bán hàng
- Báo giá → Quotation (DocType)
- Đơn bán hàng → Sales Order (DocType)
- Hoá đơn bán hàng → Sales Invoice (DocType)
- Hàng bán trả lại → `/app/sales-invoice?is_return=1` (URL)
- Công nợ phải thu → Accounts Receivable (Report)
- Bảng tổng hợp công nợ KH → Accounts Receivable Summary (Report)
- Báo cáo bán hàng → Sales Analytics (Report)

Phân hành 5: Kho
- Nhập kho → `/app/stock-entry?stock_entry_type=Material Receipt` (URL)
- Xuất kho → `/app/stock-entry?stock_entry_type=Material Issue` (URL)
- Chuyển kho → `/app/stock-entry?stock_entry_type=Material Transfer` (URL)
- Kiểm kê kho → Stock Reconciliation (DocType)
- Thẻ kho → Stock Ledger (Report)
- Báo cáo nhập xuất tồn → Stock Balance (Report)

Phân hành 6: Tài sản cố định
- Ghi tăng TSCĐ → Asset (DocType)
- Tính khấu hao → Asset Depreciation (DocType)
- Thanh lý TSCĐ → Asset (DocType)
- Sổ TSCĐ → Fixed Asset Register (Report)
- Bảng tính khấu hao → Asset Depreciation Ledger (Report)

Phân hành 7: Công cụ dụng cụ (collapsible, keep_closed: 1)
- Ghi tăng CCDC → Asset (DocType)
- Phân bổ CCDC → Journal Entry (DocType)
- Báo cáo CCDC → Fixed Asset Register (Report)

Phân hành 8: Tiền lương (collapsible, keep_closed: 1)
- Bảng chấm công → Attendance (DocType)
- Bảng lương → Payroll Entry (DocType)
- Phiếu lương → Salary Slip (DocType)

Phân hành 9: Giá thành (collapsible, keep_closed: 1)
- Tập hợp chi phí SX → BOM (DocType)
- Tính giá thành → Work Order (DocType)

Phân hành 10: Thuế (chỉ giữ links có sẵn)
- Bảng kê HĐ GTGT đầu vào → Purchase Register (Report)
- Bảng kê HĐ GTGT đầu ra → Sales Register (Report)

Phân hành 11: Tổng hợp
- Phiếu kế toán → Journal Entry (DocType)
- Kết chuyển cuối kỳ → Period Closing Voucher (DocType)
- Khoá sổ kế toán → Accounting Period (DocType)
- Sổ nhật ký chung → General Ledger (Report)
- Sổ cái → General Ledger (Report)
- Sổ chi tiết tài khoản → Sổ Chi Tiết Tài Khoản (Report)
- Bảng cân đối số phát sinh → Bảng Cân Đối Số Phát Sinh (Report)

Phân hành 12: Báo cáo tài chính (collapsible, keep_closed: 1)
- Bảng CĐKT → Balance Sheet (Report)
- BC Kết quả HĐKD → Profit and Loss Statement (Report)
- BC Lưu chuyển tiền tệ → Cash Flow (Report)

Phân hành 13: Danh mục
- Hệ thống tài khoản → Chart of Accounts (Page)
- Khách hàng → Customer (DocType)
- Nhà cung cấp → Supplier (DocType)
- Hàng hoá, vật tư → Item (DocType)
- Kho → Warehouse (DocType)
- Nhân viên → Employee (DocType)

Phân hành 14: Thiết lập
- Cài đặt kế toán → Accounts Settings (DocType)
- Import cây tài khoản → Chart of Accounts Importer (DocType)
- Năm tài chính → Fiscal Year (DocType)
- Kỳ kế toán → Accounting Period (DocType)

- [ ] **Bước 2: Kiểm tra JSON hợp lệ**

```bash
python3 -c "import json; d=json.load(open('vn_accounting/workspace_sidebar/ke_toan_vn.json')); print(f'Hợp lệ: {len(d[\"items\"])} items')"
```

- [ ] **Bước 3: Commit**

```bash
git add vn_accounting/workspace_sidebar/ke_toan_vn.json
git commit -m "feat: thêm workspace sidebar 14 phân hành kế toán Việt Nam"
```

---

## Task 9: Number Card Methods (hàm Python cho 5 KPI)

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/number_card_methods.py`

> ⚠️ FIX CRITICAL #3 từ autoplan: dùng method-type Number Cards thay vì aggregate.
> Doanh thu ghi Có (credit) TK 511, không phải Nợ (debit). Số dư tiền/công nợ cần tính hiệu debit - credit.

- [ ] **Bước 1: Tạo file number_card_methods.py**

```python
import frappe
from frappe.utils import get_first_day, getdate, today


@frappe.whitelist()
def get_total_revenue(company=None, **kwargs):
    """Tổng doanh thu tháng này (TK 511 - ghi Có)."""
    company = company or frappe.defaults.get_user_default("Company")
    first_day = get_first_day(today())
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE '511%%'
          AND company = %s
          AND is_cancelled = 0
          AND posting_date BETWEEN %s AND %s
        """,
        (company, first_day, today()),
        as_dict=True,
    )
    return result[0].total if result else 0


@frappe.whitelist()
def get_total_expenses(company=None, **kwargs):
    """Tổng chi phí tháng này (TK 621-642 - ghi Nợ)."""
    company = company or frappe.defaults.get_user_default("Company")
    first_day = get_first_day(today())
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE (account LIKE '621%%' OR account LIKE '622%%'
               OR account LIKE '623%%' OR account LIKE '627%%'
               OR account LIKE '632%%' OR account LIKE '635%%'
               OR account LIKE '641%%' OR account LIKE '642%%')
          AND company = %s
          AND is_cancelled = 0
          AND posting_date BETWEEN %s AND %s
        """,
        (company, first_day, today()),
        as_dict=True,
    )
    return result[0].total if result else 0


@frappe.whitelist()
def get_accounts_receivable(company=None, **kwargs):
    """Công nợ phải thu (số dư Nợ TK 131)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE '131%%'
          AND company = %s
          AND is_cancelled = 0
        """,
        (company,),
        as_dict=True,
    )
    return result[0].total if result else 0


@frappe.whitelist()
def get_accounts_payable(company=None, **kwargs):
    """Công nợ phải trả (số dư Có TK 331)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(credit) - SUM(debit), 0) as total
        FROM `tabGL Entry`
        WHERE account LIKE '331%%'
          AND company = %s
          AND is_cancelled = 0
        """,
        (company,),
        as_dict=True,
    )
    return result[0].total if result else 0


@frappe.whitelist()
def get_cash_balance(company=None, **kwargs):
    """Tồn quỹ (số dư Nợ TK 111 + 112)."""
    company = company or frappe.defaults.get_user_default("Company")
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(debit) - SUM(credit), 0) as total
        FROM `tabGL Entry`
        WHERE (account LIKE '111%%' OR account LIKE '112%%')
          AND company = %s
          AND is_cancelled = 0
        """,
        (company,),
        as_dict=True,
    )
    return result[0].total if result else 0
```

- [ ] **Bước 2: Commit**

```bash
git add vn_accounting/vn_accounting/number_card_methods.py
git commit -m "feat: thêm hàm Python cho Number Cards (method type)"
```

---

## Task 10: Number Cards (5 KPI)

**Files:**
- Tạo mới: 5 file JSON trong `vn_accounting/vn_accounting/number_card/`

Dùng Number Card kiểu `method` thay vì `aggregate` (fix từ autoplan).

- [ ] **Bước 1: Đọc một Number Card có sẵn để tham khảo format**

```bash
find apps/erpnext -name "*.json" -path "*/number_card/*" | head -3
```

- [ ] **Bước 2: Tạo 5 file Number Card JSON**

Mỗi card dùng `type: "Custom"` và `method` trỏ tới hàm trong `number_card_methods.py`. Nhớ thêm `filters_json` chứa company filter.

- [ ] **Bước 3: Tạo thư mục và file**

```bash
mkdir -p vn_accounting/vn_accounting/number_card/{tong_doanh_thu,tong_chi_phi,cong_no_phai_thu,cong_no_phai_tra,ton_quy}
```

- [ ] **Bước 4: Commit**

```bash
git add vn_accounting/vn_accounting/number_card/
git commit -m "feat: thêm 5 KPI Number Cards cho dashboard"
```

---

## Task 11: Dashboard Charts (4 biểu đồ)

**Files:**
- Tạo mới: 4 file JSON trong `vn_accounting/vn_accounting/dashboard_chart/`

- [ ] **Bước 1: Đọc Dashboard Chart có sẵn để tham khảo**

```bash
find apps/erpnext -name "*.json" -path "*/dashboard_chart/*" | head -3
```

- [ ] **Bước 2: Tạo 4 file biểu đồ**

- Doanh thu / Chi phí theo tháng (Bar chart)
- Công nợ phải thu (Bar chart)
- Công nợ phải trả (Bar chart)
- Biến động tiền (Line chart)

Mỗi chart phải có company filter.

- [ ] **Bước 3: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/dashboard_chart/{doanh_thu_chi_phi_thang,cong_no_phai_thu,cong_no_phai_tra,bien_dong_tien}
git add vn_accounting/vn_accounting/dashboard_chart/
git commit -m "feat: thêm 4 biểu đồ dashboard tổng quan kế toán"
```

---

## Task 12: Workspace Dashboard

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/workspace/ke_toan_vn/ke_toan_vn.json`

- [ ] **Bước 1: Đọc workspace JSON có sẵn**

```bash
find apps/erpnext -name "*.json" -path "*/workspace/*" -not -path "*/workspace_sidebar/*" | head -5
```

- [ ] **Bước 2: Tạo workspace JSON**

Layout theo design spec mục 5.3:
```
Dòng 1: Header "Tổng quan kế toán"
Dòng 2: 5 Number Cards (col=2,2,3,3,2)
Dòng 3: 2 biểu đồ cạnh nhau (col=6,6)
Dòng 4: 2 biểu đồ cạnh nhau (col=6,6)
Dòng 5: Header "Phân hành kế toán"
Dòng 6-7: 10 shortcut cards
Dòng 8: Header "Báo cáo tài chính"
Dòng 9: 3 shortcut cards (CĐKT, KQKD, LCTT)
```

- [ ] **Bước 3: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/workspace/ke_toan_vn
git add vn_accounting/vn_accounting/workspace/
git commit -m "feat: thêm workspace dashboard với KPI và biểu đồ"
```

---

## Task 13: Báo cáo — Sổ Quỹ Tiền Mặt

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/report/so_quy_tien_mat/{.json,.py,.js}`

Script Report hiển thị giao dịch tiền mặt (TK 111) theo mẫu S07-DN.

- [ ] **Bước 1: Tạo report definition JSON**

```json
{
    "doctype": "Report",
    "name": "So Quy Tien Mat",
    "report_name": "So Quy Tien Mat",
    "ref_doctype": "GL Entry",
    "report_type": "Script Report",
    "module": "VN Accounting",
    "is_standard": "Yes",
    "disabled": 0
}
```

- [ ] **Bước 2: Tạo bộ lọc (JS)**

Bộ lọc: Công ty (bắt buộc), Từ ngày, Đến ngày.

- [ ] **Bước 3: Tạo logic báo cáo (Python)**

Cột: Ngày | Số chứng từ | Loại chứng từ | Diễn giải | TK đối ứng | Thu | Chi | Tồn

Logic:
1. Lấy tài khoản tiền mặt (TK 111*)
2. Tính số dư đầu kỳ (SUM debit - credit trước from_date)
3. Lấy phát sinh trong kỳ, tính số dư luỹ kế

- [ ] **Bước 4: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/report/so_quy_tien_mat
git add vn_accounting/vn_accounting/report/so_quy_tien_mat/
git commit -m "feat: thêm báo cáo Sổ Quỹ Tiền Mặt"
```

---

## Task 14: Báo cáo — Sổ Tiền Gửi Ngân Hàng

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/report/so_tien_gui_ngan_hang/{.json,.py,.js}`

Cùng cấu trúc Sổ Quỹ Tiền Mặt nhưng cho tài khoản ngân hàng (TK 112).

- [ ] **Bước 1: Tạo report JSON, JS, Python**

Bộ lọc thêm: Tài khoản ngân hàng (Link → Account, lọc TK 112*).
Logic giống Task 13 nhưng dùng TK 112.

- [ ] **Bước 2: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/report/so_tien_gui_ngan_hang
git add vn_accounting/vn_accounting/report/so_tien_gui_ngan_hang/
git commit -m "feat: thêm báo cáo Sổ Tiền Gửi Ngân Hàng"
```

---

## Task 15: Báo cáo — Sổ Chi Tiết Tài Khoản

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/report/so_chi_tiet_tai_khoan/{.json,.py,.js}`

Sổ chi tiết cho bất kỳ tài khoản nào, có cột "TK đối ứng" (against) — đặc thù kế toán VN.

- [ ] **Bước 1: Tạo report JSON, JS, Python**

Bộ lọc: Công ty, Tài khoản (bắt buộc), Từ ngày, Đến ngày, Loại đối tượng, Đối tượng.
Cột: Ngày | Số CT | Loại CT | Diễn giải | TK đối ứng | Đối tượng | Nợ | Có | Dư Nợ | Dư Có

Logic: Tính số dư đầu kỳ → phát sinh trong kỳ → số dư luỹ kế.

- [ ] **Bước 2: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/report/so_chi_tiet_tai_khoan
git add vn_accounting/vn_accounting/report/so_chi_tiet_tai_khoan/
git commit -m "feat: thêm báo cáo Sổ Chi Tiết Tài Khoản"
```

---

## Task 16: Báo cáo — Bảng Cân Đối Số Phát Sinh

**Files:**
- Tạo mới: `vn_accounting/vn_accounting/report/bang_can_doi_so_phat_sinh/{.json,.py,.js}`

Bảng cân đối số phát sinh theo format Việt Nam: Số dư đầu kỳ (Nợ/Có) | Phát sinh trong kỳ (Nợ/Có) | Số dư cuối kỳ (Nợ/Có) — theo từng tài khoản.

- [ ] **Bước 1: Tạo report JSON, JS, Python**

Bộ lọc: Công ty, Từ ngày, Đến ngày.
Cột: Số TK | Tên tài khoản | Dư Nợ đầu kỳ | Dư Có đầu kỳ | PS Nợ trong kỳ | PS Có trong kỳ | Dư Nợ cuối kỳ | Dư Có cuối kỳ

Logic:
1. Lấy tất cả tài khoản không phải nhóm, có account_number
2. Tính số dư đầu kỳ (trước from_date)
3. Tính phát sinh trong kỳ
4. Tính số dư cuối kỳ = đầu kỳ + phát sinh
5. Dòng tổng cộng cuối bảng

- [ ] **Bước 2: Commit**

```bash
mkdir -p vn_accounting/vn_accounting/report/bang_can_doi_so_phat_sinh
git add vn_accounting/vn_accounting/report/bang_can_doi_so_phat_sinh/
git commit -m "feat: thêm báo cáo Bảng Cân Đối Số Phát Sinh"
```

---

## Task 17: Cập nhật install.py và pyproject.toml

**Files:**
- Sửa: `vn_accounting/install.py`
- Sửa: `pyproject.toml`

- [ ] **Bước 1: Cập nhật pyproject.toml**

Đổi mô tả "TT99/2024" thành "TT99/2025".

- [ ] **Bước 2: Cập nhật install.py**

```python
import frappe


def after_migrate():
    """Đảm bảo COA templates Việt Nam khả dụng sau migrate."""
    frappe.cache.delete_value("charts_for_country:Vietnam")
```

- [ ] **Bước 3: Commit**

```bash
git add vn_accounting/install.py pyproject.toml
git commit -m "chore: cập nhật install.py và sửa tham chiếu TT99/2025"
```

---

## Task 18: Kiểm tra tích hợp (Integration Test)

Kiểm tra thủ công end-to-end trong docker.

- [ ] **Bước 1: Cài app vào dev site**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local install-app vn_accounting"
```

- [ ] **Bước 2: Chạy migrate**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
```

- [ ] **Bước 3: Kiểm tra COA templates xuất hiện**

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute 'vn_accounting.chart_of_accounts.coa_registry.get_charts_for_country' --args '\"Vietnam\"'"
```

Kết quả cần có cả 2 templates Việt Nam.

- [ ] **Bước 4: Tạo công ty thử với COA Việt Nam**

Qua bench console hoặc trình duyệt: tạo Company với country=Vietnam, chọn "Việt Nam - Doanh nghiệp lớn (TT99/2025)".

- [ ] **Bước 5: Kiểm tra thiết lập mặc định**

Xác nhận default_cash_account, default_bank_account, v.v. đã được điền đúng.

- [ ] **Bước 6: Kiểm tra sidebar và workspace**

Mở site trên trình duyệt. Kiểm tra sidebar "Kế toán VN" hiện đúng và các links hoạt động.

- [ ] **Bước 7: Kiểm tra các báo cáo**

Mở 4 báo cáo tuỳ chỉnh. Xác nhận load không lỗi (dữ liệu có thể trống trên site mới).

- [ ] **Bước 8: Commit sửa lỗi (nếu có)**

```bash
git add -A
git commit -m "fix: sửa lỗi từ kiểm tra tích hợp"
```

---

## Phạm vi hoãn lại (v1.1+)

- Báo cáo tài chính VN: Bảng CĐKT B01-DN, BC KQKD B02-DN, BC LCTT B03-DN
- Báo cáo thuế: Bảng kê GTGT đầu vào/ra, Tờ khai thuế GTGT
- Sổ nhật ký chung (format VN), Sổ cái (format VN)
- Báo cáo lương, giá thành, CCDC
- Trải nghiệm empty state / onboarding
- Vietnamese print formats (Phiếu thu/chi mẫu C30-BB)

---

<!-- AUTONOMOUS DECISION LOG -->
## Decision Audit Trail

| # | Pha | Quyết định | Phân loại | Nguyên tắc | Lý do | Phương án bị loại |
|---|-----|-----------|-----------|------------|-------|-------------------|
| 1 | CEO | Giữ approach fixture-based | Cơ học | P5 rõ ràng | Không cần custom DocType cho v1.0 | Custom DocType, fork India approach |
| 2 | CEO | Giữ dashboard Tasks 10-12 | Vị giác | P3 thực dụng | ~20 phút effort, ấn tượng ban đầu tốt | Hoãn dashboard, thêm B01/B02 |
| 3 | CEO | Để Frappe xử lý empty state | Cơ học | P3 thực dụng | v1.0 tập trung tính năng cốt lõi | Custom onboarding block |
| 4 | Eng | Đổi regional_overrides → override_whitelisted_methods | Cơ học | P1 đầy đủ | get_charts_for_country thiếu @allow_regional | Giữ regional_overrides (không hoạt động) |
| 5 | Eng | Đổi after_insert → on_update | Cơ học | P1 đầy đủ | Tài khoản tạo trong on_update, không phải after_insert | Giữ after_insert (không hoạt động) |
| 6 | Design | Dùng method-type Number Cards | Cơ học | P1 đầy đủ | Aggregate không tính được số dư, DT ghi Có không phải Nợ | Giữ aggregate (sai số liệu) |
| 7 | Design | Thêm query params cho sidebar links | Cơ học | P5 rõ ràng | Links dùng chung DocType không phân biệt được | Giữ link trực tiếp (vô nghĩa) |
| 8 | Design | Loại bỏ links placeholder | Cơ học | P5 rõ ràng | Links trỏ tới tính năng chưa có làm giảm uy tín | Giữ tất cả links |
| 9 | Design | Sửa đếm phân hành 13 → 14 | Cơ học | P5 rõ ràng | Thực tế có 14 phân hành (Danh mục + Thiết lập riêng) | Giữ đếm sai |
| 10 | Eng | Thêm test kiểm tra cấu trúc COA | Cơ học | P1 đầy đủ | COA lỗi cấu trúc sẽ tạo bảng TK hỏng trong DB | Chỉ kiểm tra thủ công |
| 11 | Design | Thêm company filter cho cards/charts | Cơ học | P1 đầy đủ | Multi-company sẽ gộp dữ liệu sai | Không filter |
| 12 | Eng | Thêm idempotency guard cho on_update | Cơ học | P5 rõ ràng | on_update chạy nhiều lần, cần guard | Không guard (ghi đè mỗi lần save) |
