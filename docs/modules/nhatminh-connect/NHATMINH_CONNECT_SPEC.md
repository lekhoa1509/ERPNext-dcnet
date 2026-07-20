# NHATMINH CONNECT - TECHNICAL SPECIFICATION

**Nguồn:** Phân tích từ codebase hiện tại tại `/Users/vovanduc/Code/dcnet/bravo-connect`

**Phiên bản:** 1.0 (Đang chạy Production)

**Ngày cập nhật:** 10/01/2026

---

## 1. TỔNG QUAN

### 1.1 Mục đích

**Bravo Connect** là WordPress/WooCommerce plugin tích hợp website Nhật Minh Sports với hệ thống ERP Bravo (cũ).

### 1.2 Phạm vi tích hợp

| Chức năng | Hướng đồng bộ | Trạng thái |
|-----------|--------------|-----------|
| **Đơn hàng** | WooCommerce → Bravo | ✅ Hoạt động |
| **Tồn kho** | Bravo → WooCommerce | ✅ Hoạt động |
| **Sản phẩm** | Bravo → WooCommerce | ❓ Cần xác nhận |

### 1.3 Kiến trúc hệ thống

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  WooCommerce    │         │  Bravo Connect  │         │   Bravo ERP     │
│  (Website NM)   │◄───────►│    Plugin       │◄───────►│   (Legacy)      │
│                 │         │                 │         │                 │
│  - Đơn hàng     │  PUSH   │  - Order Sync   │  POST   │  - SalesOrder   │
│  - Sản phẩm     │  ────►  │  - Stock Sync   │  ◄────  │  - Inventory    │
│  - Tồn kho      │  ◄────  │  - REST API     │  GET    │  - Products     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## 2. LUỒNG ĐỒNG BỘ ĐƠN HÀNG

### 2.1 Trigger Event

**Hook:** `woocommerce_order_status_changed`

**Điều kiện:** Status chuyển sang `processing` hoặc `completed`

### 2.2 Workflow

```
Khách đặt hàng
    ↓
Order created (pending)
    ↓
Thanh toán thành công
    ↓
Status → processing/completed
    ↓
Hook triggered
    ↓
POST /token (Bravo Auth)
    ↓
POST /api/BravoWebApi/execute
    ↓
Log kết quả
```

### 2.3 Data Mapping

| Field Bravo | Source WooCommerce | Ghi chú |
|-------------|-------------------|---------|
| `WebId` | Order number | ID đơn hàng |
| `DocNo` | USER_PREFIX + Order number | Prefix theo subdomain |
| `DocDate` | Order created date | Format: m/d/Y |
| `CustomerCode` | Billing phone | Mã KH = SĐT |
| `CustomerName` | Billing full name | Tên KH |
| `Tel` | Billing phone | SĐT KH |
| `Address` | Billing address 1 | Địa chỉ thanh toán |
| `OrderSource` | USER_PREFIX | SHOP/ORIGIN |
| `Description` | Customer note | Ghi chú + sản phẩm không SKU |
| `PaymentStatus` | Status mapping | COD/Đã chuyển khoản |
| `DeliveryAmount` | Shipping total | Phí vận chuyển |
| `Consignee` | Shipping first name | Người nhận |
| `DeliveryAddress` | Shipping address + city + postcode | Địa chỉ giao hàng |
| `ConsigneeTel` | Shipping last name | SĐT người nhận |
| `CompReceiveInv` | Meta: billing_vat_name | Công ty nhận HĐ |
| `AddrReceiveInv` | Meta: _billing_vat_address | Địa chỉ nhận HĐ |
| `CompTaxCode` | Meta: billing_vat_taxcode | MST |
| `EmailReceiveInv` | Meta: billing_vat_email | Email nhận HĐ |

### 2.4 Payment Status Mapping

| WooCommerce Status | Bravo PaymentStatus |
|-------------------|---------------------|
| `processing` | "COD" |
| `completed` | "Đã chuyển khoản" |

### 2.5 Order Items

