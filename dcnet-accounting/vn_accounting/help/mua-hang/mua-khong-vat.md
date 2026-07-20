---
title: Mua không VAT
order: 10
summary: Báo cáo các hóa đơn mua hàng chưa nhận được hóa đơn VAT điện tử từ NCC — kèm phòng ban đề xuất để đôn đốc lấy hóa đơn.
---

## Mục đích

Báo cáo **Mua không VAT** (FB-2026-00840) giúp kế toán trưởng và bộ phận mua hàng phát hiện các **hóa đơn mua hàng** đã ghi sổ nhưng CHƯA nhận được hóa đơn VAT điện tử từ nhà cung cấp (chưa có liên kết tới phiếu Hóa đơn điện tử đầu vào). Mục đích:

- **Đôn đốc NCC giao hóa đơn** trước hạn kê khai thuế GTGT.
- **Quản trị nội bộ**: biết phòng ban nào đề xuất mua mà chưa hoàn thiện chứng từ.
- **Giải trình thanh tra**: cơ quan thuế thường hỏi "tại sao chi nhưng không có hóa đơn VAT" — báo cáo này giúp giải trình theo từng phòng ban.

## Khi nào dùng

- **Cuối tháng**: kiểm tra trước hạn nộp tờ khai thuế GTGT (ngày 20 tháng sau).
- **Cuối quý**: rà soát tổng hợp, đôn đốc NCC chốt hóa đơn cho cả quý.
- **Trước thanh tra thuế**: xuất danh sách theo phòng ban + NCC để đính kèm giải trình.

## Cách thực hiện

1. Bấm **Mua không VAT** trên menu Mua hàng → báo cáo mở (mặc định 3 tháng gần nhất).
2. Chọn **Công ty** (bắt buộc), **Chế độ xem**, **Từ ngày / Đến ngày** (bắt buộc).
3. (Tùy chọn) lọc thêm **Phòng ban đề xuất** (chọn nhiều) và **Nhà cung cấp**.
4. Bấm **Refresh** → bảng liệt kê các hóa đơn mua hàng theo chế độ đã chọn, sắp xếp ngày mới nhất trên cùng.
5. Bấm vào **Số phiếu** để mở hóa đơn mua hàng; bấm **EInvoice Inward** (ở chế độ "Có HĐ VAT") để mở phiếu hóa đơn điện tử đầu vào.
6. (Tùy chọn) bấm nút **Tạo hóa đơn mua hàng mới** ở góc trên để lập hóa đơn mới.

### Hai chế độ xem

| Chế độ | Hiển thị | Dùng để |
|---|---|---|
| **Không có HĐ VAT** (mặc định) | Hóa đơn mua đã ghi sổ, KHÔNG có liên kết hóa đơn điện tử đầu vào | Đôn đốc NCC, giải trình thanh tra |
| **Có HĐ VAT** | Hóa đơn mua đã ghi sổ, ĐÃ có ít nhất 1 liên kết hóa đơn điện tử | Đối chiếu ngược danh sách "đã có hóa đơn" |

### Các cột báo cáo

- **Số phiếu**: liên kết mở hóa đơn mua hàng.
- **Ngày**: ngày ghi sổ hóa đơn.
- **Nhà cung cấp**: NCC.
- **Tổng tiền**: tổng giá trị hóa đơn.
- **Phòng ban đề xuất**: phòng ban đề nghị mua (FB-2026-00616).
- **Mã HĐ VAT**: mã hóa đơn VAT (chỉ có giá trị ở chế độ "Có HĐ VAT").
- **EInvoice Inward**: liên kết mở phiếu hóa đơn điện tử đầu vào.
- **Trạng thái**: trạng thái hóa đơn mua hàng.

Dòng cuối cùng là dòng tổng: Σ Tổng tiền của các hóa đơn lọt bộ lọc, kèm số lượng hóa đơn.

## Định khoản tự động

Báo cáo này **không sinh bút toán — chỉ tra cứu**. Nó lọc dữ liệu từ các hóa đơn mua hàng đã ghi sổ và kiểm tra liên kết tới phiếu hóa đơn điện tử đầu vào (không tác động Sổ Cái).

## Tình huống đặc biệt & cảnh báo

- **Chỉ tính hóa đơn đã ghi sổ:** chỉ lấy hóa đơn mua hàng đã duyệt (đã ghi sổ); hóa đơn nháp không hiện.
- **"Không có HĐ VAT" ≠ "không có thuế trong mẫu thuế":** báo cáo chỉ kiểm tra LIÊN KẾT tới phiếu hóa đơn điện tử đầu vào. Một hóa đơn mua có mẫu thuế VAT 10% nhưng chưa nhận được hóa đơn điện tử từ NCC vẫn lọt vào danh sách "Không có HĐ VAT".
- **Phòng ban đề xuất** tự điền khi tạo hóa đơn mua hàng từ đơn mua hàng (FB-2026-00616). Nếu hóa đơn lập trực tiếp không qua đơn mua, kế toán có thể chọn tay phòng ban ở field "Phòng ban đề xuất".
- **Kê khai thuế GTGT đầu vào:** chỉ được khấu trừ khi đã có hóa đơn hợp lệ. Các khoản trong danh sách "Không có HĐ VAT" chưa đủ điều kiện khấu trừ cho đến khi nhận được hóa đơn.

## Báo cáo liên quan

- [Hóa đơn mua hàng](hoa-don-mua-hang.md) — chứng từ gốc của từng dòng báo cáo.
- [BC mua hàng](bc-mua-hang.md) / [BC theo mặt hàng](bc-theo-mat-hang.md) — phân tích chi tiêu mua.
- [Công nợ phải trả](cong-no-phai-tra.md) — theo dõi nghĩa vụ thanh toán cho NCC.

## FAQ

**Q: Báo cáo này có làm thay đổi sổ sách không?**
**A:** Không. Đây là báo cáo tra cứu, chỉ lọc các hóa đơn mua hàng theo tình trạng có/không liên kết hóa đơn điện tử đầu vào. Không sinh bút toán.

**Q: Vì sao một hóa đơn có thuế VAT vẫn nằm trong "Không có HĐ VAT"?**
**A:** Vì báo cáo kiểm tra liên kết tới phiếu hóa đơn điện tử đầu vào, không kiểm tra mẫu thuế. Hóa đơn đã có thuế trong hệ thống nhưng chưa nhận được hóa đơn điện tử từ NCC vẫn bị liệt kê để đôn đốc lấy hóa đơn.

**Q: Làm sao để hóa đơn ra khỏi danh sách "Không có HĐ VAT"?**
**A:** Khi nhận được và liên kết hóa đơn điện tử đầu vào của NCC với hóa đơn mua hàng tương ứng, hóa đơn sẽ chuyển sang chế độ "Có HĐ VAT".

**Q: Phòng ban đề xuất để làm gì?**
**A:** Để biết bộ phận nào đề nghị mua nhưng chưa hoàn thiện chứng từ, phục vụ đôn đốc nội bộ và giải trình thanh tra theo từng phòng ban.
