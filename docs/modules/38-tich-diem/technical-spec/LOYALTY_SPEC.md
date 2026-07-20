# Module Loyalty - Đặc tả theo Nhật Minh

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6
> **Phiên bản:** 1.0.0 | **Giai đoạn:** Bàn giao đợt 1
> **Nền tảng:** DCNET Core Loyalty Program (có sẵn)

---

## Định nghĩa

> Chương trình tích điểm và quản lý khách hàng thân thiết, nhằm giữ chân và gia tăng giá trị lifetime của khách hàng.

---

## Spec gốc từ FEATURE_SPECIFICATION.md (Section 4.6)

> **Giai đoạn:** Bàn giao đợt 1

**Chức năng yêu cầu:**
- Quy tắc tính điểm
- Quy tắc lên hạng

---

## DCNET Core Loyalty Program - Chức năng có sẵn

### Tổng quan

DCNET Core đã có sẵn module **Loyalty Program** với đầy đủ chức năng đáp ứng yêu cầu spec.

### DocTypes có sẵn

| # | DocType | Chức năng |
|---|---------|-----------|
| 1 | **Loyalty Program** | Cấu hình chương trình loyalty |
| 2 | **Loyalty Program Collection** | Quy tắc tích điểm theo hạng |
| 3 | **Loyalty Point Entry** | Lịch sử giao dịch điểm |

---

## 1. Quy tắc tính điểm (Loyalty Program Collection)

### Giải thích thuật ngữ

> **collection_factor** (Hệ số quy đổi điểm): Số tiền cần chi để được 1 điểm.
> Ví dụ: collection_factor = 10,000 nghĩa là chi 10,000 VNĐ được 1 điểm.

### Cách hoạt động

Sử dụng `collection_factor` (Hệ số quy đổi điểm) để tính điểm:

```
ĐIỂM = GIÁ TRỊ ĐƠN HÀNG ÷ COLLECTION_FACTOR
```

### Ví dụ

| Hạng | Hệ số quy đổi | Ý nghĩa |
|------|---------------|---------|
| Bronze | 10,000 | Chi 10,000 VNĐ = 1 điểm |
| Silver | 8,000 | Chi 8,000 VNĐ = 1 điểm |
| Gold | 6,000 | Chi 6,000 VNĐ = 1 điểm |
| Platinum | 5,000 | Chi 5,000 VNĐ = 1 điểm |

**Ví dụ tính toán:**
- Đơn hàng: 10,000,000 VNĐ
- Hạng: Silver (Hệ số quy đổi = 8,000)
- Điểm = 10,000,000 ÷ 8,000 = **1,250 điểm**

### Fields trong Loyalty Program Collection

| Field | Tên tiếng Việt | Mô tả |
|-------|----------------|-------|
| `tier_name` | Tên hạng | Bronze/Silver/Gold/Platinum |
| `min_spent` | Doanh số tối thiểu | Doanh số để vào hạng này |
| `collection_factor` | Hệ số quy đổi điểm | Bao nhiêu VNĐ = 1 điểm |

### CẦN XÁC NHẬN với khách hàng

| Hạng | Câu hỏi | Xác nhận |
|------|---------|----------|
| Bronze | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| Silver | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| Gold | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| Platinum | Bao nhiêu VNĐ = 1 điểm? | ☐ |

---

## 2. Quy tắc lên hạng (Multiple Tier Program)

### Cách hoạt động

Hỗ trợ `Multiple Tier Program` - tự động xác định hạng dựa trên `min_spent`:

```
Khi KH mua hàng:
1. Tính total_spent (tổng chi tiêu)
2. So sánh với min_spent của từng tier
3. Gán tier cao nhất mà KH đạt điều kiện
```

### Ví dụ cấu hình

| Hạng | Doanh số tối thiểu | Hệ số quy đổi |
|------|-------------------|---------------|
| Bronze | 0 | 10,000 VNĐ = 1 điểm |
| Silver | 20,000,000 | 8,000 VNĐ = 1 điểm |
| Gold | 50,000,000 | 6,000 VNĐ = 1 điểm |
| Platinum | 100,000,000 | 5,000 VNĐ = 1 điểm |

**Ví dụ:**
- KH chi tiêu tổng: 55,000,000 VNĐ
- Đạt điều kiện: Bronze (0), Silver (20M), Gold (50M)
- → Tự động vào hạng **Gold**

### Fields trong Loyalty Program

| Field | Type | Mô tả |
|-------|------|-------|
| `loyalty_program_type` | Select | "Single Tier Program" / "Multiple Tier Program" |
| `collection_rules` | Table | Danh sách các tier và điều kiện |
| `from_date` | Date | Ngày bắt đầu chương trình |
| `to_date` | Date | Ngày kết thúc (optional) |

### CẦN XÁC NHẬN với khách hàng

| Tham số | Câu hỏi | Xác nhận |
|---------|---------|----------|
| min_spent Silver | Doanh số tối thiểu lên Silver? | ☐ |
| min_spent Gold | Doanh số tối thiểu lên Gold? | ☐ |
| min_spent Platinum | Doanh số tối thiểu lên Platinum? | ☐ |

---

## 3. Chức năng bổ sung có sẵn

### 3.1. Sử dụng điểm (Point Redemption)

| Field | Mô tả |
|-------|-------|
| `conversion_factor` | 1 điểm = X VNĐ |

