# Module Pricing - Diagrams

> **Nguồn:** `/docs/feature/ERP_SPECIFICATION.md` Section 2, Bước 2-3 (Quản lý Bán hàng)
> **Lưu ý:** Diagrams dựa trên đặc tả YÊU CẦU, không dựa trên code hiện tại

---

## 1. Context Diagram - Module Pricing trong hệ thống ERP

```mermaid
graph TB
    subgraph "Actors"
        NVKD[Nhan vien KD]
        TPKD[Truong phong KD]
        GD[Giam doc]
        KT[Ke toan]
    end

    subgraph "Module Pricing"
        PL[Price List<br/>Bang gia]
        DP[Discount Policy<br/>Chinh sach chiet khau]
    end

    subgraph "Related Modules"
        ITEM[Item<br/>San pham]
        CUST[Customer<br/>Khach hang]
        SO[Sales Order<br/>Don hang ban]
        DO[Delivery Order<br/>Lenh xuat hang]
        SI[Sales Invoice<br/>Hoa don ban buon]
        POS[POS Invoice<br/>Hoa don ban le]
    end

    NVKD -->|Tao, cap nhat| PL
    NVKD -->|Tao, cap nhat| DP
    TPKD -->|Phe duyet| PL
    TPKD -->|Phe duyet| DP
    GD -->|Phe duyet cuoi cung| PL
    GD -->|Phe duyet cuoi cung| DP
    KT -->|Xem| PL
    KT -->|Xem| DP

    ITEM -->|Cung cap san pham| PL
    ITEM -->|Cung cap san pham| DP
    CUST -->|Doi tuong ap dung| DP

    PL -->|Cung cap gia| SO
    PL -->|Cung cap gia| SI
    PL -->|Cung cap gia| POS

    DP -->|Cung cap chiet khau| SO
    DP -->|Cung cap chiet khau| SI
    DP -->|Cung cap chiet khau| POS

    SO -->|Ke thua| DO
    DO -->|Ke thua| SI

    style PL fill:#3b82f6
    style DP fill:#60a5fa
    style SO fill:#a5b4fc
    style SI fill:#c7d2fe
    style POS fill:#e0e7ff
```

---

## 2. Sequence Diagram - Tạo bảng giá mới

```mermaid
sequenceDiagram
    actor NVKD as NV Kinh doanh
    participant UI as Web UI
    participant API as Backend API
    participant DB as Database
    participant FILE as File Storage

    NVKD->>UI: 1. Click "Tao bang gia moi"
    UI->>NVKD: 2. Hien thi form

    NVKD->>UI: 3. Nhap thong tin chung<br/>(Ten, Ngay HL, Loai, Tien te)
    UI->>API: 4. POST /api/price-list/create
    API->>DB: 5. INSERT Price List (status=Draft)
    DB-->>API: 6. Tra ve ID
    API-->>UI: 7. ID bang gia moi
    UI-->>NVKD: 8. Form chi tiet san pham

    NVKD->>UI: 9. Them san pham + gia
    UI->>API: 10. POST /api/price-list/{id}/items
    API->>DB: 11. INSERT Item Price (multiple rows)
    DB-->>API: 12. OK

    NVKD->>UI: 13. Upload file quyet dinh gia
    UI->>FILE: 14. Upload file
    FILE-->>UI: 15. File URL
    UI->>API: 16. PUT /api/price-list/{id}/attachment
    API->>DB: 17. UPDATE attachment field
    DB-->>API: 18. OK

    NVKD->>UI: 19. Click "Luu"
    UI->>API: 20. PUT /api/price-list/{id}/save
    API->>API: 21. Validate du lieu
    API->>DB: 22. UPDATE Price List
    DB-->>API: 23. OK
    API-->>UI: 24. Thanh cong
    UI-->>NVKD: 25. Thong bao: "Tao bang gia thanh cong"
```

---

## 3. Sequence Diagram - Workflow phê duyệt bảng giá

