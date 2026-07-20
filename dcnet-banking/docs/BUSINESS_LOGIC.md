# Business Logic — VN Banking

App đối soát sao kê ngân hàng và tự động ghi nhận thanh toán cho DCNet.

Tài liệu này mô tả nghiệp vụ thuần tuý — là xuất phát điểm để kế toán viên xác nhận "đúng nghiệp vụ chưa" trước khi đội kỹ thuật bắt tay xây dựng chi tiết. Không chứa chi tiết kỹ thuật (cấu trúc bảng, tên trường, code, API).

---

## 1. Bối cảnh & Mục đích

### 1.1 Vấn đề hiện tại

Hàng ngày (hoặc cuối kỳ), kế toán công nợ của DCNet phải thực hiện chuỗi công việc thủ công:

1. Đăng nhập Internet Banking của từng ngân hàng, tải file sao kê.
2. Mở file Excel, đọc từng dòng giao dịch.
3. Tra cứu hóa đơn bán (SI) / mua (PI) còn nợ tương ứng trong hệ thống kế toán.
4. Khớp từng giao dịch với hóa đơn tương ứng.
5. Lập phiếu thu / phiếu chi (Payment Entry) cho từng giao dịch.
6. Rà soát chênh lệch (phí chuyển khoản, lệch làm tròn) và hạch toán vào tài khoản chi phí phù hợp.

Cách làm này tốn rất nhiều thời gian, dễ sai sót (khớp nhầm hóa đơn, bỏ sót giao dịch, nhập sai số tiền), và khó mở rộng khi quy mô giao dịch tăng.

### 1.2 Mục tiêu app

Cho kế toán DCNet một công cụ duy nhất để:

1. Tải sao kê Excel/HTML từ các ngân hàng đang sử dụng, upload vào hệ thống.
2. Hệ thống tự động phân tích và gợi ý khớp giao dịch với hóa đơn còn nợ.
3. Với một cú nhấn, tạo phiếu thu/chi đã liên kết đúng hóa đơn, đúng đối tác.
4. Cảnh báo rõ các giao dịch thiếu thông tin, chênh lệch, hoặc không khớp để kế toán xử lý thủ công.

**Chỉ tiêu UX:** kế toán hoàn tất 100 dòng sao kê trong chưa đến 2 phút, không cần đọc hướng dẫn.

### 1.3 Người dùng

- **Kế toán công nợ** — người trực tiếp tải sao kê, đối soát, tạo phiếu. Dùng app hằng ngày.
- **Kế toán trưởng** — duyệt phiếu thu/chi nháp trước khi hạch toán chính thức (submit).
- **Quản trị viên / kế toán trưởng** — cấu hình ngưỡng dung sai, tài khoản chi phí, bật/tắt các quy tắc đối soát.

---

## 2. Phạm vi nghiệp vụ (v1)

### 2.1 Trong phạm vi

- Import sao kê từ file Excel (.xls / .xlsx) hoặc HTML (lưu ý: một số ngân hàng xuất file HTML nhưng đặt đuôi .xls) của **4 ngân hàng DCNet đang dùng: BIDV, MB Bank, Sacombank, PG Bank**.
- Nhận diện tự động định dạng của từng ngân hàng theo cấu trúc file.
- Chống trùng: upload lại cùng file, hoặc upload hai file trùng giao dịch — hệ thống không tạo giao dịch trùng.
- Đối soát tự động giữa từng giao dịch ngân hàng với danh sách Sales Invoice / Purchase Invoice còn nợ.
- Phân loại gợi ý theo 4 mức tin cậy (Cao / Trung bình / Thấp / Không có), hiển thị màu trực quan.
- Hỗ trợ một giao dịch ngân hàng khớp với **nhiều hóa đơn** (khách hàng chuyển gộp một lần nhiều HĐ).
- Cho phép tạo Payment Entry đơn lẻ hoặc hàng loạt; mặc định tạo ở trạng thái nháp để kế toán trưởng duyệt.
- Hạch toán chênh lệch nhỏ (phí chuyển khoản) vào tài khoản chi phí phù hợp theo TT99/2025.
- Loại trừ (dismiss) các giao dịch không liên quan đến công nợ (ví dụ phí định kỳ, lãi tiền gửi được ghi nhận qua quy trình khác).
- Chạy lại đối soát sau khi cấu hình thay đổi.

