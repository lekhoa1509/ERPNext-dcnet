---
title: Lịch sử chuyển dữ liệu
order: 2
summary: Nhật ký các đợt chuyển dữ liệu từ Misa — đợt nào, công ty nào, trạng thái, số dòng, số lỗi.
---

## Mục đích

**Lịch sử chuyển dữ liệu** là nhật ký ghi lại từng **đợt chuyển dữ liệu** từ Misa vào hệ thống. Mỗi đợt là một phiên import: gồm công ty đích, ngày đầu kỳ, các file đã tải lên, trạng thái hiện tại và các con số thống kê (tổng file, tổng dòng, số tài liệu đã tạo, số dòng lỗi). Đối tượng dùng là kế toán tổng hợp / kế toán trưởng và người vận hành hệ thống, để **tra cứu** và **theo dõi** tình trạng các đợt đã/đang chạy.

## Khi nào dùng

- Xem lại đã import từ Misa những đợt nào, cho công ty nào, vào thời điểm nào.
- Theo dõi trạng thái một đợt đang chạy hoặc bị treo.
- Kiểm tra số liệu tổng quát của một đợt: tổng dòng, số tài liệu đã tạo, số dòng lỗi.
- Mở lại một đợt để tiếp tục thao tác (duyệt, tạo, hoàn tác) trên Trung tâm chuyển dữ liệu Misa.

## Cách thực hiện

1. Mở từ menu **Công cụ Import → Lịch sử chuyển dữ liệu**, hoặc bấm nút **"Lịch sử"** trên Trung tâm chuyển dữ liệu Misa.
2. Danh sách hiển thị các đợt, sắp xếp mới nhất lên đầu. Các cột chính: Công ty, Tiêu đề đợt, Ngày OB (đầu kỳ), **Trạng thái**.
3. Lọc nhanh theo **Trạng thái** để tìm đợt đang chạy / đã xong / bị treo.
4. Mở một đợt để xem chi tiết: danh sách file đã tải, các mốc thời gian (khởi tạo, hoàn tất phân tích, hoàn tất tạo, hoàn tất hoàn tác), và thống kê (tổng file, tổng dòng, tài liệu đã tạo, dòng lỗi, thời điểm bị treo nếu có).

Các **trạng thái** một đợt có thể có:

| Trạng thái | Ý nghĩa |
|---|---|
| DRAFT | Mới tạo, chưa tải file |
| UPLOADED | Đã tải file, chưa phân tích |
| PARSED | Đã phân tích xong, chờ duyệt |
| REVIEWED | Đã duyệt, sẵn sàng tạo vào hệ thống |
| POSTING | Đang tạo vào hệ thống (chạy nền) |
| POSTED | Đã tạo xong |
| REVERSING | Đang hoàn tác |
| REVERSED | Đã hoàn tác |
| STUCK | Bị treo (tiến trình nền dừng quá lâu) — cần xử lý lại |

## Định khoản tự động

Mục này **không tự định khoản** — chỉ là nhật ký tra cứu. Việc dựng lại bút toán do bước "Tạo vào hệ thống" ở Trung tâm chuyển dữ liệu Misa thực hiện.

## Tình huống đặc biệt & cảnh báo

- **Không xóa tùy tiện**: chỉ có thể xóa một đợt khi nó ở trạng thái **DRAFT** hoặc **REVERSED**. Đợt đã tạo dữ liệu (POSTED) phải **Hoàn tác** về REVERSED trước, để tránh xóa nhật ký mà chứng từ vẫn còn trong sổ.
- **Đợt bị treo (STUCK)**: nếu tiến trình nền dừng quá lâu, đợt chuyển sang STUCK. Mở lại đợt trên Trung tâm chuyển dữ liệu Misa và tiếp tục — các bước được thiết kế an toàn khi chạy lại, chứng từ đã tạo sẽ không bị tạo trùng.
- **Một công ty một đợt đang chạy**: mỗi công ty chỉ nên có một đợt ở trạng thái đang hoạt động tại một thời điểm.
- **Số dòng lỗi > 0**: vào Trung tâm chuyển dữ liệu Misa, mục "Xem & Retry" để xem lý do từng nhóm lỗi và sửa nguồn trước khi chạy lại.

## Báo cáo liên quan

- [Trung tâm chuyển dữ liệu Misa](misa-migration-hub.md) — màn hình thực hiện toàn bộ quy trình import.
- [Tổng quan Công cụ Import](index.md) — giới thiệu phân hệ.

## FAQ

**Q: Tại sao tôi không xóa được một đợt đã import?**
**A:** Để bảo vệ dữ liệu sổ sách. Đợt đã tạo chứng từ vào hệ thống phải **Hoàn tác** trước (hủy + xóa các chứng từ của đợt đó), khi về trạng thái REVERSED mới xóa được nhật ký.

**Q: Một đợt hiển thị STUCK nghĩa là sao?**
**A:** Tiến trình nền của đợt đó dừng/không phản hồi quá lâu. Mở lại đợt trên Trung tâm chuyển dữ liệu Misa và bấm tiếp tục — hệ thống chỉ xử lý phần chưa xong, không tạo trùng.

**Q: "Tài liệu đã tạo" và "Tổng số dòng" khác nhau thế nào?**
**A:** "Tổng số dòng" là số dòng đọc được từ file Misa; "Tài liệu đã tạo" là số chứng từ/danh mục thực sự sinh ra trong hệ thống. Hai số này thường khác nhau vì nhiều dòng (như bảng kê) chỉ là dữ liệu tham chiếu, hoặc nhiều dòng gộp thành một chứng từ.
