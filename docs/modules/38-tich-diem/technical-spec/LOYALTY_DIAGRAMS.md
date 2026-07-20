# Module Loyalty - Diagrams

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6 - Quản lý Tích điểm
> **Phiên bản:** 1.0.0
> **Nền tảng:** DCNET Core Loyalty Program (có sẵn)

---

## 1. ERD - Entity Relationship Diagram (DCNET Core)

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

---

## 2. Workflow tổng quan

```mermaid
flowchart TD
    A[Khách hàng] --> B{Có loyalty_program?}

    B -->|Chưa| C[Gán Loyalty Program]
    B -->|Rồi| D[Đã có program]

    C --> E[Mua hàng - Sales Invoice]
    D --> E

    E --> F[Submit Invoice]
    F --> G[Tính total_spent của Customer]

    G --> H{Xác định tier theo min_spent}
    H --> I[Gán tier phù hợp]

    I --> J[Tính điểm theo collection_factor]
    J --> K[Tạo Loyalty Point Entry]

    K --> L{Invoice kế tiếp}
    L --> E

    style C fill:#81aef7
    style K fill:#a7fab9
```

---

## 3. Quy trình tích điểm

```mermaid
flowchart LR
    A[Sales Invoice Submit] --> B[Lấy Customer]
    B --> C[Lấy Loyalty Program]
    C --> D[Tính total_spent của Customer]

    D --> E{Xác định tier}
    E --> F[Lấy collection_factor của tier]

    F --> G[Tính điểm]
    G --> H["ĐIỂM = Invoice Amount ÷ Collection Factor"]

    H --> I[Tạo Loyalty Point Entry]
    I --> J[Ghi expiry_date nếu có]

    style A fill:#a7fab9
    style I fill:#a7fab9
```

---

## 4. Quy trình sử dụng điểm

```mermaid
flowchart TD
    A[Tạo Sales Invoice] --> B[Chọn Customer]
    B --> C[Lấy điểm khả dụng]

    C --> D{Muốn dùng điểm?}
    D -->|Không| E[Bỏ qua]
    D -->|Có| F[Nhập số điểm]

    F --> G{Kiểm tra điểm}
    G -->|Không đủ| H[Thông báo lỗi]
    G -->|Đủ| I[Tính Loyalty Amount]

    H --> F
    I --> J["Loyalty Amount = Points × Conversion Factor"]
    J --> K[Áp dụng giảm giá]

    K --> L[Submit Invoice]
    L --> M[Tạo Loyalty Point Entry âm]

    style I fill:#a7fab9
    style M fill:#ffd19a
```

---

## 5. Quy trình xác định hạng

```mermaid
flowchart TD
    A[Khi submit Invoice] --> B[Lấy total_spent của Customer]
    B --> C[Lấy danh sách tier từ collection_rules]

    C --> D{So sánh với min_spent}

    D --> E["Tier 1: Bronze (min_spent = 0)"]
    D --> F["Tier 2: Silver (min_spent = X1)"]
    D --> G["Tier 3: Gold (min_spent = X2)"]
    D --> H["Tier 4: Platinum (min_spent = X3)"]

    E --> I[Chọn tier cao nhất đạt điều kiện]
    F --> I
    G --> I
    H --> I

    I --> J[Áp dụng collection_factor của tier đó]

    style I fill:#a7fab9
```

---

## 6. State Diagram - Hạng thành viên

```mermaid
stateDiagram-v2
    [*] --> Bronze: Khách hàng mới (min_spent = 0)

    Bronze --> Silver: total_spent >= min_spent Silver
    Silver --> Gold: total_spent >= min_spent Gold
    Gold --> Platinum: total_spent >= min_spent Platinum

    note right of Bronze
        Hạng mặc định
        min_spent = 0
    end note

    note right of Platinum
        Hạng VIP cao nhất
    end note
```

---

## 7. Sequence Diagram - Tích hợp với Sales Invoice

```mermaid
sequenceDiagram
    actor User
    participant SI as Sales Invoice
    participant LP as Loyalty Program
    participant LPE as Loyalty Point Entry

    User->>SI: Tạo Sales Invoice
    SI->>LP: Lấy Loyalty Program của Customer
    LP-->>SI: Trả về program và tier info

    User->>SI: Submit Invoice
    SI->>LP: Tính total_spent
    LP-->>SI: Xác định tier và collection_factor

    SI->>LPE: Tạo Loyalty Point Entry (+)
    LPE-->>SI: Entry created

    Note over SI,LPE: Nếu có dùng điểm
    SI->>LPE: Tạo Loyalty Point Entry (-)
    SI->>SI: Áp dụng Loyalty Amount
```

---

## 8. Tích hợp với modules khác

```mermaid
flowchart TD
    subgraph LOYALTY["Loyalty Program"]
        L1[Loyalty Program]
        L2[Loyalty Program Collection]
        L3[Loyalty Point Entry]
    end

    subgraph CUSTOMER["Customer"]
        C1[Customer]
    end

    subgraph SALES["Sales"]
        S1[Sales Invoice]
    end

    C1 -->|loyalty_program| L1
    L1 -->|collection_rules| L2
    S1 -->|generates| L3
    L3 -->|customer| C1
    L3 -->|loyalty_program| L1
```

---

## 9. Công thức tính điểm

```mermaid
flowchart LR
    A[Invoice Amount] --> B[÷]
    C[Collection Factor] --> B
    B --> D[= Loyalty Points]

    style D fill:#a7fab9
```

**Giải thích:**
- **Collection Factor (Hệ số quy đổi điểm):** Số tiền cần chi để được 1 điểm
- VD: Collection Factor = 10,000 → Chi 10,000 VNĐ = 1 điểm

---

## 10. Công thức sử dụng điểm

```mermaid
flowchart LR
    A[Loyalty Points] --> B[×]
    C[Conversion Factor] --> B
    B --> D[= Loyalty Amount]

    style D fill:#ffd19a
```

**Giải thích:**
- **Conversion Factor (Tỷ lệ quy đổi):** Giá trị 1 điểm khi sử dụng
- VD: Conversion Factor = 1,000 → 1 điểm = 1,000 VNĐ giảm giá

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 4.6 - Quản lý Tích điểm
**Nền tảng:** DCNET Core Loyalty Program
**Ngày cập nhật:** 2026-01-13
