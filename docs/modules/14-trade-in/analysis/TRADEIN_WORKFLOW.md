# Module Thu cũ Đổi mới (Trade-in) - Workflow, ERD & UI

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5
> **Phiên bản:** 1.0.0 | **Cập nhật:** 13/01/2026

---

## 1. Workflow Diagram

### 1.1. Quy trình tổng quan

```mermaid
flowchart TD
    subgraph PHASE1["1. TIEP NHAN"]
        A["Khach mang SP cu den cua hang"] --> B["Nhan vien tiep nhan"]
        B --> C["Tao don Thu cu Doi moi"]
    end

    subgraph PHASE2["2. KIEM TRA VA DINH GIA"]
        C --> D["Kiem tra tinh trang SP cu"]
        D --> E{"SP du dieu kien?"}
        E -->|Khong| F["Tu choi thu"]
        E -->|Co| G["Dinh gia SP cu"]
        G --> H["Manager duyet gia"]
    end

    subgraph PHASE3["3. TINH TOAN"]
        H --> I["Chon SP moi cho khach"]
        I --> J["Ap dung Voucher"]
        J --> K["Tinh gia tri chenh lech"]
        K --> L["Gia moi - Gia cu - Voucher"]
    end

    subgraph PHASE4["4. XAC NHAN"]
        L --> M["Trinh bay cho khach"]
        M --> N{"Khach dong y?"}
        N -->|Khong| O["Khach tu choi"]
        N -->|Co| P["Xac nhan giao dich"]
    end

    subgraph PHASE5["5. HOAN THANH"]
        P --> Q["Nhan SP cu tu khach"]
        Q --> R["Xuat SP moi cho khach"]
        R --> S["Thu tien chenh lech"]
        S --> T["Cap nhat kho"]
        T --> U["Hoan thanh"]
    end

    F --> END["KET THUC"]
    O --> END
    U --> END
```

### 1.2. Quy trình tính giá trị chênh lệch

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 498-499)

```mermaid
flowchart LR
    A["Gia SP moi"] --> D["Phep tinh"]
    B["Gia thu SP cu"] --> D
    C["Voucher"] --> D
    D --> E["So tien KH thanh toan"]

    style A fill:#d4edda
    style B fill:#fff3cd
    style C fill:#d1ecf1
    style E fill:#f8d7da
```

**Công thức:**
```
Số tiền khách thanh toán = Giá SP mới - Giá thu SP cũ - Voucher (nếu có)
```

---

## 2. Entity Relationship Diagram (ERD)

### 2.1. ERD Tổng quan

```mermaid
erDiagram
    TRADEIN_ORDER ||--o| CUSTOMER : belongs_to
    TRADEIN_ORDER ||--|| OLD_PRODUCT : contains
    TRADEIN_ORDER ||--|| NEW_PRODUCT : contains
    TRADEIN_ORDER ||--o| VOUCHER : applies
    TRADEIN_ORDER ||--o| STAFF : handled_by
    TRADEIN_ORDER ||--o| BRANCH : at
    OLD_PRODUCT ||--o| PRODUCT : references
    NEW_PRODUCT ||--o| PRODUCT : references
    OLD_PRODUCT ||--o| INVENTORY : goes_to

    TRADEIN_ORDER {
        int id PK
        string order_code
        int customer_id FK
        string status
        decimal payment_amount
        string payment_method
        int staff_id FK
        int branch_id FK
        text notes
        datetime created_at
        datetime updated_at
    }

    OLD_PRODUCT {
        int id PK
        int tradein_order_id FK
        int product_id FK
        string condition
        decimal trade_price
        text condition_notes
        string photos
    }

    NEW_PRODUCT {
        int id PK
        int tradein_order_id FK
        int product_id FK
        decimal selling_price
    }

    CUSTOMER {
        int id PK
        string name
        string phone
        string email
    }

    PRODUCT {
        int id PK
        string name
        string sku
        decimal price
    }

    VOUCHER {
        int id PK
        string code
        decimal amount
    }
```

### 2.2. Mô tả các Entity

