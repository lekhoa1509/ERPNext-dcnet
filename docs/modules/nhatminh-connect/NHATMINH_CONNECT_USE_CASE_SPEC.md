# Đặc tả Use Cases - Module NhatMinh Connect

**Dự án:** DCNET Flow - Nhật Minh Sports
**Module:** NhatMinh Connect (WooCommerce - Bravo ERP Integration)
**Phiên bản:** 1.0 (Production)
**Nguồn:** Phân tích bravo-connect codebase
**Ngày:** 10/01/2026

---

## 📋 Mục lục

1. [Định nghĩa Module](#1-định-nghĩa-module)
2. [Danh sách Actors và Vai trò](#2-danh-sách-actors-và-vai-trò)
3. [Ma trận Phân quyền](#3-ma-trận-phân-quyền)
4. [Chi tiết Use Cases](#4-chi-tiết-use-cases)
5. [Use Case Diagram](#5-use-case-diagram)

---

## 1. Định nghĩa Module

> **Bravo Connect** là WordPress/WooCommerce plugin tích hợp website Nhật Minh Sports với hệ thống ERP Bravo (cũ).

**Phạm vi tích hợp:**
- **Đơn hàng:** WooCommerce → Bravo (Push real-time)
- **Tồn kho:** Bravo → WooCommerce (API update)
- **Sản phẩm:** Bravo → WooCommerce (Read-only)

**Nguồn:** Phân tích bravo-connect codebase

---

## 2. Danh sách Actors và Vai trò

### 2.1. Admin (WordPress Admin)

**Mô tả:** Quản trị viên WordPress có quyền truy cập backend

**Quyền hạn:**
- Cấu hình plugin settings
- Sử dụng Bulk Stock Update Tool
- Xem log files
- Quản lý kết nối Bravo API

---

### 2.2. WooCommerce System

**Mô tả:** Hệ thống WooCommerce tự động trigger events

**Chức năng:**
- Trigger order status changed events
- Lưu trữ order data
- Quản lý product stock
- Cung cấp REST API endpoints

---

### 2.3. Bravo ERP System

**Mô tả:** Hệ thống ERP cũ của Nhật Minh Sports

**Chức năng:**
- Nhận đơn hàng từ WooCommerce
- Cung cấp API cập nhật tồn kho
- Cung cấp OAuth2 authentication
- Đọc danh sách sản phẩm từ WooCommerce

---

### 2.4. Plugin System (Automated)

**Mô tả:** Plugin tự động thực hiện các tác vụ đồng bộ

**Chức năng:**
- Tự động push order khi status thay đổi
- Xử lý stock update requests từ Bravo
- Ghi log các hoạt động
- Xử lý authentication với Bravo API

---

## 3. Ma trận Phân quyền

**Nguồn:** Phân tích bravo-connect codebase

| Use Case | Admin | WooCommerce | Bravo ERP | Plugin |
|----------|-------|-------------|-----------|--------|
| **UC-01: Push đơn hàng (COD)** | - | ✓ (trigger) | - | ✓ |
| **UC-02: Push đơn hàng (Online)** | - | ✓ (trigger) | - | ✓ |
| **UC-03: Cập nhật tồn kho** | - | - | ✓ | ✓ |
| **UC-04: Đọc danh sách sản phẩm** | - | ✓ | ✓ (read) | ✓ |
| **UC-05: Bulk Stock Update** | ✓ | - | - | ✓ |
| **UC-06: Xử lý đơn không SKU** | - | ✓ (trigger) | - | ✓ |
| **UC-07: Multi-site order push** | - | ✓ (trigger) | - | ✓ |
| **UC-08: Auth error handling** | - | - | - | ✓ |
| **UC-09: Stock update failed** | - | - | ✓ | ✓ |
| **UC-10: View logs** | ✓ | - | - | - |

**Chú thích:**
- ✓ = Có quyền thực hiện
- ✓ (trigger) = Trigger event
- ✓ (read) = Chỉ đọc dữ liệu
- - = Không tham gia

---

## 4. Chi tiết Use Cases

### UC-01: Push đơn hàng khi status → processing (COD)

**ID:** UC-01
**Tên:** Push đơn hàng thanh toán COD sang Bravo
**Actors:** WooCommerce System, Plugin System, Bravo ERP
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Khi khách hàng đặt hàng và chọn thanh toán COD, đơn hàng tự động chuyển sang status "processing" và được đồng bộ sang Bravo ERP.

**Precondition:**
- WooCommerce đã cài đặt và hoạt động
- Plugin Bravo Connect đã active
- Bravo API credentials đã cấu hình
- Order có status thay đổi sang "processing"

**Main Flow:**
1. Khách hàng đặt hàng trên website với phương thức COD
2. WooCommerce tạo order với status "pending"
3. WooCommerce tự động chuyển order sang status "processing"
4. Hook `woocommerce_order_status_changed` được trigger
5. Plugin nhận event: `old_status=pending`, `new_status=processing`
6. Plugin gọi `bravoAuth()` để lấy access token:
   - POST `/token` với credentials (username=NMAPI, password, grant_type=password)
   - Nhận response chứa access_token
7. Plugin build order payload:
   - WebId = Order number
   - DocNo = USER_PREFIX + Order number (SHOP12345/ORIGIN12345)
   - DocDate = Order created date (m/d/Y format)
   - CustomerCode = Billing phone
   - CustomerName = Billing full name
   - **PaymentStatus = "COD"** (vì status = processing)
   - DeliveryAmount = Shipping total
   - DetailInfo = Array of order items (với SKU)
   - Description = Customer note + sản phẩm không SKU
8. Plugin gọi `orderToBravo()`:
   - POST `/api/BravoWebApi/execute`
   - Header: `Authorization: Bearer {access_token}`
   - Body: Order payload
9. Plugin nhận response từ Bravo
10. Plugin ghi log kết quả vào `logs.log`

**Postcondition:**
- Order được đồng bộ sang Bravo với PaymentStatus = "COD"
- Log được ghi nhận (success/error)
- Order trong WooCommerce giữ nguyên status "processing"

**Alternative Flow:**
- 6a. Nếu authentication failed:
  - Plugin ghi log error: "Auth failed"
  - Dừng quá trình (không push order)
- 8a. Nếu API call failed:
  - Plugin ghi log error với response body
  - Dừng quá trình

**Exception Flow:**
- 5a. Nếu order không có sản phẩm với SKU:
  - Chuyển sang UC-06 (Xử lý đơn không SKU)

**Business Rules:**
- Chỉ push khi new_status = "processing" hoặc "completed"
- COD orders có status = "processing"
- Mỗi order chỉ push 1 lần (không retry)

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php)

---

### UC-02: Push đơn hàng khi status → completed (Online payment)

**ID:** UC-02
**Tên:** Push đơn hàng thanh toán online sang Bravo
**Actors:** WooCommerce System, Plugin System, Bravo ERP
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Khi khách hàng thanh toán online thành công (chuyển khoản, thẻ tín dụng), admin xác nhận và chuyển order sang status "completed", đơn hàng được đồng bộ sang Bravo.

**Precondition:**
- WooCommerce đã cài đặt và hoạt động
- Plugin Bravo Connect đã active
- Order có thanh toán online thành công
- Admin chuyển order sang status "completed"

**Main Flow:**
1. Khách hàng đặt hàng với phương thức thanh toán online
2. WooCommerce tạo order với status "on-hold" (chờ xác nhận thanh toán)
3. Admin xác nhận đã nhận tiền, chuyển order sang "completed"
4. Hook `woocommerce_order_status_changed` được trigger
5. Plugin nhận event: `old_status=on-hold`, `new_status=completed`
6. Plugin gọi `bravoAuth()` để lấy access token
7. Plugin build order payload:
   - (Tương tự UC-01)
   - **PaymentStatus = "Đã chuyển khoản"** (vì status = completed)
8. Plugin gọi `orderToBravo()`
9. Plugin nhận response từ Bravo
10. Plugin ghi log kết quả

**Postcondition:**
- Order được đồng bộ sang Bravo với PaymentStatus = "Đã chuyển khoản"
- Log được ghi nhận
- Order trong WooCommerce giữ nguyên status "completed"

**Alternative Flow:**
- (Tương tự UC-01)

**Exception Flow:**
- (Tương tự UC-01)

**Business Rules:**
- Online payment orders có status = "completed"
- PaymentStatus mapping: completed → "Đã chuyển khoản"

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php)

---

### UC-03: Bravo cập nhật tồn kho qua API

**ID:** UC-03
**Tên:** Cập nhật tồn kho từ Bravo vào WooCommerce
**Actors:** Bravo ERP System, Plugin System
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Bravo ERP gọi API của WooCommerce để cập nhật số lượng tồn kho cho các sản phẩm theo SKU.

**Precondition:**
- Plugin Bravo Connect đã active
- REST API endpoint đã registered
- Bravo có API key hợp lệ
- Sản phẩm có SKU trong WooCommerce

**Main Flow:**
1. Bravo ERP chuẩn bị danh sách sản phẩm cần cập nhật stock
2. Bravo gọi API: `POST /wp-json/api/v1/stock`
3. Bravo gửi Header: `api-key: AspWOlS9KcrQmY8Il78Xrl0pUT6FeRIJ`
4. Bravo gửi Body (JSON array):
   ```json
   [
     {"itemCode": "SKU001", "quantity": 50},
     {"itemCode": "SKU002", "quantity": 100}
   ]
   ```
5. Plugin nhận request, validate API key
6. Plugin validate JSON payload format
7. Plugin loop qua từng item:
   - 7.1. Tìm product bằng SKU: `wc_get_product_id_by_sku($itemCode)`
   - 7.2. Nếu tìm thấy:
     - Load product object
     - `$product->set_manage_stock(true)`
     - `$product->set_stock_quantity($quantity)`
     - `$product->set_stock_status('instock')`
     - `$product->save()`
     - Thêm vào response: status="OK", message="Product updated successfully"
   - 7.3. Nếu không tìm thấy:
     - Thêm vào response: status="ERROR", message="Product not found"
8. Plugin trả về response (JSON array) với kết quả từng item

**Postcondition:**
- Sản phẩm được cập nhật stock_quantity
- manage_stock = true
- stock_status = 'instock'
- Response trả về cho Bravo với status từng item

**Alternative Flow:**
- 5a. Nếu API key không hợp lệ:
  - Plugin trả về 401 Unauthorized
  - Dừng quá trình
- 6a. Nếu JSON format không hợp lệ:
  - Plugin trả về 400 Bad Request
  - Dừng quá trình

**Exception Flow:**
- 7.2a. Nếu product save() failed:
  - Ghi log error
  - Trả về status="ERROR" cho item đó
  - Tiếp tục với item tiếp theo

**Response Format:**
```json
[
  {
    "itemCode": "SKU001",
    "quantity": 50,
    "status": "OK",
    "message": "Product updated successfully",
    "product_id": 123
  },
  {
    "itemCode": "SKU999",
    "quantity": 10,
    "status": "ERROR",
    "message": "Product not found"
  }
]
```

**Business Rules:**
- Chỉ update stock theo SKU (không theo product ID)
- Tự động enable manage_stock = true
- Quantity > 0 → stock_status = 'instock'
- API key hardcoded trong code

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php, method: update_stock_api)

---

### UC-04: Bravo đọc danh sách sản phẩm

**ID:** UC-04
**Tên:** Đọc danh sách sản phẩm từ WooCommerce
**Actors:** Bravo ERP System, Plugin System
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Bravo ERP gọi API để lấy danh sách sản phẩm từ WooCommerce (read-only, không tạo/cập nhật).

**Precondition:**
- Plugin Bravo Connect đã active
- REST API endpoint đã registered
- Bravo có API key hợp lệ

**Main Flow:**
1. Bravo ERP gọi API: `GET /wp-json/api/v1/product?page=1&limit=20`
2. Bravo gửi Header: `api-key: AspWOlS9KcrQmY8Il78Xrl0pUT6FeRIJ`
3. Plugin nhận request, validate API key
4. Plugin query WooCommerce products với pagination
5. Plugin build response với thông tin sản phẩm:
   - ID
   - Name
   - SKU
   - Price
   - Regular Price
   - Sale Price
   - Stock Status
   - Description
   - Categories
   - Image URL
6. Plugin trả về JSON response với pagination info

**Postcondition:**
- Bravo nhận được danh sách sản phẩm
- Không có thay đổi nào trong WooCommerce

**Alternative Flow:**
- 3a. Nếu API key không hợp lệ:
  - Plugin trả về 401 Unauthorized

**Response Format:**
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

**Business Rules:**
- Read-only (không tạo/cập nhật sản phẩm)
- Hỗ trợ pagination
- Trả về tất cả published products

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php, method: product_list_api)

---

### UC-05: Admin sử dụng Bulk Stock Update tool

**ID:** UC-05
**Tên:** Cập nhật hàng loạt trạng thái tồn kho
**Actors:** Admin
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Admin sử dụng tool để quét tất cả sản phẩm và cập nhật trạng thái tồn kho cho các sản phẩm không quản lý kho hoặc stock <= 0.

**Precondition:**
- User đã đăng nhập WordPress admin
- User có quyền quản trị
- Plugin Bravo Connect đã active

**Main Flow:**
1. Admin truy cập WordPress Admin → Tools → "Cập nhật kho"
2. Admin click button "Cập nhật kho"
3. Plugin bắt đầu quét sản phẩm (page 1, limit 100)
4. Plugin loop qua từng product trong page:
   - 4.1. Kiểm tra product type:
     - Nếu type = 'grouped' hoặc 'external': Skip product
     - Nếu type = 'simple' hoặc 'variation': Tiếp tục
   - 4.2. Kiểm tra stock status:
     - Nếu `manage_stock = false` HOẶC `stock_quantity <= 0`:
       - `$product->set_manage_stock(true)`
       - `$product->set_stock_quantity(0)`
       - `$product->set_stock_status('outofstock')`
       - `$product->save()`
       - Increment counter: updated_count++
     - Nếu đang quản lý stock đúng: Skip product
5. Plugin chuyển sang page tiếp theo (page++)
6. Lặp lại step 4-5 cho đến hết sản phẩm
7. Plugin hiển thị kết quả: "Đã cập nhật {updated_count} sản phẩm"

**Postcondition:**
- Sản phẩm không quản lý stock → enable manage_stock
- Sản phẩm stock <= 0 → set stock = 0, status = outofstock
- Admin nhận thông báo kết quả

**Alternative Flow:**
- 4.2a. Nếu product save() failed:
  - Ghi log error
  - Tiếp tục với product tiếp theo

**Business Rules:**
- Chỉ xử lý Simple products và Variations
- Bỏ qua Grouped và External products
- Process 100 products mỗi page
- Chỉ update sản phẩm không đúng chuẩn

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/StockUpdater.php)

