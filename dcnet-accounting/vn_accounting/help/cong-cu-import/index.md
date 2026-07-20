---
section: Công cụ Import
title: Tổng quan Công cụ Import
summary: Công cụ chuyển dữ liệu kế toán từ phần mềm Misa cũ sang hệ thống — dùng một lần khi khởi tạo.
---

## Mục đích

Phân hệ **Công cụ Import** chứa các tính năng giúp đưa toàn bộ dữ liệu kế toán đang nằm trên phần mềm **Misa** (Misa SME) vào hệ thống mới khi doanh nghiệp chuyển đổi. Đây là **công cụ một lần** dùng lúc khởi tạo hệ thống: bạn kết xuất các file Excel từ Misa, tải lên, hệ thống tự đọc – phân loại – dựng lại số dư đầu kỳ và toàn bộ chứng từ phát sinh, rồi để kế toán **đối chiếu số liệu** trước khi đưa vào sử dụng chính thức.

Sau khi import xong và đối chiếu cân đối, doanh nghiệp ngừng nhập liệu trên Misa và làm việc hoàn toàn trên hệ thống mới. Công cụ này không dùng cho nghiệp vụ hằng ngày.

## Khi nào dùng

- Lúc **khởi tạo hệ thống** từ dữ liệu Misa cũ (chuyển đổi phần mềm kế toán).
- Khi cần đưa **số dư đầu kỳ** (tiền mặt, ngân hàng, công nợ, tồn kho, tài sản cố định, công cụ dụng cụ, chi phí trả trước) và **toàn bộ phát sinh trong kỳ** từ Misa vào hệ thống.
- Khi muốn **tra cứu lại** các đợt chuyển dữ liệu đã thực hiện (xem nhật ký, số dòng đã tạo, dòng lỗi).
- Không dùng cho: nhập chứng từ thường ngày, đối chiếu ngân hàng định kỳ, hay khóa sổ — đó là chức năng của các phân hệ nghiệp vụ khác.

## Cách thực hiện

Phân hệ **Công cụ Import** gồm 2 mục:

| # | Mục | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | Trung tâm chuyển dữ liệu Misa | Màn hình công cụ | Quy trình 4 bước Tải lên → Phân tích → Duyệt → Tạo vào hệ thống, kèm kiểm tra cân đối sau import |
| 2 | Lịch sử chuyển dữ liệu | Danh sách | Nhật ký các đợt chuyển dữ liệu (đợt nào, công ty nào, trạng thái, số dòng, số lỗi) |

## Quy trình điển hình

1. **Chuẩn bị file Misa**: kết xuất từ Misa các file Excel cần thiết — danh mục tham chiếu (đơn vị tính, kho, phòng ban, nhóm hàng, nhóm đối tượng, công trình, phân loại tài sản cố định / công cụ dụng cụ), hệ thống tài khoản, danh sách khách hàng / nhà cung cấp / hàng hóa / nhân viên, các file số dư đầu kỳ, và các file phát sinh (Nhật ký chung, bảng kê hóa đơn bán ra / mua vào, sổ chi tiết vật tư).
2. **Tải lên** các file vào một **đợt chuyển dữ liệu** mới trên "Trung tâm chuyển dữ liệu Misa".
3. **Phân tích**: hệ thống đọc nội dung từng file, tách dòng, tự phân loại. Bước này chỉ "đọc hiểu", chưa ghi gì vào sổ.
4. **Duyệt**: kiểm tra từng nhóm dữ liệu; xử lý các dòng bị trùng/lỗi; đánh dấu đã duyệt.
5. **Tạo vào hệ thống**: hệ thống kiểm tra điều kiện (pre-flight), sau đó dựng lại danh mục → số dư đầu kỳ → chứng từ phát sinh và **ghi sổ** (đưa vào Sổ Cái).
6. **Đối chiếu sau import**: chạy "Kiểm tra cân đối sau import" để phát hiện tài khoản lệch dấu, thiếu số dư đầu kỳ, lệch công nợ; kế toán đối chiếu với bảng cân đối phát sinh của Misa.
7. **Hoàn tác (nếu cần)**: nếu phát hiện sai sót lớn, có thể hoàn tác cả đợt và làm lại từ đầu.

