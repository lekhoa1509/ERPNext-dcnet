# Screenshot Manifest — DCNET Custom Apps Training

> **Site:** `http://127.0.0.1:8000`  
> **Thời gian crawl:** 13/07/2026  
> **Persona:** System Manager (`Administrator`)  
> **Chế độ:** Read-only — không Save, Submit, Import, Delete, Disable hoặc thay đổi quyền.

## DCNET CRM

| File | Màn hình / route | Xử lý dữ liệu | Trạng thái | Ghi chú |
|---|---|:---:|---|---|
| `01-crm-dashboard-system-manager.png` | `/desk/dcnet-crm?view=dashboard` | Giữ nguyên | CAPTURED | Dashboard và KPI từ dữ liệu demo |
| `02-lead-list-system-manager.png` | `?view=leads` | Giữ nguyên | CAPTURED | Tên, email và điện thoại demo |
| `03-lead-detail-system-manager.png` | `?view=lead-detail&lead=CRM-LEAD-2026-00010` | Giữ nguyên | CAPTURED | Thông tin liên hệ demo |
| `03b-lead-create-form-system-manager.png` | Form tạo Lead | Giữ nguyên | CAPTURED | Mở form, không Save |
| `04-customer-list-system-manager.png` | `?view=customers` | Giữ nguyên | CAPTURED | Dữ liệu khách hàng demo |
| `07-contact-list-system-manager.png` | `?view=contacts` | Giữ nguyên | CAPTURED | Dữ liệu liên hệ demo |
| `08-opportunity-list-system-manager.png` | `?view=opportunities` | Giữ nguyên | CAPTURED | Dữ liệu cơ hội demo |
| `10-quotation-list-system-manager.png` | `?view=quotations` | Giữ nguyên | CAPTURED | Dữ liệu báo giá demo |
| `11-sales-order-list-system-manager.png` | `?view=orders` | Giữ nguyên | CAPTURED | Dữ liệu đơn hàng demo |
| `13-activity-workspace-system-manager.png` | `?view=activities` | Giữ nguyên | CAPTURED | Dữ liệu hoạt động demo |
| `14-care-card-list-system-manager.png` | `?view=care` | Giữ nguyên | CAPTURED | Dữ liệu chăm sóc demo |
| `16-service-account-list-system-manager.png` | `?view=accounts` | Giữ nguyên | CAPTURED | Dữ liệu tài khoản dịch vụ demo; không hiển thị secret |

## DCNET Migrate

| File | Màn hình / route | Đã che dữ liệu | Trạng thái | Ghi chú |
|---|---|:---:|---|---|
| `01-import-auto-workspace-system-manager.png` | `/desk/import-auto-home` | Không cần | CAPTURED | Workspace |
| `02-import-auto-list-system-manager.png` | `/desk/import-auto` | Không cần | CAPTURED | Danh sách một batch hiện có |
| `03-import-auto-document-system-manager.png` | `/desk/import-auto/IMPORT-AUTO-2026-00002` | Không cần | CAPTURED | Full page hồ sơ đã có |
| `03-import-auto-document-top-system-manager.png` | Cùng route | Không cần | CAPTURED | Vùng đầu hồ sơ |
| `04-file-analysis-status-system-manager.png` | Cùng route, khu vực AI status | Không cần | CAPTURED | Không bấm Import |
| — | Smart Plan / Duplicate dialog | — | BLOCKED_NO_SAFE_SAMPLE | Không mở hành động có nguy cơ chạy lại xử lý |
| — | AI Settings | — | SKIPPED_NOT_AVAILABLE | Không mở trang có thể lộ API key |

## DCNET Permission

| File | Màn hình / route | Đã che dữ liệu | Trạng thái | Ghi chú |
|---|---|:---:|---|---|
| `01-permission-workspace-system-manager.png` | `/desk/dcnet-permission` | Có | CAPTURED | Workspace |
| `02-permission-dashboard-system-manager.png` | `/desk/dcnet-permission-manager` | Có | CAPTURED | Email đã che |
| `03-create-user-dialog-system-manager.png` | Dialog Tạo user | Có | CAPTURED | Mật khẩu mặc định đã che; không Save |
| `04-module-permissions-system-manager.png` | Tab Phân quyền Module | Có | CAPTURED | Không đổi toggle, không Save |
| `06-permission-scope-list-system-manager.png` | `/desk/dcnet-permission-scope` | Có | CAPTURED | Scope Kế toán |
| — | Ma trận quyền user | — | BLOCKED_NO_SAFE_SAMPLE | Scope hiện có 0 user; không tạo user để chụp |

## Tổng hợp

- CRM: 12 ảnh hợp lệ.
- Migrate: 5 ảnh hợp lệ.
- Permission: 5 ảnh hợp lệ.
- Tổng: 22 ảnh thực tế được giữ lại.
- Không có thao tác ghi dữ liệu trong quá trình crawl.
- Một lần màn hình Opportunity tải chậm; crawler đã chờ và chụp lại ảnh hợp lệ.
