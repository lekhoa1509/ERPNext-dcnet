# CHANGELOG - Yêu cầu từ khách hàng

Lịch sử các đợt cung cấp yêu cầu/tài liệu từ Nhật Minh Sport

---

## [Đợt 2] 30/12/2025 - ERP & Quy trình Nhập hàng

### Tài liệu nhận được

Nhật Minh cung cấp **3 file Word** chi tiết về ERP & Quy trình nghiệp vụ:

| File gốc | Nội dung | Dòng |
| --- | --- | --- |
| `Tính năng yêu cầu CRM.doc` | Đặc tả ERP (Bán hàng, Mua hàng, Kho, Kế toán) | ~1,680 |
| `QUY TRÌNH NHẬP HÀNG - ĐẠI LÝ.docx` | Quy trình nhập hàng Đại lý cấp 1 (7 bước) | ~140 |
| `QUY TRÌNH NHẬP HÀNG TLTM.docx` | Quy trình nhập hàng Thăng Long TM (9 bước, 10 bộ phận) | ~165 |

### Tài liệu đã tổng hợp

| File Markdown | Nguồn | Mô tả |
| --- | --- | --- |
| [ERP_SPECIFICATION.md](./feature/ERP_SPECIFICATION.md) | `Tính năng yêu cầu CRM.doc` | 5 phân hệ ERP |
| [IMPORT_PROCESS_SPECIFICATION.md](./feature/IMPORT_PROCESS_SPECIFICATION.md) | 2 file Quy trình | 2 quy trình nhập hàng |

### Nội dung chính

#### **ERP\_SPECIFICATION.md** - 5 phân hệ

**1. Quản lý Bán hàng** (12 bước):
- Kế hoạch bán hàng theo năm
- Bảng giá niêm yết
- Chính sách chiết khấu (bán buôn/bán lẻ)
- ⚠️ **Bước 7-8: Kiểm tra hạn mức công nợ & Công nợ quá hạn** (Critical)
- Hóa đơn, Hàng trả lại, Tính thưởng

**2. Quản lý Mua hàng** (10 bước) - ⚠️ **MỚI**:
- Kế hoạch mua hàng → Đơn hàng mua → Kế hoạch giao hàng
- Đề nghị nhập hàng → Phiếu nhập mua/khẩu
- Chi phí mua hàng → Trả lại NCC → Đề nghị thanh toán
- **Tracking PO Number của hãng**
- **Import ảnh hàng loạt** (theo quy ước tên file)

**3. Quản lý Kho** (12 bước):
- Tồn kho đầu kỳ → Nhập/Xuất kho → Điều chuyển kho/vị trí
- ⚠️ **In tem mã vạch** (Tem tự in: `mã_vật_tư + ;; + số_lô`, Tem NCC: `số_seri`)
- Kiểm kê → Chênh lệch kiểm kê
- Tính giá vốn hàng xuất (trung bình tháng)
- ⚠️ **Quy trình hàng ký gửi** (TLTM ↔ Nhật Minh - 5 bước)

**4. Quản lý Kế toán** - ⚠️ **MỚI**:
- Kế toán tiền mặt, ngân hàng, công nợ phải thu/trả
- Kế toán TSCĐ, CCDC
- Kế toán thuế (kết xuất file cho phần mềm thuế)
- ⚠️ **Tính chi phí hỗ trợ của hãng**
- ⚠️ **Báo cáo chi phí theo sự kiện** (Marketing, Demo, bán hàng, sai giá)
- Báo cáo tổng hợp cho NM + Đại diện hãng (cùng dùng Bravo)

**5. Kết nối Web bán hàng**:
- Đồng bộ: Danh mục KH, Hàng hóa, Kho, Đơn hàng, Tồn kho

#### **IMPORT\_PROCESS\_SPECIFICATION.md** - 2 quy trình

**1. Quy trình Đại lý cấp 1** (7 bước):
- Họp → Trải nghiệm SP → Nhận Order Form → Đặt hàng → Vận chuyển → Nhận & Kiểm tra (01 ngày) → Thanh toán

**2. Quy trình Thăng Long TM** (9 bước):
- Lịch trình → **Khám phá SP** (6 bộ phận họp) → Đặt hàng → Xác nhận → Kế hoạch giao hàng → Vận chuyển → **Hải quan** → Catalog → Nhận & Kiểm tra (01 ngày)