## Định khoản tự động (tổng quát)

Công cụ import **không tự nghĩ ra bút toán mới** — nó **dựng lại đúng bút toán lịch sử theo nguồn Misa**:

- File **Nhật ký chung** đã chứa sẵn cặp Nợ/Có của từng chứng từ; hệ thống tạo lại đúng cặp đó (mỗi chứng từ trở thành hóa đơn bán hàng / hóa đơn mua hàng / phiếu thanh toán / phiếu nhập xuất kho / phiếu kế toán tương ứng) và đẩy vào Sổ Cái.
- File **số dư đầu kỳ** được dựng thành các bút toán đầu kỳ (số dư TK, công nợ 131/331, tồn kho, tài sản cố định 211/2141, công cụ dụng cụ, chi phí trả trước 242…).
- Vì là dữ liệu lịch sử đã chốt, công cụ **tin tưởng số liệu nguồn** — kế toán chịu trách nhiệm đối chiếu lại sau khi import.

## Tình huống đặc biệt & cảnh báo

- **Phải đối chiếu cân đối sau import**: luôn chạy "Kiểm tra cân đối sau import". Báo cáo này phân tích bảng cân đối, tự phát hiện tài khoản lệch dấu (tài sản mà dư Có, nợ phải trả mà dư Nợ…).
- **Tài khoản thụ động dễ bị thiếu**: file số dư đầu kỳ kết xuất từ Misa thường **bỏ sót một số tài khoản thụ động** (ví dụ 3387, 1331, 1551…) khiến tài khoản đó kết thúc với số dư âm sau import. Đây là vấn đề thường gặp nhất — cần kết xuất lại file đầy đủ hoặc bổ sung bằng một phiếu kế toán điều chỉnh đầu kỳ.
- **Đúng thứ tự**: phải import danh mục tham chiếu → hệ thống tài khoản → khách/nhà cung cấp/hàng hóa **trước** số dư đầu kỳ và chứng từ. Nếu thiếu, các bước sau có thể bỏ qua dữ liệu hoặc lỗi giữa chừng — bước kiểm tra pre-flight sẽ cảnh báo trước.
- **Một lần, một công ty**: mỗi công ty chỉ chạy một đợt import tại một thời điểm. Sau khi hoàn tất, không lặp lại.
- **Kỳ kế toán đã khóa**: nếu kỳ đã có chốt sổ, không thể tạo chứng từ vào kỳ đó — cần mở khóa kỳ trước.

## Báo cáo liên quan

- [Trung tâm chuyển dữ liệu Misa](misa-migration-hub.md) — màn hình thực hiện toàn bộ quy trình import.
- [Lịch sử chuyển dữ liệu](lich-su-migration.md) — tra cứu các đợt đã chạy.
- Sau khi import, dùng các báo cáo ở phân hệ **Tổng hợp** (Sổ Cái, Bảng cân đối số phát sinh) để đối chiếu với số liệu Misa.

## FAQ

**Q: Công cụ này có dùng hằng ngày không?**
**A:** Không. Đây là công cụ chuyển đổi một lần khi mới đưa hệ thống vào hoạt động. Sau khi import và đối chiếu xong, mọi nghiệp vụ làm trực tiếp trên hệ thống mới.

**Q: Import xong có an tâm là số liệu đúng chưa?**
**A:** Chưa hoàn toàn. Phải chạy "Kiểm tra cân đối sau import" và đối chiếu Bảng cân đối số phát sinh của hệ thống với của Misa (chú ý các tài khoản thụ động dễ bị thiếu). Chỉ khi cân đối khớp mới coi như đạt.

**Q: Lỡ import sai thì sao?**
**A:** Có thể bấm "Hoàn tác" để hủy + xóa mọi chứng từ do đợt đó tạo, sửa file nguồn rồi import lại. Vì vậy nên import thử và đối chiếu kỹ trước khi đưa vào dùng chính thức.

**Q: Nếu một tài khoản kết thúc với số dư âm sau import thì sao?**
**A:** Khả năng cao file số dư đầu kỳ Misa bị thiếu dòng cho tài khoản đó. Kết xuất lại file số dư đầy đủ, hoặc nhập bổ sung một phiếu kế toán điều chỉnh đầu kỳ.
