---
title: Gói sản phẩm
order: 11
summary: Khai báo combo/bộ sản phẩm bán theo gói gồm nhiều mặt hàng thành phần.
---

## Mục đích

**Gói sản phẩm** (combo/bộ sản phẩm) cho phép bán một mặt hàng "gói" đại diện cho nhiều mặt hàng thành phần. Khi bán gói, hệ thống vẫn xuất kho và ghi giá vốn theo **từng mặt hàng thành phần thực tế**, còn khách hàng và hóa đơn thể hiện ở mức gói. Phù hợp khi bán theo combo (ví dụ: bộ thiết bị mạng = modem + dây + đầu nối), khuyến mãi theo gói, hoặc bán bộ phụ kiện.

## Khi nào dùng

- Bán theo combo/bộ: một mã bán đại diện cho nhiều linh kiện.
- Khuyến mãi đóng gói nhiều mặt hàng bán chung một giá.
- Quản lý tồn ở mức thành phần nhưng bán/báo giá ở mức gói.

## Cách thực hiện

1. Trước hết, khai mặt hàng "gói" trong **Danh mục** với điều kiện: **KHÔNG phải hàng tồn kho** và **KHÔNG phải tài sản cố định** (gói chỉ là vỏ bọc bán hàng, không giữ tồn riêng).
2. Bấm **Gói sản phẩm** trên menu Kho → danh sách gói sản phẩm mở.
3. Bấm **+ Thêm** → chọn **Mặt hàng gói** (mã mới) và thêm bảng **mặt hàng thành phần** kèm **số lượng** từng thành phần.
   ![Gói sản phẩm](_images/goi-san-pham-1.png)
4. Mỗi thành phần phải có **số lượng dương** và **không được là một gói khác** (không lồng gói).
5. **Lưu**. Khi bán mặt hàng gói trên đơn/hóa đơn, hệ thống tự bung các thành phần để xuất kho.

## Định khoản tự động

**Bản thân gói sản phẩm không tự định khoản** — nó chỉ là khai báo cấu trúc. Bút toán phát sinh khi bán/xuất gói, và được ghi theo **từng mặt hàng thành phần**:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Ghi nhận doanh thu bán gói | 131/111/112 | 511 + 3331 | Doanh thu ghi ở mức gói (theo hóa đơn bán hàng) |
| Xuất kho giá vốn các thành phần | 632 | 155/156 | Xuất kho và tính giá vốn theo từng thành phần thực tế |

Vì mặt hàng gói không phải hàng tồn kho, gói không sinh bút toán tồn kho; chỉ các thành phần mới làm giảm tồn và ghi giá vốn.

## Tình huống đặc biệt & cảnh báo

- **Mặt hàng gói không giữ tồn:** gói bắt buộc là mặt hàng phi tồn kho và phi tài sản. Khai gói cho một mặt hàng tồn kho sẽ bị chặn.
- **Không lồng gói:** thành phần không được là một gói sản phẩm khác.
- **Số lượng thành phần phải dương:** mỗi dòng thành phần cần số lượng lớn hơn 0.
- **Không xóa được gói đang dùng:** nếu gói đã xuất hiện trên chứng từ đã ghi sổ (đơn/hóa đơn/phiếu kho đã duyệt), phải hủy các chứng từ đó trước khi xóa gói.
- **Đủ tồn thành phần:** bán gói yêu cầu đủ tồn của tất cả thành phần; thiếu một thành phần sẽ chặn xuất kho.
- **Đổi cấu trúc gói:** sửa thành phần không hồi tố các chứng từ đã bán trước đó.

## Báo cáo liên quan

- **BC nhập xuất tồn / Sổ chi tiết kho:** theo dõi tồn và giá vốn của các mặt hàng thành phần.
- **Nhập xuất kho:** chứng từ kho liên quan đến thành phần.

## FAQ

**Q: Gói sản phẩm có giữ tồn kho riêng không?**
**A:** Không. Gói là mặt hàng phi tồn kho. Tồn và giá vốn được quản lý ở từng mặt hàng thành phần.

**Q: Bán gói thì xuất kho thế nào?**
**A:** Hệ thống tự bung gói thành các thành phần và xuất kho từng thành phần theo số lượng đã khai trong gói.

**Q: Có lồng một gói vào gói khác được không?**
**A:** Không. Thành phần của gói không được là một gói sản phẩm khác.

**Q: Vì sao không xóa được gói?**
**A:** Vì gói đã được dùng trên chứng từ đã ghi sổ (đơn bán, hóa đơn, phiếu kho). Cần hủy các chứng từ đó trước, rồi mới xóa được gói.
