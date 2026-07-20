# DCNET Flow - Timeline 2026

> **Cập nhật:** 10/02/2026
> **2 công ty:** Thăng Long TM + Nhật Minh Sport (2 site riêng, code chung)
> **Team:** 5 người (Đức, Phương, Cường, Đạt, Hậu)
> **Strategy:** Tận dụng ERPNext tối đa, custom app cho modules đặc thù
> **Source:** Excel "Timeline dự án - TM & Nhật Minh Sports.xlsx"

---

## 1. Tổng quan

```
T3         T4          T5          T6          T7         T8
├──────────┼───────────┼───────────┼───────────┼──────────┼──────►
│ Nền tảng │ Kho+ĐH    │ Kế toán   │ CRM+DV    │ BRAVO    │ Bổ sung
│ SP, NCC  │ Bán hàng  │ 9 modules │ Lead,Fit  │ Migrate  │ Membership
│ Mua hàng │ Trade-in  │ BC Tổng   │ Coaching  │ Server   │ Dự báo
│ BC       │ KH,NV,CN  │ hợp       │ Giao vận  │ Đào tạo  │ Workshop
│          │ 5x BC     │           │ Role      │          │
31/03      30/04       30/05       30/06
```

---

## 2. T3: Bàn giao 31/03/2026

| STT | Module | TM | NM | Spec Ref | Ghi chú |
|-----|--------|:--:|:--:|----------|---------|
| 1 | Đăng nhập/Đăng xuất + Nền tảng | V | V | FEAT 1 | |
| 2 | Dashboard | V | V | FEAT 2 | |
| 3 | Quản lý Sản phẩm | V | V | FEAT 6 | Cần data BRAVO |
| 4 | Danh mục Nhà cung cấp | V | V | ERP 3 | Cần data BRAVO |
| 5 | Mua hàng | V | V | ERP 3 | |
| 6 | Báo cáo Phân tích | V | V | FEAT 14 | |

---

## 3. T4: Bàn giao 30/04/2026

| STT | Module | TM | NM | Spec Ref | Ghi chú |
|-----|--------|:--:|:--:|----------|---------|
| 7 | Quản lý Kho hàng | V | V | FEAT 8 + ERP 4 | Cần data BRAVO |
| 8 | Báo cáo Kho | V | V | ERP 4 | |
| 9 | Quản lý Đơn hàng | V | V | FEAT 5 | Cần data BRAVO |
| 10 | Bán buôn | V | V | ERP 2 | Cần data BRAVO |
| 11 | Bán lẻ | V | V | ERP 2 | Cần data BRAVO |
| 12 | Quản lý Bán hàng | V | V | FEAT 7 + ERP 2 | KH bán hàng, chiết khấu, trả lại, thưởng DS, voucher, bảng giá |
| 13 | Danh mục Bán hàng | V | V | ERP 2 | Cần data BRAVO |
| 14 | Đơn hàng Thu cũ Đổi mới | V | V | FEAT 18 | Bao gồm Trade-in tích hợp |
| 15 | Quản lý Chi nhánh | V | V | FEAT 10 | Cần data BRAVO |
| 16 | Quản lý Nhân viên | V | V | FEAT 11 | Cần data BRAVO |
| 17 | Quản lý Khách hàng | V | V | FEAT 4 | Cần data BRAVO |
| 18 | Báo cáo Đơn hàng | V | V | FEAT 14 | |
| 19 | Báo cáo Quản trị | V | V | FEAT 14 | |
| 20 | Báo cáo Nhân viên | V | V | FEAT 14 | |
| 21 | Báo cáo Khách hàng | V | V | FEAT 14 | |
| 22 | Báo cáo Doanh số | V | V | FEAT 14 | |

---

## 4. T5: Bàn giao 30/05/2026

| STT | Module | TM | NM | Spec Ref | Ghi chú |
|-----|--------|:--:|:--:|----------|---------|
| 22 | Kế toán Tiền | V | V | ERP 5 | Cần data BRAVO |
| 23 | Kế toán Mua hàng | V | V | ERP 5 | Cần data BRAVO |
| 24 | Kế toán Bán hàng | V | V | ERP 5 | Cần data BRAVO |
| 25 | Kế toán Công nợ | V | V | ERP 5 | Cần data BRAVO |
| 26 | Kế toán Hàng tồn | V | V | ERP 5 | Cần data BRAVO |
| 27 | Chi phí & Hỗ trợ | V | V | ERP 5 | Cần data BRAVO |
| 28 | Tài sản & CCDC | V | V | ERP 5 | Cần data BRAVO |
| 29 | Kế toán Thuế | V | V | ERP 5 | Cần data BRAVO |
| 30 | Kế toán Tổng hợp | V | V | ERP 5 | Cần data BRAVO |
| 31 | Báo cáo Tổng hợp | V | V | ERP 6 | |

---

## 5. T6: Bàn giao 30/06/2026

| STT | Module | TM | NM | Spec Ref | Ghi chú |
|-----|--------|:--:|:--:|----------|---------|
| 32 | Quản lý Lead | V | V | FEAT 3 | |
| 33 | Quản lý Fitting | V | V | FEAT 16 | Bao gồm Fitting tích hợp |
| 34 | Quản lý Coaching | V | X | FEAT 17 | Bao gồm Coaching tích hợp |
| 35 | Cài đặt hệ thống | V | V | FEAT 13 | |
| 36 | Chăm sóc KH tự động | V | V | FEAT 4 | |
| 37 | Quản lý tích điểm | X | V | FEAT 7 | Quy tắc tính điểm/lên hạng |
| 38 | Đơn hàng nâng cao | V | V | FEAT 5 | Bảo hành, bảo trì |
| 39 | Tích hợp Giao vận | V | V | FEAT 9 | Viettel Post, GHTK |
| 40 | Role & Permission | V | V | FEAT 12 | |
| 41 | Report Website | X | V | FEAT 15 | |
| 42 | Web & Đồng bộ | X | V | ERP 7 | |
| 43 | Kiểm soát | V | V | — | |

