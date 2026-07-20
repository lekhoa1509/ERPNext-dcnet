# UI Spec — Sale Order Detail (MISA CRM style)

> Đọc file này là đủ để code lại UI. Không cần hỏi thêm.

---

## 1. Layout tổng thể

```
┌─────────────────────────────────────────────────────────────┐
│ TOPBAR                                               h=50px  │
├──────────┬──────────────────────────────────────────────────┤
│          │ ORDER HEADER                             h=62px  │
│ SIDEBAR  ├──────────────────────────────────────────────────┤
│ w=190px  │ LEFT PANEL (w=380px) │ CONTENT (flex:1)          │
│          │                      │                           │
│          │  scroll nội bộ       │  TABS + TABLE             │
└──────────┴──────────────────────┴───────────────────────────┘
```

- Toàn màn hình `100vh`, không scroll ngoài, overflow hidden.
- Font: `Inter, -apple-system, sans-serif`, base `13px`, màu chữ `#1f2937`.
- Nền tổng: `#f3f5f9`.

---

## 2. Màu sắc

| Token | Hex | Dùng cho |
|---|---|---|
| `primary` | `#4361ee` | Link, icon active, badge count, table code |
| `primary-dark` | `#3b5bdb` | Tab active, nav-item active |
| `green` | `#16a34a` | Nút "Đề nghị ghi DS" |
| `teal` | `#0d9488` | Stars ở header, text trạng thái "Chưa thực hiện" |
| `blue-btn` | `#4361ee` | Nút download tròn |
| `orange` | `#f97316` | Icon Thanh toán |
| `blue-icon` | `#3b82f6` | Icon Giao hàng |
| `purple` | `#7c3aed` | Icon Khách hàng |
| `red` | `#e53935` | Badge thông báo |
| `border` | `#e5e9f0` | Border mặc định |
| `border-card` | `#e2e8f0` | Border card |
| `border-table` | `#e5e9f2` | Border thead |
| `border-row` | `#f0f3f8` | Border giữa các row |
| `bg-page` | `#f3f5f9` | Nền trang |
| `bg-total-row` | `#edf1f6` | Row tổng cộng |
| `bg-thead` | `#fafbfc` | Nền thead |
| `text-muted` | `#6b7280` | Label, placeholder |
| `text-dark` | `#111827` | Giá trị, tiêu đề card |
| `text-body` | `#374151` | Text thường, nút |
| `text-disabled` | `#c5ccd8` | Nút phân trang disabled |

---

## 3. Topbar `h=50px`

- Nền `#fff`, border-bottom `1px #e5e9f0`.
- **Left** (w=190px): icon grid mờ + logo "CRM" (icon Rocket nền `#2563eb` bo `10px`, text `800 19px #1a1f36`).
- **Center**: ô tìm kiếm `max-w=340px h=34px`, border `#d8dde9`, bo `7px`, placeholder màu `#9aa4b8`.
- **Right** (`margin-left:auto`): 8 icon `19px` màu `#6b7480`, khoảng cách `10px`.
  - Icon Bell có badge đỏ `#e53935` góc trên phải, `border-radius 999px`, `h=16px min-w=18px font=10px bold`.
  - Avatar cuối cùng: tròn `30px`, gradient `#c8f0ff → #f5c6a4 (135deg)`, chữ initial `bold 13px`.

---

## 4. Sidebar `w=190px`

- Nền `#fff`, border-right `1px #e5e9f0`, padding `14px 10px`.
- Mỗi nav-item: `h=36px`, `border-radius 8px`, `gap=10px`, `font 13px 600 #374151`, `margin-bottom 2px`.
- **Active**: nền `#ebedff`, chữ + icon `#3b5bdb`.
- Icon size `16px`.

---

## 5. Order Header `h=62px`

- Nền `#fff`, border-bottom `1px #e8edf4`, padding `0 20px`, space-between.

**Bên trái:**
- Icon ArrowLeft `22px #374151`
- Số đơn: `font 22px 800 #0f172a`
- Dấu `·` màu `#9ca3af font 20px`
- Chuỗi stars/reference: `color #0d9488 bold letter-spacing 2px font 15px`
- Nút download: tròn `30px`, nền `#4361ee`, icon trắng `16px`
- Icon refresh `16px #9ca3af`

**Bên phải (gap=7px):**

| Nút | Style |
|---|---|
| In | `h=34px border #dde3ef bg #fff bo 7px font 13px 600 #374151` |
| Sửa | như trên |
| Gửi phê duyệt | như trên |
| Đề nghị ghi DS | như trên nhưng `bg #16a34a border #16a34a color #fff` |
| `···` | như trên, `w=34px`, chỉ icon |

Hover nút thường: `bg #f7f8fc`. Hover primary: `bg #15803d`.

---

## 6. Left Panel `w=380px`

- Nền `#fff`, border-right `1px #e5e9f0`, padding `18px 16px 16px 18px`, scroll-y.

**Phần trên:**
- Title: `font 17px 800 #0f172a`, `margin-bottom 12px`
- "Thêm thẻ": icon Tag + text `color #4361ee font 13px 600`, `margin-bottom 16px`
- Date row: `font 13px #6b7280`, ngày bold `#374151`, nút trạng thái margin-left auto
- **Status pill**: nền `#e5e7eb`, `border-radius 999px h=32px padding 0 14px font 13px 700 #374151`, có icon ChevronDown

