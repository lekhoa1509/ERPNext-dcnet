# Đặc tả giao diện: Danh sách "Báo giá" (Quote List)

> Tài liệu này mô tả chi tiết pixel-level giao diện danh sách Báo giá của MISA AMIS CRM để tái tạo lại 100% trên nền tảng khác (ví dụ ERPnext/Frappe). Không phụ thuộc framework — chỉ mô tả cấu trúc, kích thước, màu sắc, nội dung.

**Lưu ý quan trọng:** Nút **"Thêm AI"** (nút xanh đậm có nhãn phụ "AI" cạnh nút "Thêm") — **KHÔNG triển khai**. Đây là tính năng AI riêng của MISA, không cần clone. Chỉ giữ lại 2 nút: "Nhập từ Excel" và "Thêm" (dạng outline), cộng nút "..." (more).

---

## 1. Bố cục tổng thể (layout)

Khu vực nội dung chia làm 3 cột ngang, full-height, không cuộn trang ngoài (chỉ cuộn bên trong từng cột):

```
┌───────────────────────────────────────────┬───────────────┬───────────────┐
│  KHU VỰC DANH SÁCH BÁO GIÁ (flex: 1)       │  HÀNG HÓA     │   BỘ LỌC      │
│  - Page header (title + actions)           │  (300px)      │   (260px)     │
│  - Toolbar (search + icon buttons)         │               │               │
│  - Table (scroll dọc, header sticky)       │               │               │
│  - Footer (tổng hợp + phân trang)          │               │               │
└───────────────────────────────────────────┴───────────────┴───────────────┘
```

- Panel "Hàng hóa" và "Bộ lọc" có thể ẩn/hiện độc lộc (toggle bằng icon trên toolbar).
- Panel "Bộ lọc" có nút đóng (X) riêng ở góc trên phải panel.
- Border giữa các cột: `1px solid #e5e7eb`.

---

## 2. Bảng màu (color tokens)

| Token | Hex | Dùng cho |
|---|---|---|
| `--blue` | `#1968e5` | Link, viền nút outline, icon active, chữ nút primary |
| `--blue-dark` | `#0f52ba` | Hover của nút filled |
| `--blue-light` | `#eaf2ff` | Nền dòng được chọn/hover trong bảng, nền icon-toggle active |
| `--blue-lighter` | `#f3f8ff` | Hover nút outline |
| `--navy` | `#16233f` | Nền sidebar (nếu có) |
| `--gray-50` | `#fafbfc` | Nền header bảng, nền footer |
| `--gray-100` | `#f1f3f5` | Nền ô search |
| `--gray-150` | `#eceef1` | Border giữa các dòng bảng |
| `--gray-200` | `#e5e7eb` | Border chung, viền input/button |
| `--gray-300` | `#d1d5db` | — |
| `--gray-400` | `#9ca3af` | Icon phụ, placeholder |
| `--gray-500` | `#6b7280` | Label phụ, text mờ |
| `--gray-600` | `#4b5563` | Icon thường |
| `--gray-900` | `#1f2937` | Text chính |
| `--red` | `#ff4d4f` | Badge thông báo |

Font: `"Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`. Cỡ chữ cơ bản `14px` (13.5px cho bảng/toolbar, 12–13px cho label phụ).

---

## 3. Page header (dòng tiêu đề)

- Padding: `16px 20px 12px`.
- Trái: `Tất cả báo giá` — font-size `19px`, `font-weight: 700`, màu `--gray-900`, kèm icon chevron-down (mở dropdown đổi view) ngay sau text, cách `6px`.
- Phải: các nút theo thứ tự:
  1. **`Nhập từ Excel`** — button outline: nền trắng, viền `1px solid var(--blue)`, chữ `--blue`, icon "upload" bên trái, bo góc `6px`, padding `7px 14px`, font-weight `600`.
  2. **`+ Thêm`** — cùng style outline như trên, icon "plus".
  3. ~~`Thêm AI`~~ — **bỏ qua, không làm** (xem lưu ý đầu file).
  4. Nút "..." (more-horizontal) — icon-only, tròn, `32x32px`, hover nền `--gray-100`.

---

## 4. Toolbar (dòng tìm kiếm + icon công cụ)

- Padding: `0 20px 12px`, `display:flex; justify-content:space-between`.
- **Ô tìm kiếm thông minh** bên trái:
  - Nền `--gray-100`, viền `1px solid var(--gray-200)`, bo góc `6px`, padding `7px 12px`, width `320px`.
  - Icon kính lúp bên trái (màu `--gray-400`), input placeholder `"Tìm kiếm thông minh"`.
  - Badge nhỏ **"AI"** bên phải trong ô: nền `--blue`, chữ trắng, bo góc `4px`, font-size `10px`, font-weight `700`, padding `2px 5px`.
