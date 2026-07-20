# DCNET Flow - Workflow Tổng Thể Dự Án

> **Phiên bản**: 1.0.0 | **Cập nhật**: 10/01/2026 | **Khách hàng**: Nhật Minh Sport

---

## 1. Bức Tranh Tổng Thể (Big Picture)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              DCNET FLOW - BUSINESS FLOW PLATFORM                        │
│                                   (CRM + ERP + Integration)                             │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐           │
│   │   NGUỒN     │     │    LEAD     │     │  KHÁCH HÀNG │     │  ĐƠN HÀNG   │           │
│   │   KHÁCH     │────►│  MANAGEMENT │────►│  MANAGEMENT │────►│  MANAGEMENT │           │
│   │   HÀNG      │     │             │     │             │     │             │           │
│   └─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘           │
│         │                                                            │                  │
│         ▼                                                            ▼                  │
│   ┌─────────────┐                                           ┌─────────────┐             │
│   │ • Offline   │                                           │ • Bán lẻ/sỉ │             │
│   │ • Online    │                                           │ • Fitting   │             │
│   │ • Sàn TMĐT  │                                           │ • Coaching  │             │
│   │ • B2B       │                                           │ • Thu đổi   │             │
│   └─────────────┘                                           └──────┬──────┘             │
│                                                                    │                    │
│         ┌──────────────────────────────────────────────────────────│    								│
│         │                                                          │                    │
│         ▼                                                          ▼                    │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   ┌─────────────┐             │
│   │   SẢN PHẨM  │     │     KHO     │     │  GIAO VẬN   │   │  THANH TOÁN │             │
│   │             │◄───►│             │────►│             │   │             │             │
│   └──────┬──────┘     └──────┬──────┘     └─────────────┘   └──────┬──────┘             │
│          │                   │                                     │                    │
│          │                   │                ┌────────────────────┘                    │
│          │                   ▼                ▼                                         │
│   ┌──────▼──────┐     ┌─────────────┐   ┌─────────────┐                                 │
│   │  MUA HÀNG   │────►│  KẾ TOÁN    │◄──│  CÔNG NỢ    │                                 │
│   │   (PO)      │     │  (GL/AR/AP) │   │  (Credit)   │                                 │
│   └─────────────┘     └─────────────┘   └─────────────┘                                 │
│                                                                                         │
│                                                                                         │
│   ┌────────────────────────────────────────────────────────────────────────────────┐    │
│   │                           TÍCH HỢP BÊN NGOÀI                                   │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│   │  │ WEBSITE  │  │  SHOPEE  │  │  TIKTOK  │  │  LAZADA  │  │ VIETTEL  │          │    │
│   │  │ NHATMINH │  │          │  │   SHOP   │  │          │  │   POST   │          │    │
│   │  │   (WP)   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │    │
│   │  └──────────┘                                                                  │    │
│   └────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
│   ┌────────────────────────────────────────────────────────────────────────────────┐    │
│   │                              HỆ THỐNG NỘI BỘ                                   │    │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │    │
│   │  │ NHÂN VIÊN│  │ CHI NHÁNH│  │   ROLE   │  │  BÁO CÁO │  │ ANALYTICS│          │    │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │    │
│   └────────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Luồng Chính: Lead → Customer → Order

