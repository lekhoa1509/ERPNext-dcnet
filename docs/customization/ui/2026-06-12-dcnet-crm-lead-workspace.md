# DCNET CRM Lead Workspace

**Ngày:** 12/06/2026  
**App:** `dcnet_crm`  
**Route:** `/desk/dcnet-crm#/leads`

## Nguồn yêu cầu

- `docs/feature/FEATURE_SPECIFICATION.md` Section 3.1 - Danh sách Lead
- `docs/feature/FEATURE_SPECIFICATION.md` Section 3.4 - Xem chi tiết Lead
- UI reference: `docs/competitor-analysis/misa-amis/crm/ANALYSIS.md`

## Phạm vi triển khai

- Tạo Frappe app riêng `dcnet-crm`, module kỹ thuật `DCNET CRM`
- Vue 3 workspace với top navigation
- Tri-pane Lead list:
  - Filter panel
  - Lead table
  - Communication activity panel
- Search theo tên và email
- Filter theo trạng thái, nguồn, nhân viên phụ trách và thời gian tạo
- Permission-aware API dựa trên quyền `Lead` và `Communication`
- Responsive layout cho màn hình nhỏ

## Chưa triển khai

Các field/filter sau có trong requirement nhưng chưa có mapping chuẩn trên ERPNext Lead:

- Chi nhánh
- Ngày nhận Lead
- Độ tuổi/ngày sinh
- Liên hệ lần cuối
- Tổng số tương tác

Các mục này cần được đưa vào `SPEC_MAPPING.md` hoặc custom-field specification trước
khi bổ sung, theo quy tắc spec-first của dự án.

Lead scoring và quy trình ghi doanh số trong CRM design chưa được triển khai vì hiện chỉ
có nguồn từ competitor analysis, chưa có yêu cầu khách hàng tương ứng.
