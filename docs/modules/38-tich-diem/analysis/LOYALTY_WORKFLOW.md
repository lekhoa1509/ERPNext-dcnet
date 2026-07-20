# Module Khách hàng Thân thiết (Loyalty) - Workflow

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6
> **Phiên bản:** v1.0.0 | **Nền tảng:** DCNET Core Loyalty Program (có sẵn)

---

## 1. Tổng quan

### Định nghĩa

Module Loyalty là chương trình tích điểm và quản lý khách hàng thân thiết, nhằm giữ chân và gia tăng giá trị lifetime của khách hàng.

### Yêu cầu từ Spec (Section 4.6)

| # | Chức năng | Status |
|---|-----------|--------|
| 1 | Quy tắc tính điểm | ✅ Có sẵn |
| 2 | Quy tắc lên hạng | ✅ Có sẵn |

### Chức năng có sẵn trong DCNET Core

| # | Chức năng | DocType |
|---|-----------|---------|
| 1 | Cấu hình chương trình Loyalty | Loyalty Program |
| 2 | Quy tắc tích điểm theo hạng | Loyalty Program Collection |
| 3 | Lịch sử giao dịch điểm | Loyalty Point Entry |
| 4 | Sử dụng điểm giảm giá | Sales Invoice |
| 5 | Điểm hết hạn | expiry_duration |
| 6 | Auto opt-in cho tất cả KH | auto_opt_in |

---

## 2. Workflow chính

### 2.1. Luồng tổng quan

```mermaid
flowchart TD
    A[Khách hàng] --> B{Có loyalty_program?}

    B -->|Chưa| C[Gán Loyalty Program]
    B -->|Rồi| D[Đã có program]

    C --> E[Mua hàng - Sales Invoice]
    D --> E

    E --> F[Tính total_spent]
    F --> G{Xác định tier theo min_spent}

    G --> H[Gán tier phù hợp]
    H --> I[Tính điểm theo collection_factor]
    I --> J[Tạo Loyalty Point Entry]

    J --> K{KH dùng điểm?}
    K -->|Có| L[Giảm giá đơn hàng]
    K -->|Không| M[Giữ điểm]

    L --> N[Trừ điểm - Tạo Entry âm]
    M --> E
    N --> E
```

### 2.2. Quy trình tích điểm

```mermaid
flowchart LR
    A[Sales Invoice Submit] --> B[Lấy Customer]
    B --> C[Lấy Loyalty Program]
    C --> D[Tính total_spent của KH]

    D --> E{Xác định tier}
    E --> F[Lấy collection_factor của tier]

    F --> G[Tính điểm]
    G --> H[ĐIỂM = Invoice Amount ÷ collection_factor]

    H --> I[Tạo Loyalty Point Entry]
    I --> J[Ghi expiry_date nếu có]
```

### 2.3. Quy trình sử dụng điểm

```mermaid
flowchart TD
    A[Tạo Sales Invoice] --> B[Chọn dùng điểm]
    B --> C{Kiểm tra điểm khả dụng}

    C -->|Không đủ| D[Thông báo lỗi]
    C -->|Đủ| E[Nhập số điểm muốn dùng]

    E --> F[Tính giá trị giảm]
    F --> G[loyalty_amount = points × conversion_factor]

    G --> H[Giảm giá Invoice]
    H --> I[Submit Invoice]
    I --> J[Tạo Loyalty Point Entry âm]
```

### 2.4. Quy trình xác định hạng

```mermaid
flowchart TD
    A[Khi tạo Invoice] --> B[Lấy total_spent của KH]
    B --> C[Lấy danh sách tier từ collection_rules]

    C --> D{So sánh với min_spent}

    D --> E[Tier 1: Bronze - min_spent = 0]
    D --> F[Tier 2: Silver - min_spent = X1]
    D --> G[Tier 3: Gold - min_spent = X2]
    D --> H[Tier 4: Platinum - min_spent = X3]

    E --> I[Chọn tier cao nhất đạt điều kiện]
    F --> I
    G --> I
    H --> I

    I --> J[Áp dụng collection_factor của tier đó]

    style I fill:#a7fab9
```

---

## 3. Entity Relationship

### 3.1. ERD - DCNET Core

