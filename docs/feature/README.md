# Feature Documentation

> Tài liệu đặc tả chức năng cho dự án DCNET Flow (Nhật Minh Sport)

---

## 📚 Tài liệu Đặc tả

### Đợt 1: CRM Requirements (08/12/2025)

| File | Mô tả | Modules |
|------|-------|---------|
| [FEATURE_SPECIFICATION.md](./FEATURE_SPECIFICATION.md) | Đặc tả CRM (Lead, Customer, Order, Analytics...) | 16 modules |

**Nội dung**:
- Lead Management (Danh sách, Tạo/Sửa/Xóa, Rule chia Lead)
- Customer Management (Customer 360, Chăm sóc tự động, Loyalty)
- Order Management (Lẻ/Sỉ, Fitting, Coaching, Trade-in)
- Product, Warehouse, Shipping
- Reports & Analytics (Dashboard, Heatmap, Website Analytics)
- Integrations (Bravo ERP, E-commerce, Zalo OA, Messenger)

---

### Đợt 2: ERP Requirements (30/12/2025)

| File | Mô tả | Modules |
|------|-------|---------|
| [ERP_SPECIFICATION.md](./ERP_SPECIFICATION.md) | Đặc tả ERP (Bán hàng, Mua hàng, Kho, Kế toán) | 5 phân hệ |
| [IMPORT_PROCESS_SPECIFICATION.md](./IMPORT_PROCESS_SPECIFICATION.md) | Quy trình Nhập hàng (Đại lý & TLTM) | 2 quy trình |

**Nội dung ERP_SPECIFICATION.md**:
- **Quản lý Bán hàng**: 12 bước (Kế hoạch, Bảng giá, Chiết khấu, Đơn hàng, **Hạn mức công nợ**, Hóa đơn...)
- **Quản lý Mua hàng**: 10 bước (Kế hoạch, PO, Giao hàng, Nhập khẩu, Thanh toán...)
- **Quản lý Kho**: 12 bước (Nhập/Xuất, Điều chuyển, **In tem mã vạch**, Kiểm kê, Tính giá vốn...)
- **Quản lý Kế toán**: Tiền mặt, Ngân hàng, Công nợ, TSCĐ, Thuế, **Chi phí hỗ trợ hãng**
- **Kết nối Web**: Đồng bộ Danh mục, Đơn hàng, Tồn kho

**Nội dung IMPORT_PROCESS_SPECIFICATION.md**:
- **Quy trình Đại lý cấp 1**: 7 bước (Họp → Trải nghiệm → Đặt hàng → Nhận hàng → Thanh toán)
- **Quy trình Thăng Long TM**: 9 bước (Lịch trình → Khám phá SP → Đặt hàng → Hải quan → Nhận hàng)
- **Lịch trình đặt hàng**: 7 loại sản phẩm (Gậy, Softgoods, Quần áo...)
- **Phân công bộ phận**: 10 bộ phận (GĐ KD, Marketing, Nhập hàng, Kho, Kế toán...)

---

## 📊 So sánh 2 đợt

| Tiêu chí | Đợt 1 (FEATURE_SPEC) | Đợt 2 (ERP_SPEC) |
|----------|----------------------|------------------|
| **Focus** | CRM (UX/UI, User stories) | ERP (Business process, Technical specs) |
| **Modules** | 16 modules | 5 phân hệ |
| **Chi tiết** | Danh sách cột, Filter, Search, Action buttons | Quy trình 12 bước, Thông tin cần có, Tính năng cần có |
| **Mới** | Lead, Customer 360, Analytics, Loyalty | Mua hàng, Kế toán, Hạn mức công nợ, In tem, Hàng ký gửi |

---

## 🎯 Cách sử dụng

### Scenario 1: PM muốn overview
- **Đọc**: README.md này (5 phút)
- **Xem**: 2 file SPECIFICATION để biết toàn bộ requirements

### Scenario 2: Dev build feature X
1. **CRM feature** (Lead, Customer, Order...) → Đọc FEATURE_SPECIFICATION.md
2. **ERP feature** (Mua hàng, Kế toán, Kho...) → Đọc ERP_SPECIFICATION.md
3. **Import process** → Đọc IMPORT_PROCESS_SPECIFICATION.md

### Scenario 3: BA clarify với NM
- Reference đúng file đặc tả (FEATURE_SPEC hoặc ERP_SPEC)
- Xem section/bước cụ thể

---

## 📋 Gap Analysis

| File | Mô tả |
|------|-------|
| [ERPNEXT_COVERAGE_ANALYSIS.md](./ERPNEXT_COVERAGE_ANALYSIS.md) | **Phân tích Coverage: Spec vs ERPNext v16** (~120 có sẵn / ~117 cần build mới) |

---

## 📝 Lịch sử

| Ngày | Nội dung | File |
|------|----------|------|
| 08/12/2025 | Đợt 1: CRM Requirements | FEATURE_SPECIFICATION.md |
| 30/12/2025 | Đợt 2: ERP Requirements | ERP_SPECIFICATION.md<br>IMPORT_PROCESS_SPECIFICATION.md |

---

**© 2025 DCNET Corporation**