---

### UC-06: Xử lý đơn hàng có sản phẩm không SKU

**ID:** UC-06
**Tên:** Push đơn hàng có sản phẩm không có SKU
**Actors:** WooCommerce System, Plugin System, Bravo ERP
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Khi đơn hàng chứa sản phẩm không có SKU, plugin không thêm vào DetailInfo mà ghi vào Description field.

**Precondition:**
- Order có status chuyển sang "processing" hoặc "completed"
- Order chứa ít nhất 1 sản phẩm không có SKU

**Main Flow:**
1. Plugin nhận order status changed event
2. Plugin loop qua từng order item:
   - 2.1. Lấy SKU: `$product->get_sku()`
   - 2.2. Nếu SKU không rỗng:
     - Thêm vào DetailInfo array:
       ```php
       [
         'ItemCode' => $sku,
         'Quantity' => $quantity,
         'OriginalAmount9' => $subtotal,
         'OriginalAmount' => $total
       ]
       ```
   - 2.3. Nếu SKU rỗng:
     - Thêm vào Description string:
       ```
       "Sản phẩm không SKU: {product_name} x {quantity}"
       ```
3. Plugin build complete order payload với:
   - DetailInfo = Array chỉ chứa items có SKU
   - Description = Customer note + sản phẩm không SKU
