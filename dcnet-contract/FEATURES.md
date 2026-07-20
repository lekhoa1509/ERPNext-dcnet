# DCNET Contract — Features

App: `dcnet_contract` | Stack: Frappe v16 + ERPNext v16 | Version: v0.2.0 (realignment, chưa push GitHub)

## v0.2.0 changelog (2026-05-14 — realignment 8 decisions D1-D8)

- **`DCNET Contract Item.item_kind`** — Select `Setup Fee` / `Recurring Service` / `One-off Goods` (reqd, default Recurring Service). `payment_mode` is now per-item; engine walks items and packs per-item billing rows.
- **`contract_type` computed** — derived from item_kinds (Recurring / One-off / Mixed). No more cứng Select. `appendix_no`/`appendix_date` removed.
- **`Contract Addendum` child table** — `addenda` holds the phụ lục history (addendum_no, signing date, effective_from, change_type, summary, signed PDF). Each row hints PAKD to add a matching `PAKD Revision`.
- **Auto-invoice scheduler** — `tasks.py` stamps `Sales Invoice.dcnet_contract` + `Sales Invoice.billing_period_idx` on every generated SI; `before_save` on SI/PE fills the same fields when an accountant creates one manually.
- **Custom field SI/PE fixture** — `Sales Invoice.dcnet_contract` (Link, in_standard_filter), `Sales Invoice.billing_period_idx` (Int), `Payment Entry.dcnet_contract` (Link read-only), `Payment Entry.billing_period_idx` (Int read-only). Loaded via `fixtures/custom_field.json` so `bench migrate` auto-imports them.
- **Bi-directional links** — `DCNET Contract.links` now exposes Sales Invoice + Payment Entry (filter `dcnet_contract`) so Frappe renders Connections panel + counts automatically.
- **HTML section "Hóa đơn & Thanh toán"** — Section Break + HTML field render per-period SI/PE/Commission status (8 cols, lazy-load > 50 SI).

## A. Features Đã Thực Hiện

### A1. Master Contract (DocType DCNET Contract)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A1.1 | DocType DCNET Contract | Autoname `HD-{YYYY}-{#####}`, submittable, đầy đủ thông tin HĐ (khách hàng, công ty, chi nhánh, sales person, dịch vụ, gói, địa chỉ lắp đặt) | Done | 2026-04-13 |
| A1.2 | Thông tin khách hàng mở rộng | customer_name, customer_address, phone/fax/email, tax_id, representative, CMND/CCCD | Done | 2026-04 |
| A1.3 | Sync-back khách hàng | Tự đồng bộ CMND/CCCD + địa chỉ/điện thoại về Customer khi submit HĐ | Done | 2026-04 |
| A1.4 | Contract Items (child) | `DCNET Contract Item` — gói dịch vụ, đơn giá, số lượng, doanh thu/kỳ | Done | 2026-04-13 |
| A1.5 | Branch ↔ Cost Center mapping | Child table `DCNET Contract Branch CC Map` — map chi nhánh sang cost center phục vụ GL | Done | 2026-04-13 |
| A1.6 | Auto-fill từ Customer | Điền sẵn customer_name, địa chỉ, tax_id khi chọn Customer | Done | 2026-04 |

### A2. Recurring Contract (Billing Schedule)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A2.1 | DocType Billing Schedule | Child table `DCNET Contract Billing Schedule` — lịch xuất hóa đơn theo kỳ | Done | 2026-04-13 |
| A2.2 | Auto-generate schedule | Sinh lịch billing khi submit HĐ theo chu kỳ (monthly/quarterly/yearly) | Done | 2026-04-13 |
| A2.3 | Pro-rata kỳ đầu/cuối | Tính pro-rata cho kỳ không đủ tháng (bắt đầu giữa tháng, kết thúc giữa tháng) | Done | 2026-04-13 |
| A2.4 | Status tracking | Mỗi row có status: Scheduled / Invoiced / Paid / Cancelled | Done | 2026-04-13 |
| A2.5 | Scheduled auto-invoice | Daily job `run_auto_invoice` — tự tạo Sales Invoice khi đến kỳ | Done | 2026-04-13 |
| A2.6 | PE on_submit hook | Khi Payment Entry submit → mark billing row Paid | Done | 2026-04-13 |
| A2.7 | PE on_cancel hook | Khi PE cancel → revert billing row Paid → Invoiced | Done | 2026-04-13 |
| A2.8 | Overdue check | Daily job `run_overdue_check` — cảnh báo công nợ quá hạn | Done | 2026-04-13 |

### A3. One-off Goods Contract (Shadow Sales Order)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A3.1 | Shadow SO pattern | Tự tạo Sales Order ẩn cho HĐ bán thiết bị 1 lần — module `shadow_so.py` | Done | 2026-04-13 |
| A3.2 | Cascade cancel | Cancel HĐ → cancel shadow SO kèm theo | Done | 2026-04-13 |
| A3.3 | Permission query | `permissions.so_permission_query` — ẩn shadow SO khỏi user thường | Done | 2026-04-13 |

