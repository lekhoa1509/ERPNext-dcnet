---
title: Nhà cung cấp
order: 3
summary: Danh mục đối tượng phải trả (TK 331) — mã NCC, mã số thuế, nhóm, tài khoản công nợ và khấu trừ thuế.
---

## Mục đích

Danh mục **Nhà cung cấp** lưu thông tin các đối tượng mua hàng / phải trả của doanh nghiệp. Mỗi nhà cung cấp là một **đối tượng công nợ** trên TK 331 — hệ thống theo dõi công nợ phải trả chi tiết theo từng nhà cung cấp trên cùng tài khoản 331.

Thông tin chính của một nhà cung cấp:

- **Mã / Tên nhà cung cấp**: định danh dùng trên đơn mua, hóa đơn mua.
- **Loại nhà cung cấp**: Cá nhân hoặc Tổ chức.
- **Mã số thuế (MST)**: dùng đối chiếu hóa đơn đầu vào và kê khai thuế GTGT.
- **Nhóm nhà cung cấp**: phân loại phục vụ báo cáo.
- **Diện khấu trừ thuế** (nếu áp dụng): cấu hình khấu trừ thuế TNCN cho nhà cung cấp là cá nhân / hộ kinh doanh.
- **Loại tiền tệ mặc định / Điều khoản thanh toán**: tự điền khi lập đơn mua, hóa đơn mua.
- **Tài khoản công nợ mặc định** (mục "Tài khoản"): khai theo từng công ty — nếu trống dùng TK phải trả mặc định của công ty (thường 331).

## Khi nào dùng

- **Khi có nhà cung cấp mới:** phát sinh mua hàng / dịch vụ từ đối tác chưa có trong danh mục.
- **Khi lập đơn mua / hóa đơn mua:** chọn nhà cung cấp; MST, tiền tệ, điều khoản thanh toán tự điền.
- **Khi cần khấu trừ thuế:** gán diện khấu trừ cho nhà cung cấp cá nhân / hộ kinh doanh.
- **Khi tra cứu công nợ phải trả:** xem chi tiết phải trả theo từng nhà cung cấp.

## Cách thực hiện

1. Mở **Nhà cung cấp** trên menu Danh mục → danh sách hiện ra.
2. Bấm **+ Thêm** → nhập **Tên nhà cung cấp**, chọn **Loại** và **Nhóm nhà cung cấp**.
3. Nhập **Mã số thuế (MST)** — đối chiếu với hóa đơn đầu vào.
4. (Tùy chọn) chọn **Diện khấu trừ thuế** nếu nhà cung cấp thuộc diện khấu trừ TNCN.
5. (Tùy chọn) đặt **Loại tiền tệ** và **Điều khoản thanh toán** mặc định.
6. (Tùy chọn) tại mục **Tài khoản**, thêm dòng theo **công ty** và chọn **Tài khoản phải trả** nếu cần khác chuẩn.
7. Lưu lại.

## Định khoản tự động

Danh mục nhà cung cấp **không tự sinh bút toán**. Tài khoản công nợ mặc định quyết định định khoản phía Có khi mua hàng:

| Trường hợp (chứng từ) | TK Nợ | TK Có | Ghi chú |
|---|---|---|---|
| Lập hóa đơn mua hàng (ghi nợ NCC) | 152/153/156/6xx + 1331 | 331 (theo NCC) | TK 331 lấy từ tài khoản công nợ mặc định của NCC |
| Trả tiền NCC (phiếu chi/phiếu thanh toán) | 331 (theo NCC) | 111 / 112 | Tất toán công nợ đúng đối tượng |

Bút toán chỉ phát sinh khi lập chứng từ thực tế.

## Tình huống đặc biệt & cảnh báo

- **MST sai/trùng:** mã số thuế sai làm lệch bảng kê thuế GTGT đầu vào và rủi ro không được khấu trừ. Nhập đúng MST.
- **Khấu trừ thuế TNCN:** với nhà cung cấp cá nhân / hộ kinh doanh thuộc diện khấu trừ, đặt diện khấu trừ để hóa đơn mua tự tính phần thuế giữ lại — tránh sót nghĩa vụ kê khai.
- **Vừa là NCC vừa là khách:** khai ở cả hai danh mục; công nợ phải trả (331) và phải thu (131) theo dõi riêng.
- **Đa công ty:** tài khoản công nợ khai theo từng công ty.
- **Không xóa NCC đã phát sinh:** nhà cung cấp đã có hóa đơn / công nợ không xóa được; nếu ngừng giao dịch thì khóa.

## Báo cáo liên quan

- **Báo cáo công nợ phải trả**: tổng hợp số dư phải trả theo từng nhà cung cấp.
- **Sổ chi tiết công nợ phải trả**: phát sinh và số dư TK 331 theo từng nhà cung cấp.
- **Báo cáo tuổi nợ phải trả**: phân tích nợ theo độ tuổi để lập kế hoạch chi.

## FAQ

**Q: Có cần mở mỗi nhà cung cấp một tài khoản con dưới 331 không?**
**A:** Không. Công nợ được theo dõi chi tiết theo từng nhà cung cấp trên cùng TK 331.

**Q: Trả tiền trước cho nhà cung cấp (ứng trước) ghi ở đâu?**
**A:** Tiền ứng trước ghi TK trả trước cho người bán (331 dư Nợ hoặc 1388/tài khoản tạm ứng tùy chính sách); khi nhận hóa đơn thì bù trừ.

**Q: Diện khấu trừ thuế dùng khi nào?**
**A:** Khi mua dịch vụ / hàng từ cá nhân, hộ kinh doanh thuộc diện phải khấu trừ thuế TNCN tại nguồn. Gán diện khấu trừ để hệ thống tự tính phần thuế giữ lại trên hóa đơn mua.

**Q: Khai báo nhà cung cấp mới có tạo công nợ không?**
**A:** Không. Công nợ chỉ phát sinh khi lập hóa đơn mua hàng hoặc bút toán ghi có nhà cung cấp.