```mermaid
sequenceDiagram
    actor NVKD as NV Kinh doanh
    participant API as Backend API
    participant DB as Database
    participant JOB as Scheduler
    participant EMAIL as Email Service
    actor TPKD as Truong phong KD

    Note over NVKD,TPKD: Bang gia dang o trang thai Draft

    NVKD->>API: 1. GUI phe duyet
    API->>API: 2. Validate<br/>(Co san pham, Gia > 0, Ngay HL >= Today)
    API->>DB: 3. UPDATE status=Pending Approval
    DB-->>API: 4. OK
    API->>EMAIL: 5. GUI email cho Truong phong KD
    EMAIL-->>TPKD: 6. Thong bao: Bang gia cho duyet

    TPKD->>API: 7. Xem bang gia
    API->>DB: 8. SELECT Price List + Items
    DB-->>API: 9. Du lieu bang gia
    API-->>TPKD: 10. Hien thi chi tiet

    alt Phe duyet
        TPKD->>API: 11a. Click "Phe duyet"
        API->>DB: 12a. UPDATE status=Approved,<br/>approved_by, approved_date
        DB-->>API: 13a. OK
        API->>JOB: 14a. Tao scheduled job:<br/>Chuyen Active khi den ngay HL
        JOB-->>API: 15a. Job ID
        API->>EMAIL: 16a. GUI email cho NV KD
        EMAIL-->>NVKD: 17a. Thong bao: Bang gia da duyet
    else Tu choi
        TPKD->>API: 11b. Click "Tu choi" + Ly do
        API->>DB: 12b. UPDATE status=Draft
        DB-->>API: 13b. OK
        API->>EMAIL: 14b. GUI email cho NV KD + Ly do
        EMAIL-->>NVKD: 15b. Thong bao: Bang gia bi tu choi
    end

    Note over JOB: Scheduled job chay moi ngay 00:00

    JOB->>DB: 18. SELECT WHERE status=Approved<br/>AND effective_date=TODAY
    DB-->>JOB: 19. Danh sach bang gia
    JOB->>DB: 20. UPDATE status=Active
    DB-->>JOB: 21. OK
    JOB->>EMAIL: 22. GUI email: Bang gia da co hieu luc
```

---

## 4. Activity Diagram - Áp dụng giá và chiết khấu vào đơn hàng

```mermaid
flowchart TD
    Start([NV KD tao don hang ban]) --> SelectCustomer[Chon khach hang]

    SelectCustomer --> DetermineType{Xac dinh<br/>loai khach}
    DetermineType -->|B2B| WholesaleFlow[Kênh bán buôn]
    DetermineType -->|B2C| RetailFlow[Kênh bán lẻ]

    WholesaleFlow --> SelectItem1[Chon san pham]
    RetailFlow --> SelectItem2[Chon san pham]

    SelectItem1 --> FindPriceWholesale[Tim bang gia Wholesale Active]
    SelectItem2 --> FindPriceRetail[Tim bang gia Retail Active]

    FindPriceWholesale --> CheckPrice1{Co gia?}
    FindPriceRetail --> CheckPrice2{Co gia?}

    CheckPrice1 -->|Co| ApplyPrice1[Ap dung gia tu bang gia]
    CheckPrice1 -->|Khong| ManualPrice1[Nhap gia thu cong]

    CheckPrice2 -->|Co| ApplyPrice2[Ap dung gia tu bang gia]
    CheckPrice2 -->|Khong| ManualPrice2[Nhap gia thu cong]

    ApplyPrice1 --> FindDiscountWholesale[Tim chinh sach chiet khau<br/>Wholesale Active<br/>theo khach hang]
    ApplyPrice2 --> FindDiscountRetail[Tim chinh sach chiet khau<br/>Retail Active]

    ManualPrice1 --> FindDiscountWholesale
    ManualPrice2 --> FindDiscountRetail

    FindDiscountWholesale --> CheckDiscount1{Co chinh sach?}
    FindDiscountRetail --> CheckDiscount2{Co chinh sach?}

    CheckDiscount1 -->|Co| CheckCustomer{Khach hang<br/>hop le?}
    CheckDiscount1 -->|Khong| ManualDiscount1[Nhap thu cong % CK]

    CheckCustomer -->|Co| ApplyDiscount1[Ap dung % CK tu chinh sach]
    CheckCustomer -->|Khong| ManualDiscount1

    CheckDiscount2 -->|Co| ApplyDiscount2[Ap dung % CK tu chinh sach]
    CheckDiscount2 -->|Khong| ManualDiscount2[Nhap thu cong % CK]

    ApplyDiscount1 --> CalcDiscount1["Tinh tien CK:<br/>Tien CK = Thanh tien x %CK"]
    ManualDiscount1 --> CalcDiscount1

    ApplyDiscount2 --> CalcDiscount2["Tinh tien CK:<br/>Tien CK = Thanh tien x %CK"]
    ManualDiscount2 --> CalcDiscount2

    CalcDiscount1 --> CalcFinal1["Thanh tien sau CK:<br/>= Thanh tien - Tien CK"]
    CalcDiscount2 --> SpecialDiscount{NV ban le<br/>cap CK dac biet?}

    SpecialDiscount -->|Khong| CalcFinal2["Thanh tien sau CK:<br/>= Thanh tien - Tien CK"]
    SpecialDiscount -->|Co| CalcSpecial["Tinh CK dac biet:<br/>Tien CK DB = Gia sau CK CS x %CK DB"]

    CalcSpecial --> CalcFinal3["Thanh tien cuoi cung:<br/>= Thanh tien - Tien CK CS - Tien CK DB"]

    CalcFinal1 --> SaveRef1[Luu tham chieu:<br/>- So bang gia<br/>- So chinh sach CK]
    CalcFinal2 --> SaveRef2[Luu tham chieu:<br/>- So bang gia<br/>- So chinh sach CK]
    CalcFinal3 --> SaveRef3[Luu tham chieu:<br/>- So bang gia<br/>- So chinh sach CK<br/>- % CK dac biet]

    SaveRef1 --> End([Hoan thanh don hang])
    SaveRef2 --> End
    SaveRef3 --> End

    style WholesaleFlow fill:#3b82f6,color:#fff
    style RetailFlow fill:#60a5fa,color:#fff
    style ApplyPrice1 fill:#4ade80
    style ApplyPrice2 fill:#4ade80
    style ApplyDiscount1 fill:#4ade80
    style ApplyDiscount2 fill:#4ade80
    style CalcSpecial fill:#fbbf24
    style CalcFinal3 fill:#22c55e
```