```mermaid
erDiagram
    CUSTOMER ||--o| LOYALTY_PROGRAM : has
    LOYALTY_PROGRAM ||--o{ LOYALTY_PROGRAM_COLLECTION : has
    CUSTOMER ||--o{ LOYALTY_POINT_ENTRY : has
    SALES_INVOICE ||--o| LOYALTY_POINT_ENTRY : generates

    CUSTOMER {
        string name PK
        string customer_name
        link loyalty_program FK
    }

    LOYALTY_PROGRAM {
        string name PK
        string loyalty_program_name
        select loyalty_program_type
        date from_date
        date to_date
        check auto_opt_in
        link customer_group
        link customer_territory
        float conversion_factor
        int expiry_duration
        link expense_account
    }

    LOYALTY_PROGRAM_COLLECTION {
        string tier_name
        currency min_spent
        currency collection_factor
    }

    LOYALTY_POINT_ENTRY {
        string name PK
        link loyalty_program FK
        data loyalty_program_tier
        link customer FK
        link invoice FK
        int loyalty_points
        currency purchase_amount
        date expiry_date
        date posting_date
    }

    SALES_INVOICE {
        string name PK
        link customer FK
        int loyalty_points
        currency loyalty_amount
        link loyalty_program FK
    }
```

### 3.2. Chi tiết các Entity

#### LOYALTY_PROGRAM

| Field | Type | Mô tả |
|-------|------|-------|
| loyalty_program_name | Data | Tên chương trình |
| loyalty_program_type | Select | Single Tier / Multiple Tier |
| from_date | Date | Ngày bắt đầu |
| to_date | Date | Ngày kết thúc |
| auto_opt_in | Check | Tự động cho tất cả KH |
| customer_group | Link | Lọc theo nhóm KH |
| customer_territory | Link | Lọc theo khu vực |
| conversion_factor | Float | 1 điểm = X VNĐ |
| expiry_duration | Int | Số ngày hết hạn |
| expense_account | Link | Tài khoản chi phí |
| collection_rules | Table | Danh sách tier |

#### LOYALTY_PROGRAM_COLLECTION (Tier)

| Field | Type | Mô tả |
|-------|------|-------|
| tier_name | Data | Tên hạng (Bronze/Silver/Gold/Platinum) |
| min_spent | Currency | Doanh số tối thiểu để vào hạng |
| collection_factor | Currency | X VNĐ = 1 điểm |

#### LOYALTY_POINT_ENTRY

| Field | Type | Mô tả |
|-------|------|-------|
| loyalty_program | Link | Chương trình loyalty |
| loyalty_program_tier | Data | Hạng tại thời điểm giao dịch |
| customer | Link | Khách hàng |
| invoice_type | Link | Loại chứng từ |
| invoice | Dynamic Link | Link tới Invoice |
| loyalty_points | Int | Số điểm (+/-) |
| purchase_amount | Currency | Giá trị mua hàng |
| expiry_date | Date | Ngày hết hạn điểm |
| posting_date | Date | Ngày giao dịch |

---

## 4. Công thức tính điểm

### 4.1. Công thức

```
ĐIỂM = GIÁ TRỊ INVOICE ÷ COLLECTION_FACTOR
```

### 4.2. Ví dụ

| Tier | collection_factor | Invoice 10,000,000 VNĐ | Điểm |
|------|-------------------|------------------------|------|
| Bronze | 10,000 | 10,000,000 ÷ 10,000 | 1,000 |
| Silver | 8,000 | 10,000,000 ÷ 8,000 | 1,250 |
| Gold | 6,000 | 10,000,000 ÷ 6,000 | 1,667 |
| Platinum | 5,000 | 10,000,000 ÷ 5,000 | 2,000 |

### 4.3. Cần xác nhận với khách hàng

| Tham số | Câu hỏi | Xác nhận |
|---------|---------|----------|
| collection_factor Bronze | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| collection_factor Silver | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| collection_factor Gold | Bao nhiêu VNĐ = 1 điểm? | ☐ |
| collection_factor Platinum | Bao nhiêu VNĐ = 1 điểm? | ☐ |

---

## 5. Quy đổi điểm sang tiền

### 5.1. Công thức

```
SỐ TIỀN GIẢM = SỐ ĐIỂM × CONVERSION_FACTOR
```

### 5.2. Ví dụ

- conversion_factor = 1,000 (1 điểm = 1,000 VNĐ)
- KH có 500 điểm
- Giảm giá = 500 × 1,000 = **500,000 VNĐ**

### 5.3. Cần xác nhận với khách hàng

| Câu hỏi | Xác nhận |
|---------|----------|
| Có cho dùng điểm đổi giảm giá? | ☐ |
| 1 điểm = bao nhiêu VNĐ? | ☐ |

---

## 6. Điều kiện lên hạng

### 6.1. Cách hoạt động

Hệ thống xác định hạng dựa trên `total_spent` của khách hàng:

```mermaid
flowchart TD
    A[Lấy total_spent từ Loyalty Point Entry] --> B{So sánh với min_spent}

    B -->|total_spent >= 0| C[Bronze]
    B -->|total_spent >= X1| D[Silver]
    B -->|total_spent >= X2| E[Gold]
    B -->|total_spent >= X3| F[Platinum]

    C --> G[Chọn tier cao nhất đạt điều kiện]
    D --> G
    E --> G
    F --> G
```

