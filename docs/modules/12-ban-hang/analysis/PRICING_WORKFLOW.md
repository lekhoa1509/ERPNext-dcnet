# Module Pricing - Đặc tả Workflow & ERD

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2, Bước 2-3 (Quản lý Bán hàng - Bảng giá & Chiết khấu)
> **Lưu ý:** Đây là đặc tả YÊU CẦU, code phải làm theo đặc tả này

---

## 1. Định nghĩa

> Module **Pricing** quản lý bảng giá niêm yết và chính sách chiết khấu cho kênh bán buôn (B2B) và bán lẻ (B2C).

**Phạm vi:**
- Bảng giá bán niêm yết (Wholesale & Retail)
- Chính sách chiết khấu bán buôn
- Chính sách chiết khấu bán lẻ (bao gồm chiết khấu đặc biệt)

---

## 2. ERD - Entity Relationship Diagram

### 2.1. ERD Overview

```mermaid
erDiagram
    PRICE_LIST ||--o{ ITEM_PRICE : contains
    DISCOUNT_POLICY ||--o{ DISCOUNT_POLICY_ITEM : contains

    PRICE_LIST {
        VARCHAR name PK
        VARCHAR price_list_name
        VARCHAR status
        DATE effective_date
        DATE expiry_date
        VARCHAR price_list_type
        VARCHAR currency
        INT selling
        INT buying
        VARCHAR created_by
        VARCHAR approved_by
        DATETIME approved_date
        TEXT description
        TEXT attachment
    }

    ITEM_PRICE {
        VARCHAR name PK
        VARCHAR parent FK
        VARCHAR item_code FK
        VARCHAR item_name
        DECIMAL price_list_rate
        VARCHAR uom
        TEXT note
    }

    DISCOUNT_POLICY {
        VARCHAR name PK
        VARCHAR policy_name
        VARCHAR status
        DATE apply_date
        DATE expiry_date
        VARCHAR policy_type
        VARCHAR customer FK
        VARCHAR customer_group FK
        VARCHAR created_by
        VARCHAR approved_by
        DATETIME approved_date
        TEXT description
        TEXT attachment
    }

    DISCOUNT_POLICY_ITEM {
        VARCHAR name PK
        VARCHAR parent FK
        VARCHAR item_code FK
        VARCHAR item_name
        DECIMAL discount_percentage
        DECIMAL min_qty
        DECIMAL max_qty
    }

    ITEM {
        VARCHAR item_code PK
        VARCHAR item_name
        VARCHAR item_group
    }

    CUSTOMER {
        VARCHAR name PK
        VARCHAR customer_name
        VARCHAR customer_group
    }

    SALES_ORDER {
        VARCHAR name PK
        VARCHAR customer FK
        DATE transaction_date
        VARCHAR price_list FK
        VARCHAR discount_policy FK
    }

    SALES_ORDER_ITEM {
        VARCHAR name PK
        VARCHAR parent FK
        VARCHAR item_code FK
        DECIMAL qty
        DECIMAL rate
        DECIMAL discount_percentage
        DECIMAL discount_amount
    }

    ITEM_PRICE }o--|| ITEM : references
    DISCOUNT_POLICY_ITEM }o--|| ITEM : references
    DISCOUNT_POLICY }o--o| CUSTOMER : "applies to"
    SALES_ORDER }o--|| CUSTOMER : "belongs to"
    SALES_ORDER }o--o| PRICE_LIST : "uses"
    SALES_ORDER }o--o| DISCOUNT_POLICY : "uses"
    SALES_ORDER ||--o{ SALES_ORDER_ITEM : contains
    SALES_ORDER_ITEM }o--|| ITEM : references
```

### 2.2. Mô tả các bảng chính

#### Bảng: `tabPrice List` (Bảng giá)

**Quan hệ:**
- 1 Price List → N Item Price (1-N)
- 1 Item → N Item Price (1-N, qua nhiều bảng giá)
- 1 Price List → N Sales Order (1-N, reference)

**Trường quan trọng:**
- `status`: Draft | Pending Approval | Approved | Active | Expired | Cancelled
- `price_list_type`: Wholesale | Retail
- `effective_date`, `expiry_date`: Xác định khoảng thời gian hiệu lực

#### Bảng: `tabDiscount Policy` (Chính sách chiết khấu)