### 2.2 Ngoài phạm vi (v1)

Những nội dung sau đã nằm trong yêu cầu gốc nhưng **không làm trong v1**, sẽ giải quyết ở các dự án/giai đoạn sau:

- Các ngân hàng khác ngoài 4 ngân hàng hiện tại — sẽ bổ sung khi có mẫu file thật và nhu cầu.
- Giao dịch ngoại tệ (USD / EUR) và tỷ giá hối đoái — dùng chức năng sẵn có của ERPNext, không tuỳ biến.
- Kết nối trực tiếp API ngân hàng (Open Banking) — vẫn upload file tay. Kiến trúc được chuẩn bị sẵn để mở rộng, không phải tái kiến trúc khi làm v2.
- Dự báo dòng tiền — nằm ở các module Hợp đồng và PAKD khác.
- Khế ước vay (loan tracking).
- Người dùng tự tạo quy tắc regex tuỳ ý qua giao diện (advanced) — ẩn trong v1.
- Chấm điểm tin cậy bằng học máy (ML scoring).
- Quy tắc khác nhau cho từng tài khoản ngân hàng — cấu trúc sẵn sàng, chưa mở giao diện ở v1.
- Giao diện mobile — v1 chỉ chạy trên desk (máy tính bàn).
- Đối soát thẻ tín dụng.

---

## 3. Vai trò & Phân quyền

| Vai trò | Được làm gì |
|---|---|
| Kế toán công nợ (Accounts User) | Vào màn hình đối soát, upload sao kê, xem gợi ý, tạo phiếu thu/chi ở trạng thái nháp, xác nhận khớp từng dòng, loại trừ (dismiss) giao dịch không liên quan. |
| Kế toán trưởng (Accounts Manager) | Tất cả quyền của kế toán công nợ, cộng thêm: submit (hạch toán chính thức) phiếu thu/chi, chỉnh cấu hình trong Bank Statement Settings (ngưỡng dung sai, matcher nào bật/tắt, tài khoản chi phí chênh lệch). |
| Quản trị hệ thống (System Manager) | Toàn quyền, bao gồm thêm định dạng ngân hàng mới, đăng ký matcher mới, sửa fixtures gốc. |
| Vai trò khác | Không truy cập. |

Các quyết định ảnh hưởng trực tiếp tới báo cáo tài chính (chọn tài khoản chi phí, đặt ngưỡng dung sai, cho phép tự động submit) **phải do người có trách nhiệm kế toán xác nhận**, không phải developer tự đặt.

---

## 4. Quy tắc nghiệp vụ chính

### 4.1 Import sao kê

**Quy trình nghiệp vụ:**

1. Kế toán tải file sao kê từ Internet Banking của ngân hàng tương ứng.
2. Vào màn hình "Đối soát ngân hàng" (Bank Reconcile), chọn tài khoản ngân hàng của công ty tương ứng với sao kê.
3. Kéo thả file vào màn hình upload.
4. Hệ thống nhận diện định dạng theo đặc điểm file (số cột, hàng tiêu đề, merged cell, tên sheet…) và chọn bộ tham số parse phù hợp.
5. Mỗi đợt import được lưu lại như một "phiên đối soát" có ghi nhận: tài khoản ngân hàng, khoảng ngày, file gốc, tổng số dòng, số dòng khớp / chưa khớp / trùng lặp, trạng thái (Nháp / Đã parse / Đã rà soát / Đã hạch toán).

**Chống trùng (dedupe):**

- Mỗi giao dịch ngân hàng được gắn một "dấu vân tay" dựa trên: ngày giao dịch + số tiền + số tham chiếu ngân hàng + nội dung chuyển khoản.
- Nếu giao dịch đã tồn tại trong hệ thống (dù từ đợt import trước hoặc từ ngân hàng khác) → bỏ qua, không tạo trùng.
- Upload lại cùng một file: 0 giao dịch mới được tạo ra, kế toán có thể upload nhầm mà không lo nhân đôi dữ liệu.
- Upload hai file gần giống nhau (ví dụ: file tháng trước có một dòng được sửa lại): chỉ dòng mới được thêm, dòng cũ vẫn là 1 bản ghi duy nhất.

