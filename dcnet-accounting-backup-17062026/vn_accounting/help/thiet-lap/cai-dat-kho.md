---
title: Cài đặt kho
order: 9
summary: Cấu hình quy tắc kho — phương pháp tính giá xuất, cho phép tồn âm, đặt TK kho mặc định và các ràng buộc nhập/xuất.
---

## Mục đích

**Cài đặt kho** khai báo các quy tắc chung cho nghiệp vụ kho: phương pháp tính giá xuất kho, cho phép tồn kho âm hay không, TK kho/chênh lệch mặc định, hành vi tạo phiếu nhập xuất, cập nhật giá vốn... Các quy tắc này áp dụng cho mọi phiếu nhập/xuất kho và ảnh hưởng trực tiếp tới giá vốn (TK 632) và giá trị tồn kho (TK 152/153/155/156).

## Khi nào dùng

- **Khi mới triển khai:** chọn phương pháp tính giá xuất kho và các quy tắc tồn kho phù hợp với chính sách công ty (theo TT99/2025).
- **Khi cần cho phép tồn âm tạm thời:** ví dụ nhập xuất chéo ngày trong giai đoạn chuyển đổi dữ liệu.
- **Khi đặt TK mặc định cho chênh lệch kiểm kê / điều chỉnh kho.**

## Cách thực hiện

1. Mở **Cài đặt kho** trên menu Thiết lập.
2. Rà soát và đặt các nhóm cấu hình chính:
   - **Phương pháp tính giá xuất kho:** Bình quân gia quyền (Moving Average) hoặc Nhập trước Xuất trước (FIFO).
   - **Cho phép tồn kho âm:** bật/tắt. Mặc định nên **tắt** để tránh xuất quá tồn.
   - **TK chênh lệch / điều chỉnh kho mặc định** (dùng khi kiểm kê, điều chỉnh).
   - Quy tắc cập nhật kho, tự tạo phiếu, đơn vị tính mặc định...
3. Lưu — áp dụng cho phiếu nhập/xuất kế tiếp.

## Định khoản tự động

Cài đặt kho **không tự sinh bút toán**, nhưng **quyết định cách hệ thống định khoản** khi nhập/xuất kho:

| Cấu hình | Ảnh hưởng định khoản |
|---|---|
| Phương pháp tính giá xuất kho | Quyết định trị giá xuất → giá vốn TK 632 và giá trị tồn TK 15x |
| TK chênh lệch/điều chỉnh kho | TK ghi chênh lệch khi kiểm kê/điều chỉnh (thường 632 hoặc TK chênh lệch) |
| Cho phép tồn âm | Cho/không cho ghi sổ phiếu xuất khi tồn không đủ |

> Nghiệp vụ kho cụ thể (nhập kho, xuất kho, kiểm kê) sinh bút toán ở phân hệ **Kho** — Cài đặt kho chỉ đặt quy tắc nền.

## Tình huống đặc biệt & cảnh báo

- **Đổi phương pháp tính giá xuất kho khi đã có phát sinh là rủi ro.** Nên chốt phương pháp ngay từ đầu kỳ; đổi giữa kỳ có thể làm lệch giá vốn đã ghi.
- **"Cho phép tồn âm" chỉ nên bật tạm** trong giai đoạn nhập dữ liệu chuyển đổi (xuất trước, nhập sau theo ngày), rồi tắt lại khi vận hành bình thường — tránh xuất vượt tồn ngoài ý muốn.
- **TK kho mặc định lấy từ thiết lập kho/công ty** — đảm bảo TK kho có "Loại TK" = Kho trong [Cây tài khoản](cay-tai-khoan.md), nếu không nghiệp vụ kho báo lỗi.
- **Mặt hàng đánh số lô/serial** có ràng buộc tồn theo lô riêng, không nới lỏng bởi "cho phép tồn âm" cấp kho.

## Báo cáo liên quan

- [Cây tài khoản](cay-tai-khoan.md) — đặt "Loại TK = Kho" cho TK 15x.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — TK giá vốn công trình (632) cho xây lắp.
- Phân hệ **Kho** — nhập/xuất/kiểm kê và các sổ kho.

## FAQ

**Q: Nên chọn Bình quân gia quyền hay FIFO?**
**A:** Tùy chính sách kế toán đã đăng ký của công ty. Bình quân gia quyền phổ biến và đơn giản; FIFO phù hợp khi giá biến động và cần khớp lô. Chốt một phương pháp từ đầu kỳ.

**Q: Vì sao tôi không xuất được kho dù còn hàng trên giấy?**
**A:** Có thể "Cho phép tồn âm" đang tắt và tồn trên hệ thống chưa khớp thực tế (chưa nhập đủ phiếu nhập). Nhập bổ sung phiếu nhập đúng ngày, hoặc kiểm kê điều chỉnh.

**Q: Cài đặt kho có sinh bút toán không?**
**A:** Không. Nó chỉ đặt quy tắc; bút toán phát sinh từ các phiếu nhập/xuất/kiểm kê ở phân hệ Kho theo quy tắc này.
