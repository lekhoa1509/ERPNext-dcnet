# Hướng Dẫn Sử Dụng Module Quản Lý Lead

> **Hệ thống:** DCNET Flow
>
> **Phiên bản:** 1.0 | **Ngày:** 29/01/2026
>
> **Đối tượng:** Nhân viên Sales, Quản lý Sales

---

## Mục Lục

1. [Giới Thiệu](#1-giới-thiệu)
2. [Truy Cập Module Lead](#2-truy-cập-module-lead)
3. [Danh Sách Lead](#3-danh-sách-lead)
4. [Tạo Lead Mới](#4-tạo-lead-mới)
5. [Xem Chi Tiết Lead](#5-xem-chi-tiết-lead)
6. [Cập Nhật Lead](#6-cập-nhật-lead)
7. [Tương Tác Với Lead](#7-tương-tác-với-lead)
8. [Chuyển Đổi Lead](#8-chuyển-đổi-lead)
9. [Import/Export Lead](#9-importexport-lead)
10. [Báo Cáo Lead](#10-báo-cáo-lead)
11. [Câu Hỏi Thường Gặp](#11-câu-hỏi-thường-gặp)

---

## 1. Giới Thiệu

### 1.1. Lead là gì?

**Lead** là khách hàng tiềm năng - người có quan tâm đến sản phẩm/dịch vụ nhưng **chưa có giao dịch thành công**.

**Ví dụ:**
- Khách hỏi giá gậy golf qua Facebook
- Khách để lại số điện thoại trên website
- Khách được giới thiệu từ người quen

### 1.2. Vòng đời của Lead

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VÒNG ĐỜI LEAD                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌──────────┐ │
│   │  MỚI   │───▶│  ĐANG  │───▶│  BÁO   │───▶│  ĐẶT   │───▶│  KHÁCH   │ │
│   │        │    │ TƯ VẤN │    │  GIÁ   │    │  HÀNG  │    │   HÀNG   │ │
│   └────────┘    └────────┘    └────────┘    └────────┘    └──────────┘ │
│      Lead         Open        Quotation    Sales Order     Customer     │
│                                                                          │
│   Trạng thái có thể quay lại hoặc chuyển sang "Không liên hệ"           │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.3. Các trạng thái Lead

| Trạng thái | Ý nghĩa | Khi nào sử dụng |
|------------|---------|-----------------|
| **Lead** | Mới tạo | Lead vừa nhập vào hệ thống |
| **Open** | Đang xử lý | Đã bắt đầu liên hệ với khách |
| **Replied** | Đã phản hồi | Khách đã trả lời (email, tin nhắn) |
| **Interested** | Quan tâm | Khách thể hiện quan tâm mua hàng |
| **Opportunity** | Cơ hội | Đã tạo cơ hội bán hàng |
| **Quotation** | Báo giá | Đã gửi báo giá cho khách |
| **Converted** | Đã chuyển đổi | Khách đã mua hàng, thành Customer |
| **Do Not Contact** | Không liên hệ | Khách từ chối, không muốn liên hệ |

---

## 2. Truy Cập Module Lead

### 2.1. Từ Menu chính

```
Bước 1: Đăng nhập hệ thống
Bước 2: Click vào "CRM" trên thanh menu trái
Bước 3: Chọn "Lead"
```

**Đường dẫn:** `Home → CRM → Lead`

### 2.2. Từ Search Bar

```
Bước 1: Nhấn phím "/" hoặc click vào ô Search trên thanh trên cùng
Bước 2: Gõ "Lead"
Bước 3: Chọn "Lead List" từ kết quả
```

### 2.3. Shortcut (Phím tắt)

| Phím tắt | Chức năng |
|----------|-----------|
| `Alt + S` | Mở Search Bar |
| `Ctrl + G` | Đi đến (Go to) - gõ "Lead" |

---

## 3. Danh Sách Lead

### 3.1. Giao diện danh sách

Khi truy cập Lead List, bạn sẽ thấy:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Lead                                           [+ Add Lead] [Menu ▼]   │
├─────────────────────────────────────────────────────────────────────────┤
│ [🔍 Search...]  [Edit Filters]  [Save Filter]                           │
├─────────────────────────────────────────────────────────────────────────┤
│ □ │ ID           │ Tên KH      │ Trạng thái │ Nguồn    │ NV phụ trách │
├───┼──────────────┼─────────────┼────────────┼──────────┼──────────────┤
│ □ │ LEAD-0001    │ Nguyễn Văn A│ Open       │ Facebook │ sales@...    │
│ □ │ LEAD-0002    │ Trần Thị B  │ Interested │ Website  │ sales2@...   │
│ □ │ LEAD-0003    │ Lê Văn C    │ Quotation  │ Referral │ sales@...    │
│ □ │ LEAD-0004    │ Phạm Thị D  │ Lead       │ Walk-in  │ (chưa gán)   │
└───┴──────────────┴─────────────┴────────────┴──────────┴──────────────┘
│ Showing 1-20 of 156                              [◀ Prev] [Next ▶]     │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2. Tìm kiếm Lead

**Tìm kiếm nhanh:**
```
1. Click vào ô "Search..."
2. Gõ tên, email, hoặc số điện thoại
3. Kết quả hiển thị ngay lập tức
```

**Ví dụ tìm kiếm:**
- `Nguyễn` → Tìm tất cả lead có tên chứa "Nguyễn"
- `0901234567` → Tìm lead có số điện thoại này
- `golf@gmail.com` → Tìm lead có email này

### 3.3. Lọc Lead (Filter)

**Bước 1:** Click **[Edit Filters]**

**Bước 2:** Chọn điều kiện lọc:

| Điều kiện | Cách sử dụng | Ví dụ |
|-----------|--------------|-------|
| **Status** | Chọn trạng thái | Status = "Open" |
| **Lead Owner** | Chọn NV phụ trách | Lead Owner = "sales@company.com" |
| **Source** | Chọn nguồn | Source = "Facebook" |
| **Territory** | Chọn khu vực | Territory = "Hà Nội" |
| **Creation** | Chọn ngày tạo | Creation >= "01-01-2026" |

**Bước 3:** Click **[Apply]** để áp dụng

**Bước 4:** (Tùy chọn) Click **[Save Filter]** để lưu bộ lọc thường dùng

**Ví dụ bộ lọc hay dùng:**
- "Lead của tôi chưa xử lý": `Lead Owner = me` AND `Status = Lead`
- "Lead từ Facebook tuần này": `Source = Facebook` AND `Creation >= 7 ngày trước`

### 3.4. Sắp xếp danh sách

**Cách 1:** Click vào tiêu đề cột
- Click 1 lần: Sắp xếp tăng dần (A→Z, 1→9)
- Click 2 lần: Sắp xếp giảm dần (Z→A, 9→1)

**Cách 2:** Sử dụng Sort trong Edit Filters

### 3.5. Ẩn/Hiện cột

```
1. Click [Menu ▼] góc phải
2. Chọn "Pick Columns"
3. Tick/Untick các cột muốn hiển thị
4. Kéo thả để sắp xếp thứ tự cột
5. Click [Apply]
```

**Các cột khuyến nghị hiển thị:**
- ID (Mã Lead)
- Lead Name (Tên)
- Status (Trạng thái)
- Mobile No (SĐT)
- Email
- Source (Nguồn)
- Lead Owner (NV phụ trách)
- Creation (Ngày tạo)

---

## 4. Tạo Lead Mới

### 4.1. Cách tạo Lead

**Bước 1:** Click **[+ Add Lead]** hoặc nhấn `Ctrl + B`

**Bước 2:** Điền thông tin:

```
┌─────────────────────────────────────────────────────────────────────────┐
│ New Lead                                                    [Save]      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ═══ THÔNG TIN CƠ BẢN ═══════════════════════════════════════════════   │
│                                                                          │
│ Salutation:     [Mr.        ▼]     First Name*:   [_______________]    │
│ Middle Name:    [_______________]   Last Name:     [_______________]    │
│                                                                          │
│ ═══ THÔNG TIN LIÊN HỆ ══════════════════════════════════════════════   │
│                                                                          │
│ Email:          [_______________]   Phone:         [_______________]    │
│ Mobile No:      [_______________]   WhatsApp:      [_______________]    │
│                                                                          │
│ ═══ THÔNG TIN TỔ CHỨC ══════════════════════════════════════════════   │
│                                                                          │
│ Company Name:   [_______________]   Job Title:     [_______________]    │
│ Industry:       [_______________]   Territory:     [_______________]    │
│                                                                          │
│ ═══ PHÂN LOẠI ══════════════════════════════════════════════════════   │
│                                                                          │
│ Status:         [Lead        ▼]     Lead Owner:    [_______________]    │
│ Source:         [_______________]   Company:       [_______________]    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.2. Các trường thông tin quan trọng

#### Thông tin bắt buộc (*)

| Trường | Mô tả | Ví dụ |
|--------|-------|-------|
| **First Name** | Tên | Văn A |
| hoặc **Company Name** | Tên công ty (nếu là tổ chức) | Golf Store ABC |

> **Lưu ý:** Phải nhập ít nhất một trong hai: First Name hoặc Company Name

#### Thông tin khuyến nghị

| Trường | Mô tả | Ví dụ |
|--------|-------|-------|
| **Mobile No** | Số điện thoại di động | 0901234567 |
| **Email** | Địa chỉ email | nguyenvana@gmail.com |
| **Source** | Nguồn lead đến từ đâu | Facebook, Website, Referral |
| **Lead Owner** | Nhân viên phụ trách | sales@company.com |
| **Territory** | Khu vực địa lý | Hà Nội, TP.HCM |

#### Thông tin bổ sung

| Trường | Mô tả | Ví dụ |
|--------|-------|-------|
| **Salutation** | Danh xưng | Mr., Mrs., Ms. |
| **Last Name** | Họ | Nguyễn |
| **Gender** | Giới tính | Male, Female |
| **Phone** | Điện thoại bàn | 02812345678 |
| **WhatsApp** | Số WhatsApp | 0901234567 |
| **Company Name** | Tên công ty | Golf Pro Shop |
| **Job Title** | Chức vụ | Giám đốc |
| **Industry** | Ngành nghề | Retail, Sports |
| **City** | Thành phố | Hà Nội |
| **State** | Tỉnh/Thành | Hà Nội |
| **Country** | Quốc gia | Vietnam |

### 4.3. Chọn nguồn Lead (Source)

Nguồn lead giúp theo dõi hiệu quả marketing:

| Nguồn | Khi nào chọn |
|-------|--------------|
| **Facebook** | Lead từ Facebook page, Messenger |
| **Website** | Lead từ form trên website |
| **Referral** | Được giới thiệu từ khách hàng khác |
| **Walk-in** | Khách đến trực tiếp cửa hàng |
| **Phone** | Khách gọi điện hỏi |
| **Email Campaign** | Lead từ chiến dịch email |
| **Event** | Lead từ sự kiện, hội chợ |

### 4.4. Gán người phụ trách (Lead Owner)

```
1. Click vào trường "Lead Owner"
2. Gõ tên hoặc email nhân viên
3. Chọn từ danh sách gợi ý
```

**Lưu ý:**
- Nếu để trống, Lead Owner mặc định là người tạo
- Lead Owner nhận thông báo khi có cập nhật về lead

### 4.5. Lưu Lead

```
1. Kiểm tra lại thông tin đã nhập
2. Click [Save] hoặc nhấn Ctrl + S
3. Hệ thống tự động tạo mã: CRM-LEAD-2026-XXXX
```

**Sau khi lưu:**
- Lead xuất hiện trong danh sách
- Hệ thống kiểm tra trùng email (nếu bật)
- Có thể tạo Contact tự động (nếu cấu hình)

---

## 5. Xem Chi Tiết Lead

### 5.1. Mở chi tiết Lead

**Cách 1:** Click vào tên Lead trong danh sách
**Cách 2:** Click vào mã Lead (ID)

### 5.2. Giao diện chi tiết

```
┌─────────────────────────────────────────────────────────────────────────┐
│ CRM-LEAD-2026-0001: Nguyễn Văn A                                        │
│ Status: [Open ▼]                    [Edit] [Menu ▼] [Create ▼] [...]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ ┌─ THÔNG TIN ─────────────────────┐  ┌─ LIÊN HỆ ────────────────────┐  │
│ │ Lead Name: Nguyễn Văn A         │  │ Mobile: 0901234567           │  │
│ │ Company: Golf Pro Shop          │  │ Email: nguyenvana@gmail.com  │  │
│ │ Job Title: Manager              │  │ Phone: 02812345678           │  │
│ │ Territory: Hà Nội               │  │ WhatsApp: 0901234567         │  │
│ │ Source: Facebook                │  │                              │  │
│ │ Lead Owner: sales@company.com   │  │                              │  │
│ └─────────────────────────────────┘  └──────────────────────────────┘  │
│                                                                          │
│ ┌─ ĐỊA CHỈ ───────────────────────────────────────────────────────────┐ │
│ │ City: Hà Nội  |  State: Hà Nội  |  Country: Vietnam                 │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│ ═══════════════════════════════════════════════════════════════════════ │
│                                                                          │
│ [Activity] [Comments] [Emails] [Attachments] [Linked Documents]         │
│                                                                          │
│ ┌─ COMMENTS (3) ──────────────────────────────────────────────────────┐ │
│ │ 📝 sales@company.com - 29/01/2026 10:30                             │ │
│ │    "Đã gọi điện, KH quan tâm gậy Driver Titleist TSR2"              │ │
│ │                                                                      │ │
│ │ 📝 sales@company.com - 28/01/2026 14:00                             │ │
│ │    "KH hỏi giá qua Facebook, đã trả lời sơ bộ"                      │ │
│ └─────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│ [+ Add Comment]                                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.3. Các tab thông tin

| Tab | Nội dung |
|-----|----------|
| **Activity** | Lịch sử hoạt động (tạo, sửa, chuyển trạng thái) |
| **Comments** | Ghi chú nội bộ của nhân viên |
| **Emails** | Danh sách email đã gửi/nhận với lead |
| **Attachments** | Tài liệu đính kèm (PDF, hình ảnh...) |
| **Linked Documents** | Các tài liệu liên quan (Quotation, Opportunity...) |

---

## 6. Cập Nhật Lead

### 6.1. Chỉnh sửa thông tin

```
1. Mở chi tiết Lead
2. Click [Edit] hoặc nhấn Ctrl + E
3. Sửa thông tin cần thiết
4. Click [Save] hoặc nhấn Ctrl + S
```

### 6.2. Thay đổi trạng thái

**Cách 1: Từ dropdown Status**
```
1. Click vào dropdown [Status]
2. Chọn trạng thái mới
3. Hệ thống tự động lưu
```

**Cách 2: Khi tạo tài liệu mới**
- Tạo Opportunity → Status tự động thành "Opportunity"
- Tạo Quotation → Status tự động thành "Quotation"
- Tạo Sales Order → Status tự động thành "Converted"

### 6.3. Thay đổi người phụ trách

```
1. Click [Edit]
2. Sửa trường "Lead Owner"
3. Chọn nhân viên mới
4. Click [Save]
```

**Lưu ý:** Nhân viên mới sẽ nhận thông báo về việc được gán lead

### 6.4. Cập nhật địa chỉ

Lead có thể có nhiều địa chỉ (giao hàng, văn phòng...). Để thêm/sửa:

```
1. Trong chi tiết Lead, tìm section "Address"
2. Click [+ Add Address] để thêm mới
3. Hoặc click vào địa chỉ hiện tại để sửa
```

---

## 7. Tương Tác Với Lead

### 7.1. Thêm ghi chú (Comment)

Ghi chú dùng để lưu lại các trao đổi, ghi nhớ về lead.

```
1. Mở chi tiết Lead
2. Cuộn xuống section Comments
3. Click [+ Add Comment]
4. Nhập nội dung ghi chú
5. Nhấn Enter hoặc click [Comment]
```

**Ví dụ ghi chú hay dùng:**
- "Đã gọi điện 10h sáng, KH bận họp, hẹn gọi lại 3h chiều"
- "KH quan tâm gậy Driver, budget khoảng 15-20 triệu"
- "Đã gửi báo giá qua Zalo, chờ phản hồi"

### 7.2. Đính kèm tài liệu

```
1. Mở chi tiết Lead
2. Click tab [Attachments]
3. Click [Attach] hoặc kéo thả file
4. Chọn file từ máy tính
5. File được upload và gắn với Lead
```

**Các loại file thường đính kèm:**
- Báo giá PDF
- Hình ảnh sản phẩm khách quan tâm
- Chứng từ, hợp đồng
- Catalogue

### 7.3. Gửi Email

```
1. Mở chi tiết Lead
2. Click [Menu ▼] → [Email]
3. Điền nội dung email:
   - To: (tự động điền email của Lead)
   - Subject: Tiêu đề
   - Message: Nội dung
4. Click [Send]
```

**Lưu ý:**
- Email được lưu trong tab "Emails" của Lead
- Có thể đính kèm file trong email
- Hỗ trợ email template có sẵn

### 7.4. Tạo lịch hẹn/Task

```
1. Mở chi tiết Lead
2. Click [Menu ▼] → [New Event] hoặc [New Task]
3. Điền thông tin:
   - Subject: "Gọi lại KH Nguyễn Văn A"
   - Date/Time: 29/01/2026 15:00
4. Click [Save]
```

**Event/Task sẽ:**
- Hiển thị trong Calendar
- Gửi reminder trước giờ hẹn
- Liên kết với Lead

---

## 8. Chuyển Đổi Lead

### 8.1. Tổng quan các hướng chuyển đổi

```
                    ┌─────────────┐
                    │    LEAD     │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ Opportunity │ │  Quotation  │ │  Customer   │
    │ (Cơ hội)    │ │  (Báo giá)  │ │ (Trực tiếp) │
    └──────┬──────┘ └──────┬──────┘ └─────────────┘
           │               │
           ▼               ▼
    ┌─────────────┐ ┌─────────────┐
    │  Quotation  │ │ Sales Order │
    │  (Báo giá)  │ │  (Đơn hàng) │
    └──────┬──────┘ └─────────────┘
           │
           ▼
    ┌─────────────┐
    │ Sales Order │
    │  (Đơn hàng) │
    └─────────────┘
```

### 8.2. Tạo Báo giá từ Lead (Quotation)

Khi khách hàng yêu cầu báo giá:

```
1. Mở chi tiết Lead
2. Click [Create ▼] → [Quotation]
3. Hệ thống tự động điền:
   - Customer Name từ Lead Name
   - Contact info từ Lead
4. Thêm sản phẩm:
   - Click [Add Row] trong bảng Items
   - Chọn Item (sản phẩm)
   - Nhập Qty (số lượng)
   - Giá tự động lấy từ Price List
5. Kiểm tra tổng tiền
6. Click [Save] → [Submit]
```

**Sau khi Submit Quotation:**
- Lead Status tự động → "Quotation"
- Báo giá xuất hiện trong tab "Linked Documents"

### 8.3. Tạo Cơ hội bán hàng (Opportunity)

Khi muốn theo dõi chi tiết cơ hội:

```
1. Mở chi tiết Lead
2. Click [Create ▼] → [Opportunity]
3. Điền thông tin:
   - Opportunity Type: Sales
   - Expected Closing: Ngày dự kiến chốt
   - Probability: Xác suất thành công (%)
4. Thêm sản phẩm dự kiến (nếu có)
5. Click [Save]
```

**Opportunity giúp:**
- Theo dõi pipeline bán hàng
- Dự báo doanh thu
- Quản lý nhiều báo giá cho cùng 1 cơ hội

### 8.4. Chuyển trực tiếp thành Khách hàng

Khi Lead đã mua hàng và cần tạo Customer:

```
1. Mở chi tiết Lead
2. Click [Create ▼] → [Customer]
3. Hệ thống tự động điền:
   - Customer Name từ Company Name hoặc Lead Name
   - Contact info
4. Chọn Customer Type: Individual / Company
5. Click [Save]
```

**Sau khi tạo Customer:**
- Lead Status → "Converted"
- Có thể tạo đơn hàng từ Customer

### 8.5. Tạo Đơn hàng (Sales Order)

Từ Quotation đã được khách chấp nhận:

```
1. Mở Quotation
2. Click [Create ▼] → [Sales Order]
3. Kiểm tra thông tin:
   - Customer: (tự động)
   - Items: (tự động từ Quotation)
   - Delivery Date: Ngày giao hàng
4. Click [Save] → [Submit]
```

**Sau khi Submit Sales Order:**
- Customer được tạo tự động (nếu từ Lead)
- Lead Status → "Converted"
- Có thể tạo: Delivery Note, Sales Invoice

---

## 9. Import/Export Lead

### 9.1. Import Lead từ Excel

**Bước 1: Tải template**
```
1. Vào Lead List
2. Click [Menu ▼] → [Import]
3. Click [Download Template]
4. Mở file Excel template
```

**Bước 2: Điền dữ liệu**

Template có các cột:
| Cột | Bắt buộc | Ví dụ |
|-----|----------|-------|
| First Name | Có* | Văn A |
| Last Name | Không | Nguyễn |
| Company Name | Có* | Golf Store |
| Email | Không | a@email.com |
| Mobile No | Không | 0901234567 |
| Source | Không | Facebook |
| Lead Owner | Không | sales@company.com |
| Territory | Không | Hà Nội |

> *Bắt buộc 1 trong 2: First Name hoặc Company Name

**Bước 3: Upload và Import**
```
1. Quay lại trang Import
2. Click [Upload] → Chọn file Excel đã điền
3. Kiểm tra Preview dữ liệu
4. Click [Start Import]
5. Chờ hệ thống xử lý
6. Xem kết quả: Thành công / Lỗi
```

**Xử lý lỗi Import:**
- Kiểm tra format ngày tháng (DD-MM-YYYY)
- Kiểm tra email đúng định dạng
- Kiểm tra Source, Territory có trong hệ thống

### 9.2. Export Lead ra Excel

```
1. Vào Lead List
2. (Tùy chọn) Lọc dữ liệu cần export
3. Click [Menu ▼] → [Export]
4. Chọn:
   - File Type: Excel / CSV
   - Export Fields: All / Selected
5. Click [Export]
6. File tự động tải về
```

**Tips Export:**
- Lọc trước khi export để giảm dung lượng file
- Chọn "Selected Fields" nếu chỉ cần một số cột

---

## 10. Báo Cáo Lead

### 10.1. Truy cập báo cáo

```
Home → CRM → Reports
```

### 10.2. Các báo cáo có sẵn

#### Lead Details Report
Chi tiết tất cả Lead với đầy đủ thông tin.

```
1. Chọn Report: Lead Details
2. Đặt Filter:
   - Company: Chọn chi nhánh
   - From Date / To Date: Khoảng thời gian
   - Territory: Khu vực
   - Status: Trạng thái
3. Click [Refresh]
```

**Thông tin hiển thị:**
- Lead ID, Name, Status
- Owner, Territory, Source
- Contact info (Email, Phone)
- Address

#### Lead Conversion Time
Thời gian trung bình từ Lead → Customer.

**Giúp đánh giá:**
- Hiệu quả quy trình bán hàng
- So sánh giữa các nhân viên/nguồn lead

#### Lead Owner Efficiency
Hiệu suất theo từng nhân viên.

**Thông tin:**
- Số Lead được gán
- Số Lead đã chuyển đổi
- Tỷ lệ chuyển đổi (%)

### 10.3. Xuất báo cáo

```
1. Mở báo cáo
2. Click [Menu ▼] → [Export]
3. Chọn: Excel / PDF / Print
```

---

## 11. Câu Hỏi Thường Gặp

### Q1: Làm sao biết Lead đã được ai xử lý chưa?

**A:** Kiểm tra trường "Lead Owner":
- Nếu có giá trị → Đã có người phụ trách
- Nếu trống → Chưa được gán

Cách lọc Lead chưa gán:
```
Edit Filters → Lead Owner: is not set → Apply
```

### Q2: Tại sao không tạo được Quotation từ Lead?

**A:** Kiểm tra:
1. Lead phải có ít nhất Email hoặc Phone
2. Bạn phải có quyền tạo Quotation (Sales User trở lên)
3. Lead không ở trạng thái "Do Not Contact"

### Q3: Lead bị trùng email, xử lý thế nào?

**A:** Hệ thống cảnh báo khi email trùng:
- **Nếu là cùng 1 người:** Không tạo Lead mới, cập nhật Lead cũ
- **Nếu là người khác (cùng công ty):** Liên hệ Admin để bật "Allow Duplicate Email"

### Q4: Làm sao khôi phục Lead đã xóa?

**A:** Lead đã xóa có thể khôi phục trong 30 ngày:
```
1. Vào Lead List
2. Click [Menu ▼] → [Deleted Documents]
3. Tìm Lead cần khôi phục
4. Click [Restore]
```

### Q5: Muốn gán nhiều Lead cho 1 nhân viên cùng lúc?

**A:** Sử dụng Bulk Action:
```
1. Trong Lead List, tick chọn nhiều Lead
2. Click [Actions ▼] → [Assign To]
3. Chọn nhân viên
4. Click [Assign]
```

### Q6: Status tự động thay đổi là sao?

**A:** Status được cập nhật tự động khi:
| Hành động | Status mới |
|-----------|------------|
| Tạo Opportunity | Opportunity |
| Tạo/Submit Quotation | Quotation |
| Submit Sales Order | Converted |

Bạn vẫn có thể đổi Status thủ công nếu cần.

### Q7: Làm sao xem tất cả hoạt động với 1 Lead?

**A:** Trong chi tiết Lead:
1. Tab **Activity**: Lịch sử thay đổi
2. Tab **Comments**: Ghi chú nội bộ
3. Tab **Emails**: Email đã gửi/nhận
4. Tab **Linked Documents**: Quotation, Opportunity, Sales Order liên quan

### Q8: Lead từ Facebook/Zalo vào hệ thống thế nào?

**A:** Có 2 cách:
1. **Thủ công:** Nhân viên tạo Lead, chọn Source = "Facebook" hoặc "Zalo"
2. **Tự động (cần cấu hình):** Tích hợp API với các nền tảng

### Q9: Có thể tùy chỉnh các trạng thái Lead không?

**A:** Liên hệ Admin. Có thể:
- Thêm trạng thái mới
- Đổi tên trạng thái (tiếng Việt)
- Thay đổi màu hiển thị

### Q10: Làm sao xuất danh sách Lead theo nguồn?

**A:**
```
1. Vào Lead List
2. Edit Filters → Source = "Facebook"
3. Apply
4. Menu ▼ → Export
```

---

## Phụ Lục

### A. Bảng phím tắt

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + B` | Tạo mới (New) |
| `Ctrl + S` | Lưu (Save) |
| `Ctrl + E` | Chỉnh sửa (Edit) |
| `Ctrl + G` | Đi đến (Go to) |
| `/` | Mở Search |
| `Esc` | Đóng dialog/Hủy |

### B. Glossary (Thuật ngữ)

| Thuật ngữ | Tiếng Việt | Mô tả |
|-----------|------------|-------|
| Lead | Khách tiềm năng | Khách hàng chưa mua |
| Opportunity | Cơ hội | Cơ hội bán hàng đang theo |
| Quotation | Báo giá | Bảng báo giá sản phẩm |
| Sales Order | Đơn hàng | Đơn đặt hàng đã xác nhận |
| Customer | Khách hàng | Khách đã có giao dịch |
| Territory | Khu vực | Vùng địa lý |
| Source | Nguồn | Nguồn Lead đến |
| Lead Owner | NV phụ trách | Nhân viên quản lý Lead |
| Pipeline | Quy trình | Luồng xử lý bán hàng |

### C. Liên hệ hỗ trợ

| Vấn đề | Liên hệ |
|--------|---------|
| Lỗi hệ thống | IT Support |
| Hướng dẫn sử dụng | Training Team |
| Yêu cầu tính năng mới | Product Manager |

---

**Document Version:** 1.0
**Created:** 29/01/2026
**Last Updated:** 29/01/2026
**Author:** DCNET Team

---

*© 2026 DCNET Telecom. All rights reserved.*