4. Plugin push order sang Bravo (tương tự UC-01)

**Postcondition:**
- Order được push sang Bravo
- Sản phẩm có SKU → trong DetailInfo
- Sản phẩm không SKU → trong Description

**Business Rules:**
- Sản phẩm không SKU KHÔNG được thêm vào DetailInfo
- Thông tin sản phẩm không SKU ghi vào Description để Bravo xử lý thủ công

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php)

---

### UC-07: Multi-site order push (SHOP vs ORIGIN)

**ID:** UC-07
**Tên:** Push đơn hàng từ nhiều subdomain
**Actors:** WooCommerce System, Plugin System, Bravo ERP
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Hệ thống hỗ trợ 2 subdomain (shop.nhatminhsports.vn và nhatminhsports.vn), tự động xác định USER_PREFIX theo subdomain để phân biệt nguồn đơn hàng.

**Precondition:**
- Plugin Bravo Connect đã active trên cả 2 sites
- Order được tạo từ 1 trong 2 sites

**Main Flow:**
1. Plugin nhận order status changed event
2. Plugin detect subdomain từ site URL:
   - Nếu subdomain = "shop" → USER_PREFIX = "SHOP"
   - Nếu subdomain = "origin" hoặc không có → USER_PREFIX = "ORIGIN"
