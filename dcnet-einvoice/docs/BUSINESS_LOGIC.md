# Business Logic — Ứng dụng Hóa đơn điện tử (einvoice)

> Tài liệu nghiệp vụ thuần. Mô tả WHO/WHAT/WHEN/WHY bằng ngôn ngữ kế toán Việt Nam. Không chứa tên DocType, field, API, hay mã nguồn. Đây là xuất phát điểm của dự án — spec kỹ thuật và kế hoạch triển khai đều phải dẫn nguồn về tài liệu này.

---

## 1. Bối cảnh & Mục đích

Từ ngày 01/07/2022, toàn bộ doanh nghiệp Việt Nam bắt buộc sử dụng Hóa đơn điện tử (HĐĐT) có mã hoặc không có mã của cơ quan thuế, thay thế hoàn toàn hóa đơn giấy. Khung pháp lý chính gồm Nghị định 123/2020/NĐ-CP và Thông tư 78/2021/TT-BTC. Doanh nghiệp không được tự in HĐĐT trên hệ thống của mình — mỗi hóa đơn bán ra phải đi qua một nhà cung cấp dịch vụ HĐĐT được Tổng cục Thuế chấp thuận (T-VAN / tổ chức truyền nhận), ký số, và đẩy dữ liệu lên cơ quan thuế.

Do vậy, một doanh nghiệp dùng ERP không thể "tự phát hành" HĐĐT mà phải tích hợp với ít nhất một nhà cung cấp HĐĐT bên ngoài. Thị trường Việt Nam hiện có hàng chục nhà cung cấp (Mắt Bão, Viettel, MISA, VNPT, BKAV, M-Invoice, EasyInvoice, ...). Mỗi nhà cung cấp có API, cấu trúc dữ liệu, quy trình cấp token, cách ký số riêng, nhưng đều phải tuân theo khuôn mẫu dữ liệu chung do Tổng cục Thuế quy định (XML theo chuẩn TCT).

Ứng dụng `einvoice` đóng vai trò là **lớp tích hợp (integration layer)** giữa hệ thống ERP của doanh nghiệp và một hoặc nhiều nhà cung cấp HĐĐT, phục vụ hai chiều nghiệp vụ:

- **Đầu ra (outward):** Doanh nghiệp bán hàng/dịch vụ, phát hành HĐĐT cho khách hàng thông qua nhà cung cấp.
- **Đầu vào (inward):** Doanh nghiệp mua hàng/dịch vụ, nhận HĐĐT từ nhà cung cấp của bên bán, cần đối chiếu và hạch toán vào sổ sách.

Mục tiêu của ứng dụng: kế toán không phải thao tác trên cổng web của nhà cung cấp HĐĐT cho từng hóa đơn, dữ liệu ERP và HĐĐT không bị lệch, giảm thiểu nhập liệu tay và sai sót kê khai.

## 2. Phạm vi

### Trong phạm vi (in scope)

- Phát hành HĐĐT đầu ra từ hóa đơn bán hàng (đã duyệt/đã ghi sổ) sang cổng nhà cung cấp HĐĐT, lấy về số HĐ, mã tra cứu, tệp PDF/XML.
- Huỷ HĐĐT đầu ra đã phát hành (có lý do), đồng bộ trạng thái huỷ với nhà cung cấp.
- Đồng bộ định kỳ HĐĐT đầu vào từ cổng nhà cung cấp về ERP, lưu tạm dưới dạng "danh sách HĐ đầu vào chờ xử lý".
- Tự động đối chiếu (matching) HĐĐT đầu vào với các hóa đơn mua hàng đã nhập trong ERP (nếu có) hoặc tự động tạo mới hóa đơn mua trong ERP từ dữ liệu đầu vào.
- Cấu hình nhiều nhà cung cấp HĐĐT theo từng pháp nhân (công ty), có một nhà cung cấp mặc định để dùng khi hệ thống không xác định được lựa chọn cụ thể.
- Phát hành hàng loạt (bulk) một nhóm hóa đơn đã chọn, với giới hạn số lượng cấu hình được.
- Ghi nhật ký mọi lần phát hành và mọi lần đồng bộ đầu vào, phục vụ đối soát và kiểm toán nội bộ.

