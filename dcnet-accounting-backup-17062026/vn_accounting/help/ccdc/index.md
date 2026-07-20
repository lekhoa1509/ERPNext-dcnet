---
section: CCDC
title: Tổng quan CCDC (Công cụ dụng cụ)
summary: Giới thiệu phân hệ Công cụ dụng cụ — danh sách, lịch phân bổ qua TK 242, ghi giảm, bàn giao, kiểm kê và sổ S22-DN.
---

## Mục đích

Phân hệ **CCDC (Công cụ dụng cụ)** quản lý toàn bộ vòng đời của công cụ, dụng cụ có giá trị nhỏ (không đủ tiêu chuẩn ghi nhận tài sản cố định): từ lúc **mua về nhập kho**, **đưa vào sử dụng và phân bổ dần** chi phí qua TK 242 (chi phí chờ phân bổ), đến **ghi giảm khi hỏng/mất/thanh lý**. Phân hệ cũng dùng chung nghiệp vụ **bàn giao** và **kiểm kê** với phân hệ TSCĐ, và cung cấp **sổ S22-DN** theo dõi chi tiết TSCĐ và CCDC theo TT99/2025.

## Khi nào dùng

- Khi mua công cụ dụng cụ (máy tính, bàn ghế, dụng cụ thi công, đồ dùng văn phòng giá trị nhỏ) cần phân bổ chi phí dần thay vì ghi thẳng vào chi phí một lần.
- Theo dõi tình trạng phân bổ từng kỳ của mỗi công cụ dụng cụ.
- Khi công cụ dụng cụ hỏng, mất, hết sử dụng cần ghi giảm và đẩy số dư còn lại vào chi phí.
- Khi điều chuyển công cụ giữa người giữ / phòng ban / kho.
- Định kỳ kiểm kê thực tế công cụ dụng cụ đối chiếu sổ sách.

## Cách thực hiện

Cấu trúc phân hệ **CCDC** gồm các mục sau:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Danh sách CCDC | Danh sách | Khai báo và theo dõi từng công cụ dụng cụ (TK 153/242) |
| 2 | Lịch phân bổ CCDC | Danh sách | Lịch phân bổ chi phí dần qua TK 242 → 627/641/6423 |
| 3 | Ghi giảm CCDC | Danh sách | Xử lý hỏng/mất/thanh lý, xóa số dư TK 242 |
| 4 | Bàn giao CCDC | Danh sách | Điều chuyển công cụ giữa người giữ / phòng ban / kho (dùng chung với TSCĐ) |
| 5 | Kiểm kê CCDC | Danh sách | Biên bản kiểm kê thực tế (dùng chung với TSCĐ) |
| 6 | Sổ S22-DN | Báo cáo | Sổ theo dõi chi tiết TSCĐ và CCDC theo TT99/2025 |

> **Lưu ý:** **Lịch phân bổ CCDC (242→6423)** và **Lịch phân bổ CCDC** là cùng một chức năng (cùng một danh sách). Phần "242→6423" chỉ nhấn mạnh đường định khoản mặc định khi phân bổ vào chi phí công cụ dụng cụ. Xem chi tiết tại [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md).

### Quy trình điển hình

1. **Mua công cụ dụng cụ:** tạo phiếu trong **Danh sách CCDC** → khai báo giá trị, số kỳ phân bổ, ngày bắt đầu dùng → bấm **Duyệt (Submit)**. Hệ thống tự sinh bút toán mua và tự tạo **Lịch phân bổ CCDC**.
2. **Phân bổ hằng tháng:** hệ thống tự động phân bổ từng kỳ theo lịch (chạy ngầm hằng ngày); hoặc mở **Lịch phân bổ CCDC** bấm nút phân bổ cho từng kỳ. Mỗi kỳ sinh một bút toán Nợ 6423 / Có 242.
3. **Bàn giao khi đổi người giữ:** lập **Bàn giao CCDC** chọn phạm vi CCDC, từ người giữ → người nhận.
4. **Kiểm kê định kỳ:** lập **Kiểm kê CCDC**, tải danh sách công cụ theo kho, đối chiếu thực tế, ghi nhận mất/hỏng.
5. **Ghi giảm khi thanh lý:** lập **Ghi giảm CCDC** khi công cụ hỏng/mất/hết dùng → xóa số dư còn lại trên TK 242 vào chi phí.
6. **Tra cứu:** mở **Sổ S22-DN** để xem toàn cảnh TSCĐ + CCDC theo kho và tình trạng.

### Liên kết tới các bài hướng dẫn chi tiết

