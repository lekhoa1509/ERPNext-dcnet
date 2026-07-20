# PROMPT: Xây dựng app `dcnet_hrm` — HRM Việt Nam trên nền Frappe HR

Bạn là senior Frappe/ERPNext developer. Nhiệm vụ: xây dựng custom app **`dcnet_hrm`** thay thế/bổ sung Frappe HR để đáp ứng đầy đủ nghiệp vụ nhân sự – tiền lương theo pháp luật Việt Nam. App này theo pattern giống `dcnet_apps` / `dcnet-crm`: một app độc lập, cài đè lên bench có sẵn `frappe`, `erpnext`, `hrms`.

---

## 1. BỐI CẢNH & NGUYÊN TẮC KIẾN TRÚC

- **Môi trường**: đọc project và lấy môi trường giống như dcnet-crm
- **KHÔNG viết lại** các doctype đã có của Frappe HR (Employee, Attendance, Leave, Salary Slip, Payroll Entry...). Chỉ:
  1. **Extend** bằng Custom Field + `doc_events` hooks.
  2. **Tạo doctype mới** cho nghiệp vụ VN không có tương đương.
  3. **Ghi đè logic tính lương** bằng Python module hook vào `Salary Slip.validate` — KHÔNG dùng formula string của Salary Component cho BHXH/TNCN.
- **KHÔNG dùng** `override_doctype_class` cho Salary Slip trừ khi bất khả kháng (hrms hay breaking change).
- Mọi Custom Field, Property Setter, Salary Component mẫu, Holiday List mẫu phải nằm trong **fixtures** của app để deploy site mới không mất:
  ```python
  fixtures = [
      {"dt": "Custom Field", "filters": [["module", "=", "DCNET HRM"]]},
      {"dt": "Property Setter", "filters": [["module", "=", "DCNET HRM"]]},
  ]
  ```
- Code style: docstring tiếng Việt cho nghiệp vụ, tên biến tiếng Anh. Mọi hằng số pháp lý (tỷ lệ BH, bậc thuế, mức giảm trừ) đặt trong doctype cấu hình hoặc file `constants.py` có version theo hiệu lực thời gian — **không hardcode rải rác**.
- Số tiền: dùng VND, không thập phân. Làm tròn theo quy tắc: BH làm tròn đến đồng, thuế TNCN làm tròn đến đồng.

---

## 2. CẤU TRÚC APP

```
dcnet_hrm/
├── dcnet_hrm/
│   ├── hooks.py
│   ├── constants.py                 # hằng số pháp lý có hiệu lực thời gian
│   ├── payroll/
│   │   ├── vn_payroll.py            # engine tính lương VN (core)
│   │   ├── social_insurance.py      # tính BHXH/BHYT/BHTN
│   │   ├── pit.py                   # thuế TNCN lũy tiến, NET→GROSS
│   │   └── overtime.py              # tăng ca 150/200/300% + đêm
│   ├── doctype/                     # doctype mới (liệt kê mục 4)
│   ├── report/                      # báo cáo (mục 6)
│   ├── export/                      # xuất Excel template nhà nước (openpyxl)
│   │   └── templates/               # file .xlsx gốc: D02-LT, 05-KK-TNCN...
│   ├── integrations/
│   │   └── zkteco/                  # connector máy chấm công
│   └── fixtures/
├── pyproject.toml
└── README.md
```

---

## 3. CUSTOM FIELD TRÊN DOCTYPE CÓ SẴN

### 3.1 Employee
| Fieldname | Label | Type | Ghi chú |
|---|---|---|---|
| `si_number` | Mã số BHXH | Data | unique |
| `personal_tax_code` | MST cá nhân | Data | |
| `citizen_id` | Số CCCD | Data | |
| `citizen_id_issue_date` | Ngày cấp CCCD | Date | |
| `citizen_id_issue_place` | Nơi cấp | Data | |
| `insurance_status` | Tình trạng đóng BH | Select: Đóng đầy đủ / Chỉ BHYT / Không đóng | default: Đóng đầy đủ |
| `minimum_wage_region` | Vùng lương tối thiểu | Select: I / II / III / IV | |
| `union_member` | Đoàn viên công đoàn | Check | ảnh hưởng đoàn phí 1% |