| Entity | Mô tả | Nguồn |
|--------|-------|-------|
| **TRADEIN_ORDER** | Đơn thu cũ đổi mới | Section 5.2.4 |
| **OLD_PRODUCT** | Thông tin SP cũ khách trả | Section 5.2.4, Line 492 |
| **NEW_PRODUCT** | Thông tin SP mới khách nhận | Section 5.2.4, Line 493 |
| **CUSTOMER** | Khách hàng | Section 4 |
| **PRODUCT** | Danh mục sản phẩm | Section 6 |
| **VOUCHER** | Mã giảm giá | Section 5.2.4, Line 499 |

---

## 3. State Diagram

### 3.1. Trạng thái đơn Trade-in (Đề xuất)

```mermaid
stateDiagram-v2
    [*] --> NEW

    NEW --> INSPECTION : Staff bat dau kiem tra
    NEW --> CANCELLED : Khach huy

    INSPECTION --> PRICED : Da dinh gia xong
    INSPECTION --> CANCELLED : SP khong dat

    PRICED --> CONFIRMED : Khach dong y gia
    PRICED --> CANCELLED : Khach tu choi

    CONFIRMED --> PROCESSING : Bat dau xu ly
    CONFIRMED --> CANCELLED : Khach doi y

    PROCESSING --> COMPLETED : Giao dich thanh cong
    PROCESSING --> CANCELLED : Loi xu ly

    COMPLETED --> [*]
    CANCELLED --> [*]

    NEW: Moi tao
    INSPECTION: Dang kiem tra
    PRICED: Da dinh gia
    CONFIRMED: Da xac nhan
    PROCESSING: Dang xu ly
    COMPLETED: Hoan thanh
    CANCELLED: Da huy
```

### 3.2. Ma trận chuyển trạng thái

| Từ | Đến | Điều kiện | Actor |
|----|-----|-----------|-------|
| NEW | INSPECTION | Bắt đầu kiểm tra SP cũ | Staff |
| NEW | CANCELLED | Khách hủy yêu cầu | Staff |
| INSPECTION | PRICED | Hoàn thành định giá | Staff/Manager |
| INSPECTION | CANCELLED | SP không đủ điều kiện | Staff |
| PRICED | CONFIRMED | Khách đồng ý giá | Staff |
| PRICED | CANCELLED | Khách từ chối giá | Staff |
| CONFIRMED | PROCESSING | Bắt đầu giao dịch | Staff |
| CONFIRMED | CANCELLED | Khách đổi ý | Staff/Manager |
| PROCESSING | COMPLETED | Giao dịch thành công | Staff |
| PROCESSING | CANCELLED | Lỗi xử lý | Manager |

---

## 4. UI Mockups

### 4.1. Danh sách đơn Trade-in

```
┌─────────────────────────────────────────────────────────────────────────┐
│ DANH SÁCH ĐƠN THU CŨ ĐỔI MỚI                         [+ Tạo đơn mới]   │
├─────────────────────────────────────────────────────────────────────────┤
│ 🔍 Tìm kiếm: [________________]  📅 Từ: [__/__/____] Đến: [__/__/____] │
│ Trạng thái: [Tất cả ▼]  Chi nhánh: [Tất cả ▼]                          │
├─────────────────────────────────────────────────────────────────────────┤
│ Mã đơn    │ Khách hàng   │ SP Cũ      │ SP Mới     │ Chênh lệch │ TT   │
├───────────┼──────────────┼────────────┼────────────┼────────────┼──────┤
│ TI-001    │ Nguyễn Văn A │ Driver     │ Driver     │ 9,500,000  │ ✅   │
│           │ 0901234567   │ Callaway   │ TaylorMade │            │      │
├───────────┼──────────────┼────────────┼────────────┼────────────┼──────┤
│ TI-002    │ Trần Thị B   │ Iron Set   │ Iron Set   │ 12,000,000 │ 🟡   │
│           │ 0912345678   │ Titleist   │ Mizuno     │            │      │
├───────────┼──────────────┼────────────┼────────────┼────────────┼──────┤
│ TI-003    │ Lê Văn C     │ Putter     │ Putter     │ 3,500,000  │ ⏳   │
│           │ 0923456789   │ Odyssey    │ Scotty     │            │      │
└─────────────────────────────────────────────────────────────────────────┘
│                              [1] [2] [3] ... [10]                       │
└─────────────────────────────────────────────────────────────────────────┘

Trạng thái: ✅ Hoàn thành  🟡 Đang xử lý  ⏳ Chờ xác nhận  ❌ Đã hủy
```