### A4. Contract Lifecycle & State Machine

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A4.1 | State machine | Module `utils/state_machine.py` — transition rules | Done | 2026-04-13 |
| A4.2 | Workflow states | Draft / Pending / Active / Suspended / Terminated / Expired | Done | 2026-04 |
| A4.3 | Scheduled expire | Daily job `run_expire_contracts` — auto set Expired khi hết hạn | Done | 2026-04-13 |
| A4.4 | Revision chain | Track HĐ sửa đổi qua các phiên bản (parent_contract link) | Done | 2026-04-13 |
| A4.5 | Cancel mid-term | Xử lý chấm dứt giữa kỳ, tính pro-rata phần đã sử dụng | Done | 2026-04-13 |
| A4.6 | English-first workflow | Tất cả Select options bằng English, vi.csv dịch | Done | 2026-04 |

### A5. Template Management (Contract Template)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A5.1 | DocType DCNET Contract Template | Quản lý thư viện mẫu HĐ | Done | 2026-04-13 |
| A5.2 | Child: Template Item | `DCNET Contract Template Item` — gói dịch vụ mặc định | Done | 2026-04-13 |
| A5.3 | Child: Template Placeholder | `DCNET Contract Template Placeholder` — khai báo biến trong mẫu | Done | 2026-04-16 |
| A5.4 | Upload/preview/active | Upload .docx, toggle active/inactive | Done | 2026-04-16 |
| A5.5 | Apply template | `template_engine.apply_template()` — áp mẫu vào HĐ (@frappe.whitelist) | Done | 2026-04-16 |
| A5.6 | Client integration | `dcnet_contract_template_integration.js` — nút "Áp dụng mẫu" trên form HĐ | Done | 2026-04-16 |
| A5.7 | Dual-format migrate | Tự chuyển template format cũ sang format mới trong `_migrate_templates_to_dual_format` | Done | 2026-04-16 |

### A6. DOCX Template Engine (Print)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A6.1 | DOCX generator | Module `utils/docx_generator.py` — điền biến vào .docx mẫu | Done | 2026-04-13 |
| A6.2 | Placeholder engine | Module `utils/placeholder_engine.py` — hỗ trợ dual-language + typo detection | Done | 2026-04-16 |
| A6.3 | 6 mẫu DOCX mặc định | hd-dich-vu-vien-thong, hd-ftth-doanh-nghiep, hd-ftth-ho-gia-dinh, pl-internet-leased-line-ill, pl-kenh-thue-rieng-p2p, pl-truyen-so-lieu-mpls | Done | 2026-04-13 |
| A6.4 | Placeholders đầy đủ | Mỗi mẫu ≥34 key: thông tin Bên A/Bên B, service section, phụ lục | Done | 2026-04-13 |
| A6.5 | Auto re-upload on migrate | Compare content disk vs DB → re-upload khi file trên disk đổi | Done | 2026-04-13 |
| A6.6 | Standalone print button | Nút in .docx trực tiếp từ form HĐ, không qua Print Format HTML | Done | 2026-04 |
| A6.7 | Print Format HTML: Hợp đồng chuẩn | `hop_dong_chuan` — full-content print từ DOCX template | Done | 2026-04 |
| A6.8 | Print Format HTML: Phụ lục | `phu_luc_hop_dong` — phụ lục HĐ | Done | 2026-04 |

### A7. Credit Note & Cancel Mid-term

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A7.1 | Auto credit note on cancel | Tự tạo credit note khi cancel HĐ có SI đã phát hành | Done | 2026-04 |
| A7.2 | Clear workflow_state before insert | Fix lỗi insert credit note với workflow_state cũ | Done | 2026-04 |

### A8. VAT & GL Integration

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A8.1 | VAT template | Gán Sales Taxes and Charges Template mặc định theo Settings | Done | 2026-04 |
| A8.2 | Income account override | Override TK doanh thu theo service_type / package | Done | 2026-04 |
| A8.3 | Revenue recognition on SI | Doanh thu ghi nhận ngay trên Sales Invoice (theo review 2026-04-16) | Done | 2026-04 |
| A8.4 | JE draft by default | Các bút toán liên quan HĐ mặc định tạo Draft | Done | 2026-04 |

### A9. Settings

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A9.1 | DocType DCNET Contract Settings | Single DocType — cấu hình mặc định | Done | 2026-04-13 |
| A9.2 | Default accounts | TK doanh thu, TK phải thu, VAT template, cost center mặc định | Done | 2026-04-13 |
| A9.3 | Cutoff & grace period | Cấu hình ngày cutoff billing, grace period overdue | Done | 2026-04-13 |

