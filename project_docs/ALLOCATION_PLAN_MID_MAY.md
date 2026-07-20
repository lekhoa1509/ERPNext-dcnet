# DCNET Flow — Job Allocation Plan (Mid-May 2026 Deadline)

> **Team:** 3 người — anh Long (70% difficult), HauLN (15%), DatMLT (15%)
> **Deadline:** 15/05/2026
> **Baseline:** March features ~done, focus on T4+T5 features
> **Total remaining:** ~173 features

---

## Summary

| Person       |  Features  | Focus                                                                                                                             | Difficulty          |
| ------------ | :--------: | --------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| **anh Long** | ~121 (70%) | Difficult modules: Kế toán, Trade-in, Fitting, Coaching, Bán buôn, Đơn hàng, TMĐT, Giao vận, Tích điểm, Membership, CSKH, Reports | NEW + HARD + MEDIUM |
| **HauLN**    | ~26 (15%)  | Easy-medium modules: Chi nhánh, Nhân viên, Mua hàng (remaining), Kho (tem/barcode), Dashboard, Cài đặt hệ thống                   | EASY + MEDIUM       |
| **DatMLT**   | ~26 (15%)  | Easy-medium modules: Khách hàng, Bảng giá, Chính sách BH, Bán lẻ (easy parts), Báo cáo đơn giản                                   | EASY + MEDIUM       |

---

## Phase 1: 21/03 → 05/04 — Finish T3 + Start T4 Easy

### anh Long

| #   | Module       | Feature                | Difficulty |
| --- | ------------ | ---------------------- | :--------: |
| 153 | Kế toán Thuế | Kế toán thuế VAT/HĐĐT  |    NEW     |
| 154 | Kế toán Thuế | Kết xuất HTKK          |    NEW     |
| 139 | Kế toán Tiền | Quản lý tiền ngân hàng |   MEDIUM   |
| 148 | Chi phí      | Chi phí hỗ trợ hãng    |   MEDIUM   |
| 149 | Chi phí      | Phân bổ chi phí        |   MEDIUM   |
| 151 | Tài sản      | Khấu hao theo giờ      |   MEDIUM   |
| 156 | Kế toán TH   | Báo cáo chi phí        |   MEDIUM   |
| 157 | Kế toán TH   | Báo cáo quản trị       |   MEDIUM   |
| 160 | Báo cáo TH   | BC tồn kho theo model  |   MEDIUM   |
| 162 | Báo cáo TH   | BC tồn kho vòng đời    |    HARD    |
| 167 | Dự báo       | Dự báo doanh thu       |    HARD    |
| 249 | Sản phẩm     | Quản lý thuộc tính SP  |    HARD    |

### HauLN

| #   | Module    | Feature                       | Difficulty |
| --- | --------- | ----------------------------- | :--------: |
| 10  | Mua hàng  | Nhập hàng theo serial (scan)  |    HARD    |
| 11  | Mua hàng  | Nhập hàng theo mã vạch        |   MEDIUM   |
| 30  | Kho       | Tạo tem sản phẩm              |    HARD    |
| 31  | Kho       | In tem                        |    HARD    |
| 63  | Dashboard | Doanh số theo ngày/tuần/tháng |   MEDIUM   |
| 64  | Dashboard | Doanh số bán lẻ tổng          |   MEDIUM   |

### DatMLT

| #   | Module      | Feature                  | Difficulty |
| --- | ----------- | ------------------------ | :--------: |
| 20  | Báo cáo     | BC hàng sắp hết vòng đời |    HARD    |
| 21  | Báo cáo     | BC hàng điều chuyển      |    EASY    |
| 22  | Báo cáo     | BC hàng thanh lý/sale    |   MEDIUM   |
| 36  | Báo cáo Kho | BC vòng đời SP           |   MEDIUM   |
| 37  | Báo cáo Kho | Phân tích kho nhanh/chậm |    EASY    |
| 46  | Báo cáo bán | BC luân chuyển hàng hóa  |   MEDIUM   |

---

## Phase 2: 05/04 → 20/04 — T4 Core (Đơn hàng, Bán hàng, Bán buôn)

### anh Long

