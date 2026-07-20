# Bank Statement Settings — Tham chiếu cấu hình

Tài liệu dành cho quản trị viên và người dùng nâng cao.

Bank Statement Settings là DocType singleton (1 bản ghi duy nhất) quản lý toàn bộ cấu hình cho quy trình import sao kê và đối soát công nợ.

## Các trường cấu hình

### Bật/Tắt Matcher

| Trường | Mặc định | Mô tả |
|--------|----------|-------|
| `enable_matcher_invoice_no` | ON | InvoiceNoMatcher — trích xuất số hóa đơn từ nội dung chuyển khoản bằng regex |
| `enable_matcher_invoice_amount` | ON | InvoiceAmountMatcher — tìm hóa đơn có outstanding_amount khớp số tiền giao dịch |
| `enable_matcher_party_amount` | ON | PartyAmountMatcher — xác định đối tác từ tài khoản đối ứng, tìm hóa đơn khớp |
| `enable_matcher_name_amount` | ON | NameAmountMatcher — khớp mờ tên đối tác (fuzzy match ≥80%); luôn trả về Low confidence |

Tắt một matcher → các giao dịch từng khớp bởi matcher đó sẽ không còn gợi ý khi chạy lại đối soát.

### Cấu hình Multi-Invoice

| Trường | Mặc định | Mô tả |
|--------|----------|-------|
| `enable_multi_invoice_match` | ON | Cho phép 1 giao dịch khớp nhiều hóa đơn |
| `multi_invoice_max_combinations` | 5 | Số tổ hợp hóa đơn tối đa thử (giới hạn để tránh tính toán quá lâu) |

### Cửa sổ thời gian

| Trường | Mặc định | Mô tả |
|--------|----------|-------|
| `amount_date_tolerance_days` | 3 | Phạm vi ngày tìm kiếm hóa đơn: ±N ngày so với ngày giao dịch ngân hàng |

### Mẫu regex số hóa đơn (`invoice_number_patterns`)

Bảng con (child table) chứa danh sách regex để trích xuất số hóa đơn từ nội dung chuyển khoản.

**Mặc định (seeded):**

| Pattern | Giải thích |
|---------|-----------|
| `ACC-SI-\d{4}-\d+` | Sales Invoice theo định dạng ERPNext Accounting (ví dụ: ACC-SI-2026-00045) |
| `ACC-PI-\d{4}-\d+` | Purchase Invoice theo định dạng ERPNext Accounting |
| `SI-\d+` | Sales Invoice đơn giản (ví dụ: SI-00123) |
| `PINV-\d+` | Purchase Invoice đơn giản |

**Thêm pattern mới:**

Nếu công ty sử dụng hóa đơn điện tử (HĐĐT) với mã riêng, thêm regex vào bảng này. Ví dụ:
- Hóa đơn HĐĐT: `HD\d{7}` → khớp "HD0012345"
- Mã đặt hàng: `PO-\d{4}-\d+` → khớp "PO-2026-00089"

Regex sử dụng cú pháp Python `re` module. Tất cả pattern được thử lần lượt trên mỗi nội dung chuyển khoản — pattern đầu tiên khớp sẽ được sử dụng.

### Dung sai (Tolerance)

| Trường | Mặc định | Mô tả |
|--------|----------|-------|
| `tolerance_type` | Fixed Amount | Loại dung sai: "Fixed Amount" hoặc "Percent" |
| `tolerance_fixed_amount` | 1,000 VND | Chênh lệch tối đa chấp nhận (khi tolerance_type = Fixed Amount) |
| `tolerance_percent` | 0.1% | Chênh lệch tối đa theo phần trăm (khi tolerance_type = Percent) |

**Cách tính dung sai:**

- **Fixed Amount**: `|số_tiền_GD - tổng_hóa_đơn| ≤ tolerance_fixed_amount`
- **Percent**: `|số_tiền_GD - tổng_hóa_đơn| / tổng_hóa_đơn × 100 ≤ tolerance_percent`

Ví dụ: Giao dịch 10,001,000 VND khớp hóa đơn 10,000,000 VND → chênh lệch 1,000 VND ≤ dung sai 1,000 VND → **khớp**.

### Hành vi Payment Entry

| Trường | Mặc định | Mô tả |
|--------|----------|-------|
| `default_pe_action` | Draft | Tạo PE ở trạng thái Draft (nháp) hoặc Submit (đã gửi) |
| `default_mode_of_payment_credit` | _(trống)_ | Phương thức thanh toán mặc định cho giao dịch Có (tiền vào). Gợi ý: "Wire Transfer" |
| `default_mode_of_payment_debit` | _(trống)_ | Phương thức thanh toán mặc định cho giao dịch Nợ (tiền ra) |
| `difference_account` | _(trống)_ | Tài khoản hạch toán chênh lệch (Link → Account). Xem mục "Xử lý chênh lệch" bên dưới |

