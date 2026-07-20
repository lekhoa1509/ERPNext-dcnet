---
title: Sổ chi tiết kho
order: 9
summary: Sổ chi tiết từng lần nhập/xuất của một mặt hàng theo kho, kèm số dư lũy kế.
---

## Mục đích

**Sổ chi tiết kho** (sổ kho) liệt kê **từng lần nhập/xuất** của hàng tồn kho theo thứ tự thời gian, kèm **số lượng** và **giá trị** mỗi lần, **số dư lũy kế** sau mỗi giao dịch, và **chứng từ gốc** tạo ra biến động đó. Đây là báo cáo truy vết chi tiết nhất của phân hệ Kho — dùng để giải thích vì sao tồn cuối của một mặt hàng lại ra con số như vậy.

## Khi nào dùng

- Truy vết: kiểm tra chính xác từng lần nhập/xuất của một mặt hàng tại một kho.
- Đối chiếu: khi BC nhập xuất tồn báo số bất thường, mở Sổ chi tiết kho để tìm phiếu gây lệch.
- Kiểm tra giá vốn: xem đơn giá xuất từng lần theo phương pháp tính giá.
- Tìm phiếu theo số chứng từ, theo lô, theo dự án.

## Cách thực hiện

1. Bấm **Sổ chi tiết kho** trên menu Kho → báo cáo mở.
   ![Sổ chi tiết kho](_images/so-chi-tiet-kho-1.png)
2. Nhập bộ lọc:
   - **Công ty**, **Từ ngày / Đến ngày**.
   - **Kho**, **Mặt hàng**, **Nhóm hàng** (tùy chọn).
   - **Số lô**, **Thương hiệu**, **Số chứng từ**, **Dự án** (lọc thu hẹp).
3. Bấm **Refresh** → bảng hiển thị theo thứ tự thời gian: **Ngày**, **Mặt hàng**, **Kho**, **SL nhập/xuất** (vào dương, ra âm), **Đơn giá**, **Giá trị**, **SL lũy kế**, **Giá trị lũy kế**, **Loại chứng từ**, **Số chứng từ**.
4. Bấm vào dòng để mở chứng từ gốc (phiếu nhập xuất kho, phiếu xuất kho, hóa đơn…).

## Định khoản tự động

**Không tự định khoản** — đây là sổ tra cứu, phản ánh biến động đã ghi nhận từ các chứng từ kho, không sinh bút toán mới.

## Tình huống đặc biệt & cảnh báo

- **Thứ tự thời gian quyết định giá vốn:** sổ sắp theo ngày; phiếu nhập/xuất sai ngày làm đơn giá xuất và số dư lũy kế sai.
- **Số dư âm giữa kỳ:** nếu số dư lũy kế xuống âm tại một thời điểm → có lần xuất trước khi nhập; rà lại ngày chứng từ.
- **Lọc theo lô/dự án:** dùng khi cần truy vết hẹp; bỏ trống để xem toàn bộ.
- **Nhiều dòng cùng phiếu:** một phiếu nhập xuất kho có thể tạo nhiều dòng trên sổ (nhiều mặt hàng/kho).
- **Báo cáo nền tảng ERP:** báo cáo chuẩn của hệ thống, mô tả theo nghiệp vụ VN.

## Báo cáo liên quan

- **BC nhập xuất tồn:** số tổng hợp; Sổ chi tiết kho giải thích chi tiết tạo nên số đó.
- **Số lô / Số seri:** lọc sổ theo lô để xem lịch sử của lô/seri.
- **Nhập xuất kho / Kiểm kê kho:** chứng từ gốc mở từ dòng sổ.

## FAQ

**Q: Sổ chi tiết kho khác BC nhập xuất tồn ở điểm nào?**
**A:** BC nhập xuất tồn là số **tổng hợp** (tồn đầu – nhập – xuất – tồn cuối). Sổ chi tiết kho là **từng dòng** giao dịch với số dư lũy kế — giải thích chi tiết cho con số tổng hợp.

**Q: Mở chứng từ gốc từ sổ được không?**
**A:** Được. Bấm vào dòng để mở phiếu/hóa đơn tạo ra biến động; hệ thống giữ menu ở phân hệ hiện hành.

**Q: Vì sao đơn giá xuất khác đơn giá nhập?**
**A:** Đơn giá xuất tính theo phương pháp tính giá đã chọn (bình quân gia quyền, nhập trước xuất trước) chứ không bằng đúng đơn giá nhập từng lần.

**Q: Lọc theo số lô như thế nào?**
**A:** Điền ô **Số lô** để chỉ xem các lần nhập/xuất của lô đó.
