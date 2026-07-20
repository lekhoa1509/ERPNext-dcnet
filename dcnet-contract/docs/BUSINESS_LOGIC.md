# Business Logic — DCNET Contract

App quản lý hợp đồng kinh doanh cho DCNET — nhà cung cấp dịch vụ viễn thông và trung tâm dữ liệu (ISP + Data Center).

Tài liệu này mô tả **nghiệp vụ thuần túy**. Mục đích: để Giám đốc kinh doanh và Kế toán trưởng DCNET đọc, đối chiếu với quy chế công ty và xác nhận "đúng nghiệp vụ chưa" trước khi đội kỹ thuật viết code. Tài liệu không chứa chi tiết kỹ thuật.

---

## 1. Bối cảnh & Mục đích

DCNET là nhà cung cấp dịch vụ viễn thông + trung tâm dữ liệu, cung cấp:

- **Dịch vụ viễn thông doanh nghiệp:** kênh truyền P2P, MPLS, internet leased line (ILL), FTTH cho doanh nghiệp.
- **Dịch vụ CNTT:** quản trị hệ thống, thuê chỗ đặt máy chủ (colocation), cho thuê tủ rack.
- **Bán vật tư thiết bị (VTTB):** router, switch, máy chủ kèm dịch vụ cài đặt.
- **Thi công công trình:** hạ tầng mạng, triển khai hệ thống.

Toàn bộ khách hàng của DCNET là **doanh nghiệp (B2B)**. DCNET không kinh doanh FTTH hộ gia đình cá nhân — mọi hợp đồng FTTH đều là hợp đồng với doanh nghiệp nhỏ/vừa.

Hiện tại, toàn bộ nghiệp vụ hợp đồng đang được quản lý bằng file giấy + Excel. Mỗi hợp đồng có 1 bộ file Word/PDF (đã in, đã ký, scan lại), và thông tin thanh toán định kỳ theo dõi rời rạc trên sổ kế toán. Khi chuyển đổi từ Misa sang ERPNext, phần quản lý hợp đồng cần được số hóa thành một module chuyên biệt vì:

- ERPNext mặc định chỉ có **Sales Order** (đơn bán đứt — phù hợp bán vật tư) và **Subscription** (lặp lại đơn giản — không đủ cho hợp đồng dịch vụ viễn thông VN).
- ERPNext không có khái niệm "Hợp đồng" với vòng đời nhiều năm (ký → kích hoạt → tạm dừng → gia hạn → chấm dứt), có số hợp đồng giấy, có phụ lục, có lịch thanh toán định kỳ, có phí lắp đặt 1 lần.
- Quy chế kế toán Việt Nam (TT99/2025) và quy chế nội bộ DCNET có những ràng buộc riêng: chốt doanh thu, proration khi ký giữa tháng, gắn hoa hồng nhân viên kinh doanh theo cash basis.

App `dcnet_contract` ra đời để lấp chỗ trống này — là "primitive" (nền tảng) quản lý hợp đồng. Phần chính sách hoa hồng và chi phí ngoài được tách ra một app riêng là `dcnet_pakd` (Phương Án Kinh Doanh).

---

## 2. Phạm vi nghiệp vụ

### 2.1 Trong phạm vi (v1)

- Quản lý **master hợp đồng**: số hiệu nội bộ + số hợp đồng giấy, khách hàng, nhân viên kinh doanh phụ trách, chi nhánh, thời hạn, giá trị, điều khoản.
- **Hợp đồng có thể chứa nhiều loại hạng mục** (`item_kind`): Setup Fee, Recurring Service, One-off Goods — bao gồm cả hợp đồng hỗn hợp 1 HD vừa bán thiết bị vừa ký dịch vụ định kỳ.
- **Sinh lịch thanh toán tự động** khi hợp đồng được duyệt: walk items, mỗi item sinh BS row theo `item_kind` và `payment_mode` của nó.
- **Tính toán pro-rata** tự động khi hợp đồng kích hoạt giữa tháng hoặc chấm dứt giữa tháng.
- **Xuất hóa đơn tự động** theo lịch đã sinh — khi đến hạn, hệ thống tạo hóa đơn bán (Sales Invoice) cho khách hàng.
- **Theo dõi thanh toán**: khi khách trả tiền, cập nhật trạng thái kỳ billing tương ứng (đã thu / còn nợ / quá hạn).
- **Vòng đời hợp đồng**: nháp → đang hiệu lực → tạm dừng → gia hạn hoặc chấm dứt hoặc hết hạn.
- **Quản lý template hợp đồng**: admin/pháp chế duyệt các mẫu hợp đồng Word chuẩn, nhân viên kinh doanh chọn template khi tạo hợp đồng, hệ thống tự điền thông tin khách và xuất file Word/PDF.
- **Cảnh báo hết hạn**: gửi email nhắc trước khi hợp đồng hết hạn.
- **Phát sự kiện "khách đã trả"** để app `dcnet_pakd` bắt và tính hoa hồng nhân viên.

### 2.2 Ngoài phạm vi (v1)