- **Nhóm icon bên phải** (mỗi icon: nút vuông `32x32px`, viền `1px solid var(--gray-200)`, nền trắng, bo góc `6px`, cách nhau `6px`):
  1. Icon "refresh" (làm mới danh sách).
  2. Icon "settings" (bánh răng — cấu hình cột).
  3. Icon "layers/cube" — **toggle mở/đóng panel "Hàng hóa"**. Khi đang mở: nền `--blue-light`, viền `--blue`, icon màu `--blue`.
  4. Icon "filter" (phễu lọc) — **toggle mở/đóng panel "Bộ lọc"**. Cùng style active như trên.

---

## 5. Bảng danh sách báo giá

### Cột (theo đúng thứ tự, đúng tên hiển thị)

| Cột | Rộng | Ghi chú |
|---|---|---|
| checkbox | 40px | checkbox chọn tất cả ở header, checkbox từng dòng |
| Thẻ | — | cột luôn để trống trong dữ liệu mẫu (nhãn/tag) |
| Số báo giá | — | link màu `--blue`, font-weight `500`, có gạch chân khi hover |
| Ngày báo giá | — | có icon "sort" (mũi tên lên-xuống) cạnh tên cột, cỡ `13px` |
| Hiệu lực đến ngày | — | có thể để trống |
| Khách hàng | max-width 260px | text dài bị cắt bằng `ellipsis`, có `title` tooltip đầy đủ |
| Liên hệ | — | tên người liên hệ, hoặc dấu `-` nếu trống |

### Style

- Header: nền `--gray-50`, sticky top, border-bottom `1px solid var(--gray-200)`, chữ `--gray-600`, `font-weight:600`, padding `9px 14px`.
- Dòng dữ liệu: padding `9px 14px`, border-bottom `1px solid var(--gray-150)`.
- Hover dòng: nền `--gray-50`.
- **Dòng đang chọn/nổi bật** (ví dụ dòng đầu tiên trong ảnh mẫu): nền `--blue-light`.
- Checkbox: `accent-color: var(--blue)`, kích thước `15x15px`.

### Dữ liệu mẫu (16 dòng hiển thị, tổng "Tổng số 288")

| Số báo giá | Ngày báo giá | Hiệu lực đến ngày | Khách hàng | Liên hệ |
|---|---|---|---|---|
| BG0240956 | 13/07/2026 | | CÔNG TY TNHH CÔNG NGHỆ VIỄN THÔ... | Minh Quan |
| BG0240953 | 09/07/2026 | 31/07/2026 | CHI NHÁNH CÔNG TY TNHH THỰC PHẨ... | Mr Tuấn STB |
| BG0240957 | 13/07/2026 | | CÔNG TY TNHH CÔNG NGHỆ VIỄN THÔ... | Minh Quan |
| BG0240961 | 16/07/2026 | | CÔNG TY TNHH CÔNG NGHỆ VIỄN THÔ... | Minh Quan |
| BG0240958 | 14/07/2026 | 31/07/2026 | CÔNG TY TNHH THỰC PHẨM & NƯỚC GI... | Mr. Thịnh – Deca Plu... |
| BG0240955 | 13/07/2026 | | CÔNG TY CỔ PHẦN CÔNG NGHỆ MOBIF... | Lê Thị Phương Thảo |
| BG0240954 | 09/07/2026 | 31/07/2026 | CÔNG TY TNHH THỰC PHẨM & NƯỚC GI... | Mr. Thịnh – Deca Plu... |
| BG0240946 | 02/07/2026 | | CÔNG TY CỔ PHẦN HẠ TẦNG VIỄN THÔ... | Long |
| BG0240948 | 03/07/2026 | | CÔNG TY TNHH AINAVIO | Trung |
| BG0240952 | 09/07/2026 | | CÔNG TY CỔ PHẦN HẠ TẦNG VIỄN THÔ... | Long |
| BG0240951 | 09/07/2026 | 15/07/2026 | CÔNG TY TNHH ROCHDALE SPEARS | Mr Quỳnh |
| BG0240950 | 08/07/2026 | | CÔNG TY CỔ PHẦN ANNE HILL | - |
| 060726/BG | 06/07/2026 | 20/07/2026 | NGÂN HÀNG TMCP ĐẦU TƯ VÀ PHÁT TRI... | Hùng |
| BG0240949 | 06/07/2026 | | CÔNG TY CỔ PHẦN HẠ TẦNG VIỄN THÔ... | Long |
| BG0240947 | 03/07/2026 | | CÔNG TY CỔ PHẦN HẠ TẦNG VIỄN THÔ... | Long |
| BG0240944 | 26/06/2026 | | CÔNG TY CỔ PHẦN HẠ TẦNG VIỄN THÔ... | Long |

---

## 6. Footer bảng (tổng hợp + phân trang)