### 4.2. Form tạo đơn Trade-in

```
┌─────────────────────────────────────────────────────────────────────────┐
│ TẠO ĐƠN THU CŨ ĐỔI MỚI                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ THÔNG TIN KHÁCH HÀNG                                                   │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ Khách hàng: [Tìm kiếm khách hàng...          ▼] [+ Tạo mới]    │    │
│ │ SĐT: 0901234567          Email: customer@email.com              │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│ THÔNG TIN SẢN PHẨM CŨ (KHÁCH TRẢ)                                      │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ Tên SP:     [Driver Callaway Big Bertha                    ]    │    │
│ │ Thương hiệu: [Callaway          ▼]                              │    │
│ │ Tình trạng: [Tốt ▼]    ○ Mới  ● Tốt  ○ Trung bình  ○ Kém       │    │
│ │ Giá thu:    [5,000,000         ] VNĐ                            │    │
│ │ Ghi chú:    [Đầu gậy còn tốt, grip cần thay              ]     │    │
│ │ Hình ảnh:   [📷 Thêm ảnh]                                       │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│ THÔNG TIN SẢN PHẨM MỚI (KHÁCH NHẬN)                                    │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ Sản phẩm:   [Tìm kiếm sản phẩm...            ▼]                │    │
│ │ Tên:        Driver TaylorMade Stealth 2                         │    │
│ │ Giá bán:    15,000,000 VNĐ                                      │    │
│ │ Tồn kho:    5 (Chi nhánh HCM)                                   │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│ TÍNH TOÁN                                                              │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ Giá SP mới:         15,000,000 VNĐ                              │    │
│ │ Giá thu SP cũ:     - 5,000,000 VNĐ                              │    │
│ │ Voucher:           [SUMMER2026  ] -500,000 VNĐ [Áp dụng]        │    │
│ │ ─────────────────────────────────                               │    │
│ │ KHÁCH THANH TOÁN:   9,500,000 VNĐ                               │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│ Ghi chú đơn hàng:                                                      │
│ ┌─────────────────────────────────────────────────────────────────┐    │
│ │ [                                                            ]  │    │
│ └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│                              [Hủy]  [Lưu nháp]  [Tạo đơn]              │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3. Chi tiết đơn Trade-in

```
┌─────────────────────────────────────────────────────────────────────────┐
│ CHI TIẾT ĐƠN THU CŨ ĐỔI MỚI #TI-001                                    │
│ Trạng thái: [✅ Hoàn thành]                    [Cập nhật] [In] [Hủy]   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│ ┌── KHÁCH HÀNG ─────────────┐  ┌── THÔNG TIN ĐƠN ──────────────────┐  │
│ │ Tên: Nguyễn Văn A         │  │ Mã đơn: TI-001                    │  │
│ │ SĐT: 0901234567           │  │ Ngày tạo: 13/01/2026 10:30        │  │
│ │ Email: nva@email.com      │  │ NV xử lý: Trần Thị Sale           │  │
│ └───────────────────────────┘  │ Chi nhánh: HCM - Quận 1           │  │
│                                └────────────────────────────────────┘  │
│                                                                         │
│ ┌── SẢN PHẨM CŨ ────────────────────────────────────────────────────┐ │
│ │ Tên: Driver Callaway Big Bertha                                    │ │
│ │ Thương hiệu: Callaway                                              │ │
│ │ Tình trạng: Tốt                                                    │ │
│ │ Giá thu: 5,000,000 VNĐ                                             │ │
│ │ Ghi chú: Đầu gậy còn tốt, grip cần thay                           │ │
│ │ [📷 Xem ảnh]                                                       │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌── SẢN PHẨM MỚI ───────────────────────────────────────────────────┐ │
│ │ Tên: Driver TaylorMade Stealth 2                                   │ │
│ │ SKU: TM-STL2-001                                                   │ │
│ │ Giá bán: 15,000,000 VNĐ                                            │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌── THANH TOÁN ─────────────────────────────────────────────────────┐ │
│ │ Giá SP mới:         15,000,000 VNĐ                                 │ │
│ │ Giá thu SP cũ:     - 5,000,000 VNĐ                                 │ │
│ │ Voucher (SUMMER2026): -500,000 VNĐ                                 │ │
│ │ ───────────────────────────────────                                │ │
│ │ TỔNG THANH TOÁN:     9,500,000 VNĐ                                 │ │
│ │ Phương thức: Chuyển khoản                                          │ │
│ └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│ ┌── LỊCH SỬ ────────────────────────────────────────────────────────┐ │
│ │ 13/01/2026 10:30 - Tạo đơn (Trần Thị Sale)                        │ │
│ │ 13/01/2026 10:35 - Kiểm tra SP cũ (Trần Thị Sale)                 │ │
│ │ 13/01/2026 10:45 - Định giá: 5,000,000 VNĐ (Nguyễn Văn Manager)   │ │
│ │ 13/01/2026 11:00 - Khách xác nhận đồng ý                          │ │
│ │ 13/01/2026 11:15 - Hoàn thành giao dịch (Trần Thị Sale)           │ │
│ └────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Sequence Diagram - Tạo đơn Trade-in