- **Chữ ký điện tử**: chưa tích hợp. Hợp đồng vẫn in ra ký tay rồi scan lưu lại.
- **Hóa đơn điện tử (e-invoice)**: sẽ tích hợp qua module khác, không thuộc app này.
- **Hợp đồng ngoại tệ**: v1 chỉ hỗ trợ VND. Ngoại tệ để sprint sau.
- **Customer portal**: khách hàng tự đăng nhập xem hợp đồng và hóa đơn — để sau 6 tháng.
- **Gia hạn tự động không can thiệp**: v1 chỉ gửi email cảnh báo, việc gia hạn vẫn do nhân viên kinh doanh thao tác tay.
- **Theo dõi SLA (uptime, response time)**: để sprint sau.
- **Tính toán hoa hồng**: thuộc app `dcnet_pakd`, không thuộc app này.

---

## 3. Vai trò & Người dùng

| Vai trò | Mô tả công việc trên hợp đồng |
|---|---|
| **Nhân viên kinh doanh (NVKD)** | Tạo hợp đồng nháp, điền thông tin khách, sản phẩm/dịch vụ, giá. Chỉ được sửa hợp đồng của mình khi còn ở trạng thái nháp. |
| **Trưởng phòng kinh doanh / Giám đốc kinh doanh** | Kiểm tra và duyệt hợp đồng (chuyển từ nháp sang đang hiệu lực). Có quyền xem mọi hợp đồng trong chi nhánh của mình. |
| **Kế toán (Accounts Manager)** | Theo dõi lịch thu, tạo hóa đơn khi đến kỳ, ghi nhận thanh toán, cập nhật kỳ quá hạn, xử lý chấm dứt hợp đồng, tạo credit note khi có hoàn tiền. Có quyền xem và sửa toàn bộ hợp đồng. |
| **Pháp chế / Phòng tổng hợp** | Tác giả của template hợp đồng. Upload file Word mẫu, chỉnh sửa nội dung boilerplate (điều khoản chung, hiệu lực, chấm dứt...). |
| **CEO / Tổng Giám đốc** | Duyệt template hợp đồng mới, ký hợp đồng giấy cuối cùng. Có quyền truy cập toàn bộ hệ thống. |
| **Admin / IT / System Manager** | Cấu hình hệ thống, ánh xạ tài khoản kế toán mặc định, phân quyền người dùng. |
| **Khách hàng** | Nhận bản hợp đồng đã in, nhận hóa đơn định kỳ, thanh toán. Chưa tự đăng nhập hệ thống trong v1. |

---

## 4. Phân loại hợp đồng — theo **item_kind** (CRITICAL, đổi 2026-05-14)

Đây là khác biệt nghiệp vụ quan trọng nhất của app. **1 hợp đồng có thể mix nhiều loại hạng mục cùng lúc** — không phải chia thành 2 hợp đồng riêng như cách cũ.

Mỗi hạng mục (`DCNET Contract Item`) có trường `item_kind` thuộc 1 trong 3 loại:

| `item_kind` | Mô tả | Ví dụ | Chu kỳ thu | Có kho? | Có hoa hồng? |
|---|---|---|---|---|---|
| **Setup Fee** | Phí lắp đặt / kích hoạt 1 lần | Phí lắp đặt P2P, phí đấu nối FTTH | 1 lần khi nghiệm thu | Không | **Không** (rule 6.4) |
| **Recurring Service** | Dịch vụ định kỳ tháng/quý | Cước P2P, MPLS, FTTH DN, IT Managed Service, thuê rack | Định kỳ theo `payment_mode` (Monthly/Prepay) | Không | Có |
| **One-off Goods** | Bán vật tư hoặc thi công 1 lần | Bán router/switch/server, thi công công trình | 1 lần khi giao hàng/nghiệm thu | Có (qua shadow Sales Order) | Có |

### 4.1 `contract_type` = computed từ items

Hệ thống tự suy `contract_type` từ danh sách `items`:

| Items chứa | `contract_type` |
|---|---|
| Chỉ Recurring Service (có/không có Setup Fee) | `Recurring` |
| Chỉ One-off Goods | `One-off` |
| Có cả Recurring Service và One-off Goods | `Mixed` |

Người dùng KHÔNG chọn `contract_type` tay; chỉ thêm/sửa hạng mục.

### 4.2 `payment_mode` per-item, không phải per-contract

Mỗi item có chu kỳ riêng:

- **Setup Fee items:** luôn 1 lần tại `acceptance_date`.
- **Recurring Service items:** chọn Monthly (thu sau từng tháng) hoặc Prepay (thu trước toàn bộ thời hạn gói).
- **One-off Goods items:** luôn 1 lần tại `delivery_date` hoặc `acceptance_date`.

Một hợp đồng hỗn hợp có thể có recurring item Monthly + recurring item Prepay + one-off goods cùng lúc, mỗi loại sinh BS row riêng theo logic của mình.

### 4.3 Ví dụ vòng đời

**HD đơn thuần recurring:** Khách A ký P2P HCM-HN 100Mbps ngày 15/01/2026, gói 12 tháng, cước 10.500.000đ/tháng, phí lắp đặt 3.000.000đ.

