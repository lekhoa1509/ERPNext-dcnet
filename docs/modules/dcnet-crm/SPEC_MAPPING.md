# DCNET CRM — Spec → ERPNext Mapping

> **Nguồn:** `docs/feature/FEATURE_SPECIFICATION.md` mục 2, 3, 4, 5, 13, 14  
> **ERPNext:** v16 — CRM, Selling và Frappe Desk  
> **UX tham khảo:** MISA/video; không phải nguồn tạo thêm nghiệp vụ  
> **Cập nhật:** 13/07/2026

## Quy ước

| Tag | Nghĩa |
|---|---|
| `USE` | ERPNext có sẵn, dùng trực tiếp |
| `CFG` | ERPNext có, cần cấu hình |
| `EXT` | Mở rộng DocType/UI/API chuẩn |
| `NEW` | Khái niệm không có tương đương phù hợp, build trong `dcnet_crm` |
| `REF` | Theo dõi và nghiệm thu ở module khác |

| Trạng thái | Nghĩa |
|---|---|
| Ready | Core flow đã có và đã kiểm tra |
| Partial | Có một phần, chưa đáp ứng toàn bộ spec |
| Blocked | Thiếu business rule, provider hoặc credential |
| Ref | Không thuộc phạm vi hoàn thành của app CRM |

## 2. Dashboard

Dashboard trong `dcnet_crm` là màn hình vận hành CRM, không thay thế dashboard
doanh số chính thức của module 02.

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 2.1 | Doanh số ngày/tuần/tháng và khoảng tùy chọn | Dashboard/Báo cáo doanh số; API CRM mới chỉ tổng hợp đơn theo khoảng | `REF` | Partial |
| 2.2 | Doanh số bán sỉ theo đại lý | `Sales Order`, Customer Group; module báo cáo | `REF` | Ref |
| 2.3 | Tổng doanh số bán lẻ | `Sales Order`, Customer Type/Group; module báo cáo | `REF` | Ref |
| 2.4 | Doanh số theo nguồn khách hàng | `Lead Source`/UTM + báo cáo | `REF` | Ref |
| 2.5 | Doanh số theo nguồn đơn hàng | Trường nguồn đơn + báo cáo | `REF` | Blocked |
| 2.6 | Top 20 sản phẩm bán chạy | Sales Analytics/Item-wise report | `REF` | Ref |

## 3. Quản lý Lead

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 3.1 | Danh sách, cột, search/filter, tags | `Lead` + Vue list/filter/column UI | `EXT` | Partial |
| 3.2 | Tạo Lead và kiểm tra trùng | `Lead` + internal form + validation | `EXT` | Partial |
| 3.3 | Import Excel | Frappe Data Import | `CFG` | Ready |
| 3.4 | Chi tiết, giao dịch, tư vấn, bình luận, tài liệu | `Lead`, `Communication`, `Comment`, `ToDo`, `File` | `EXT` | Partial |
| 3.5 | Cập nhật thông tin, tài liệu, người phụ trách | `Lead`, Assignment, `File` | `EXT` | Partial |
| 3.6 | Xóa Lead | Permission và delete chuẩn | `USE` | Partial |
| 3.7 | Lead tự động từ `nhanh_vn`/đa kênh | Integration chưa có schema/credential | `EXT` | Blocked |
| 3.8 | Export Excel | Permission-aware export API | `EXT` | Ready |
| 3.9 | API tạo khách hàng từ hệ thống khác | Authenticated Frappe API | `EXT` | Ready |

## 4. Quản lý Khách hàng

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 4.1 | Danh sách, cột, search/filter | `Customer` + saved view/column/filter UI | `EXT` | Ready core |
| 4.2 | Hồ sơ 360, giao dịch, điểm, công nợ, tài liệu | Internal profile + linked ERPNext transactions | `EXT` | Partial |
| 4.3.1 | Lịch chăm sóc tự động | `ToDo`/Event + `CRM Care Card`; thiếu scheduler hoàn chỉnh | `NEW` | Partial |
| 4.3.2 | Lịch gửi khuyến mãi tự động | Cần segmentation, provider và rule gửi | `NEW` | Blocked |
| 4.3.3 | Ticket hỗ trợ | Map sang `Issue` + assignment/workflow | `EXT` | Chưa làm |
| 4.3.4 | Phân quyền CSKH theo nhóm | User Permission/assignment | `EXT` | Partial |
| 4.3.5 | Khảo sát hài lòng | Web Form/Survey + liên kết Customer | `EXT` | Partial |
| 4.3.6 | Zalo OA/Messenger | External integration | `NEW` | Blocked |
| 4.3.7 | Upsell/Cross-sell tự động | Lịch sử mua + recommendation/send rule | `NEW` | Blocked |
| 4.4 | Cập nhật Customer, chiết khấu, lịch chăm sóc, tài liệu | `Customer` + internal edit UI | `EXT` | Partial |
| 4.5 | CRUD nguồn khách hàng | `Lead Source`/UTM Source | `CFG` | Ready core |
| 4.6 | Quy tắc tích điểm/lên hạng | ERPNext Loyalty Program; module 38 | `REF` | Ref |
| 4.7 | Xóa Customer | Permission/dependency chuẩn | `USE` | Partial |
| 4.8 | Import Excel | Frappe Data Import | `CFG` | Ready |
| 4.9 | Export Excel | Permission-aware export API | `EXT` | Ready |