**Ví dụ:**
- conversion_factor = 1,000
- KH có 500 điểm → Đổi được 500,000 VNĐ giảm giá

### 3.2. Điểm hết hạn (Point Expiry)

| Field | Mô tả |
|-------|-------|
| `expiry_duration` | Số ngày điểm có hiệu lực |

**Ví dụ:**
- expiry_duration = 365
- Điểm tích ngày 01/01 → Hết hạn 31/12

### 3.3. Auto Opt-in

| Field | Mô tả |
|-------|-------|
| `auto_opt_in` | Tự động áp dụng cho tất cả KH |

### 3.4. Lọc theo Territory/Customer Group

| Field | Mô tả |
|-------|-------|
| `customer_territory` | Áp dụng cho KH thuộc territory |
| `customer_group` | Áp dụng cho KH thuộc group |

### CẦN XÁC NHẬN với khách hàng

| Chức năng | Câu hỏi | Xác nhận |
|-----------|---------|----------|
| Sử dụng điểm | Có cho KH dùng điểm đổi giảm giá? | ☐ |
| Tỷ lệ quy đổi | 1 điểm = bao nhiêu VNĐ? | ☐ |
| Điểm hết hạn | Điểm có hết hạn không? Sau bao lâu? | ☐ |
| Auto opt-in | Tự động áp dụng cho tất cả KH? | ☐ |

---

## 4. Tích hợp có sẵn

### 4.1. Với Sales Invoice

- Tự động tích điểm khi submit Sales Invoice
- Cho phép dùng điểm giảm giá tại Invoice
- Ghi nhận expense vào sổ kế toán

### 4.2. Với Customer

- Field `loyalty_program` trong Customer
- Hiển thị điểm hiện tại
- Link tới Loyalty Point Entry

---

## 5. Lịch sử giao dịch điểm (Loyalty Point Entry)

### Fields có sẵn

| Field | Type | Mô tả |
|-------|------|-------|
| `loyalty_program` | Link | Chương trình loyalty |
| `loyalty_program_tier` | Data | Hạng tại thời điểm giao dịch |
| `customer` | Link | Khách hàng |
| `invoice_type` | Link | Loại chứng từ (Sales Invoice) |
| `invoice` | Dynamic Link | Link tới Invoice |
| `loyalty_points` | Int | Số điểm (+/-) |
| `purchase_amount` | Currency | Giá trị mua hàng |
| `expiry_date` | Date | Ngày hết hạn điểm |
| `posting_date` | Date | Ngày giao dịch |

---

## 6. Tổng hợp - Mapping Spec vs DCNET Core

| # | Yêu cầu từ Spec | DCNET Core Feature | Status |
|---|-----------------|---------------------|--------|
| 1 | Quy tắc tính điểm | Loyalty Program Collection (collection_factor) | ✅ Có sẵn |
| 2 | Quy tắc lên hạng | Multiple Tier Program (min_spent) | ✅ Có sẵn |

**Chức năng bổ sung có sẵn (cần xác nhận với KH):**

| # | Chức năng | Cần confirm |
|---|-----------|-------------|
| 3 | Sử dụng điểm (conversion_factor) | ☐ |
| 4 | Điểm hết hạn (expiry_duration) | ☐ |
| 5 | Lịch sử giao dịch (Loyalty Point Entry) | ☐ |
| 6 | Auto opt-in | ☐ |

---

## 7. Hướng dẫn cấu hình

### Bước 1: Tạo Loyalty Program

**Điền thông tin:**
- Loyalty Program Name: "Nhật Minh Golf Club"
- Loyalty Program Type: "Multiple Tier Program"
- From Date: Ngày bắt đầu
- Auto Opt In: ✅ (nếu áp dụng cho tất cả KH)

### Bước 2: Cấu hình Collection Rules (Tier)

Thêm các tier vào bảng Collection Rules:

| Tier Name | Minimum Total Spent | Collection Factor |
|-----------|---------------------|-------------------|
| Bronze | 0 | (cần confirm) |
| Silver | (cần confirm) | (cần confirm) |
| Gold | (cần confirm) | (cần confirm) |
| Platinum | (cần confirm) | (cần confirm) |

### Bước 3: Cấu hình Redemption (nếu có)

- Conversion Factor: 1 điểm = X VNĐ
- Expiry Duration: X ngày
- Expense Account: Tài khoản ghi nhận chi phí

---

## 8. Câu hỏi cần clarify với khách hàng

| # | Câu hỏi | Ảnh hưởng đến |
|---|---------|---------------|
| 1 | Hệ số quy đổi điểm cho từng hạng? (Bao nhiêu VNĐ = 1 điểm) | Tính điểm |
| 2 | Doanh số tối thiểu cho từng hạng? | Lên hạng |
| 3 | Có cho dùng điểm đổi giảm giá không? | Sử dụng điểm |
| 4 | Nếu có, 1 điểm = bao nhiêu VNĐ? | Tỷ lệ quy đổi |
| 5 | Điểm có hết hạn không? Sau bao lâu? | Thời hạn điểm |
| 6 | Áp dụng tự động cho tất cả KH? | Tự động đăng ký |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6 - Quản lý Tích điểm
**Nền tảng:** DCNET Core Loyalty Program
**Cập nhật:** 2026-01-13
