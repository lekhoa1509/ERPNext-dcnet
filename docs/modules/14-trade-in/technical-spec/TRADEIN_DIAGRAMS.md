# Module Thu cũ Đổi mới (Trade-in) - Diagrams

> **Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5
> **Phiên bản:** 1.0.0 | **Cập nhật:** 13/01/2026

---

## 1. Activity Diagrams

### 1.1. Quy trình tạo đơn Trade-in

```mermaid
flowchart TB
    START(("Bat dau")) --> A["Khach mang SP cu den cua hang"]
    A --> B["Nhan vien tiep nhan"]
    B --> C["Kiem tra tinh trang SP cu"]

    C --> D{"SP du dieu kien thu?"}
    D -->|Khong| E["Thong bao tu choi"]
    E --> END1(("Ket thuc"))

    D -->|Co| F["Dinh gia SP cu"]
    F --> G{"Gia > nguong?"}
    G -->|Co| H["Manager duyet gia"]
    G -->|Khong| I["Tu dong chap nhan"]
    H --> I

    I --> J["Chon SP moi cho khach"]
    J --> K["Kiem tra ton kho"]
    K --> L{"Con hang?"}
    L -->|Khong| M["Chon SP khac"]
    M --> J

    L -->|Co| N["Ap dung voucher"]
    N --> O["Tinh gia tri chenh lech"]
    O --> P["Trinh bay cho khach"]

    P --> Q{"Khach dong y?"}
    Q -->|Khong| R["Khach tu choi"]
    R --> END2(("Ket thuc"))

    Q -->|Co| S["Tao don hang"]
    S --> T["Nhan SP cu"]
    T --> U["Giao SP moi"]
    U --> V["Thu tien chenh lech"]
    V --> W["Cap nhat kho"]
    W --> X["Hoan thanh"]
    X --> END3(("Ket thuc"))
```

### 1.2. Quy trình định giá SP cũ

```mermaid
flowchart TB
    START(("Bat dau")) --> A["Nhan SP cu tu khach"]
    A --> B["Kiem tra ngoai quan"]

    B --> C{"Con nguyen ven?"}
    C -->|Khong| D["Ghi nhan hu hong"]
    C -->|Co| E["Kiem tra chuc nang"]
    D --> E

    E --> F{"Hoat dong tot?"}
    F -->|Khong| G["Tu choi thu"]
    G --> END1(("Ket thuc"))

    F -->|Co| H["Xac dinh muc do"]
    H --> I["Tra cuu gia thi truong"]
    I --> J["Tinh gia thu"]

    J --> K{"Gia > 5 trieu?"}
    K -->|Co| L["Yeu cau Manager duyet"]
    L --> M{"Duyet?"}
    M -->|Khong| N["Dieu chinh gia"]
    N --> L
    M -->|Co| O["Xac nhan gia thu"]

    K -->|Khong| O
    O --> END2(("Ket thuc"))
```

---

## 2. Sequence Diagrams

### 2.1. Luồng tạo đơn Trade-in đầy đủ

```mermaid
sequenceDiagram
    autonumber
    participant KH as Khach hang
    participant NV as Nhan vien
    participant HT as He thong
    participant QL as Quan ly
    participant KHO as Kho

    KH->>NV: Mang SP cu den cua hang
    NV->>HT: Tao don Thu cu Doi moi

    rect rgb(240, 248, 255)
        Note over NV,HT: KIEM TRA SP CU
        NV->>NV: Kiem tra tinh trang SP cu
        NV->>HT: Nhap thong tin SP cu
        NV->>HT: De xuat gia thu
    end

    alt Gia > nguong duyet
        NV->>QL: Yeu cau duyet gia
        QL-->>NV: Duyet gia thu
    end

    rect rgb(255, 248, 240)
        Note over NV,HT: CHON SP MOI
        NV->>HT: Chon san pham moi
        HT->>KHO: Kiem tra ton kho
        KHO-->>HT: Thong tin ton kho
        HT-->>NV: Hien thi thong tin SP
    end

    rect rgb(240, 255, 240)
        Note over NV,HT: TINH TOAN
        NV->>HT: Ap dung voucher
        HT-->>NV: Tinh gia tri chenh lech
        NV->>KH: Trinh bay so tien can tra
    end

    alt Khach dong y
        KH-->>NV: Xac nhan dong y
        NV->>HT: Xac nhan giao dich

        rect rgb(255, 240, 240)
            Note over HT,KHO: CAP NHAT KHO
            HT->>KHO: Nhap SP cu vao kho
            HT->>KHO: Xuat SP moi
            KHO-->>HT: Cap nhat thanh cong
        end

        NV->>KH: Nhan SP cu - Giao SP moi
        KH->>NV: Thanh toan tien chenh lech
        NV->>HT: Hoan thanh don
        HT-->>NV: Thong bao thanh cong
    else Khach tu choi
        KH-->>NV: Tu choi giao dich
        NV->>HT: Huy don
    end
```