### Ngoài phạm vi (out of scope)

- **Ký số (digital signature) bằng USB Token / HSM.** Toàn bộ việc ký số do nhà cung cấp HĐĐT thực hiện trên hạ tầng của họ. Ứng dụng chỉ gửi dữ liệu và nhận kết quả đã được ký.
- **Quản lý mã tra cứu của khách hàng B2C / POS.** Ứng dụng hướng tới nghiệp vụ B2B: khách hàng là doanh nghiệp có mã số thuế. Các tình huống bán lẻ cho cá nhân (không có MST) vẫn có thể phát hành nhưng không phải trọng tâm tối ưu.
- **In hóa đơn giấy / hóa đơn tự in nội bộ.** Không còn hợp lệ theo pháp luật hiện hành.
- **Cổng người mua tra cứu.** Mỗi nhà cung cấp HĐĐT đã có cổng riêng (tra cứu qua mã + MST); ứng dụng không dựng lại.
- **Kê khai thuế GTGT theo kỳ.** Ứng dụng cung cấp dữ liệu nguồn nhưng không thay thế tờ khai thuế.
- **Viettel và MISA.** Trong phiên bản hiện tại, chỉ có luồng tích hợp Mắt Bão được coi là hoàn thiện. Viettel và MISA được giữ chỗ ở dạng khung (stub) với thông báo "chưa sẵn sàng, liên hệ để triển khai" khi người dùng cố gắng cấu hình.

## 3. Vai trò người dùng

| Vai trò | Trách nhiệm chính |
|---|---|
| Kế toán bán hàng | Tạo hóa đơn bán hàng trong ERP, phát hành HĐĐT sau khi hóa đơn được duyệt, xử lý huỷ HĐ sai, xuất hàng loạt cuối kỳ. |
| Kế toán mua hàng | Rà soát danh sách HĐĐT đầu vào đã đồng bộ về, đối chiếu với hóa đơn mua (nếu đã nhập trước), xác nhận tạo mới hóa đơn mua từ dữ liệu đầu vào, đánh dấu các HĐ bị bỏ qua. |
| Kế toán trưởng | Duyệt chính sách phát hành (chế độ nháp vs phát hành ngay), ngưỡng sai lệch cho auto-match, giới hạn bulk. Phê duyệt huỷ HĐ có giá trị lớn. |
| Quản trị hệ thống (System Manager) | Khai báo các nhà cung cấp HĐĐT, nhập URL/tài khoản/token, chọn mẫu số – ký hiệu hóa đơn theo hợp đồng đã ký với nhà cung cấp. Bật/tắt lịch đồng bộ tự động. Không tham gia nghiệp vụ hàng ngày. |
| Kiểm toán / Auditor | Xem nhật ký phát hành và nhật ký đồng bộ (chỉ đọc). Đối chiếu giữa hóa đơn bán trong ERP và HĐĐT đã phát hành ngoài cổng. |

Quyền thao tác nghiệp vụ giới hạn ở hai nhóm: **Quản trị hệ thống** và **Kế toán trưởng (Accounts Manager)**. Kế toán cấp thấp hơn (Accounts User) chỉ được xem. Điều này xuất phát từ yêu cầu kiểm soát: việc phát hành HĐĐT không thể thu hồi (chỉ có thể huỷ và phát hành thay thế, vẫn có dấu vết pháp lý), nên không thể giao cho người dùng không chịu trách nhiệm kế toán.

## 4. Khái niệm "Nhà cung cấp HĐĐT" (Provider)

Một **nhà cung cấp HĐĐT** (provider) trong ứng dụng đại diện cho một cấu hình kết nối cụ thể tới một cổng dịch vụ HĐĐT bên ngoài, gắn với:

- Một pháp nhân (công ty) của doanh nghiệp — vì mỗi công ty có một mã số thuế riêng và thường ký hợp đồng với một nhà cung cấp riêng.
- Mã số thuế công ty, dùng khi gọi API (nhà cung cấp dùng MST để phân định dữ liệu của từng khách hàng của họ).
- URL API (có thể tách riêng URL cho luồng đầu ra và URL cho luồng đầu vào — Mắt Bão dùng hai URL khác nhau).
- Thông tin xác thực (token, hoặc username/password, hoặc API key — tuỳ chính sách của từng nhà cung cấp).
- Ký hiệu mẫu số và ký hiệu hóa đơn mặc định (xem Mục 5).

