---
title: Khách hàng
order: 2
summary: Danh mục đối tượng phải thu (TK 131) — mã khách, mã số thuế, nhóm khách, tài khoản công nợ mặc định.
---

## Mục đích

Danh mục **Khách hàng** lưu thông tin các đối tượng bán hàng / phải thu của doanh nghiệp. Mỗi khách hàng là một **đối tượng công nợ** trên TK 131 — hệ thống theo dõi công nợ phải thu chi tiết theo từng khách trên cùng tài khoản 131, không cần mở tài khoản con cho mỗi khách.

Thông tin chính của một khách hàng:

- **Mã / Tên khách hàng**: định danh dùng trên hóa đơn, báo giá, đơn hàng.
- **Loại khách hàng**: Cá nhân hoặc Tổ chức (Company / Individual).
- **Mã số thuế (MST)**: bắt buộc với khách hàng doanh nghiệp — dùng cho hóa đơn điện tử và tờ khai thuế.
- **Nhóm khách hàng / Khu vực**: phục vụ phân loại, báo cáo, chính sách giá.
- **Loại tiền tệ mặc định / Bảng giá mặc định**: tự điền khi lập báo giá, đơn bán, hóa đơn.
- **Tài khoản công nợ mặc định** (mục "Tài khoản"): khai theo từng công ty — nếu để trống thì dùng TK phải thu mặc định của công ty (thường 131).
- **Điều khoản thanh toán**: hạn nợ mặc định để tính lịch thu tiền.

## Khi nào dùng

- **Khi có khách hàng mới:** ký hợp đồng, phát sinh bán hàng cho đối tượng chưa có trong danh mục.
- **Khi lập hóa đơn / báo giá / đơn bán:** chọn khách từ danh mục; thông tin MST, tiền tệ, bảng giá tự điền.
- **Khi cần tài khoản công nợ riêng:** một số khách đặc thù cần theo dõi trên tài khoản phải thu khác chuẩn.
- **Khi tra cứu công nợ:** xem chi tiết phải thu theo từng khách.

## Cách thực hiện

1. Mở **Khách hàng** trên menu Danh mục → danh sách khách hiện ra.
2. Bấm **+ Thêm** → nhập **Tên khách hàng**, chọn **Loại khách hàng**, **Nhóm khách hàng**, **Khu vực**.
3. Nhập **Mã số thuế (MST)** — kiểm tra kỹ với khách doanh nghiệp.
4. (Tùy chọn) đặt **Loại tiền tệ** và **Bảng giá** mặc định.
5. (Tùy chọn) tại mục **Tài khoản**, thêm dòng theo **công ty** và chọn **Tài khoản phải thu** nếu cần khác chuẩn.
6. Lưu lại → khách hàng sẵn sàng để chọn trên chứng từ.

## Định khoản tự động

Danh mục khách hàng **không tự sinh bút toán**. Nhưng tài khoản công nợ mặc định của khách quyết định định khoản phía Nợ khi bán hàng:

| Trường hợp (chứng từ) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Lập hóa đơn bán hàng (ghi nợ khách) | 131 (theo khách) | 511 + 3331 | TK 131 lấy từ tài khoản công nợ mặc định của khách |
| Thu tiền khách (phiếu thu/phiếu thanh toán) | 111 / 112 | 131 (theo khách) | Tất toán công nợ đúng đối tượng |

Bút toán chỉ phát sinh khi lập chứng từ thực tế — không phải khi khai báo khách.

## Tình huống đặc biệt & cảnh báo

- **MST sai/trùng:** mã số thuế sai làm hóa đơn điện tử bị từ chối và lệch tờ khai thuế. Với khách doanh nghiệp, nhập đủ và đúng MST.
- **Khách cá nhân (hộ gia đình):** loại Cá nhân thường không có MST; vẫn theo dõi công nợ bình thường trên TK 131.
- **Vừa là khách vừa là nhà cung cấp:** nếu một đối tác vừa mua vừa bán, khai cả ở Khách hàng và Nhà cung cấp; công nợ phải thu (131) và phải trả (331) theo dõi riêng, có thể bù trừ thủ công bằng bút toán.
- **Đa công ty:** tài khoản công nợ mặc định khai theo từng công ty — kiểm tra đúng công ty.
- **Không xóa khách đã phát sinh:** khách đã có hóa đơn / công nợ không xóa được; nếu ngừng giao dịch thì khóa (`Đã vô hiệu`).

## Báo cáo liên quan

- **Báo cáo công nợ phải thu**: tổng hợp số dư phải thu theo từng khách.
- **Sổ chi tiết công nợ phải thu**: phát sinh và số dư TK 131 theo từng khách.
- **Báo cáo tuổi nợ phải thu**: phân tích nợ theo độ tuổi để đôn đốc thu.

## FAQ

**Q: Có cần mở mỗi khách một tài khoản con dưới 131 không?**
**A:** Không. Công nợ được theo dõi chi tiết theo từng khách trên cùng TK 131. Chỉ đặt tài khoản công nợ khác khi khách thuộc nhóm cần tách riêng (ví dụ phải thu nội bộ).

**Q: Khai báo khách hàng mới có tạo phát sinh công nợ không?**
**A:** Không. Công nợ chỉ phát sinh khi lập hóa đơn bán hàng hoặc bút toán ghi nợ khách.

**Q: Khách thanh toán trước (đặt cọc) thì hạch toán ở đâu?**
**A:** Tiền nhận trước ghi vào TK người mua trả tiền trước (131 dư Có hoặc 3387 tùy chính sách); khi xuất hóa đơn thì bù trừ. Xem hướng dẫn phần Bán hàng / Tiền mặt.

**Q: Loại tiền tệ mặc định để làm gì?**
**A:** Khi khách giao dịch bằng ngoại tệ, đặt loại tiền tệ mặc định để báo giá / hóa đơn tự điền đúng tiền tệ và áp tỷ giá ngày phát sinh.
