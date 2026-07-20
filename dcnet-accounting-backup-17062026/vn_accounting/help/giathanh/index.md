---
section: Giá thành
title: Tổng quan Giá thành
summary: Phân hệ Giá thành — phân bổ chi phí mua hàng vào giá vốn, chi phí trả trước (242), giá thành công trình xây lắp và kết chuyển 627 → 154 → 632 theo TT99/2025.
---

## Mục đích

Phân hệ **Giá thành** quản lý việc tập hợp và phân bổ chi phí để xác định đúng **giá vốn / giá thành** theo VAS TT99/2025, gồm ba nhóm nghiệp vụ:

1. **Phân bổ chi phí mua hàng** (landed cost): cộng phụ phí vận chuyển, bảo hiểm, thuế NK... vào giá trị hàng tồn kho (152/156), tách TK 1561/1562 và kết chuyển phụ phí vào giá vốn cuối kỳ.
2. **Chi phí trả trước (TK 242)**: phân bổ dần chi phí chờ phân bổ ra nhiều kỳ (Dr 6xx / Cr 242).
3. **Giá thành công trình xây lắp**: gom chi phí theo giai đoạn cho từng công trình, kết chuyển TK 627 → 154 → 632, xuất hóa đơn theo đợt nghiệm thu.

## Khi nào dùng

- Mua hàng có phụ phí (vận chuyển, hải quan, bảo hiểm) cần cộng vào giá vốn.
- Có chi phí trả trước cần phân bổ dần (thuê nhà, bảo hiểm, công cụ dụng cụ).
- Doanh nghiệp xây lắp / thi công cần tính giá thành công trình theo giai đoạn.
- Cuối kỳ: kết chuyển chi phí sản xuất chung, phân bổ phụ phí vào giá vốn.

## Cách thực hiện

Cấu trúc menu **Giá thành** gồm các mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Phân bổ chi phí mua hàng | Chứng từ | Cộng phụ phí vào giá vốn hàng tồn (152/156), tách 1561/1562 |
| 2 | Chi phí chờ phân bổ | Báo cáo | Liệt kê chi phí mua hàng treo TK 1388 chưa phân bổ |
| 3 | Lịch phân bổ CP trả trước (242) | Chứng từ | Phân bổ dần chi phí trả trước qua nhiều kỳ |
| 4 | Dự án — Giá thành | Chứng từ | Hồ sơ tính giá thành công trình theo giai đoạn |
| 5 | Tiến độ xuất hóa đơn | Báo cáo | Theo dõi mốc xuất hóa đơn từng giai đoạn công trình |
| 6 | Kết chuyển CP SXC (627 → 154) | Chứng từ | Phân bổ chi phí gián tiếp ra công trình, kết chuyển 627→154 |
| 7 | Phân bổ phụ phí vào giá vốn (cuối kỳ) | Chứng từ | Kết chuyển phụ phí (1562) của hàng đã bán về 1561 |
| 8 | Cấu hình phân bổ chi phí mua hàng | Cài đặt | Khai loại phụ phí, TK mặc định, tách TK kho 1562 |

> Mục **Phân bổ phụ phí vào giá vốn (cuối kỳ)** xuất hiện ở nhiều vị trí trong menu nhưng là cùng một chức năng — chỉ cần dùng một nơi.

### Quy trình điển hình

**A. Mua hàng có phụ phí:**
1. Nhập phiếu nhập kho / hóa đơn mua hàng.
2. **Phân bổ chi phí mua hàng** → cộng phụ phí vào giá vốn (tự tách 1562 nếu đã cấu hình).
3. Cuối kỳ: **Phân bổ phụ phí vào giá vốn (cuối kỳ)** để kết chuyển phụ phí của hàng đã bán (1562 → 1561).

**B. Chi phí trả trước:**
1. Ghi nhận Dr 242 (thủ công hoặc từ hóa đơn mua).
2. **Lịch phân bổ CP trả trước (242)** → sinh lịch → ghi sổ → phân bổ từng kỳ (Dr 6xx / Cr 242).

