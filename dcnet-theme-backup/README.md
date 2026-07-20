# DCNET Theme

DCNET custom Frappe app cung cấp 2 nhóm tính năng:

1. **Theme** — preset CSS, applicator, desktop icon override
2. **Sidebar routing** — context-primary workspace sidebar resolver (merged từ
   `dcnet_sidebar_routing` v0.3.0). Tránh việc Frappe tự động chuyển sidebar
   khi entity nằm trong nhiều workspace sidebars (Address ∈ Buying ∪ Selling).

Các app tích hợp đăng ký sidebar context bằng cách thêm `dcnet_theme` vào
`required_apps`. Boot session emits `user_allowed_modules` +
`workspace_sidebar_modules` để `sidebar.bundle.js` xử lý 2-tier resolution.

## Quy trình phát triển

```
feature/*  ─┐
fix/*       ├──→ PR → develop → PR (owner) → main → tag v1.x.x
refactor/*  │
chore/*     │
docs/*     ─┘

hotfix/* → PR → main (owner) → tag patch
             └→ PR → develop (sync)
```

### Tạo nhánh mới

```bash
git checkout develop
git checkout -b feature/ten-tinh-nang
```

### Cài đặt với Frappe Manager

```bash
fm create mybench --apps dcnet-cloud/dcnet-theme:main
```