Một công ty **có thể cấu hình nhiều provider** (ví dụ dự phòng khi nhà cung cấp chính gặp sự cố), nhưng **tại một thời điểm chỉ chọn một provider để phát hành**. Hệ thống có một "provider mặc định" toàn cục dùng cho trường hợp không truyền tham số cụ thể.

Nhà cung cấp có thuộc tính **trạng thái kết nối** (chưa thử, đã kết nối, thất bại) và thời điểm kiểm tra lần cuối. Người quản trị bấm "Kiểm tra kết nối" để xác nhận cấu hình đúng trước khi đưa vào vận hành.

Hỗ trợ ba loại provider hiện hữu (Mắt Bão, Viettel, MISA) cộng với một loại "Custom" để mở rộng sau. Viettel và MISA hiện ở dạng stub — khi người dùng chọn loại này và cố phát hành, hệ thống trả về thông báo "provider chưa sẵn sàng, vui lòng liên hệ đội triển khai" thay vì báo lỗi kỹ thuật khó hiểu.

## 5. Quy tắc nghiệp vụ đầu ra (Outward)

### 5.1 Vòng đời của một hóa đơn bán trong ERP gắn với HĐĐT

1. Kế toán bán hàng tạo hóa đơn bán hàng trong ERP ở trạng thái nháp.
2. Hóa đơn được **duyệt/ghi sổ** (Submitted) — đây là điểm tham chiếu bắt buộc: **không thể phát hành HĐĐT từ hóa đơn còn ở trạng thái nháp**, vì HĐĐT mang giá trị pháp lý, không được phép tuỳ ý sửa sau đó.
3. Người dùng bấm "Phát hành HĐĐT" trên hóa đơn. Hệ thống ánh xạ dữ liệu ERP sang cấu trúc mà nhà cung cấp yêu cầu, gửi đi, nhận về **số hóa đơn, ký hiệu mẫu số, ký hiệu hóa đơn, mã tra cứu, và đường dẫn PDF**.
4. Hóa đơn ERP được đánh dấu "đã phát hành HĐĐT" cùng thông tin từ nhà cung cấp. Từ lúc này không được phát hành lại.
5. Khi cần huỷ (do nhập sai, thoả thuận huỷ với khách), người dùng bấm "Huỷ HĐĐT" kèm **lý do huỷ bắt buộc**. Hệ thống gửi lệnh huỷ sang nhà cung cấp, nhận xác nhận huỷ, cập nhật trạng thái. Lý do huỷ lưu vĩnh viễn phục vụ kiểm toán.
6. Sau huỷ, hóa đơn ERP có thể phát hành HĐĐT mới (thay thế). Đây là một HĐĐT hoàn toàn độc lập về mặt pháp lý.

### 5.2 Ký hiệu mẫu số & ký hiệu hóa đơn

Theo Thông tư 78/2021, mỗi HĐĐT có:

- **Ký hiệu mẫu số** (1 chữ số): `1` cho HĐ giá trị gia tăng (GTGT), `2` cho HĐ bán hàng, `3`/`4`/`5`/`6` cho các loại đặc thù (xuất khẩu, bán tài sản công, tem, dự trữ quốc gia...).
- **Ký hiệu hóa đơn** (6 ký tự, ví dụ `C25TAT`): ký tự đầu `C` (có mã của cơ quan thuế) hoặc `K` (không mã); hai chữ số năm; 3 ký tự còn lại do người bán tự quy ước nhưng phải đăng ký với cơ quan thuế.

Doanh nghiệp mua sẵn các "cuộn ký hiệu" từ nhà cung cấp HĐĐT — ứng dụng không tự sinh ký hiệu mà lấy mặc định từ cấu hình provider, và cho phép người dùng ghi đè khi cần (ví dụ: một hóa đơn xuất khẩu dùng mẫu số khác).

### 5.3 Chế độ phát hành: Nháp (Draft) vs Phát hành ngay (Publish)

