# Bravo Integration Questions

> **Module:** `dcnet/bravo`
>
> **Ưu tiên:** Cao
>
> **Mục đích:** Xác định scope, phương thức và khả năng tích hợp với Bravo ERP

---

## Tổng quan vấn đề

Trong phụ lục docx chỉ đề cập **3 điểm** về Bravo:

| # | Yêu cầu trong docx | Chi tiết |
|---|-------------------|----------|
| 1 | Danh sách Chi nhánh | "API hoặc Excel đồng bộ với Bravo" |
| 2 | Import Sản phẩm | "Import sản phẩm từ Bravo qua Excel hoặc API" |
| 3 | Tồn kho (2 chiều) | "Lấy/Cập nhật tồn kho từ/sang ERP Bravo" |

**Vấn đề:** Không biết Nhật Minh đang dùng những chức năng gì trên Bravo → Không xác định được scope sync.

---

## 1. Chức năng đang sử dụng trên Bravo

### 1.1. Nhật Minh đang dùng module gì trên Bravo?

| # | Module Bravo | Đang dùng? | Ghi chú |
|---|--------------|------------|---------|
| 1 | Quản lý Sản phẩm | ☐ Có ☐ Không | |
| 2 | Quản lý Kho / Tồn kho | ☐ Có ☐ Không | |
| 3 | Quản lý Đơn hàng / Bán hàng | ☐ Có ☐ Không | |
| 4 | Quản lý Khách hàng | ☐ Có ☐ Không | |
| 5 | Kế toán / Công nợ | ☐ Có ☐ Không | |
| 6 | Quản lý Nhân sự | ☐ Có ☐ Không | |
| 7 | Báo cáo | ☐ Có ☐ Không | |
| 8 | Khác | | |

### 1.2. Workflow hiện tại

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | **Nhập sản phẩm mới** ở đâu? | ☐ Bravo ☐ Website ☐ Khác |
| 2 | **Quản lý tồn kho** ở đâu? | ☐ Bravo ☐ Website ☐ Khác |
| 3 | **Bán hàng offline** (cửa hàng) dùng gì? | ☐ Bravo ☐ POS riêng ☐ Khác |
| 4 | **Bán hàng online** (web) đơn về đâu? | ☐ Bravo ☐ WooCommerce ☐ Cả hai |
| 5 | **Quản lý khách hàng** ở đâu? | ☐ Bravo ☐ Excel ☐ Khác |
| 6 | **Kế toán / Công nợ** ở đâu? | ☐ Bravo ☐ Excel ☐ Khác |

### 1.3. Dữ liệu Master

| # | Loại dữ liệu | Master ở đâu? | Ghi chú |
|---|--------------|---------------|---------|
| 1 | Sản phẩm | ☐ Bravo ☐ CRM mới | |
| 2 | Tồn kho | ☐ Bravo ☐ CRM mới | |
| 3 | Khách hàng | ☐ Bravo ☐ CRM mới | |
| 4 | Đơn hàng | ☐ Bravo ☐ CRM mới | |
| 5 | Chi nhánh | ☐ Bravo ☐ CRM mới | |
| 6 | Nhân viên | ☐ Bravo ☐ CRM mới | |

---

## 2. Khả năng kỹ thuật của Bravo

### 2.1. API

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | Bravo đã có API sẵn chưa? | ☐ Có ☐ Không ☐ Không biết |
| 2 | Nếu có, là API đọc hay ghi? | ☐ Chỉ đọc ☐ Chỉ ghi ☐ Cả hai |
| 3 | Có tài liệu API không? | ☐ Có ☐ Không |
| 4 | Cần request Bravo cung cấp API không? | ☐ Có ☐ Không |
| 5 | Nếu cần request, có mất phí không? | ☐ Có ☐ Không ☐ Không biết |

### 2.2. Database Access

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | Bravo cho phép kết nối DB từ bên ngoài không? | ☐ Có ☐ Không |
| 2 | Loại database của Bravo? | ☐ SQL Server ☐ Oracle ☐ Khác |
| 3 | Có tài liệu DB schema không? | ☐ Có ☐ Không |