**DetailInfo Array:**
```json
{
  "ItemCode": "SKU001",
  "Quantity": 2,
  "OriginalAmount9": 500000,
  "OriginalAmount": 450000
}
```

**Lưu ý:** Sản phẩm không có SKU → ghi vào `Description` thay vì `DetailInfo`

---

## 3. LUỒNG ĐỒNG BỘ TỒN KHO

### 3.1 API Endpoint

**URL:** `POST /wp-json/api/v1/stock`

**Authentication:** Header `api-key: AspWOlS9KcrQmY8Il78Xrl0pUT6FeRIJ`

### 3.2 Request Format

```json
[
  {
    "itemCode": "SKU001",
    "quantity": 50
  },
  {
    "itemCode": "SKU002",
    "quantity": 100
  }
]
```

### 3.3 Xử lý

1. Kiểm tra API key
2. Với mỗi item:
   - Tìm product theo SKU
   - Cập nhật `stock_quantity`
   - Set `stock_status = 'instock'`
   - Enable `manage_stock = true`

### 3.4 Response Format

```json
[
  {
    "itemCode": "SKU001",
    "quantity": 50,
    "status": "OK",
    "message": "Product updated successfully",
    "product_id": 123
  }
]
```

---

## 4. ĐỒNG BỘ SẢN PHẨM

### 4.1 API Endpoint (READ-ONLY)

**URL:** `GET /wp-json/api/v1/product`

**Mục đích:** Cho phép Bravo ĐỌC danh sách sản phẩm từ WooCommerce

### 4.2 Response Format

```json
{
  "limit": 20,
  "page": 1,
  "total": 500,
  "data": [
    {
      "ID": 123,
      "Name": "Gậy golf Titleist",
      "SKU": "GOLF001",
      "Price": "5000000",
      "Regular Price": "6000000",
      "Sale Price": "5000000",
      "Stock Status": "instock",
      "Description": "...",
      "Categories": "Golf Clubs",
      "Image URL": "https://..."
    }
  ]
}
```

### 4.3 ⚠️ Giới hạn

**KHÔNG hỗ trợ:**
- Tạo sản phẩm mới từ Bravo → WooCommerce
- Cập nhật giá từ Bravo
- Cập nhật tên/mô tả sản phẩm
- Đồng bộ hình ảnh
- Đồng bộ danh mục

**Quy tắc:** Thông tin sản phẩm phải được quản lý trực tiếp trên WooCommerce

---

## 5. MULTI-SITE SUPPORT

### 5.1 Subdomain Detection

```php
// Tự động xác định USER_PREFIX
shop.nhatminhsports.vn  → USER_PREFIX = "SHOP"
nhatminhsports.vn       → USER_PREFIX = "ORIGIN"
```

### 5.2 Áp dụng

- Prefix cho mã đơn hàng: `SHOP12345`, `ORIGIN12346`
- Xác định nguồn đơn hàng: `OrderSource = "SHOP"` hoặc `"ORIGIN"`

---

## 6. CẤU HÌNH HỆ THỐNG

### 6.1 Bravo ERP API

**Endpoint:** `http://222.252.4.126:60124`

**Authentication:** OAuth2 Password Grant
```
POST /token
Body: username=NMAPI&password=***&grant_type=password
Response: { "access_token": "..." }
```

### 6.2 API Endpoints

| Endpoint | Method | Auth | Mô tả |
|----------|--------|------|-------|
| `/token` | POST | - | Lấy access token |
| `/api/BravoWebApi/execute` | POST | Bearer | Push đơn hàng |
| `/wp-json/api/v1/customer` | GET | api-key | Lấy danh sách KH |
| `/wp-json/api/v1/product` | GET | api-key | Lấy danh sách SP |
| `/wp-json/api/v1/stock` | POST | api-key | Cập nhật tồn kho |

### 6.3 Logging

**File:** `logs.log` (plugin root directory)

**Library:** Monolog

**Nội dung:**
- Order info khi push
- Bravo API response
- Stock update errors

---

## 7. ADMIN TOOLS