**Quan hệ:**
- 1 Discount Policy → N Discount Policy Item (1-N)
- 1 Customer → N Discount Policy (1-N, áp dụng nhiều chính sách)
- 1 Discount Policy → N Sales Order (1-N, reference)

**Trường quan trọng:**
- `status`: Draft | Pending Approval | Approved | Active | Expired | Cancelled
- `policy_type`: Wholesale | Retail
- `customer`, `customer_group`: Đối tượng áp dụng (Buôn), NULL nếu Lẻ

---

## 3. Workflow - Bảng giá (Price List)

### 3.1. State Diagram - Bảng giá

```mermaid
stateDiagram-v2
    [*] --> draft: Tao moi

    draft --> pending_approval: Gui duyet
    draft --> cancelled: Huy bo

    pending_approval --> approved: Phe duyet
    pending_approval --> draft: Tu choi
    pending_approval --> cancelled: Huy bo

    approved --> active: Den ngay hieu luc
    approved --> cancelled: Huy truoc ngay HL

    active --> expired: Het hieu luc
    active --> cancelled: Huy khan cap

    expired --> [*]
    cancelled --> [*]

    note right of draft
        Nhan vien KD
        Nhap thong tin bang gia
    end note

    note right of pending_approval
        Cho Truong phong KD
        hoac Giam doc duyet
    end note

    note right of active
        Tu dong ap dung
        khi den ngay hieu luc
    end note

    note right of expired
        Het han, khong the chon
        trong don hang/hoa don
    end note
```

### 3.2. Flowchart - Quy trình phê duyệt bảng giá

```mermaid
flowchart TD
    Start([NV KD tao bang gia]) --> Draft[Trang thai: Draft]

    Draft --> EnterInfo[Nhap thong tin chung:<br/>Ten, Ngay hieu luc, Loai, Tien te]
    EnterInfo --> EnterItems[Nhap chi tiet:<br/>San pham, Gia ban]
    EnterItems --> Attach[Dinh kem file quyet dinh gia]

    Attach --> Submit[NV KD gui phe duyet]
    Submit --> Validate{Validate<br/>du lieu}

    Validate -->|Loi| FixErrors[Sua loi]
    FixErrors --> Submit

    Validate -->|OK| Pending[Trang thai: Pending Approval]
    Pending --> Notify1[Gui thong bao den Truong phong KD]

    Notify1 --> Review[Truong phong KD xem xet]
    Review --> Decision{Quyet dinh}

    Decision -->|Tu choi| Reject[Tra lai Draft + Ly do]
    Reject --> Draft

    Decision -->|Phe duyet| Approved[Trang thai: Approved]
    Approved --> Notify2[Gui thong bao den NV KD]

    Approved --> Schedule[Len lich tu dong chuyen Active]
    Schedule --> Wait[Cho den ngay hieu luc]

    Wait --> CheckDate{Ngay hien tai<br/>= Ngay HL?}
    CheckDate -->|Chua den| Wait
    CheckDate -->|Den roi| Active[Trang thai: Active]

    Active --> Notify3[Gui thong bao: Bang gia da co hieu luc]
    Active --> UseInSO[Co the chon trong don hang/hoa don]

    Active --> CheckExpiry{Het han?}
    CheckExpiry -->|Chua| Active
    CheckExpiry -->|Roi| Expired[Trang thai: Expired]

    Expired --> End([Ket thuc])

    style Draft fill:#cbd5e1
    style Pending fill:#fbbf24
    style Approved fill:#4ade80
    style Active fill:#22c55e
    style Expired fill:#94a3b8
    style Reject fill:#fca5a1
```

### 3.3. Sequence Diagram - Tạo và phê duyệt bảng giá