```mermaid
flowchart TB
    subgraph SOURCES["📥 NGUỒN KHÁCH HÀNG"]
        direction LR
        OFF[🏪 Offline<br/>Vãng lai, Giới thiệu]
        ONL[🌐 Online<br/>Google, Facebook, Website]
        ECO[🛒 Sàn TMĐT<br/>Shopee, TikTok, Lazada]
        B2B[🏢 B2B<br/>Ngân hàng, CTV, TTĐT]
    end

    subgraph LEAD["👤 LEAD MANAGEMENT"]
        L1[Tiếp nhận Lead]
        L2[Phân công NV]
        L3[Tư vấn & Chăm sóc]
        L4{Quan tâm?}
    end

    subgraph CUSTOMER["👥 KHÁCH HÀNG"]
        C1[Tạo Khách hàng]
        C2[Phân loại<br/>Lẻ / Sỉ]
        C3[Gán Bảng giá]
        C4[Chăm sóc định kỳ]
    end

    subgraph ORDER["📦 ĐƠN HÀNG"]
        direction TB
        O1[Đơn Bán lẻ/Sỉ]
        O2[Đơn Fitting]
        O3[Đơn Coaching]
        O4[Đơn Thu cũ Đổi mới]
    end

    subgraph PROCESS["⚙️ XỬ LÝ ĐƠN"]
        P1[Xác nhận đơn]
        P2[Xuất kho]
        P3[Giao vận]
        P4[Thanh toán]
        P5[Hoàn thành]
    end

    %% Flow
    OFF --> L1
    ONL --> L1
    ECO --> L1
    B2B --> L1

    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 -->|Có| C1
    L4 -->|Không| L3

    C1 --> C2
    C2 --> C3
    C3 --> C4

    C4 --> O1
    C4 --> O2
    C4 --> O3
    C4 --> O4

    O1 --> P1
    O2 --> P1
    O3 --> P1
    O4 --> P1

    P1 --> P2
    P2 --> P3
    P3 --> P4
    P4 --> P5
```

---

## 3. Các Module Chức Năng

```mermaid
mindmap
  root((DCNET FLOW))
    CRM
      Lead Management
        Danh sách Lead
        Tạo Lead
        Lịch sử tư vấn
        Chuyển thành KH
      Customer Management
        Khách lẻ / Sỉ
        Công nợ
        Lịch sử giao dịch
        Chăm sóc định kỳ
      Credit Management
        Hạn mức công nợ
        AR Tracking
      Loyalty
        Tích điểm tự động
        Hạng thành viên
        Đổi điểm ưu đãi
    Sales
      Order Management
        Đơn bán lẻ/sỉ
        Đơn Fitting
        Đơn Coaching
        Đơn Thu cũ Đổi mới
      Advanced Pricing
        Bảng giá phức tạp
        Chiết khấu đa nguồn
      Sales Target
        KPI bán hàng
        Tính thưởng
      Consignment
        Hàng ký gửi
        Tracking
        Settlement
    Operations
      Warehouse
        Đa kho
        Tồn kho FIFO/Moving Avg
        Đồng bộ Website
      Purchase
        Mua hàng
        PO Management
      Import Management
        Quy trình nhập hàng
        Tracking container
      Supplier Support
        Chi phí hỗ trợ hãng
      Barcode Printing
        In tem mã vạch
      Giao vận
        Viettel Post
        GHTK, GHN
    Accounting
      GL (General Ledger)
      AR/AP
      Tax Management
    Integrations
      Website NhatMinh (WP)
        Nhận Đơn hàng
        Push Tồn kho
      Sàn TMĐT
        Shopee
        TikTok Shop
        Lazada
      Giao tiếp
        Zalo OA
        Messenger
    Admin
      Nhân viên
      Chi nhánh
      Role & Permission
      Settings
    Analytics
      Dashboard
      Báo cáo Doanh số
      Báo cáo Kho
      Website Analytics
```

---

## 4. Luồng Đơn Hàng Chi Tiết

### 4.1. Đơn Bán Lẻ/Sỉ (Sản phẩm thông thường)