**Lưu ý về định dạng:**
- File từ một số ngân hàng có đầu đề tiếng Việt ở dòng trên và tiếng Anh ở dòng dưới (song ngữ).
- Một số ngân hàng (PG Bank / Petrolimex) xuất file HTML nhưng đặt đuôi .xls — hệ thống nhận biết và parse theo cách phù hợp.
- Một số ngân hàng (MB Bank) có các ô gộp (merged cells) và các dòng tổng hợp xen kẽ giao dịch — hệ thống bỏ qua các dòng tổng hợp / số dư cuối ngày.

### 4.2 Đối soát (matching) và 4 mức tin cậy

Sau khi import, mỗi giao dịch được đưa qua một chuỗi quy tắc đối soát. Kết quả gán một trong 4 mức tin cậy, hiển thị trực quan bằng màu:

| Màu | Mức | Ý nghĩa nghiệp vụ | Hành động của kế toán |
|---|---|---|---|
| 🟢 Xanh lá | Cao (High) | Số hóa đơn xuất hiện trong nội dung chuyển khoản, đồng thời số tiền chính xác. | Hệ thống tự tạo Payment Entry nháp. Kế toán rà nhanh rồi submit hàng loạt. |
| 🟡 Vàng | Trung bình (Medium) | Số tiền khớp (trong dung sai cho phép) với một hóa đơn duy nhất, hoặc khớp qua số tài khoản đối tác. | Xem bảng bên, xác nhận hóa đơn / đối tác đúng, rồi bấm tạo PE. |
| 🟠 Cam | Thấp (Low) | Chỉ khớp mờ theo tên đối tác (tên gần giống, ví dụ viết tắt), hoặc thông tin không chắc chắn. | Phải xác nhận thủ công; có badge "Cần xác nhận". |
| 🔴 Đỏ | Không có (None) | Không quy tắc nào cho gợi ý. | Kế toán tự chọn đối tác + hóa đơn, hoặc dismiss nếu giao dịch không liên quan. |

**Nguyên tắc:**
- Chỉ mức **Cao** mới được hệ thống tự tạo phiếu thu/chi — các mức khác luôn đòi xác nhận của người dùng. Lý do: tạo nhầm phiếu = sai sổ, rủi ro không chấp nhận được.
- Thứ tự các quy tắc là **dừng ngay khi có quy tắc đầu tiên cho ra kết quả** (first-hit-wins), không tổng điểm — để kết quả đối soát là deterministic và giải thích được.

### 4.3 Các quy tắc đối soát (matcher)

Hệ thống có 4 quy tắc đối soát chính, chạy theo thứ tự ưu tiên cấu hình được:

**(a) Khớp theo số hóa đơn trong nội dung chuyển khoản** — mặc định mức Cao

Quy tắc tìm trong nội dung chuyển khoản (ví dụ: "TT HD ACC-SI-2026-00045") các mẫu số hóa đơn được cấu hình (ví dụ: `ACC-SI-...`, `SI-...`, `PINV-...`, hoặc mã hóa đơn điện tử VAT theo TT78/2021 / TT99/2025). Với mỗi mã tìm thấy, hệ thống tra cứu trong danh sách hóa đơn còn nợ:

- Tìm được ≥ 1 hóa đơn và tổng số tiền còn nợ **khớp chính xác** với số tiền giao dịch → mức Cao.
- Tổng số tiền lệch **trong dung sai** → mức Trung bình.
- Không khớp số tiền → mức Thấp (cần xác nhận thủ công).

Giải thích hiển thị cho người dùng: "Tìm thấy SI-0123 trong nội dung chuyển khoản. Số tiền khớp chính xác."

Các mẫu regex do kế toán trưởng cấu hình — tránh hardcode. Công ty có thể bổ sung mẫu riêng (mã đặt hàng, mã hóa đơn điện tử, mã nội bộ…).

**(b) Khớp theo số tiền hóa đơn còn nợ** — mặc định mức Trung bình

Chỉ chạy khi quy tắc (a) không ra kết quả. Hệ thống tìm các hóa đơn còn nợ có **số tiền còn nợ** bằng đúng số tiền giao dịch (trong dung sai) và **ngày lập hóa đơn nằm trong khoảng ±N ngày** quanh ngày giao dịch.

