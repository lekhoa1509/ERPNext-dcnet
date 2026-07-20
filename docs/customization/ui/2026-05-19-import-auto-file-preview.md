# Import tự động (AI) File Preview Popup & Feedback History

## Overview

Thêm khả năng bấm vào tên tệp trong bảng **Import tự động (AI)** để mở popup review nội dung Excel trước khi import, đồng thời lưu lịch sử góp ý khi người dùng yêu cầu AI phân tích lại.

## Requirements

- Người dùng cần xem nhanh file Excel đã được AI phân tích ngay trên màn form.
- Popup chỉ đọc dữ liệu preview, không ghi dữ liệu và không tự tạo Data Import.
- API preview phải kiểm tra quyền đọc trên document **Import tự động (AI)**.
- Mỗi lần người dùng gửi ý kiến phân tích lại phải được lưu như log chat.
- Log phải có cả ý kiến người dùng và phản hồi/kết quả phân tích của AI.

## Implementation

- Tên file trong bảng được đổi từ text thường thành button dạng link.
- Khi click, client gọi `preview_import_file`.
- Server đọc workbook bằng service Excel hiện có và trả về metadata + sample rows theo sheet.
- Dialog hiển thị thông tin file, trạng thái AI, số dòng, độ tin cậy, và bảng preview cho từng sheet.
- Dialog **Phân tích lại tệp** hiển thị `Lịch sử ý kiến` dạng chat log.
- Khi gửi ý kiến, backend append entry vào `feedback_history_json`.
- Khi job AI hoàn tất, entry tương ứng được cập nhật `ai_response`, DocType sau phân tích, confidence và trạng thái.
- Các lần phân tích sau gửi cả lịch sử góp ý trước đó vào prompt để AI có context hội thoại.

## Technical Notes

- Files changed:
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.js`
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto/import_auto.py`
  - `dcnet-migrate/dcnet_migrate/import_auto/doctype/import_auto_file/import_auto_file.json`
  - `dcnet-migrate/dcnet_migrate/import_auto/services/processor.py`
- Preview giới hạn 30 dòng mẫu mỗi sheet để tránh popup quá nặng.
- API dùng quyền `read`; các thao tác import/phân tích lại vẫn giữ quyền `write`.
- Feedback history lưu trong field JSON ẩn trên từng dòng `Import Auto File`.

## Deployment

Chạy migrate để sync field JSON mới, sau đó clear cache nếu site đang cache assets DocType JS:

```bash
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local migrate"
docker exec devcontainer-frappe-1 bash -c "cd /workspace/development/frappe-bench && bench --site flow.local clear-cache"
```

## Future Updates

- Có thể thêm filter/search trong popup nếu file có nhiều cột.
- Có thể thêm nút mở Data Import từ popup khi dòng đã có bản nháp Data Import.
- Có thể tách feedback history thành DocType riêng nếu sau này cần báo cáo/audit nâng cao.

## Troubleshooting

- Nếu popup báo không đọc được file, kiểm tra `file_path` còn tồn tại trong container.
- Nếu click không phản hồi, clear cache và reload browser.
- Nếu lịch sử ý kiến không hiện, kiểm tra field `feedback_history_json` đã được sync qua migrate chưa.

## Verification Checklist

- [ ] Click tên file mở popup review.
- [ ] Popup hiển thị metadata file và sheet preview.
- [ ] User không có quyền đọc document không gọi được API.
- [ ] Import/Reanalyze vẫn hoạt động như trước.
- [ ] Gửi nhiều ý kiến tạo nhiều entry trong lịch sử.
- [ ] Khi AI phân tích xong, entry có phản hồi AI và trạng thái mới.
