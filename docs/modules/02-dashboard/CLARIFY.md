# 02 - Dashboard: Van de can Clarify

> **Ngay tao:** 16/02/2026
> **Trang thai:** Cho khach hang xac nhan

---

## Quy uoc

| Icon | Y nghia |
|------|---------|
| :red_circle: | **Critical** — Block trien khai, can tra loi truoc khi code |
| :orange_circle: | **High** — Anh huong thiet ke, can tra loi truoc Sprint |
| :yellow_circle: | **Medium** — Co the dung gia tri mac dinh, confirm sau |
| :green_circle: | **Resolved** — Da co cau tra loi |

---

## 1. Customer Group (Phan loai khach hang)

| # | Cau hoi | Priority | Anh huong | Tra loi | Nguon |
|---|---------|----------|-----------|---------|-------|
| 1.1 | Ten Customer Group cho khach si la "Khach si", "Dai ly", hay ten khac? | :green_circle: Resolved | Filter Number Card 2.2 (ban si) | **"Khách sỉ"** — da co trong `install.py` `setup_customer_groups()`, tu dong tao khi migrate | 2.2 |
| 1.2 | Ten Customer Group cho khach le la "Khach le" hay ten khac? | :green_circle: Resolved | Filter Number Card 2.3 (ban le) | **"Khách lẻ"** — da co trong `install.py` `setup_customer_groups()`, tu dong tao khi migrate | 2.3 |

---

## 2. Nguon don hang (Order Source)

| # | Cau hoi | Priority | Anh huong | Tra loi | Nguon |
|---|---------|----------|-----------|---------|-------|
| 2.1 | Danh sach nguon don hang hien tai: Online, Offline, TMDT, Facebook, Zalo, Website, Khac — dung va du chua? | :orange_circle: High | Custom field `custom_order_source` tren SO + SI, chart 2.5 | Recommend: dung danh sach hien tai, bo sung sau | 2.5 |

---

---

## Thong ke

| Priority | So luong |
|----------|----------|
| :red_circle: Critical | 0 |
| :orange_circle: High | 1 |
| :green_circle: Resolved | 2 |
| **Tong** | **3** |