```mermaid
sequenceDiagram
    actor NVKD as NV Kinh doanh
    participant UI as Web UI
    participant API as API Server
    participant DB as Database
    participant JOB as Scheduler
    actor TPKD as Truong phong KD
    participant EMAIL as Email Service

    NVKD->>UI: 1. Tao bang gia moi
    UI->>API: POST /api/price-list
    API->>DB: INSERT Price List (status=Draft)
    DB-->>API: OK
    API-->>UI: Tra ve ID bang gia
    UI-->>NVKD: Hien thi form

    NVKD->>UI: 2. Nhap san pham va gia
    UI->>API: POST /api/price-list/{id}/items
    API->>DB: INSERT Item Price (multiple)
    DB-->>API: OK

    NVKD->>UI: 3. Dinh kem file
    UI->>API: POST /api/price-list/{id}/attachment
    API->>DB: UPDATE attachment field
    DB-->>API: OK

    NVKD->>UI: 4. Gui phe duyet
    UI->>API: PUT /api/price-list/{id}/submit
    API->>API: Validate (gia > 0, co san pham...)
    API->>DB: UPDATE status=Pending Approval
    DB-->>API: OK
    API->>EMAIL: Gui email den Truong phong KD
    EMAIL-->>TPKD: Thong bao: Bang gia cho duyet

    TPKD->>UI: 5. Xem bang gia
    UI->>API: GET /api/price-list/{id}
    API->>DB: SELECT Price List + Items
    DB-->>API: Du lieu bang gia
    API-->>UI: JSON
    UI-->>TPKD: Hien thi thong tin

    TPKD->>UI: 6. Phe duyet
    UI->>API: PUT /api/price-list/{id}/approve
    API->>DB: UPDATE status=Approved, approved_by, approved_date
    DB-->>API: OK
    API->>JOB: Len lich chuyen Active khi den ngay HL
    JOB-->>API: Job created
    API->>EMAIL: Gui email den NV KD
    EMAIL-->>NVKD: Thong bao: Bang gia da duyet

    Note over JOB: Scheduled Job chay moi ngay 00:00

    JOB->>DB: SELECT Price List WHERE status=Approved AND effective_date=TODAY
    DB-->>JOB: Danh sach bang gia
    JOB->>DB: UPDATE status=Active
    DB-->>JOB: OK
    JOB->>EMAIL: Gui email: Bang gia da co hieu luc
```

---

## 4. Workflow - Chính sách chiết khấu (Discount Policy)

### 4.1. State Diagram - Chính sách chiết khấu

```mermaid
stateDiagram-v2
    [*] --> draft: Tao moi

    draft --> pending_approval: Gui duyet
    draft --> cancelled: Huy bo

    pending_approval --> approved: Phe duyet
    pending_approval --> draft: Tu choi
    pending_approval --> cancelled: Huy bo

    approved --> active: Den ngay ap dung
    approved --> cancelled: Huy truoc ngay ap dung

    active --> expired: Het hieu luc
    active --> cancelled: Huy khan cap

    expired --> [*]
    cancelled --> [*]

    note right of active
        Ap dung tu dong
        Tich hop vao don hang
    end note
```

### 4.2. Flowchart - Áp dụng chiết khấu vào đơn hàng

```mermaid
flowchart TD
    Start([NV KD tao don hang]) --> SelectCust[Chon khach hang]

    SelectCust --> SelectItem[Chon san pham]
    SelectItem --> GetPrice[He thong tu dong lay gia<br/>tu bang gia Active]

    GetPrice --> FindDiscount{Tim chinh sach<br/>chiet khau Active?}

    FindDiscount -->|Tim thay| CheckCust{Kiem tra<br/>doi tuong?}
    FindDiscount -->|Khong tim thay| ManualDisc[Cho phep nhap tay % chiet khau]

    CheckCust -->|Khach hang khop| CheckItem{San pham<br/>co trong CS?}
    CheckCust -->|Khach hang khong khop| ManualDisc

    CheckItem -->|Co| ApplyDisc[Ap dung % chiet khau tu chinh sach]
    CheckItem -->|Khong| ManualDisc

    ApplyDisc --> CalcDisc[Tinh tien chiet khau:<br/>Tien CK = Thanh tien x %CK]
    ManualDisc --> CalcDisc

    CalcDisc --> CalcFinal["Tinh thanh tien sau CK:<br/>Thanh tien sau CK = Thanh tien - Tien CK"]

    CalcFinal --> SaveRef[Luu tham chieu:<br/>- So bang gia<br/>- So chinh sach chiet khau]

    SaveRef --> End([Hoan thanh don hang])

    style ApplyDisc fill:#4ade80
    style ManualDisc fill:#fbbf24
    style CalcFinal fill:#22c55e
```

---

## 5. Data Flow - Tích hợp với các module khác

### 5.1. Tích hợp với Sales Order (Đơn đặt hàng bán)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 4 (Lines 86-100)

