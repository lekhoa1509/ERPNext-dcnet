# Competitor Analysis

Tài liệu phân tích các phần mềm quản trị doanh nghiệp trên thị trường Việt Nam, phục vụ tham khảo khi thiết kế DCNET Flow.

## Mục đích

1. Hiểu cách tiếp cận của đối thủ với các bài toán tương tự
2. Lấy ý tưởng UX/UI và workflow tốt
3. Đánh giá gap giữa ERPNext và expectations của khách hàng VN
4. Định hướng tính năng custom cần phát triển

## Phần mềm đã phân tích

| Phần mềm | Modules | Ghi chú |
|-----------|---------|---------|
| [MISA AMIS](misa-amis/) | [Quy Trình](misa-amis/quy-trinh/ANALYSIS.md), [HRM](misa-amis/hrm/ANALYSIS.md) | Nền tảng SaaS lớn nhất VN, 170,000+ DN |

## Hướng dẫn thêm phần mềm mới

Tạo folder theo cấu trúc:

```
docs/competitor-analysis/
└── {ten-phan-mem}/
    ├── README.md           # Tổng quan platform
    └── {ten-module}/
        └── ANALYSIS.md     # Phân tích chi tiết module
```

Mỗi `ANALYSIS.md` cần có:
- Tổng quan sản phẩm (tên, platform, khách hàng, giá)
- Kiến trúc và tính năng chính
- Ưu/nhược điểm
- **Mapping so sánh với ERPNext** (bảng gap analysis)
- Sources (link tham khảo)

## Phần mềm tiềm năng phân tích thêm

- **1Office** — ERP SaaS VN (quy trình, HRM, CRM)
- **Base.vn** — Work management platform
- **FastWork** — Quy trình phê duyệt
- **SAP Business One** — ERP quốc tế phổ biến tại VN
- **Odoo** — Open-source ERP (đối thủ trực tiếp ERPNext)