### Bảng quy tắc (Rules Table) — v2 scaffold

| Trường | Mô tả |
|--------|-------|
| `rule_key` | Tên matcher hoặc quy tắc |
| `enabled` | Bật/tắt |
| `priority` | Thứ tự ưu tiên (kéo thả) |
| `confidence_override` | Ghi đè mức tin cậy |
| `tolerance_override` | Ghi đè dung sai |
| `bank_account` | Áp dụng cho tài khoản ngân hàng cụ thể (v2) |

## Xử lý chênh lệch theo TT99/2025

Theo Thông tư 99/2025/TT-BTC, các khoản chênh lệch nhỏ giữa sao kê ngân hàng và hóa đơn (phí chuyển khoản, phí dịch vụ ngân hàng) được hạch toán vào tài khoản chi phí phù hợp.

### Cách hoạt động

1. Nếu `difference_account` **đã cấu hình** VÀ chênh lệch ≤ dung sai:
   - Payment Entry tự động thêm dòng **Deductions** (khấu trừ)
   - Tài khoản: giá trị của `difference_account`
   - Số tiền: phần chênh lệch

2. Nếu `difference_account` **chưa cấu hình** (trống):
   - Không thêm dòng Deductions
   - PE tạo với số tiền gốc từ giao dịch ngân hàng

3. Nếu chênh lệch **vượt dung sai**:
   - Không tự động tạo PE
   - Giao dịch hiển thị cảnh báo, người dùng xử lý thủ công

### Tài khoản chi phí phù hợp (TT99/2025)

| Tài khoản | Tên | Sử dụng cho |
|-----------|-----|------------|
| **6415** | Chi phí dịch vụ mua hàng | Phí chuyển khoản liên quan đến mua hàng |
| **6425** | Chi phí dịch vụ ngân hàng | Phí duy trì tài khoản, phí giao dịch chung |
| **6427** | Chi phí tài chính khác | Chênh lệch tỷ giá nhỏ, phí khác |

**Cấu hình:** Vào Bank Statement Settings → trường "Difference Account" → chọn tài khoản phù hợp (ví dụ: 6425 - Chi phí dịch vụ ngân hàng).

## Thêm Matcher mới

Để thêm một matcher tùy chỉnh:

1. **Tạo file Python** tại `vn_banking/match/my_matcher.py`
2. **Kế thừa `BaseMatcher`**:

```python
from vn_banking.match.base import BaseMatcher

class MyCustomMatcher(BaseMatcher):
    name = "MyCustomMatcher"
    default_confidence = "Medium"

    def match(self, transaction, outstanding_invoices):
        """
        Args:
            transaction: NormalizedTransaction (date, deposit, withdrawal,
                        description, reference_number, counter_account_no,
                        counter_account_name, raw_row)
            outstanding_invoices: list of outstanding SI/PI

        Returns:
            MatchCandidate or None
                MatchCandidate fields: party_type, party, invoices,
                total_allocated, difference, confidence,
                matched_by, explanation
        """
        # Logic khớp tùy chỉnh
        return None
```

3. **Đăng ký** trong fixture `fixtures/bank_matcher_type.json`:
```json
{
    "name": "MyCustomMatcher",
    "module_path": "vn_banking.match.my_matcher.MyCustomMatcher",
    "default_confidence": "Medium",
    "enabled": 1,
    "priority": 50
}
```

4. **Viết test** tại `tests/test_my_matcher.py`

## Thêm định dạng ngân hàng mới

1. **Lấy file mẫu** sao kê từ ngân hàng mới
2. **Đặt vào** `tests/fixtures/sample_<bank_name>.xlsx`
3. **Phân tích cấu trúc**: header row, cột ngày/số tiền/nội dung — xem `docs/accounting-requirements/banking/ANALYSIS.md` để theo pattern phân tích
4. **Thêm entry** vào `fixtures/bank_statement_format.json`:
```json
{
    "name": "New Bank",
    "bank_name": "New Bank",
    "file_type": "Excel",
    "header_row": 5,
    "date_column": "A",
    "date_format": "%d/%m/%Y",
    "credit_column": "E",
    "debit_column": "F",
    "description_column": "C",
    "reference_column": "B",
    "counter_account_column": "G",
    "counter_name_column": "H"
}
```
5. **Viết test** parse file mẫu → verify row count, decimals, dates, direction
6. **Chạy test**: `bench --site <site> run-tests --app vn_banking`