---

## 5. Deployment Diagram - Kiến trúc hệ thống

```mermaid
graph TB
    subgraph "Client Layer"
        WEB[Web Browser]
        MOBILE[Mobile App]
    end

    subgraph "Application Layer"
        NGINX[Nginx<br/>Load Balancer]
        API1[API Server 1<br/>ERPNext/Frappe]
        API2[API Server 2<br/>ERPNext/Frappe]
    end

    subgraph "Data Layer"
        REDIS[Redis Cache<br/>Session + Price Cache]
        DB[(MariaDB Database<br/>tabPrice List<br/>tabDiscount Policy<br/>tabItem Price)]
        FILES[File Storage<br/>S3/MinIO<br/>Price decision files]
    end

    subgraph "Background Jobs"
        SCHEDULER[Frappe Scheduler<br/>- Auto activate price lists<br/>- Auto expire price lists<br/>- Email notifications]
    end

    WEB -->|HTTPS| NGINX
    MOBILE -->|HTTPS| NGINX

    NGINX -->|Round Robin| API1
    NGINX -->|Round Robin| API2

    API1 -->|Read/Write| DB
    API2 -->|Read/Write| DB

    API1 -->|Cache| REDIS
    API2 -->|Cache| REDIS

    API1 -->|Upload/Download| FILES
    API2 -->|Upload/Download| FILES

    SCHEDULER -->|Scheduled Tasks| API1
    SCHEDULER -->|DB Operations| DB

    style NGINX fill:#3b82f6,color:#fff
    style API1 fill:#60a5fa,color:#fff
    style API2 fill:#60a5fa,color:#fff
    style DB fill:#22c55e,color:#fff
    style REDIS fill:#ef4444,color:#fff
    style SCHEDULER fill:#f59e0b
```

---

## 6. Component Diagram - Cấu trúc module Pricing

