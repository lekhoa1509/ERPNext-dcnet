---
title: Cây tài khoản
order: 2
summary: Danh mục hệ thống tài khoản kế toán (TT99/2025) — khởi tạo, sắp xếp theo cấp cha-con, đặt loại TK và loại gốc cho từng tài khoản.
---

## Mục đích

**Cây tài khoản** là danh mục toàn bộ tài khoản kế toán của công ty, tổ chức theo cấu trúc cây cha-con (TK tổng hợp → TK chi tiết). Đây là **xương sống** của toàn hệ thống: mọi bút toán, hóa đơn, phiếu thu/chi, báo cáo tài chính đều tham chiếu tới các TK trong cây này.

Tài liệu này nhấn vào khía cạnh **khởi tạo và quản trị cây TK** ở phân hệ Thiết lập (tạo TK mới, sắp xếp cấp bậc, đặt loại TK). Để biết cách tra cứu/sử dụng TK trong nghiệp vụ hằng ngày, xem phân hệ **Danh mục**.

> **Lưu ý:** Mục "Cây tài khoản" xuất hiện ở cả phân hệ **Danh mục** và **Thiết lập**. Cùng một danh mục — ở Thiết lập nhấn vào việc khởi tạo/cấu trúc, ở Danh mục nhấn vào việc tra cứu hằng ngày.

## Khi nào dùng

- **Khi mới triển khai:** khởi tạo cây TK theo hệ thống tài khoản chuẩn (TT99/2025) hoặc nhập từ file (xem [Import cây tài khoản](import-cay-tai-khoan.md)).
- **Khi cần TK chi tiết mới:** ví dụ tách 112 thành 1121-BIDV, 1122-Vietcombank theo từng ngân hàng; tách 511 theo nhóm dịch vụ.
- **Khi đặt loại TK:** gán "Loại TK" (account_type) cho TK lá (Tiền mặt, Ngân hàng, Phải thu, Phải trả, Kho, Khấu hao lũy kế...) để hệ thống định khoản và lọc đúng.
- **Khi rà soát số dư đầu kỳ:** kiểm tra cấu trúc TK trước khi nhập số dư mở sổ.

## Cách thực hiện

1. Mở **Cây tài khoản** trên menu. Màn hình hiển thị dạng cây, các TK tổng hợp (nhóm) có thể bung/thu.
2. Bấm vào một TK nhóm → **Thêm tài khoản con** để tạo TK chi tiết bên dưới.
3. Khai các trường chính của một tài khoản:
   - **Số hiệu TK** (account_number): ví dụ `1121`, `5113`. Hệ thống ghép thành tên hiển thị `1121 - Tiền gửi BIDV`.
   - **Tên tài khoản** (account_name): mô tả tiếng Việt.
   - **Là nhóm** (is_group): bật nếu là TK tổng hợp (có TK con), tắt nếu là TK lá (hạch toán trực tiếp).
   - **Loại gốc** (root_type): Tài sản / Nợ phải trả / Vốn chủ sở hữu / Thu nhập / Chi phí.
   - **Loại TK** (account_type): chỉ đặt cho TK lá — Tiền mặt, Ngân hàng, Phải thu, Phải trả, Kho, Khấu hao lũy kế, Thuế... Loại TK quyết định cách hệ thống định khoản và đặt ràng buộc.
   - **TK cha** (parent_account): TK tổng hợp chứa nó.
4. Lưu. Có thể kéo-thả để chuyển một TK sang nhánh cha khác.

### Khởi tạo nhanh bằng file

Để nạp cả cây TK một lần từ bảng tính, dùng công cụ **[Import cây tài khoản](import-cay-tai-khoan.md)** — tải mẫu, điền theo cột, tải lên.

## Định khoản tự động

Danh mục này **không tự sinh bút toán** — chỉ khai báo TK để các nghiệp vụ khác tham chiếu. Việc đặt **đúng "Loại TK"** cho TK lá là quan trọng vì nhiều chức năng định khoản tự động dựa vào nó:

| Loại TK cần đặt | Nghiệp vụ phụ thuộc |
|---|---|
| Tiền mặt | Phiếu thu/chi tiền mặt, sổ quỹ |
| Ngân hàng | Đối chiếu ngân hàng, sổ tiền gửi |
| Phải thu / Phải trả | Hóa đơn bán/mua, công nợ |
| Kho | Nhập/xuất kho, giá vốn |
| Khấu hao lũy kế / Khấu hao | Khấu hao TSCĐ (2141 / 627-641-642) |
| Thuế | Khai báo VAT, TK 3331/1331 |

## Tình huống đặc biệt & cảnh báo

- **Không xóa được TK đã phát sinh bút toán.** TK đã có số dư hoặc đã ghi sổ chỉ có thể **vô hiệu hóa** (disabled), không xóa. Đây là yêu cầu bắt buộc để bảo toàn dữ liệu kế toán.
- **TK lá phải đặt "Loại TK" phù hợp** — nếu để trống, một số chức năng (ví dụ tạo Tài khoản ngân hàng, khấu hao) sẽ báo lỗi thiếu loại TK.
- **Một TK lá ngân hàng = một Tài khoản ngân hàng.** Nếu công ty có nhiều ngân hàng, cần tạo TK con riêng (1121, 1122, 1123...) cho từng ngân hàng để khai báo được nhiều Tài khoản ngân hàng.
- **Đặt số hiệu TK theo TT99/2025.** TT99/2025 có hiệu lực 2026-01-01 thay TT200/2014: TK 242 đổi tên "Chi phí chờ phân bổ", bỏ TK 142, đổi cấu trúc một số TK con — khởi tạo cây mới nên theo TT99/2025.
- **TK nhóm không hạch toán trực tiếp.** Chỉ TK lá (is_group = tắt) mới ghi được bút toán.

## Báo cáo liên quan

- [Import cây tài khoản](import-cay-tai-khoan.md) — nạp cả cây TK từ file.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — chọn TK mặc định từ cây này cho các nghiệp vụ.
- [Năm tài chính](nam-tai-chinh.md), [Kỳ kế toán](ky-ke-toan.md) — khung thời gian khóa sổ.
- Phân hệ **Danh mục** — tra cứu TK hằng ngày.

## FAQ

**Q: Tôi nên tạo cây TK thủ công hay import từ file?**
**A:** Triển khai mới nên import (xem [Import cây tài khoản](import-cay-tai-khoan.md)) để nạp nhanh theo hệ thống tài khoản TT99/2025, sau đó chỉnh tay các TK chi tiết riêng của công ty (ngân hàng, nhóm dịch vụ).

**Q: Vì sao TK hiển thị `1121 - Tiền gửi BIDV` mà không phải chỉ `1121`?**
**A:** Tên hiển thị tự ghép từ Số hiệu TK + Tên tài khoản để dễ nhận diện. Khi định khoản, gõ số hiệu hoặc tên đều tìm ra.

**Q: Xóa nhầm không được, làm sao loại bỏ một TK không dùng?**
**A:** Nếu TK chưa phát sinh, có thể xóa; nếu đã phát sinh, hãy vô hiệu hóa (đánh dấu disabled) — TK sẽ ẩn khỏi danh sách chọn nhưng vẫn giữ lịch sử.