- Chỉ có 1 hóa đơn khớp duy nhất → đề xuất mức Trung bình.
- Có ≥ 2 hóa đơn cùng số tiền khớp → **không đưa ra đề xuất** (tránh khớp nhầm). Kế toán xử lý tay.

Lưu ý: so với số **còn nợ**, không so với số tổng của hóa đơn (vì một hóa đơn có thể đã thanh toán một phần).

**(c) Khớp theo đối tác qua số tài khoản đối ứng** — mặc định mức Trung bình

Nhận diện đối tác (khách hàng / nhà cung cấp) qua số tài khoản đối ứng trong sao kê (cột "Đơn vị chuyển / Đơn vị thụ hưởng" hoặc tương đương). Sau khi biết đối tác, tìm các hóa đơn còn nợ của đối tác này có số tiền khớp.

- Nếu đối tác xác định được nhưng không khớp một hóa đơn đơn lẻ → thử tổ hợp **nhiều hóa đơn** của cùng đối tác có tổng bằng số tiền giao dịch (đến tối đa 5 hóa đơn).
- Chọn tổ hợp có ít hóa đơn nhất; nếu có nhiều tổ hợp cùng kích thước → chọn tổ hợp có hóa đơn sớm nhất.

Giải thích hiển thị: "Đối tác ABC theo số tài khoản đối ứng. Gợi ý tổ hợp 2 hóa đơn: SI-0100 + SI-0101."

**(d) Khớp mờ theo tên đối tác trong nội dung chuyển khoản** — mặc định mức Thấp

Chỉ chạy khi ba quy tắc trên đều không ra kết quả. So tên đối tác với các cụm tên xuất hiện trong nội dung chuyển khoản, cho phép biến thể phổ biến: "CTY" ↔ "Công ty", viết hoa/thường, có/không dấu tiếng Việt. Ngưỡng tương đồng khoảng 80% để loại bỏ tên ngắn gây nhầm lẫn.

Luôn trả về mức Thấp — phải xác nhận tay.

### 4.4 Dung sai (tolerance)

Hai loại dung sai có thể chọn:

- **Giá trị tuyệt đối** (mặc định): chênh lệch ≤ N VND (mặc định 1.000 VND).
- **Theo phần trăm**: chênh lệch / số hóa đơn ≤ N% (mặc định 0,1%).

Cửa sổ thời gian tìm hóa đơn quanh ngày giao dịch: mặc định ±3 ngày. Có thể nới rộng khi cần (ví dụ khách thanh toán trễ, chuyển qua đêm cuối tuần).

### 4.5 Tạo phiếu thu / chi (Payment Entry)

**Tạo đơn lẻ:**
- Chọn giao dịch → ở bảng bên (side panel) xác nhận đối tác và hóa đơn → bấm "Tạo phiếu".
- Phiếu tạo ra được điền sẵn: ngày = ngày giao dịch, số tiền = số trên sao kê, liên kết đối tác, liên kết các hóa đơn phân bổ, phương thức thanh toán (gợi ý: Chuyển khoản / Bank Draft).

**Tạo hàng loạt:**
- Tích chọn nhiều giao dịch mức Cao (đã có phiếu nháp) → "Tạo PE hàng loạt" → N phiếu nháp được tạo.
- "Submit hàng loạt" → hạch toán chính thức toàn bộ phiếu nháp của **đợt import đang mở** (không ảnh hưởng các phiếu nháp của đợt khác).

**Mặc định Draft / Submit:**
- Mặc định tạo phiếu ở trạng thái **Nháp (Draft)** — kế toán trưởng duyệt lại trước khi hạch toán.
- Có thể cấu hình tự động Submit cho mức Cao, nhưng khuyến cáo chỉ bật sau một thời gian vận hành ổn định và có niềm tin vào kết quả đối soát.

**1 giao dịch → nhiều phiếu (phân bổ):**
- Khi một giao dịch khớp với nhiều hóa đơn → một phiếu duy nhất chứa nhiều dòng phân bổ, tối đa 5 hóa đơn mặc định (điều chỉnh được trong cấu hình).

### 4.6 Xử lý chênh lệch nhỏ (phí ngân hàng) — theo TT99/2025