3. Plugin build order payload với:
   - **DocNo = USER_PREFIX + Order number**
     - VD: "SHOP12345" hoặc "ORIGIN12346"
   - **OrderSource = USER_PREFIX**
     - VD: "SHOP" hoặc "ORIGIN"
4. Plugin push order sang Bravo với prefix tương ứng

**Postcondition:**
- Order được push với mã đơn hàng có prefix
- Bravo nhận biết được nguồn đơn từ SHOP hay ORIGIN

**Example:**
- Order #12345 từ shop.nhatminhsports.vn:
  - DocNo = "SHOP12345"
  - OrderSource = "SHOP"
- Order #12346 từ nhatminhsports.vn:
  - DocNo = "ORIGIN12346"
  - OrderSource = "ORIGIN"

**Business Rules:**
- shop.nhatminhsports.vn → SHOP prefix
- nhatminhsports.vn → ORIGIN prefix
- Prefix tự động detect (không cần config)

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Helpers.php)

---

### UC-08: Xử lý order push failed (auth error)

**ID:** UC-08
**Tên:** Xử lý lỗi authentication khi push order
**Actors:** Plugin System, Bravo ERP
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Khi authentication với Bravo API thất bại, plugin ghi log error và dừng quá trình push order.

**Precondition:**
- Order có status chuyển sang "processing" hoặc "completed"
- Bravo API credentials không hợp lệ hoặc Bravo server không phản hồi