```mermaid
flowchart LR
    subgraph Input
        PL[Price List Active]
        DP[Discount Policy Active]
        CUST[Khach hang]
        ITEM[San pham]
    end

    subgraph "Sales Order"
        SO[Sales Order]
        SOI[Sales Order Item]
    end

    subgraph Output
        PRICE[Don gia truoc CK]
        DISC[% Chiet khau]
        AMOUNT[Thanh tien sau CK]
    end

    PL -->|Lay gia| PRICE
    DP -->|Lay % CK| DISC

    CUST --> SO
    ITEM --> SOI
    SO --> SOI

    PRICE --> SOI
    DISC --> SOI

    SOI --> AMOUNT

    style SO fill:#3b82f6
    style SOI fill:#60a5fa
```

**Quy tắc:**
1. Hệ thống tự động tìm bảng giá Active theo loại khách hàng (Buôn/Lẻ)
2. Hệ thống tự động tìm chính sách chiết khấu Active theo khách hàng và sản phẩm
3. Nếu không tìm thấy chính sách, cho phép nhập tay % chiết khấu
4. Thông tin đơn hàng bao gồm:
   - Số bảng giá
   - Số chính sách chiết khấu
   - % chiết khấu
   - Tiền chiết khấu
   - Đơn giá trước/sau chiết khấu
   - Thành tiền trước/sau chiết khấu

### 5.2. Tích hợp với Delivery Order (Lệnh xuất hàng)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 6 (Lines 110-135)

```mermaid
flowchart LR
    SO[Sales Order] -->|Ke thua| DO[Delivery Order]

    subgraph "Du lieu ke thua"
        PRICE[Don gia]
        DISC[Chiet khau]
        REF[Tham chieu bang gia/chinh sach]
    end

    SO --> PRICE
    SO --> DISC
    SO --> REF

    PRICE --> DO
    DISC --> DO
    REF --> DO

    style DO fill:#3b82f6
```

**Quy tắc:**
- Lệnh xuất kế thừa 100% thông tin giá và chiết khấu từ đơn hàng
- Không cho phép sửa giá trên lệnh xuất (phân quyền)

### 5.3. Tích hợp với Sales Invoice (Hóa đơn bán buôn)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 9 (Lines 164-182)

```mermaid
flowchart TD
    DO[Delivery Order] --> INV[Sales Invoice]

    INV --> Auto[Tu dong lay bang gia/chinh sach<br/>theo ngay hoa don]

    Auto --> Compare{So sanh gia<br/>voi lenh xuat}

    Compare -->|Khop| OK[Hoa don hop le]
    Compare -->|Khong khop| Warning[Canh bao: Gia khac nhau]

    Warning --> Manual[Yeu cau nguoi dung xac nhan]
    Manual --> OK

    OK --> Save[Luu hoa don]

    style Warning fill:#fbbf24
    style OK fill:#4ade80
```

**Quy tắc:**
1. Tự động lấy số bảng giá, số chính sách chiết khấu theo ngày hóa đơn
2. **Cảnh báo** nếu giá bán trên lệnh xuất khác với giá bán trên hóa đơn
3. Yêu cầu xác nhận nếu có sự khác biệt

### 5.4. Tích hợp với POS Invoice (Hóa đơn bán lẻ)

**Nguồn:** ERP_SPECIFICATION.md Section 2, Bước 3 (Quy trình Bán lẻ) (Lines 254-265)

```mermaid
flowchart TD
    Start([Nhan vien ban hang<br/>tao hoa don le]) --> SelectItem[Chon san pham]

    SelectItem --> GetPrice[Tu dong lay gia<br/>tu bang gia Retail Active]

    GetPrice --> GetPolicy[Tu dong lay chinh sach<br/>chiet khau Retail Active]

    GetPolicy --> CalcPolicy["Tinh tien CK theo chinh sach:<br/>Tien CK = Thanh tien x %CK"]

    CalcPolicy --> SpecialDisc{Nhan vien cap<br/>CK dac biet?}

    SpecialDisc -->|Khong| Final1[Thanh tien sau CK]
    SpecialDisc -->|Co| CalcSpecial["Tinh CK dac biet:<br/>Tien CK DB = (Thanh tien - Tien CK CS) x %CK DB"]

    CalcSpecial --> Final2[Thanh tien cuoi cung]

    Final1 --> Save[Luu hoa don]
    Final2 --> Save

    Save --> End([Hoan thanh])

    style GetPrice fill:#3b82f6
    style GetPolicy fill:#60a5fa
    style CalcSpecial fill:#fbbf24
    style Final2 fill:#22c55e
```