- **Khai báo & vòng đời**: [Danh sách CCDC](danh-sach-ccdc.md), [Lịch phân bổ CCDC](lich-phan-bo-ccdc.md), [Ghi giảm CCDC](ghi-giam-ccdc.md).
- **Quản lý hiện vật (dùng chung với TSCĐ)**: [Bàn giao CCDC](ban-giao-ccdc.md), [Kiểm kê CCDC](kiem-ke-ccdc.md).
- **Báo cáo**: [Sổ S22-DN](so-s22-dn.md).

## Định khoản tự động (tổng quát)

Phân hệ CCDC **tự sinh bút toán** ở các bước chính (theo TT99/2025):

| Bước | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Mua nhập kho | 153 | 331 | Nợ phải trả nhà cung cấp |
| Xuất dùng (đưa vào phân bổ) | 242 | 153 | Chuyển sang chi phí chờ phân bổ |
| VAT đầu vào (nếu có) | 1331 | 331 | Theo thuế suất khai báo |
| Phân bổ từng kỳ | 6423 | 242 | Có thể đổi sang 627/641 theo bộ phận |
| Ghi giảm — xóa số dư 242 | 6423 | 242 | Phần chưa phân bổ hết đẩy vào chi phí |
| Ghi giảm — bồi thường (nếu có) | 1388 | 711 | Cá nhân/đơn vị bồi thường |

Bút toán mua + xuất dùng được gộp ngay khi **Duyệt** phiếu trong Danh sách CCDC, làm TK 153 chỉ là tài khoản trung gian (số dư về 0), toàn bộ giá trị nằm ở TK 242.

## Tình huống đặc biệt & cảnh báo

- **Phân biệt với TSCĐ:** công cụ dụng cụ giá trị nhỏ, thời gian dùng ngắn → phân bổ qua TK 242. Tài sản đủ tiêu chuẩn (TK 211, khấu hao 2141) thuộc phân hệ TSCĐ.
- **TK 242 đổi tên theo TT99/2025:** từ "Chi phí trả trước" (TT200) thành **"Chi phí chờ phân bổ"**. Đã bỏ TK 142.
- **Bàn giao & Kiểm kê dùng chung với TSCĐ:** mỗi phiếu có trường **Phạm vi (TSCĐ / CCDC)** — chọn đúng CCDC để chỉ thao tác trên công cụ dụng cụ. Cùng một biểu mẫu phục vụ cả hai phân hệ.
- **Sổ S22-DN hiện chưa hiển thị dòng CCDC:** xem [Sổ S22-DN](so-s22-dn.md) phần cảnh báo — có lỗi kỹ thuật khiến phần CCDC bị bỏ qua, cần khắc phục ở bản cập nhật.
- **Ghi giảm chỉ làm một lần:** công cụ đã ở trạng thái "Đã ghi giảm" không thể ghi giảm lại.

## Báo cáo liên quan

- **Sổ S22-DN**: theo dõi chi tiết TSCĐ và CCDC.
- **Sổ Cái** TK 242, 153, 6423: kiểm tra số dư và phát sinh phân bổ.
- **Bảng cân đối số phát sinh**: kiểm tra số dư TK 242 cuối kỳ.

## FAQ

**Q: Khi nào ghi là công cụ dụng cụ (CCDC) thay vì tài sản cố định (TSCĐ)?**
**A:** Khi giá trị nhỏ hơn ngưỡng ghi nhận TSCĐ và/hoặc thời gian sử dụng ngắn. CCDC phân bổ chi phí dần qua TK 242; TSCĐ trích khấu hao qua TK 211/2141.

**Q: Sau khi duyệt phiếu CCDC, lịch phân bổ có tự tạo không?**
**A:** Có. Khi bấm Duyệt trong Danh sách CCDC, hệ thống tự sinh bút toán mua + xuất dùng và tự tạo Lịch phân bổ CCDC với đủ số kỳ đã khai báo.

**Q: Mỗi kỳ phân bổ vào tài khoản chi phí nào?**
**A:** Mặc định Nợ TK 6423 (chi phí công cụ dụng cụ) / Có TK 242. Có thể đổi TK Nợ thành 627 (bộ phận sản xuất) hoặc 641 (bộ phận bán hàng) ở từng dòng lịch hoặc trên phiếu CCDC.

**Q: Bàn giao và kiểm kê CCDC có khác TSCĐ không?**
**A:** Dùng chung biểu mẫu, chỉ khác ở trường **Phạm vi**. Chọn "CCDC" để thao tác trên công cụ dụng cụ.