**Main Flow:**
1. Plugin nhận order status changed event
2. Plugin gọi `bravoAuth()`:
   - POST `/token` với credentials
3. Bravo API trả về error:
   - HTTP 401 Unauthorized (sai username/password)
   - HTTP 500 Internal Server Error
   - Network timeout
4. Plugin nhận response với status code != 200
5. Plugin ghi log error:
   ```
   [2026-01-10 08:30:15] order.ERROR: Auth failed - Status: 401
   ```
6. Plugin dừng quá trình (không push order)

**Postcondition:**
- Order KHÔNG được push sang Bravo
- Error được ghi log vào `logs.log`
- Order status trong WooCommerce không thay đổi

**Alternative Flow:**
- Không có auto-retry mechanism
- Admin phải check log và xử lý thủ công

**Exception Flow:**
- Nếu cần push lại, admin phải:
  - Fix authentication credentials
  - Manually trigger order sync (hiện không có UI)

**Business Rules:**
- Không retry khi auth failed
- Không có notification cho admin
- Order bị "mất" sync (silent failure)

**Pain Point:**
- Không có recovery mechanism
- Admin không biết order failed nếu không check log

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Helpers.php, method: bravoAuth)

---

### UC-09: Xử lý stock update failed (SKU not found)

**ID:** UC-09
**Tên:** Xử lý lỗi cập nhật tồn kho khi SKU không tồn tại
**Actors:** Bravo ERP System, Plugin System
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Khi Bravo gọi API cập nhật stock cho SKU không tồn tại trong WooCommerce, plugin trả về error cho item đó và tiếp tục xử lý các item khác.

**Precondition:**
- Bravo gọi API `POST /api/v1/stock`
- Request chứa SKU không tồn tại trong WooCommerce

**Main Flow:**
1. Bravo gọi API với payload:
   ```json
   [
     {"itemCode": "SKU001", "quantity": 50},
     {"itemCode": "SKU999", "quantity": 10}
   ]
   ```