- **Nháp:** gửi sang cổng nhà cung cấp ở trạng thái bản nháp; kế toán vào cổng nhà cung cấp xem lại rồi mới xác nhận phát hành chính thức. Áp dụng cho doanh nghiệp muốn có bước kiểm tra cuối trước khi đẩy lên cơ quan thuế.
- **Phát hành ngay:** gửi và phát hành luôn. Áp dụng cho doanh nghiệp tin tưởng dữ liệu ERP và muốn tối ưu tốc độ.

Cấu hình ở cấp hệ thống (chế độ mặc định) nhưng có thể ghi đè khi phát hành từng hóa đơn.

### 5.4 Phát hành hàng loạt (Bulk)

Cuối tháng, kế toán có thể chọn một tập hợp hóa đơn đã duyệt và phát hành đồng loạt. Quy tắc:

- Tổng số hóa đơn mỗi lần bulk không vượt quá **giới hạn cấu hình** (mặc định 50), tránh treo hệ thống hoặc vi phạm rate limit của nhà cung cấp.
- Nếu số hóa đơn vượt một ngưỡng nhỏ (ví dụ 5), xử lý chuyển về chạy nền (background job) để không khoá trình duyệt người dùng; dưới ngưỡng thì chạy đồng bộ để thấy kết quả ngay.
- Mỗi hóa đơn trong lô xử lý độc lập: lỗi ở một hóa đơn không dừng cả lô. Kết quả trả về gồm danh sách thành công và danh sách lỗi kèm lý do.

### 5.5 Hình thức thanh toán

HĐĐT theo chuẩn TCT bắt buộc ghi "hình thức thanh toán" (tiền mặt, chuyển khoản, ...). Nếu hóa đơn ERP chưa có phương thức thanh toán (bán chịu, chưa thu), hệ thống dùng **giá trị mặc định cấu hình ở cấp hệ thống** (thường là "Chuyển khoản"). Đây là thoả hiệp thực tế — hoàn toàn hợp lệ theo quy định.

## 6. Quy tắc nghiệp vụ đầu vào (Inward)

### 6.1 Đồng bộ định kỳ

Ứng dụng chạy một tác vụ nền định kỳ với **tần suất cấu hình được** (15 phút / 1 giờ / 6 giờ / 1 ngày / 1 tuần). Mỗi lần chạy:

1. Kiểm tra đã tới thời điểm chạy kế tiếp chưa (so với lần sync gần nhất). Nếu chưa đủ khoảng thời gian, bỏ qua lần chạy này — lịch cron nội bộ có thể bắn nhiều lần nhưng không được đồng bộ dồn dập lên cổng nhà cung cấp.
2. Đảm bảo **chỉ có một tiến trình sync chạy cùng lúc** (khoá phân tán) — trường hợp scheduler lỗi và chạy trùng, lần thứ hai bỏ qua.
3. Với mỗi provider đang bật, gọi API lấy danh sách HĐĐT đầu vào trong khoảng **N ngày gần nhất** (mặc định 30 ngày, cấu hình được).
4. Phân tích từng HĐ trả về, lưu vào danh sách "HĐ đầu vào chờ xử lý" với trạng thái **Mới**.
5. Ghi nhật ký đồng bộ: thời điểm, provider, số lượng HĐ lấy về, số HĐ mới, số HĐ đã tồn tại, lỗi nếu có.
6. Cập nhật thời điểm sync gần nhất.

Người dùng cũng có thể bấm "Sync ngay" để chạy thủ công, không chịu ràng buộc về khoảng thời gian tối thiểu.

### 6.2 Xử lý HĐ đầu vào đã đồng bộ

Mỗi HĐ đầu vào có các thuộc tính: nhà cung cấp (bên bán), mã số thuế bên bán, số hóa đơn, ngày lập, ký hiệu mẫu số & ký hiệu, tổng tiền trước thuế, **thuế suất**, tiền thuế, tổng thanh toán, mã tra cứu, đường dẫn PDF.

Trạng thái xử lý: **Mới → Đã ghép (Matched) → Đã tạo HĐ mua (PI Created)**; hoặc **Bỏ qua (Ignored)**; hoặc **Lỗi (Error)**.

Logic ghép nối (matching):

