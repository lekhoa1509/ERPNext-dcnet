---
title: Danh sách CCDC
order: 1
summary: Khai báo và theo dõi từng công cụ dụng cụ — tự sinh bút toán mua và lịch phân bổ qua TK 242.
---

## Mục đích

**Danh sách CCDC** là nơi khai báo từng **công cụ dụng cụ** (máy tính, bàn ghế, dụng cụ thi công, đồ dùng giá trị nhỏ): giá trị, số kỳ phân bổ, ngày đưa vào sử dụng, người giữ và kho. Khi **Duyệt** phiếu, hệ thống tự ghi bút toán mua nhập kho + xuất dùng (đưa toàn bộ giá trị vào TK 242) và tự tạo **Lịch phân bổ CCDC** để phân bổ chi phí dần.

## Khi nào dùng

- Mua công cụ dụng cụ mới cần phân bổ chi phí dần thay vì ghi thẳng một lần vào chi phí.
- Theo dõi tình trạng từng công cụ: Mới mua → Đang sử dụng → Hết phân bổ → Đã ghi giảm.
- Gắn người giữ (custodian) và kho/địa điểm cho mỗi công cụ để phục vụ bàn giao và kiểm kê.

## Cách thực hiện

1. Bấm **Danh sách CCDC** trên menu CCDC → **+ Thêm** để tạo phiếu mới.
2. Khai báo các thông tin chính:
   - **Mã công cụ / Tên công cụ** (Item Code / Item Name).
   - **Loại CCDC** (CCDC Category), **Công ty**, **Kho/Địa điểm** (Location), **Người giữ** (Custodian).
   - **Giá trị** (Cost) — bắt buộc lớn hơn 0.
   - **Có VAT?** và **Thuế suất VAT (%)** nếu hóa đơn mua có thuế.
   - **Ngày mua** (Purchase Date), **Ngày đưa vào sử dụng** (Available For Use Date) — là ngày bắt đầu phân bổ.
   - **Thời gian sử dụng (tháng)** và **Số kỳ phân bổ** (Allocation Periods) — bắt buộc tối thiểu 1.
3. Bảng **Hạch toán** tự điền sẵn các dòng định khoản khi lưu. Có thể chỉnh tay nếu cần (tổng phải khớp giá trị + VAT, lệch quá 1 đồng sẽ báo lỗi).
4. Bấm **Lưu**, sau đó **Duyệt (Submit)** → hệ thống ghi bút toán và tạo lịch phân bổ. Trạng thái chuyển sang **Đang sử dụng**.

   ![Phiếu CCDC](_images/danh-sach-ccdc-1.png)

## Định khoản tự động

Khi **Duyệt** phiếu, hệ thống ghi gộp bút toán mua + xuất dùng (lấy theo bảng Hạch toán; nếu trống thì tự dựng theo mẫu mặc định):

| Trường hợp | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Mua nhập kho | 153 | 331 | Tạo công nợ nhà cung cấp |
| Xuất dùng (đưa vào phân bổ) | 242 | 153 | TK 153 trở về 0, dồn giá trị vào TK 242 |
| VAT đầu vào (nếu có VAT) | 1331 | 331 | Theo thuế suất khai báo |

Sau khi duyệt, các kỳ phân bổ tiếp theo (Nợ 6423 / Có 242) do **Lịch phân bổ CCDC** thực hiện — xem [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md).

## Tình huống đặc biệt & cảnh báo

- **TK 153 là tài khoản trung gian:** gộp hai bút toán (mua + xuất dùng) làm TK 153 về 0, toàn bộ giá trị nằm ở TK 242. Thiết kế này tránh số dư âm TK 153 trên báo cáo tình hình tài chính (B01).
- **Số kỳ phân bổ:** ví dụ giá trị 12.000.000 chia 12 kỳ → mỗi kỳ 1.000.000; kỳ cuối nhận phần chênh lệch làm tròn để khớp tổng.
- **Hủy phiếu (Cancel):** hệ thống tự hủy bút toán mua đã ghi, trạng thái quay về **Mới mua**.
- **Sửa định khoản tay:** chỉnh trong bảng Hạch toán nhưng tổng các dòng phải khớp giá trị + VAT (lệch quá 1 đồng bị chặn lưu).
- **Tài khoản chi phí (Expense Account) và TK 242 (Prepayment Account):** có thể đặt riêng trên phiếu; nếu để trống hệ thống dùng 6423 (chi phí) và 242 (chờ phân bổ) mặc định cho công ty.

## Báo cáo liên quan

- [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md): theo dõi và thực hiện phân bổ từng kỳ.
- [Ghi giảm CCDC](ghi-giam-ccdc.md): xử lý khi công cụ hỏng/mất/thanh lý.
- [Sổ S22-DN](so-s22-dn.md): sổ theo dõi TSCĐ + CCDC.

## FAQ

**Q: Tại sao có hai dòng định khoản 153 và 242 khi mua một công cụ?**
**A:** Vì có hai sự kiện kinh tế: nhập kho (Dr 153 / Cr 331) và xuất dùng để phân bổ (Dr 242 / Cr 153). Gộp lại làm TK 153 chỉ là trung gian (số dư 0), giá trị nằm ở TK 242 — đúng chuẩn VAS và tránh số dư âm trên báo cáo.

**Q: Lịch phân bổ có tự tạo sau khi duyệt không?**
**A:** Có. Duyệt phiếu sẽ tự sinh đủ số kỳ phân bổ đã khai báo.

**Q: Công cụ mua mà chưa dùng ngay thì sao?**
**A:** Đặt **Ngày đưa vào sử dụng** đúng ngày bắt đầu phân bổ — lịch phân bổ sẽ tính kỳ đầu từ ngày này.

**Q: Đổi tài khoản chi phí phân bổ từ 6423 sang 627/641 được không?**
**A:** Được. Đặt Expense Account trên phiếu, hoặc chỉnh từng dòng trong [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md).