- Items: 1× Setup Fee (3M) + 1× Recurring Service Monthly (10.5M/tháng × 12).
- `contract_type` = Recurring.
- Ngày 15/01: nghiệm thu → sinh lịch thu 13 kỳ.
- Kỳ Setup Fee: 3.000.000đ, thu ngay.
- Kỳ tháng 1/2026: pro-rata 17 ngày → ~5.763.000đ.
- Kỳ tháng 2 đến tháng 12/2026: mỗi kỳ full 10.500.000đ.
- Kỳ tháng 1/2027: pro-rata 14 ngày → ~4.746.000đ.
- Ngày 14/01/2027: hợp đồng hết hạn.

**HD hỗn hợp:** Khách B ký 1 hợp đồng gồm: bán 1 switch Juniper (one-off 50.000.000đ) + ký IT Managed Service 12 tháng (cước 8.000.000đ/tháng) + phí lắp đặt 5.000.000đ.

- Items: 1× One-off Goods (50M) + 1× Setup Fee (5M) + 1× Recurring Service Monthly (8M × 12).
- `contract_type` = Mixed.
- Shadow Sales Order tự sinh CHỈ cho item One-off Goods (vì có stock item).
- Lịch billing: 1 Setup Fee + 1 One-off Goods + 12 Recurring → 14 BS rows.

### 4.4 Loại dịch vụ (`service_type`) — vẫn dùng để in hợp đồng và phân loại doanh thu

`service_type` (P2P / MPLS / ILL / FTTH DN / IT Managed / VTTB / Thi công) **không** còn ràng buộc với `contract_type`. Tự do mix:

- 1 hợp đồng `service_type=IT Managed` có thể có item One-off Goods (bán server kèm) + Recurring Service (IT managed monthly).
- 1 hợp đồng `service_type=VTTB` có thể là one-off thuần (bán hàng), nhưng cũng có thể kèm phí cài đặt định kỳ nếu cần.

`service_type` được dùng cho: chọn template hợp đồng, áp commission rate template (PAKD), phân loại báo cáo doanh thu.

---

## 5. Vòng đời hợp đồng (đổi 2026-05-14)

**Bỏ trạng thái Revised** — vì model mới: thay đổi giữa kỳ không tạo hợp đồng mới mà thêm 1 row vào `addenda` child table của hợp đồng gốc (xem §6.9). Hợp đồng gốc tiếp tục sống.

Mỗi hợp đồng đi qua các trạng thái sau:

1. **Nháp (Draft):** NVKD mới tạo, đang điền thông tin. Có thể sửa tự do. Chưa phát sinh nghĩa vụ nào.
2. **Đang hiệu lực (Active):** Trưởng phòng kinh doanh / Giám đốc duyệt, hợp đồng được kích hoạt. Hệ thống sinh lịch thanh toán. Items chính không được sửa nữa; muốn đổi giá/gói/thời hạn → thêm Addendum (§6.9).
3. **Tạm dừng (Suspended):** Khách hàng yêu cầu tạm dừng dịch vụ. Các kỳ billing chưa đến hạn không xuất hóa đơn trong thời gian tạm dừng. Có thể quay lại trạng thái Đang hiệu lực khi khách tiếp tục.
4. **Chấm dứt (Cancelled):** Khách hủy trước khi hết hạn. Tất cả các kỳ billing trong tương lai không còn phát sinh hóa đơn. Các kỳ đã xuất hóa đơn và đã thu tiền thì giữ nguyên; nếu có khoản đã thu chưa sử dụng dịch vụ (đặc biệt với Prepay) thì cần tạo credit note hoàn lại.
5. **Hết hạn (Expired):** Tự động khi đến ngày kết thúc. Nếu không có gia hạn, hợp đồng đóng lại. Lịch sử thanh toán vẫn được lưu trữ.

### 5.1 Ràng buộc chuyển trạng thái

- Từ Nháp chỉ đi đến Đang hiệu lực (khi duyệt) hoặc Chấm dứt (khi hủy nháp).
- Từ Đang hiệu lực có thể đi đến Tạm dừng, Hết hạn, Chấm dứt.
- Từ Tạm dừng có thể quay lại Đang hiệu lực, hoặc đi thẳng đến Chấm dứt / Hết hạn.
- Hết hạn là trạng thái cuối — không quay ngược lại.
- Thêm Addendum không đổi trạng thái hợp đồng (vẫn Active). Chỉ Items / dates / Pricing trong items effective_from sau addendum.date thay đổi.

### 5.2 Ai có quyền chuyển trạng thái

- NVKD: chỉ tạo và hủy khi còn Nháp.
- Trưởng phòng kinh doanh / Giám đốc kinh doanh: duyệt từ Nháp → Đang hiệu lực.
- Kế toán: chấm dứt giữa chừng, chấm Hết hạn, xử lý Tạm dừng.
- Hệ thống tự động: chuyển Hết hạn khi đến ngày kết thúc (daily scheduler).

---

## 6. Quy tắc nghiệp vụ chính