- **Tìm HĐ mua đã tồn tại trong ERP** có cùng nhà cung cấp, ngày gần tương đương (trong ±N ngày, mặc định 3), và tổng tiền trong ngưỡng sai lệch (mặc định ±1%). Nếu tìm thấy duy nhất một → ghép tự động, đánh dấu "Đã ghép".
- **Nếu không tìm thấy** → kế toán mua có thể bấm "Tạo HĐ mua" để tự động dựng HĐ mua trong ERP từ dữ liệu HĐĐT đầu vào.
- **Nếu bản thân HĐ đầu vào không thuộc nghiệp vụ cần ghi sổ** (ví dụ hóa đơn dịch vụ đã ghi nhận theo cách khác) → kế toán đánh dấu "Bỏ qua" kèm ghi chú nếu cần.

### 6.3 Ánh xạ thuế suất khi tạo HĐ mua tự động

HĐĐT đầu vào có một thuế suất cụ thể (ví dụ 0%, 5%, 8%, 10%). HĐ mua trong ERP cần gắn **mẫu thuế** (tax template) phù hợp để ERP tự tính thuế GTGT đầu vào đúng tài khoản kế toán. Quy tắc:

1. Tính thuế suất thực tế từ dữ liệu HĐĐT: `tiền thuế / tổng trước thuế × 100`, làm tròn.
2. Duyệt danh sách mẫu thuế đầu vào của công ty, tìm mẫu có **thuế suất trùng khớp**.
3. Nếu có một mẫu trùng → dùng mẫu đó.
4. Nếu có nhiều mẫu cùng thuế suất → ưu tiên mẫu được đánh dấu mặc định; nếu không có mặc định, dùng mẫu đầu tiên.
5. Nếu không có mẫu nào trùng → cảnh báo người dùng "không tìm thấy mẫu thuế {X}%", dùng tạm mẫu mặc định và yêu cầu kế toán kiểm tra.
6. Nếu công ty chưa có mẫu thuế nào → dừng quy trình, yêu cầu thiết lập trước.

Sau khi tạo HĐ mua, so sánh tổng thuế mà ERP tính được với tổng thuế trên HĐĐT: nếu chênh lệch trên 1%, cảnh báo cho kế toán kiểm tra thủ công.

## 7. Vòng đời tài liệu — Tóm tắt

### Luồng đầu ra

```
Hóa đơn bán ERP (Nháp) → Duyệt (Submitted) → Phát hành HĐĐT
   → {Nháp trên cổng nhà cung cấp} hoặc {Đã phát hành}
   → Có số HĐ + mã tra cứu + PDF → Lưu nhật ký phát hành
   [Huỷ kèm lý do] → Đồng bộ huỷ → Có thể phát hành thay thế (HĐĐT mới)
```

### Luồng đầu vào

```
Scheduler → Gọi cổng nhà cung cấp → Lấy danh sách HĐ đầu vào N ngày gần nhất
   → Lưu HĐ đầu vào (Mới) → Ghi nhật ký đồng bộ
Kế toán mua xử lý:
   [Auto-match tìm được HĐ mua ERP] → Đã ghép
   [Bấm tạo HĐ mua] → Chọn mẫu thuế phù hợp → Tạo HĐ mua → PI Created
   [Bấm bỏ qua] → Ignored
   [Thuế suất bất thường hoặc lỗi API] → Error → Kế toán can thiệp
```

## 8. Quy tắc bảo mật & quyền

- Chỉ vai trò **Quản trị hệ thống** và **Kế toán trưởng** được phép gọi các thao tác phát hành, huỷ, sync. Người dùng đọc-only không thể phát hành HĐ.
- Tokens xác thực với nhà cung cấp HĐĐT được **cache tạm thời trong Redis** với thời gian hết hạn ngắn hơn TTL gốc của token (ví dụ token 1 giờ cache 58 phút, để tránh dùng token đã hết hạn). Không lưu token lâu dài vào cơ sở dữ liệu ngoài thời điểm cấu hình ban đầu.
- Mật khẩu, token, API key được lưu ở dạng **mật khẩu được mã hoá** trong DB (Password fieldtype của Frappe), không hiển thị trên giao diện sau khi lưu.
- Nhật ký lỗi không được ghi nội dung đầy đủ của payload hóa đơn (tránh lộ dữ liệu khách hàng/giá bán ra log hệ thống); chỉ ghi mã lỗi và thông báo tóm tắt.
- Mọi lần phát hành và huỷ đều có **dấu vết ai thực hiện, khi nào, kết quả gì** — phục vụ thanh tra thuế và kiểm toán nội bộ.

