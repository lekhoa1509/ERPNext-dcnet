---
title: Lịch phân bổ CCDC
order: 2
summary: Lịch phân bổ chi phí công cụ dụng cụ dần qua TK 242 → 6423/627/641, tự động hằng tháng hoặc bấm tay từng kỳ.
---

## Mục đích

**Lịch phân bổ CCDC** ghi nhận kế hoạch phân bổ chi phí của một công cụ dụng cụ thành nhiều kỳ (thường theo tháng). Mỗi kỳ phân bổ sinh một bút toán Nợ TK 6423 (chi phí công cụ dụng cụ) / Có TK 242 (chi phí chờ phân bổ). Lịch được hệ thống **tự tạo** khi duyệt phiếu trong [Danh sách CCDC](danh-sach-ccdc.md) — không cần lập tay.

> Mục **Lịch phân bổ CCDC (242→6423)** trên menu là cùng một chức năng này; ký hiệu "242→6423" chỉ nhấn mạnh đường định khoản mặc định.

## Khi nào dùng

- Theo dõi tiến độ phân bổ từng công cụ dụng cụ (đã phân bổ bao nhiêu kỳ / tổng số kỳ).
- Phân bổ thủ công một kỳ ngay khi cần (không chờ lịch chạy ngầm).
- Điều chỉnh tài khoản chi phí Nợ cho từng kỳ (6423 → 627 nếu là bộ phận sản xuất, 641 nếu là bộ phận bán hàng).

## Cách thực hiện

1. Bấm **Lịch phân bổ CCDC** trên menu CCDC → chọn lịch của công cụ cần xem.
2. Xem các thông tin: **Công cụ** (CCDC Item), **Ngày bắt đầu**, **Tổng giá trị**, **Số kỳ**, **Tần suất** (Monthly), **Trạng thái** (Active / Completed / Cancelled).
3. Bảng các kỳ phân bổ hiển thị: số kỳ, ngày bắt đầu kỳ, số tiền phân bổ, trạng thái (Pending / Posted / Cancelled), bút toán đã ghi.
4. **Phân bổ một kỳ thủ công:** bấm nút phân bổ kỳ tương ứng → hệ thống ghi bút toán kỳ đó, cập nhật trạng thái kỳ thành **Posted**. Thao tác này **không trùng lặp** — kỳ đã ghi sẽ không ghi lại.
5. **Phân bổ tự động:** hệ thống chạy ngầm hằng ngày, tự ghi mọi kỳ có ngày bắt đầu ≤ hôm nay mà còn ở trạng thái Pending.

   ![Lịch phân bổ CCDC](_images/lich-phan-bo-ccdc-1.png)

## Định khoản tự động

Mỗi kỳ phân bổ sinh một bút toán:

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Phân bổ chi phí công cụ dụng cụ (mặc định) | 6423 | 242 | Diễn giải "Phân bổ CCDC kỳ N" |
| Bộ phận sản xuất | 627 | 242 | Đặt TK Nợ = 627 trên dòng lịch |
| Bộ phận bán hàng | 641 | 242 | Đặt TK Nợ = 641 trên dòng lịch |

TK Nợ lấy theo thứ tự ưu tiên: TK đặt riêng trên từng dòng kỳ → tài khoản chi phí của phiếu CCDC → mặc định 6423. TK Có ưu tiên tương tự: dòng kỳ → TK 242 của phiếu → mặc định 242.

## Tình huống đặc biệt & cảnh báo

- **Hoàn tất tự động:** khi tất cả các kỳ đã Posted, lịch chuyển sang **Completed** và công cụ chuyển sang trạng thái **Hết phân bổ**.
- **Ghi giảm giữa chừng:** nếu công cụ bị ghi giảm trước khi phân bổ hết, các kỳ còn Pending sẽ bị **hủy (Cancelled)** và số dư còn lại trên TK 242 được đẩy vào chi phí qua phiếu [Ghi giảm CCDC](ghi-giam-ccdc.md).
- **Không ghi trùng:** nút phân bổ và lịch chạy ngầm đều kiểm tra trạng thái — kỳ đã có bút toán sẽ trả về "đã ghi" thay vì tạo bút toán mới.
- **Lỗi phân bổ ngầm:** nếu một kỳ lỗi khi chạy tự động, hệ thống ghi nhật ký lỗi và tiếp tục các kỳ khác (không dừng toàn bộ).
- **Kỳ cuối làm tròn:** số tiền kỳ cuối nhận phần chênh lệch để tổng các kỳ khớp đúng giá trị công cụ.

## Báo cáo liên quan

- [Danh sách CCDC](danh-sach-ccdc.md): nơi tạo công cụ và phát sinh lịch phân bổ.
- [Ghi giảm CCDC](ghi-giam-ccdc.md): xử lý phần chưa phân bổ hết khi thanh lý.
- **Sổ Cái** TK 242 và 6423: kiểm tra phát sinh phân bổ từng kỳ.

## FAQ

**Q: Có phải tự lập lịch phân bổ không?**
**A:** Không. Lịch tự tạo khi duyệt phiếu trong Danh sách CCDC, với đủ số kỳ đã khai báo.

**Q: Nếu quên/bỏ lỡ kỳ phân bổ thì sao?**
**A:** Hệ thống chạy ngầm hằng ngày sẽ tự ghi mọi kỳ đến hạn còn Pending. Có thể bấm phân bổ thủ công bất cứ lúc nào.

**Q: Đổi tài khoản chi phí Nợ cho riêng một kỳ được không?**
**A:** Được. Đặt TK Nợ trên dòng kỳ tương ứng trước khi phân bổ; hệ thống ưu tiên giá trị trên dòng.

**Q: Phân bổ rồi có bị ghi trùng nếu bấm lại không?**
**A:** Không. Kỳ đã ghi (có bút toán) sẽ trả kết quả "đã ghi" và không tạo bút toán mới.