### 2.3. Export/Import

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | Bravo có chức năng export Excel không? | ☐ Có ☐ Không |
| 2 | Có thể schedule export tự động không? | ☐ Có ☐ Không |
| 3 | Bravo có chức năng import Excel không? | ☐ Có ☐ Không |

---

## 3. Đầu mối kỹ thuật

| # | Câu hỏi | Trả lời |
|---|---------|---------|
| 1 | Ai quản lý Bravo của Nhật Minh? | ☐ Tự quản lý ☐ Bravo support |
| 2 | Đầu mối kỹ thuật Bravo? | Tên: _________ SĐT: _________ |
| 3 | Có hợp đồng support với Bravo không? | ☐ Có ☐ Không |
| 4 | Phiên bản Bravo đang dùng? | ☐ Bravo 8 ☐ Bravo 10 ☐ Khác |

---

## 4. Tài liệu cần từ Nhật Minh

| # | Tài liệu | Deadline | Trạng thái |
|---|----------|----------|------------|
| 1 | Screenshot các màn hình Bravo đang dùng | 10 ngày đầu | ☐ Chưa có |
| 2 | Mẫu file Excel export từ Bravo (SP, Kho, KH) | 10 ngày đầu | ☐ Chưa có |
| 3 | Tài liệu API Bravo (nếu có) | 10 ngày đầu | ☐ Chưa có |
| 4 | Danh sách mã sản phẩm | 10 ngày đầu | ☐ Chưa có |
| 5 | Danh sách mã chi nhánh/kho | 10 ngày đầu | ☐ Chưa có |
| 6 | Danh sách mã nhân viên | 10 ngày đầu | ☐ Chưa có |

---

## 5. Các giải pháp Sync khả thi

### 5.1. Tùy thuộc vào khả năng Bravo

| Tình huống | Giải pháp | Effort | Timeline |
|------------|-----------|--------|----------|
| **Bravo có API đọc/ghi** | API Integration trực tiếp | Thấp | 2-3 tuần |
| **Bravo chỉ có API ghi** | API ghi + Excel đọc | TB | 3-4 tuần |
| **Bravo cho truy cập DB** | SQL Query trực tiếp | TB | 2-3 tuần |
| **Bravo chỉ có Excel** | Import/Export thủ công hoặc scheduled | Thấp | 1-2 tuần |
| **Bravo không hỗ trợ gì** | Chỉ sync qua WooCommerce | Cao | Hạn chế |

### 5.2. Đề xuất chiến lược

```
GIAI ĐOẠN 1 (MVP - Tháng 1-2):
└── Dùng Excel import
    • Sản phẩm từ Bravo → CRM
    • Tồn kho từ Bravo → CRM
    • Chi nhánh từ Bravo → CRM
    • Không block tiến độ dự án

GIAI ĐOẠN 2 (Tháng 3-4):
└── Nếu Bravo cung cấp API
    • Sync tồn kho real-time (2 chiều)
    • Sync đơn hàng (nếu cần)

BACKUP PLAN:
└── Nếu Bravo không hỗ trợ API
    • Scheduled Excel export/import
    • Hoặc sync qua WooCommerce (nếu đã có)
```

---

## 6. Rủi ro & Mitigation

| Rủi ro | Mức độ | Mitigation |
|--------|--------|------------|
| Bravo không có API | Cao | Dùng Excel, chấp nhận không real-time |
| Bravo tính phí API | TB | Đưa vào budget hoặc dùng Excel |
| Cấu trúc data Bravo phức tạp | TB | Cần tài liệu sớm để estimate |
| Bravo support chậm | TB | Liên hệ sớm, có backup plan |

---

## 7. Kết luận cần xác nhận

| # | Câu hỏi quyết định | Trả lời | Impact |
|---|-------------------|---------|--------|
| 1 | Bravo có API không? | | Quyết định giải pháp |
| 2 | Scope sync những gì? | | Estimate effort |
| 3 | Dữ liệu master ở đâu? | | Chiều sync |
| 4 | Chấp nhận sync qua Excel không? | | Backup plan |

---

*Cập nhật: 2025-12-08*