Trên thực tế, số tiền thực nhận thường lệch vài nghìn đồng so với số hóa đơn vì phí chuyển khoản bị trừ bên nhận. Ví dụ: hóa đơn 12.500.000 VND → nhận 12.499.500 VND → chênh 500 VND.

**Quy tắc hạch toán theo Thông tư 99/2025/TT-BTC:**

Chênh lệch này là **chi phí dịch vụ ngân hàng**, không phải khoản write-off qua tài khoản đặc biệt. Tuỳ theo bản chất công ty, hạch toán vào một trong các tài khoản:

| Tài khoản | Tên | Trường hợp sử dụng |
|---|---|---|
| 6415 | Chi phí dịch vụ mua hàng | Phí chuyển khoản liên quan hoạt động mua |
| 6425 | Chi phí dịch vụ ngân hàng | Phí duy trì tài khoản, phí giao dịch chung |
| 6427 | Chi phí tài chính khác | Chênh lệch tỷ giá nhỏ, phí khác |

Một số công ty hạch toán qua TK 635 (chi phí tài chính) hoặc 811 (chi phí khác), ít phổ biến hơn.

**Cách hoạt động trong app:**

1. Quản trị viên chọn **tài khoản chi phí chênh lệch** mặc định trong cấu hình (một lần duy nhất).
2. Khi tạo phiếu cho một giao dịch có chênh lệch ≤ dung sai VÀ đã cấu hình tài khoản này → phiếu tự thêm một dòng Deductions (khấu trừ) với tài khoản và số tiền chênh lệch.
3. Nếu chưa cấu hình tài khoản → phiếu tạo với số tiền gốc, không hạch toán chênh lệch (giữ nguyên hành vi ERPNext chuẩn).
4. Nếu chênh lệch **vượt** dung sai → không tự tạo phiếu, giao dịch được đánh cảnh báo vàng, kế toán xử lý tay.

Không hardcode số tài khoản — hệ thống kế toán của mỗi công ty có thể khác nhau.

### 4.7 Loại trừ (dismiss) giao dịch không liên quan

Một số giao dịch trên sao kê không liên quan công nợ khách hàng / nhà cung cấp, chẳng hạn:

- Phí quản lý tài khoản, phí SMS banking định kỳ.
- Lãi tiền gửi được ghi nhận qua quy trình riêng.
- Chuyển khoản nội bộ giữa hai tài khoản của cùng công ty.

Kế toán có thể **dismiss** để ẩn giao dịch khỏi danh sách đối soát — không tạo phiếu, không cảnh báo, vẫn giữ bản ghi gốc để audit.

### 4.8 Chạy lại đối soát sau khi thay đổi cấu hình

Khi kế toán trưởng chỉnh cấu hình (bật/tắt matcher, đổi dung sai, thêm mẫu regex mới) → màn hình đối soát hiện cảnh báo "Cấu hình đã thay đổi — chạy lại?" với nút chạy lại. Hệ thống áp dụng cấu hình mới cho các giao dịch chưa tạo phiếu, giữ nguyên các giao dịch đã có phiếu.

---

## 5. Workflow sử dụng hàng ngày

Quy trình chuẩn mỗi ngày / mỗi phiên đối soát:

1. Cuối ngày (hoặc đầu ngày hôm sau), kế toán đăng nhập Internet Banking, tải file sao kê từng tài khoản.
2. Mở màn hình "Đối soát ngân hàng", chọn tài khoản ngân hàng tương ứng với file.
3. Upload file → hệ thống parse → hiển thị bảng giao dịch kèm màu.
4. **Xử lý theo thứ tự từ xanh tới đỏ:**
   - 🟢 Xanh: tích chọn tất cả → bấm "Submit hàng loạt" các phiếu nháp đã có.
   - 🟡 Vàng: click từng dòng → xem bảng bên → xác nhận hóa đơn/đối tác → tạo phiếu.
   - 🟠 Cam: click từng dòng → xem gợi ý mờ → nếu đúng thì xác nhận, nếu sai thì chọn tay.
   - 🔴 Đỏ: click từng dòng → chọn tay đối tác và hóa đơn, hoặc dismiss nếu không liên quan.
