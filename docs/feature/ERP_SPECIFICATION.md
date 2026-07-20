# DCNET Flow - Đặc tả ERP

> **Tài liệu đặc tả ERP** - Quản lý Bán hàng, Mua hàng, Kho, Kế toán
>
> **Phiên bản**: 1.1.0 | **Cập nhật**: 24/01/2026 | **Khách hàng**: Nhật Minh Sport
>
> **Nguồn gốc**:
> - Nhật Minh Sport | **Ngày nhận**: 30/12/2025
> - `PHASE_2_FEATURES.xlsx` - Bảng features chi tiết (15/01/2026)

### 📝 Lịch sử cập nhật

| Ngày | Nội dung | Người cập nhật |
|------|----------|----------------|
| 30/01/2026 | **Thêm sơ đồ luồng dữ liệu**: Quy trình Quản lý Kho (Section 4.0) - ASCII diagram 12 bước + kiểm kê | DCNET |
| 30/01/2026 | **Thêm sơ đồ luồng dữ liệu**: Quy trình Mua hàng (Section 3.2.0) - ASCII diagram 10 bước + báo cáo | DCNET |
| 30/01/2026 | **Thêm sơ đồ luồng dữ liệu**: Quy trình Bán lẻ (Section 2.1) - ASCII diagram + so sánh với Bán buôn | DCNET |
| 30/01/2026 | **Thêm sơ đồ luồng dữ liệu**: Quy trình Bán buôn (Section 2.0) - ASCII diagram + giải thích luồng từ tài liệu khách hàng | DCNET |
| 24/01/2026 | **Đồng bộ với PHASE_2_FEATURES.xlsx**: Cập nhật tổng 23 modules, 102 features. Chi tiết Kho (20 features), Kế toán (20 features), Web Sync (5 features) | DCNET |
| 30/12/2025 | Phiên bản gốc từ khách hàng | Nhật Minh Sport |

---

## Tổng quan Phase 2: ERP

> **Duration**: 90 ngày (3 tháng) | **Total**: 23 modules, 102 features
>
> **Source**: PHASE_2_FEATURES.xlsx | **Last Updated**: 24/01/2026

### Tổng kết theo Đợt

| Đợt | Thời gian | Số modules | Số features |
|-----|-----------|------------|-------------|
| **Đợt 1**: Quản lý Bán hàng + Mua hàng | 30 ngày | 5 | 38 |
| **Đợt 2**: Quản lý Kho + Kế toán | 45 ngày | 12 | 44 |
| **Đợt 3**: Báo cáo + Kết nối Web | 15 ngày | 6 | 20 |
| **TỔNG** | **90 ngày** | **23 modules** | **102 features** |

---

## Mục lục