```mermaid
flowchart LR
    subgraph INPUT["📝 TẠO ĐƠN"]
        A1[Chọn KH/Tạo mới]
        A2[Chọn Sản phẩm]
        A3[Áp dụng Bảng giá]
        A4[Áp Voucher/Coupon]
    end

    subgraph PRICING["💰 TÍNH GIÁ"]
        B1["Giá niêm yết"]
        B2["- Chiết khấu nguồn"]
        B3["- Giảm giá web"]
        B4["- Coupon"]
        B5["- Voucher"]
        B6["= Giá cuối"]
    end

    subgraph PROCESS["⚙️ XỬ LÝ"]
        C1[Xác nhận đơn]
        C2[Chuyển Kho]
        C3[Xuất hàng]
        C4[Tạo vận đơn]
    end

    subgraph DELIVERY["🚚 GIAO HÀNG"]
        D1[Viettel Post]
        D2[Tracking]
        D3[Giao thành công]
    end

    subgraph COMPLETE["✅ HOÀN TẤT"]
        E1[Thanh toán]
        E2[Cập nhật công nợ]
        E3[Tích điểm]
        E4[Đơn hoàn thành]
    end

    A1 --> A2 --> A3 --> A4
    A4 --> B1 --> B2 --> B3 --> B4 --> B5 --> B6
    B6 --> C1 --> C2 --> C3 --> C4
    C4 --> D1 --> D2 --> D3
    D3 --> E1 --> E2 --> E3 --> E4
```

### 4.2. Đơn Fitting

```mermaid
flowchart TB
    subgraph BOOKING["📅 ĐẶT LỊCH"]
        F1[KH đăng ký Fitting<br/>qua Website]
        F2[Chọn dịch vụ + Ngày giờ]
        F3[Xác nhận lịch hẹn]
    end

    subgraph SESSION["🏌️ BUỔI FITTING"]
        F4[KH đến fitting]
        F5[Thu thập thông tin<br/>Chiều cao, Cân nặng<br/>Size tay, Cấp độ]
        F6[Đo các thông số kỹ thuật<br/>Tốc độ gậy/bóng<br/>Swing, Đường bóng]
    end

    subgraph RESULT["📋 KẾT QUẢ"]
        F7[Đề xuất gậy phù hợp]
        F8[Dịch vụ phát sinh<br/>Grip, Shaft, Combo]
        F9[Tạo đơn hàng]
    end

    subgraph FOLLOWUP["📞 THEO DÕI"]
        F10[Lưu hồ sơ KH]
        F11[Chăm sóc sau fitting]
        F12[Upsell sản phẩm]
    end

    F1 --> F2 --> F3
    F3 --> F4 --> F5 --> F6
    F6 --> F7 --> F8 --> F9
    F9 --> F10 --> F11 --> F12
```

### 4.3. Đơn Coaching

```mermaid
flowchart TB
    subgraph ENROLL["📝 ĐĂNG KÝ"]
        G1[Tiếp nhận học viên]
        G2[Thu thập hồ sơ<br/>Thông tin, Trình độ, Mục tiêu]
        G3[Test đầu vào]
        G3a[Nhập thông số kỹ thuật<br/>COACHING_SPECS]
    end

    subgraph PACKAGE["📦 GÓI HỌC"]
        G4[Chọn gói huấn luyện<br/>8 buổi cơ bản<br/>12 buổi nâng cao]
        G5[Phân công HLV]
        G5a[Chọn sân tập<br/>GOLF_COURSE]
        G6[Sắp lịch học]
    end

    subgraph TRAINING["🏌️ HUẤN LUYỆN"]
        G7[Buổi học định kỳ]
        G8[Ghi nhận tiến bộ]
        G9[Điều chỉnh chương trình]
    end

    subgraph COMPLETE["✅ HOÀN THÀNH"]
        G10[Đánh giá kết quả]
        G11[Chăm sóc sau khóa]
        G12[Upsell sản phẩm/<br/>Khóa học tiếp]
    end

    G1 --> G2 --> G3 --> G3a
    G3a --> G4 --> G5 --> G5a --> G6
    G6 --> G7 --> G8 --> G9
    G9 --> G10 --> G11 --> G12
```

#### Entities chính của Coaching:

| Entity | Mô tả |
| --- | --- |
| `COACHING_ORDER` | Đơn đăng ký khóa học |
| `COACHING_PACKAGE` | Gói huấn luyện (8 buổi, 12 buổi...) |
| `COACH` | HLV (extend từ Employee) |
| `GOLF_COURSE` | Sân tập (đối tác hoặc của NM) |
| `COACHING_SESSION` | Từng buổi học, điểm danh |
| `COACHING_TEST` | Bài test đầu vào |
| `COACHING_SPECS` | Thông số kỹ thuật học viên (tương tự Fitting) |

### 4.4. Đơn Thu Cũ Đổi Mới

```mermaid
flowchart LR
    subgraph OLD["🔄 HÀNG CŨ"]
        H1[KH mang gậy cũ]
        H2[Kiểm tra tình trạng]
        H3[Định giá thu mua]
    end

    subgraph NEW["🆕 HÀNG MỚI"]
        H4[KH chọn gậy mới]
        H5[Giá gậy mới]
    end

    subgraph CALC["🧮 TÍNH TOÁN"]
        H6["Giá mới - Giá thu cũ<br/>- Voucher (nếu có)<br/>= Số tiền thanh toán"]
    end

    subgraph DONE["✅ HOÀN TẤT"]
        H7[Thanh toán chênh lệch]
        H8[Bàn giao gậy mới]
        H9[Nhập kho gậy cũ]
    end

    H1 --> H2 --> H3
    H4 --> H5
    H3 --> H6
    H5 --> H6
    H6 --> H7 --> H8 --> H9
```

---

## 5. Tích Hợp Website NhatMinh (WordPress/WooCommerce)

```mermaid
flowchart TB
    subgraph WEBSITE["🌐 WEBSITE NHATMINH<br/>(WordPress/WooCommerce)"]
        WC1[(Products)]
        WC2[(Stock)]
        WC3[(Orders)]
        WC4[(Customers)]
    end

    subgraph CRM["💼 DCNET FLOW"]
        CR1[(Products)]
        CR2[(Inventories)]
        CR3[(Orders)]
        CR4[(Customers)]
    end

    subgraph SYNC["🔄 ĐỒNG BỘ (NhatMinh Connect Plugin)"]
        S1[Webhook - Push Orders]
        S2[REST API - Update Stock]
    end

    WC3 -->|"Hook: order_status_changed"| S1 --> CR3

    CR2 -->|"POST /wp-json/api/v1/stock"| S2 --> WC2

    note1["⚠️ Sản phẩm quản lý trên Website<br/>CRM cập nhật Tồn kho về Website<br/>Website push Đơn hàng sang CRM"]
```

### 5.1 Workflow Đồng Bộ Chi Tiết

```mermaid
sequenceDiagram
    participant WEB as Website NhatMinh
    participant PLUGIN as NhatMinh Connect
    participant CRM as DCNET Flow

    Note over WEB,CRM: 1️⃣ KHÁCH ĐẶT HÀNG TRÊN WEBSITE

    WEB->>WEB: Khách checkout & thanh toán
    WEB->>WEB: Order status: pending → processing
    WEB->>PLUGIN: Trigger: woocommerce_order_status_changed

    Note over PLUGIN: 2️⃣ PUSH ĐƠN HÀNG TỪ WEBSITE → CRM

    PLUGIN->>CRM: POST /api/auth/token
    CRM-->>PLUGIN: access_token
    PLUGIN->>CRM: POST /api/orders/sync<br/>{order data}
    CRM-->>PLUGIN: 200 OK

    Note over CRM: 3️⃣ XỬ LÝ ĐƠN HÀNG TRÊN CRM

    CRM->>CRM: Confirm order
    CRM->>CRM: Xuất kho
    CRM->>CRM: Cập nhật tồn kho

    Note over CRM,WEB: 4️⃣ ĐỒNG BỘ TỒN KHO CRM → WEBSITE

    CRM->>PLUGIN: POST /wp-json/api/v1/stock<br/>[{sku, quantity}]
    PLUGIN->>WEB: Update stock_quantity
    WEB-->>PLUGIN: 200 OK
    PLUGIN-->>CRM: Stock updated
```