```mermaid
graph TB
    subgraph "Pricing Module"
        subgraph "Controllers"
            PLC[PriceListController]
            DPC[DiscountPolicyController]
        end

        subgraph "Services"
            PLS[PriceListService<br/>- create<br/>- approve<br/>- activate<br/>- expire]
            DPS[DiscountPolicyService<br/>- create<br/>- approve<br/>- activate<br/>- apply]
            CALC[PriceCalculatorService<br/>- getPrice<br/>- applyDiscount<br/>- calculateTotal]
        end

        subgraph "Repositories"
            PLR[PriceListRepository]
            DPR[DiscountPolicyRepository]
        end

        subgraph "Models"
            PLM[PriceList Model]
            IPM[ItemPrice Model]
            DPM[DiscountPolicy Model]
            DPIM[DiscountPolicyItem Model]
        end

        subgraph "Jobs"
            ACT[ActivatePriceListJob]
            EXP[ExpirePriceListJob]
            NOTIF[NotificationJob]
        end
    end

    subgraph "External Modules"
        ITEM[Item Module]
        CUST[Customer Module]
        SO[Sales Order Module]
    end

    PLC --> PLS
    DPC --> DPS

    PLS --> PLR
    DPS --> DPR
    PLS --> CALC
    DPS --> CALC

    PLR --> PLM
    PLR --> IPM
    DPR --> DPM
    DPR --> DPIM

    ACT --> PLS
    EXP --> PLS
    NOTIF --> PLS
    NOTIF --> DPS

    PLS -->|Get item info| ITEM
    DPS -->|Get customer info| CUST
    CALC -->|Used by| SO

    style PLC fill:#3b82f6,color:#fff
    style DPC fill:#3b82f6,color:#fff
    style PLS fill:#60a5fa,color:#fff
    style DPS fill:#60a5fa,color:#fff
    style CALC fill:#22c55e,color:#fff
```

---

## 7. State Machine Diagram - Trạng thái bảng giá (với Guards)

```mermaid
stateDiagram-v2
    [*] --> draft: create

    draft --> pending_approval: submit<br/>[has items AND prices > 0 AND effective_date >= today]
    draft --> cancelled: cancel<br/>[user has permission]

    pending_approval --> approved: approve<br/>[user is Manager or Director]
    pending_approval --> draft: reject<br/>[user is Manager or Director AND has reason]
    pending_approval --> cancelled: cancel<br/>[user has permission]

    approved --> active: auto_activate<br/>[current_date = effective_date]
    approved --> cancelled: cancel<br/>[user is Director AND has reason]

    active --> expired: auto_expire<br/>[current_date > expiry_date OR replaced by new price list]
    active --> cancelled: cancel<br/>[user is Director AND has reason AND confirmed]

    expired --> [*]
    cancelled --> [*]

    note right of draft
        Guards:
        - has items
        - prices > 0
        - effective_date >= today
    end note

    note right of pending_approval
        Guards:
        - user role = Manager | Director
        - has rejection reason if rejecting
    end note

    note right of approved
        Guard:
        - current_date = effective_date
        Actions:
        - Schedule activation job
        - Send notification
    end note

    note right of active
        Guard:
        - Expiry condition met OR new price list exists
        Actions:
        - Update status
        - Send expiry notification
    end note
```

---

## 8. Data Flow Diagram - Luồng dữ liệu giá và chiết khấu

```mermaid
flowchart LR
    subgraph "Input"
        USER[Nguoi dung<br/>NV KD, TP KD]
        FILE[File dinh kem<br/>Quyet dinh gia]
        ITEM_DATA[Item Master<br/>San pham]
        CUST_DATA[Customer Master<br/>Khach hang]
    end

    subgraph "Process 1: Create Price List"
        CREATE_PL[Tao bang gia]
        VALIDATE_PL[Validate du lieu]
        SAVE_PL[Luu vao DB]
    end

    subgraph "Process 2: Approve Price List"
        REVIEW[Xem xet bang gia]
        APPROVE[Phe duyet]
        SCHEDULE[Len lich Active]
    end

    subgraph "Process 3: Apply to Sales Order"
        GET_PRICE[Lay gia tu bang gia Active]
        GET_DISCOUNT[Lay chiet khau tu chinh sach Active]
        CALCULATE[Tinh toan tong tien]
    end

    subgraph "Storage"
        DB[(Database<br/>Price List<br/>Discount Policy)]
        CACHE[(Redis Cache<br/>Active Prices)]
    end

    subgraph "Output"
        NOTIF[Thong bao Email]
        SO[Sales Order<br/>with Price & Discount]
        REPORT[Bao cao gia/chiet khau]
    end

    USER --> CREATE_PL
    FILE --> CREATE_PL
    ITEM_DATA --> CREATE_PL

    CREATE_PL --> VALIDATE_PL
    VALIDATE_PL --> SAVE_PL
    SAVE_PL --> DB

    USER --> REVIEW
    DB --> REVIEW
    REVIEW --> APPROVE
    APPROVE --> DB
    APPROVE --> SCHEDULE
    SCHEDULE --> NOTIF

    ITEM_DATA --> GET_PRICE
    CUST_DATA --> GET_DISCOUNT
    DB --> GET_PRICE
    DB --> GET_DISCOUNT

    GET_PRICE --> CACHE
    CACHE --> CALCULATE
    GET_DISCOUNT --> CALCULATE

    CALCULATE --> SO
    DB --> REPORT

    style CREATE_PL fill:#3b82f6,color:#fff
    style APPROVE fill:#4ade80
    style CALCULATE fill:#22c55e,color:#fff
    style DB fill:#94a3b8
    style CACHE fill:#ef4444,color:#fff
```

