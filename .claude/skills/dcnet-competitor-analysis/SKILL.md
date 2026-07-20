---
name: dcnet-competitor-analysis
description: Use when analyzing competitor software modules (MISA AMIS, 1Office, Base.vn, Odoo, SAP) to create structured ANALYSIS.md with ERPNext gap mapping. Triggers - phan tich doi thu, competitor analysis, so sanh phan mem, MISA, 1Office, Base.vn, Odoo
---

# DCNET Competitor Analysis

## Overview

Phân tích chi tiết module phần mềm đối thủ, tạo ANALYSIS.md chuẩn với ERPNext gap mapping phục vụ thiết kế DCNET Flow.

## When to Use

- User says `/dcnet-competitor-analysis {platform} {module}` (e.g., `/dcnet-competitor-analysis misa-amis hrm`)
- User wants to analyze a competitor's module
- User says "phân tích đối thủ", "so sánh phần mềm", "competitor analysis"
- User wants ERPNext gap mapping for a specific competitor feature

## Invocation

```
/dcnet-competitor-analysis {platform} {module}
```

**Examples:**
- `/dcnet-competitor-analysis misa-amis hrm`
- `/dcnet-competitor-analysis misa-amis ke-toan`
- `/dcnet-competitor-analysis 1office crm`

## Process

```
┌─────────────────────────────────────────────────┐
│ 1. RESEARCH — Thu thập thông tin                │
│    • Web search: trang chính thức + help center │
│    • Tính năng, giá, screenshots, API docs      │
│    • Ưu/nhược điểm từ reviews                  │
├─────────────────────────────────────────────────┤
│ 2. STRUCTURE — Phân tích theo 9 sections chuẩn  │
│    • Tổng quan → Trụ cột → Tích hợp → BC      │
│    • Ưu/nhược → Gap mapping → Bài học          │
├─────────────────────────────────────────────────┤
│ 3. MAP — So sánh với ERPNext                    │
│    • Từng tính năng → ERPNext equivalent        │
│    • Gap level: Available / Partial / Full gap  │
│    • Tổng kết % coverage                        │
├─────────────────────────────────────────────────┤
│ 4. SATELLITE — Xác định modules vệ tinh        │
│    • Module nào liên quan/phụ thuộc?            │
│    • Tên gọi trong hệ sinh thái đối thủ?       │
│    • Map sang ERPNext DocType tương ứng         │
├─────────────────────────────────────────────────┤
│ 5. WRITE — Tạo ANALYSIS.md + cập nhật README   │
│    • Output: docs/competitor-analysis/{platform}/{module}/ANALYSIS.md │
│    • Update: {platform}/README.md + parent README.md │
└─────────────────────────────────────────────────┘
```

## Output Structure — ANALYSIS.md

**9 sections bắt buộc** (theo template đã proven từ quy-trinh):

| # | Section | Nội dung |
|---|---------|----------|
| 1 | **Tổng quan sản phẩm** | Tên, thuộc platform nào, SaaS/On-premise, khách hàng, giá, mobile, AI, website. Sơ đồ vị trí trong hệ sinh thái |
| 2 | **Trụ cột chính** (2-4 pillars) | Phân tích sâu từng nhóm tính năng lớn. Bảng chi tiết, flow diagrams |
| 3 | **Tích hợp** | Kết nối với modules/apps khác trong hệ sinh thái. Open API capabilities |
| 4 | **Báo cáo & Dashboard** | Report builder, dashboard, export capabilities |
| 5 | **Quản lý chất lượng** (nếu có) | QA, compliance, audit trail |
| 6 | **Ưu điểm** | Numbered list, focus điểm mạnh thực sự |
| 7 | **Nhược điểm / Hạn chế** | Numbered list, đánh giá khách quan |
| 8 | **Mapping vs ERPNext** | ⭐ Bảng gap analysis chi tiết — cột: #, Tính năng, ERPNext equivalent, Gap level, Ghi chú. Tổng kết Available/Partial/Full gap/N/A |
| 9 | **Bài học áp dụng cho DCNET Flow** | UX/UI lessons, workflow design, integration ideas |

**Cuối file:** Section Sources với links tham khảo (trang chính thức + help center)

## Gap Levels

| Level | Ký hiệu | Nghĩa | Action |
|-------|----------|--------|--------|
| **Available** | ✅ | ERPNext có sẵn | Config + test |
| **Partial** | 🔶 | ERPNext có nhưng cần bổ sung | Custom field/script |
| **Full gap** | ❌ | ERPNext không có, cần build | Custom DocType/module |
| **N/A** | ➖ | Không cần cho DCNET Flow | Skip |

## Satellite Module Analysis

Mỗi module phân tích cần xác định **modules vệ tinh** — các module liên quan/phụ thuộc:

```markdown
## Modules vệ tinh

| Module vệ tinh | Tên trong {platform} | ERPNext equivalent | Vai trò |
|-----------------|----------------------|--------------------|---------|
| Phòng ban       | AMIS HRM → Cơ cấu tổ chức | Department (tree) | Cung cấp org structure cho workflow |
| Nhân viên       | AMIS HRM → Hồ sơ NV | Employee | Master data |
| ...              | ...                  | ...                | ...     |
```

## Research Strategy

### Web Search Queries
```
"{platform name}" "{module name}" site:help*.vn OR site:*.misa.vn
"{platform name}" "{module name}" tính năng
"{platform name}" "{module name}" hướng dẫn sử dụng
"{platform name}" "{module name}" đánh giá review
"{platform name}" API documentation
```

### Key Sources for MISA AMIS
- Main: `amis.misa.vn/amis-{module}/`
- Help: `helpamis.misa.vn/amis-{module}/`
- Blog: `amis.misa.vn/tag/{module}/`

## File Naming Convention

```
docs/competitor-analysis/
└── {platform-slug}/           # misa-amis, 1office, base-vn, odoo
    ├── README.md              # Platform overview + module list
    └── {module-slug}/         # hrm, ke-toan, crm, ban-hang, kho
        └── ANALYSIS.md        # Phân tích chi tiết
```

**Slug rules:** lowercase, dấu gạch ngang, không dấu tiếng Việt

## Quality Checklist

- [ ] 9 sections đầy đủ
- [ ] Gap mapping table có ≥15 tính năng
- [ ] Tổng kết gap % (Available/Partial/Full gap/N/A)
- [ ] Satellite modules identified + mapped to ERPNext
- [ ] Sources section với ≥4 links
- [ ] Platform README.md updated
- [ ] Parent README.md updated
- [ ] Key takeaways cho DCNET Flow (actionable, không generic)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Chỉ list tính năng, không map ERPNext | Mỗi tính năng PHẢI có ERPNext equivalent + gap level |
| Gap analysis quá sơ sài (<10 items) | Tối thiểu 15 tính năng, cover hết trụ cột chính |
| Bài học quá generic ("UX tốt") | Cụ thể: "Giao diện phê duyệt nên có Approve/Reject rõ ràng" |
| Thiếu satellite modules | Luôn hỏi: module này phụ thuộc data từ đâu? output đi đâu? |
| Copy-paste từ website không phân tích | Phải có nhận xét, so sánh, đánh giá — không phải dịch lại marketing |
