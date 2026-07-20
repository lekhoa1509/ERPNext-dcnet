# SUBAGENT BRIEF — Viết help cho 1 section của vn_accounting

Bạn là subagent viết tài liệu help cho phân hệ **VN Accounting** (app `vn_accounting`) trên bench `frappe-bench-dcnet`. Đọc brief này là đủ context — KHÔNG cần đọc gì khác ngoài code bạn sẽ tham chiếu.

## Bối cảnh
- Bench: `/home/long/long/frappe-bench-dcnet`. App: `apps/vn_accounting`. Site test: `dcnet.localhost`, công ty `DCNET`.
- Python: `/home/long/long/frappe-bench-dcnet/env/bin/python`. Site path: `/home/long/long/frappe-bench-dcnet/sites`.
- Help đặt tại `apps/vn_accounting/vn_accounting/help/<section-slug>/`.

## Nhiệm vụ của bạn (cho section được giao)
1. **Đọc code thực tế** của từng item (report `.py`/`.js`, doctype controller, page bundle) để viết help CHÍNH XÁC theo code — KHÔNG bịa.
2. **Triage dữ liệu**: với mỗi report, chạy `execute()` cho DCNET (xem mục Data triage) → ghi nhận report nào RỖNG (0 rows).
3. **Viết/ghi đè** mỗi item 1 file `.md` trong `help/<section-slug>/` theo template bên dưới. Viết cả `index.md` cho section.
4. **Trả về** (trong message cuối) theo đúng "Return format" — KHÔNG tự sửa hooks.py, KHÔNG `bench build`, KHÔNG bơm dữ liệu. Main agent lo các việc đó.

## Quy tắc thuật ngữ (BẮT BUỘC — tiếng Việt thuần)
- KHÔNG dùng tên DocType tiếng Anh trong nội dung. Dùng:
  - Journal Entry → **phiếu kế toán / bút toán**
  - Payment Entry → **phiếu thanh toán**
  - Sales Invoice → **hóa đơn bán hàng**; Purchase Invoice → **hóa đơn mua hàng**
  - Delivery Note → **phiếu xuất kho**; Purchase Receipt → **phiếu nhập kho**
  - Stock Entry → **phiếu nhập xuất kho**; Sales Order → **đơn bán hàng**; Purchase Order → **đơn mua hàng**
  - GL/General Ledger → **Sổ Cái**; docstatus submitted → **đã ghi sổ/đã duyệt**
- KHÔNG nhắc "Frappe" hay "ERPNext". Nếu cần nói về nền tảng, chỉ dùng "**ERP**" hoặc "hệ thống".
- Viết tiếng Việt CÓ DẤU đầy đủ. Số hiệu TK theo VAS (111, 112, 131, 331, 511, 632, 642, 242, 154, 627, 3331, 3387, 911, 4212...).
- Tham chiếu **TT99/2025** khi nói về biểu mẫu/sổ/tài khoản (hiệu lực 2026-01-01, thay TT200/2014). KHÔNG mặc định TT200.

## Cấu trúc template (theo `help/tien-mat/`)
Mỗi **article** `<slug>.md` — frontmatter + 7 mục H2 (KHÔNG thêm `# Title` vào body vì đã có frontmatter title):
```markdown
---
title: <Tên hiển thị tiếng Việt>
order: <số thứ tự trong section>
summary: <1 câu tóm tắt>
---

## Mục đích
<Báo cáo/chức năng này làm gì, dùng cho ai>

## Khi nào dùng
- <gạch đầu dòng các tình huống>

## Cách thực hiện
1. <các bước thao tác thực tế trên UI>
   (có thể tham chiếu ảnh: ![Alt](_images/<slug>-1.png) — KHÔNG bắt buộc tạo ảnh)
2. <bộ lọc, nút bấm>

## Định khoản tự động
<Nếu chức năng sinh bút toán: bảng | Trường hợp | TK Nợ | TK Có | Ghi chú |. Nếu KHÔNG sinh bút toán (report/list): nói rõ "không tự định khoản — chỉ tra cứu/nhập liệu".>

## Tình huống đặc biệt & cảnh báo
- <edge cases, cảnh báo VAS, lỗi thường gặp>

## Báo cáo liên quan
- <liên kết tới article khác cùng/khác section>

## FAQ
**Q: ...?**
**A:** ...
```