### 5.2 REST API Endpoints

**A. Website → CRM (Push - Đơn hàng)**

| Endpoint | Method | Mô tả | Trigger |
| --- | --- | --- | --- |
| `/api/orders/sync` | POST | Nhận đơn hàng từ Website | Webhook (real-time) |

**B. CRM → Website (Push - Tồn kho)**

| Endpoint | Method | Mô tả | Trigger |
| --- | --- | --- | --- |
| `/wp-json/api/v1/stock` | POST | Cập nhật tồn kho | After xuất kho |

**Header:** `api-key: <API_KEY>`

**Đơn hàng - Payload (Website → CRM):**

```json
{
  "WebId": 12345,
  "DocNo": "ORIGIN12345",
  "DocDate": "01/10/2026",
  "CustomerCode": "0912345678",
  "CustomerName": "Nguyễn Văn A",
  "Tel": "0912345678",
  "Address": "123 Đường ABC, Q1, TP.HCM",
  "OrderSource": "ORIGIN",
  "Description": "Ghi chú của khách",
  "PaymentStatus": "COD",
  "DeliveryAmount": 30000,
  "Consignee": "Người nhận",
  "DeliveryAddress": "Địa chỉ giao hàng",
  "ConsigneeTel": "0987654321",
  "DetailInfo": [
    {
      "ItemCode": "SKU001",
      "Quantity": 2,
      "OriginalAmount9": 500000,
      "OriginalAmount": 450000
    }
  ]
}
```

**Tồn kho - Payload (CRM → Website):**

```json
[
  {"itemCode": "SKU001", "quantity": 50},
  {"itemCode": "SKU002", "quantity": 100}
]
```

### 5.3 Data Mapping

**Order Status Mapping:**

| WooCommerce Status | CRM PaymentStatus |
| --- | --- |
| `processing` | "COD" |
| `completed` | "Đã chuyển khoản" |

**Field Mapping:**

| CRM Field | Website Source | Ghi chú |
| --- | --- | --- |
| `WebId` | Order number | ID đơn hàng |
| `DocNo` | PREFIX + Order number | ORIGIN12345 |
| `DocDate` | Order created date | Format: m/d/Y |
| `CustomerCode` | Billing phone | SĐT khách |
| `CustomerName` | Billing full name | Tên đầy đủ |
| `Address` | Billing address 1 | Địa chỉ xuất hóa đơn |
| `PaymentStatus` | Order status | COD / Đã CK |
| `DeliveryAmount` | Shipping total | Phí ship |
| `Consignee` | Shipping first name | Người nhận |
| `DeliveryAddress` | Shipping address full | Địa chỉ giao hàng |
| `ConsigneeTel` | Shipping phone | SĐT người nhận |
| `DetailInfo[]` | Order items | Chỉ sản phẩm có SKU |

### 5.4 Quy Tắc Đồng Bộ

| Dữ liệu | Chiều | Frequency | Ghi chú |
| --- | --- | --- | --- |
| Đơn hàng | Website → CRM | Real-time (webhook) | Khi status changed |
| Tồn kho | CRM → Website | Real-time | Sau khi xuất kho |

**⚠️ LƯU Ý:**
- **Sản phẩm**: Quản lý trực tiếp trên Website (không đồng bộ)
- **Đơn hàng**: Website push sang CRM khi có đơn mới
- **Tồn kho**: CRM push về Website sau khi xuất kho
- CRM có thể đọc Sản phẩm/Khách hàng từ Website nếu cần (qua API)

### 5.5 Multi-site Support

Plugin tự động xác định `PREFIX` dựa trên subdomain:

| Domain | PREFIX | OrderSource |
| --- | --- | --- |
| `nhatminhsports.vn` | ORIGIN | ORIGIN |
| `shop.nhatminhsports.vn` | SHOP | SHOP |

### 5.6 Plugin Architecture

```
nhatminh-connect/              # WordPress Plugin (cài trên Website)
├── index.php                  # Plugin entry point
├── composer.json              # Dependencies (Guzzle, Monolog)
├── logs.log                   # Log file
├── Inc/
│   ├── Init.php               # Service registration
│   └── Core/
│       ├── Api.php            # REST API & Order hooks
│       │                      # - Hook: woocommerce_order_status_changed
│       │                      # - Endpoint: /api/v1/stock (receive)
│       │                      # - Endpoint: /api/v1/product (read)
│       │                      # - Endpoint: /api/v1/customer (read)
│       ├── StockUpdater.php   # Admin bulk stock update tool
│       ├── Helpers.php        # CRM API functions
│       │                      # - crmAuth()
│       │                      # - orderToCRM($token, $order)
│       └── Middleware.php     # API key authentication
└── vendor/                    # Composer dependencies
```

**Dependencies:**
- `monolog/monolog` ^3.9 - Logging
- `guzzlehttp/guzzle` ^7.9 - HTTP Client

---

## 6. Tích Hợp Sàn TMĐT

```mermaid
flowchart TB
    subgraph PLATFORMS["🛒 SÀN TMĐT"]
        P1[Shopee]
        P2[TikTok Shop]
        P3[Lazada]
        P4[Website]
    end

    subgraph CRM["💼 DCNET FLOW"]
        C1[Đơn hàng]
        C2[Sản phẩm]
        C3[Tồn kho]
        C4[Khách hàng]
    end

    subgraph ACTIONS["⚡ HÀNH ĐỘNG"]
        A1[Đồng bộ đơn mới]
        A2[Cập nhật tồn kho]
        A3[Cập nhật trạng thái]
    end

    P1 --> A1
    P2 --> A1
    P3 --> A1
    P4 --> A1

    A1 --> C1
    C1 --> C4

    C2 --> A2 --> P1
    C2 --> A2 --> P2
    C2 --> A2 --> P3

    C1 --> A3 --> P1
    C1 --> A3 --> P2
    C1 --> A3 --> P3
```

---

## 7. Luồng Giao Vận

```mermaid
flowchart LR
    subgraph CRM["💼 CRM"]
        A1[Đơn đã xuất kho]
        A2[Tạo vận đơn]
    end

    subgraph CARRIER["🚚 VIETTEL POST"]
        B1[Nhận đơn]
        B2[Lấy hàng]
        B3[Vận chuyển]
        B4[Giao hàng]
    end

    subgraph TRACKING["📍 TRACKING"]
        C1[Mã giao vận]
        C2[Trạng thái]
        C3[Cập nhật tự động]
    end

    subgraph RESULT["✅ KẾT QUẢ"]
        D1{Giao thành công?}
        D2[Xác nhận COD]
        D3[Hoàn trả]
    end

    A1 --> A2 --> B1
    B1 --> B2 --> B3 --> B4
    B1 --> C1
    B2 --> C2
    B3 --> C2
    B4 --> C2
    C2 --> C3 --> A1

    B4 --> D1
    D1 -->|Có| D2
    D1 -->|Không| D3
```

---

## 8. Dashboard & Báo Cáo