5. Kiểm tra số tổng kết: "120 giao dịch · 85 khớp · 20 gợi ý · 15 chưa · chênh 12.000 VND".
6. Báo cáo đối soát hoàn tất cho kế toán trưởng duyệt.

Mục tiêu: tập trung 95% thời gian vào các dòng thật sự cần phán đoán (Medium / Low / None), không phải vào các dòng đã rõ (High).

---

## 6. Edge cases nghiệp vụ — Khi nào khác?

Theo nguyên tắc "mỗi quy tắc phải được kiểm lại: khi nào không áp dụng, khi nào áp dụng khác, khi nào dữ liệu vi phạm giả định", dưới đây là các tình huống đã được xem xét:

### 6.1 Import & dedupe

- **Upload lại cùng file** → 0 giao dịch mới, an toàn.
- **Sao kê thiếu một giao dịch** (ngân hàng báo thiếu, cần bổ sung): upload file sửa → chỉ dòng mới được thêm.
- **Sao kê trùng giao dịch** (cùng ngân hàng xuất 2 file chồng lấn ngày): dedupe xử lý tự động, mỗi giao dịch chỉ 1 bản ghi duy nhất.
- **File sai định dạng** (không phải sao kê, hoặc sao kê của ngân hàng khác): hệ thống báo lỗi trong nhật ký import, đề xuất chọn tay định dạng hoặc huỷ.
- **File HTML đuôi .xls** (PG Bank): nhận diện tự động bằng 32 byte đầu file, route sang parser HTML.
- **Dòng không phải giao dịch** (dòng tổng hợp "Số dư cuối ngày", dòng trống, header lặp): bỏ qua.

### 6.2 Matching

- **Khách chuyển gộp 3 hóa đơn một lần:** quy tắc (c) tổ hợp đa hóa đơn xử lý tự động khi đã xác định được đối tác qua số tài khoản.
- **Khách trả thiếu / trả thừa so với hóa đơn:**
  - Lệch ≤ dung sai → hạch toán chênh lệch vào TK phí (nếu đã cấu hình), mức tin cậy xuống Trung bình.
  - Lệch > dung sai → không tự tạo phiếu, cảnh báo vàng, kế toán xử lý tay (có thể tạo phiếu với số tiền thực tế, phần còn lại để hóa đơn vẫn còn nợ).
- **Nhiều hóa đơn cùng số tiền còn nợ:** quy tắc (b) chủ động bỏ qua để tránh khớp nhầm.
- **Cùng số tài khoản dùng cho 2 khách hàng khác nhau:** hiếm, nhưng tồn tại. Trong trường hợp này quy tắc (c) sẽ trả về đối tác gần nhất được cập nhật — khuyến cáo quản trị cập nhật dữ liệu master để 1 tài khoản = 1 đối tác.
- **Tên đối tác quá ngắn** ("ABC", 3 ký tự): quy tắc (d) chỉ trả về mức Thấp và yêu cầu xác nhận tay, tránh false positive.
- **Nội dung chuyển khoản chứa nhiều số hóa đơn nhưng chỉ một số còn nợ:** quy tắc (a) gom tất cả mã, chỉ ghép với hóa đơn còn nợ, bỏ qua hóa đơn đã thanh toán.
- **Số hóa đơn công ty đổi định dạng giữa các kỳ** (ví dụ thêm mã chi nhánh): quản trị thêm mẫu regex mới trong cấu hình, không cần sửa code.

### 6.3 Chênh lệch & phí

- **Tài khoản chi phí chênh lệch bị vô hiệu/đóng:** phiếu tạo ra sẽ bị từ chối bởi kiểm tra kế toán → cần chọn tài khoản khác.
- **Chênh lệch âm (nhận nhiều hơn hóa đơn):** nếu ≤ dung sai → hạch toán như chiều ngược lại; nếu > dung sai → cảnh báo và không tự tạo.
- **Phí ngân hàng định kỳ trên sao kê** (phí SMS, phí duy trì): không có hóa đơn đối ứng → rơi vào mức Đỏ → kế toán dismiss hoặc lập phiếu chi phí riêng.

### 6.4 Tạo phiếu

