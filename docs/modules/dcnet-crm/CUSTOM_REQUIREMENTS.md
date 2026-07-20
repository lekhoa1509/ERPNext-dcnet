# DCNET CRM — Custom Requirements

> Trích từ các mục `EXT`/`NEW` trong `SPEC_MAPPING.md`. Chỉ liệt kê phần custom
> có nguồn từ specification; không coi UI tham khảo là nghiệp vụ mới.

## Custom app và UI

| Thành phần | Mục đích | Spec ref | Trạng thái |
|---|---|---|---|
| Vue workspace `/desk/dcnet-crm` | UI hợp nhất cho các DocType CRM/Selling chuẩn | 3, 4, 5 | Implemented core |
| Dashboard vận hành CRM | KPI và phễu dùng dữ liệu permission-aware | 14.1–14.4 | Partial |
| Lead workspace/detail/form | Danh sách, form, timeline và chuyển đổi | 3.1–3.5 | Partial |
| Customer workspace/profile | Hồ sơ 360 và chứng từ liên quan | 4.1, 4.2, 4.4 | Implemented core |
| Opportunity workspace/form | Quản lý phễu và thương vụ | 13.1 | Implemented core |
| Quotation/Sales Order workspace | Danh sách, tạo và chi tiết chứng từ | 5.1–5.5 | Implemented core |
| Activities/Care workspace | Công việc và chăm sóc khách hàng | 4.3.1 | Partial |

## Custom DocTypes

| DocType | Mục đích | Spec ref | Ghi chú |
|---|---|---|---|
| `CRM Care Card` | Hồ sơ/lịch chăm sóc CRM | 4.3.1 | Owned by `dcnet_crm` |
| `DCNET Service Account` | Tài khoản dịch vụ phát sinh từ dòng đơn hàng | 5.2.1 | Khái niệm DCNET, liên kết `Sales Order` |

## API và permission

| Hạng mục | Yêu cầu | Spec ref |
|---|---|---|
| Permission-aware list/detail/export | Dùng `frappe.get_list` và kiểm tra quyền DocType | 3.1, 3.4, 3.8, 4.1, 4.2, 4.9, 5.1, 5.4, 5.10 |
| API tạo Customer | Authenticated endpoint, giữ nguồn và chống dữ liệu sai | 3.9 |
| API tạo Sales Order | Không bypass validation/docstatus ERPNext | 5.11 |
| Dashboard aggregation | Chỉ tổng hợp bản ghi người dùng được phép đọc | 14.1–14.4 |

## Tích hợp chưa triển khai

| Hạng mục | Dependency cần xác nhận | Spec ref |
|---|---|---|
| Auto-create Lead | Provider, auth, payload, deduplication | 3.7 |
| Promotion automation | Segmentation, schedule, provider, opt-out | 4.3.2 |
| Zalo/Messenger | Provider và credential | 4.3.6 |
| Upsell/Cross-sell | Rule gợi ý và kênh gửi | 4.3.7 |
| Resell/feedback | Trigger và business rule | 5.9 |
| E-commerce sync | Platform priority, auth và schema | 5.12 |

## Sidebar và routing

- Native Frappe Workspace Sidebar là navigation duy nhất.
- `Bàn làm việc` → Page `dcnet-crm`, route option `view=dashboard`.
- Không có mục `Tất cả` và không render sidebar thứ hai trong Vue.
- Active state phải đồng bộ theo `view` hiện tại.

## Verification bắt buộc

- Frontend syntax và Vue template compile.
- API integration tests với transaction rollback.
- Permission tests cho role Sales User, Sales Manager và System Manager.
- Build asset, migrate, clear cache và smoke test route.
