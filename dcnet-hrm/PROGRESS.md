# dcnet_hrm — Progress Tracker

> Nguồn yêu cầu: `../prompt-dcnet-hrm.md` (repo root `flow_next/`).
> Cập nhật lần cuối: xem git log của file này.

## Trạng thái tổng quan

| Phase | Trạng thái | Ghi chú |
|-------|-----------|---------|
| Phase 1 — Payroll VN (core) | ✅ Hoàn thành | 22 test pass |
| Phase 2 — Pháp lý | 🟡 Gần xong | Thiếu 3 file mẫu Excel gốc + số liệu vùng lương 2026 |
| Phase 3 — Chấm công & OT | ⬜ Chưa làm | ZKTeco, Overtime Request, overtime engine |

**Toàn app hiện tại: 36/36 unit test pass** (`bench --site flow.local run-tests --app dcnet_hrm`).
App đã cài + migrate thành công trên site `flow.local` (devcontainer).

---

## Đã làm — Phase 1

- `constants.py` — bậc thuế TNCN (7 bậc), hệ số OT, giờ đêm, thuế thử việc 10%, ngưỡng 14 ngày công. Tất cả có `effective_from` (versioned).
- Custom Field: `Employee` (si_number, personal_tax_code, citizen_id*, insurance_status, minimum_wage_region, union_member), `Salary Structure Assignment` (insurance_salary, net_agreement), `Salary Slip` (capped_insurance_salary, taxable_income, assessable_income, dependent_count, pit_breakdown).
- DocType: `VN Payroll Settings` (Single), `Insurance Rate` (+ `Insurance Rate Detail`), `Statutory Wage`, `Dependent`.
- Engine `payroll/vn_payroll.py` (+ `social_insurance.py`, `pit.py`) — hook `Salary Slip.validate`. Chạy đủ 9 bước: BH có trần (theo lương cơ sở / lương tối thiểu vùng), thuế TNCN lũy tiến, giảm trừ NPT theo kỳ, khấu trừ 10% thử việc, đoàn phí/kinh phí công đoàn, giải NET→GROSS bằng vòng lặp hội tụ (`solve_net_to_gross`, tối đa 20 vòng, sai số < 1 đồng).
- `translations/vi.csv` — i18n chuẩn Frappe: label/message viết English, dịch VN qua CSV. Đổi Language của User/System Settings tự đổi UI, không cần switcher riêng. Đã verify bằng `frappe.translate.get_all_translations("vi")`.
- Test: `tests/test_vn_payroll.py` — 22 case (dưới/trên trần BH, trần theo vùng BHTN, có/không/NPT giữa kỳ, NET→GROSS, thử việc 10%, <14 ngày công, "thai sản" (payment_days=0), phụ cấp cơm/điện thoại, đoàn phí có/không trần).

## Đã làm — Phase 2

- **Labor Contract** (submittable): vòng đời Draft→Active→Expired/Terminated. `before_submit` chặn (a) 2 HĐ Active chồng thời gian, (b) ký Xác định thời hạn (Fixed-term) lần 3 liên tiếp trừ khi điền `override_reason`. `on_submit` set status Active (**qua `db_set`**, xem lưu ý bug bên dưới) + nếu có `previous_contract`: set HĐ cũ → Terminated, và nếu `insurance_salary` đổi thì tự tạo **Draft** Insurance Declaration (loại "Rate Adjustment") để HR xem lại — không tự submit.
- **Scheduler daily** (`run_daily_expiry_check`, hooked trong `hooks.py`): HĐ hết hạn trong 30 ngày → tạo Notification Log cho user có role HR Manager/HR User; HĐ quá `end_date` → tự chuyển Expired.
- **Insurance Declaration** (submittable): child table `employees` (employee, si_number, old/new_amount, effective_date, reason). Quyền `submit` giới hạn role HR Manager = tương đương "Draft → HR Manager duyệt → Submitted" (không dùng Frappe Workflow doctype riêng — dùng permission có sẵn, đơn giản hơn). Nút UI "Export D02-LT" (`insurance_declaration.js`) gọi `export/d02lt.py`.
- **PIT Annual Settlement** (không submittable — chỉ là bảng tổng hợp làm việc): field `fiscal_year` + `company` (field `company` là bổ sung kỹ thuật cần thiết, không có trong spec gốc — vì aggregation cần biết phạm vi công ty). Nút "Aggregate from Salary Slips" gộp theo NĂM từ các Salary Slip đã submit; thuế phải nộp cả năm tính lại theo **biểu thuế năm = biểu tháng × 12** (`pit.calculate_annual`, Thông tư 111/2013 Điều 7.2). Nút "Export 05/QTT-TNCN" gọi `export/qtt_tncn.py`.
- **Report `05-KK-TNCN`** (Script Report, `dcnet_hrm/dcnet_hrm/report/05_kk_tncn/`): tổng hợp thuế TNCN đã khấu trừ theo kỳ + company, filter from_date/to_date. Nút "Export 05/KK-TNCN" gọi `export/kk_tncn.py`.
- Test: `tests/test_labor_contract.py`, `tests/test_insurance_declaration.py`, `tests/test_pit_annual_settlement.py`.

### 🐛 Bug đã bắt được nhờ chạy test thật (đáng nhớ)