### 6.1 Số hợp đồng

Có 2 loại số hợp đồng song song:

- **Số nội bộ hệ thống:** dạng `HD-2026-00001`, `HD-2026-00002`... Tự động sinh khi tạo hợp đồng. Số reset về `00001` mỗi năm. Tiền tố `HD` = "Hợp đồng". Mục đích: dễ tra cứu, dễ sort theo thời gian trong báo cáo.
- **Số hợp đồng giấy:** dạng `1302/HDDV/DCNET-CBBANK` — số in trên bản giấy đã ký. Điền tay khi nhận được bản ký. Được dùng để đối chiếu với kế toán cũ, in trên hóa đơn và báo cáo cho khách.

Mỗi hợp đồng có đúng 1 số nội bộ (bắt buộc, duy nhất) và tối đa 1 số giấy (tùy chọn, duy nhất nếu điền).

### 6.2 Ngày hợp đồng vs ngày nghiệm thu

2 ngày khác nhau, đều quan trọng:

- **Ngày ký hợp đồng (contract date):** ngày 2 bên ký giấy.
- **Ngày nghiệm thu / kích hoạt dịch vụ (acceptance date):** ngày dịch vụ thực sự bắt đầu — thường sau ngày ký 1-7 ngày (lắp đặt, đấu nối, nghiệm thu kỹ thuật).

Lịch billing tính từ **ngày nghiệm thu**, không phải ngày ký. Điều này phản ánh đúng thực tế: khách chỉ trả tiền khi dịch vụ thực sự hoạt động.

### 6.3 Billing định kỳ và quy tắc pro-rata

**Quy tắc chung:** khi dịch vụ kích hoạt đúng ngày 1 của tháng → tháng đầu tính đủ 1 tháng. Khi kích hoạt giữa tháng → tháng đầu pro-rata theo số ngày thực tế.

**Công thức pro-rata (khớp nguyên văn Mẫu 01 Excel hiện hành):**

> Tổng cước tháng = Làm tròn(Cước hàng tháng / số ngày trong tháng, không lấy phần thập phân) × Số ngày thực tế sử dụng trong tháng

Làm tròn cước ngày **trước** khi nhân với số ngày, không làm tròn tổng cuối. Đây là cách Excel Mẫu 01 đang làm, giữ nguyên để kế toán không phải tính lại các hợp đồng cũ.

**Ví dụ:** Cước 10.500.000đ/tháng, tháng 1 có 31 ngày, khách dùng 17 ngày (15/01 - 31/01):

- Cước 1 ngày = round(10.500.000 / 31, 0) = 338.709,67... → làm tròn thành 339.000đ (làm tròn đến đơn vị VND).
- Cước 17 ngày = 339.000 × 17 = 5.763.000đ.

Chế độ làm tròn mặc định: **làm tròn 4 xuống 5 lên (half-up)** — đúng theo Excel Việt Nam. Kế toán có thể đổi sang banker's rounding qua cấu hình hệ thống nếu muốn.

**Tháng cuối kỳ:** tương tự tháng đầu, tính pro-rata theo số ngày thực tế nếu không đủ tháng.

**Kỳ trả trước (Prepay):** không pro-rata. Xuất 1 hóa đơn duy nhất = cước tháng × số tháng gói.

### 6.4 Phí lắp đặt (setup fee)

- Tách thành 1 kỳ riêng trong lịch billing, ngay trước kỳ tháng 1. Kế toán dễ đối chiếu từng khoản.
- Xuất hóa đơn ngay khi hợp đồng kích hoạt, không chờ đến cuối tháng.
- **Không phát sinh hoa hồng** cho NVKD. Setup fee là chi phí thu hồi đầu tư thiết bị + nhân công lắp đặt, không phải doanh thu dịch vụ — đội NVKD không được tính commission trên khoản này.
- **Không phát sinh chi phí ngoài** (Manager Services, Add Costs, Phí GPVT) — setup fee chảy thẳng vào doanh thu net, không bị trừ phần trăm chi phí.

### 6.5 Ngày đáo hạn hóa đơn (due date)

Mặc định: ngày cuối của kỳ billing. Ví dụ cước tháng 1/2026 → đáo hạn 31/01/2026. Đây là chuẩn viễn thông Việt Nam: dùng xong rồi trả.

Với **Prepay**, due date = ngày kích hoạt (trả trước).

Kế toán có thể cấu hình lại qua hệ thống theo mẫu payment terms riêng (ví dụ: cho nợ 30 ngày sau cuối kỳ).

### 6.6 Thời gian ân hạn (grace period) và quá hạn

Sau ngày đáo hạn, hệ thống cho khách **15 ngày ân hạn** (mặc định, kế toán có thể đổi qua cấu hình). Hết 15 ngày mà chưa nhận được thanh toán → kỳ billing chuyển trạng thái "Quá hạn".

Quá hạn chỉ là cảnh báo cho kế toán, không tự động chuyển hợp đồng sang Tạm dừng. Việc Tạm dừng dịch vụ vì nợ là quyết định kinh doanh, do con người thực hiện thủ công.