## 9. Edge Cases

### 9.1 HĐ đã phát hành nhưng bị huỷ phía ERP

Hóa đơn bán trong ERP đã phát hành HĐĐT, sau đó kế toán huỷ hóa đơn ERP (docstatus → 2). Quy tắc: **huỷ ERP không tự động huỷ HĐĐT** — vì HĐĐT đã có giá trị pháp lý bên ngoài. Người dùng phải chủ động bấm "Huỷ HĐĐT" kèm lý do. Nếu không huỷ HĐĐT mà đã huỷ HĐ ERP, sổ sách nội bộ và dữ liệu thuế sẽ lệch, cần nghiệp vụ đối chiếu cuối kỳ phát hiện.

### 9.2 HĐ thuế suất 0% / không chịu thuế / 5% / 8% / 10%

Cần xử lý đầy đủ các thuế suất GTGT hợp lệ của Việt Nam: 0% (xuất khẩu, dịch vụ cung ứng ra nước ngoài), 5% (nhóm thiết yếu), 8% (giảm theo nghị quyết 43/2022 — có thời hạn), 10% (thông thường), và "không chịu thuế" (dạy học, y tế...). Mỗi thuế suất cần có mẫu thuế tương ứng trong ERP để ánh xạ khi tạo HĐ mua đầu vào. Thuế suất 8% là tạm thời — chính sách có thể thay đổi, cấu hình mẫu thuế phải linh hoạt để kế toán tự cập nhật.

### 9.3 HĐ ngoại tệ

HĐĐT cho hợp đồng xuất khẩu / khách nước ngoài phát hành bằng USD/EUR kèm tỷ giá quy đổi về VND. Cơ quan thuế Việt Nam yêu cầu tiền thuế GTGT ghi bằng VND dù hóa đơn gốc bằng ngoại tệ. Ánh xạ ERP → HĐĐT phải đính kèm tỷ giá tại thời điểm phát hành.

### 9.4 HĐ có chiết khấu (thương mại / thanh toán)

Chiết khấu thương mại trên HĐĐT thể hiện ở cột "thành tiền" của từng dòng hàng (đã trừ chiết khấu). Chiết khấu thanh toán không thể hiện trên HĐĐT (là thỏa thuận riêng). Ánh xạ từ ERP phải phân biệt hai loại này — nếu ERP lưu chiết khấu dưới dạng dòng âm, cần gom lại về đơn giá đúng trước khi gửi.

### 9.5 Provider token hết hạn giữa bulk issuance

Lô 30 HĐ đang phát hành, token hết hạn sau HĐ thứ 12. Quy tắc: mỗi lần gọi API phát hiện lỗi 401/token invalid → tự động gọi lại đăng nhập, xoá cache token, thử lại đúng một lần; nếu vẫn thất bại → đánh dấu HĐ đó lỗi, chuyển tiếp sang HĐ kế. Không được dừng cả lô vì một lỗi auth tạm thời.

### 9.6 Scheduler chạy khi chưa cấu hình Settings

Ứng dụng vừa được cài, quản trị chưa vào cấu hình — tác vụ đồng bộ định kỳ vẫn bị kích hoạt bởi cron nội bộ. Quy tắc: phát hiện chưa có cấu hình → **thoát im lặng** (không báo lỗi, không ghi log lỗi), đợi đến khi quản trị cấu hình xong.

### 9.7 HĐ đầu vào trùng (duplicate)

Lần đồng bộ thứ 2 lấy lại chính HĐ đã tải về lần trước (khoảng thời gian sync chồng lấn). Quy tắc: **mã tra cứu là duy nhất** — HĐ mới có mã tra cứu trùng với HĐ đã lưu → bỏ qua, không tạo bản thứ hai. Ghi nhận trong nhật ký đồng bộ dưới dạng "số HĐ đã có sẵn".