### 3.2 Salary Structure Assignment
| Fieldname | Label | Type | Ghi chú |
|---|---|---|---|
| `insurance_salary` | Lương đóng BH | Currency | mức đóng BH thỏa thuận, KHÁC lương thực nhận |
| `net_agreement` | Thỏa thuận lương NET | Check | nếu tick → engine giải NET→GROSS |

### 3.3 Salary Slip (readonly, để đối chiếu — engine set giá trị)
| Fieldname | Label | Type |
|---|---|---|
| `capped_insurance_salary` | Lương đóng BH (đã áp trần) | Currency |
| `taxable_income` | Thu nhập chịu thuế | Currency |
| `assessable_income` | Thu nhập tính thuế | Currency |
| `dependent_count` | Số NPT trong kỳ | Int |
| `pit_breakdown` | Chi tiết bậc thuế | Small Text (JSON) |

---

## 4. DOCTYPE MỚI

### 4.1 `VN Payroll Settings` (Single)
Cấu hình toàn cục: link đến bảng tỷ lệ BH hiện hành, mức giảm trừ bản thân (11.000.000), mức giảm trừ NPT (4.400.000), trần miễn thuế tiền cơm (730.000), % kinh phí công đoàn (2%), % đoàn phí (1%, cap theo quy định).

### 4.2 `Insurance Rate` 
Bảng tỷ lệ BH có hiệu lực thời gian. Fields: `effective_from` (Date), child table `rates` gồm: loại (BHXH/BHYT/BHTN/TNLĐ-BNN), % NLĐ, % DN. Seed dữ liệu hiện hành: BHXH 8/17.5, BHYT 1.5/3, BHTN 1/1, TNLĐ-BNN 0/0.5.

### 4.3 `Statutory Wage` 
Lương cơ sở & lương tối thiểu vùng theo hiệu lực thời gian. Fields: `effective_from`, `base_salary` (lương cơ sở), `region_1..region_4` (tối thiểu vùng). Engine tra bảng theo **ngày bắt đầu kỳ lương** để tính trần: trần BHXH/BHYT = 20 × lương cơ sở; trần BHTN = 20 × lương tối thiểu vùng của NV.

### 4.4 `Dependent` (Người phụ thuộc)
Fields: `employee` (Link), `full_name`, `relationship` (Select: Con / Vợ-Chồng / Cha-Mẹ / Khác), `dob`, `tax_code`, `citizen_id`, **`deduction_from` (Date - tháng bắt đầu giảm trừ)**, **`deduction_to` (Date - tháng kết thúc, để trống = đang áp dụng)**, `registration_status` (Đã đăng ký / Chờ MST). Engine đếm NPT theo kỳ lương: NPT được tính nếu kỳ lương nằm trong [deduction_from, deduction_to].

### 4.5 `Labor Contract` (Hợp đồng lao động) — submittable
Fields: `employee`, `contract_type` (Select: Thử việc / Xác định thời hạn / Không xác định thời hạn), `contract_number` (unique), `start_date`, `end_date` (bắt buộc trừ KXĐTH), `base_salary`, `insurance_salary`, `allowances` (child table: tên phụ cấp, số tiền, chịu thuế Check, đóng BH Check), `status` (Draft/Active/Expired/Terminated), `previous_contract` (Link tự trỏ).
Logic:
- Validate: NV chỉ có 1 HĐ Active tại một thời điểm; HĐ XĐTH tối đa ký 2 lần liên tiếp → lần 3 bắt buộc KXĐTH (warning, cho override có lý do).
- Scheduler daily: HĐ hết hạn trong 30 ngày → tạo Notification/Email cho HR; quá `end_date` → chuyển status Expired.
- Khi submit HĐ mới có `insurance_salary` khác HĐ cũ → gợi ý tạo `Insurance Declaration` điều chỉnh.