### 6.7 Ghi nhận doanh thu (tuân thủ VAS)

- Doanh thu ghi nhận **ngay khi phát hành hóa đơn** (CR 5113 — Doanh thu dịch vụ), không hoãn sang tài khoản 3387.
- Áp dụng cho cả trường hợp Prepay: khách trả trước 12 tháng → ghi nhận doanh thu 12 tháng ngay trên 1 hóa đơn. Nghĩa vụ dịch vụ tiếp diễn được ghi chú trong thuyết minh báo cáo tài chính.
- VAT tách dòng trên hóa đơn (tài khoản 3331 — Thuế GTGT đầu ra). Lịch billing lưu số liệu chưa VAT; VAT tính khi tạo hóa đơn dựa trên template thuế của mặt hàng.

### 6.8 Template hợp đồng và xuất file Word/PDF

**Nguyên tắc:** một mẫu hợp đồng được phê duyệt trước bởi pháp chế + tổng giám đốc; NVKD chọn template khi tạo hợp đồng mới; hệ thống tự điền các biến (tên khách, địa chỉ, MST, giá, thời hạn...) và xuất file Word / PDF để in ký.

**Vòng đời template:**

1. **Nháp:** Pháp chế upload file Word mẫu, chỉnh sửa nội dung.
2. **Chờ duyệt:** Trình trưởng phòng kinh doanh xem xét.
3. **Đã duyệt:** Tổng giám đốc phê duyệt → NVKD sử dụng được.
4. **Lưu trữ:** Template cũ không dùng nữa nhưng các hợp đồng đã dùng template cũ vẫn giữ bản đó nguyên vẹn.

**Biến thay thế:** mỗi template chứa các placeholder như `{{Tên khách hàng}}`, `{{Số hợp đồng}}`, `{{Thời hạn}}`... Hệ thống thay thế tự động khi xuất file.

**Chỉnh sửa per-hợp-đồng:** NVKD có thể chỉnh sửa một vài câu của template riêng cho hợp đồng cụ thể (ví dụ: thêm điều khoản đặc biệt), không ảnh hưởng template gốc.

### 6.9 Phụ lục hợp đồng — child table `Contract Addendum` (đổi 2026-05-14)

**Bỏ pattern cũ** (single flat `appendix_no` + `appendix_date` trên Contract). Mọi phụ lục lưu trong child table `addenda`:

| Field | Mô tả |
|---|---|
| `addendum_no` | Số phụ lục giấy (vd PL01, PL02) |
| `addendum_date` | Ngày ký phụ lục |
| `effective_from` | Ngày áp dụng thay đổi (thường = `addendum_date` hoặc sau) |
| `change_type` | Gia hạn / Đổi gói / Đổi giá / Bổ sung items / Khác |
| `change_summary` | Nội dung thay đổi (tóm tắt 2-3 câu) |
| `signed_pdf` | File scan phụ lục đã ký (tùy chọn) |

Phụ lục KHÔNG thay thế hợp đồng gốc — bổ sung vào nó. Hợp đồng gốc giữ Active. Phụ lục in ra kèm hợp đồng gốc.

### 6.10 Điều chỉnh hợp đồng giữa kỳ — qua Addendum + PAKD Revision

Khi khách yêu cầu thay đổi **giá** hoặc **gói dịch vụ** giữa kỳ (upgrade, downgrade, gia hạn):

1. **Thêm 1 row vào `addenda`** child table của hợp đồng (`addendum_no`, `effective_from`, `change_type`, `change_summary`).
2. **Sửa Items** của hợp đồng nếu cần (thêm item mới, sửa đơn giá, đổi `payment_mode` của item — nhưng chỉ ảnh hưởng `effective_from` về sau).
3. Hệ thống prompt tạo **PAKD Revision** tương ứng (nếu hợp đồng đã có PAKD active) — xem PAKD BUSINESS_LOGIC §5.4.
4. **Engine billing schedule** cho future periods (posting_date ≥ `effective_from`) áp giá mới. Past periods giữ nguyên.
5. Hợp đồng **không đổi trạng thái** — vẫn Active. Không có Revised state nữa.

**Pro-rata khi đổi giá giữa kỳ:** kỳ đang chạy chia 2 phần — phần trước `effective_from` ở giá cũ, phần sau ở giá mới. Engine xử lý tự động dựa trên ngày của BS row.

### 6.11 Chấm dứt giữa kỳ và credit note

Khi khách chấm dứt hợp đồng trước khi hết hạn:

- Các kỳ billing trong tương lai chưa xuất hóa đơn → hủy.
- Các kỳ đã xuất hóa đơn nhưng chưa thu tiền → cân nhắc: có thu cho phần đã dùng không? Thường thu.
- **Trường hợp Prepay đã thu toàn bộ:** phần chưa sử dụng phải **hoàn lại** qua credit note. Hệ thống hiển thị cảnh báo "cần tạo credit note" khi chấm dứt sớm một hợp đồng Prepay còn thời gian chưa dùng.

### 6.12 Nhân viên kinh doanh phụ trách

