---
title: Kỳ kế toán
order: 5
summary: Khai báo và khóa sổ theo từng kỳ kế toán (tháng/quý) — chặn ghi/sửa chứng từ vào kỳ đã chốt để bảo toàn số liệu đã báo cáo.
---

## Mục đích

**Kỳ kế toán** cho phép định nghĩa một khoảng thời gian (tháng, quý...) và **khóa sổ** kỳ đó: khi đã chốt, hệ thống chặn việc ghi mới hoặc sửa/hủy chứng từ rơi vào kỳ — bảo toàn số liệu đã quyết toán/đã nộp báo cáo.

> **Lưu ý:** Mục "Kỳ kế toán" xuất hiện ở cả phân hệ **Tổng hợp** và **Thiết lập**. Cùng một danh mục — ở Thiết lập nhấn vào việc thiết lập khóa kỳ ban đầu; ở Tổng hợp nhấn vào nghiệp vụ chốt sổ định kỳ.

## Khi nào dùng

- **Cuối mỗi tháng/quý:** sau khi đối chiếu xong, chốt kỳ để không ai sửa số liệu đã báo cáo.
- **Sau khi nộp tờ khai thuế / báo cáo tài chính:** khóa kỳ tương ứng.
- **Khi cần mở lại kỳ:** kế toán trưởng mở khóa tạm để điều chỉnh, rồi chốt lại.

## Cách thực hiện

1. Mở **Kỳ kế toán** trên menu.
2. Bấm **+ Thêm**:
   - **Tên kỳ:** ví dụ `Tháng 01/2026`.
   - **Ngày bắt đầu — Ngày kết thúc** kỳ.
   - **Công ty.**
3. Thiết lập **danh sách loại chứng từ bị khóa** trong kỳ (mặc định khóa toàn bộ nghiệp vụ kế toán). Có thể chừa ra một số loại nếu cần.
4. Lưu → kỳ được khóa. Muốn mở lại, xóa/sửa kỳ (cần quyền phù hợp).

## Định khoản tự động

Khai báo này **không sinh bút toán** — chỉ đặt **rào chặn ghi sổ** theo thời gian. Khi một kỳ đã khóa, mọi cố gắng ghi/sửa/hủy chứng từ có ngày rơi vào kỳ sẽ bị từ chối với cảnh báo kỳ đã đóng.

## Tình huống đặc biệt & cảnh báo

- **Khóa kỳ ≠ kết chuyển cuối kỳ.** Kết chuyển TK 911 là nghiệp vụ tạo bút toán (ở phân hệ Tổng hợp); khóa kỳ chỉ là rào chặn. Thông thường: kết chuyển xong → đối chiếu → mới khóa kỳ.
- **Đã khóa thì không nhập lùi được** chứng từ vào kỳ đó. Nếu phát hiện sai sót sau khi khóa, mở khóa kỳ (cần quyền), điều chỉnh, rồi khóa lại — và lưu vết lý do.
- **Nhập số dư đầu kỳ / dữ liệu chuyển đổi:** thực hiện TRƯỚC khi khóa các kỳ quá khứ, hoặc tạm mở khóa để nhập.
- **Cẩn trọng khi xóa kỳ để mở khóa:** chỉ kế toán trưởng/quản trị nên thao tác; ghi lại lý do mở khóa để phục vụ kiểm toán.

## Báo cáo liên quan

- [Năm tài chính](nam-tai-chinh.md) — khung năm chứa các kỳ.
- [Cài đặt kế toán](cai-dat-ke-toan.md) — cấu hình kết chuyển TK 911 chạy trước khi khóa kỳ.
- Phân hệ **Tổng hợp** — nghiệp vụ kết chuyển và chốt sổ.

## FAQ

**Q: Khóa kỳ rồi vẫn cần kết chuyển 911 — làm sao?**
**A:** Kết chuyển TRƯỚC khi khóa. Nếu lỡ khóa rồi mới cần kết chuyển, mở khóa kỳ tạm thời, chạy kết chuyển, đối chiếu, rồi khóa lại.

**Q: Tôi muốn chặn sửa hóa đơn nhưng vẫn cho ghi phiếu thu trong kỳ đã chốt?**
**A:** Khi tạo Kỳ kế toán có thể chọn danh sách loại chứng từ bị khóa — chừa loại bạn muốn vẫn cho ghi. Tuy nhiên thông thường nên khóa toàn bộ để giữ tính nhất quán.

**Q: Mở lại kỳ đã khóa có để lại dấu vết không?**
**A:** Có. Mọi thay đổi (tạo/sửa/xóa kỳ) được hệ thống lưu lịch sử thay đổi để phục vụ kiểm toán.