```mermaid
sequenceDiagram
    participant C as Khach hang
    participant S as Sales Staff
    participant SYS as He thong
    participant M as Manager
    participant INV as Kho

    C->>S: Mang SP cu den cua hang
    S->>SYS: Tao don Thu cu Doi moi
    SYS-->>S: Hien thi form tao don

    S->>SYS: Nhap thong tin khach hang
    S->>SYS: Nhap thong tin SP cu
    S->>SYS: Nhap gia thu SP cu
    S->>M: Yeu cau duyet gia
    M-->>S: Duyet gia thu

    S->>SYS: Chon SP moi
    SYS->>INV: Kiem tra ton kho
    INV-->>SYS: Con hang

    S->>SYS: Ap dung voucher
    SYS-->>S: Tinh gia tri chenh lech

    S->>C: Trinh bay gia tri chenh lech
    C-->>S: Dong y

    S->>SYS: Xac nhan giao dich
    SYS->>INV: Nhap SP cu, Xuat SP moi
    INV-->>SYS: Cap nhat thanh cong

    S->>C: Nhan SP cu, Giao SP moi
    C->>S: Thanh toan tien chenh lech
    S->>SYS: Hoan thanh don
    SYS-->>S: Don hoan thanh
```

---

## 6. Integration Points

### 6.1. Tích hợp với các module

```mermaid
flowchart TB
    subgraph TRADEIN["Module Trade-in"]
        TI["Don Thu cu Doi moi"]
    end

    subgraph CUSTOMER["Module Khach hang"]
        CUS["Khach hang"]
    end

    subgraph PRODUCT["Module San pham"]
        PRD["San pham"]
    end

    subgraph INVENTORY["Module Kho"]
        INV["Ton kho"]
        WH_OLD["Kho hang cu"]
    end

    subgraph PROMOTION["Module Khuyen mai"]
        VCH["Voucher"]
    end

    subgraph RESELL["Module Resell"]
        RS["Ban lai SP cu"]
    end

    CUS --> TI
    PRD --> TI
    VCH --> TI
    TI --> INV
    TI --> WH_OLD
    WH_OLD --> RS
```

### 6.2. Data Flow

| Từ Module | Đến Module | Dữ liệu | Hành động |
|-----------|------------|---------|-----------|
| Khách hàng | Trade-in | Customer info | Lookup |
| Sản phẩm | Trade-in | Product info | Lookup |
| Trade-in | Kho | SP cũ | Nhập kho |
| Trade-in | Kho | SP mới | Xuất kho |
| Voucher | Trade-in | Discount | Áp dụng |
| Trade-in | Resell | SP cũ | Bán lại |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5
**Lưu ý:** Workflow và trạng thái được **đề xuất** dựa trên quy trình nghiệp vụ. UI mockups là bản phác thảo, cần xác nhận với khách hàng.