**Quy tắc: mỗi hợp đồng có đúng 1 NVKD phụ trách.** Hoa hồng không chia. Đây là quy chế DCNET hiện hành.

Nếu trong tương lai DCNET đưa ra chính sách co-sales (nhiều NVKD cùng phụ trách 1 hợp đồng, chia hoa hồng theo tỷ lệ), sẽ xử lý ở app `dcnet_pakd` chứ không đổi cấu trúc hợp đồng.

### 6.13 Chi nhánh (branch)

DCNET có **2 chi nhánh kinh doanh:** HCM và HN. Mỗi hợp đồng phải gắn với 1 chi nhánh. Chi nhánh ảnh hưởng:

- Doanh thu được phân bổ vào cost center tương ứng của chi nhánh.
- Trưởng phòng kinh doanh chỉ xem được hợp đồng của chi nhánh mình.
- Báo cáo doanh thu tách theo chi nhánh.

### 6.14 Liên kết với app PAKD (đổi 2026-05-14)

- **1 PAKD = 1 hợp đồng**, sống suốt đời hợp đồng. Hệ thống ràng buộc duy nhất.
- Khi hợp đồng có phụ lục → PAKD thêm 1 row vào `PAKD Revision` child table tương ứng. PAKD parent không tạo mới.
- PAKD tính hoa hồng NVKD + các khoản chi cho phía khách hàng (Manager Services, Add Costs, Referral), trình duyệt theo workflow riêng.
- Khi khách thanh toán → `dcnet_contract` phát sự kiện `contract_billing_period_paid` → `dcnet_pakd` bắt sự kiện → tính và ghi nhận hoa hồng + bút toán nháp chi phí cho NVKD và người nhận khác.
- Hoa hồng tính theo **cash basis**: khách trả đến đâu, hoa hồng phát sinh đến đó.

### 6.15 Liên kết SI / PE với hợp đồng (mới 2026-05-14)

Sales Invoice + Payment Entry có 2 custom field mới (do `dcnet_contract` quản lý):

- `dcnet_contract` (Link → DCNET Contract) — auto-fill khi auto-invoice scheduler sinh SI; PE fetch từ references SI.
- `billing_period_idx` (Int) — index của BS row sinh ra SI.

Kế toán mở SI hoặc PE thấy ngay hợp đồng nào, kỳ nào. List view filter được theo hợp đồng.

### 6.16 Bi-directional navigation (mới 2026-05-14)

Form Contract hiển thị section "Hóa đơn & Thanh toán" — bảng tích hợp:
- Mỗi kỳ billing có cột: hóa đơn (link SI), trạng thái thu, phiếu thu (link PE), trạng thái hoa hồng.
- Click hóa đơn / phiếu thu → mở SI / PE; ngược lại SI/PE có "Connections" panel show hợp đồng + PAKD.
- Form PAKD cũng có section tương tự (derive qua `contract_ref`).

Chi tiết chính sách hoa hồng + chi phí ngoài không thuộc phạm vi tài liệu này; xem `apps/dcnet_pakd/docs/BUSINESS_LOGIC.md` và spec realignment `docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md`.

---

## 7. Edge cases nghiệp vụ

Phần này liệt kê các tình huống nghiệp vụ không điển hình cần xử lý đúng.

### 7.1 Ký giữa tháng / cuối tháng

- **Ký ngày 15 tháng có 31 ngày, gói 12 tháng:** tháng 1 pro-rata 17 ngày, tháng 2–12 full, tháng 13 pro-rata 14 ngày. Tổng cộng 13 kỳ billing.
- **Ký ngày 31/01 (1 ngày cuối tháng):** tháng 1 pro-rata đúng 1 ngày. Có thể kế toán muốn gộp 1 ngày này vào tháng 2 — **không làm**, vẫn tạo kỳ riêng cho đúng nguyên tắc audit.

### 7.2 Năm nhuận

- Ký ngày 29/02/2028, gói 12 tháng. Ngày kết thúc bình thường sẽ là 28/02/2029 (không có 29/02 ở năm 2029). Tháng cuối ngắn hơn 1 ngày. Hệ thống xử lý tự động bằng cách "co lại" sang ngày hợp lệ cuối cùng của tháng.

### 7.3 Gói 1 tháng

- Trường hợp thử nghiệm trial: gói đúng 1 tháng. Nếu ký giữa tháng → chỉ sinh đúng 1 kỳ billing pro-rata. Hợp lệ.

### 7.4 Hợp đồng giá 0đ

- Trường hợp khuyến mãi free trial: đơn giá = 0. Lịch billing vẫn sinh đủ kỳ nhưng amount = 0. Khi đến kỳ, hệ thống vẫn tạo hóa đơn giá 0 (để audit đầy đủ), hoặc kế toán chọn bỏ qua — tùy chính sách.

### 7.5 Khách hộ gia đình

- DCNET không kinh doanh FTTH hộ gia đình cá nhân. Tuy nhiên khi tạo khách mới, cần xử lý trường hợp khách là doanh nghiệp nhỏ / cá nhân không có MST. Thông tin thay thế: CCCD/CMND, địa chỉ thường trú. Trường MST (tax_id) để trống hợp lệ.

