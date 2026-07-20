# Module Progress Tracker

> **Cập nhật:** 17/02/2026
> **Tổng:** 44 modules chức năng (T3-T8) + 4 operational (T7)
> **Cách dùng:** Claude đọc file này trước khi bắt đầu module mới. Update sau mỗi thay đổi.

---

## Hướng dẫn đọc

| Icon | Ý nghĩa |
|------|---------|
| :white_check_mark: | Xong |
| :construction: | Đang làm |
| :x: | Chưa làm |
| — | Không cần (module đơn giản / không áp dụng) |

**Docs Columns:**
- **R** = README.md
- **SM** = SPEC_MAPPING.md (file chính)
- **CL** = CLARIFY.md
- **CR** = CUSTOM_REQUIREMENTS.md
- **MK** = mockup/
- **UG** = user-guide/

**Code Status:** `none` (chưa code) | `config` (chỉ config ERPNext) | `partial` (đang code) | `done` (xong) | `n/a` (không cần code)

---

## T3: Bàn giao 31/03/2026

| STT | Module | R | SM | CL | CR | MK | UG | Code | Ghi chú |
|-----|--------|:-:|:--:|:--:|:--:|:--:|:--:|:----:|---------|
| 01 | Đăng nhập/Nền tảng | :white_check_mark: | — | — | — | — | — | n/a | Frappe built-in, chỉ config |
| 02 | Dashboard | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | done | PR [#6](https://github.com/dcnet-cloud/flow_next/pull/6) |
| 03 | Sản phẩm | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | :x: | none | Docs done, chưa code |
| 04 | Nhà cung cấp | :white_check_mark: | :white_check_mark: | :white_check_mark: | — | — | :x: | none | Đơn giản, 100% CFG |
| 05 | Mua hàng | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | :x: | none | Trung bình-khó, 11 EXT/NEW |
| 06 | Báo cáo Phân tích | :white_check_mark: | :white_check_mark: | :white_check_mark: | :white_check_mark: | — | :x: | none | FEAT 14.5 + ERP 6.3, 7 features, ~13 ngày |

**T3 Progress: 6/6 modules done (01 config, 02 full, 03-06 docs done)** :white_check_mark:

---

## T4: Bàn giao 30/04/2026

| STT | Module | R | SM | CL | CR | MK | UG | Code | Ghi chú |
|-----|--------|:-:|:--:|:--:|:--:|:--:|:--:|:----:|---------|
| 07 | Kho hàng | :white_check_mark: | :x: | :white_check_mark: | :x: | :x: | :x: | none | Có analysis + tech-spec (format cũ) |
| 08 | Báo cáo Kho | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 09 | Đơn hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | Có analysis + tech-spec (format cũ) |
| 10 | Bán buôn | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 11 | Bán lẻ | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 12 | Bán hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | Có analysis + tech-spec (format cũ) |
| 13 | Danh mục Bán hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 14 | Trade-in | :x: | :x: | :x: | :x: | :x: | :x: | none | Có analysis + tech-spec (format cũ) |
| 15 | Chi nhánh | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 16 | Nhân viên | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 17 | Khách hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 18 | BC Đơn hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 19 | BC Quản trị | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 20 | BC Nhân viên | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 21 | BC Khách hàng | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 22 | BC Doanh số | :x: | :x: | :x: | :x: | :x: | :x: | none | |

**T4 Progress: 0/16 modules done (4 có docs format cũ, cần update)**

---

## T5: Bàn giao 30/05/2026

| STT | Module | R | SM | CL | CR | MK | UG | Code | Ghi chú |
|-----|--------|:-:|:--:|:--:|:--:|:--:|:--:|:----:|---------|
| 23 | KT Tiền | :x: | :x: | :x: | :x: | — | :x: | none | |
| 24 | KT Mua hàng | :x: | :x: | :x: | :x: | — | :x: | none | |
| 25 | KT Bán hàng | :x: | :x: | :x: | :x: | — | :x: | none | |
| 26 | KT Công nợ | :x: | :x: | :x: | :x: | — | :x: | none | |
| 27 | KT Hàng tồn | :x: | :x: | :x: | :x: | — | :x: | none | |
| 28 | Chi phí & Hỗ trợ | :x: | :x: | :x: | :x: | — | :x: | none | |
| 29 | Tài sản & CCDC | :x: | :x: | :x: | :x: | — | :x: | none | |
| 30 | KT Thuế | :x: | :x: | :x: | :x: | — | :x: | none | |
| 31 | KT Tổng hợp | :x: | :x: | :x: | :x: | — | :x: | none | |
| 32 | BC Tổng hợp | :x: | :x: | :x: | :x: | — | :x: | none | |

**T5 Progress: 0/10 modules done (kế toán — module phức tạp nhất)**

---

## T6: Bàn giao 30/06/2026

| STT | Module | Cty | R | SM | CL | CR | MK | UG | Code | Ghi chú |
|-----|--------|-----|:-:|:--:|:--:|:--:|:--:|:--:|:----:|---------|
| 33 | Lead | TM+NM | :x: | :x: | :x: | :x: | :x: | :construction: | partial | Có code lead_validation + user-guide (format cũ) |
| 34 | Fitting | TM+NM | :x: | :x: | :x: | :x: | :x: | :x: | partial | Có code DocType + analysis (format cũ) |
| 35 | Coaching | TM | :x: | :x: | :x: | :x: | :white_check_mark: | :x: | none | Có mockup HTML |
| 36 | Cài đặt | TM+NM | :x: | :x: | :x: | :x: | — | :x: | none | |
| 37 | CSKH | TM+NM | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 38 | Tích điểm | NM | :x: | :x: | :x: | :x: | :x: | :x: | none | Có analysis (format cũ) |
| 39 | ĐH nâng cao | TM+NM | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 40 | Giao vận | TM+NM | :x: | :x: | :x: | :x: | :x: | :x: | none | Có analysis (format cũ) |
| 41 | Role & Perm | TM+NM | :x: | :x: | :x: | :x: | — | :x: | none | |
| 42 | Report Website | NM | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 43 | Web & Đồng bộ | NM | :x: | :x: | :x: | :x: | :x: | :x: | none | |
| 44 | Kiểm soát | TM+NM | :x: | :x: | :x: | :x: | — | :x: | none | |

**T6 Progress: 0/12 modules done (2 có code partial, 6 có docs format cũ)**

---

## T8: Bổ sung

| STT | Module | Cty | R | SM | CL | CR | MK | UG | Code | Ghi chú |
|-----|--------|-----|:-:|:--:|:--:|:--:|:--:|:--:|:----:|---------|
| 49 | Membership | TM | :x: | :x: | :x: | :x: | :x: | :x: | none | Chưa có spec chi tiết |
| 50 | Dự báo DT | TM | :x: | :x: | :x: | :x: | :x: | :x: | none | Chưa có spec chi tiết |
| 51 | Workshop | TM | :x: | :x: | :x: | :x: | :x: | :x: | none | Chưa có spec chi tiết |

**T8 Progress: 0/3 modules done (chưa có spec)**

---

## Tổng kết

| Milestone | Tổng | Done | Partial/Old | Chưa làm |
|-----------|:----:|:----:|:-----------:|:--------:|
| **T3** | 6 | 6 | 0 | 0 |
| **T4** | 16 | 0 | 4 (format cũ) | 12 |
| **T5** | 10 | 0 | 0 | 10 |
| **T6** | 12 | 0 | 6 (format cũ) | 6 |
| **T8** | 3 | 0 | 0 | 3 |
| **Tổng** | **47** | **6** | **10** | **31** |

### Docs format cũ cần update (dùng `/dcnet-module {STT} --update`)

| STT | Module | Có gì |
|-----|--------|-------|
| 07 | Kho hàng | README + CLARIFY + analysis/ + technical-spec/ |
| 09 | Đơn hàng | analysis/ + technical-spec/ |
| 12 | Bán hàng | analysis/ + technical-spec/ |
| 14 | Trade-in | analysis/ + technical-spec/ |
| 33 | Lead | analysis/ + technical-spec/ + implementation/ + user-guide/ |
| 34 | Fitting | analysis/ + technical-spec/ + implementation/ |
| 35 | Coaching | analysis/ + technical-spec/ + mockup/ |
| 38 | Tích điểm | analysis/ + technical-spec/ |
| 40 | Giao vận | analysis/ + technical-spec/ |

### Legacy folders (chưa migrate)

| Folder | Map tới STT | Ghi chú |
|--------|-------------|---------|
| credit-management | 26 (KT Công nợ) | Cần verify trước khi move |
| ~~import-management~~ | ~~05 (Mua hàng)~~ | Đã migrate sang 05-mua-hang/, folder đã xóa |
| nhatminh-connect | 43 (Web & Đồng bộ) | NM only |

---

## Ưu tiên tiếp theo

1. ~~**T3 (deadline 31/03):** Module 06 (BC Phân tích)~~ **DONE** — T3 docs hoàn thành 6/6
2. **T4 (deadline 30/04):** 07-22 (16 modules — bắt đầu với 07, 09, 12, 14)
3. **Format cũ:** Update 9 modules có docs cũ sang Spec-First format

---

**Lưu ý cho Claude:** Khi bắt đầu module mới, đọc file này để:
- Biết module nào đã xong, đang làm, chưa làm
- Biết module nào có docs format cũ cần update
- Cập nhật file này sau khi hoàn thành mỗi module
