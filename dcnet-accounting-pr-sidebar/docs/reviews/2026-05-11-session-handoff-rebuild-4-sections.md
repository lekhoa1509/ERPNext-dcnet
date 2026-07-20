# Handoff — Rebuild 4 Sidebar Sections: Giá thành / Tổng hợp / BCTC / Phân tích & Quản trị

**Người viết:** Claude Opus 4.7
**Ngày:** 2026-05-11
**Bối cảnh:** User (Long) thất vọng với kết quả multi-session (10 sessions / opus + sonnet alternating) đã tạo 4 sections nói trên. Muốn rebuild lại từ đầu trong session mới.

---

## 1. Trạng thái hiện tại

### Branch
- Local: `feat/giathanh-tonghop-bctc` (chưa push remote)
- Base: `78af380` (Merge PR #48)
- 18 commits ahead, +11,141 / −228 lines, 94 files
- Working tree clean

### 4 sections sidebar hiện tại (DB synced, 128 items total)

#### Giá thành (6 items)
- Phân bổ chi phí mua hàng → Landed Cost Voucher ✅ (đã wire JS + COA resolver, hoạt động)
- Chi phí chờ phân bổ → Landed Cost Pending Allocation Report ✅
- Cấu hình phân bổ chi phí mua hàng → LCV Allocation Settings ✅
- Báo cáo tính giá thành SX → manufacturing-costing-wizard Page ⚠️ (đã neuter JE creation, chỉ còn aggregate + unit cost)
- Kết quả tính giá thành → Work In Progress Valuation DocType ⚠️ (còn sống nhưng chưa rõ workflow tiếp theo)
- Tập hợp chi phí SX kỳ → Production Cost Aggregation Report ⚠️ (chưa implement phân bổ 627 đa tiêu thức)

#### Tổng hợp (7 items)
- Đánh giá lại ngoại tệ → Exchange Rate Revaluation (ERPNext native) ✅
- Phiếu khóa sổ kỳ → Period Closing Voucher (ERPNext native) ✅
- Định nghĩa kỳ kế toán → Accounting Period (ERPNext native) ✅
- Sổ nhật ký chung (S03a-DN) → S03a-DN So Nhat Ky Chung Report ⚠️ (chưa verify đúng TT99/2025 layout)
- Sổ cái (S03b-DN) → S03b-DN So Cai Report ⚠️
- Sổ chi tiết tài khoản → Account Detail Ledger ⚠️
- Bảng cân đối số phát sinh → Trial Balance Sheet ⚠️

#### Báo cáo tài chính (5 items)
- Báo cáo tình hình tài chính (B01-DN) → B01-DN Bao Cao Tinh Hinh Tai Chinh Report ⚠️ (chưa verify mapping đúng)
- Báo cáo kết quả HĐKD (B02-DN) → B02-DN Bao Cao KQHDKD Report ⚠️
- Báo cáo lưu chuyển tiền tệ (B03-DN) → B03-DN Bao Cao LCTT Report ⚠️
- Thuyết minh BCTC (B09-DN) → b09-dn-generator Page ⚠️
- Cấu hình BCTC Mapping → BCTC Mapping DocType ⚠️

#### Phân tích & Quản trị (4 items, section mới tạo)
- Lợi nhuận gộp → Gross Profit (ERPNext native) ✅
- Lãi/Lỗ gộp & ròng → Gross and Net Profit Report ✅
- Phân tích lợi nhuận → Profitability Analysis ✅
- Chỉ số tài chính → Financial Ratios ✅

(Section này dùng ERPNext core reports, không có custom code — đó là lý do tất cả ✅)

---

## 2. Tài liệu opus đã viết trong session (input cho session mới)

| File | Nội dung |
|---|---|
| `docs/reviews/2026-05-11-sidebar-review-giathanh-tonghop-bctc.md` | KTT-mode review từng item — phát hiện 17/29 items có vấn đề. Đề xuất cấu trúc mới (đã apply một phần) |
| `docs/reviews/2026-05-11-realtime-accounting-conflict-analysis.md` | Phân tích xung đột ERPNext real-time vs TT99/2025 traditional flow. Audit 3 wizard (period-closing, manufacturing-costing, LCV) tìm bug nghiêm trọng |
| `docs/specs/2026-05-11-giathanh-tonghop-bctc.md` (sonnet viết, 916 dòng) | Spec gốc của multi-session — **CẨN THẬN**: nhiều assumption sai về real-time accounting, một số mapping TK chưa đúng VAS |
| `docs/BUSINESS_LOGIC.md §11-14` | Business logic 4 section — cũng có assumption sai (vd: bảng §11.6 ghi LCV expense_account = 156, thực ra phải là 331/333x) |
| `docs/plans/2026-05-11-giathanh-tonghop-bctc-plan.md` | Plan thực thi của multi-session |
| `docs/multi-session/giathanh-tonghop-bctc.md` | Task file |

---

## 3. Lỗi điển hình của multi-session (PHẢI tránh ở session mới)

| Lỗi | Root cause | Lesson |
|---|---|---|
| Period-closing wizard có 3 bug nghiêm trọng (cancel/idempotent/duplicate PCV) | Sonnet không hiểu real-time GL semantics của ERPNext. Build wizard theo TT200 truyền thống mà không check ERPNext PCV đã có sẵn | **Audit ERPNext native trước khi build custom**. Nếu native đã giải quyết, dùng native |
| Manufacturing-costing-wizard double-count với Stock Entry | Sonnet không trace Stock Entry "Manufacture" tự sinh GL real-time | **Vẽ data flow trước khi viết JE creation code** |
| VAT NK khấu trừ làm LCV row | Sonnet copy mechanism từ TT200 sample, không hiểu LCV ERPNext luôn capitalize | **Mọi JE phải trace lại VAS section + ERPNext core mechanism** |
| Sidebar có duplicates + ERPNext-core/custom mix | Sonnet add từng item theo spec mà không cross-check với items đã có | **Sidebar build phải có ONE pass tổng hợp** — không build per-phase |
| LCV thiếu client-side JS, 2 checkbox vô tác dụng | Spec không yêu cầu client JS; sonnet build server-only | **Mọi UI flag (Check/Select) trên form custom field PHẢI có client-side handler nếu thay đổi UI** |
| Default expense accounts rỗng (mặc dù comment "resolved per-company") | Sonnet viết comment intent nhưng không implement | **Comment-without-code là bug — phải có test cho mỗi nhánh code** |
| 13/17 acceptance criteria "verified" nhưng feature thực không chạy | Sonnet check file tồn tại, JSON parse được — không test live browser | **Acceptance criteria phải là live functional test, không phải structural assertion** |
| Sonnet alternating với opus trong multi-session | Runner default --model sonnet cho continuations, chỉ session 1 là opus | **Multi-session với --model opus chỉ apply session 1**. Phải hard-code lại nếu muốn opus throughout |

---

## 4. Decisions đã chốt + chưa chốt

### Đã chốt (qua AskUserQuestion trong session)
- ✅ Bỏ wizard period-closing-911, dùng ERPNext native Period Closing Voucher
- ✅ Refactor manufacturing-costing-wizard thành report-only (không tự create JE)
- ✅ Sổ Nhật ký chung KHÔNG cần hiển thị bút toán kết chuyển 5xx→911 monthly — PCV yearly là đủ
- ✅ DN target: nhỏ-vừa (SI/PI <500/tháng, 1-3 cost center)
- ✅ VAT NK khấu trừ KHÔNG làm LCV row, tạo JE riêng qua button
- ✅ Section "Phân tích & Quản trị" tạo mới, tách khỏi BCTC chuẩn
- ✅ BC hợp nhất ẩn hoàn toàn (DN single-entity)
- ✅ BOM → Section "Danh mục"
- ✅ Work Order bỏ khỏi sidebar KTT

### Chưa chốt — câu hỏi cho session mới
1. **Tập hợp chi phí SX kỳ + Báo cáo tính giá thành SX**: 2 entry points có overlap (cả 2 đều aggregate 621/622/627). Có cần cả 2 không? Hay merge?
2. **WIP Valuation (Work In Progress Valuation)**: KTT lưu kết quả tính giá thành ở đây để làm gì sau đó? Có cần workflow approve/post-JE không?
3. **TT 627 phân bổ đa tiêu thức**: 6 tiêu thức (giờ máy/công/sản lượng/NVL/NC/tổng trực tiếp) chưa implement. Có cần cho DN target (nhỏ-vừa) không?
4. **B01-DN/B02-DN/B03-DN custom reports**: sonnet code có chạy được không? Mapping TK qua BCTC Mapping DocType có đúng TT99/2025 không?
5. **B09-DN multi-sheet Excel**: page sinh Excel có đầy đủ template + nhãn không?
6. **Sổ S03a/S03b-DN**: layout có khớp Phụ lục IV TT99/2025 không?
7. **PCV `pcv_hooks.py`**: validate vn_lock_unlock_reason — field này đã thêm vào PCV chưa? Hook có chạy không?

---

## 5. Đề xuất phương pháp cho session mới

### KHÔNG NÊN
- ❌ Không dùng multi-session.sh — sonnet sẽ lặp lại lỗi
- ❌ Không inherit spec gốc `2026-05-11-giathanh-tonghop-bctc.md` mà không challenge từng giả định
- ❌ Không build hết 4 section trong 1 session — sẽ rơi vào pattern "structurally OK, business wrong"

### NÊN
1. **Bắt đầu bằng `/office-hours` hoặc `/superpowers:brainstorming`** với prompt:
   > "Em là KTT của DN VN nhỏ-vừa dùng ERPNext. Đọc 2 review docs ở `docs/reviews/2026-05-11-*.md` để hiểu trạng thái + lỗi. Brainstorm với em scope thực tế của 4 section sidebar: Giá thành / Tổng hợp / BCTC / Phân tích. Mỗi section trả lời: (a) KTT làm gì hàng ngày/cuối kỳ? (b) ERPNext native đã hỗ trợ gì? (c) Cần custom gì? (d) Workflow + JE chuẩn theo VAS + ERPNext real-time."

2. **Sau brainstorm, viết spec mới ngắn gọn** (≤300 dòng, không phải 916 dòng như cũ). Mỗi feature có:
   - Why (VAS reference)
   - ERPNext native cover được bao nhiêu %
   - Custom cần làm gì (chỉ phần delta)
   - Live test criteria (mở browser, click X, expect Y)

3. **Implement từng section một**, commit + live test ngay trước khi chuyển section. Không multi-session.

4. **Mỗi feature DocType/Page/Report custom: viết live test scenario trước, code sau** (TDD-ish nhưng cho browser flow).

### Có thể dùng cho session mới
- `apps/vn_accounting/docs/reviews/2026-05-11-sidebar-review-giathanh-tonghop-bctc.md` — bảng review từng item, cấu trúc đề xuất
- `apps/vn_accounting/docs/reviews/2026-05-11-realtime-accounting-conflict-analysis.md` — bug đã tìm được + design pattern đúng

### Phần đã đúng — giữ lại
- LCV (Landed Cost Voucher) feature trong section Giá thành:
  - Custom fields `vn_is_import_lcv`, `vn_is_subject_to_import_duty`
  - JS `landed_cost_voucher.js` (155 dòng)
  - Hook `lcv_hooks.py` + `seed.py` (COA resolver)
  - LCV Allocation Settings (Single DocType) với 11 expense types
  - Helper button "Tạo phiếu VAT NK khấu trừ"
- Section "Phân tích & Quản trị" (4 ERPNext core reports) — không có custom code, không có bug
- Sidebar items đã dedup + restructure (commit `f0c5e42`, `4fc5302`)

### Phần đáng nghi — cần verify ở session mới
- `manufacturing-costing-wizard` page (đã neuter JE creation, nhưng aggregate + unit cost logic chưa test live)
- `period_closing.pcv_hooks.py` — hook trên ERPNext PCV native, chưa verify validate logic chạy đúng
- 4 BCTC custom reports (B01/B02/B03 + B09) — chưa test render
- 2 sổ TT99/2025 (S03a-DN, S03b-DN) — chưa test render đúng layout
- BCTC Mapping DocType + mapping seed — chưa test

### Phần có thể bỏ
- `manufacturing-costing-wizard` page nếu KTT của DN nhỏ-vừa không dùng (DN nhỏ ERPNext Stock Entry + Work Order là đủ). Cân nhắc bỏ luôn, để dành nâng cấp sau.
- `Work In Progress Valuation` DocType — nếu không có workflow rõ ràng để dùng, bỏ.

---

## 6. State của môi trường

- bench `frappe-bench-dcnet` đang chạy port 8001
- Site `dcnet.localhost` (default site)
- Company test: `DCNET` (Vietnam, abbr DC)
- VN COA đầy đủ trong DCNET: 1331, 33312, 3333, 3332, 331, 152, 155, 156, 3388
- User test login bằng Administrator hoặc user thuộc Accounts Manager role

---

## 7. Câu lệnh cho session mới (template prompt)

```
Đọc file handoff: apps/vn_accounting/docs/reviews/2026-05-11-session-handoff-rebuild-4-sections.md
+ 2 reviews liên quan trong cùng folder.

Em muốn rebuild 4 sidebar sections: Giá thành / Tổng hợp / Báo cáo tài chính
/ Phân tích & Quản trị từ đầu — đúng nghiệp vụ KTT của DN VN nhỏ-vừa dùng
ERPNext, tránh các lỗi đã phát hiện trong session trước.

Bắt đầu bằng /superpowers:brainstorming. Cho từng section, brainstorm với
em scope thực sự cần thiết theo phương pháp đã ghi ở §5 của handoff. Sau
brainstorm 4 section, viết spec mới ngắn (<= 300 dòng) rồi mới code.

Branch hiện tại: feat/giathanh-tonghop-bctc, 18 commits ahead of 78af380.
Không revert; đi tiếp trên cùng branch, sửa từng cái khi cần.
```