**`index.md`** của section — frontmatter `section:` + `title:` + `summary:`, body gồm: Mục đích, Khi nào dùng, Cách thực hiện (bảng liệt kê các mục menu của section), Quy trình điển hình, Liên kết tới các article, Định khoản tự động (tổng quát), Tình huống đặc biệt, Báo cáo liên quan, FAQ.

## Cách tìm code
- Report: `apps/vn_accounting/vn_accounting/vn_accounting/report/<snake_slug>/<snake_slug>.py` (logic) + `.js` (filter) + `.json` (metadata). Nếu là report của ERPNext (Accounts Payable, Stock Balance, Sales Analytics...) thì nằm trong `apps/erpnext/...` — đọc để hiểu cột/bộ lọc, mô tả theo nghiệp vụ VN.
- DocType controller: `apps/<app>/.../doctype/<snake>/<snake>.py` (tìm bằng `find apps -path "*doctype/<snake>*"`). Đọc `validate`/`on_submit` để biết bút toán + ràng buộc.
- Page: `apps/vn_accounting/.../page/<slug>/` hoặc bundle trong `public/js/`.

## Data triage (chạy cho mỗi report)
```bash
cd /home/long/long/frappe-bench-dcnet/sites
../env/bin/python -c "
import frappe, importlib
frappe.init(site='dcnet.localhost', sites_path='/home/long/long/frappe-bench-dcnet/sites'); frappe.connect(); frappe.set_user('Administrator')
m=importlib.import_module('vn_accounting.vn_accounting.report.<snake_slug>.<snake_slug>')
res=m.execute({'company':'DCNET','from_date':'2026-01-01','to_date':'2026-12-31'})
print(len(res[1]) if len(res)>1 else 0, 'rows')
frappe.destroy()
"
```
Với report ERPNext: có thể bỏ qua execute (filter phức tạp) — chỉ cần ghi "report ERPNext, kiểm tra data ở main".

## ISOLATION CONTRACT (BẮT BUỘC — để không xung đột git & frontend)
Nhiều subagent chạy SONG SONG trên CÙNG 1 working tree. Để không mất việc / không xung đột:
1. **CHỈ ghi file trong đúng 1 thư mục `help/<section-slug-của-bạn>/`.** Mỗi subagent sở hữu 1 thư mục riêng → đường dẫn rời nhau → không bao giờ đụng file của nhau. TUYỆT ĐỐI không tạo/sửa file ngoài thư mục đó.
2. **KHÔNG chạy bất kỳ lệnh git nào** (`git add/commit/checkout/stash/restore...`). Main agent commit tập trung sau cùng.
3. **KHÔNG sửa file dùng chung**: `hooks.py`, `__init__.py`, fixtures, bất kỳ `.py`/`.js` của app. Chỉ trả về REGISTRATION_NEEDED để main thêm vào hooks.py.
4. **KHÔNG mở browser / Playwright / điều hướng URL.** Chỉ kiểm tra dữ liệu bằng `execute()` qua `env/bin/python` (read-only). Frontend testing do main lo độc quyền → tránh tranh chấp trình duyệt.
5. **KHÔNG chạy** `bench build` / `bench migrate` / `bench restart` / bơm dữ liệu / `frappe.db.commit()` ghi dữ liệu. Data triage chỉ ĐỌC (execute), không ghi.
6. Nếu lỡ thấy cần sửa code/data → KHÔNG sửa, ghi vào ISSUES_FOUND để main xử lý.

## Return format (message cuối — JSON-ish, ngắn gọn)
```
SECTION: <tên>
FILES_WRITTEN: [help/<slug>/index.md, help/<slug>/<a>.md, ...]
REGISTRATION_NEEDED:   # main sẽ thêm vào hooks.py
  - kind: report|doctype|page
    key: "<Report/DocType name hoặc page-slug>"
    content_dir: "help/<slug>"
    default_article: "<file-slug>"
    section: "<Section>"
    title: "<title>"
EMPTY_REPORTS: ["<Report name>", ...]   # report 0 rows cần bơm data
ISSUES_FOUND:
  - item: "<tên item>"
    severity: minor|serious
    desc: "<mô tả>"
    fixed_in_help: true|false   # minor có thể đã giải thích/né trong help
SItuation notes: <ghi chú VAS nếu có>
```
Viết help CHẤT LƯỢNG, căn cứ code thật. Đây là tài liệu cho kế toán VN dùng thật.