### A10. Workspace, Dashboard & Navigation

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A10.1 | Workspace Contract Manager | 4 number cards + 3 charts + 3 shortcuts, title ASCII | Done | 2026-04-13 |
| A10.2 | Workspace Sidebar | `dcnet_contract.json` — điều hướng sidebar riêng | Done | 2026-04-13 |
| A10.3 | Desktop Icon | Đăng ký icon Desk home, link_type=Workspace Sidebar, link_to set | Done | 2026-04 |
| A10.4 | 4 Number Cards | Active Contracts, Total Monthly Revenue, Overdue Amount, Contracts Expiring This Month | Done | 2026-04-13 |
| A10.5 | 3 Dashboard Charts | Monthly Contract Value, Revenue by Service Type, Contracts by Status | Done | 2026-04-13 |
| A10.6 | Number card methods | `number_card_methods.py` — custom query cho các KPI | Done | 2026-04-13 |

### A11. Reports

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A11.1 | Contract Expiry Report | Script Report — danh sách HĐ sắp hết hạn | Done | 2026-04-13 |
| A11.2 | Outstanding Receivables by Contract | Script Report — công nợ phải thu theo HĐ | Done | 2026-04-13 |

### A12. Integration với PAKD

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A12.1 | Contract ↔ PAKD linkage | Field link 2 chiều giữa HĐ và PAKD | Done | 2026-04 |
| A12.2 | Vietnamese labels | Label tiếng Việt cho các field link, translation CSV | Done | 2026-04 |

### A13. Localization (English-first i18n)

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A13.1 | English-first source | Tất cả Select options, error messages, report headers bằng English | Done | 2026-04 |
| A13.2 | Vietnamese translations | 159 entries trong `translations/vi.csv` | Done | 2026-04 |

### A14. Tests

| # | Feature | Mô tả | Status | Ngày |
|---|---------|-------|--------|------|
| A14.1 | test_dcnet_contract | 18 test cases — controller, validate, submit/cancel | Done | 2026-04-13 |
| A14.2 | test_billing_schedule | 19 test cases — sinh lịch, pro-rata, auto-invoice | Done | 2026-04-13 |
| A14.3 | test_state_machine | 16 test cases — workflow transition rules | Done | 2026-04-13 |
| A14.4 | test_tasks_and_events | 13 test cases — scheduler jobs, PE hooks | Done | 2026-04-13 |
| A14.5 | test_docx_generator | 19 test cases — DOCX fill variable | Done | 2026-04-13 |
| A14.6 | test_placeholder_engine | 15 test cases — dual-language + typo detection | Done | 2026-04-16 |
| A14.7 | test_template_engine | 6 test cases — apply template | Done | 2026-04-16 |
| A14.8 | Edge case guards | Validation guards: HĐ rỗng item, cancel khi đã thu, revision không hợp lệ | Done | 2026-04 |

---

## B. Features Đang Phát Triển

(Trống — v0.1.0 code-complete, chưa push lên GitHub)

---

## C. Features Sẽ Thực Hiện

### C1. E-signature & E-invoice

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C1.1 | E-signature integration | Tích hợp chữ ký điện tử (VNPT/Viettel/FPT) cho HĐ | High | Khách hàng ký online |
| C1.2 | E-invoice integration | Tự phát hành hóa đơn điện tử khi tạo SI từ billing schedule | High | VNPT/Viettel/BKAV |

### C2. Đa tiền tệ & Gia hạn

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C2.1 | Multi-currency contracts | Hỗ trợ USD/EUR cho HĐ với khách nước ngoài | Medium | Cần tỷ giá + multi-currency SI |
| C2.2 | Auto-renewal | Tự gia hạn HĐ khi gần hết hạn + notification | Medium | Cấu hình per contract |
| C2.3 | Renewal proposal | Sinh bản đề xuất gia hạn với giá cập nhật | Low | |

### C3. Customer Self-Service

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C3.1 | Customer portal | Khách hàng xem HĐ, hóa đơn, công nợ qua portal | Medium | Dùng Frappe Portal |
| C3.2 | Mobile app khách hàng | App cho khách hàng tự quản lý HĐ, báo sự cố | Low | |

### C4. Báo Cáo Nâng Cao

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C4.1 | Churn report | Tỉ lệ khách hàng hủy HĐ theo tháng | Medium | |
| C4.2 | Revenue by contract type | Doanh thu chia theo loại HĐ / dịch vụ | Medium | |
| C4.3 | Customer lifetime value | CLV — tổng doanh thu trọn đời khách hàng | Low | |

### C5. Tích Hợp Khác

| # | Feature | Mô tả | Priority | Ghi chú |
|---|---------|-------|----------|---------|
| C5.1 | CRM integration | Link Opportunity → Contract khi chốt deal | Medium | Frappe CRM |
| C5.2 | HRMS commission | Trigger commission cho sales khi HĐ Active | High | Qua dcnet_pakd |
| C5.3 | vn_banking reconcile | Đối soát PE từ sao kê ngân hàng → mark billing Paid | High | App riêng vn_banking |

---

## Legend

| Status | Nghĩa |
|--------|-------|
| Done | Code-complete trên branch main (chưa push GitHub, v0.1.0) |
| In Progress | Đang fix/build trên feature branch |
| Planned | Có spec hoặc đã thảo luận, chưa bắt đầu code |
| — (Priority) | High = cần cho go-live, Medium = cần trong 3 tháng, Low = nice-to-have |