## 5. Quản lý Đơn hàng

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 5.1 | Danh sách, cột, loại đơn, search/filter | `Sales Order` + internal list | `EXT` | Ready core |
| 5.2.1 | Tạo đơn vật dụng bán lẻ/bán buôn | Internal form tạo `Sales Order` chuẩn | `EXT` | Ready core |
| 5.2.2 | Sales Order phát sinh từ Fitting | Module 34 Fitting | `REF` | Ref |
| 5.2.3 | Sales Order phát sinh từ Coaching | Module 35 Coaching | `REF` | Ref |
| 5.2.4 | Sales Order thu cũ đổi mới | Module 14 Trade-in | `REF` | Ref |
| 5.2.5 | Đơn bảo hành/bảo trì | Workflow bảo hành riêng | `REF` | Chưa làm |
| 5.2.6 | Kiểm tra tồn theo kho | ERPNext stock balance API | `EXT` | Ready core |
| 5.3 | Import đơn hàng | Frappe Data Import | `CFG` | Ready |
| 5.4 | Chi tiết đơn hàng | Internal Sales Order detail | `EXT` | Ready core |
| 5.5 | Cập nhật đơn hàng | ERPNext draft/submit rules | `USE` | Ready core |
| 5.6 | Bảo hành | Warranty/Issue + custom workflow | `REF` | Chưa làm |
| 5.7 | Xóa đơn hàng | ERPNext permission/docstatus | `USE` | Ready core |
| 5.8 | In đơn hàng | ERPNext Print Format | `CFG` | Partial |
| 5.9 | Resell/feedback/cross-sell | Chưa có rule và provider | `NEW` | Blocked |
| 5.10 | Export đơn hàng | Permission-aware export API | `EXT` | Ready |
| 5.11 | API tạo đơn hàng | Authenticated API tạo `Sales Order` | `EXT` | Ready |
| 5.12 | Đồng bộ Shopee/TikTok/Lazada/Website | External integrations | `NEW` | Blocked |

## 13. Cài đặt

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 13.1 | Phân công Lead, tags, trạng thái cơ hội | Assignment, Tag, `Sales Stage` | `CFG` | Partial |
| 13.2 | CRUD chức vụ và phân quyền | Designation/Role; module HR/Permission | `REF` | Ref |
| 13.3 | CRUD nhóm khách hàng | `Customer Group` | `CFG` | Ready core |
| 13.4 | Trạng thái đơn hàng | ERPNext status/docstatus; tùy chỉnh cần xác nhận | `CFG` | Blocked clarify |
| 13.5 | Hành động nhân viên | `ToDo`, `Event`, `Communication`; tùy chỉnh cần xác nhận | `EXT` | Partial |

## 14. Báo cáo

| Spec | Yêu cầu | ERPNext/DCNET mapping | Tag | Trạng thái |
|---|---|---|---|---|
| 14.1 | Báo cáo doanh số theo thời gian/chi nhánh/tag/nguồn/sản phẩm | ERPNext reports + custom Script Reports | `EXT` | Partial |
| 14.2 | Báo cáo đơn hàng và dịch vụ đặc thù | Sales Analytics + module Fitting/Coaching | `EXT` | Partial |
| 14.3 | Báo cáo Lead/Customer/doanh thu/hài lòng | CRM reports + survey data | `EXT` | Partial |
| 14.4 | Báo cáo hiệu suất nhân viên | Sales Person/owner reports | `EXT` | Partial |
| 14.5 | Báo cáo kho | Module 08/ERPNext Stock reports | `REF` | Ref |

## DocType ownership

| UI/domain | Dữ liệu | Quyết định |
|---|---|---|
| Lead | `Lead` | Dùng lại ERPNext |
| Cơ hội | `Opportunity` | Dùng lại ERPNext |
| Khách hàng | `Customer` | Dùng lại ERPNext |
| Liên hệ | `Contact` | Dùng lại ERPNext |
| Báo giá | `Quotation` | Dùng lại ERPNext |
| Đơn hàng | `Sales Order` | Dùng lại ERPNext |
| Hoạt động | `ToDo`, `Event`, `Comment`, `Communication` | Dùng lại Frappe/ERPNext |
| Thẻ chăm sóc | `CRM Care Card` | Custom DocType trong `dcnet_crm`, phục vụ 4.3.1 |
| Tài khoản dịch vụ | `DCNET Service Account` | Custom DocType trong `dcnet_crm`, liên kết dòng Sales Order |

Không tạo bản sao cho các DocType CRM chuẩn. Hai Custom DocType nêu trên là các
khái niệm riêng của DCNET và được sở hữu trực tiếp bởi app `dcnet_crm`.

## Kiểm soát phạm vi

- Dashboard CRM hiện tại không được đánh dấu hoàn thành cho toàn bộ mục 2/14.
- Tích hợp ngoài không triển khai giả khi chưa có provider, credential và schema.
- Feature tham khảo MISA nhưng không có trong specification không được đưa vào
  mapping như yêu cầu khách hàng.