### 2.2. Luồng hủy đơn Trade-in

```mermaid
sequenceDiagram
    autonumber
    participant NV as Nhan vien
    participant QL as Quan ly
    participant HT as He thong

    NV->>HT: Yeu cau huy don
    HT-->>NV: Hien thi trang thai don

    alt Don chua hoan thanh
        NV->>QL: Yeu cau duyet huy
        QL->>HT: Duyet huy don
        HT->>HT: Kiem tra da cap nhat kho chua

        alt Da cap nhat kho
            HT->>HT: Hoan tac cap nhat kho
        end

        HT-->>QL: Huy thanh cong
        QL-->>NV: Thong bao da huy
    else Don da hoan thanh
        HT-->>NV: Khong the huy - Don da hoan thanh
    end
```

---

## 3. Component Diagram

### 3.1. Kiến trúc Module Trade-in

```mermaid
flowchart TB
    subgraph UI["Giao dien nguoi dung"]
        UI_LIST["Danh sach don"]
        UI_CREATE["Tao don moi"]
        UI_DETAIL["Chi tiet don"]
    end

    subgraph API["API Layer"]
        API_TRADEIN["Trade-in API"]
    end

    subgraph SERVICE["Business Logic"]
        SVC_ORDER["Order Service"]
        SVC_PRICING["Pricing Service"]
        SVC_INVENTORY["Inventory Service"]
    end

    subgraph DATA["Data Layer"]
        DB_ORDER[("Trade-in Orders")]
        DB_PRODUCT[("Products")]
        DB_CUSTOMER[("Customers")]
        DB_INVENTORY[("Inventory")]
    end

    UI_LIST --> API_TRADEIN
    UI_CREATE --> API_TRADEIN
    UI_DETAIL --> API_TRADEIN

    API_TRADEIN --> SVC_ORDER
    API_TRADEIN --> SVC_PRICING
    API_TRADEIN --> SVC_INVENTORY

    SVC_ORDER --> DB_ORDER
    SVC_ORDER --> DB_CUSTOMER
    SVC_PRICING --> DB_PRODUCT
    SVC_INVENTORY --> DB_INVENTORY
```

---

## 4. Data Flow Diagram

### 4.1. DFD Level 0 - Context

```mermaid
flowchart LR
    KH["Khach hang"] -->|SP cu| TI["He thong Trade-in"]
    TI -->|SP moi| KH
    TI -->|Tien chenh lech| KH

    NV["Nhan vien"] -->|Tao/Cap nhat don| TI
    TI -->|Thong tin don| NV

    QL["Quan ly"] -->|Duyet gia| TI
    TI -->|Bao cao| QL

    KHO["He thong Kho"] <-->|Cap nhat ton kho| TI
```

### 4.2. DFD Level 1 - Chi tiết

```mermaid
flowchart TB
    subgraph INPUT
        I1["Thong tin KH"]
        I2["Thong tin SP cu"]
        I3["Thong tin SP moi"]
        I4["Voucher"]
    end

    subgraph PROCESS
        P1["1. Tao don"]
        P2["2. Dinh gia"]
        P3["3. Tinh toan"]
        P4["4. Xu ly kho"]
        P5["5. Hoan thanh"]
    end

    subgraph OUTPUT
        O1["Don hang"]
        O2["Phieu nhap kho"]
        O3["Phieu xuat kho"]
        O4["Hoa don"]
    end

    subgraph STORAGE
        S1[("D1: Don Trade-in")]
        S2[("D2: San pham")]
        S3[("D3: Ton kho")]
    end

    I1 --> P1
    I2 --> P1
    P1 --> S1

    S1 --> P2
    P2 --> S1

    I3 --> P3
    I4 --> P3
    S2 --> P3
    P3 --> S1

    S1 --> P4
    P4 --> S3
    P4 --> O2
    P4 --> O3

    S1 --> P5
    P5 --> O1
    P5 --> O4
```

---

## 5. Class Diagram (Đề xuất)

