---
title: Danh sách hợp đồng
order: 1
summary: Hợp đồng dịch vụ DCNET — cam kết bán hàng, tự sinh lịch xuất hóa đơn định kỳ khi duyệt, và tự lập hóa đơn trả lại khi hủy giữa kỳ.
---

## Mục đích

**Danh sách hợp đồng** là nơi quản lý hợp đồng dịch vụ với khách hàng: thông tin khách, gói dịch vụ, kỳ hạn, phí khởi tạo, ngày nghiệm thu. Khi hợp đồng được duyệt (ghi sổ), hệ thống **tự sinh lịch xuất hóa đơn** — mỗi kỳ thu tiền một dòng — làm cơ sở để xuất hóa đơn định kỳ và theo dõi công nợ.

Hợp đồng phân loại theo bản chất từng dòng dịch vụ:
- **Dịch vụ định kỳ** (P2P, MPLS, ILL, FTTH DN, FTTH HGD, IT Managed): thu phí hằng tháng/quý theo kỳ.
- **Hàng bán đứt / thi công** (VTTB, Thi công): bán một lần. Hệ thống lập đơn bán hàng ngầm để theo dõi xuất kho.
- **Phí khởi tạo:** thu một lần khi nghiệm thu.
- **Hỗn hợp:** vừa định kỳ vừa bán đứt.

## Khi nào dùng

- Ký hợp đồng mới với khách hàng.
- Sửa đổi / gia hạn hợp đồng (lập bản sửa đổi — bản cũ chuyển trạng thái "Đã sửa đổi").
- Tạm ngừng / khôi phục / hủy hợp đồng giữa kỳ.
- Tra cứu cam kết, lịch hóa đơn, và các giao dịch liên quan (hóa đơn, phiếu thu, bút toán) của một hợp đồng.

## Cách thực hiện

1. Mở **Danh sách hợp đồng** → "+ Thêm".
2. Chọn khách hàng — hệ thống tự điền địa chỉ, người đại diện, điện thoại, tài khoản ngân hàng từ dữ liệu chủ.
3. Nhập các dòng dịch vụ: tên gói, loại dòng (dịch vụ định kỳ / hàng bán đứt / phí khởi tạo), số lượng, đơn giá. Đơn giá phải lớn hơn 0 và số lượng ≥ 1.
4. Nhập kỳ hạn gói (số tháng), hình thức thanh toán (hằng tháng / quý...), ngày nghiệm thu.
5. Bấm **Ghi sổ** (duyệt) — bắt buộc có ngày nghiệm thu trước khi ghi sổ. Hệ thống sẽ:
   - Sinh **lịch xuất hóa đơn** cho từng kỳ (chia tỷ lệ theo ngày nếu kỳ đầu lệch lịch dương).
   - Lập **đơn bán hàng ngầm** cho dòng hàng bán đứt.
   - Đồng bộ thông tin khách (mã số thuế, địa chỉ, liên hệ, tài khoản ngân hàng) về dữ liệu chủ.
6. Nút **Tạm ngừng / Khôi phục** để chuyển trạng thái khi khách tạm dừng dịch vụ.

## Định khoản tự động

Lập và duyệt hợp đồng **không trực tiếp sinh bút toán**. Hợp đồng chỉ tạo ra **lịch xuất hóa đơn**; doanh thu và thuế chỉ được ghi nhận khi hóa đơn bán hàng từng kỳ được ghi sổ (xem [Hóa đơn cần ghi sổ](hoa-don-can-ghi-so.md)).

Khi **hủy hợp đồng giữa kỳ**, hệ thống xử lý theo trạng thái từng kỳ trong lịch:

| Trạng thái kỳ | Hành động khi hủy | Bút toán |
|---|---|---|
| Dự kiến (chưa xuất hóa đơn) | Chuyển sang "Đã hủy" | Không |
| Đã xuất hóa đơn / Quá hạn | Tự lập **hóa đơn trả lại** (credit note) | Giảm trừ doanh thu + thuế của kỳ đó |
| Đã thu tiền | Chỉ cảnh báo — không tự hoàn tiền | Kế toán lập phiếu chi hoàn tiền thủ công nếu cần |

## Tình huống đặc biệt & cảnh báo

- **Bắt buộc ngày nghiệm thu trước khi ghi sổ:** không thể duyệt hợp đồng thiếu ngày nghiệm thu (vì lịch hóa đơn tính từ ngày này).
- **Hàng bán đứt phải gắn mặt hàng kho:** dòng "hàng bán đứt" thuộc dịch vụ VTTB phải liên kết một mặt hàng để lập đơn bán hàng ngầm (theo dõi xuất kho).
- **Sửa đổi hợp đồng:** khi tạo bản sửa đổi, bản cũ tự chuyển sang trạng thái "Đã sửa đổi" (phân biệt với hủy thuần túy); các kỳ tương lai của bản cũ được hủy.
- **Phí khởi tạo tự tính:** nếu có dòng "Phí khởi tạo", hệ thống tính tổng các dòng đó làm phí khởi tạo, bỏ qua giá trị nhập tay.
- **Đồng bộ một chiều, nhẹ tay:** đồng bộ thông tin khách chỉ ghi đè khi trường trên hợp đồng có giá trị — không xóa dữ liệu chủ đang có.

## Báo cáo liên quan

- [Hóa đơn cần ghi sổ](hoa-don-can-ghi-so.md): hóa đơn nháp sinh từ lịch hợp đồng.
- [Công nợ theo hợp đồng](cong-no-theo-hop-dong.md) và [Kỳ thu tiền quá hạn](ky-thu-tien-qua-han.md): theo dõi kỳ chưa thu.
- [Thu tiền theo hợp đồng](thu-tien-theo-hop-dong.md): dòng tiền thực thu.
- [Phương án kinh doanh](phuong-an-kinh-doanh.md): PAKD gắn hợp đồng để tính hoa hồng.

## FAQ

**Q: Vì sao sau khi ghi sổ hợp đồng lại có sẵn nhiều dòng trong lịch xuất hóa đơn?**
**A:** Hệ thống tự chia kỳ hạn gói thành các kỳ thu tiền (theo hình thức thanh toán) và tạo một dòng/kỳ. Đến hạn từng kỳ, hệ thống sinh hóa đơn nháp tương ứng.

**Q: Khách tạm ngừng dịch vụ rồi quay lại — làm sao?**
**A:** Dùng nút **Tạm ngừng** rồi **Khôi phục**. Không cần hủy + lập lại hợp đồng.

**Q: Tôi hủy hợp đồng nhưng kỳ đã thu tiền — hệ thống có tự hoàn tiền không?**
**A:** Không. Hệ thống chỉ cảnh báo và ghi chú; kế toán tự lập phiếu chi hoàn tiền cho khách nếu cần.