**C. Giá thành công trình xây lắp:**
1. Tạo **Dự án — Giá thành** + khai giai đoạn.
2. Nhập chi phí tag công trình hằng ngày.
3. Cuối tháng: pin chi phí vào giai đoạn (Pivot Tool); **Kết chuyển CP SXC (627→154)** cho chi phí gián tiếp.
4. Nghiệm thu: tạo hóa đơn từ giai đoạn → ghi sổ (sinh Dr 632 / Cr 154).
5. Hoàn tất: đóng công trình, chốt 154.

### Liên kết tới các bài hướng dẫn chi tiết

- **Phân bổ chi phí mua hàng**: [cơ bản](lcv-co-ban.md), [hàng nhập khẩu](lcv-nhap-khau.md), [cấu hình](lcv-allocation-settings.md), [chi phí chờ phân bổ](landed-cost-pending-allocation.md), [phân bổ phụ phí cuối kỳ](inventory-cost-reallocation.md).
- **Chi phí trả trước**: [Lịch phân bổ CP trả trước (242)](vn-deferred-expense-schedule.md).
- **Giá thành công trình**: [Dự án — Giá thành](project-costing-tinh-gia-thanh.md), [6 phương pháp markup](project-costing-stage-markup.md), [Pivot Tool](project-costing-pivot-tool.md), [Kết chuyển CP SXC](project-costing-allocation-run.md), [Phân bổ lương + khấu hao](project-costing-luong-khau-hao.md), [Đóng công trình](project-costing-close.md), [Tiến độ xuất hóa đơn](project-invoicing-progress.md), [Setup dự án xây lắp](du-an-xay-lap.md), [Tính giá thành sản xuất](giathanh-sanxuat.md).

## Định khoản tự động

| Nghiệp vụ | TK Nợ | TK Có |
|---|---|---|
| Cộng phụ phí mua hàng vào giá vốn | 1561 (sau đó bù 1562/1561) | 331 / 111 / 112 |
| Phân bổ chi phí trả trước từng kỳ | 6xx | 242 |
| Kết chuyển chi phí gián tiếp vào công trình | 154 | 627 / 622 / 6424 |
| Giá vốn công trình khi xuất hóa đơn giai đoạn | 632 | 154 |
| Write-off chi phí dư khi đóng công trình | 642 / 632 | 154 |

Các báo cáo (Chi phí chờ phân bổ, Tiến độ xuất hóa đơn) chỉ tra cứu, không sinh bút toán.

## Tình huống đặc biệt & cảnh báo

- **TT99/2025 bỏ TK 142** — mọi chi phí trả trước dùng TK 242 ("Chi phí chờ phân bổ").
- **TK 156 tách 1561 (giá mua) / 1562 (chi phí thu mua)** — cần cấu hình TK 1562 và bật bút toán bù tại [Cấu hình phân bổ chi phí mua hàng](lcv-allocation-settings.md).
- **Doanh nghiệp xây lắp bắt buộc TK 627** cho chi phí sản xuất chung, kết chuyển 627 → 154 (vượt công suất bình thường ghi thẳng 632).
- **Cuối kỳ TK 627 phải = 0** và **công trình hoàn thành TK 154 phải = 0** — hệ thống cảnh báo nếu còn số dư.

## Báo cáo liên quan

- [Sổ Cái] các TK 156, 242, 154, 627, 632.
- Báo cáo kết quả kinh doanh: so sánh doanh thu 511 với giá vốn 632.

## FAQ

**Q: Vì sao một mục lại xuất hiện nhiều lần trong menu?**
**A:** Mục "Phân bổ phụ phí vào giá vốn (cuối kỳ)" được đặt ở vài vị trí cho tiện truy cập — tất cả mở cùng một chức năng. Dùng bất kỳ nơi nào.

**Q: Phân hệ này có tự động xuất hóa đơn / khóa sổ không?**
**A:** Không. Phân hệ sinh bút toán nháp hoặc đã ghi sổ tùy chức năng; việc khóa sổ kỳ do chứng từ khóa sổ riêng đảm nhiệm. Các báo cáo chỉ để tra cứu.