```mermaid
classDiagram
    class TradeInOrder {
        +String orderCode
        +Customer customer
        +OldProduct oldProduct
        +NewProduct newProduct
        +Voucher voucher
        +Decimal paymentAmount
        +String status
        +Staff staff
        +Branch branch
        +DateTime createdAt
        +create()
        +update()
        +cancel()
        +complete()
        +calculatePayment()
    }

    class OldProduct {
        +Product product
        +String condition
        +Decimal tradePrice
        +String notes
        +String photos
        +inspect()
        +setPrice()
    }

    class NewProduct {
        +Product product
        +Decimal sellingPrice
        +checkStock()
    }

    class Customer {
        +String name
        +String phone
        +String email
    }

    class Product {
        +String sku
        +String name
        +String brand
        +Decimal price
    }

    class Voucher {
        +String code
        +Decimal amount
        +apply()
        +validate()
    }

    class Staff {
        +String name
        +String role
    }

    class Branch {
        +String name
        +String location
    }

    TradeInOrder "1" --> "1" Customer
    TradeInOrder "1" --> "1" OldProduct
    TradeInOrder "1" --> "1" NewProduct
    TradeInOrder "1" --> "0..1" Voucher
    TradeInOrder "1" --> "1" Staff
    TradeInOrder "1" --> "1" Branch
    OldProduct "1" --> "1" Product
    NewProduct "1" --> "1" Product
```

---

## 6. Timeline - Một giao dịch Trade-in

```mermaid
gantt
    title Timeline giao dich Trade-in
    dateFormat HH:mm
    axisFormat %H:%M

    section Tiep nhan
    Khach den cua hang           :a1, 10:00, 5m
    Tiep nhan yeu cau           :a2, after a1, 5m

    section Kiem tra
    Kiem tra SP cu              :b1, after a2, 10m
    Dinh gia SP cu              :b2, after b1, 5m
    Duyet gia                   :b3, after b2, 5m

    section Giao dich
    Chon SP moi                 :c1, after b3, 5m
    Tinh toan chenh lech        :c2, after c1, 2m
    Khach xac nhan              :c3, after c2, 5m

    section Hoan thanh
    Nhan SP cu - Giao SP moi    :d1, after c3, 5m
    Thanh toan                  :d2, after d1, 5m
    Cap nhat he thong           :d3, after d2, 3m
```

---

## 7. Trạng thái và Hành động

### 7.1. State-Action Matrix

```mermaid
flowchart LR
    subgraph States
        S1["NEW"]
        S2["INSPECTION"]
        S3["PRICED"]
        S4["CONFIRMED"]
        S5["PROCESSING"]
        S6["COMPLETED"]
        S7["CANCELLED"]
    end

    subgraph Actions
        A1["Bat dau kiem tra"]
        A2["Hoan thanh dinh gia"]
        A3["Khach dong y"]
        A4["Bat dau xu ly"]
        A5["Hoan thanh"]
        A6["Huy"]
    end

    S1 -->|A1| S2
    S2 -->|A2| S3
    S3 -->|A3| S4
    S4 -->|A4| S5
    S5 -->|A5| S6

    S1 -->|A6| S7
    S2 -->|A6| S7
    S3 -->|A6| S7
    S4 -->|A6| S7
    S5 -->|A6| S7
```

---

## 8. Công thức tính toán

### 8.1. Visual công thức

**Nguồn:** FEATURE_SPECIFICATION.md Section 5.2.4 (Line 498-499)

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│   │  Giá SP     │   │  Giá thu    │   │   Voucher   │          │
│   │    mới      │ - │   SP cũ     │ - │   (nếu có)  │          │
│   │ 15,000,000  │   │  5,000,000  │   │   500,000   │          │
│   └─────────────┘   └─────────────┘   └─────────────┘          │
│          │                 │                 │                  │
│          └────────────────┬┴─────────────────┘                  │
│                           ▼                                     │
│                  ┌─────────────────┐                           │
│                  │   Số tiền KH    │                           │
│                  │   thanh toán    │                           │
│                  │   9,500,000     │                           │
│                  └─────────────────┘                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Danh sách Diagrams

| # | Diagram | Loại | Mô tả |
|---|---------|------|-------|
| 1.1 | Quy trình tạo đơn | Activity | Flow tạo đơn trade-in đầy đủ |
| 1.2 | Quy trình định giá | Activity | Flow định giá SP cũ |
| 2.1 | Tạo đơn đầy đủ | Sequence | Luồng tạo đơn với các actors |
| 2.2 | Hủy đơn | Sequence | Luồng hủy đơn trade-in |
| 3.1 | Kiến trúc module | Component | Cấu trúc kỹ thuật module |
| 4.1 | DFD Level 0 | Data Flow | Context diagram |
| 4.2 | DFD Level 1 | Data Flow | Chi tiết data flow |
| 5 | Class Diagram | Class | Cấu trúc đối tượng |
| 6 | Timeline | Gantt | Timeline 1 giao dịch |
| 7.1 | State-Action | Flowchart | Trạng thái và hành động |

---

**Nguồn:** `/docs/feature/FEATURE_SPECIFICATION.md` Section 5.2.4, 5.4, 5.5
**Lưu ý:** Các diagrams được **thiết kế** dựa trên quy trình nghiệp vụ. Cần review và xác nhận với khách hàng.
