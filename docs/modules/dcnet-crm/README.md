# DCNET CRM

> Tài liệu kỹ thuật cho custom app `dcnet_crm`. Đây là app trải nghiệm người
> dùng liên module, không thay thế tài liệu nghiệp vụ theo STT của từng module.

| Hạng mục | Giá trị |
|---|---|
| **Phạm vi** | Dashboard CRM, Lead, Liên hệ, Khách hàng, Cơ hội, Báo giá, Đơn hàng, Hoạt động, Thẻ chăm sóc, Tài khoản dịch vụ |
| **Công ty** | Thăng Long TM + Nhật Minh Sport |
| **Nguồn chính thức** | `docs/feature/FEATURE_SPECIFICATION.md` mục 2, 3, 4, 5, 13, 14 |
| **ERPNext base** | `Lead`, `Contact`, `Customer`, `Opportunity`, `Quotation`, `Sales Order`, `ToDo`, `Event` |
| **Custom app** | `dcnet-crm/` |
| **Route** | `/desk/dcnet-crm?view=dashboard` |
| **Trạng thái** | Đang hoàn thiện; core CRM ready, integrations và một số CSKH/report còn partial/blocked |

## Nguyên tắc phạm vi

- Specification khách hàng là source of truth.
- MISA/video chỉ là nguồn tham khảo UI/interaction.
- Không hiển thị control production cho tính năng chưa hoàn thiện.
- Mọi API phải dùng permission của Frappe/ERPNext.
- Không sửa ERPNext core và không nhân bản các DocType CRM chuẩn.

## Điều hướng hiện tại

`Bàn làm việc` mở trực tiếp dashboard. Sidebar không còn mục `Tất cả`.

| Menu | View | Dữ liệu chính |
|---|---|---|
| Bàn làm việc | `dashboard` | KPI và phễu CRM |
| Tiềm năng | `leads` | `Lead` |
| Liên hệ | `contacts` | `Contact` |
| Khách hàng | `customers` | `Customer` |
| Cơ hội | `opportunities` | `Opportunity` |
| Báo giá | `quotations` | `Quotation` |
| Đơn hàng | `orders` | `Sales Order` |
| Tài khoản | `accounts` | `DCNET Service Account` |
| Hoạt động | `activities` | `ToDo`, `Event`, `Comment` |
| Thẻ chăm sóc | `care` | `CRM Care Card` |

## Dashboard CRM

Dashboard dùng layout bento theo mẫu UI được duyệt, gồm:

- KPI Tiềm năng, Cơ hội, Khách hàng, Đơn hàng và Giá trị đơn hàng.
- Phễu và donut cơ cấu cơ hội theo `Sales Stage`.
- Thao tác nhanh tạo Lead, Opportunity, Customer và Quotation.
- Nút làm mới dữ liệu; dữ liệu tuân theo quyền người dùng hiện tại.

Dashboard này là màn hình vận hành CRM. Các báo cáo doanh số đầy đủ của đặc tả
mục 2 và 14 vẫn được theo dõi tại module Dashboard/Báo cáo tương ứng; không coi
KPI CRM hiện tại là đã hoàn thành toàn bộ 2.1–2.6 hoặc 14.1–14.4.

## Tiến độ tài liệu

- [x] README
- [x] SPEC_MAPPING.md
- [x] CLARIFY.md
- [x] CUSTOM_REQUIREMENTS.md
- [x] Workflow tracker
- [x] UI customization log
- [x] User guide dùng chung tại `docs/training/custom-apps/dcnet-crm/USER_GUIDE.md`
- [ ] Khách hàng xác nhận integrations, GPS và công thức báo cáo
- [ ] PR / merge

## Tài liệu trong folder

| File | Mô tả |
|---|---|
| `SPEC_MAPPING.md` | Mapping từng mục spec sang ERPNext và trạng thái app |
| `CLARIFY.md` | Các câu hỏi còn chờ khách hàng xác nhận |
| `CUSTOM_REQUIREMENTS.md` | Các phần EXT/NEW thuộc custom app |
| `WORKFLOW_TRACKER.md` | Tiến độ triển khai và kiểm tra |

## Code reference

| Thành phần | File |
|---|---|
| Vue root/router | `dcnet-crm/frontend/src/app.js` |
| Dashboard | `dcnet-crm/frontend/src/features/dashboard/` |
| Feature views | `dcnet-crm/frontend/src/features/` |
| Styling | `dcnet-crm/frontend/src/styles.css` |
| Permission-aware API | `dcnet-crm/dcnet_crm/api.py` |
| Setup/sidebar | `dcnet-crm/dcnet_crm/install.py` |
| Sidebar fixture | `dcnet-crm/dcnet_crm/workspace_sidebar/crm.json` |

## Tài liệu liên quan

- `dcnet-crm/docs/FEATURE_MATRIX.md`
- `dcnet-crm/HANDOFF.md`
- `docs/customization/ui/2026-07-13-dcnet-crm-dashboard-redesign.md`
- `docs/training/custom-apps/dcnet-crm/USER_GUIDE.md`