### 9.8 HĐ đầu vào có thuế suất không khớp mẫu thuế nào

Nhà cung cấp phát hành HĐ với thuế suất 7% (sai chính sách, nhưng vẫn là dữ liệu thực). Hệ thống không tìm được mẫu thuế 7% → cảnh báo, dùng mẫu mặc định, và để kế toán quyết định giữ nguyên hay yêu cầu nhà cung cấp điều chỉnh.

### 9.9 Mã số thuế khách hàng sai định dạng

MST Việt Nam có quy tắc 10 hoặc 13 chữ số. Nếu khách hàng nhập sai (ví dụ 11 số, hoặc có chữ), HĐĐT sẽ bị cổng nhà cung cấp từ chối. Cần validate MST trước khi phát hành và trả thông báo lỗi rõ ràng để kế toán sửa trực tiếp, không để HĐ ERP rơi vào trạng thái nhập nhằng.

### 9.10 HĐ gộp (nhiều ngày hoạt động thành một HĐĐT)

Một số ngành (bán lẻ, vận tải) phát hành HĐ gộp cuối ngày/cuối tuần cho nhiều giao dịch nhỏ. Ứng dụng hỗ trợ dạng HĐ gộp thông qua một hóa đơn ERP đại diện — không tự tạo logic gộp riêng vì tính gộp đã phản ánh qua quy trình nghiệp vụ trước đó.

### 9.11 Nhà cung cấp HĐĐT ngừng dịch vụ / đổi URL

Mắt Bão / Viettel / MISA thỉnh thoảng đổi domain hoặc deprecate endpoint. Quy tắc vận hành: cấu hình URL tách riêng (không hard-code), theo dõi mã lỗi 404/DNS để phát hiện sớm, có kênh liên hệ đội triển khai để cập nhật.

### 9.12 Thay đổi chính sách mẫu số & ký hiệu giữa kỳ

Cơ quan thuế cho phép đăng ký ký hiệu HĐ mới khi hết cuộn cũ. Khi đổi ký hiệu, quản trị cập nhật ở cấu hình provider. HĐ đã phát hành giữ ký hiệu cũ; HĐ mới phát hành dùng ký hiệu mới. Ứng dụng phải cho phép chuyển trơn tru, không yêu cầu dừng hệ thống.

## 10. Tham chiếu pháp lý

- **Nghị định 123/2020/NĐ-CP** (19/10/2020) — Quy định về hóa đơn, chứng từ. Hiệu lực 01/07/2022.
- **Thông tư 78/2021/TT-BTC** (17/09/2021) — Hướng dẫn thực hiện Nghị định 123/2020, quy định chi tiết về HĐĐT: ký hiệu mẫu số, ký hiệu hóa đơn, định dạng dữ liệu, truyền nhận với cơ quan thuế.
- **Nghị quyết 43/2022/QH15** và các văn bản kế thừa — Giảm thuế GTGT từ 10% xuống 8% cho một số nhóm hàng hoá dịch vụ (có thời hạn, cần theo dõi các lần gia hạn).
- **Luật Quản lý thuế 38/2019/QH14** — Quy định chung về nghĩa vụ lập, xuất, lưu trữ hóa đơn.
- **Chuẩn định dạng XML TCT** — Cấu trúc dữ liệu HĐĐT chuẩn do Tổng cục Thuế ban hành; tất cả nhà cung cấp HĐĐT phải tuân theo.

Doanh nghiệp sử dụng ứng dụng chịu trách nhiệm tuân thủ các quy định trên. Ứng dụng `einvoice` chỉ là công cụ hỗ trợ tích hợp kỹ thuật — không thay thế trách nhiệm pháp lý của doanh nghiệp đối với tính chính xác của dữ liệu hóa đơn và việc kê khai thuế.

---

**Ghi chú maintainer:** Khi có thay đổi về nhà cung cấp HĐĐT (thêm Viettel/MISA), thay đổi chính sách thuế (thuế suất mới, thời hạn giảm thuế), hoặc phát sinh edge case mới từ thực tế vận hành, cập nhật trực tiếp vào tài liệu này trước, sau đó mới điều chỉnh spec kỹ thuật và mã nguồn.