---

## 9. Class Diagram - Cấu trúc dữ liệu (Simplified)

```mermaid
classDiagram
    class PriceList {
        +String name
        +String price_list_name
        +String status
        +Date effective_date
        +Date expiry_date
        +String price_list_type
        +String currency
        +String created_by
        +String approved_by
        +DateTime approved_date
        +submit()
        +approve()
        +reject()
        +activate()
        +expire()
        +cancel()
    }

    class ItemPrice {
        +String name
        +String parent
        +String item_code
        +String item_name
        +Decimal price_list_rate
        +String uom
        +getPrice()
    }

    class DiscountPolicy {
        +String name
        +String policy_name
        +String status
        +Date apply_date
        +Date expiry_date
        +String policy_type
        +String customer
        +String customer_group
        +submit()
        +approve()
        +activate()
        +getDiscountPercentage()
    }

    class DiscountPolicyItem {
        +String name
        +String parent
        +String item_code
        +String item_name
        +Decimal discount_percentage
        +Decimal min_qty
        +Decimal max_qty
        +isApplicable()
    }

    class SalesOrder {
        +String name
        +String customer
        +Date transaction_date
        +String price_list
        +String discount_policy
        +applyPricing()
        +calculate()
    }

    class SalesOrderItem {
        +String item_code
        +Decimal qty
        +Decimal rate
        +Decimal discount_percentage
        +Decimal discount_amount
        +Decimal amount
        +calculateAmount()
    }

    PriceList "1" --> "*" ItemPrice : contains
    DiscountPolicy "1" --> "*" DiscountPolicyItem : contains
    SalesOrder "1" --> "*" SalesOrderItem : contains
    SalesOrder "*" --> "0..1" PriceList : uses
    SalesOrder "*" --> "0..1" DiscountPolicy : uses
```

---

## 10. Integration Diagram - Tích hợp với các module khác

```mermaid
graph TB
    subgraph "Pricing Module"
        PL[Price List]
        DP[Discount Policy]
    end

    subgraph "Sales Module"
        SO[Sales Order]
        DO[Delivery Order]
        SI[Sales Invoice]
    end

    subgraph "POS Module"
        POS[POS Invoice]
    end

    subgraph "Master Data"
        ITEM[Item]
        CUST[Customer]
    end

    subgraph "Accounting Module"
        ACC[GL Entry]
        AR[Accounts Receivable]
    end

    subgraph "Reporting Module"
        RPT1[Price History Report]
        RPT2[Discount Effectiveness Report]
        RPT3[Pricing Dashboard]
    end

    ITEM -->|Item Code, Item Name| PL
    ITEM -->|Item Code, Item Name| DP

    CUST -->|Customer, Customer Group| DP

    PL -->|Price| SO
    DP -->|Discount %| SO

    SO -->|Inherit Price & Discount| DO
    DO -->|Inherit Price & Discount| SI

    PL -->|Price| POS
    DP -->|Discount %| POS

    SI -->|Amount| ACC
    SI -->|Amount| AR

    POS -->|Amount| ACC
    POS -->|Amount| AR

    PL -->|Data| RPT1
    DP -->|Data| RPT2
    PL -->|Data| RPT3
    DP -->|Data| RPT3
    SO -->|Data| RPT2

    style PL fill:#3b82f6,color:#fff
    style DP fill:#60a5fa,color:#fff
    style SO fill:#a5b4fc
    style SI fill:#c7d2fe
    style POS fill:#e0e7ff
    style ACC fill:#fbbf24
```

---

**Tổng kết:**
- **10 loại diagrams** mô tả toàn diện module Pricing
- **Context, Sequence, Activity, Deployment, Component, State Machine, Data Flow, Class, Integration**
- **Mermaid syntax** tuân thủ quy tắc: ASCII IDs, quoted labels, Unix line endings
- **Ready for validation** với `/mermaid-doctor`