### 6.2. Ví dụ cấu hình

| Tier | min_spent |
|------|-----------|
| Bronze | 0 |
| Silver | 20,000,000 |
| Gold | 50,000,000 |
| Platinum | 100,000,000 |

**Ví dụ:**
- KH có total_spent = 55,000,000
- Đạt: Bronze (0), Silver (20M), Gold (50M)
- → Gán tier **Gold**

### 6.3. Cần xác nhận với khách hàng

| Tham số | Câu hỏi | Xác nhận |
|---------|---------|----------|
| min_spent Silver | Doanh số tối thiểu? | ☐ |
| min_spent Gold | Doanh số tối thiểu? | ☐ |
| min_spent Platinum | Doanh số tối thiểu? | ☐ |

---

## 7. Điểm hết hạn

### 7.1. Cách hoạt động

- Cấu hình `expiry_duration` trong Loyalty Program (số ngày)
- Khi tạo Loyalty Point Entry, hệ thống tính `expiry_date = posting_date + expiry_duration`
- Điểm hết hạn không còn khả dụng

### 7.2. Cần xác nhận với khách hàng

| Câu hỏi | Xác nhận |
|---------|----------|
| Điểm có hết hạn không? | ☐ |
| Nếu có, sau bao nhiêu ngày? | ☐ |

---

## 8. Tích hợp

### 8.1. Với Customer

```mermaid
flowchart LR
    A[Customer] --> B[Field: loyalty_program]
    B --> C[Link tới Loyalty Program]
    A --> D[Hiển thị điểm hiện tại]
```

### 8.2. Với Sales Invoice

```mermaid
sequenceDiagram
    actor User
    participant SI as Sales Invoice
    participant LP as Loyalty Program
    participant LPE as Loyalty Point Entry

    User->>SI: Tạo Sales Invoice
    SI->>LP: Lấy thông tin loyalty của Customer
    LP-->>SI: Trả về tier, collection_factor

    User->>SI: Submit Invoice
    SI->>LPE: Tạo entry tích điểm (+)

    Note over SI: Nếu KH dùng điểm
    SI->>LPE: Tạo entry tiêu điểm (-)
    SI->>SI: Giảm giá theo loyalty_amount
```

---

## 9. Quyền & Bảo mật

### 9.1. Phân quyền có sẵn

| Role | Loyalty Program | Loyalty Point Entry |
|------|-----------------|---------------------|
| System Manager | Full access | Full access |
| Accounts Manager | Read | Read |
| Accounts User | Read | Read |
| Auditor | Read | Read |

---

## 10. Hướng dẫn cấu hình

### Bước 1: Tạo Loyalty Program

1. Vào **Selling > Settings > Loyalty Program**
2. Điền thông tin:
   - Loyalty Program Name: "Nhật Minh Golf Club"
   - Loyalty Program Type: "Multiple Tier Program"
   - From Date: Ngày bắt đầu
   - Auto Opt In: ✅ (nếu áp dụng cho tất cả)

### Bước 2: Cấu hình Collection Rules

Thêm các tier vào bảng:

| Tier Name | Minimum Total Spent | Collection Factor |
|-----------|---------------------|-------------------|
| Bronze | 0 | (cần confirm) |
| Silver | (cần confirm) | (cần confirm) |
| Gold | (cần confirm) | (cần confirm) |
| Platinum | (cần confirm) | (cần confirm) |

### Bước 3: Cấu hình Redemption (nếu có)

- Conversion Factor: 1 điểm = X VNĐ
- Expiry Duration: X ngày
- Expense Account: Chọn tài khoản chi phí

### Bước 4: Gán cho Customer

- Nếu `auto_opt_in` = ✅ → Tự động áp dụng
- Nếu không → Vào Customer > chọn Loyalty Program

---

## 11. Câu hỏi cần clarify với khách hàng

| # | Câu hỏi | Ảnh hưởng đến |
|---|---------|---------------|
| 1 | collection_factor cho từng hạng? | Tính điểm |
| 2 | min_spent cho từng hạng? | Lên hạng |
| 3 | Có cho dùng điểm đổi giảm giá? | Redemption |
| 4 | 1 điểm = bao nhiêu VNĐ? | conversion_factor |
| 5 | Điểm có hết hạn không? Sau bao lâu? | expiry_duration |
| 6 | Áp dụng tự động cho tất cả KH? | auto_opt_in |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6 - Quản lý Tích điểm
**Nền tảng:** DCNET Core Loyalty Program
**Cập nhật:** 2026-01-13