### 4.6 `Insurance Declaration` (Báo tăng / giảm / điều chỉnh BHXH) — submittable
Fields: `declaration_type` (Select: Tăng mới / Giảm hẳn / Nghỉ không lương / Nghỉ thai sản / Điều chỉnh mức đóng), `month` (kỳ báo cáo), child table `employees`: employee, mã số BHXH, mức đóng cũ, mức đóng mới, ngày hiệu lực, lý do.
- Button **"Xuất D02-LT"**: gọi `export/d02lt.py` fill vào template Excel gốc bằng openpyxl.
- Workflow: Draft → HR Manager duyệt → Submitted.

### 4.7 `Overtime Request` — submittable
Fields: `employee`, `date`, `from_time`, `to_time`, `ot_type` (auto-detect từ ngày: Ngày thường / Ngày nghỉ tuần / Lễ Tết — tra Holiday List), `is_night` (Check, 22h–6h), `hours`, `approver`.
Validate giới hạn: cảnh báo khi tổng OT vượt 40h/tháng hoặc 200h/năm (300h nếu company setting cho phép).

### 4.8 `PIT Annual Settlement` (Quyết toán thuế TNCN năm)
Fields: `fiscal_year`, child table tổng hợp theo NV: tổng thu nhập chịu thuế, tổng giảm trừ, thuế đã khấu trừ, thuế phải nộp cả năm, chênh lệch (hoàn/truy thu). Button tổng hợp từ Salary Slip đã submit trong năm + button xuất 05/QTT-TNCN.

---

## 5. PAYROLL ENGINE (`payroll/vn_payroll.py`) — PHẦN QUAN TRỌNG NHẤT

Hook:
```python
doc_events = {
    "Salary Slip": {"validate": "dcnet_hrm.payroll.vn_payroll.calculate"}
}
```

Tạo sẵn (fixtures) các Salary Component với formula rỗng, engine ghi đè `amount`:
- Earnings: `Lương cơ bản`, `Phụ cấp cơm`, `Phụ cấp điện thoại`, `Phụ cấp xăng xe`, `Tăng ca`, `Lương tháng 13`
- Deductions: `BHXH (NLĐ)`, `BHYT (NLĐ)`, `BHTN (NLĐ)`, `Đoàn phí công đoàn`, `Thuế TNCN`
- Employer contributions (không trừ vào lương, chỉ hạch toán): `BHXH (DN)`, `BHYT (DN)`, `BHTN (DN)`, `TNLĐ-BNN (DN)`, `Kinh phí công đoàn (DN)`

Thuật toán `calculate(doc, method)`:
1. Lấy `insurance_salary` từ Salary Structure Assignment (fallback: lương cơ bản).
2. Tra `Statutory Wage` + `Insurance Rate` hiệu lực theo `doc.start_date`. Áp trần: BHXH/BHYT cap 20×lương cơ sở; BHTN cap 20×tối thiểu vùng theo `minimum_wage_region` của NV.
3. Tính BH NLĐ + DN, set amount vào component. Pro-rate: nếu NV làm < 14 ngày công trong tháng → không đóng BHXH tháng đó (theo quy định), có setting bật/tắt.
4. Thu nhập chịu thuế = tổng earnings − các khoản miễn (cơm ≤ 730k, phần vượt chịu thuế; điện thoại theo quy chế = miễn nếu Check `non_taxable` trên allowance; **phần OT vượt hệ số 100% được miễn thuế** — chỉ phần lương chênh lệch do hệ số 150/200/300 miễn, phần tương ứng đơn giá giờ thường vẫn chịu thuế).
5. Thu nhập tính thuế = chịu thuế − BH bắt buộc NLĐ − 11.000.000 − 4.400.000 × NPT(kỳ này).
6. Thuế TNCN lũy tiến 7 bậc (5/10/15/20/25/30/35%), dùng công thức rút gọn, lưu breakdown JSON vào `pit_breakdown`.
7. Hợp đồng < 3 tháng hoặc thử việc có thu nhập ≥ 2.000.000/lần: khấu trừ **10% flat**, không giảm trừ (setting theo Labor Contract type).
8. Nếu `net_agreement`: giải ngược GROSS từ NET bằng vòng lặp hội tụ (iterate tối đa 20 vòng, sai số < 1 đồng) — có unit test riêng.
9. Đoàn phí 1% lương đóng BH nếu `union_member` (cap theo quy định); kinh phí công đoàn 2% quỹ lương đóng BH (DN).

