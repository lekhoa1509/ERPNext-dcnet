# HTKK XML Schemas

Thư mục này chứa file XML mẫu export từ phần mềm HTKK, dùng làm tham chiếu
cấu trúc khi sinh XML.

## Cách thêm schema mới

1. Cài HTKK phiên bản mới nhất (hiện tại 5.5.8) trên Windows
2. Mở HTKK → chọn loại tờ khai cần thêm
3. Điền dữ liệu mẫu (hoặc để trống)
4. Nhấn **"Kết xuất XML"** → lưu file
5. Copy file XML vào thư mục này, đặt tên theo convention:
   - `01_gtgt.xml` — Tờ khai 01/GTGT
   - `03_tndn.xml` — Tờ khai 03/TNDN
   - `bctc.xml` — Báo cáo tài chính
6. Phân tích cấu trúc XML để xác định tên element chính xác
7. Cập nhật module declaration tương ứng trong `declarations/`

## Namespace

Tất cả tờ khai HTKK sử dụng namespace:
```
http://kekhaithue.gdt.gov.vn/TKhaiThue
```

## Lưu ý

- KHÔNG commit file XML chứa dữ liệu thật (MST, tên công ty thật)
- Thay thế thông tin nhạy cảm bằng dữ liệu giả trước khi commit
- File XML mẫu chỉ dùng để tham chiếu cấu trúc, không dùng runtime
