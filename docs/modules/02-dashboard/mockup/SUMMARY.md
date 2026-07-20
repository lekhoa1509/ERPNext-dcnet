# UI Mockup — 02 Dashboard

## Screens

| File | Screen | Ghi chu |
|------|--------|---------|
| `dashboard.mockup.html` | Workspace Dashboard | Trang chinh: Number Card + Chart + future widgets |

## Design Decisions

### Layout
- **Frappe v16 Workspace layout**: Navbar (48px) + Sidebar (220px) + Content area
- **Filter bar**: Quick time range (Ngay/Thang/Quy/Nam) + date picker + chi nhanh filter
- **Grid responsive**: 3 columns → 2 → 1 tren mobile

### T3 Core (6 features)
- **3 Number Cards**: Doanh so tong, Ban si, Ban le — hien thi value + trend %
- **2 Bar Charts** (nguon KH + nguon don): Horizontal bars voi label + value
- **1 Bar Chart** (Top 20 SP): Full-width, hien thi 10 items + link xem them

### T4-T8 Future Widgets
- **Dashed border + gray background**: Phan biet voi widgets hien tai
- **Placeholder values (—)**: Cho thay data chua co
- **Badge milestone**: Hien thi milestone ban giao (T4, T6)
- **3 sections**: Trade-in (T4), Fitting (T6), Coaching (T6 - TM only)

### Sample Data
- **Nganh golf**: San pham golf (gay, bong, ao, giay, tui, gang tay, mu, o)
- **So lieu thuc te**: Doanh so ty dong, so luong ban thuc te
- **Nguon KH**: Cua hang, Facebook, Zalo, Website, Gioi thieu
- **Nguon don**: Offline, Online, TMDT, Khac

## Mo file

```bash
open docs/modules/02-dashboard/mockup/dashboard.mockup.html
```

## Created

- 2026-02-11
- Standalone HTML, khong can server