| #   | Module   | Feature                              | Difficulty |
| --- | -------- | ------------------------------------ | :--------: |
| 55  | Đơn hàng | Danh sách ĐH (4 loại + 6 filters)    |    HARD    |
| 56  | Đơn hàng | Tạo ĐH Vật dụng (13 fields)          |    HARD    |
| 60  | Đơn hàng | Xem chi tiết ĐH + Bảo hành + Công nợ |    HARD    |
| 62  | Đơn hàng | Resell / Cross-sell                  |    NEW     |
| 79  | Bán lẻ   | Chính sách chiết khấu bán lẻ         |    HARD    |
| 80  | Bán lẻ   | Hóa đơn bán lẻ + HĐĐT                |    HARD    |
| 77  | Danh mục | Kế hoạch doanh số năm                |    HARD    |
| 85  | Bán hàng | Tính thưởng DS (3-step workflow)     |    HARD    |
| 112 | Bán buôn | Kế hoạch bán hàng theo năm           |   MEDIUM   |
| 113 | Bán buôn | Bảng giá bán niêm yết                |   MEDIUM   |
| 114 | Bán buôn | Chính sách CK bán buôn               |   MEDIUM   |
| 115 | Bán buôn | Đơn đặt hàng bán (13 fields)         |   MEDIUM   |
| 117 | Bán buôn | Lệnh xuất hàng + Check công nợ       |    HARD    |
| 118 | Bán buôn | Kiểm tra hạn mức công nợ             |    HARD    |
| 119 | Bán buôn | Cảnh báo công nợ quá hạn             |    HARD    |
| 120 | Bán buôn | Hóa đơn bán buôn                     |   MEDIUM   |
| 121 | Bán buôn | Lệnh nhập hàng trả lại               |   MEDIUM   |
| 122 | Bán buôn | Hàng bán bị trả lại                  |   MEDIUM   |
| 123 | Bán buôn | Tính thưởng đạt KH doanh số          |    HARD    |

### HauLN

| #   | Module    | Feature             | Difficulty |
| --- | --------- | ------------------- | :--------: |
| 87  | Chi nhánh | Danh sách Chi nhánh |    EASY    |
| 88  | Chi nhánh | Tạo Chi nhánh       |    EASY    |
| 89  | Chi nhánh | Chi tiết Chi nhánh  |    EASY    |
| 90  | Chi nhánh | Cập nhật Chi nhánh  |    EASY    |
| 91  | Chi nhánh | Xóa Chi nhánh       |    EASY    |
| 92  | Nhân viên | Danh sách NV        |    EASY    |
| 93  | Nhân viên | Tạo NV              |    EASY    |
| 94  | Nhân viên | Chi tiết NV         |    EASY    |
| 95  | Nhân viên | Cập nhật NV         |    EASY    |
| 96  | Nhân viên | Xóa NV              |    EASY    |
| 97  | Nhân viên | Import NV           |    EASY    |
| 98  | Nhân viên | Export NV           |    EASY    |

### DatMLT

| #      | Module     | Feature                    | Difficulty |
| ------ | ---------- | -------------------------- | :--------: |
| 104    | Khách hàng | Danh sách KH               |    EASY    |
| 105    | Khách hàng | Chi tiết KH                |    EASY    |
| 106    | Khách hàng | Cập nhật KH                |    EASY    |
| 107    | Khách hàng | Nguồn KH                   |    EASY    |
| 108    | Khách hàng | Xóa KH                     |    EASY    |
| 110    | Khách hàng | Import KH                  |    EASY    |
| 111    | Khách hàng | Export KH                  |    EASY    |
| 78     | Bán lẻ     | Bảng giá bán lẻ            |    EASY    |
| 82     | Bán hàng   | Chính sách CK              |    EASY    |
| 83     | Bán hàng   | Bán lẻ (5 sub)             |    EASY    |
| 84     | Bán hàng   | Hàng trả lại               |    EASY    |
| 86     | Bán hàng   | Voucher                    |    EASY    |
| 99-103 | Bán hàng   | Bảng giá CRUD (5 features) |    EASY    |

---

## Phase 3: 20/04 → 05/05 — T4 Advanced (Trade-in, Fitting, Coaching)

### anh Long

| #       | Module   | Feature                                | Difficulty  |
| ------- | -------- | -------------------------------------- | :---------: |
| 124-132 | Trade-in | Full Trade-in module (9 features)      |  NEW/HARD   |
| 202-211 | Fitting  | Full Fitting module (10 features)      |  NEW/HARD   |
| 184-197 | Coaching | Full Coaching module (14 features)     | MEDIUM/HARD |
| 74      | TMĐT     | E-commerce sync (Shopee/TikTok/Lazada) |     NEW     |

### HauLN

| #   | Module   | Feature                  | Difficulty |
| --- | -------- | ------------------------ | :--------: |
| 67  | Mua hàng | Thông tin nguồn tiền     |    EASY    |
| 68  | Mua hàng | Phương thức thanh toán   |    EASY    |
| 69  | Mua hàng | Theo dõi thanh toán PO   |    EASY    |
| 70  | Mua hàng | Đính kèm chứng từ        |    EASY    |
| 72  | Mua hàng | Lịch sử mua hàng         |    EASY    |
| 73  | Mua hàng | Báo cáo mua hàng         |   MEDIUM   |
| 109 | Báo cáo  | BC Nhân viên (4 reports) |   MEDIUM   |