### 7.1 Bulk Stock Update

**Vị trí:** WordPress Admin → Tools → "Cập nhật kho"

**Chức năng:**
- Quét tất cả sản phẩm (100/trang)
- Với sản phẩm không quản lý kho hoặc `stock_quantity <= 0`:
  - Enable `manage_stock = true`
  - Set `stock_quantity = 0`
  - Set `stock_status = 'outofstock'`

**Áp dụng:** Simple products & Variations

**Bỏ qua:** Grouped, External products

---

## 8. KIẾN TRÚC CODE

### 8.1 Directory Structure

```
bravo-connect/
├── index.php                 # Plugin entry point
├── composer.json
├── logs.log                  # Log file
├── Inc/
│   ├── Init.php              # Service registration
│   └── Core/
│       ├── Api.php           # REST API & Order hooks
│       ├── StockUpdater.php  # Admin bulk update
│       ├── Helpers.php       # Bravo API functions
│       └── Middleware.php    # Auth middleware
└── vendor/                   # Composer dependencies
```

### 8.2 Dependencies

- `monolog/monolog` ^3.9 - Logging
- `guzzlehttp/guzzle` ^7.9 - HTTP Client

### 8.3 PSR-4 Namespace

`TtSoft\` → `Inc/`

---

## 9. ❓ CÂU HỎI CẦN CLARIFY

### 9.1 Đồng bộ sản phẩm

**Hiện tại:** Plugin chỉ cho phép Bravo ĐỌC sản phẩm, KHÔNG TẠO/CẬP NHẬT

**Câu hỏi:**
1. Sản phẩm hiện tại được tạo thế nào?
   - ☐ Nhập thủ công trên WooCommerce
   - ☐ Có plugin/hệ thống khác đồng bộ từ Bravo
   - ☐ Import CSV/Excel

2. Có cần đồng bộ sản phẩm từ Bravo vào WooCommerce?
   - ☐ Có - cần tự động
   - ☐ Không - tiếp tục thủ công

### 9.2 Tích hợp với FlowNext (CRM mới)

**FlowNext** đang được xây dựng để thay thế Bravo ERP

**Câu hỏi:**
1. Có cần tích hợp WooCommerce với FlowNext?
   - ☐ Có - tương tự Bravo Connect
   - ☐ Không - giữ nguyên Bravo

2. Nếu CÓ, phạm vi tích hợp:
   - ☐ Đơn hàng: WooCommerce → FlowNext
   - ☐ Tồn kho: FlowNext → WooCommerce
   - ☐ Sản phẩm: FlowNext ↔ WooCommerce (2 chiều)
   - ☐ Khách hàng: WooCommerce → FlowNext
   - ☐ Đơn giá: FlowNext → WooCommerce

3. Timeline migration:
   - ☐ Chạy song song Bravo + FlowNext
   - ☐ Chuyển đổi hoàn toàn sang FlowNext
   - ☐ Thời gian dự kiến: __________

### 9.3 Multi-site Architecture

**Hiện tại:** 2 sites (shop.nhatminhsports.vn, nhatminhsports.vn)

**Câu hỏi:**
1. Có thêm site mới trong tương lai?
2. Tất cả sites đều cần tích hợp với FlowNext?

---

## 10. KẾT LUẬN

### 10.1 Điểm mạnh

✅ Tự động đồng bộ đơn hàng real-time
✅ Hỗ trợ multi-site
✅ Cập nhật tồn kho linh hoạt
✅ Logging đầy đủ

### 10.2 Hạn chế

⚠️ Không đồng bộ sản phẩm tự động
⚠️ Phụ thuộc vào Bravo ERP (legacy system)
⚠️ API key hardcoded trong code

### 10.3 Đề xuất

📌 Cần meeting với Nhật Minh để clarify:
- Quy trình quản lý sản phẩm hiện tại
- Kế hoạch migration sang FlowNext
- Yêu cầu tích hợp mới (nếu có)

---

**Người lập:** Claude Code (FlowNext Team)

**Ngày:** 10/01/2026