2. Plugin validate API key (success)
3. Plugin loop qua items:
   - 3.1. Process "SKU001":
     - `wc_get_product_id_by_sku("SKU001")` → Found (ID: 123)
     - Update stock success
     - Add to response: status="OK"
   - 3.2. Process "SKU999":
     - `wc_get_product_id_by_sku("SKU999")` → NULL (not found)
     - Skip update
     - Add to response: status="ERROR", message="Product not found"
4. Plugin trả về response array với status từng item

**Postcondition:**
- SKU tồn tại → stock được update
- SKU không tồn tại → trả về error, không update
- Response cho Bravo biết kết quả từng item

**Response Example:**
```json
[
  {
    "itemCode": "SKU001",
    "quantity": 50,
    "status": "OK",
    "message": "Product updated successfully",
    "product_id": 123
  },
  {
    "itemCode": "SKU999",
    "quantity": 10,
    "status": "ERROR",
    "message": "Product not found"
  }
]
```

**Business Rules:**
- Xử lý partial success/failure
- Item failed không ảnh hưởng items khác
- Trả về detailed response cho từng item

**Nguồn:** Phân tích bravo-connect codebase (Inc/Core/Api.php, method: update_stock_api)

---

### UC-10: Admin xem logs

**ID:** UC-10
**Tên:** Xem log file hoạt động
**Actors:** Admin
**Nguồn:** Phân tích bravo-connect codebase

**Mô tả:**
Admin truy cập file log để xem lịch sử đồng bộ đơn hàng và cập nhật tồn kho.

**Precondition:**
- Plugin đã hoạt động và có events
- File `logs.log` tồn tại trong plugin folder

**Main Flow:**
1. Admin truy cập server qua FTP/SSH
2. Admin navigate đến plugin folder:
   ```
   wp-content/plugins/bravo-connect/logs.log
   ```
3. Admin mở file logs.log
4. Admin đọc log entries:
   ```
   [2026-01-10 08:30:15] order.INFO: Info Order ==== {"order_id":12345,"old_status":"pending","new_status":"processing"}
   [2026-01-10 08:30:16] order.INFO: Push Order To Bravo Info ==== {...}
   [2026-01-10 08:30:18] order.INFO: Push Order To Bravo ==== {"code":200,"message":"Success"}
   ```

**Postcondition:**
- Admin hiểu được order nào đã sync
- Admin xác định được error nếu có

**Alternative Flow:**
- Hiện không có UI để xem logs trong WordPress admin
- Phải truy cập trực tiếp file

**Pain Point:**
- Không có admin UI
- Không có search/filter logs
- File có thể rất lớn nếu chạy lâu

**Nguồn:** Phân tích bravo-connect codebase (logs.log)

---

## 5. Use Case Diagram

### 5.1. Sơ đồ Use Case (Text)

**Nguồn:** Phân tích bravo-connect codebase

```
┌──────────────────────────────────────────────────────────────────────┐
│                 «System» NhatMinh Connect Integration                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌─────────────────────────────────┐                                  │
│  │ UC-01: Push order (COD)         │◄────────────┐                    │
│  └─────────────────────────────────┘             │                    │
│                                                   │                    │
│  ┌─────────────────────────────────┐             │                    │
│  │ UC-02: Push order (Online)      │◄────────────┼─────────┐          │
│  └─────────────────────────────────┘             │         │          │
│                                                   │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-06: Handle no-SKU items      │◄────────────┼─────────┤          │
│  └─────────────────────────────────┘             │         │          │
│           ▲ «include»                            │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-07: Multi-site push          │◄────────────┼─────────┤          │
│  └─────────────────────────────────┘             │         │          │
│           ▲ «include»                            │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-08: Auth error handling      │◄────────────┼─────────┤          │
│  └─────────────────────────────────┘             │         │          │
│                                                   │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-03: Update stock from Bravo  │◄────────────┼─────────┼──────────┤
│  └─────────────────────────────────┘             │         │          │
│           │                                       │         │          │
│           ▼ «extends»                             │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-09: Stock update failed      │◄────────────┼─────────┼──────────┤
│  └─────────────────────────────────┘             │         │          │
│                                                   │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-04: Read product list        │◄────────────┼─────────┼──────────┤
│  └─────────────────────────────────┘             │         │          │
│                                                   │         │          │
│  ┌─────────────────────────────────┐             │         │          │
│  │ UC-05: Bulk stock update tool   │◄────────────┼─────────┘          │
│  └─────────────────────────────────┘             │                    │
│                                                   │                    │
│  ┌─────────────────────────────────┐             │                    │
│  │ UC-10: View logs                │◄────────────┘                    │
│  └─────────────────────────────────┘                                  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘

      ┌────────────┐         ┌──────────┐         ┌────────────┐
      │ WooCommerce│         │  Plugin  │         │ Bravo ERP  │
      │   System   │         │  System  │         │   System   │
      └────────────┘         └──────────┘         └────────────┘
            │                      │                      │
            │                 ┌────────┐                 │
            └─────────────────│ Admin  │─────────────────┘
                              └────────┘
```

