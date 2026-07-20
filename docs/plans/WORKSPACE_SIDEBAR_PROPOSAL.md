# Workspace Sidebar System - Proposal v2

> **Ngày tạo:** 18/03/2026 | **Cập nhật:** 18/03/2026
> **Branch:** `feature/workspace-sidebar-customization`
> **Tác giả:** Nguyễn Hoàng Long
>
> **Nguồn tham chiếu:**
> - Tài liệu dự án trong `project_docs/`
> - [Club Champion - Golf Club Fitting Process](https://clubchampion.com/golf-club-fitting-process)
> - [2nd Swing - Trade-In Golf Clubs](https://www.2ndswing.com/trade-in-golf-clubs)
> - [True Spec Golf - What Happens During A Club Fitting](https://truespecgolf.com/blog/2023/01/04/what-happens-during-a-club-fitting/)
> - [ProAgenda - Golf Coaching Software](https://www.proagenda.com/blog/how-to-manage-golf-professionals-in-one-golf-management-program-0)
> - [Callaway Trade-In Program](https://www.callawaygolf.com/golf-clubs/trade-in-trade-up)

---

## 1. Tổng quan

### 1.1 Danh sách Workspace Sidebars (11 workspaces)

| # | Workspace | Mô tả | Loại |
|---|-----------|-------|------|
| 1 | **Sản phẩm** | Item, Attributes, Variants, Bảng giá, Hình ảnh | Override |
| 2 | **Mua hàng** | PO, Nhập kho, NCC, Landed Cost, Thanh toán | Override |
| 3 | **Tồn kho** | Nhập/Xuất/Điều chuyển, Lô, Serial, Mùa vụ | Override |
| 4 | **Bán hàng** | Đơn hàng, Giao hàng, Hóa đơn, Chiết khấu | Override |
| 5 | **Trade-in** | Thu cũ đổi mới - workflow riêng | **Mới** |
| 6 | **Fitting** | Dịch vụ fitting gậy - workflow riêng | **Mới** |
| 7 | **Coaching** | Dịch vụ huấn luyện golf - workflow riêng | **Mới** |
| 8 | **Khách hàng & CRM** | Lead, KH, Membership, Tích điểm, CSKH | Override |
| 9 | **Kế toán** | Thu chi, Công nợ, Liên công ty, Thuế, BC | Override |
| 10 | **Nhân sự & Chi nhánh** | Nhân viên, Chi nhánh, Hoa hồng | **Mới** |
| 11 | **Tích hợp** | TMĐT, Giao vận, Website sync | **Mới** |

---

## 2. Chi tiết từng Workspace

### 2.1 Sản phẩm (Products)

> **Đặc thù ngành golf:** Biến thể theo shaft flex, loft, lie angle, grip size, tay thuận/trái.

```
Sản phẩm (Products)
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo sản phẩm mới (/app/item/new)
├── + Import sản phẩm (Excel)
│
├── ─────────── Danh mục ───────────
├── Sản phẩm (Item)
├── Nhóm sản phẩm (Item Group)
├── Thương hiệu (Brand)
│
├── ─────────── Biến thể & Thuộc tính ───────────
├── Thuộc tính sản phẩm (Item Attribute)
│   ├── shaft_flex: Ladies, Senior, Regular, Stiff, X-Stiff
│   ├── shaft_material: Steel, Graphite, Multi-Material
│   ├── loft_angle: 9°, 10.5°, 12°, ...
│   ├── lie_angle: Standard, Flat, Upright
│   ├── hand: Right-Handed, Left-Handed
│   ├── grip_size: Undersize, Standard, Midsize, Oversize
│   ├── club_length: Standard, +0.5", +1", -0.5"
│   └── season: SS2026, FW2026, SS2025, FW2025 (mùa vụ)
├── Mẫu biến thể (Item Variant Settings)
├── Sản phẩm gốc (Template Items)
│
├── ─────────── Giá ───────────
├── Bảng giá (Price List)
│   ├── Bảng giá TM niêm yết
│   ├── Bảng giá Nhật Minh (= TM × tỷ lệ CK)
│   ├── Bảng giá Đại lý cấp 1
│   ├── Bảng giá Đại lý cấp 2
│   └── Bảng giá Bán lẻ
├── Giá sản phẩm (Item Price)
├── Quy tắc giá (Pricing Rule)
│
├── ─────────── Hình ảnh & Tài liệu ───────────
├── Hình ảnh sản phẩm (#66)
├── Tài liệu sản phẩm
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Danh sách sản phẩm
│   ├── Sản phẩm theo nhóm
│   ├── Giá sản phẩm theo bảng giá
│   └── Sản phẩm thiếu thông tin
│
└── Cài đặt sản phẩm (Stock Settings > Item)
```

---

### 2.2 Mua hàng (Buying)

> **Nguồn:** SIDEBAR_NAVIGATION.md, mua_hang.json
> **Luồng:** Yêu cầu mua → Báo giá NCC → PO → Nhận hàng → Landed Cost → Hóa đơn → Thanh toán

```
Mua hàng (Buying)
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo đơn mua (PO)
├── + Tạo yêu cầu mua (Material Request)
├── + Nhập hàng (Purchase Receipt)
│
├── ─────────── Yêu cầu & Đặt hàng ───────────
├── Yêu cầu mua hàng (Material Request)
│   └── Lịch đặt hàng cố định theo mùa vụ
│       ├── Gậy: Tháng 9-10
│       ├── Quần áo & PK: Hàng tháng
│       └── Hàng JP: Tháng 6-7 / 11-12
├── Yêu cầu báo giá (Request for Quotation)
├── Báo giá NCC (Supplier Quotation) - #65 Ưu đãi NCC
├── Đơn mua hàng (Purchase Order) - #04-#08
│   └── Quy trình duyệt: GĐ KD → Ban Lãnh Đạo
│
├── ─────────── Nhận hàng ───────────
├── Phiếu nhập kho (Purchase Receipt) - #07, #71
│   ├── Nhập theo lô (#09)
│   ├── Nhập theo serial (#10)
│   ├── Nhập theo mã vạch (#11)
│   └── Khai báo vòng đời SP (#12)
├── **Chi phí nhập khẩu (Landed Cost Voucher)** ⚠️ BẮT BUỘC
│   └── Phân bổ thuế NK, phí vận chuyển vào giá vốn
├── Biên bản kiểm nhận hàng (Print Format)
├── Trả hàng NCC (Purchase Return)
│
├── ─────────── Hóa đơn & Thanh toán ───────────
├── Hóa đơn mua (Purchase Invoice) - #140
├── Phiếu thanh toán NCC (Payment Entry) - #141
│   ├── Nguồn tiền (#67): Quỹ TM / TK Ngân hàng
│   └── Phương thức (#68): TM / CK / Công nợ
├── Theo dõi thanh toán PO (#69)
├── Đính kèm chứng từ (#70)
├── **Điều khoản thanh toán theo đại lý** ⚠️ BẮT BUỘC
│
├── ─────────── Nhà cung cấp (collapsed) ───────────
│   ├── Nhà cung cấp (Supplier) - #42
│   ├── Nhóm NCC (Supplier Group)
│   ├── Bảng giá NCC (Price List) - #43
│   └── Liên hệ NCC (Contact)
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Theo dõi đơn mua (Procurement Tracker)
│   ├── Phân tích PO (Purchase Order Analysis)
│   ├── Hàng cần đặt & nhận (Items to Order and Receive)
│   ├── Công nợ phải trả (Accounts Payable Summary)
│   ├── Lịch sử mua hàng (#72)
│   ├── Giá mua bình quân (#73)
│   ├── ─────────── BC Tùy chỉnh ───────────
│   ├── BC-01 Theo dõi mua hàng & dự kiến bán (Hạnh)
│   ├── BC-02 Tổng hợp theo dõi đơn hàng (Hạnh)
│   ├── BC-03 Theo dõi kế hoạch mua hàng (Hạnh + Dung)
│   ├── BC-04 Dự kiến chia hàng theo lệnh (Hạnh + Dung)
│   ├── BC-05 So sánh kế hoạch vs đơn hàng (Hạnh + Dung)
│   ├── BC-12 Tổng hợp nhập kho (Dung)
│   ├── BC-13 Theo dõi đặt hàng Gậy (Hạnh)
│   └── BC-14 Theo dõi đặt hàng Quần áo/PK (Hạnh)
│
└── Cài đặt mua hàng (Buying Settings)
```

---

### 2.3 Tồn kho (Stock)

> **Nguồn:** SIDEBAR_NAVIGATION.md, kho.json
> **Đặc thù:** Quản lý Serial (gậy golf), Lô, Mùa vụ (SS/FW), Điều chuyển liên công ty

```
Tồn kho (Stock)
│
├── ─────────── Tạo nhanh ───────────
├── + Nhập kho (Stock Entry - Material Receipt)
├── + Xuất kho (Stock Entry - Material Issue)
├── + Điều chuyển kho (Stock Entry - Material Transfer)
├── + Kiểm kê (Stock Reconciliation)
│
├── ─────────── Nhập - Xuất - Điều chuyển ───────────
├── Phiếu kho (Stock Entry) - #32
├── Phiếu nhập từ PO (Purchase Receipt) - #25
├── Phiếu xuất bán (Delivery Note) - #26
├── Sổ cái kho (Stock Ledger) - #27
├── **Điều chuyển liên công ty TM ↔ NM** ⚠️ BẮT BUỘC
├── Phân bổ hàng trước nhập (Pre-allocation)
│
├── ─────────── Quản lý kho ───────────
├── Kho hàng (Warehouse) - #47
│   └── Vị trí kho dạng cây (#48): Khu vực → Kệ → Ô
├── Danh mục vật tư trong kho (#49)
│
├── ─────────── Lô & Serial ───────────
├── Lô hàng (Batch) - #23
│   └── Vòng đời SP: 6 tháng / 1 năm / 2 năm
├── Serial (Serial No) - #24
│   └── Trạng thái: Tồn / Ký gửi / Đã bán
├── Tem mã vạch (Barcode Label) - #29
├── Tạo tem (#30) + In tem (#31)
│
├── ─────────── Mùa vụ (Season) ───────────
├── **Theo dõi hàng theo mùa vụ** (Custom Field)
│   └── SS/FW + năm: SS2026, FW2026
├── Lọc báo cáo theo mùa vụ
│
├── ─────────── Tồn kho & Kiểm kê ───────────
├── Theo dõi tồn kho dự kiến (#28)
├── Giữ hàng theo đơn (Stock Reservation) - #50
├── Kiểm kê kho (#51)
├── Điều chỉnh kho (#52) - Thừa/thiếu + Lý do
├── Cảnh báo tồn thấp / hết vòng đời (#53)
├── Lịch sử xuất nhập kho (#54)
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Tồn kho (Stock Balance) - #38a
│   ├── Giá trị tồn kho (#38b)
│   ├── SP dưới mức tối thiểu (#38c)
│   ├── Tồn khả dụng (Stock Projected Qty) - #35
│   ├── Hàng bán chậm (Stock Ageing) - #19, #37
│   ├── Hàng sắp hết hạn (Batch Expiry) - #20, #36
│   ├── NXT theo Serial/Lô (#33)
│   ├── Báo cáo theo Serial (#34)
│   ├── Hàng điều chuyển (#21)
│   ├── Hàng thanh lý/sale (#22)
│   ├── ─────────── BC Tùy chỉnh ───────────
│   ├── BC-07 NXT chi tiết Nhật Minh (Dung)
│   │   └── 3 layout × 2 chế độ xem × Giá = TM × CK
│   ├── BC-08 NXT chi tiết TM (Chị Ngân)
│   └── BC-10 Tổng hợp tồn kho (Dung)
│
└── Cài đặt kho (Stock Settings)
```

---

### 2.4 Bán hàng (Selling)

> **Nguồn:** SIDEBAR_NAVIGATION.md, ban_hang.json
> **Luồng:** Báo giá → Đơn hàng → Giữ hàng → Xuất kho → Hóa đơn → Thu tiền

```
Bán hàng (Selling)
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo đơn hàng (Sales Order)
├── + Tạo hóa đơn (Sales Invoice)
├── + Xuất hàng (Delivery Note)
│
├── ─────────── Báo giá & Đơn hàng ───────────
├── Báo giá (Quotation) - B2B cho đại lý
├── Đơn bán hàng (Sales Order) - #55-#62
│   ├── Loại đơn: Vật dụng / Fitting / Coaching / Trade-in
│   ├── Kiểm tra tồn kho khi tạo đơn (#57)
│   └── Đề xuất mua lại / cross-sell (#62)
├── Import/Export đơn hàng (#58, #59)
│
├── ─────────── Giao hàng ───────────
├── Phiếu giao hàng (Delivery Note) - #117
│   └── Kiểm tra công nợ trước khi xuất
├── Trả hàng bán (Sales Return) - #121, #122
│   └── Kiểm tra serial có trên HĐ khách
│
├── ─────────── Hóa đơn & Thanh toán ───────────
├── Hóa đơn bán (Sales Invoice)
│   ├── Bán lẻ (#80): Auto CK + Thẻ + HĐĐT
│   └── Bán buôn (#120): Kế thừa từ DN + Auto giá
├── Phiếu thu (Payment Entry)
├── Credit Note (Giảm giá/Điều chỉnh)
│
├── ─────────── Bán lẻ ───────────
├── Bảng giá bán lẻ (#78)
├── Chính sách CK bán lẻ (#79)
│
├── ─────────── Bán buôn ───────────
├── Kế hoạch bán hàng theo năm (#112)
├── Bảng giá niêm yết (#113)
├── Chính sách CK bán buôn (#114)
├── Kiểm tra hạn mức công nợ (#118)
├── Cảnh báo công nợ quá hạn (#119)
├── Tính thưởng đạt kế hoạch DS (#123)
│
├── ─────────── Khách hàng (collapsed) ───────────
│   ├── Khách hàng (Customer) - #104-#108
│   ├── Nhóm KH (Customer Group)
│   │   └── Đại lý cấp 1, Đại lý cấp 2, Khách lẻ
│   ├── Nguồn KH (Lead Source) - #107
│   └── Import/Export KH (#110, #111)
│
├── ─────────── Chính sách (collapsed) ───────────
│   ├── Bảng giá (Price List) - #99-#103
│   ├── Quy tắc giá (Pricing Rule) - #82
│   ├── Voucher/Coupon (#86)
│   ├── Tính thưởng DS (#85)
│   └── Hạn mức tín dụng (Credit Limit)
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Phân tích bán hàng (#44)
│   ├── DS theo đại lý (#45)
│   ├── Luân chuyển hàng (#46)
│   ├── Tổng hợp đơn hàng (#133)
│   ├── DS theo thời gian (#137)
│   ├── BC khách hàng (#136)
│   ├── Công nợ phải thu (AR Summary)
│   ├── ─────────── BC Tùy chỉnh ───────────
│   ├── BC-06 Tổng hợp đơn Nhật Minh (Dung)
│   ├── BC-09 Bán hàng theo đại lý TM (Chị Ngân)
│   └── BC-11 Tổng hợp bán hàng (Dung)
│
└── Cài đặt bán hàng (Selling Settings)
```

---

### 2.5 Trade-in (Thu cũ đổi mới)

> **Workflow:** Khách mang gậy cũ → Kiểm tra tình trạng → Định giá → KH xác nhận → Nhập kho cũ → Áp credit vào đơn mới

```
Trade-in (Thu cũ đổi mới)
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo đơn Trade-in mới
├── + Định giá nhanh
│
├── ─────────── Đơn Trade-in ───────────
├── Danh sách đơn Trade-in (#124)
├── Tạo đơn Trade-in (#125)
│   └── SP cũ (tên, thương hiệu, tình trạng, giá, ảnh) + SP mới + Voucher
├── Chi tiết đơn Trade-in (#127)
├── Cập nhật đơn Trade-in (#128)
│
├── ─────────── Trạng thái (#126) ───────────
├── Mới
├── Đang kiểm tra
├── Đã định giá
├── Chờ KH xác nhận
├── Đang xử lý
├── Hoàn thành
├── Hủy
│
├── ─────────── Quy trình kiểm tra (#129) ───────────
├── Checklist kiểm tra tình trạng
│   ├── Scratches / Dents
│   ├── Shaft condition
│   ├── Grip wear
│   └── Head/Face condition
├── Ghi nhận ảnh
├── Đề xuất giá
├── Manager duyệt
│
├── ─────────── Tích hợp kho (#130) ───────────
├── Nhập SP cũ vào kho Trade-in
├── Xuất SP mới cho khách
├── Tự động cập nhật tồn kho
│
├── ─────────── Cài đặt (collapsed) ───────────
│   ├── Bảng giá thu mua (Trade-in Price List)
│   ├── Tiêu chí đánh giá tình trạng
│   └── Quy định Trade-in
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Tổng hợp Trade-in (#131)
│   ├── Giá trị hàng cũ đã thu
│   ├── Doanh thu chênh lệch
│   └── BC theo chi nhánh/NV
│
├── ─────────── Dashboard Widget (#132) ───────────
│   ├── Số đơn Trade-in
│   ├── Giá trị chênh lệch
│   ├── Số SP cũ
│   └── Top SP Trade-in
│
└── Cài đặt Trade-in
```

---

### 2.6 Fitting (Dịch vụ Fitting gậy)

> **Workflow:** Đặt lịch → Phỏng vấn → Test swing → Phân tích data → Đề xuất specs → Sales Order
> **Mã:** FIT-YYYY-MM-DD-XX

```
Fitting (Dịch vụ Fitting gậy)
│
├── ─────────── Tạo nhanh ───────────
├── + Đặt lịch Fitting mới
├── + Ghi nhận kết quả Fitting
│
├── ─────────── Lịch hẹn ───────────
├── Lịch Fitting hôm nay
├── Lịch Fitting tuần này
├── Tất cả lịch hẹn (Fitting Appointment) - #202
│
├── ─────────── Quy trình Fitting ───────────
├── Tạo đơn Fitting (#203)
│   └── Nguồn + KH + Lịch hẹn + Chi nhánh + NV Fitting
├── Trạng thái (#204): Mới → Đã XN → Đang thực hiện → Hoàn thành/Hủy
├── Nhập thông số kỹ thuật (#205)
│   ├── Chiều cao, Cân nặng
│   ├── Wrist-to-floor
│   ├── Hand size
│   ├── Swing speed
│   ├── Launch angle
│   ├── Spin rate
│   ├── Ball speed
│   ├── Carry distance
│   ├── Smash factor
│   ├── Handicap
│   └── Skill level
├── Đề xuất specs (Fitting Recommendation)
│
├── ─────────── Dịch vụ phát sinh (#206) ───────────
├── Lắp shaft
├── Thay grip
├── Điều chỉnh loft/lie
├── Đặt gậy custom
├── Combo fitting + gậy
│
├── ─────────── Phân công (#207) ───────────
├── Phân công NV Fitting
├── Đổi NV phụ trách
│
├── ─────────── Chuyển đổi (#208) ───────────
├── Tạo Sales Order từ Fitting
│   └── Button "Tạo đơn hàng" + Pre-fill + Link
│
├── ─────────── Tích hợp Website (#209) ───────────
├── API nhận đăng ký từ website
├── Auto tạo đơn
├── Thông báo cho Sale
│
├── ─────────── Nhân viên Fitting (collapsed) ───────────
│   ├── Danh sách Fitter
│   ├── Lịch làm việc
│   └── KPI Fitter
│
├── ─────────── Báo cáo (collapsed) (#210) ───────────
│   ├── Số buổi Fitting
│   ├── Tỷ lệ chuyển đổi (Fitting → Sales)
│   ├── Doanh thu từ Fitting
│   ├── Doanh thu linh kiện phát sinh
│   └── BC theo NV Fitting
│
├── ─────────── Dashboard Widget (#211) ───────────
│   ├── Số buổi Fitting
│   ├── Doanh thu
│   ├── Tỷ lệ chuyển đổi
│   └── Top NV Fitting
│
└── Cài đặt Fitting
```

---

### 2.7 Coaching (Dịch vụ huấn luyện Golf)

> **Workflow:** Đăng ký → Test đầu vào → Tư vấn gói → Thanh toán → Xếp lịch → Điểm danh → Tiến độ
> **Mã:** COA-YYYY-MM-DD-XX

```
Coaching (Dịch vụ huấn luyện)
│
├── ─────────── Tạo nhanh ───────────
├── + Đăng ký học viên mới
├── + Đặt lịch buổi học
├── + Điểm danh
│
├── ─────────── Lịch học ───────────
├── Lịch học hôm nay
├── Lịch học tuần này
├── Calendar view
│
├── ─────────── Học viên ───────────
├── Danh sách đơn Coaching (#184)
├── Học viên (Student)
├── Hồ sơ học viên (Student Profile)
├── Test đầu vào (#190)
│   └── Ngày test + HLV test + Kết quả + Đề xuất gói
├── Nhập thông số kỹ thuật (#191)
├── Tiến độ học tập (#193)
│
├── ─────────── Trạng thái học viên (#186) ───────────
├── Mới đăng ký
├── Đã test
├── Đang tư vấn
├── Đã thanh toán
├── Đang học
├── Tạm dừng
├── Hoàn thành
├── Hủy
│
├── ─────────── Khóa học & Buổi học ───────────
├── Gói huấn luyện (#187)
│   └── Tên gói, Loại, Số buổi, Thời lượng, Giá, Mô tả
├── Đăng ký khóa học (Course Enrollment) - #185
├── Buổi học (#192)
│   └── Lịch từng buổi + Trạng thái + Nội dung + Bài tập
├── Điểm danh (Attendance)
│
├── ─────────── Huấn luyện viên (collapsed) (#188) ───────────
│   ├── Danh sách HLV
│   ├── Link Employee
│   ├── Chứng chỉ & Kinh nghiệm
│   ├── Chuyên môn
│   ├── Rating
│   └── KPI HLV
│
├── ─────────── Sân tập (collapsed) (#189) ───────────
│   ├── Danh sách sân tập
│   ├── Địa chỉ
│   ├── Số lane
│   ├── SĐT
│   └── Đối tác
│
├── ─────────── Thanh toán (#194) ───────────
├── Tạo Sales Order từ Coaching
│   └── Đơn học phí + Đơn phụ kiện + Link + Theo dõi công nợ
├── Thu học phí
├── Công nợ học phí
│
├── ─────────── Thông báo (#195) ───────────
├── Gửi lịch qua Zalo/Email
├── Thay đổi giờ
├── Nhắc thi đấu
│
├── ─────────── Báo cáo (collapsed) (#196) ───────────
│   ├── Doanh thu đào tạo
│   ├── DT SP phát sinh
│   ├── Số học viên
│   └── KPI HLV
│
├── ─────────── Dashboard Widget (#197) ───────────
│   ├── Số học viên
│   ├── Doanh thu
│   ├── DT SP
│   ├── Top HLV
│   └── Tỷ lệ hoàn thành
│
└── Cài đặt Coaching
```

---

### 2.8 Khách hàng & CRM

```
Khách hàng & CRM
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo Lead mới
├── + Tạo khách hàng
├── + Tạo cơ hội
│
├── ─────────── Quản lý Lead (#175-#183) ───────────
├── Lead
├── Cơ hội (Opportunity)
├── Phân công Lead (#198)
├── Auto từ nhanh_vn (#180) - Webhook
├── Expose API (#183)
│
├── ─────────── Khách hàng ───────────
├── Khách hàng (Customer)
├── Nhóm KH (Customer Group) - #200
├── Tags KH (#199)
├── Trạng thái cơ hội (#201)
│
├── ─────────── Membership ───────────
├── Thành viên (Membership)
├── Gói thành viên (Membership Package)
├── Tích điểm (Loyalty Point Entry)
├── Đổi điểm
│
├── ─────────── Chăm sóc KH (#212-#216) ───────────
├── Phiếu hỗ trợ (Issue) - #214
│   └── Trạng thái: Chưa XL / Đang XL / Đã xong
├── Lịch chăm sóc tự động (#212)
├── Lịch gửi KM tự động (#213)
├── Phân quyền CSKH (#215)
├── Khảo sát hài lòng (#216)
│
├── ─────────── Tích hợp (#217) ───────────
├── Zalo OA
├── Messenger
│
├── ─────────── Cài đặt (collapsed) ───────────
│   ├── Nguồn Lead (Lead Source)
│   ├── Chiến dịch (Campaign)
│   └── Khu vực (Territory)
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Chuyển đổi Lead
│   ├── Top KH doanh thu
│   ├── KH mới theo tháng
│   └── Mức độ hài lòng
│
└── Cài đặt CRM (CRM Settings)
```

---

### 2.9 Kế toán (Accounting)

> **Đặc thù:** 2 pháp nhân TM + NM, giao dịch liên công ty, theo TT200/2014

```
Kế toán (Accounting)
│
├── ─────────── Tạo nhanh ───────────
├── + Lập phiếu thu
├── + Lập phiếu chi
├── + Bút toán (Journal Entry)
│
├── ─────────── Tiền mặt & Ngân hàng ───────────
├── Quản lý tiền mặt - Sổ quỹ (#138)
├── Quản lý tiền ngân hàng (#139)
├── Đối chiếu sao kê ngân hàng (Bank Reconciliation)
│
├── ─────────── Hóa đơn ───────────
├── Hóa đơn bán (Sales Invoice) - #142
├── Hóa đơn mua (Purchase Invoice) - #140
├── **Hóa đơn liên công ty TM ↔ NM** ⚠️ BẮT BUỘC
│   └── TM xuất HĐ bán → Auto tạo HĐ mua phía NM
├── Hóa đơn điện tử (#153)
│
├── ─────────── Thanh toán ───────────
├── Phiếu thu/chi (Payment Entry)
├── Tạm ứng - Hoàn ứng (#145)
│
├── ─────────── Công nợ ───────────
├── Công nợ phải thu (#143)
│   └── Hạn thanh toán + Tuổi nợ
├── Công nợ phải trả (#144)
├── **Điều khoản TT theo đại lý** ⚠️ BẮT BUỘC
│   └── 30 ngày, 45 ngày, v.v. theo từng đại lý
│
├── ─────────── Giá vốn & Tồn kho ───────────
├── Giá trị tồn kho (#146)
├── Giá vốn hàng bán COGS (#147)
│   └── FIFO / Bình quân di động
├── Phiếu phân bổ chi phí NK (Landed Cost)
│
├── ─────────── Chi phí & Phân bổ ───────────
├── Chi phí hỗ trợ hãng (#148)
│   └── Marketing + Trưng bày + Demo
├── Phân bổ chi phí (#149)
│   └── Theo SP + Theo chiến dịch
├── Trung tâm chi phí (Cost Center)
├── Hoa hồng nhân viên (Sales Person Commission)
│
├── ─────────── Tài sản & CCDC ───────────
├── Tài sản cố định (Asset) - #150
├── Khấu hao tài sản theo giờ (#151)
├── Công cụ dụng cụ (#152)
│
├── ─────────── Thuế ───────────
├── Kế toán thuế GTGT (#153)
├── **Kết xuất HTKK** (#154) - Xuất file theo chuẩn thuế
│
├── ─────────── Cài đặt (collapsed) ───────────
│   ├── Hệ thống tài khoản (Chart of Accounts)
│   ├── Cấu hình liên công ty TM + NM
│   ├── Trung tâm chi phí
│   ├── Năm tài chính
│   └── Điều khoản thanh toán
│
├── ─────────── Báo cáo (collapsed) ───────────
│   ├── Sổ cái (General Ledger)
│   ├── Bảng cân đối số phát sinh (Trial Balance)
│   ├── Báo cáo KQKD (#155)
│   ├── Bảng cân đối kế toán (Balance Sheet)
│   ├── **Báo cáo lưu chuyển tiền tệ** ⚠️ BẮT BUỘC
│   ├── BC chi phí (#156)
│   ├── BC quản trị (#157)
│   ├── Tổng hợp NXT (#158)
│   ├── Tồn kho theo kho (#159)
│   ├── Tồn kho theo model (#160)
│   ├── Tồn kho theo lô (#161)
│   ├── Tồn kho theo vòng đời (#162)
│   ├── BC-15 Theo dõi dòng tiền (Chị Ngân)
│   ├── Công nợ phải thu (AR Summary)
│   ├── Công nợ phải trả (AP Summary)
│   └── BC tuổi nợ công nợ phải thu
│
├── ─────────── Mẫu in ───────────
├── **Mẫu in hóa đơn chuẩn VN** (TT200)
├── Mẫu phiếu thu/chi
│
└── Cài đặt kế toán (Accounts Settings)
```

---

### 2.10 Nhân sự & Chi nhánh (HR)

```
Nhân sự & Chi nhánh (HR)
│
├── ─────────── Tạo nhanh ───────────
├── + Tạo nhân viên mới
├── + Tạo chi nhánh
│
├── ─────────── Chi nhánh (#87-#91) ───────────
├── Danh sách Chi nhánh
├── Tạo Chi nhánh
│   └── Tên + Địa chỉ + SĐT + Email + Gán kho
├── Chi tiết Chi nhánh
│   └── Thông tin + Kho liên kết + DS nhân viên
│
├── ─────────── Nhân viên (#92-#98) ───────────
├── Danh sách Nhân viên
├── Tạo Nhân viên (đơn lẻ / hàng loạt)
├── Chi tiết Nhân viên
├── Import/Export NV (Excel)
│
├── ─────────── Hoa hồng & KPI ───────────
├── Nhân viên kinh doanh (Sales Person)
├── Hoa hồng nhân viên
│   └── Fitting / Coaching / Bán hàng
├── KPI nhân viên
│
├── ─────────── Báo cáo (#109) ───────────
│   ├── Tỷ lệ chốt đơn
│   ├── Số đơn
│   ├── Doanh thu theo NV
│   └── Hiệu suất
│
└── Cài đặt HR (HR Settings)
```

---

### 2.11 Tích hợp (Integrations)

```
Tích hợp (Integrations)
│
├── ─────────── Sàn TMĐT (#74) ───────────
├── Shopee
├── TikTok Shop
├── Lazada
├── Website
│
├── ─────────── Đồng bộ dữ liệu (#170-#174) ───────────
├── Đồng bộ danh mục KH (2 chiều)
├── Đồng bộ danh mục hàng hóa (CRM → Website)
├── Đồng bộ tồn kho real-time
├── Đồng bộ đơn hàng (Website → CRM)
│
├── ─────────── Giao vận (#168-#169) ───────────
├── Danh sách đơn giao vận
├── Viettel Post
│   └── Tạo đơn + Đồng bộ mã/dịch vụ/giá/trạng thái
├── GHTK
│
├── ─────────── Cài đặt ───────────
├── API Keys
├── Webhook endpoints
├── Cấu hình đồng bộ
│
└── Logs & Errors
```

---

## 3. Dashboard Widgets (#39-#41, #63-#64, #167)

```
Dashboard
│
├── ─────────── Doanh số tổng quan ───────────
├── Doanh số theo ngày/tuần/tháng (#63)
├── Doanh số bán lẻ tổng (#64)
├── Doanh số theo nguồn KH (#39)
├── Doanh số theo nguồn đơn (#40)
├── Top 20 SP bán chạy (#41)
│
├── ─────────── Dự báo & Cảnh báo ───────────
├── Dự báo doanh thu (#167)
├── Cảnh báo hụt doanh số
│
├── ─────────── Trade-in Widget (#132) ───────────
├── Fitting Widget (#211)
└── Coaching Widget (#197)
```

---

## 4. Báo cáo tùy chỉnh (15 BC từ Danh sách BC)

| # | Tên báo cáo | Người yêu cầu | Workspace |
|---|-------------|---------------|-----------|
| BC-01 | Theo dõi mua hàng & dự kiến bán | Hạnh | Mua hàng |
| BC-02 | Tổng hợp theo dõi đơn hàng | Hạnh | Mua hàng |
| BC-03 | Theo dõi kế hoạch mua hàng | Hạnh + Dung | Mua hàng |
| BC-04 | Dự kiến chia hàng theo lệnh | Hạnh + Dung | Mua hàng |
| BC-05 | So sánh kế hoạch vs đơn hàng | Hạnh + Dung | Mua hàng |
| BC-06 | Tổng hợp theo dõi đơn NM | Dung | Bán hàng |
| BC-07 | NXT chi tiết Nhật Minh | Dung | Tồn kho |
| BC-08 | NXT chi tiết TM | Chị Ngân | Tồn kho |
| BC-09 | Bán hàng theo đại lý TM | Chị Ngân | Bán hàng |
| BC-10 | Tổng hợp tồn kho | Dung | Tồn kho |
| BC-11 | Tổng hợp bán hàng | Dung | Bán hàng |
| BC-12 | Tổng hợp nhập kho | Dung | Mua hàng |
| BC-13 | Theo dõi đặt hàng Gậy | Hạnh | Mua hàng |
| BC-14 | Theo dõi đặt hàng Quần áo/PK | Hạnh | Mua hàng |
| BC-15 | Theo dõi dòng tiền | Chị Ngân | Kế toán |

---

## 5. Các chức năng BẮT BUỘC ⚠️

| Chức năng | Phân hệ | Ghi chú |
|-----------|---------|---------|
| Chi phí nhập khẩu (Landed Cost Voucher) | Mua hàng / Kế toán | Phân bổ thuế NK, phí vận chuyển |
| Điều khoản thanh toán theo đại lý | Mua hàng / Kế toán | 30/45 ngày theo từng đại lý |
| Giao dịch liên công ty TM ↔ NM | Kế toán | 2 pháp nhân riêng |
| Điều chuyển kho liên công ty | Tồn kho | TM ↔ NM |
| Báo cáo lưu chuyển tiền tệ | Kế toán | BC-15 |

---

## 6. Cấu trúc files

```
dcnet_apps/dcnet_apps/workspace_sidebar/
├── products.json      # Quản lý sản phẩm
├── buying.json        # Mua hàng
├── stock.json         # Tồn kho
├── selling.json       # Bán hàng
├── tradein.json       # Trade-in (Custom)
├── fitting.json       # Fitting (Custom)
├── coaching.json      # Coaching (Custom)
├── crm.json           # Khách hàng & CRM
├── accounts.json      # Kế toán
├── hr.json            # Nhân sự & Chi nhánh (Custom)
└── integrations.json  # Tích hợp (Custom)
```

---

## 7. Custom DocTypes cần tạo

### Trade-in
- Trade-in Order, Trade-in Valuation, Trade-in Item, Trade-in Price List

### Fitting
- Fitting Appointment, Fitting Order, Fitting Profile, Fitting Measurement, Fitter

### Coaching
- Student, Coach, Coaching Package, Course Enrollment, Coaching Session, Training Ground, Skill Assessment

### Membership
- Membership, Membership Package

---

**Tác giả:** Nguyễn Hoàng Long
**Review:** Cần review từ team và khách hàng