---

## 6. T7: Migration + Server + Đào tạo

| STT | Module | TM | NM | Ghi chú |
|-----|--------|:--:|:--:|---------|
| 44 | Migrate dữ liệu BRAVO | V | V | Lấy trong khoảng time muốn kiểm tra |
| 45 | Cài đặt Server Khách | V | V | |
| 46 | Bàn giao, chuyển server | V | V | Có thể lùi T8 nếu đẩy #49-51 vào đầu T7 |
| 47 | Đào tạo, hướng dẫn | V | V | |

---

## 7. T8: Modules bổ sung

> Phát sinh sau họp C.Linh 3/2/2026. Chưa có spec chi tiết.

| STT | Module | TM | NM | Spec Ref | Ghi chú |
|-----|--------|:--:|:--:|----------|---------|
| 49 | Membership | V | X | — | Quản lý gói/thẻ, QR check-in, nâng/hạ hạng |
| 50 | Dự báo doanh thu | V | X | — | Cảnh báo hụt doanh số |
| 51 | Workshop/Event | V | X | — | Đơn hàng dịch vụ, tag workshop/event |

---

## 8. Phân tách TM vs NM

**TM only (NM không có):**

| Module | Tháng | Ghi chú |
|--------|-------|---------|
| Coaching (#34) | T6 | Quản lý HLV, gói học, sân tập, lịch học, điểm danh |
| Membership (#49) | T8 | Quản lý gói/thẻ, QR check-in, nâng/hạ hạng |
| Dự báo doanh thu (#50) | T8 | Cảnh báo hụt doanh số |
| Workshop/Event (#51) | T8 | Đơn hàng dịch vụ, tag workshop/event |

**NM only (TM không có):**

| Module | Tháng | Ghi chú |
|--------|-------|---------|
| Quản lý tích điểm (#37) | T6 | Quy tắc tính điểm, lên hạng |
| Report Website (#41) | T6 | Heatmap, phân tích web |
| Web & Đồng bộ (#42) | T6 | API đồng bộ KH, SP, Đơn hàng, Tồn kho |

---

## 9. Custom Modules cần build

Modules không có sẵn trong ERPNext, cần develop từ đầu hoặc mở rộng nhiều.

| Module | Tháng | Mô tả | ERPNext base |
|--------|-------|-------|:------------:|
| Mua hàng nâng cao | T3 | PO workflow, NCC management | 70% |
| Quản lý Bán hàng | T4 | Chiết khấu, thưởng DS, voucher, bảng giá | 65% |
| Thu cũ Đổi mới | T4 | Định giá, checklist, tích hợp kho | 0% |
| Barcode/Tem | T4 | In tem tự in + tem NCC | 0% |
| Ký gửi (Consignment) | T4 | Quy trình 5 bước TLTM ↔ NM | 0% |
| Kế toán VN | T5 | TT200/TT133, báo cáo thuế VN | 50% |
| Fitting | T6 | 14 thông số kỹ thuật, tạo SO | 0% |
| Coaching | T6 | HLV, gói học, điểm danh (TM only) | 0% |
| CSKH tự động | T6 | Lịch chăm sóc, khảo sát, ticket | 30% |
| Giao vận | T6 | Viettel Post, GHTK integration | 0% |
| Tích điểm | T6 | Quy tắc điểm, lên hạng (NM only) | 40% |
| Report Website | T6 | Heatmap, phân tích (NM only) | 0% |
| Web & Đồng bộ | T6 | API sync KH, SP, ĐH, Tồn kho (NM only) | 0% |
| Membership | T8 | Gói/thẻ, QR check-in (TM only) | 0% |
| Dự báo DT | T8 | Cảnh báo hụt doanh số (TM only) | 0% |
| Workshop/Event | T8 | ĐH dịch vụ, tag event (TM only) | 0% |

---

## 10. Risks & Dependencies

| Rủi ro | Mức độ | Giảm thiểu |
|--------|--------|------------|
| BRAVO data không clean | Cao | Yêu cầu access sớm (trước 01/05) để review cấu trúc |
| Chậm cung cấp BRAVO access | Cao | Escalate sớm, set hard deadline |
| Scope creep (khách thêm yêu cầu) | Trung bình | Mọi thay đổi cần approval, trở về spec gốc |
| Kế toán không khớp BRAVO | Cao | Dành riêng T7 để validate |
| Server chậm | Trung bình | Yêu cầu ready trước 01/07 |
| T8 modules chưa có spec chi tiết | Trung bình | Clarify với khách trước khi bắt đầu T6 |

**Dependencies từ khách hàng:**

| Deadline | Yêu cầu | Mức độ |
|----------|---------|--------|
| Trước 01/04 | Confirm user list, chi nhánh, kho | Trung bình |
| Trước 01/05 | Access BRAVO hoặc export Excel | **CRITICAL** |
| Trước 01/06 | Full data export từ BRAVO (master + opening) | **CRITICAL** |
| Trước 01/07 | Server production ready | **CRITICAL** |

---

## 11. Changelog

| Ngày | Thay đổi |
|------|----------|
| 30/01/2026 | V1 — Tạo timeline (Phase 1-6, monthly) |
| 10/02/2026 | V2 — Rewrite theo Excel khách hàng (T3-T8, 2 công ty TM+NM) |