**Công thức chiết khấu đặc biệt:**
```
Tiền chiết khấu đặc biệt = (Tiền hàng trước CK - Tiền CK theo chính sách) × Tỷ lệ CK đặc biệt
```

**Ví dụ:**
- Giá niêm yết: 10,000,000 VND
- CK theo chính sách (10%): 1,000,000 VND
- Giá sau CK CS: 9,000,000 VND
- CK đặc biệt (5%): 9,000,000 × 5% = 450,000 VND
- **Giá cuối cùng: 8,550,000 VND**

---

## 6. Ma trận chuyển trạng thái

### 6.1. Ma trận chuyển trạng thái - Bảng giá

| Từ \ Đến | Draft | Pending Approval | Approved | Active | Expired | Cancelled |
|----------|-------|------------------|----------|--------|---------|-----------|
| **Draft** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **Pending Approval** | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Approved** | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| **Active** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **Expired** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Cancelled** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

**Giải thích:**
- ✅ = Cho phép chuyển
- ❌ = Không cho phép chuyển

### 6.2. Điều kiện chuyển trạng thái

| Chuyển trạng thái | Điều kiện | Người thực hiện | Hành động sau chuyển |
|-------------------|-----------|-----------------|----------------------|
| **Draft → Pending Approval** | - Có ít nhất 1 sản phẩm<br/>- Giá > 0<br/>- Ngày hiệu lực >= Ngày hiện tại | NV KD, TP KD, GD | Gửi thông báo đến người phê duyệt |
| **Pending Approval → Approved** | - Người duyệt có quyền | TP KD, GD | Lên lịch tự động Active |
| **Pending Approval → Draft** | - Người duyệt từ chối<br/>- Nhập lý do | TP KD, GD | Gửi thông báo lý do từ chối |
| **Approved → Active** | - Ngày hiện tại = Ngày hiệu lực | System (Auto) | Gửi thông báo: Bảng giá đã Active |
| **Active → Expired** | - Ngày hiện tại > Ngày hết hiệu lực<br/>- HOẶC: Có bảng giá mới thay thế | System (Auto) | Gửi thông báo: Bảng giá đã hết hạn |
| **Any → Cancelled** | - Người hủy có quyền cao<br/>- Nhập lý do hủy | TP KD, GD | Gửi thông báo lý do hủy |

---

## 7. Dashboard và Báo cáo

### 7.1. Dashboard Trạng thái

```mermaid
graph LR
    subgraph "Bang gia"
        D1[Draft: 3]
        P1["Pending: 2"]
        A1[Approved: 1]
        AC1[Active: 5]
        E1[Expired: 12]
    end

    subgraph "Chinh sach chiet khau"
        D2[Draft: 2]
        P2["Pending: 1"]
        A2[Approved: 0]
        AC2[Active: 4]
        E2[Expired: 8]
    end

    style D1 fill:#cbd5e1
    style P1 fill:#fbbf24
    style A1 fill:#4ade80
    style AC1 fill:#22c55e
    style E1 fill:#94a3b8

    style D2 fill:#cbd5e1
    style P2 fill:#fbbf24
    style A2 fill:#4ade80
    style AC2 fill:#22c55e
    style E2 fill:#94a3b8
```

### 7.2. Báo cáo lịch sử giá theo sản phẩm

**Mục đích:** Xem giá của 1 sản phẩm thay đổi như thế nào qua thời gian

**Dữ liệu:**
- Sản phẩm: "TaylorMade Stealth 2 Driver"
- Thời gian: Q1/2024 → Q4/2025

| Ngày hiệu lực | Số bảng giá | Giá bán (VND) | Thay đổi (%) | Người lập |
|---------------|-------------|---------------|--------------|-----------|
| 01/01/2024 | PL-2024-001 | 15,000,000 | - | Nguyễn Văn A |
| 01/04/2024 | PL-2024-002 | 14,500,000 | -3.3% | Nguyễn Văn A |
| 01/07/2024 | PL-2024-003 | 14,000,000 | -3.4% | Trần Thị B |
| 01/10/2024 | PL-2024-004 | 13,500,000 | -3.6% | Trần Thị B |
| 01/01/2025 | PL-2025-001 | 13,000,000 | -3.7% | Lê Văn C |

**Biểu đồ:** Line chart thể hiện xu hướng giảm giá

### 7.3. Báo cáo hiệu quả chiết khấu

**Mục đích:** Đánh giá hiệu quả của các chính sách chiết khấu

**Dữ liệu:**