- **Thất bại do thiếu quyền / validation kế toán:** giao dịch giữ nguyên, lỗi ghi vào nhật ký đợt import; các phiếu khác trong batch vẫn tiếp tục tạo — không fail cả batch.
- **Chuyển khoản nội bộ giữa 2 tài khoản của chính công ty:** hệ thống không biết đây là nội bộ trừ khi được cấu hình; kế toán dismiss và lập bút toán điều chuyển thủ công.
- **Nhận tiền từ đối tác chưa có trong hệ thống:** giao dịch rơi vào mức Đỏ; kế toán tạo Customer / Supplier trước, rồi quay lại khớp.

### 6.5 Đa công ty / đa tiền tệ

- **Hệ thống có nhiều công ty:** hệ thống chỉ lấy hóa đơn thuộc đúng công ty của tài khoản ngân hàng đang đối soát, không trộn lẫn.
- **Ngoại tệ USD/EUR:** ngoài phạm vi v1 — xem mục 2.2.

---

## 7. Cấu hình quan trọng (ai chốt gì)

Các thông số sau quyết định kết quả đối soát và ảnh hưởng báo cáo tài chính. Theo nguyên tắc "AI đề xuất, con người chốt", các giá trị này **phải do kế toán trưởng / quản trị xác nhận**, không do đội phát triển tự đặt:

- **Tài khoản hạch toán chênh lệch** (mặc định trống): chọn đúng theo chart of accounts của công ty (gợi ý 6415 / 6425 / 6427 theo TT99/2025). Chọn sai = báo cáo chi phí sai.
- **Ngưỡng dung sai**: quá cao → write-off nhiều; quá thấp → nhiều dòng cần review tay. Mặc định 1.000 VND, điều chỉnh theo quy mô giao dịch.
- **Có cho tự động Submit phiếu không?** Mặc định Draft (nháp, kế toán trưởng duyệt). Chỉ chuyển sang Submit sau khi vận hành ổn định.
- **Mẫu regex số hóa đơn**: mặc định có sẵn cho định dạng ERPNext. Nếu công ty dùng mã hóa đơn riêng (HĐĐT VAT TT78/2021, mã nội bộ…) → bổ sung.
- **Ma trận phân quyền**: ai được submit phiếu, ai được sửa cấu hình — quyết định bởi quản lý.

---

## 8. Tham chiếu pháp lý & chuẩn nghiệp vụ

- **Thông tư 99/2025/TT-BTC**: phân loại chi phí dịch vụ ngân hàng (6415 / 6425 / 6427).
- **Thông tư 78/2021/TT-BTC**: mẫu hóa đơn điện tử VAT (các công ty sử dụng cần cấu hình regex tương ứng trong danh sách mẫu số hóa đơn).
- Chuẩn mực kế toán Việt Nam (VAS): đối soát sổ phụ ngân hàng, ghi nhận phiếu thu/phiếu chi, hạch toán công nợ.

---

## 9. Tóm tắt nguyên tắc thiết kế nghiệp vụ

1. **Minh bạch & giải thích được**: mỗi gợi ý của hệ thống đều có lời giải thích lý do ("Khớp theo số hóa đơn trong nội dung. Số tiền khớp chính xác.") — kế toán không phải tin "hộp đen".
2. **Deterministic**: cùng dữ liệu cho ra cùng kết quả. Không có điểm ngẫu nhiên / gray zone khó debug.
3. **Con người duyệt việc ảnh hưởng tiền**: mặc định tạo phiếu nháp, không auto submit ở các mức không chắc chắn. Các cấu hình ảnh hưởng báo cáo tài chính đều do người có thẩm quyền đặt.
4. **Dễ mở rộng cho ngân hàng mới**: thêm ngân hàng = thêm một bộ tham số định dạng + file mẫu, không cần dev viết code mới.
5. **Sẵn sàng cho tương lai**: kiến trúc dữ liệu đã chừa chỗ cho v2 (pull API ngân hàng, webhook), không phải thay đổi lớn khi mở rộng.
6. **Giữ nguyên tắc kế toán VN**: chênh lệch phí ngân hàng đi vào TK chi phí phù hợp (TT99/2025), không "write-off" qua tài khoản đặc biệt.

---

*Tài liệu nghiệp vụ này là xuất phát điểm — mọi thay đổi về phạm vi, quy tắc đối soát, hoặc cách xử lý chênh lệch cần cập nhật file này trước khi sửa code.*
