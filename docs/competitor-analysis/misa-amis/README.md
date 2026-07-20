# MISA AMIS — Tổng quan nền tảng

## Giới thiệu

MISA AMIS là nền tảng quản trị doanh nghiệp hợp nhất lớn nhất Việt Nam, phục vụ 170,000+ doanh nghiệp. Platform SaaS (cloud-based), no-code, tích hợp AI.

## Kiến trúc 4 mảng

| Mảng | Ứng dụng chính | Tương đương DCNET Flow |
|------|----------------|----------------------|
| **Tài chính** | Kế toán, Hóa đơn điện tử, Quản lý tài sản | Modules 22-30 (Kế toán) |
| **Bán hàng** | CRM, Bán hàng, Marketing | Modules 08-14 (Bán hàng), 33-36 (CRM) |
| **Nhân sự** | HRM, Chấm công, Tính lương | Ngoài scope DCNET Flow |
| **Điều hành** | Quy trình, Công việc, Tài liệu | Workflow engine (ERPNext built-in) |

## Quy mô

- **40+ ứng dụng** trong hệ sinh thái
- **170,000+ khách hàng** (SME Việt Nam)
- **50+ tính năng AI** tích hợp
- **Mobile app** đầy đủ (iOS/Android)

## Modules đã phân tích

| Module | File | Ngày |
|--------|------|------|
| [Quy Trình](quy-trinh/ANALYSIS.md) | `quy-trinh/ANALYSIS.md` | 17/03/2026 |
| [HRM (Nhân sự)](hrm/ANALYSIS.md) | `hrm/ANALYSIS.md` | 19/03/2026 |
| [CRM (Bán hàng)](crm/ANALYSIS.md) | `crm/ANALYSIS.md` | 11/06/2026 |

## Nhận xét chung

**Điểm mạnh:** Tích hợp hệ sinh thái, UX phù hợp VN, no-code, giá SME-friendly.

**Điểm yếu:** Vendor lock-in, không open-source, không self-hosted, API hạn chế.

**So với ERPNext:** MISA mạnh hơn ở UX/localization cho VN, ERPNext mạnh hơn ở customization/open-source/API. DCNET Flow cần kết hợp ưu điểm cả hai.
