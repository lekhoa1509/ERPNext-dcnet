# Modules - DCNET Flow

> Tai lieu ky thuat va phan tich cho tung module, to chuc theo STT ban giao.
> **Triet ly:** Spec-First, ERPNext-Mapped — moi feature khach hang duoc map sang ERPNext.

---

## Cau truc chuan (ap dung cho moi module)

```
docs/modules/{STT}-{slug}/
├── README.md                  # Luon co — tong quan, progress tracker
├── SPEC_MAPPING.md            # Luon co — ⭐ spec → ERPNext mapping (file chinh)
├── CLARIFY.md                 # Neu co van de can hoi khach hang
├── CUSTOM_REQUIREMENTS.md     # Neu co phan can custom (EXT/NEW)
├── analysis/                  # Phan tich sau (module phuc tap)
├── technical-spec/            # Spec ky thuat chi tiet (neu can)
├── mockup/                    # HTML prototypes (neu can thiet ke UI)
└── user-guide/                # HDSD tieng Viet (cho end-user)
```

### File chinh

| File | Bat buoc? | Mo ta |
|------|:---------:|-------|
| `README.md` | **Co** | Tong quan module, milestone, cong ty, tien do |
| `SPEC_MAPPING.md` | **Co** | Map tung feature spec → ERPNext. Dung dung so spec khach hang |
| `CLARIFY.md` | Neu can | Cau hoi can clarify voi khach hang (priority icons) |
| `CUSTOM_REQUIREMENTS.md` | Neu can | Tong hop phan can custom — extract tu SPEC_MAPPING |

### Tags trong SPEC_MAPPING

| Tag | Nghia | Action can lam |
|-----|--------|----------------|
| `USE` | ERPNext co san, dung ngay | Config + test |
| `CFG` | ERPNext co, can config/setup | Setup data, settings, permissions |
| `EXT` | ERPNext co, can mo rong | Custom field, client/server script |
| `NEW` | ERPNext khong co, can build | Custom DocType, module moi |
| `REF` | Thuoc module khac | Tham chieu — link sang module tuong ung |

### Scale theo do phuc tap

| Loai | Files | Vi du |
|------|-------|-------|
| **Don gian** | README + SPEC_MAPPING | 15-chi-nhanh, 16-nhan-vien |
| **Trung binh** | + CLARIFY + CUSTOM_REQUIREMENTS | 09-don-hang, 17-khach-hang |
| **Phuc tap** | + analysis/ + mockup/ | 07-kho-hang, 12-ban-hang, ke toan |
| **Dac thu** | Full set | 14-trade-in, 34-fitting, 40-giao-van |

### Quy tac quan trong

1. **Dung dung so feature cua spec** (VD: 4.1.1, 4.1.2) — KHONG tu dat feature ID rieng
2. **Khong them, khong bot, khong gop** features so voi spec goc
3. **SPEC_MAPPING la file lam viec chinh** — moi nguoi nhin vao day
4. **CUSTOM_REQUIREMENTS** chi tao khi co features tag `EXT` hoac `NEW`
5. **Subfolder chi tao khi co noi dung** — khong tao folder rong

### Tao docs

```bash
/dcnet-module {STT}              # Tao moi
/dcnet-module {STT} --update     # Cap nhat module da co sang cau truc moi
/dcnet-mockup {STT}              # Tao UI mockup
/dcnet-guide {STT}               # Tao user guide tieng Viet
```

---

## Modules da co docs

### T3: Ban giao 31/03/2026

| STT | Folder | Module | Cong ty | Status |
|-----|--------|--------|---------|--------|
| 01 | [01-dang-nhap](./01-dang-nhap/) | Dang nhap/Nen tang | TM + NM | Config only |
| 02 | [02-dashboard](./02-dashboard/) | Dashboard | TM + NM | DONE (docs + code) |
| 03 | [03-san-pham](./03-san-pham/) | Quan ly San pham | TM + NM | Docs done, chua code |

### T4: Ban giao 30/04/2026

| STT | Folder | Module | Cong ty | Status |
|-----|--------|--------|---------|--------|
| 07 | [07-kho-hang](./07-kho-hang/) | Quan ly Kho hang | TM + NM | NEEDS UPDATE |
| 09 | [09-don-hang](./09-don-hang/) | Quan ly Don hang | TM + NM | NEEDS UPDATE |
| 12 | [12-ban-hang](./12-ban-hang/) | Quan ly Ban hang (pricing) | TM + NM | NEEDS UPDATE |
| 14 | [14-trade-in](./14-trade-in/) | Don hang Thu cu Doi moi | TM + NM | NEEDS UPDATE |

### T6: Ban giao 30/06/2026

| STT | Folder | Module | Cong ty | Status |
|-----|--------|--------|---------|--------|
| 33 | [33-lead](./33-lead/) | Quan ly Lead | TM + NM | NEEDS UPDATE |
| 34 | [34-fitting](./34-fitting/) | Quan ly Fitting | TM + NM | NEEDS UPDATE |
| 35 | [35-coaching](./35-coaching/) | Quan ly Coaching | TM only | NEEDS UPDATE |
| 38 | [38-tich-diem](./38-tich-diem/) | Quan ly tich diem | NM only | NEEDS UPDATE |
| 40 | [40-giao-van](./40-giao-van/) | Tich hop Giao van | TM + NM | NEEDS UPDATE |

### Chua migrate (giu vi tri cu)

| Folder | Module | Ghi chu |
|--------|--------|---------|
| [credit-management](./credit-management/) | Quan ly cong no | Can verify truoc khi move |
| [import-management](./import-management/) | Quy trinh nhap hang | Can verify truoc khi move |
| [nhatminh-connect](./nhatminh-connect/) | Web & Dong bo NM | Can verify truoc khi move |

---

## Danh sach STT day du

> Xem chi tiet: [TIMELINE_2026.md](../roadmap/TIMELINE_2026.md)

| T3 (6) | T4 (16) | T5 (10) | T6 (12) | T8 (3) |
|--------|---------|---------|---------|--------|
| 01-06 | 07-22 | 23-32 | 33-44 | 49-51 |

---

## Tai lieu lien quan

- **Spec goc (source of truth):** [docs/feature/](../feature/)
- **ERPNext flows (tham khao):** [docs/erpnext-flows/](../erpnext-flows/)
- **Source mapping:** `.claude/skills/dcnet-module/references/source-mapping.md`

---

**Cap nhat:** 16/02/2026
