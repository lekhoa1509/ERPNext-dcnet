---
title: Khoá sổ kỳ kế toán
order: 3
summary: Phiếu khoá sổ cuối năm kết chuyển kết quả vào TK lợi nhuận, kết hợp Kỳ kế toán để cấm hạch toán lùi vào kỳ đã đóng.
---

## Mục đích

**Khoá sổ kỳ kế toán** (Phiếu khoá sổ — số hiệu chứng từ PCV) là chứng từ cuối năm tài chính: hệ thống kết chuyển số dư các tài khoản lãi/lỗ về tài khoản lợi nhuận chưa phân phối, chốt kết quả năm. Kết hợp với **Kỳ kế toán** (xem [Định nghĩa kỳ kế toán](dinh-nghia-ky-ke-toan.md)), việc khoá sổ giúp **cấm hạch toán lùi ngày** — không ai được tạo/sửa/hủy chứng từ có ngày rơi vào kỳ đã đóng. Mục đích: bảo toàn số liệu phục vụ báo cáo thuế, kiểm toán, quyết toán.

## Khi nào dùng

- **Cuối năm tài chính:** sau khi đã hoàn tất bút toán kết chuyển định kỳ (911 → 4212), đối chiếu sổ và được xác nhận → lập Phiếu khoá sổ để chốt năm.
- **Cuối tháng/quý:** dùng **Kỳ kế toán** để khoá hạch toán lùi sau khi đã nộp tờ khai và đối soát số liệu.
- **Chưa nên khoá khi:** còn phiếu kế toán ở trạng thái Nháp chưa ghi sổ; chưa kết chuyển 911; đang chờ hóa đơn chậm; đang kiểm kê tài sản/hàng tồn kho.

## Cách thực hiện

**A. Cấm hạch toán lùi (Kỳ kế toán) — áp dụng tháng/quý/năm:**

1. Mở **Định nghĩa kỳ kế toán** → tạo kỳ với Ngày bắt đầu / Ngày kết thúc.
2. Trong bảng **Chứng từ đóng**, tick các loại chứng từ cần cấm (Phiếu kế toán, Hóa đơn bán/mua, Phiếu thanh toán...).
3. Lưu. Từ đó, mọi chứng từ có ngày rơi trong kỳ đều bị chặn tạo/sửa/hủy.

**B. Phiếu khoá sổ cuối năm:**

1. Mở danh sách **Khoá sổ kỳ** → **+ Thêm**.
2. Chọn **Công ty**, **Năm tài chính**, **Ngày kết thúc kỳ** (31/12/YYYY).
3. Chọn **TK kết chuyển** (Closing Account Head) — phải là tài khoản loại Nguồn vốn / Nợ phải trả (VD TK 4211 — lợi nhuận năm trước).
4. Bấm **Ghi sổ**. Hệ thống tự kết chuyển số dư lãi/lỗ vào tài khoản kết chuyển và ghi nhật ký kiểm toán.

## Định khoản tự động

Phiếu khoá sổ cuối năm SINH bút toán kết chuyển số dư các tài khoản kết quả vào tài khoản lợi nhuận:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Kết chuyển TK kết quả có số dư Có vào TK lợi nhuận | TK kết quả | TK kết chuyển (4211) | Theo dấu số dư từng tài khoản |
| Kết chuyển TK kết quả có số dư Nợ | TK kết chuyển (4211) | TK kết quả | |

> **Định nghĩa kỳ kế toán** (mục cấm hạch toán lùi) KHÔNG sinh bút toán — chỉ thiết lập rào chặn ngày. Phiếu khoá sổ cuối năm thì có sinh bút toán kết chuyển.

## Tình huống đặc biệt & cảnh báo

- **Ai được phép:** chỉ Kế toán trưởng (hoặc vai trò được miễn trừ — exempted role khai báo trên Kỳ kế toán) mới khoá/mở khoá. Kế toán viên thường không thực hiện được.
- **Hậu quả khi đã khoá (Kỳ kế toán):** sửa/tạo/hủy chứng từ có ngày trong kỳ đã đóng đều bị từ chối với thông báo "Kỳ ... đã bị khóa". Xem số liệu và xuất báo cáo vẫn được phép.
- **TK kết chuyển phải đúng loại:** Closing Account Head của Phiếu khoá sổ phải là Nguồn vốn / Nợ phải trả (Liability/Equity); chọn sai loại sẽ bị từ chối.
- **Năm trước phải đóng trước:** không thể khoá năm hiện tại nếu năm trước chưa được khoá (kiểm tra trình tự năm tài chính).
- **Phân biệt với kết chuyển định kỳ:** Phiếu khoá sổ là bước CHỐT cuối cùng; bút toán kết chuyển doanh thu/chi phí về 911 do [Phiếu kết chuyển định kỳ](phieu-ket-chuyen-dinh-ky.md) đảm nhiệm và phải làm xong trước.
- **Cần sửa sau khi đã khoá:** ưu tiên tạo chứng từ điều chỉnh ở kỳ tiếp theo; nếu bắt buộc, mở khoá kỳ theo quy trình [Mở khoá kỳ](mo-khoa-ky.md) rồi khoá lại ngay.

## Báo cáo liên quan

- [Định nghĩa kỳ kế toán](dinh-nghia-ky-ke-toan.md): thiết lập rào chặn hạch toán lùi.
- [Mở khoá kỳ kế toán đã đóng](mo-khoa-ky.md): quy trình mở khoá + nhật ký kiểm toán.
- [Phiếu kết chuyển định kỳ (911 → 4212)](phieu-ket-chuyen-dinh-ky.md): làm xong trước khi khoá sổ.
- [Bảng cân đối số phát sinh](trial-balance.md): kiểm tra số liệu cân trước khi khoá.

## FAQ

**Q: Khoá sổ và kết chuyển cuối kỳ có phải là một?**
**A:** Không. Kết chuyển (911 → 4212) là bước HẠCH TOÁN tạo bút toán xác định lãi/lỗ. Khoá sổ là bước CHỐT/CẤM hạch toán lùi (qua Kỳ kế toán) hoặc kết chuyển lợi nhuận cuối năm (qua Phiếu khoá sổ). Làm kết chuyển trước, khoá sổ sau.

**Q: Một vai trò có thể được miễn khoá sổ không?**
**A:** Có. Trên Kỳ kế toán có trường "Vai trò miễn trừ" (exempted role) — người mang vai trò đó vẫn hạch toán được vào kỳ đã đóng. Dùng thận trọng, chỉ cấp cho KTT.

**Q: Sau khi khoá, xem báo cáo kỳ cũ còn được không?**
**A:** Được. Khoá sổ chỉ chặn ghi/sửa; mọi thao tác xem và xuất báo cáo của kỳ đã đóng vẫn bình thường.

**Q: Lỡ khoá nhầm thì sao?**
**A:** Mở khoá theo quy trình [Mở khoá kỳ](mo-khoa-ky.md). Mọi thao tác mở khoá đều ghi nhật ký kiểm toán không xóa được.