**Unit tests bắt buộc** (`tests/test_vn_payroll.py`): ít nhất 12 case — lương dưới/trên trần, có/không NPT, NPT vào giữa năm, NET→GROSS, thử việc 10%, OT miễn thuế, < 14 ngày công, nghỉ thai sản (BHXH trả, không tính lương DN).

---

## 6. BÁO CÁO & XUẤT FILE

Script Report (Frappe):
1. **Bảng lương tổng hợp tháng** — full breakdown BH + thuế, group theo phòng ban, xuất Excel.
2. **Báo cáo BHXH tháng** — đối chiếu số phải nộp NLĐ + DN.
3. **Tờ khai 05/KK-TNCN** (quý/tháng) — xuất Excel đúng format HTKK.
4. **D02-LT** — từ Insurance Declaration.
5. **Báo cáo tình hình sử dụng lao động** (6 tháng/năm) cho Sở LĐTBXH.

Nguyên tắc xuất: dùng **openpyxl fill vào file template gốc** đặt trong `export/templates/`, không tự vẽ layout.

---

## 7. CHẤM CÔNG (Phase 3)

- `integrations/zkteco/`: pull log từ máy ZKTeco (thư viện `pyzk`, TCP 4370) theo scheduler 15 phút → tạo `Employee Checkin` → dùng auto-attendance có sẵn của Frappe HR.
- Doctype `Attendance Machine`: IP, port, mapping user_id máy ↔ Employee.
- OT thực tế đối chiếu `Overtime Request` đã duyệt, tính tiền trong `payroll/overtime.py` theo hệ số + đêm (+20% lương đêm, +20% trên phần OT nếu OT đêm ngày thường... theo Điều 98 BLLĐ).

---

## 8. LỘ TRÌNH IMPLEMENT (làm theo thứ tự, mỗi phase chạy được độc lập)

**Phase 1 — Payroll VN (core):** constants + VN Payroll Settings + Insurance Rate + Statutory Wage + Dependent + Custom Fields + `vn_payroll.py` + unit tests + báo cáo bảng lương tháng.
**Phase 2 — Pháp lý:** Labor Contract (vòng đời + notification) + Insurance Declaration + export D02-LT + 05/KK-TNCN + PIT Annual Settlement.
**Phase 3 — Chấm công & OT:** ZKTeco connector + Overtime Request + overtime engine + báo cáo lao động.

Với mỗi phase: tạo doctype qua `bench` (JSON chuẩn trong app, không tạo tay trên UI), viết test, migrate thử trên site sạch để verify fixtures.

---

## 9. YÊU CẦU ĐẦU RA CỦA BẠN

1. Scaffold app `dcnet_hrm` (bench new-app) với cấu trúc mục 2.
2. Implement lần lượt theo Phase, mỗi bước show đầy đủ: JSON doctype, Python controller, hooks, fixtures, test.
3. Trước khi code Phase 1, xác nhận lại với tôi: version hrms đang dùng, và các Salary Component đang có sẵn trên site (nếu có) để tránh trùng tên.
4. Không giải thích lan man — code trước, chú thích nghiệp vụ ngắn gọn bằng tiếng Việt tại chỗ cần thiết.