### DatMLT

| #   | Module   | Feature                    | Difficulty |
| --- | -------- | -------------------------- | :--------: |
| 75  | Danh mục | Danh mục đối tượng KH/NCC  |   MEDIUM   |
| 76  | Danh mục | Danh mục vật tư hàng hóa   |   MEDIUM   |
| 81  | Bán hàng | Kế hoạch BH                |   MEDIUM   |
| 133 | Báo cáo  | BC Đơn hàng (4 categories) |   MEDIUM   |
| 134 | Báo cáo  | BC quản trị theo yêu cầu   |   MEDIUM   |
| 135 | Báo cáo  | Kết xuất báo cáo Excel/PDF |    EASY    |
| 136 | Báo cáo  | BC Khách hàng (4 reports)  |   MEDIUM   |
| 137 | Báo cáo  | BC Doanh số (7 reports)    |   MEDIUM   |

---

## Phase 4: 05/05 → 15/05 — T5 (CSKH, Tích điểm, Giao vận, Polish)

### anh Long

| #       | Module     | Feature                                   | Difficulty |
| ------- | ---------- | ----------------------------------------- | :--------: |
| 212-218 | CSKH       | Full CSKH module (7 features)             |    HARD    |
| 222     | Tích điểm  | Tích điểm + Quy tắc lên hạng              |    HARD    |
| 223-235 | Bảo hành   | Đơn hàng BH-BT (8 features)               |    HARD    |
| 168-169 | Giao vận   | Viettel Post / GHTK (2 features)          |    HARD    |
| 170-174 | Web sync   | Đồng bộ KH/SP/Kho/ĐH/Tồn kho (5 features) |    HARD    |
| 234     | Kiểm soát  | Audit log                                 |   MEDIUM   |
| 236-243 | Membership | Full Membership module (9 features)       |    HARD    |
| 244     | Workshop   | Workshop/Event                            |   MEDIUM   |

### HauLN

| #   | Module  | Feature                   | Difficulty |
| --- | ------- | ------------------------- | :--------: |
| 198 | Cài đặt | Phân công Lead            |    EASY    |
| 199 | Cài đặt | Quản lý tags KH           |    EASY    |
| 200 | Cài đặt | Danh sách Nhóm KH         |    EASY    |
| 201 | Cài đặt | Quản lý trạng thái cơ hội |    EASY    |
| 219 | Cài đặt | Danh sách Chức vụ         |    EASY    |
| 220 | Cài đặt | Danh sách Trạng thái ĐH   |    EASY    |
| 221 | Cài đặt | Danh sách Hành động NV    |    EASY    |

### DatMLT

| #       | Module         | Feature                     | Difficulty |
| ------- | -------------- | --------------------------- | :--------: |
| 180     | Lead           | Auto từ nhanh_vn (webhook)  |   MEDIUM   |
| 225-228 | Report Website | 4 website analytics reports |   MEDIUM   |
| 5       | Mua hàng       | Chi tiết PO                 |    EASY    |
| 116     | Bán buôn       | Kiểm tra tồn kho trước xuất |    EASY    |

---

## Post-deadline / Defer (nếu không kịp)

| #   | Feature                 | Reason                  |
| --- | ----------------------- | ----------------------- |
| 245 | Migrate dữ liệu BRAVO   | Needs BRAVO access — T7 |
| 246 | Cài đặt server khách    | T7                      |
| 247 | Bàn giao, chuyển server | T7                      |
| 248 | Đào tạo                 | T7                      |

---

## Risk Assessment

| Risk                                      | Impact | Mitigation                                                              |
| ----------------------------------------- | ------ | ----------------------------------------------------------------------- |
| anh Long overloaded (121 features)        | High   | Use AI agents for code generation, parallel development with tmux teams |
| Customer confirmation pending (⏳)        | Medium | Escalate — list all pending items, request batch confirmation           |
| Trade-in/Fitting/Coaching are NEW modules | High   | Start with DocType design, use /dcnet-start workflow                    |
| E-commerce integration complexity         | High   | Start API research early, may need to defer some platforms              |
| BRAVO data not available                  | Medium | Use sample data for now, migrate T7                                     |

---

## Weekly Check-in Template

```
### Week of [DATE]
- anh Long: [features done] / [features planned]
- HauLN: [features done] / [features planned]
- DatMLT: [features done] / [features planned]
- Blockers:
- Customer pending:
```

---

**Created:** 2026-03-21
**Last Updated:** 2026-03-21