### 7.6 Hợp đồng kéo qua năm tài chính

- Ký 15/10/2026, gói 12 tháng. Kỳ 3 tháng cuối (10/2027–01/2028) rơi vào năm 2027. Doanh thu tự phân bổ đúng kỳ kế toán dựa trên ngày xuất hóa đơn — không cần can thiệp tay.

### 7.7 Chấm dứt Prepay còn thừa nhiều tháng

- Khách Prepay 12 tháng, dùng 3 tháng, muốn chấm dứt. Hệ thống cảnh báo: "Cần tạo credit note hoàn lại X tháng đã thu chưa dùng". Kế toán xác nhận số tiền và tạo credit note. Giá trị hoàn pro-rata theo ngày, không phải theo tháng tròn.

### 7.8 Upgrade giữa kỳ (đổi 2026-05-14)

- Khách đang dùng P2P 100Mbps, muốn lên 200Mbps từ 15/03. Quy trình mới:
  1. Thêm 1 row Addendum (`change_type=Đổi gói`, `effective_from=15/03`, `change_summary="Nâng băng thông 100→200Mbps"`).
  2. Sửa item Recurring Service: thay `unit_price` mới = giá 200Mbps.
  3. Hợp đồng vẫn Active (không có Revised state).
  4. Hóa đơn tháng 3 chia 2 dòng: 14 ngày đầu @ giá 100Mbps + 17 ngày sau @ giá 200Mbps. Engine xử lý dựa trên `effective_from` của Addendum.
  5. PAKD prompt tạo 1 PAKD Revision tương ứng — approval workflow chạy lại cho revision này. Commission/Beneficiary của future periods áp tỷ lệ mới.

### 7.9 Backdating (nhập ngược hợp đồng cũ)

- Kế toán nhập hợp đồng đã ký từ tháng trước vào hệ thống (do chuyển đổi từ Misa). Cho phép ngày nghiệm thu trong quá khứ. Lịch billing sinh bình thường; các kỳ đã qua trạng thái "đã quá hạn" — kế toán đối chiếu với hóa đơn cũ và đánh dấu "đã thu" thủ công.

### 7.10 Ngày ký trước ngày nghiệm thu

- Ký 10/03 nhưng 20/03 mới nghiệm thu xong (đợi lắp đặt). Hợp lệ. Lịch billing tính từ 20/03.

### 7.11 Chấm dứt khi đang tạm dừng

- Khách đang tạm dừng, sau đó quyết định chấm dứt hẳn. Cho phép chuyển trực tiếp Tạm dừng → Chấm dứt, không cần bật lại Đang hiệu lực trước.

### 7.12 Nhiều phụ lục liên tiếp

- Hợp đồng có thể có nhiều phụ lục theo thời gian (phụ lục 01, 02, 03...). Số phụ lục + ngày phụ lục duy nhất trong phạm vi 1 hợp đồng.

---

## 8. Báo cáo / Dashboard (dự kiến)

- **Danh sách hợp đồng sắp hết hạn:** 30/60/90 ngày nữa, cảnh báo nhân viên kinh doanh liên hệ gia hạn.
- **Doanh thu theo loại hợp đồng:** tách recurring vs one-off, tách theo loại dịch vụ (P2P, MPLS, ILL, FTTH DN, IT Managed, VTTB, Thi công).
- **Doanh thu theo chi nhánh:** HCM vs HN.
- **Doanh thu theo nhân viên kinh doanh:** để đánh giá KPI.
- **Tỷ lệ chấm dứt sớm (churn):** theo tháng, theo loại dịch vụ.
- **Công nợ theo hợp đồng:** các kỳ billing còn "Đã xuất hóa đơn" hoặc "Quá hạn". Kế toán dùng để đôn đốc thu tiền.
- **Hợp đồng chưa sinh hóa đơn:** các kỳ tới hạn nhưng hệ thống chưa tự xuất hóa đơn (lỗi scheduler hoặc cấu hình).

---

## 9. Tham chiếu pháp lý và kế toán

- **Luật Thương mại 2005** — điều khoản chung về hợp đồng.
- **VAS (Vietnamese Accounting Standards)** — ghi nhận doanh thu dịch vụ.
- **Thông tư 99/2025** — Chế độ kế toán doanh nghiệp Việt Nam. Hệ thống tài khoản 5113 (Doanh thu dịch vụ), 3331 (Thuế GTGT đầu ra), 131 (Phải thu khách hàng), 111/112 (Tiền mặt / Tiền gửi ngân hàng).
- **Luật Viễn thông + các thông tư hướng dẫn** — phí quyền viễn thông, phí CIVT (áp dụng với dịch vụ P2P, MPLS, ILL). Ảnh hưởng tới phần chi phí ngoài thuộc app `dcnet_pakd`.

---

## 10. Ngoài phạm vi v1 (roadmap tham khảo)

Các tính năng đã được thảo luận nhưng hoãn lại cho các sprint sau:

