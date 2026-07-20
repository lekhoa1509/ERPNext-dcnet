---
title: Phiếu xuất kho
order: 10
summary: Giao hàng hóa cho khách — ghi giảm tồn kho và ghi nhận giá vốn (Nợ 632 / Có 156).
---

## Mục đích

**Phiếu xuất kho** ghi nhận việc giao hàng hóa cho khách hàng — **ghi giảm tồn kho** và **ghi nhận giá vốn hàng bán**. Khi ghi sổ, hệ thống tạo bút toán Nợ TK 632 / Có TK 156 (theo phương pháp xuất kho của mặt hàng) và cập nhật sổ kho. Phiếu xuất kho thường lập trước hoặc song song với hóa đơn bán hàng.

## Khi nào dùng

- Giao hàng hóa cho khách (có theo dõi tồn kho).
- Tách thời điểm giao hàng và thời điểm xuất hóa đơn (giao trước, hóa đơn sau).
- Giao hàng nhiều lần cho một đơn bán hàng.
- Công trình xây lắp: xuất vật tư và tập hợp chi phí theo công trình (TK 154).

## Cách thực hiện

1. Mở **Phiếu xuất kho** → "+ Thêm" (hoặc từ đơn bán hàng: "Tạo > Phiếu xuất kho").
2. Chọn **Khách hàng**, **kho xuất**, **ngày ghi sổ**.
3. Kiểm tra các dòng mặt hàng + số lượng + kho nguồn.
4. (Công trình) Chọn **Loại chi phí** (Trực tiếp / Phân bổ) và **TK tập hợp chi phí công trình** (mặc định TK 154) nếu xuất vật tư cho công trình.
5. Lưu và ghi sổ → giảm tồn kho + sinh bút toán giá vốn.
6. Bước tiếp theo: từ phiếu xuất kho → **"Tạo > Hóa đơn bán hàng"** để ghi nhận doanh thu.

## Định khoản tự động

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Xuất kho bán hàng hóa | 632 | 156 | Giá vốn theo phương pháp xuất kho (FIFO/bình quân) |
| Xuất thành phẩm bán | 632 | 155 | Nếu là thành phẩm sản xuất |
| Xuất vật tư cho công trình (trực tiếp) | 154 | 156 | Tập hợp chi phí theo công trình |
| Xuất vật tư chung (phân bổ) | 627 → 154 | 156 | Chi phí chung phân bổ qua đợt phân bổ |

> **Công trình xây lắp (TT99/2025):** với loại chi phí "Phân bổ" hoặc khi chọn TK tập hợp công trình, hệ thống tự tạo **bút toán bù** sau khi ghi sổ để chuyển chi phí về đúng TK công trình (mặc định TK 154). Kế toán trưởng có thể đổi TK tập hợp cho từng chứng từ.

## Tình huống đặc biệt & cảnh báo

- **Giá vốn theo phương pháp xuất kho:** giá vốn (TK 632) tính theo phương pháp khai báo trên mặt hàng (bình quân gia quyền / nhập trước xuất trước). Đảm bảo có giá nhập kho trước đó, nếu không giá vốn = 0.
- **Tồn kho âm:** nếu xuất quá tồn, hệ thống có thể chặn (tùy cấu hình cho phép tồn âm). Kiểm tra tồn kho trước khi xuất.
- **Hàng theo lô/số seri:** mặt hàng quản lý theo lô/số seri cần chọn đúng lô khi xuất — hệ thống kiểm tra tồn theo từng lô.
- **TK tập hợp chi phí công trình:** chỉ dùng cho doanh nghiệp xây lắp/thi công; doanh nghiệp thương mại thuần bỏ trống (xuất bán bình thường Nợ 632 / Có 156).
- **Hủy phiếu xuất kho:** hủy sẽ hoàn lại tồn kho; nếu đã có hóa đơn gắn vào, xử lý hóa đơn trước.

## Báo cáo liên quan

- [Hóa đơn bán hàng](hoa-don-ban-hang.md): ghi nhận doanh thu sau khi giao hàng.
- [Đơn bán hàng](don-ban-hang.md): nguồn của phiếu xuất kho.
- **Sổ Cái** (phân hệ Tổng hợp): theo dõi phát sinh TK 632, 156, 154.

## FAQ

**Q: Phải lập phiếu xuất kho rồi mới lập hóa đơn?**
**A:** Không bắt buộc. Có thể lập hóa đơn bán hàng có bật cập nhật tồn kho để vừa ghi doanh thu vừa ghi giá vốn cùng lúc. Tách phiếu xuất kho hữu ích khi giao hàng và xuất hóa đơn ở hai thời điểm khác nhau.

**Q: Bán dịch vụ (không có hàng tồn) có cần phiếu xuất kho không?**
**A:** Không. Dịch vụ không quản lý tồn kho — lập thẳng hóa đơn bán hàng.

**Q: Giá vốn bị 0 — vì sao?**
**A:** Mặt hàng chưa có giá nhập kho (chưa từng nhập hoặc tồn = 0). Cần có nghiệp vụ nhập kho/định giá trước khi xuất bán.