1. [Phạm vi sử dụng](#1-phạm-vi-sử-dụng)
2. [Quản lý Bán hàng](#2-quản-lý-bán-hàng)
3. [Quản lý Mua hàng](#3-quản-lý-mua-hàng)
4. [Quản lý Kho](#4-quản-lý-kho)
5. [Quản lý Kế toán](#5-quản-lý-kế-toán)
6. [Báo cáo Tổng hợp](#6-báo-cáo-tổng-hợp) ⭐ *Mới*
7. [Kết nối Web bán hàng](#7-kết-nối-web-bán-hàng)

---

## 1. Phạm vi sử dụng

### Các phân hệ cần có:

| Phân hệ | Tính năng | Sử dụng |
|---------|-----------|---------|
| **Quản lý bán hàng** | Cập nhật kế hoạch, theo dõi bán hàng, chiết khấu, thanh toán, đơn hàng, lệnh xuất | ✅ |
| | Tính thưởng khi KH đạt target | ✅ |
| | Cập nhật sản lượng bán hàng của Đại lý | ✅ |
| **Quản lý mua hàng** | Import hình ảnh SP (quần áo, phụ kiện) có nguyên tắc | ✅ |
| | Cập nhật và theo dõi PO theo PO Number của hãng | ✅ |
| | Theo dõi thực hiện mua hàng, thanh toán, tính ưu đãi NCC | ✅ |
| **Quản lý kho** | Nhập/xuất theo mã số, kho, lô, vị trí, Serial | ✅ |
| | Theo dõi nhập/xuất/tồn theo mã vạch | ✅ |
| | Trừ tồn kho khả dụng (giữ theo đơn hàng) | ✅ |
| | Chức năng tạo tem, in tem trên hệ thống | ✅ |
| **Quản lý kế toán** | Kế toán tiền mặt, ngân hàng, mua hàng, bán hàng | ✅ |
| | Kế toán công nợ phải thu/trả, tạm ứng | ✅ |
| | Kế toán TSCĐ, CCDC | ✅ |
| | Tính chi phí hỗ trợ của hãng | ✅ |
| | Báo cáo chi phí theo sự kiện (marketing, demo, bán hàng, sai giá) | ✅ |
| | Báo cáo tổng hợp cho NM + Đại diện hãng (cùng dùng Bravo) | ✅ |
| **Kết nối Web** | Đồng bộ danh mục KH, hàng hóa, kho, đơn hàng, tồn kho | ✅ |

---

## 2. Quản lý Bán hàng

### Quy trình Bán buôn (12 bước)

#### 2.0. Sơ đồ luồng dữ liệu

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                              QUY TRÌNH BÁN BUÔN                                          │
├────────────────────────────────┬──────────────────────┬─────────────────────────────────┤
│        BP KINH DOANH           │       BP KHO         │          BP KẾ TOÁN             │
├────────────────────────────────┼──────────────────────┼─────────────────────────────────┤
│                                │                      │                                 │
│    ┌──────────────────┐        │                      │                                 │
│    │ 1. Kế hoạch      │        │                      │                                 │
│    │    bán hàng      │        │                      │                                 │
│    └────────┬─────────┘        │                      │                                 │
│             │                  │                      │                                 │
│             ▼                  │                      │                                 │
│    ┌──────────────────┐        │                      │                                 │
│    │ 2. Bảng giá      │        │                      │                                 │
│    │    niêm yết      │        │                      │                                 │
│    └────────┬─────────┘        │                      │                                 │
│             │                  │                      │                                 │
│             ▼                  │                      │                                 │
│    ┌──────────────────┐        │                      │                                 │
│    │ 3. Chính sách    │        │                      │                                 │
│    │    chiết khấu    │        │                      │                                 │
│    └────────┬─────────┘        │                      │                                 │
│             │                  │                      │                                 │
│             ▼                  │                      │                                 │
│    ┌──────────────────┐        │                      │                                 │
│    │ 4. Đơn đặt       │        │                      │                                 │
│    │    hàng bán      │        │                      │                                 │
│    └────────┬─────────┘        │                      │                                 │
│             │                  │                      │                                 │
│             ▼                  │                      │                                 │
│        ◇────────◇              │                      │                                 │
│       ╱ 5. Kiểm  ╲             │                      │                                 │
│      ╱  tra tồn   ╲            │                      │                                 │
│      ╲    kho     ╱            │                      │                                 │
│       ╲──────────╱             │                      │                                 │
│             │                  │                      │                                 │
│  Không đạt ◄┘                  │                      │                                 │
│  (quay lại 4)                  │                      │                                 │
│             │ Đạt              │                      │                                 │
│             ▼                  │                      │                                 │
│    ┌──────────────────┐        │                      │                                 │
│    │ 6. Lệnh xuất     │───────►│ (Chuyển Kho          │                                 │
│    │    hàng          │        │  thực hiện xuất)     │                                 │
│    └────────┬─────────┘        │                      │                                 │
│             │                  │                      │                                 │
│    ┌────────┴────────┐         │                      │                                 │
│    ▼                 ▼         │                      │                                 │
│ ◇────────◇      ◇────────◇    │                      │                                 │
│╱ 7. Kiểm ╲    ╱ 8. Kiểm  ╲    │                      │                                 │
│  tra hạn      tra hóa đơn     │                      │                                 │
│╲   mức   ╱    ╲  quá hạn ╱    │                      │                                 │
│ ╲───────╱      ╲────────╱     │                      │                                 │
│    │ Đạt          │ Đạt       │                      │                                 │
│    │   Không đạt  │           │                      │                                 │
│    │◄─────────────┤           │                      │                                 │
│    │  (quay lại 6)            │                      │                                 │
│    └──────┬───────┘           │                      │                                 │
│           │                   │                      │                                 │
│           └───────────────────┼──────────────────────┼────────┐                        │
│                               │                      │        ▼                        │
│                               │                      │ ┌──────────────────┐            │
│                               │                      │ │ 9. Hóa đơn       │            │
│                               │                      │ │    bán hàng      │            │
│                               │                      │ └────────┬─────────┘            │
│                               │                      │          │                      │
│    ┌──────────────────┐       │                      │          │ (Phát sinh hàng      │
│    │ 10. Lệnh nhập    │◄──────┼──────────────────────┼──────────┘  bán bị trả lại)     │
│    │     hàng         │       │                      │          (nét đứt)              │
│    └────────┬─────────┘       │                      │                                 │
│             │                 │                      │                                 │
│             └─────────────────┼──────────────────────┼────────┐                        │
│                               │                      │        ▼                        │
│                               │                      │ ┌──────────────────┐            │
│                               │                      │ │ 11. Hàng bán     │            │
│                               │                      │ │     bị trả lại   │            │
│                               │                      │ └──────────────────┘            │
│                               │                      │          │                      │
│    ┌──────────────────┐       │                      │          │                      │
│    │ 12. Tính thưởng  │◄──────┼──────────────────────┼──────────┘                      │
│    │     doanh số     │       │                      │                                 │
│    └──────────────────┘       │                      │                                 │
│                               │                      │                                 │
└───────────────────────────────┴──────────────────────┴─────────────────────────────────┘
```

**Chú thích:**
- `┌───┐` = Bước xử lý (Rectangle)
- `◇───◇` = Điểm quyết định (Diamond)
- `────►` = Luồng chính
- `- - -►` = Luồng phụ (phát sinh khi có trả hàng)

**Giải thích luồng:**

| Bước | Tên | Bộ phận | Mô tả |
|------|-----|---------|-------|
| 1 | Kế hoạch bán hàng | Kinh doanh | Lập kế hoạch theo năm cho từng KH |
| 2 | Bảng giá niêm yết | Kinh doanh | Cập nhật giá bán cho từng mặt hàng |
| 3 | Chính sách chiết khấu | Kinh doanh | Cập nhật tỷ lệ chiết khấu theo KH/mặt hàng |
| 4 | Đơn đặt hàng bán | Kinh doanh | NVKD lập đơn hàng dựa trên bảng giá & chiết khấu |
| 5 | Kiểm tra tồn kho | Kinh doanh | ◇ Kiểm tra còn đủ hàng không → Không đạt: quay lại bước 4 |
| 6 | Lệnh xuất hàng | Kinh doanh → Kho | Chuyển cho Kho thực hiện xuất |
| 7 | Kiểm tra hạn mức | Kinh doanh | ◇ Công nợ có vượt hạn mức không |
| 8 | Kiểm tra hóa đơn quá hạn | Kinh doanh | ◇ KH có hóa đơn quá hạn không → Không đạt: quay lại bước 6 |
| 9 | Hóa đơn bán hàng | Kế toán | Xuất hóa đơn cho KH |
| 10 | Lệnh nhập hàng | Kinh doanh | Chỉ khi có hàng bán bị trả lại |
| 11 | Hàng bán bị trả lại | Kế toán | Ghi nhận hàng trả lại, giảm công nợ |
| 12 | Tính thưởng doanh số | Kinh doanh | Tính thưởng = Doanh thu (9) - Hàng trả lại (11) |

> **Nguồn:** Tài liệu khách hàng - II. QUẢN LÝ BÁN HÀNG - 4.1.1 Sơ đồ luồng dữ liệu

---

### Quy trình Bán lẻ (3 bước)

#### 2.1. Sơ đồ luồng dữ liệu

```
┌─────────────────────────────────────────────────────────────────────┐
│                        QUY TRÌNH BÁN LẺ                             │
├────────────────────────────────┬────────────────────────────────────┤
│        BP Kinh doanh           │           Cửa hàng                 │
├────────────────────────────────┼────────────────────────────────────┤
│                                │                                    │
│  ┌──────────────────────────┐  │                                    │
│  │ 1. Xây dựng bảng giá     │  │                                    │
│  │    niêm yết              │  │                                    │
│  └────────────┬─────────────┘  │                                    │
│               │                │                                    │
│               ▼                │                                    │
│  ┌──────────────────────────┐  │                                    │
│  │ 2. Cập nhật chính sách   │  │                                    │
│  │    chiết khấu            │──┼───────────────┐                    │
│  └──────────────────────────┘  │               │                    │
│                                │               ▼                    │
│                                │  ┌──────────────────────────────┐  │
│                                │  │ 3. Hoá đơn bán lẻ            │  │
│                                │  └──────────────────────────────┘  │
│                                │                                    │
└────────────────────────────────┴────────────────────────────────────┘
```

**Giải thích luồng:**

| Bước | Tên | Bộ phận | Mô tả |
|------|-----|---------|-------|
| 1 | Xây dựng bảng giá niêm yết | Kinh doanh | Thiết lập giá bán lẻ cho từng sản phẩm |
| 2 | Cập nhật chính sách chiết khấu | Kinh doanh | Định nghĩa các mức chiết khấu áp dụng |
| 3 | Hoá đơn bán lẻ | Cửa hàng | Tạo hoá đơn bán hàng trực tiếp cho khách lẻ (POS) |

**So sánh Bán buôn vs Bán lẻ:**

| Tiêu chí | Bán buôn | Bán lẻ |
|----------|----------|--------|
| Số bước | 12 bước | 3 bước |
| Kế hoạch bán hàng | ✅ Có | ❌ Không |
| Đơn đặt hàng | ✅ Có | ❌ Không |
| Kiểm tra công nợ | ✅ Có | ❌ Không |
| Lệnh xuất kho | ✅ Riêng biệt | ❌ Tích hợp trong hoá đơn |
| Tính thưởng doanh số | ✅ Có | ❌ Không |

> **Nguồn:** Tài liệu khách hàng - II. QUẢN LÝ BÁN HÀNG - 4.1.2 Sơ đồ luồng dữ liệu (Bán lẻ)

---

#### Bước 1: Kế hoạch bán hàng theo năm

**Mục đích**: Cập nhật kế hoạch theo năm cho từng KH để tính thưởng doanh số khi đạt kế hoạch năm.

**Chức năng**: Kế hoạch bán hàng

**Bộ phận**: Kinh doanh | **Tần suất**: Theo năm

#### Bước 2: Bảng giá bán niêm yết

**Mục đích**: Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

**Màn hình**: Bảng giá niêm yết

**Thông tin cần có**:
- Thông tin chung: Ngày hiệu lực, số bảng giá, người lập, nội dung
- Thông tin chi tiết: Mã hàng hóa, tên hàng hóa, giá bán, ghi chú

**Tính năng**: Đính kèm file quyết định giá

**Bộ phận**: Kinh doanh | **Tần suất**: Khi có thay đổi

#### Bước 3: Chính sách chiết khấu bán buôn

**Mục đích**: Cập nhật tỷ lệ chiết khấu cho từng KH theo từng mặt hàng để lên đơn hàng.

**Màn hình**: Chính sách chiết khấu bán buôn

**Thông tin cần có**:
- Thông tin chung: Ngày áp dụng, đối tượng, nội dung
- Thông tin chi tiết: Mã hàng hóa, tên hàng hóa, tỷ lệ chiết khấu

**Tính năng**: Đính kèm file

**Bộ phận**: Kinh doanh | **Tần suất**: Khi có thay đổi

#### Bước 4: Đơn đặt hàng bán

**Mục đích**: Sau khi có nhu cầu từ KH, NVKD lập đơn hàng bán để ghi nhận.

**Cách làm**: Cập nhật đơn đặt hàng dựa trên bảng giá và chính sách chiết khấu đã ban hành.

**Màn hình**: Đơn đặt hàng bán

**Thông tin cần có**:
- Thông tin chung: Ngày, số đơn hàng, tiền tệ, khách hàng, địa chỉ, người liên hệ, người lập, điều khoản giao hàng, điều khoản thanh toán, phương thức thanh toán
- Thông tin chi tiết: Mã hàng, tên hàng, đơn vị tính, số lượng, đơn giá trước chiết khấu, thành tiền trước chiết khấu, số bảng giá, số chính sách chiết khấu, % chiết khấu, tiền chiết khấu, thành tiền sau chiết khấu, ngày dự kiến giao

**Thống nhất**: Nếu không nhập số chính sách chiết khấu thì cho phép tự nhập tay tỷ lệ chiết khấu.

**Bộ phận**: Kinh doanh | **Tần suất**: Hàng ngày

#### Bước 5: Kiểm tra tồn kho

**Mục đích**: Bộ phận KD kiểm tra tham khảo tồn kho xem còn đủ hàng hóa để xuất kho.

**Cách làm**: Bộ phận KD kiểm tra tồn kho để phản hồi cho KH.

**Bộ phận**: Kinh doanh | **Tần suất**: Hàng ngày

#### Bước 6: Lệnh xuất hàng

**Mục đích**: Sau khi có đơn hàng đến lịch giao hàng, bộ phận KD lập lệnh xuất hàng gửi tới bộ phận kho.

**Cách làm**: Bộ phận Kinh doanh kế thừa dữ liệu từ đơn hàng.

**Màn hình**: Lệnh xuất hàng

**Thông tin cần có**:
- Thông tin chung: Ngày đề nghị, Người đề nghị, kho xuất, khách hàng
- Thông tin chi tiết: Mã vật tư, tên vật tư, đvt, số lượng, đơn giá trước chiết khấu, thành tiền, số chính sách chiết khấu, % chiết khấu, tiền chiết khấu, tiền sau chiết khấu

**Tính năng cần có**:
- Kế thừa dữ liệu từ đơn hàng bán
- Kiểm tra hạn mức và công nợ quá hạn

**Yêu cầu phân quyền**:
- Phân quyền bộ phận kho không nhìn thấy đơn giá, thành tiền
- Phân quyền bộ phận kho không được sửa lại thông tin khách hàng, mặt hàng, số lượng yêu cầu

**Thống nhất chung**:
- Bộ phận kho cập nhật thông tin thực xuất (mặt hàng, seri, lô, kho, số lượng) để làm cơ sở cho kế toán kế thừa dữ liệu
- Khi kiểm tra điều kiện xuất hàng thì phải hiển thị số dư công nợ thực tế, công nợ dự kiến (bao gồm cả lệnh xuất hàng chưa xuất), số hóa đơn quá hạn

**Bộ phận**: Kinh doanh

#### Bước 7: Kiểm tra hạn mức công nợ

**Mục đích**: Bộ phận KD kiểm tra hạn mức công nợ của KH.

**Cách làm**: Bộ phận KD kiểm tra hạn mức công nợ. Trường hợp hết hạn mức, bộ phận KD lập lại đơn hàng, hợp đồng gửi lại KH.

**Màn hình**: Hạn mức công nợ

**Thông tin cần có**:
- Thông tin chung: Ngày áp dụng, tài khoản công nợ
- Thông tin chi tiết: Mã khách hàng, tên khách hàng, giá trị hạn mức

**Tính năng**: Đính kèm file

**Bộ phận**: Kinh doanh | **Tần suất**: Hàng ngày

#### Bước 8: Kiểm tra công nợ quá hạn

**Mục đích**: Bộ phận KD kiểm tra xem nếu có hóa đơn quá hạn hoặc quá hạn mức không để làm cơ sở cho quyết định có xuất hàng cho KH không.

**Cách làm**: Bộ phận KD thực hiện cập nhật các mặt hàng cần xuất. Khi lưu, phần mềm sẽ thực hiện kiểm tra nếu có hóa đơn quá hạn sẽ hiện cảnh báo.

**Điều kiện xuất hàng hợp lệ**:
1. Khách hàng không có hóa đơn quá hạn
2. Giá trị công nợ hiện tại + giá trị trên các lệnh xuất đã duyệt chưa xuất + giá trị trên lệnh xuất hàng hiện tại không lớn hơn hạn mức công nợ

**Xử lý ngoại lệ**: Nếu không thỏa mãn 2 điều kiện trên thì Kế toán trưởng phải xác nhận thì lệnh xuất mới hợp lệ.

#### Bước 9: Hóa đơn bán buôn

**Mục đích**: Kế toán thực hiện xuất hóa đơn cho khách.

**Cách làm**: Bộ phận kế toán căn cứ số lượng thực xuất trên lệnh xuất của bộ phận kho để xuất hóa đơn cho KH.

**Màn hình**: Hóa đơn bán buôn

**Thông tin cần có**:
- Thông tin chung: Ngày chứng từ, khách hàng, hình thức thanh toán, số hóa đơn, hạn thanh toán, mã tiền tệ, tổng tiền hàng, tổng tiền chiết khấu, tổng tiền thuế, tổng tiền
- Thông tin chi tiết: Mã vật tư, tên vật tư, đvt, số đơn hàng, số lệnh xuất hàng, kho hàng, số lượng, số bảng giá bán, đơn giá trước chiết khấu, thành tiền trước chiết khấu, số chính sách chiết khấu, % chiết khấu, tiền chiết khấu, thành tiền sau chiết khấu
- Thông tin chi tiết lô, seri: số lô, số seri, số lượng

**Tính năng cần có**:
- Kế thừa dữ liệu từ lệnh xuất hàng
- Tự động lấy ra số bảng giá, số chính sách chiết khấu theo ngày hóa đơn
- Cảnh báo nếu giá bán trên lệnh xuất khác với giá bán trên hóa đơn

**Bộ phận**: Kế toán | **Tần suất**: Hàng ngày

#### Bước 10: Lệnh nhập hàng trả lại

**Mục đích**: Kinh doanh thực hiện yêu cầu kho nhập hàng trả lại nếu có hàng bán bị trả lại.

**Cách làm**: Bộ phận Kinh doanh kế thừa dữ liệu từ hóa đơn bán hàng để lập lệnh nhập hàng trả lại.

**Màn hình**: Lệnh nhập hàng

**Thông tin cần có**:
- Thông tin chung: Ngày đề nghị, Người đề nghị, kho nhập, khách hàng
- Thông tin chi tiết: Mã vật tư, tên vật tư, đvt, số lượng, đơn giá, thành tiền
- Thông tin chi tiết: Mã lô, số seri, kho, số lượng

**Tính năng**: Kế thừa dữ liệu từ hóa đơn

**Thống nhất chung**: Bộ phận kho cập nhật thông tin thực nhập (mã hàng, mã lô, số seri, số lượng) để làm cơ sở cho kế toán kế thừa sang phiếu hàng bán trả lại.

**Bộ phận**: Kinh doanh | **Tần suất**: Khi có phát sinh

#### Bước 11: Hàng bán bị trả lại

**Mục đích**: Bộ phận kế toán kế thừa danh sách mặt hàng, seri, số lô từ lệnh nhập hàng trả lại để ghi nhận hàng bán bị trả lại.

**Màn hình**: Hàng bán bị trả lại

**Thông tin cần có**:
- Thông tin chung: Ngày, Số phiếu, Thông tin khách hàng, Lý do
- Thông tin chi tiết: Mã hàng, Tên hàng, đơn vị tính, số lượng, kho nhập, ngày dự kiến giao, số đơn hàng, số hóa đơn, ghi chú
- Thông tin chi tiết lô, seri: số lô, số seri, số lượng

**Tính năng cần có**:
- Kế thừa dữ liệu từ đề nghị nhập hàng trả lại
- Kiểm tra nếu seri nhập không tồn tại trên hóa đơn bán hàng của KH trả lại thì cảnh báo

**Bộ phận**: Kế toán | **Tần suất**: Khi có phát sinh

#### Bước 12: Tính thưởng đạt kế hoạch doanh số

**Mục đích**: Dùng cho bộ phận kế toán tính toán, ghi nhận lại chương trình chiết khấu, khuyến mại KH được hưởng làm căn cứ thu tiền từ KH.

**Cách làm**: Thực hiện chức năng tính CKKM, công nợ KH thanh toán ghi nhận tại báo có, phiếu thu tiền mặt.

**Bộ phận**: Kế toán | **Tần suất**: Khi có phát sinh

---

### Quy trình Bán lẻ (3 bước)

#### Bước 1: Bảng giá bán niêm yết

**Mục đích**: Cập nhật giá bán cho từng mặt hàng theo từng thời điểm.

**Màn hình**: Bảng giá niêm yết

**Bộ phận**: Kinh doanh | **Tần suất**: Khi có thay đổi

#### Bước 2: Chính sách chiết khấu bán lẻ

**Mục đích**: Cập nhật tỷ lệ chiết khấu cho khách lẻ theo từng mặt hàng.

**Màn hình**: Chính sách chiết khấu bán lẻ

**Thông tin cần có**:
- Thông tin chung: Ngày áp dụng, nội dung
- Thông tin chi tiết: Mã hàng hóa, tên hàng hóa, tỷ lệ chiết khấu

**Tính năng**: Đính kèm file

**Bộ phận**: Kinh doanh | **Tần suất**: Khi có thay đổi

#### Bước 3: Hóa đơn bán lẻ

**Mục đích**: Nhân viên bán hàng tại cửa hàng thực hiện lập phiếu bán hàng cho KH.

**Màn hình**: Hóa đơn bán lẻ

**Thông tin cần có**:
- Thông tin chung: Ngày, số chứng từ, số điện thoại KH, doanh số lũy kế, nhân viên kinh doanh, kho, khách hàng, địa chỉ, diễn giải, tiền hàng, tiền chiết khấu, tổng tiền, trả lại khách, tiền thanh toán, tab thẻ thanh toán, loại thuế, thuế suất, tiền thuế, yêu cầu xuất hóa đơn điện tử (Không lấy hóa đơn, phát hành hóa đơn sau, phát hành hóa đơn ngay)
- Thông tin chi tiết hàng hóa: Mã hàng, tên vật tư hàng hóa, đvt, số bảng giá, số chính sách chiết khấu, đơn giá, thành tiền, tiền chiết khấu theo chính sách, tỷ lệ chiết khấu đặc biệt, tiền chiết khấu đặc biệt
- Thông tin chi tiết lô, seri: số lô, số seri, số lượng

**Công thức**: Tiền chiết khấu đặc biệt = (tiền hàng trước chiết khấu - tiền chiết khấu theo chính sách) × tỷ lệ chiết khấu đặc biệt

**Bộ phận**: Cửa hàng | **Tần suất**: Hàng ngày

---

### Danh mục liên quan

#### Danh mục đối tượng (Khách hàng)

**Mô tả**: Dùng để khai báo danh mục các đối tượng như: nhà cung cấp, khách hàng, đối tượng nội bộ.

**Thông tin chung**: Mã đối tượng, tên đối tượng, loại đối tượng, địa chỉ, mã số thuế, người đại diện, điện thoại, email, nhóm đối tượng, thông tin tài khoản ngân hàng, phương thức thanh toán, kỳ hạn thanh toán.

#### Danh mục vật tư hàng hóa

**Thông tin chung**: Mã hàng, tên hàng hóa, đơn vị tính, macro, location, product group, color, category, phân loại doanh số, product type, statis factor, nhóm 1-6.

**Thông tin đơn vị tính quy đổi**: Đơn vị tính, hệ số quy đổi.

**Tính năng**:
- **Theo dõi lô**: Phần mềm kiểm tra được thông tin nhập xuất tồn kho theo từng mã lô. Yêu cầu: Trên tất cả các màn hình nhập dữ liệu (tồn kho đầu kỳ, phiếu nhập, phiếu xuất...), người sử dụng đều phải cập nhật thông tin mã lô tương ứng với vật tư cần theo dõi.

#### Kế hoạch doanh số năm

**Mục đích**: Dùng để nhập giá trị doanh số tiêu thụ theo kế hoạch của từng KH.

**Thông tin chung**: Ngày áp dụng, khách hàng, tổng doanh số.

**Thông tin chi tiết**: Chủng loại, % doanh số, tiền doanh số.

**Tính năng**: Đính kèm file.

---

## 3. Quản lý Mua hàng

> **Giai đoạn:** Bàn giao đợt 1
>
> **Tổng features:** 20 (từ PHASE_2_FEATURES.xlsx)

### 3.0. Danh mục NCC (2 features) ⭐ *Mới*

#### 3.0.1. Danh mục nhà cung cấp

- Quản lý thông tin NCC (Mã, Tên, Nhóm, Điều khoản thanh toán)

#### 3.0.2. Bảng giá nhà cung cấp

- Giá theo model/SKU + Hiệu lực giá
- Làm cơ sở tính KM đầu vào

---

### 3.1. Features Mua hàng mới (18 features) ⭐ *Từ Excel*

| # | Feature | Mô tả |
|---|---------|-------|
| 1 | Ưu đãi NCC | Chiết khấu % + Chiết khấu tiền + Quà tặng |
| 2 | Import hình ảnh SP | Import ảnh theo model + Quy tắc đặt tên ảnh |
| 3 | Tạo PO (Purchase Order) | PO Number (auto) + NCC + Kho nhận + Ngày đặt |
| 4 | Chi tiết PO | Model + SKU + Số lượng + Giá mua |
| 5 | Theo dõi PO theo số PO | Trạng thái: Nháp → Đã gửi NCC → Đang giao → Hoàn thành |
| 6 | Cập nhật lệnh nhập hàng | Sinh lệnh nhập từ PO + Nhập một phần / nhiều lần |
| 7 | Theo dõi thực hiện mua hàng | Đã đặt + Đã nhận một phần (%) + Đã nhận đủ |
| 8 | Nhập hàng theo lô | Mã lô + Ngày nhập + Gắn với PO |
| 9 | Nhập hàng theo serial | Serial duy nhất + Scan serial khi nhập |
| 10 | Nhập hàng theo mã vạch | Gán barcode cho SP/serial + Nhập kho bằng quét |
| 11 | Khai báo vòng đời SP | 6 tháng / 1 năm / 2 năm + Tính từ ngày nhập |
| 12 | Thông tin nguồn tiền | Quỹ tiền mặt / TK ngân hàng |
| 13 | Phương thức thanh toán | Tiền mặt + Chuyển khoản + Công nợ |
| 14 | Theo dõi thanh toán PO | Đã thanh toán + Thanh toán 1 phần + Còn nợ |
| 15 | Đính kèm chứng từ | Hóa đơn NCC + Phiếu giao hàng + Hợp đồng |
| 16 | Trạng thái phiếu nhập | Nháp + Chờ duyệt + Đã nhập kho |
| 17 | Lịch sử mua hàng | Theo NCC + Theo PO + Theo SP |
| 18 | Báo cáo mua hàng | Giá mua bình quân + NCC tốt nhất + Chi phí mua |

---

### 3.2. Quy trình Mua hàng chi tiết (10 bước)

#### 3.2.0. Sơ đồ luồng dữ liệu

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           QUY TRÌNH MUA HÀNG                                │
├─────────────────────────────────────┬───────────────────────────────────────┤
│           BP MUA HÀNG               │          BP KẾ TOÁN, KHO              │
├─────────────────────────────────────┼───────────────────────────────────────┤
│                                     │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 1. Kế hoạch mua hàng          │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  │                  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 2. Đơn hàng mua/              │  │                                       │
│  │    Hợp đồng mua               │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  │                  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 3. Kế hoạch giao hàng         │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  │                  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 4. Đề nghị nhập hàng          │──┼─────────────┐                         │
│  └───────────────────────────────┘  │             │                         │
│                                     │             ▼                         │
│                                     │  ┌───────────────────────────────┐    │
│                  ┌──────────────────┼──│ 5. Phiếu nhập mua/            │    │
│                  │                  │  │    Phiếu nhập khẩu            │──┐ │
│                  │                  │  └───────────────────────────────┘  │ │
│                  │                  │                                     │ │
│                  ▼                  │                                     │ │
│  ┌───────────────────────────────┐  │                                     │ │
│  │ 6. Lệnh xuất trả lại NCC      │──┼─────────────┐                       │ │
│  └───────────────────────────────┘  │             │                       │ │
│                                     │             ▼                       │ │
│                                     │  ┌───────────────────────────────┐  │ │
│                                     │  │ 7. Phiếu xuất trả NCC         │  │ │
│                                     │  └───────────────────────────────┘  │ │
│                  ┌──────────────────┼─────────────────────────────────────┘ │
│                  │                  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 8. Xác nhận công nợ           │  │                                       │
│  └───────────────┬───────────────┘  │                                       │
│                  │                  │                                       │
│                  ▼                  │                                       │
│  ┌───────────────────────────────┐  │                                       │
│  │ 9. Đề nghị thanh toán         │──┼─────────────┐                         │
│  └───────────────────────────────┘  │             │                         │
│                                     │             ▼                         │
│                                     │  ┌───────────────────────────────┐    │
│                                     │  │ 10. Phiếu chi/ Báo nợ         │    │
│                                     │  └───────────────┬───────────────┘    │
│                                     │                  │                    │
├─────────────────────────────────────┴──────────────────┼────────────────────┤
│                                                        ▼                    │
│                                      ┌───────────────────────┐              │
│                                      │   Hệ thống báo cáo    │              │
│                                      └───────────────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Giải thích luồng:**

| Bước | Tên | Bộ phận | Mô tả |
|------|-----|---------|-------|
| 1 | Kế hoạch mua hàng | Mua hàng | Lập kế hoạch mua theo kỳ/năm |
| 2 | Đơn hàng mua/Hợp đồng mua | Mua hàng | Tạo PO hoặc hợp đồng với NCC |
| 3 | Kế hoạch giao hàng | Mua hàng | Lên lịch nhận hàng từ NCC |
| 4 | Đề nghị nhập hàng | Mua hàng | Yêu cầu Kho nhập hàng |
| 5 | Phiếu nhập mua/Phiếu nhập khẩu | Kế toán, Kho | Ghi nhận nhập kho → Trỏ đến 6 và 8 |
| 6 | Lệnh xuất trả lại NCC | Mua hàng | Lệnh trả hàng cho NCC |
| 7 | Phiếu xuất trả NCC | Kế toán, Kho | Ghi nhận xuất kho trả |
| 8 | Xác nhận công nợ | Mua hàng | Đối chiếu công nợ với NCC |
| 9 | Đề nghị thanh toán | Mua hàng | Lập đề xuất thanh toán |
| 10 | Phiếu chi/Báo nợ | Kế toán, Kho | Thanh toán → Hệ thống báo cáo |

> **Nguồn:** Tài liệu khách hàng - III. QUẢN LÝ MUA HÀNG - Sơ đồ luồng dữ liệu

---

#### Bước 1: Kế hoạch mua hàng

**Mục đích**: Dùng cho bộ phận mua hàng cập nhật kế hoạch mua hàng gửi nhà cung cấp.

**Cách làm**: Căn cứ vào báo giá được phê duyệt, nhu cầu đặt hàng, phòng mua hàng thực hiện cập nhật kế hoạch mua hàng.

**Màn hình**: Kế hoạch mua hàng

**Thông tin cần có**:
- Thông tin chung: Ngày, số kế hoạch, nhà cung cấp, nội dung
- Thông tin chi tiết: Mã vật tư, tên vật tư, đvt, loại mua (Demo/Purchase), đơn giá, Family, year, category, sub category, shaft, price, số lượng tháng 1-12

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 2: Đơn hàng mua

**Mục đích**: Dùng cho bộ phận mua hàng cập nhật, quản lý đơn đặt hàng, hợp đồng với nhà cung cấp.

**Cách làm**: Căn cứ vào báo giá được phê duyệt, phòng mua hàng thực hiện ký đơn hàng.

**Màn hình**: Đơn hàng mua

**Thông tin cần có**:
- Thông tin chung: Ngày, số đơn hàng mua, người lập, nội dung, nhà cung cấp, điều khoản thanh toán, điều khoản giao hàng
- Thông tin chi tiết: Mã vật tư, tên vật tư, đvt, số lượng, ghi chú, số kế hoạch mua hàng

**Tính năng**: Kế thừa thông tin từ kế hoạch mua hàng (lấy mã hàng hóa, đơn giá và các thuộc tính của hàng hóa).

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 3: Kế hoạch giao hàng

**Mục đích**: Dùng cho bộ phận mua hàng cập nhật kế hoạch giao hàng khi nhận được lịch giao hàng từ nhà cung cấp.

**Cách làm**: Căn cứ vào lịch giao hàng, phòng mua hàng cập nhật kế hoạch giao hàng.

**Màn hình**: Kế hoạch giao hàng

**Thông tin cần có**:
- Thông tin chung: Ngày chứng từ, số chứng từ, người lập, nội dung, nhà cung cấp
- Thông tin chi tiết: Mã vật tư, tên vật tư chính thức, tên vật tư theo danh mục, Vendor name, **PO Number**, PO Create Date, Buyer name, Type, Product Group, Category, Location, Model, Stastic factor, Total Unit, Ship to, Month, Confirm ship date, Ship mode, Ean, Upc, PO comment, Remark, số kế hoạch mua hàng, số đơn đặt hàng

**Tính năng cần có**:
- Kế thừa thông tin từ đơn đặt hàng
- Cảnh báo nếu tên vật tư chính thức khác với tên vật tư trên danh mục

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 4: Đề nghị nhập hàng

**Mục đích**: Dùng cho phòng mua hàng ghi nhận hàng hóa chuẩn bị về kho.

**Cách làm**: Phòng mua hàng lập đề nghị nhập hàng trên hệ thống, đồng thời bộ phận kho cũng nhận được thông báo để sắp xếp vị trí chứa hàng.

**Màn hình**: Lệnh nhập hàng

**Thông tin cần có**:
- Thông tin chung: Ngày, số lệnh, người lập, nội dung, nhà cung cấp, kho, tình trạng thông quan, ngày dự kiến thông quan, ngày thực tế thông quan
- Thông tin chi tiết: Mã vật tư, tên vật tư, số lượng, khách hàng, số kế hoạch mua hàng, số đơn hàng, số kế hoạch giao hàng
- Thông tin chi tiết lô: Số lot, số Serial number, số lượng

**Tính năng**: Kế thừa dữ liệu từ kế hoạch giao hàng.

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 5: Phiếu nhập mua/Nhập khẩu

**Mục đích**: Bộ phận kế toán tiến hành cập nhật phiếu nhập (Nhập mua, nhập khẩu) để ghi nhận công nợ và nhập kho cho hàng hóa.

**Cách làm**: Căn cứ vào yêu cầu của bộ phận mua hàng, bộ phận kế toán tạo phiếu nhập mua ghi nhận hàng hóa, vật tư nhập kho thực tế.

**Màn hình**: Phiếu nhập mua/Nhập khẩu

**Thông tin cần có**:
- Thông tin chung: Ngày, số phiếu, người lập, nội dung, nhà cung cấp, tiền tệ, kho, số tờ khai
- Thông tin chi tiết: Mã vật tư, tên vật tư, số lượng, đơn giá nhập, thành tiền, số lô, seri, số đơn hàng, số lệnh nhập hàng, số kế hoạch mua hàng, số kế hoạch giao hàng, đơn giá kế hoạch, đơn giá đơn hàng

**Tính năng cần có**:
- Kế thừa dữ liệu từ lệnh nhập hàng
- Cảnh báo nếu giá nhập khác giá đơn hàng

**Bộ phận**: Kế toán | **Tần suất**: Khi có phát sinh

#### Bước 6: Chi phí mua hàng

**Mục đích**: Bộ phận mua hàng cập nhật chi phí mua hàng (Vận chuyển, bốc dỡ...).

**Cách làm**: Bộ phận mua hàng cập nhật tại phiếu chi phí mua hàng.

**Màn hình**: Chi phí mua hàng

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 7: Lệnh xuất trả lại NCC

**Mục đích**: Dùng cho bộ phận mua hàng lập lệnh xuất hàng để bộ phận kho chuẩn bị hàng.

**Cách làm**: Bộ phận mua hàng thống kê sản phẩm lỗi, hỏng, không đạt chất lượng gửi trả NCC.

**Màn hình**: Lệnh xuất hàng

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 8: Trả lại NCC

**Mục đích**: Dùng cho bộ phận kho trả lại hàng không đạt chất lượng cho NCC.

**Cách làm**: Bộ phận kế thừa dữ liệu từ Lệnh xuất trả lại NCC.

**Màn hình**: Phiếu xuất trả lại

**Bộ phận**: Kế toán | **Tần suất**: Khi có phát sinh

#### Bước 9: Xác nhận công nợ

**Mục đích**: Bộ phận mua hàng xác nhận công nợ và thực hiện lập đề nghị thanh toán cho NCC.

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

#### Bước 10: Đề nghị thanh toán

**Mục đích**: Dùng cho phòng mua hàng lập đề nghị thanh toán gửi tới bộ phận kế toán để thanh toán tiền hàng cho nhà cung cấp.

**Cách làm**: Căn cứ theo việc hoàn tất giao hàng của nhà cung cấp và hồ sơ, Phòng mua hàng làm đề nghị thanh toán cho nhà cung cấp đủ điều kiện thanh toán.

**Màn hình**: Đề nghị thanh toán

**Thông tin cần có**: Ngày đề nghị, Số đề nghị, Nội dung, Nhà cung cấp, Đơn hàng mua/Hợp đồng mua, Giá trị đơn hàng, Đã tạm ứng, Giá trị thanh toán, Người lập, hình thức thanh toán.

**Tính năng**: Kế thừa dữ liệu từ đơn hàng mua/Hợp đồng mua.

**Bộ phận**: Mua hàng | **Tần suất**: Khi có phát sinh

---

### Danh mục liên quan

#### Tính năng import ảnh

**Mục đích**: Nhân viên mua hàng thực hiện cập nhật ảnh cho nhiều mặt hàng từ thư mục được chọn.

**Cách làm**: Nhân viên mua hàng chọn thư mục ảnh có chứa ảnh cần cập nhật. Phần mềm đọc file ảnh, dựa vào tên file ảnh theo quy ước để nhận diện được file ảnh là của mã hàng hóa nào để thực hiện cập nhật ảnh lên thư mục trên server. Sau khi cập nhật xong, người dùng vào danh mục vật tư hàng hóa để kích vào file đính kèm để xem ảnh.

---

### Báo cáo quản trị

**Báo cáo so sánh kế hoạch mua hàng và đơn hàng**

---

## 4. Quản lý Kho

> **Giai đoạn:** Bàn giao đợt 2
>
> **Tổng features:** 20 (Kho hàng) + 5 (Báo cáo Kho)

### 4.0. Sơ đồ luồng dữ liệu

```
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│                              QUY TRÌNH QUẢN LÝ KHO                                         │
├─────────────────────┬────────────────────────────────────┬─────────────────────────────────┤
│     BP KHO NHẬP     │  BP KẾ TOÁN, MUA HÀNG, BÁN HÀNG   │         BP KHO XUẤT             │
├─────────────────────┼────────────────────────────────────┼─────────────────────────────────┤
│                     │                                    │                                 │
│                     │     ┌────────────────────────┐     │                                 │
│                     │     │ 1. Tồn kho đầu kỳ      │     │                                 │
│                     │     └───────────┬────────────┘     │                                 │
│                     │                 │                  │                                 │
│    ┌────────────────┼─────────────────┼──────────────────┼───────────────────┐             │
│    │                │                 │                  │                   │             │
│    ▼                │                 │                  │                   ▼             │
│ ┌─────────────────┐ │                 │                  │  ┌─────────────────────────┐    │
│ │ 2. Phiếu nhập   │ │                 │                  │  │ 5. Phiếu xuất kho       │    │
│ │    kho          │ │                 │                  │  └─────────────────────────┘    │
│ └────────┬────────┘ │                 │                  │                   │             │
│          │          │                 │                  │                   ▼             │
│          │          │                 │                  │  ┌─────────────────────────┐    │
│ ┌─────────────────┐ │                 │                  │  │ 6. Phiếu xuất CCDC      │    │
│ │ 3. Phiếu nhập   │ │                 │                  │  └─────────────────────────┘    │
│ │    mua          │ │                 │                  │                   │             │
│ └────────┬────────┘ │                 │                  │                   ▼             │
│          │          │                 │                  │  ┌─────────────────────────┐    │
│          │          │                 │                  │  │ 7. Phiếu điều chuyển    │    │
│ ┌─────────────────┐ │                 │                  │  │    kho                  │    │
│ │ 4. Phiếu nhập   │ │                 │                  │  └─────────────────────────┘    │
│ │    khẩu         │ │                 │                  │                   │             │
│ └────────┬────────┘ │                 │                  │                   ▼             │
│          │          │                 │                  │  ┌─────────────────────────┐    │
│          │          │                 │                  │  │ 8. Phiếu điều chuyển    │    │
│          │          │                 │                  │  │    vị trí               │    │
│          │          │                 │                  │  └─────────────┬───────────┘    │
│          │          │                 │                  │                │               │
│          └──────────┼─────────────────┼──────────────────┼────────────────┘               │
│                     │                 │                  │                                 │
│                     │                 ▼                  │                                 │
│                     │     ┌────────────────────────┐     │                                 │
│                     │     │ 9. Lệnh kiểm kê        │     │                                 │
│                     │     └───────────┬────────────┘     │                                 │
│                     │                 │                  │                                 │
│                     │                 ▼                  │                                 │
│                     │     ┌────────────────────────┐     │                                 │
│                     │     │ 10. Phiếu kiểm kê      │     │                                 │
│                     │     └───────────┬────────────┘     │                                 │
│                     │                 │                  │                                 │
│                     │                 ▼                  │                                 │
│                     │           ◇──────────◇            │                                 │
│                     │          ╱  Thừa/     ╲           │                                 │
│                     │         ╱   Thiếu?    ╲          │                                 │
│                     │         ╲             ╱          │                                 │
│                     │          ╲───────────╱           │                                 │
│                     │           │         │             │                                 │
│        Yes          │           │         │ No          │                                 │
│    ┌────────────────┼───────────┘         │             │                                 │
│    ▼                │                     │             │                                 │
│ ┌─────────────────┐ │                     │             │                                 │
│ │ 11. Phiếu Nhập/ │ │                     │             │                                 │
│ │ xuất chênh lệch │ │                     │             │                                 │
│ │ kiểm kê         │ │                     │             │                                 │
│ └─────────────────┘ │                     │             │                                 │
│                     │                     ▼             │                                 │
│                     │     ┌────────────────────────┐     │                                 │
│                     │     │ 12. Tính giá vốn hàng  │     │                                 │
│                     │     │     xuất               │     │                                 │
│                     │     └───────────┬────────────┘     │                                 │
│                     │                 │                  │                                 │
│                     │                 ▼                  │                                 │
│                     │     ┌────────────────────────┐     │                                 │
│                     │     │   Hệ thống báo cáo     │     │                                 │
│                     │     └────────────────────────┘     │                                 │
│                     │                                    │                                 │
└─────────────────────┴────────────────────────────────────┴─────────────────────────────────┘
```

**Giải thích luồng:**

| Bước | Tên | Bộ phận | Mô tả |
|------|-----|---------|-------|
| 1 | Tồn kho đầu kỳ | Kế toán, Mua hàng, Bán hàng | Số dư tồn kho đầu kỳ |
| 2 | Phiếu nhập kho | Kho nhập | Nhập kho nội bộ |
| 3 | Phiếu nhập mua | Kho nhập | Nhập kho từ mua hàng |
| 4 | Phiếu nhập khẩu | Kho nhập | Nhập kho từ nhập khẩu |
| 5 | Phiếu xuất kho | Kho xuất | Xuất kho bán hàng |
| 6 | Phiếu xuất CCDC | Kho xuất | Xuất công cụ dụng cụ |
| 7 | Phiếu điều chuyển kho | Kho xuất | Chuyển hàng giữa các kho |
| 8 | Phiếu điều chuyển vị trí | Kho xuất | Chuyển hàng trong cùng kho |
| 9 | Lệnh kiểm kê | Kế toán, Mua hàng, Bán hàng | Lệnh thực hiện kiểm kê |
| 10 | Phiếu kiểm kê | Kế toán, Mua hàng, Bán hàng | Ghi nhận kết quả kiểm kê |
| 11 | Phiếu Nhập/xuất chênh lệch kiểm kê | Kho nhập | Điều chỉnh khi Thừa/Thiếu (Yes) |
| 12 | Tính giá vốn hàng xuất | Kế toán, Mua hàng, Bán hàng | Tính giá vốn (No) → Báo cáo |

> **Nguồn:** Tài liệu khách hàng - IV. QUẢN LÝ KHO - 6.1.1 Sơ đồ luồng dữ liệu

---

### 4.1. Kho hàng (20 features)

#### 4.1.1. Danh sách kho

- Mã kho + Tên kho + Địa chỉ + NV phụ trách + Trạng thái
- Nút tích xác định có cho phép xuất âm kho hay không

#### 4.1.2. Quản lý vị trí kho ⭐ *Mới*

- Khu vực + Kệ + Ô/Vị trí
- Gán vị trí cho sản phẩm

#### 4.1.3. Danh mục vật tư hàng hóa

- Mã SP + Model + SKU + Nhóm SP
- Theo dõi lô: Phần mềm kiểm tra được thông tin nhập xuất tồn kho theo từng mã lô

#### 4.1.4. Quản lý theo lô (Batch/Lot)

- Mã lô + Ngày nhập + Vòng đời SP + Tồn theo lô
- Trước khi thực hiện lập phiếu nhập thì thủ kho khai báo thông tin lô hàng hóa

#### 4.1.5. Quản lý theo Serial ⭐ *Mới*

- Serial hàng hóa duy nhất
- Trạng thái serial: **Tồn** / **Ký gửi** / **Đã bán**
- Lịch sử serial

#### 4.1.6. Quản lý nhập kho

- Nhập từ NCC + Nhập điều chuyển + Nhập trả hàng
- Gắn phiếu nhập
- Thông tin: Ngày, số phiếu, người lập, nội dung, nhà cung cấp, tiền tệ, kho
- Chi tiết: Mã vật tư, tên vật tư, số lượng, đơn giá, thành tiền, số lô, seri, số đơn hàng

#### 4.1.7. Quản lý xuất kho

- Xuất bán hàng + Xuất điều chuyển + Xuất hao hụt
- Xuất CCDC (công cụ dụng cụ) với thông tin phân bổ

#### 4.1.8. Nhập xuất theo mã số

- Theo mã SP + Theo kho + Theo lô + Theo vị trí

#### 4.1.9. Theo dõi tồn kho

- Tồn thực tế + Tồn khả dụng + Tồn giữ

#### 4.1.10. Tồn kho khả dụng ⭐ *Mới*

- **Công thức**: Tồn khả dụng = Tồn thực tế – Tồn giữ
- Cập nhật realtime

#### 4.1.11. Giữ hàng theo đơn ⭐ *Mới*

- Giữ tồn khi tạo đơn hàng
- Hoàn tồn khi hủy đơn
- Trừ tồn khi hoàn thành đơn

#### 4.1.12. Quản lý mã vạch

- Gán mã vạch cho SP/serial
- Quét khi nhập – xuất
- Quy ước mã vạch:
  - Tem tự in: `mã vật tư + ;; + số lô`
  - Tem NCC: `số seri`

#### 4.1.13. Tạo tem sản phẩm

- Tem mã SP + Tem serial + Tem lô
- Thông tin: Ngày, loại tem, người lập, số lô, nước sản xuất, NCC, đơn vị nhập khẩu

#### 4.1.14. In tem

- In đơn chiếc + In hàng loạt
- Tùy chỉnh mẫu tem
- Kế thừa mặt hàng, seri từ phiếu nhập khẩu

#### 4.1.15. Điều chuyển kho

- Kho đi / kho đến + SP / lô / serial
- Kế thừa dữ liệu từ đề nghị xuất kho nội bộ
- Quy trình: Đơn vị xuất → Kho trung gian → Đơn vị nhận

#### 4.1.16. Kiểm kê kho

- Theo kho + Theo vị trí
- So sánh thực tế & hệ thống
- Chi tiết: Mã hàng, đơn vị tính, số lượng, lô/lot, serial

#### 4.1.17. Điều chỉnh kho

- Xử lý Thừa/thiếu sau kiểm kê
- Ghi nhận lý do
- Tạo phiếu nhập/xuất chênh lệch kiểm kê

#### 4.1.18. Cảnh báo kho ⭐ *Mới*

- Tồn thấp (MIN) - cảnh báo khi dưới định mức
- Sắp hết vòng đời - cảnh báo trước X ngày

#### 4.1.19. Lịch sử kho

- Nhập + Xuất + Điều chuyển
- Ai thao tác + Thời gian

#### 4.1.20. Tính giá vốn hàng xuất

- Tính và áp giá vốn vào các phiếu xuất
- **Phương pháp**: Trung bình tháng (hoặc FIFO)

---

### 4.2. Báo cáo Kho (5 features)

#### 4.2.1. Báo cáo nhập xuất tồn

- Theo kho + Theo SP + Theo lô

#### 4.2.2. Báo cáo theo serial

- Serial tồn + Serial đã bán

#### 4.2.3. Báo cáo tồn khả dụng

- Tồn thực tế vs tồn giữ

#### 4.2.4. Báo cáo vòng đời SP

- Còn 60 ngày + Còn 45 ngày

#### 4.2.5. Phân tích kho

- Hàng bán nhanh/chậm + Hàng cần sale

---

### 4.3. Quy trình đặc biệt

#### Xuất nội bộ giữa các cửa hàng

1. Nhân viên phụ trách điều phối hàng hóa thực hiện lập lệnh xuất hàng
2. Cửa hàng xuất làm phiếu xuất điều chuyển kho (Kho xuất: kho ký gửi, Kho nhập: kho ký gửi)
3. Trưởng cửa hàng xuất duyệt phiếu xuất để xác nhận lượng xuất
4. Trưởng cửa hàng nhận duyệt phiếu xuất để xác nhận lượng nhập

#### Quy trình hàng ký gửi (Thăng Long TM ↔ Nhật Minh)

**Nhập xuất hàng ký gửi**:
1. Tại khay Thăng Long làm phiếu xuất điều chuyển kho từ kho tổng sang kho ký gửi
2. Tại khay Nhật Minh làm phiếu nhập kho vào ký gửi tại cửa hàng

**Mua bán giữa Nhật Minh và Thăng Long TM**:
1. Nhật Minh tổng hợp số lượng thực tế bán cho KH để gửi Thăng Long làm căn cứ xuất hóa đơn
2. Thăng Long xuất hóa đơn từ kho hàng ký gửi cho Nhật Minh
3. Nhật Minh lập phiếu nhập mua đưa vào kho xuất hóa đơn

**Bán hàng tại Nhật Minh**:
1. Bán hàng cho KH từ kho xuất hóa đơn để ghi nhận tăng doanh thu, công nợ
2. Xuất kho hàng ký gửi để giảm lượng tồn kho
3. Lập phiếu nhập mua đưa vào kho xuất hóa đơn để cuối tháng tính được giá vốn

---

## 5. Quản lý Kế toán

> **Giai đoạn:** Bàn giao đợt 2
>
> **Tổng features:** 20

### 5.0. Thông tin chung

- **Chế độ kế toán áp dụng**: Thông tư 99
- **Hình thức sổ kế toán**: Nhật ký chung
- **Phương pháp tính giá xuất kho**: Trung bình tháng (hoặc FIFO)
- **Theo dõi đồng tiền hạch toán**: VND
- **Phương pháp đánh giá CLTG**: Theo thông tư 99
- **Phương pháp tính khấu hao TSCĐ**: Đường thẳng

---

### 5.1. Kế toán tiền (2 features)

#### 5.1.1. Quản lý tiền mặt

- Số dư đầu kỳ + Thu – chi + Sổ quỹ
- Lập và in phiếu Thu, Chi theo Thông tư 200
- Theo dõi Quỹ

#### 5.1.2. Quản lý tiền ngân hàng

- Nhiều tài khoản + Biến động số dư + Sao kê
- Lập và in Báo Nợ, Báo Có
- Tự động hạch toán chênh lệch tỷ giá ngoại tệ
- Đánh giá chênh lệch tỷ giá cuối kỳ
- Theo dõi khế ước

---

### 5.2. Kế toán mua hàng (2 features)

#### 5.2.1. Kế toán mua hàng

- Nhận dữ liệu từ PO & phiếu nhập + Giá vốn
- Lập và in phiếu nhập mua, phiếu chi phí vận chuyển
- Theo dõi, hạch toán thuế GTGT, thuế nhập khẩu
- Phân bổ chi phí mua, vận chuyển, thuế nhập cho các mặt hàng

#### 5.2.2. Theo dõi thanh toán mua

- Đã thanh toán + Thanh toán 1 phần + Công nợ
- Phiếu chi trả nhà cung cấp, bù trừ công nợ, thanh toán tạm ứng

---

### 5.3. Kế toán bán hàng (1 feature)

#### 5.3.1. Ghi nhận doanh thu

- Theo đơn hàng + Theo kênh bán
- Lập và in hóa đơn, phiếu hàng bán bị trả lại, phiếu thu tiền hàng
- Tính giá vốn hàng bán trung bình tháng
- Các báo cáo thuế GTGT

---

### 5.4. Kế toán công nợ (3 features)

#### 5.4.1. Công nợ phải thu

- Hạn thanh toán + Tuổi nợ
- Báo cáo tổng hợp, chi tiết công nợ phải thu khách hàng

#### 5.4.2. Công nợ phải trả

- Gắn với PO / phiếu nhập
- Theo dõi công nợ phải trả nhà cung cấp, bảng đối chiếu công nợ

#### 5.4.3. Tạm ứng - Hoàn ứng

- Nhân viên / NCC + Đối trừ công nợ

---

### 5.5. Kế toán tồn kho (2 features)

#### 5.5.1. Giá trị tồn kho

- Theo kho + Theo batch
- Quản lý nhập/xuất/tồn hàng hóa vật tư theo kho, mặt hàng, nhóm hàng

#### 5.5.2. Giá vốn bán hàng (COGS)

- Phương pháp: FIFO / Bình quân
- Tính giá vốn tự động

---

### 5.6. Chi phí & Hỗ trợ (2 features)

#### 5.6.1. Chi phí hỗ trợ hãng

- Marketing + Trưng bày + Demo
- Ghi nhận và phân bổ chi phí hỗ trợ từ hãng cho từng sự kiện, chương trình

#### 5.6.2. Phân bổ chi phí

- Theo SP + Theo chiến dịch
- Báo cáo chi phí theo sự kiện (Marketing, Demo, Bán hàng, Sai giá)

---

### 5.7. Tài sản & CCDC (2 features)

#### 5.7.1. Quản lý TSCĐ

- Nguyên giá + Khấu hao
- Khai báo, đăng ký và quản lý tài sản với thông số kỹ thuật, đặc điểm
- Tự động tính và hạch toán khấu hao theo phương pháp đường thẳng
- In báo cáo: Thẻ tài sản, sổ tài sản, bảng tính khấu hao, báo cáo tăng giảm

#### 5.7.2. Công cụ dụng cụ

- Phân bổ nhiều kỳ
- Theo dõi các lần xuất dùng, giá trị phân bổ vào chi phí
- Bảng phân bổ giá trị CCDC, bảng tổng hợp tình hình sử dụng

---

### 5.8. Kế toán thuế (2 features)

#### 5.8.1. Kế toán thuế

- VAT đầu vào/ra
- Các báo cáo thuế GTGT

#### 5.8.2. Kết xuất dữ liệu thuế

- Xuất file HTKK + Theo chuẩn thuế

---

### 5.9. Kế toán tổng hợp (4 features)

#### 5.9.1. Báo cáo KQKD

- Doanh thu + Chi phí + Lợi nhuận

#### 5.9.2. Báo cáo chi phí

- Marketing + Demo + Sale

#### 5.9.3. Báo cáo quản trị

- Theo chi nhánh + Theo đại lý
- Báo cáo tổng hợp cho Nhật Minh và Đại diện hãng

#### 5.9.4. Kiểm soát - Audit log ⭐ *Mới*

- Ai thao tác + Thời gian
- Lập các phiếu bổ sung nghiệp vụ hạch toán
- Bút toán tự động: chênh lệch tỷ giá, định kỳ, kết chuyển và phân bổ

---

## 6. Báo cáo Tổng hợp

> **Giai đoạn:** Bàn giao đợt 3
>
> **Tổng features:** 14
>
> ⭐ *Mới thêm từ PHASE_2_FEATURES.xlsx*

### 6.1. Báo cáo Tồn kho Tổng hợp (5 features)

#### 6.1.1. Tổng hợp nhập - xuất - tồn

- Tổng số lượng nhập + Tổng số lượng xuất + Tồn kho cuối kỳ

#### 6.1.2. Báo cáo tồn kho theo kho

- Theo từng kho/chi nhánh + Giá trị tồn kho

#### 6.1.3. Báo cáo tồn kho theo model

- Model / SKU + Số lượng tồn + Tỷ trọng tồn

#### 6.1.4. Báo cáo tồn kho theo lô

- Mã lô + Ngày nhập + Tồn theo lô

#### 6.1.5. Báo cáo tồn kho theo vòng đời

- Hàng mới + Hàng chậm bán + Hàng sắp hết vòng đời

---

### 6.2. Báo cáo Bán hàng (3 features)

#### 6.2.1. Báo cáo hàng bán ra

- Số lượng bán + Theo thời gian + Theo kênh bán

#### 6.2.2. Báo cáo hàng bán theo đại lý

- Doanh số từng đại lý + Sản lượng bán

#### 6.2.3. Báo cáo luân chuyển hàng hóa

- Tốc độ bán + Thời gian lưu kho

---

### 6.3. Báo cáo Phân tích (4 features)

#### 6.3.1. Báo cáo hàng tồn chậm

- Hàng bán chậm + Đề xuất sale / điều chuyển

#### 6.3.2. Báo cáo hàng sắp hết vòng đời

- Còn 60 ngày + Còn 45 ngày

#### 6.3.3. Báo cáo hàng điều chuyển

- Điều chuyển giữa các kho + Điều chuyển cho đại lý

#### 6.3.4. Báo cáo hàng thanh lý / sale

- Sale campaign + Thanh lý

---

### 6.4. Báo cáo Quản trị (2 features)

#### 6.4.1. Báo cáo quản trị theo yêu cầu

- Theo thời gian + Theo sản phẩm + Theo đại lý

#### 6.4.2. Kết xuất báo cáo

- Excel + PDF

---

## 7. Kết nối Web bán hàng

> **Giai đoạn:** Bàn giao đợt 3
>
> **Tổng features:** 6
>
> ⭐ *Chi tiết hóa từ PHASE_2_FEATURES.xlsx*

### 7.1. Đồng bộ dữ liệu (1 feature)

#### 7.1.1. Đồng bộ dữ liệu chuẩn hóa

- Dữ liệu chuẩn hóa + Chia sẻ cho hãng

---

### 7.2. Web Sync (5 features)

#### 7.2.1. Đồng bộ danh mục KH

- Sync customer data giữa CRM và Website
- **Chiều đồng bộ**: 2 chiều (Web ↔ CRM)

#### 7.2.2. Đồng bộ danh mục hàng hóa

- Sync product catalog (hình ảnh, mô tả, giá)
- **Chiều đồng bộ**: 1 chiều (CRM → Website)

#### 7.2.3. Đồng bộ danh mục kho

- Sync warehouse data
- **Chiều đồng bộ**: 1 chiều (CRM → Website)

#### 7.2.4. Đồng bộ đơn hàng

- Auto tạo đơn hàng từ Website → CRM
- Update trạng thái
- **Chiều đồng bộ**: 1 chiều (Web → CRM)

#### 7.2.5. Đồng bộ tồn kho

- Real-time sync tồn kho khả dụng → Website
- **Chiều đồng bộ**: 1 chiều (CRM → Website)

---

### 7.3. Bảng tóm tắt đồng bộ

| Dữ liệu | Chiều đồng bộ | Ghi chú |
|---------|---------------|---------|
| Danh mục khách hàng | Web ↔ CRM | 2 chiều |
| Danh mục hàng hóa | CRM → Web | 1 chiều (hình ảnh, mô tả, giá) |
| Danh mục kho | CRM → Web | 1 chiều |
| Đơn hàng | Web → CRM | Auto tạo + Update status |
| Tồn kho | CRM → Web | Real-time sync |

---

**© 2025 DCNET Corporation - Powered by DCNET Cloud**