`on_submit()` chạy **SAU** khi Frappe đã `db_update()` — gán `self.status = "Active"` trực tiếp trong `on_submit` **không được lưu xuống DB** (chỉ đổi in-memory). Đây là cùng loại lỗi mà CLAUDE.md cảnh báo cho `on_update`, nhưng hoá ra áp dụng cho `on_submit` luôn. Đã sửa bằng `self.db_set("status", "Active", notify=False)`. Nếu viết thêm doctype submittable mới, nhớ áp dụng đúng pattern này, KHÔNG gán field trực tiếp trong `on_submit`.

Một bug nhỏ khác: filter `{"name": ["not in", []]}` (list rỗng) trong `frappe.get_all` không hoạt động như mong đợi (không match được gì thay vì match tất cả) — phải bỏ hẳn key `"name"` khỏi filter khi list rỗng, không truyền `not in []`.

---

## ⚠️ Việc còn thiếu — CẦN từ khách/anh Khoa, KHÔNG tự bịa

1. **3 file mẫu Excel gốc** (chưa có, không thể tự vẽ layout theo nguyên tắc spec mục 6):
   - `export/templates/D02-LT.xlsx` (BHXH Việt Nam)
   - `export/templates/05-KK-TNCN.xlsx` (định dạng HTKK)
   - `export/templates/05-QTT-TNCN.xlsx` (định dạng HTKK)
   - Hiện tại 3 hàm `export_d02lt/export_kk_tncn/export_qtt_tncn` throw thông báo rõ ràng yêu cầu file mẫu + chưa xác nhận toạ độ cell (`CELL_MAP` trong `d02lt.py` là placeholder, cần đối chiếu file mẫu thật rồi mới bỏ comment `_write_rows()`).
2. **Quyết định kiến trúc**: repo có sẵn app `dcnet_htkk` (`HTKK Declaration`, `HTKK Template Manager`) — có thể đã có cơ chế xuất tờ khai chung cho toàn hệ thống (demo: `HTKK-01/GTGT-Quý1-2026`). Cần quyết định: `dcnet_hrm` tự làm export riêng (như hiện tại, đúng theo prompt gốc) hay tích hợp vào engine `dcnet_htkk`? Nếu tích hợp thì tránh trùng lặp hạ tầng khai thuế.
3. **Số liệu lương tối thiểu vùng I–IV** hiệu lực 01/07/2026 (mức lương cơ sở 2.530.000đ user đã cung cấp, nhưng 4 số vùng thì chưa) — cần để thêm bản ghi `Statutory Wage` mới (`effective_from=2026-07-01`), KHÔNG sửa bản ghi 2024-07-01 cũ.
4. Repo `dcnet-hrm/` **chưa là git repo riêng** (khác các app khác như `dcnet-contract` có `.git` riêng) — hỏi trước khi `git init` + commit đầu tiên.

## ⚠️ Giả định đã đưa ra (đã flag trong code, cần khách xác nhận khi rảnh)

- **NET→GROSS**: `Salary Structure Assignment.base` được hiểu là mức NET thoả thuận khi `net_agreement=1`; chỉ earning "Lương cơ bản" được giải ngược, phụ cấp khác giữ nguyên.
- **OT miễn thuế** (phần vượt hệ số 100%): Phase 1 CHƯA tách được — thiếu breakdown giờ OT theo hệ số (thuộc Overtime Request, Phase 3). Hiện tại toàn bộ "Tăng ca" tính chịu thuế (có test pin lại hành vi này: `test_overtime_fully_taxable_phase1_gap`).
- **Nhận diện thử việc/HĐ ngắn hạn** (để áp thuế 10% flat): dùng `Employee.employment_type == "Probation"` HOẶC `contract_end_date - date_of_joining < 3 tháng`. Sẽ chuyển hẳn sang `Labor Contract.contract_type` khi dữ liệu HĐ đầy đủ hơn.
- **Trần đoàn phí công đoàn**: field `union_fee_monthly_cap` để trống/0 = không áp trần — chưa có số cụ thể theo quy định.
- **Lương cơ sở/tối thiểu vùng 2024-07-01**: theo Nghị định 73–74/2024/NĐ-CP — cần xác nhận đã có Nghị định mới hơn (ngoài mức 01/07/2026 đang chờ số liệu ở trên) hay chưa.

---

## Việc tiếp theo khi resume

1. Nhận số liệu vùng I–IV → thêm `Statutory Wage` mới 2026-07-01 (`dcnet_hrm/install.py` có sẵn `seed_statutory_wage()` làm mẫu, viết thêm 1 patch/script tương tự, KHÔNG chỉnh hàm seed cũ).
2. Quyết định hướng export (tự làm vs tích hợp `dcnet_htkk`) rồi hoàn thiện `CELL_MAP`/mapping thật khi có file mẫu.
3. Phase 3: `integrations/zkteco/` (pull log máy chấm công), `Overtime Request` doctype + `payroll/overtime.py`, rồi nối lại vào `vn_payroll.py` để xử lý đúng phần OT miễn thuế (gap đã note ở trên).
4. Xem lại toàn bộ giả định ở mục trên với khách, cập nhật `CUSTOM_REQUIREMENTS.md`/`CLARIFY.md` nếu module này sau được đưa vào cấu trúc `docs/modules/{STT}-{slug}/` chuẩn của dự án.

## Lệnh hữu ích

```bash
# Cài lại / migrate (site flow.local, devcontainer-frappe-1)
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"

# Chạy test
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local run-tests --app dcnet_hrm"

# Kiểm tra bản dịch vi.csv đã load
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local execute frappe.translate.get_all_translations --args \"['vi']\""
```