- Nền `--gray-50`, border-top `1px solid var(--gray-200)`, padding `8px 20px`, `display:flex; justify-content:space-between`, font-size `13px`.
- **Bên trái** — nhóm tổng hợp, mỗi mục cách nhau `22px`, dạng `label: value`:
  - `Tổng số` → **288** (chữ số màu `--blue`, đậm)
  - `Thành tiền` → `*******` (giá trị bị che, màu `--gray-500`)
  - `Tiền thuế` → `*******`
  - `Tiền chiết khấu` → `*******`
  - `Tổng tiền` → `*******`
- **Bên phải** — phân trang:
  - `Số dòng/trang` + dropdown hiển thị **20** (kèm chevron-down)
  - `1 - 20` (khoảng dòng đang xem)
  - 4 nút icon: `«` (về đầu), `‹` (lùi), `›` (tiến), `»` (đến cuối) — mỗi nút `26x26px`, hover nền `--gray-150`.

---

## 7. Panel "Hàng hóa" (bên phải, rộng 300px)

- Header panel: padding `14px 16px`, border-bottom `1px solid var(--gray-200)`.
  - Trái: `Hàng hóa` (bold, `14.5px`) + badge số lượng tròn nền `--blue`, chữ trắng (`4`).
  - Phải: icon "search" và icon "edit" (bút chì), mỗi icon `28x28px`.
- **Danh sách sản phẩm** (lặp lại 4 mục, dữ liệu giống hệt nhau trong ảnh mẫu):
  - Mỗi item: padding `12px 16px`, border-bottom `1px solid var(--gray-150)`.
  - Dòng 1 (tên): `#{index}. DV_MPLS_L2 - Truyền số liệu (MPLS)` — font-weight `600`, kèm icon chevron-down bên phải (để mở rộng chi tiết).
  - Dòng 2 (công thức tính, giá trị bị che): `1 Tháng x ******* = *******` — màu `--gray-500`.
  - Dòng 3: icon "message-circle" (bình luận) + số `0`, canh phải, màu `--gray-400`, font-size `12.5px`.
- **Footer panel** (dưới cùng, nền `--gray-50`, border-top):
  - Dòng 1: `Số lượng: 4`   `Số lượng giao: 0` (2 mục cách đều, số in đậm).
  - Dòng 2: `Tổng tiền` (đậm) — giá trị `*******` (đậm) kèm icon chevron-up nhỏ bên phải.

---

## 8. Panel "Bộ lọc" (bên phải cùng, rộng 260px)

- Header: padding `14px 16px`, border-bottom. Trái: `Bộ lọc` (bold `14.5px`). Phải: icon "close" (X) để đóng panel.
- **Mục "ĐÃ LƯU"** (SAVED): section header dạng button full-width, uppercase, font-size `12px`, font-weight `700`, màu `--gray-500`, có icon chevron-up/down để thu gọn — mặc định đang **mở** nhưng không có nội dung mẫu bên dưới (để trống, chờ dữ liệu bộ lọc đã lưu).
- **Mục "TIÊU CHÍ LỌC"** (FILTER CRITERIA): cùng style section header, mặc định mở.
  - Ô tìm kiếm tiêu chí: nền `--gray-100`, bo góc `6px`, icon kính lúp, placeholder `"Tìm kiếm tiêu chí"`.
  - Danh sách checkbox tiêu chí (theo đúng thứ tự, tất cả chưa check mặc định):
    1. Thẻ
    2. Số báo giá
    3. Ngày báo giá
    4. Hiệu lực đến ngày
    5. Khách hàng
    6. Liên hệ
    7. Tổng tiền
    8. Tình trạng
    9. Mô tả
  - Link `Xem thêm` (màu `--blue`, in đậm) ở cuối để hiển thị thêm tiêu chí khác (không có trong danh sách mẫu).

---

## 9. Trạng thái tương tác cần có

- Toggle mở/đóng panel "Hàng hóa" và "Bộ lọc" độc lập bằng 2 icon trên toolbar.
- Đóng panel "Bộ lọc" bằng nút X trên chính panel đó.
- Checkbox chọn dòng + checkbox "chọn tất cả" ở header bảng.
- Sắp xếp theo cột "Ngày báo giá" (icon sort).
- Dòng đầu tiên trong bảng ở trạng thái highlight sẵn (mô phỏng dòng đang được xem/chọn).

---

## 10. Ghi chú triển khai cho ERPnext/Frappe

- Có thể build bằng Frappe Custom Page / Vue component nhúng trong Frappe Desk, hoặc HTML report view tùy kiến trúc hiện có của dự án ERPnext.
- Giữ đúng khoảng cách, màu sắc, cỡ chữ như bảng trên để đảm bảo giống 100% về mặt hình ảnh.
- **Không** cần render nút "Thêm AI" — chỉ 2 nút hành động (`Nhập từ Excel`, `Thêm`) + nút more (`...`).
- Toàn bộ giá trị tiền (`*******`) trong ảnh mẫu là dữ liệu bị che do phân quyền xem — khi triển khai thật, thay bằng giá trị số thực nếu người dùng có quyền xem, nếu không giữ nguyên dạng che (mask).