| Chính sách | Khách hàng | Doanh số (VND) | Tiền CK (VND) | % CK | Số đơn hàng |
|-----------|------------|----------------|---------------|------|-------------|
| DP-2025-001 | Đại lý A | 500,000,000 | 50,000,000 | 10% | 25 |
| DP-2025-002 | Đại lý B | 300,000,000 | 45,000,000 | 15% | 18 |
| DP-2025-003 | Nhóm VIP | 800,000,000 | 80,000,000 | 10% | 42 |

**Phân tích:**
- Top 3 khách hàng được hưởng chiết khấu cao nhất
- Tỷ lệ đơn hàng có áp dụng chiết khấu: 87%
- Tổng tiền chiết khấu trong tháng: 175,000,000 VND

---

## 8. Quy tắc nghiệp vụ (Business Rules)

### 8.1. Bảng giá

1. **Hiệu lực:**
   - Ngày hiệu lực phải >= Ngày hiện tại (khi tạo mới)
   - Ngày hết hiệu lực phải > Ngày hiệu lực (nếu có)

2. **Duy nhất:**
   - Có thể có nhiều bảng giá Active cùng lúc (phân biệt theo loại: Buôn/Lẻ)
   - Hệ thống ưu tiên bảng giá có Ngày hiệu lực gần nhất

3. **Sản phẩm:**
   - Mỗi sản phẩm chỉ xuất hiện 1 lần trong 1 bảng giá
   - Giá bán phải > 0

4. **Phê duyệt:**
   - Bảng giá Draft không thể sử dụng trong đơn hàng/hóa đơn
   - Chỉ bảng giá Active mới có thể chọn

5. **Hủy bỏ:**
   - Nếu bảng giá đang được sử dụng trong đơn hàng/hóa đơn chưa hoàn thành → Cần quyền Giám đốc để hủy

### 8.2. Chính sách chiết khấu

1. **Đối tượng:**
   - Chiết khấu Buôn: Phải chỉ định Khách hàng hoặc Nhóm khách hàng
   - Chiết khấu Lẻ: Áp dụng cho tất cả khách lẻ

2. **Tỷ lệ:**
   - Tỷ lệ chiết khấu: 0% ≤ % ≤ 100%
   - Tỷ lệ chiết khấu đặc biệt (Bán lẻ): Theo quyền hạn nhân viên

3. **Áp dụng:**
   - Nếu 1 khách hàng có nhiều chính sách Active → Ưu tiên chính sách có % chiết khấu cao nhất
   - Nếu không chọn chính sách → Cho phép nhập tay % chiết khấu

4. **Tích hợp:**
   - Chiết khấu áp dụng trên giá từ bảng giá (không phải giá nhập tay)
   - Công thức: `Thành tiền sau CK = Thành tiền trước CK - (Thành tiền trước CK × % CK)`

---

## 9. Câu hỏi cần làm rõ

### 9.1. Hiệu lực bảng giá

❓ **Hỏi:** Có cho phép nhiều bảng giá Active cùng lúc không?
- Nếu có: Ưu tiên theo thứ tự nào?
- Nếu không: Có tự động Expire bảng giá cũ không?

### 9.2. Chiết khấu theo số lượng

❓ **Hỏi:** Có chiết khấu theo số lượng mua không? (VD: Mua >= 100 sp giảm 10%)

### 9.3. Chiết khấu kết hợp

❓ **Hỏi:** Có cho phép áp dụng nhiều chính sách chiết khấu cùng lúc không?
❓ **Hỏi:** Thứ tự áp dụng chiết khấu như thế nào? (Nối tiếp hay song song)

### 9.4. Giá theo kho

❓ **Hỏi:** Giá có khác nhau theo kho không? (VD: Kho trung tâm vs Chi nhánh)

### 9.5. Giá theo tiền tệ

❓ **Hỏi:** Có nhiều bảng giá theo tiền tệ không? (VND, USD...)
❓ **Hỏi:** Tỷ giá quy đổi lấy từ đâu?

---

**Tổng kết:**
- **2 entity chính:** Price List, Discount Policy
- **Workflow:** Draft → Pending Approval → Approved → Active → Expired
- **Tích hợp:** Sales Order, Delivery Order, Sales Invoice, POS Invoice
- **Business Rules:** Đảm bảo tính nhất quán giữa các chứng từ
- **5 nhóm câu hỏi** cần làm rõ với khách hàng
