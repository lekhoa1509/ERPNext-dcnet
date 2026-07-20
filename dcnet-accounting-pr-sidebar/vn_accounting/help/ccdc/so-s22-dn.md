---
title: Sổ S22-DN
order: 6
summary: Sổ theo dõi chi tiết TSCĐ và CCDC theo TT99/2025 — danh sách tài sản và công cụ kèm vị trí, người giữ, giá trị, tình trạng.
---

## Mục đích

**Sổ S22-DN** là sổ theo dõi chi tiết **tài sản cố định (TSCĐ)** và **công cụ dụng cụ (CCDC)** theo mẫu sổ kế toán của TT99/2025. Sổ liệt kê từng tài sản/công cụ kèm vị trí, người giữ, giá trị sổ sách và tình trạng — phục vụ tra cứu, đối chiếu và in báo cáo theo dõi.

## Khi nào dùng

- Xem toàn cảnh danh mục TSCĐ + CCDC của công ty theo từng kho/địa điểm.
- Đối chiếu vị trí và người giữ trước/sau khi bàn giao, kiểm kê.
- In sổ theo dõi cuối kỳ theo mẫu TT99/2025.

## Cách thực hiện

1. Bấm **Sổ S22-DN** trên menu CCDC (hoặc TSCĐ) → báo cáo mở.
2. Nhập bộ lọc: **Công ty** (Company) và **Kho/Địa điểm** (Location) — đều tùy chọn.
3. Bấm **Refresh** → bảng hiển thị các dòng với cột:

   | Cột | Ý nghĩa |
   |---|---|
   | Loại | TSCĐ hoặc CCDC |
   | Tên | Mã tài sản / công cụ |
   | Vị trí | Kho/Địa điểm đang đặt |
   | Người giữ | Nhân viên quản lý |
   | Giá trị sổ sách | Nguyên giá / giá trị công cụ |
   | Tình trạng | Trạng thái hiện tại |

   ![Sổ S22-DN](_images/so-s22-dn-1.png)

## Định khoản tự động

Sổ S22-DN **không tự định khoản** — đây là báo cáo tra cứu, lấy số liệu từ danh mục TSCĐ và CCDC đã duyệt.

## Tình huống đặc biệt & cảnh báo

- **Cảnh báo: hiện sổ chưa hiển thị dòng CCDC.** Trên dữ liệu hiện tại, sổ chỉ liệt kê các dòng TSCĐ; phần công cụ dụng cụ bị bỏ qua do một lỗi kỹ thuật trong điều kiện kiểm tra bảng dữ liệu CCDC. Trong khi chờ khắc phục, để tra cứu công cụ dụng cụ hãy dùng trực tiếp [Danh sách CCDC](danh-sach-ccdc.md). Sau khi bản cập nhật khắc phục lỗi, sổ sẽ hiển thị đủ cả TSCĐ và CCDC.
- **Lọc theo vị trí:** nếu công cụ chưa gán Kho/Địa điểm thì lọc theo vị trí sẽ không hiện công cụ đó — hãy gán vị trí trên phiếu trong Danh sách CCDC.
- **Chỉ hiển thị bản đã duyệt:** sổ chỉ lấy tài sản/công cụ ở trạng thái đã ghi sổ (đã duyệt). Bản nháp không xuất hiện.
- **Giá trị sổ sách:** với TSCĐ là tổng nguyên giá; với CCDC là giá trị mua ban đầu (không phản ánh số đã phân bổ).

## Báo cáo liên quan

- [Danh sách CCDC](danh-sach-ccdc.md): chi tiết từng công cụ dụng cụ và trạng thái phân bổ.
- [Bàn giao CCDC](ban-giao-ccdc.md), [Kiểm kê CCDC](kiem-ke-ccdc.md): cập nhật vị trí và người giữ phản ánh trên sổ.
- **Sổ Cái** TK 242, 211: kiểm tra số dư và phân bổ/khấu hao.

## FAQ

**Q: Tại sao sổ chỉ thấy TSCĐ mà không thấy CCDC?**
**A:** Đây là lỗi kỹ thuật ở điều kiện kiểm tra bảng dữ liệu CCDC khiến phần CCDC bị bỏ qua. Trong khi chờ khắc phục, tra cứu công cụ dụng cụ trực tiếp ở Danh sách CCDC.

**Q: Giá trị sổ sách của CCDC là giá trị nào?**
**A:** Là giá trị mua ban đầu của công cụ; không trừ phần đã phân bổ. Muốn xem số đã/còn phân bổ, vào Lịch phân bổ CCDC.

**Q: Vì sao một công cụ không xuất hiện trên sổ?**
**A:** Có thể công cụ chưa được duyệt (còn bản nháp), hoặc chưa gán vị trí trong khi đang lọc theo vị trí — kiểm tra lại trên phiếu trong Danh sách CCDC.