### 5.2. Mối quan hệ Actors và Use Cases

**WooCommerce System:**
- UC-01: Push order (COD) - Trigger event
- UC-02: Push order (Online) - Trigger event
- UC-06: Handle no-SKU items - Provide data
- UC-07: Multi-site push - Provide site info

**Bravo ERP System:**
- UC-03: Update stock from Bravo - Initiate request
- UC-04: Read product list - Initiate request
- UC-09: Stock update failed - Receive error response

**Plugin System:**
- UC-01: Push order (COD) - Execute sync
- UC-02: Push order (Online) - Execute sync
- UC-03: Update stock from Bravo - Process request
- UC-04: Read product list - Process request
- UC-06: Handle no-SKU items - Execute logic
- UC-07: Multi-site push - Execute logic
- UC-08: Auth error handling - Handle errors
- UC-09: Stock update failed - Handle errors

**Admin:**
- UC-05: Bulk stock update tool - Initiate action
- UC-10: View logs - View information

### 5.3. Mối quan hệ Include/Extends

**Include:**
- UC-01, UC-02 «include» UC-06: Order push luôn kiểm tra no-SKU items
- UC-01, UC-02 «include» UC-07: Order push luôn detect multi-site
- UC-01, UC-02 «include» UC-08: Order push luôn handle auth errors

**Extends:**
- UC-09 «extends» UC-03: Stock update có thể failed khi SKU not found

**Nguồn:** Phân tích bravo-connect codebase

---

## 📚 Tham khảo

**Tài liệu liên quan:**
- [NHATMINH_CONNECT_SPEC.md](./NHATMINH_CONNECT_SPEC.md) - Technical Specification
- [NHATMINH_CONNECT_STATUS.md](./NHATMINH_CONNECT_STATUS.md) - Status & Workflow
- [NHATMINH_CONNECT_WORKFLOW.md](./NHATMINH_CONNECT_WORKFLOW.md) - ERD và Sequence Diagrams
- [NHATMINH_CONNECT_DIAGRAMS.md](./NHATMINH_CONNECT_DIAGRAMS.md) - Activity Diagrams

---

## 📝 Ghi chú quan trọng

1. **Nguồn tích hợp:** Plugin hiện đang chạy production tại Nhật Minh Sports, tích hợp 2 sites (shop.nhatminhsports.vn và nhatminhsports.vn)

2. **Payment Status Mapping:**
   - Order status = "processing" → PaymentStatus = "COD"
   - Order status = "completed" → PaymentStatus = "Đã chuyển khoản"

3. **Multi-site Support:**
   - shop.nhatminhsports.vn → USER_PREFIX = "SHOP"
   - nhatminhsports.vn → USER_PREFIX = "ORIGIN"

4. **Sản phẩm không SKU:** Không được thêm vào DetailInfo, chỉ ghi vào Description

5. **Pain Points hiện tại:**
   - Không có retry mechanism khi sync failed
   - Không có admin UI để xem sync status
   - Không có notification khi có error
   - API key hardcoded trong code

6. **Bulk Stock Update Tool:** Chỉ xử lý Simple products và Variations, bỏ qua Grouped và External products

---

**Ngày cập nhật:** 10/01/2026
**Người soạn:** Claude Code (FlowNext Team)
**Nguồn:** Phân tích bravo-connect codebase tại `/Users/vovanduc/Code/dcnet/bravo-connect`