**Lịch trình đặt hàng** - 7 loại sản phẩm:
- Gậy năm tiếp theo (T9-10)
- Driver, FW, Rescue, Irons (Launch T1-2, MOQ 10 pcs)
- Softgoods US (Hàng tháng)
- Gậy P Series (2 năm/lần)
- Putters, Wedges (Hàng năm)
- Quần áo & PK JP (2 lần/năm: Xuân/Hè T6-7, Thu/Đông T11-12)

**Phân công bộ phận** (10 bộ phận):
- Giám đốc Kinh Doanh (chủ trì họp đánh giá SP mới)
- Nhập hàng, Marketing, Kinh doanh, Kỹ thuật, Fashionista
- Đại lý cấp 1, Kế toán, Kho, Logistics

### Impact - Những gì bổ sung

Đợt tài liệu này **bổ sung thêm**:
- ✅ **Quản lý Mua hàng** (10 bước) - Thiếu hoàn toàn trong FEATURE_SPEC
- ✅ **Quản lý Kế toán** (đầy đủ) - Thiếu hoàn toàn trong FEATURE_SPEC
- ✅ **Hạn mức công nợ** (Bước 7-8 Bán hàng) - Critical
- ✅ **Hàng ký gửi** (TLTM ↔ NM) - Critical
- ✅ **In tem mã vạch** - Quan trọng
- ✅ **Import ảnh hàng loạt** - Nice-to-have
- ✅ **Quy trình Nhập hàng** (2 quy trình, lịch trình, phân công) - Đầy đủ

### Plugins bổ sung

Thêm **6 plugins mới** (tổng cộng 16 plugins):

**Critical:**
- `dcnet/pricing` - Bảng giá, chiết khấu
- `dcnet/credit-management` - Hạn mức công nợ
- `dcnet/consignment` - Hàng ký gửi

**Supporting:**
- `dcnet/purchase` - Quản lý Mua hàng
- `dcnet/accounting` - Quản lý Kế toán
- `dcnet/barcode-printing` - In tem mã vạch

---

## [Đợt 1] 08/12/2025 - CRM Specification

### Tài liệu nhận được

| File gốc | Nguồn | Mô tả |
| --- | --- | --- |
| PHỤ LỤC Hợp đồng | Hợp đồng DCNET - Nhật Minh | Đặc tả CRM |

### Tài liệu đã tổng hợp

| File Markdown | Nguồn | Mô tả |
| --- | --- | --- |
| [FEATURE_SPECIFICATION.md](./feature/FEATURE_SPECIFICATION.md) | PHỤ LỤC hợp đồng | 16 modules CRM |

### Nội dung chính

**Modules CRM** (16 modules):
1. **Lead Management**: Danh sách, Tạo/Sửa/Xóa, Rule chia Lead
2. **Customer Management**: Customer 360, Chăm sóc tự động, Loyalty
3. **Order Management**: Lẻ/Sỉ, Fitting, Coaching, Trade-in
4. **Product**: Danh mục, Biến thể, Thương hiệu
5. **Warehouse**: Đa kho, Tồn kho
6. **Shipping**: Viettel Post, tracking
7. **Reports & Analytics**: Dashboard, Heatmap, Website Analytics
8. **Integrations**: Bravo ERP, E-commerce, Zalo OA, Messenger

### Plugins ban đầu

**Phase 1 - Critical (6 plugins):**
- `dcnet/leads` - Lead management
- `dcnet/fitting` - Đơn Fitting golf
- `dcnet/coaching` - Đơn Coaching
- `dcnet/bravo` - Sync Bravo ERP

**Phase 2 - Supporting (4 plugins):**
- `dcnet/ecommerce` - Shopee, TikTok, Lazada
- `dcnet/shipping` - Viettel Post

---

## Timeline Summary

| Đợt | Ngày | Nội dung | Plugins | Modules |
| --- | --- | --- | --- | --- |
| **Đợt 1** | 08/12/2025 | CRM Specification | 6 plugins | 16 modules |
| **Đợt 2** | 30/12/2025 | ERP + Quy trình | +6 plugins (tổng 12) | +5 phân hệ ERP |
| **Meeting** | 30/12/2025 | Quyết định BỎ Bravo, làm Kho+Kế toán | -1 +2 (tổng 13) | Timeline 6→8 tháng |

---

**© 2025 DCNET Corporation**