**Cards** (margin-bottom `12px` mỗi card):

```
border: 1px solid #e2e8f0
border-radius: 10px
padding: 14px 15px
background: #fff
box-shadow: 0 1px 2px rgba(0,0,0,0.04)
```

- **Card Khách hàng**: flex row, gap `12px`, `min-h 70px`.
  - Icon Building2 `19px #7c3aed`
  - Tên KH: `13px 700 #111827`
  - Mã KH · SĐT: `13px #6b7280 margin-top 5px`
  - Icon ChevronRight `17px #9ca3af` (margin-left auto)

- **Card Thanh toán / Giao hàng**:
  - Header (`.card-head`): flex, gap `9px`, icon `17px` (orange/blue) + label bold + status text (margin-left auto) + icon Circle
  - Field list (`.field-group`): `margin-top 12px gap 6px`
    - Mỗi field: grid `148px 1fr`, label `#6b7280`, value `13px 600 #111827`

**Thông tin tóm tắt:**
- Title `16px 800 #111827` + icon nút SlidersHorizontal `34px bo 8px border #dde3ef`
- Field list như trên, value "Chưa thực hiện" dùng `color #0d9488`

---

## 7. Tabs `h=48px`

- Flex, `align-items: flex-end`, border-bottom `1px #e8edf4`, overflow-x hidden (no scrollbar).
- Mỗi tab: `h=48px padding 0 14px 12px font 13px 600 #6b7280 white-space nowrap`.
- **Active tab**: `color #3b5bdb`, pseudo `::after` — `position absolute bottom 0 left 12px right 12px h=2.5px bg #3b5bdb bo 2px`.
- **Badge count**: `border-radius 999px font 11px 700 padding 1px 6px`.
  - Blue badge (tab active): `bg #4361ee color #fff`
  - Gray badge (other tabs): `bg #e5e7eb color #6b7280`

---

## 8. Goods Table (bảng hàng hóa)

**Wrapper `.goods-card`:**
```
bg #fff  border 1px #e8edf4  border-radius 10px  overflow hidden
flex column  flex:1  min-height 0
```

**Header `.goods-top` h=50px:**
- Title `15px 800 #111827`
- Links bên phải: icon + text `color #4361ee 13px 600 gap 8px`

**Table:**
```
border-collapse: collapse
table-layout: fixed
font-size: 13px
```

| Cột | Width |
|---|---|
| STT | 48px, text-align center |
| Mã hàng hóa | 130px, `color #4361ee font 600` |
| Tên hàng hóa | 180px |
| Mô tả | 185px |
| Đơn vị tính | 82px |
| Số lượng | 72px, text-align center |
| Đơn giá | 115px |
| Thành tiền | 115px |

**thead th:** `h=40px bg #fafbfc border-bottom+right 1px #e5e9f2 padding 0 12px font 600 #374151`

**tbody td:** `h=44px border-bottom+right 1px #f0f3f8 padding 0 12px font 500 #1f2937 vertical-align middle`

**Row đầu tiên** (nếu có mô tả dài): `height auto min-h 72px vertical-align top padding-top 12px`
- Mô tả hiển thị bullet points, có link "xem thêm" màu `#4361ee`

**Row tổng cộng:**
```
background: #edf1f6
font-weight: 700
height: 44px
border-bottom: none
```

**Scrollbar giả bên dưới table:**
- `h=8px bg #d1d8e3 border-top 1px #c8cfd9`
- Thumb: `position absolute right=0 top=1px w=40% h=5px bg #aab4c5 bo 4px`

---

## 9. Pager `h=46px`

- Flex space-between, `font 13px padding-top 6px`.
- "Tổng số N": `font 600 #374151`
- **Right**: gap `12px`
  - Label "Số dòng/trang": `#6b7280`
  - Dropdown "20": `h=32px border #dde3ef bo 7px font 600 #374151`
  - Range "1 - N": `font 500 #374151`
  - 4 nút điều hướng: `28×28px border #dde3ef bo 6px`, khi disabled: `color #c5ccd8 border #e8ecf4 bg #f9fafb`

---

## 10. Nút nổi

- **Float collapse** (giữa left panel và content): `fixed left≈558px top≈580px w=16px h=40px border #d8dfe9 bg #fff bo 6px color #8b96a8`
- **Right stick** (sát mép phải): `fixed right=0 top=50% w=16px h=32px bg #1d6cf6 color #fff bo 6px 0 0 6px`

---

## 11. Quy tắc chung

- Tất cả border đều `1px solid`, không bao giờ `2px+`.
- Border-radius: card=`10px`, button=`7px`, nav=`8px`, pill=`999px`, avatar=`50%`.
- Không dùng shadow nặng — chỉ `0 1px 2px rgba(0,0,0,0.04)` cho card.
- Icon library: **lucide-vue-next** (hoặc lucide-react), size mặc định `16–19px`.
- Spacing unit: bội số `4px` (4, 8, 12, 14, 16, 18, 20...).
- Tất cả font-weight chỉ dùng: `500` (body), `600` (label/button), `700` (bold), `800` (heading).
