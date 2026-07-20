# DCNET CRM Feature Matrix

> Nguồn bắt buộc: `docs/feature/FEATURE_SPECIFICATION.md`  
> Nguồn tham khảo: `dcnet-crm/docs/SPEC-CRM-tinh-nang.md`  
> Cập nhật: 13/07/2026 — dashboard bento + sidebar `Bàn làm việc`

> Phạm vi release hiện tại: chỉ các luồng đã có trên sidebar, UI bám MISA.
> Tính năng mới và tích hợp ngoài được hoãn sang giai đoạn sau. `Tài khoản`
> sử dụng DocType custom `DCNET Service Account`, không phải Account kế toán.

## Module trên sidebar

| Module | DocType chính | Phạm vi production | Trạng thái |
|---|---|---|---|
| Bàn làm việc / Dashboard | Reports/API tổng hợp | KPI Lead, Opportunity, Customer, Order, giá trị đơn; phễu và cơ cấu stage | Ready vận hành, reports còn Partial |
| Tiềm năng | Lead | 3.1–3.9: CRUD, import/export, detail, chuyển đổi, nguồn ngoài/API | Ready core |
| Liên hệ | Contact | Hỗ trợ hồ sơ Lead/Customer | Ready core |
| Khách hàng | Customer | 4.1–4.9: hồ sơ 360, chăm sóc, CRUD, import/export | Partial |
| Cơ hội | Opportunity | Luồng bán hàng hỗ trợ Lead/Customer | Ready core |
| Báo giá | Quotation | Chứng từ trước Sales Order | Ready core |
| Đơn hàng | Sales Order | 5.1–5.11 trong phạm vi đơn hàng chuẩn | Ready core |
| Tài khoản | DCNET Service Account | Tự sinh từ dòng Sales Order; list/search/detail/export và liên kết đơn hàng | Ready core |
| Hoạt động | ToDo/Event/Comment | Timeline và giao việc | Partial |
| Thẻ chăm sóc | CRM Care Card | 4.3 chăm sóc khách hàng | Partial |

## Feature chính thức và coverage

| Spec | Feature | Coverage hiện tại | Việc còn lại để Done |
|---|---|---|---|
| 2.1–2.6 | Dashboard doanh số | Partial | Báo cáo theo nguồn và Top sản phẩm |
| 3.1 | Danh sách/search/filter/cột Lead | Partial | Saved filter, tags đầy đủ |
| 3.2 | Tạo Lead + check trùng | Partial | Duplicate preview trước lưu |
| 3.3 | Import Lead | Ready qua Data Import | Kiểm thử template/import lỗi |
| 3.4 | Chi tiết Lead/tư vấn/tài liệu | Partial | Upload/delete file, activity CRUD |
| 3.5 | Cập nhật Lead | Ready core | Hoàn thiện attachment/owner UX |
| 3.6 | Xóa Lead | Partial | Production delete policy |
| 3.7 | Lead từ nguồn ngoài | Blocked external | Cần credential/schema `nhanh_vn` |
| 3.8 | Export Lead | Ready | Excel theo search và quyền người dùng |
| 3.9 | API tạo Customer | Ready authenticated | Đã có test chuyển Lead → Customer + Opportunity |
| 4.1 | Danh sách/filter/cột Customer | Ready core | Một số metric nâng cao |
| 4.2 | Hồ sơ Customer 360 | Ready core | Loyalty/debt summary chuẩn hóa |
| 4.3.1 | Lịch chăm sóc | Partial | Recurrence/reminder scheduler |
| 4.3.2 | Lịch khuyến mãi | Blocked external | Chưa có provider/rule được duyệt |
| 4.3.3 | Ticket | Missing | Map sang Issue + UI |
| 4.3.4 | Phân quyền nhóm CSKH | Partial | Customer assignment UI |
| 4.3.5 | Khảo sát hài lòng | Partial | Form/web route gửi khảo sát |
| 4.3.6 | Zalo/Messenger | Blocked external | Credential/provider chưa có |
| 4.3.7 | Upsell/Cross-sell | Missing | Rule và kênh gửi chưa được duyệt |
| 4.4 | Cập nhật Customer | Ready core | Lịch chăm sóc/chiết khấu riêng |
| 4.5 | Nguồn Customer | Ready qua Lead Source | Settings UX |
| 4.6 | Tích điểm | ERPNext Loyalty Program | Ngoài app CRM hiện tại |
| 4.7 | Xóa Customer | Partial | Production delete policy |
| 4.8 | Import Customer | Ready qua Data Import | Kiểm thử template/import lỗi |
| 4.9 | Export Customer | Ready | Excel theo search và quyền người dùng |
| 5.1 | Danh sách Sales Order | Ready core | Hoàn thiện print UX |
| 5.2 | Tạo Sales Order | Ready core | Các loại Fitting/Coaching/Trade-in thuộc app khác |
| 5.3 | Import Sales Order | Ready qua Data Import | UAT mẫu import |
| 5.4 | Chi tiết Sales Order | Ready core | Hoàn thiện link điều hướng |
| 5.5 | Cập nhật Sales Order | Ready core | UAT draft/submitted |
| 5.6 | Bảo hành | Ngoài core CRM | Thuộc workflow bảo hành được duyệt riêng |
| 5.7 | Xóa Sales Order | ERPNext permission | Chỉ draft/cancel theo chuẩn |
| 5.8 | In Sales Order | ERPNext Print | Hoàn thiện nút CRM |
| 5.9 | Resell | Blocked clarify | Chưa có business rule |
| 5.10 | Export Sales Order | Ready | Excel theo search và quyền người dùng |
| 5.11 | API Sales Order | Ready authenticated | Contract/API tests |
| 5.12 | Đồng bộ sàn TMĐT | Blocked external | Credential/schema từng sàn |

## Điều hướng production

- `Bàn làm việc` mở `/desk/dcnet-crm?view=dashboard`.
- Sidebar không còn mục `Tất cả`; dashboard chỉ có một điểm truy cập.
- Active state được đồng bộ theo view hiện tại.
- Dashboard dùng layout bento, dữ liệu KPI/phễu tuân theo permission của người dùng.
- Dashboard vận hành không thay thế bộ báo cáo đầy đủ tại spec 2.1–2.6 và
  14.1–14.4.

## Quy tắc production

- `Ready`: có code, permission và test.
- `Partial/Missing`: không được hiện như control hoạt động trong production.
- `Blocked external`: không triển khai giả khi chưa có credential hoặc business rule.
- Feature tham khảo MISA nhưng không xuất hiện trong spec khách hàng không được tính
  là blocker production.
- Không thêm module/feature mới ngoài sidebar trong release hiện tại.