```mermaid
flowchart TB
    subgraph DATA["📊 NGUỒN DỮ LIỆU"]
        D1[Đơn hàng]
        D2[Khách hàng]
        D3[Sản phẩm]
        D4[Kho]
        D5[Fitting/Coaching]
    end

    subgraph DASHBOARD["📈 DASHBOARD"]
        DB1[Doanh số ngày/tuần/tháng]
        DB2[Doanh số bán sỉ/lẻ]
        DB3[Doanh số theo nguồn]
        DB4[Top 20 SP bán chạy]
    end

    subgraph REPORTS["📋 BÁO CÁO"]
        R1[Báo cáo Doanh số]
        R2[Báo cáo Đơn hàng]
        R3[Báo cáo Khách hàng]
        R4[Báo cáo Kho]
        R5[Báo cáo Fitting]
        R6[Báo cáo Coaching]
    end

    subgraph ANALYTICS["🔍 WEBSITE ANALYTICS"]
        A1[Lưu lượng truy cập]
        A2[Tỉ lệ chuyển đổi]
        A3[Heatmap]
        A4[Session Recording]
    end

    D1 --> DB1
    D1 --> DB2
    D2 --> DB3
    D3 --> DB4

    D1 --> R1
    D1 --> R2
    D2 --> R3
    D4 --> R4
    D5 --> R5
    D5 --> R6

    D1 --> A1
    D1 --> A2
```

---

## 9. Phân Quyền Hệ Thống

```mermaid
flowchart TB
    subgraph ROLES["👥 VAI TRÒ"]
        R1[Admin]
        R2[Manager]
        R3[Sales]
        R4[Warehouse]
        R5[HLV/Fitter]
    end

    subgraph PERMISSIONS["🔐 QUYỀN HẠN"]
        P1[Full Access]
        P2[Dashboard + Reports<br/>Manage Staff]
        P3[Lead + Customer<br/>Order]
        P4[Inventory<br/>Shipping]
        P5[Fitting/Coaching<br/>Order specific]
    end

    subgraph MODULES["📦 MODULE"]
        M1[Tất cả]
        M2[Dashboard, Báo cáo<br/>Nhân viên, Settings]
        M3[Lead, KH, Đơn hàng<br/>Sản phẩm]
        M4[Kho, Giao vận]
        M5[Fitting, Coaching]
    end

    R1 --> P1 --> M1
    R2 --> P2 --> M2
    R3 --> P3 --> M3
    R4 --> P4 --> M4
    R5 --> P5 --> M5
```

---

## 10. Timeline Triển Khai

> **⚠️ Đang được update** - Timeline chi tiết đang được lên kế hoạch

---

## 11. Tech Stack

```
```

---

## 12. Tổng Kết Module

| # | Module | Chức năng chính |
| --- | --- | --- |
| 1 | **Lead Management** | Pipeline, tư vấn, chuyển KH |
| 2 | **Warehouse** | Đa kho, tồn kho, FIFO/Moving Avg |
| 3 | **Accounting** | Kế toán, GL, AR/AP |
| 4 | **Advanced Pricing** | Bảng giá phức tạp, chiết khấu đa nguồn |
| 5 | **Credit Management** | Hạn mức công nợ, AR tracking |
| 6 | **Fitting Service** | Đơn Fitting, test thông số, đề xuất gậy |
| 7 | **Coaching Program** | Đăng ký khóa học, quản lý buổi học, HLV |
| 8 | **Consignment** | Hàng ký gửi, tracking, settlement |
| 9 | **Purchase Management** | Quản lý Mua hàng, PO |
| 10 | **Sales Target** | KPI bán hàng, tính thưởng |
| 11 | **Supplier Support** | Chi phí hỗ trợ hãng |
| 12 | **Import Management** | Quy trình nhập hàng, tracking container |
| 13 | **Barcode Printing** | In tem mã vạch |
| 14 | **WooCommerce** | ⭐ PRIORITY - WordPress sync (đang chạy) |
| 15 | **E-commerce** | Shopee, TikTok, Lazada |
| 16 | **Shipping** | Viettel Post, GHTK, GHN |
| 17 | **Partners** | Quản lý KH, NCC, Đại lý (có sẵn) |
| 18 | **Loyalty** | Tích điểm, hạng thành viên |

**Tổng:** 18 modules

---

**© 2026 DCNET**