- **Chữ ký điện tử tích hợp:** v1 xuất PDF, ký tay, scan lại. Tương lai xem xét tích hợp MISA eSign, VNPT CA, hoặc DocuSign.
- **E-invoice (hóa đơn điện tử):** tích hợp với nhà cung cấp e-invoice Việt Nam — module riêng, đồng bộ số hóa đơn về `dcnet_contract`.
- **Customer portal:** khách tự đăng nhập xem hợp đồng, hóa đơn, lịch sử thanh toán, download PDF.
- **Hợp đồng ngoại tệ:** hiện chỉ VND. Tương lai hỗ trợ USD cho khách quốc tế (datacenter thuê rack).
- **SLA tracking:** theo dõi uptime, thời gian phản hồi sự cố, tự động tính phạt SLA trừ vào hóa đơn.
- **Gia hạn tự động (auto-renewal):** khi hợp đồng hết hạn và cấu hình bật auto-renew, hệ thống tự tạo hợp đồng mới kế thừa điều khoản. V1 chỉ cảnh báo email, con người vẫn thao tác tay.
- **API cho đại lý:** đại lý FTTH tự tạo hợp đồng qua API, đi qua workflow duyệt của DCNET.
- **Forecast dòng tiền:** dựa trên lịch billing dự kiến, dự báo dòng tiền 3-6-12 tháng tới.
- **Hợp đồng co-sales (nhiều NVKD):** chia hoa hồng theo tỷ lệ — thuộc trách nhiệm app `dcnet_pakd`.

---

## 11. Open items cần xác nhận với kế toán trưởng DCNET

Các mục sau đang được dev dùng giá trị mặc định, kế toán có thể override qua giao diện cấu hình bất cứ lúc nào:

| # | Mục | Mặc định đề xuất |
|---|---|---|
| 1 | Thời gian ân hạn quá hạn (grace period) | 15 ngày sau ngày đáo hạn |
| 2 | Chế độ làm tròn pro-rata | Làm tròn 4 xuống 5 lên (half-up), khớp Excel VN |
| 3 | Công thức pro-rata | Theo số ngày thực tế của từng tháng (không dùng 30 ngày cố định) |
| 4 | Thời điểm cảnh báo hết hạn | 30 ngày trước ngày kết thúc |
| 5 | Xử lý credit note khi chấm dứt | Cảnh báo thủ công, kế toán tự tạo |
| 6 | Write-off nợ khó đòi | Thao tác thủ công, quyền Kế toán trưởng |
| 7 | Tạm dừng dịch vụ khi khách nợ | Thủ công, không tự động theo số ngày quá hạn |
| 8 | Quy trình duyệt hợp đồng | Trưởng phòng kinh doanh duyệt là đủ, không có chain nhiều cấp |
| 9 | Số template hợp đồng khởi tạo | 1 mẫu chung + 1 mẫu cho mỗi loại dịch vụ (7 loại) |

Ngoài ra, để chốt lần cuối trước khi đưa vào vận hành thực, kế toán vui lòng cung cấp:

- **Bản mẫu hợp đồng thực tế** (đã anonymize) cho: 1 P2P hoặc MPLS, 1 FTTH DN, 1 VTTB hoặc Thi công, 1 hợp đồng đã từng có điều chỉnh giữa kỳ.
- **Danh sách tài khoản kế toán mặc định** cần ánh xạ (doanh thu, phải thu, tiền mặt, tiền gửi, VAT) — cần thiết để hệ thống tự tạo bút toán đúng khi xuất hóa đơn.
- **Ma trận phân quyền chi tiết** cho từng chi nhánh: ai được xem/sửa hợp đồng của chi nhánh nào.

---

## 12. Ghi chú cuối

Tài liệu này được viết dựa trên tổng hợp 4 tài liệu thiết kế nội bộ:

1. Spec chi tiết Sprint A1 của `dcnet_contract` — mô hình dữ liệu, lịch billing, state machine.
2. Tài liệu kiến trúc liên kết `dcnet_contract` ↔ `dcnet_pakd` — lý do tách app, mô hình shadow Sales Order, sprint order.
3. Tài liệu các câu hỏi nghiệp vụ đã trả lời với đội dev — chốt cash-basis commission, chỉ B2B, 1 NVKD / 1 hợp đồng, VND only.
4. **Realignment spec 2026-05-14** (`docs/specs/2026-05-14-contract-pakd-vnacc-realignment.md`) — chốt 8 decision tái cấu trúc 3 app, bao gồm: HD hỗn hợp item-level, Contract Addendum child table thay revision chain, Custom field SI/PE, bi-directional navigation, bỏ Mẫu 02 PAKD, sửa semantic MS/AC.

Mọi thay đổi chính sách (tỷ lệ, tài khoản, ngưỡng thời gian) đều có thể thực hiện qua **giao diện cấu hình của hệ thống**, không cần can thiệp code. Khi đội kế toán DCNET đọc tài liệu này và có câu hỏi / đề xuất chỉnh sửa, ghi chú lại và trao đổi với đội dự án trước khi đội kỹ thuật bắt tay viết code sprint A1.
