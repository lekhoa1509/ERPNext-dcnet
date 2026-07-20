---
project: frappe-bench-dcnet
base_branch: feat/contract-pakd-post-review
app: dcnet_contract
---

# Contract Template Management — UI & Engine

## 1. Overview

Standardize and automate DCNET's contract document workflow. Currently staff manually edit .docx files in MS Word and print. This feature introduces:

1. **Template Management** — upload .docx, rich HTML editing, dual-language placeholder system, 2-level approval workflow
2. **Contract Form Integration** — template selection, auto-fill, per-contract editing via Quill, version tracking
3. **Document Generation** — PDF (Frappe Print + CSS @page), DOCX (python-docx fill + per-contract edit injection)

### Architecture: HTML-First + DOCX Sidecar

> **Why:** No lightweight open-source library natively edits .docx in-browser at Word quality without a heavy server (OnlyOffice ~2GB RAM). Instead, use HTML as the operational format (edit, preview, placeholder management) and keep the original .docx for pixel-perfect Word export via the existing python-docx fill engine.

```
HTML = operational format  (edit, preview, diff, approval)
DOCX = export format       (python-docx fill on original template)
PDF  = from HTML           (Frappe wkhtmltopdf + CSS @page)
```

> **Rejected:** OnlyOffice (too heavy, Docker dependency, ~2GB RAM for a document editor). DOCX-only approach (no in-browser editing without heavy server). HTML-only approach (DOCX export quality too low from html-to-docx).

## 2. Roles

| Role | Frappe Role | Responsibility |
|------|------------|----------------|
| Sales (KD) | Sales User | Create contracts, select template, per-contract edits |
| Sales Manager (TP KD) | Sales Manager | Review templates, manage which templates are used |
| Legal / Admin Dept (Pháp chế / TP Tổng hợp) | Contract Template Manager (new) | Author templates (.docx upload + HTML edit) |
| CEO (TGĐ) | CEO (new) | Approve templates, sign final contracts, full access |
| Admin/IT | System Manager | Full access, placeholder mapping, system config |

**Full access:** TGĐ and Admin/IT have unrestricted access to all template and contract operations.

## 3. Template Data Model

### DCNET Contract Template (upgrade existing DocType)

#### Existing fields (unchanged)
- `template_name` (Data, unique, reqd)
- `template_category` (Select: "Hợp đồng" | "Phụ lục")
- `service_type` (Select: P2P, MPLS, ILL, FTTH DN, IT Managed, VTTB, Thi công)
- `contract_type` (Select: Recurring | One-off)
- `payment_mode` (Select: Prepay, Monthly, OneOff)
- `package_term_months` (Int)
- `default_items` (Table: DCNET Contract Template Item)
- `default_terms` (Text)
- `boilerplate_text` (Text Editor)

#### New fields

**Versioning & Approval:**
- `version` (Int, default 1) — auto-increment on new .docx upload
- `status` (Select: Draft | Pending Review | Approved | Archived)
- `reviewed_by` (Link: User) — TP KD
- `approved_by` (Link: User) — TGĐ
- `reviewed_date` (Datetime)
- `approved_date` (Datetime)
- `change_log` (Small Text) — description of changes vs previous version

**Dual Format:**
- `template_file` (Attach) — .docx original (source for DOCX export) [existing]
- `template_html` (Long Text) — HTML converted from .docx (source for editing + preview + PDF)

**Placeholder Management:**
- `placeholders` (Table: DCNET Contract Template Placeholder) — [existing, enhanced]
- `placeholder_guide_html` (Long Text) — auto-generated bilingual help table

### Template Status Workflow

```
Draft ──→ Pending Review ──→ Approved ──→ Archived
  ↑            │                            │
  └────────────┘ (reject)                   │
  ↑                                         │
  └─────────────────────────────────────────┘ (new version → clone as Draft)
```

- **Draft:** Legal/Admin uploads .docx + edits HTML. Placeholders auto-discovered.
- **Pending Review:** Submitted for TP KD review.
- **Approved:** TGĐ approves → Sales can use for new contracts.
- **Archived:** Not available for new contracts. Existing contracts keep their reference.

> **Why not Frappe Workflow:** Simple linear flow (3 transitions). Frappe Workflow engine is overkill for a non-submittable DocType. Status Select + controller permission checks are sufficient.

## 4. Placeholder System

### Dual-Language Support

Placeholders accept both English keys and Vietnamese labels:

```
{{customer_name}}      ← English key
{{Tên khách hàng}}     ← Vietnamese label
```

Both resolve to the same value.

### PLACEHOLDER_MAP Structure

```python
PLACEHOLDER_MAP = {
    "customer_name": {
        "vi": "Tên khách hàng",
        "source": "customer.customer_name",
        "example": "Công ty TNHH ABC",
        "group": "Bên A (Khách hàng)",
    },
    "contract_number": {
        "vi": "Số hợp đồng",
        "source": "doc.contract_no_external",
        "example": "DCNET/2026/001",
        "group": "Hợp đồng",
    },
    # ... 60+ entries
}

# Auto-build reverse lookup on module load
VI_TO_KEY = {v["vi"]: k for k, v in PLACEHOLDER_MAP.items()}
```

### Resolve Logic

```python
def resolve_placeholder(raw_key):
    key = raw_key.strip()
    if key in PLACEHOLDER_MAP:
        return key                    # English match
    if key in VI_TO_KEY:
        return VI_TO_KEY[key]         # Vietnamese match
    return None                       # Unknown
```

### Placeholder Validation (on template save)

Each placeholder in the template gets one of 4 statuses:

| Status | Display | Action |
|--------|---------|--------|
| **Matched** | `✅ {{customer_name}} → Tên khách hàng — source: Customer.customer_name` | None needed |
| **Typo suspect** | `⚠️ {{Ten khach hang}} — Missing diacritics. Did you mean {{Tên khách hàng}}? [Auto-fix]` | Button to auto-replace in template_html |
| **Unknown** | `⚠️ {{so_giay_phep}} — Not in system. Similar: {{contract_number}}, {{customer_tax_id}}. When creating contracts, this field will be EMPTY. [Mark for IT]` | Button to flag for dev |
| **Removed** | `ℹ️ Template v2 removed {{fax_number}} (Số fax) vs v1. Add back with {{fax_number}} or {{Số fax}} if still needed.` | Informational |

**Typo detection:** Uses `unidecode` to normalize Vietnamese → ASCII, then exact-match against normalized English keys and Vietnamese labels. No fuzzy matching (too risky — wrong match = wrong field).

**[Auto-fix] button:** Replaces the typo in `template_html` and re-scans. One-click fix.

**[Mark for IT] button:** Sets `needs_dev_mapping = True` on the placeholder child row → visible in list view for IT to filter and add mapping.

### Placeholder Guide (displayed on Template form)

Auto-generated bilingual table:

| Key (EN) | Label (VI) | Description | Source | Example |
|----------|-----------|-------------|--------|---------|
| `{{customer_name}}` | `{{Tên khách hàng}}` | Full name of Party A | Customer.customer_name | Công ty TNHH ABC |
| `{{customer_tax_id}}` | `{{Mã số thuế KH}}` | Tax ID of Party A | Customer.tax_id | 0123456789 |
| `{{contract_number}}` | `{{Số hợp đồng}}` | External contract number | Contract.contract_no_external | DCNET/2026/001 |
| `{{monthly_fee}}` | `{{Phí hàng tháng}}` | Monthly fee before VAT | Calculated from items | 5,000,000 |

Grouped by: Bên A (Khách hàng), Bên B (Công ty), Hợp đồng, Dịch vụ, Tài chính, Ngày tháng, Hạng mục.

## 5. Contract Form Integration

### New Fields on DCNET Contract

- `template_ref` (Link: DCNET Contract Template)
- `template_version` (Int, read-only) — snapshot of template version at apply time
- `contract_html` (Long Text) — HTML canonical for this contract, editable via Quill
- `contract_html_edited` (Check, read-only) — True if sales edited HTML after fill. Detection: set via client script `on_change` on `contract_html` field — compare current value against `_original_contract_html` (cached on form load). Only set to True if content differs from the auto-filled version.
- `template_outdated` (Check, read-only) — True if template has newer version

### Template Selection Flow

```
1. Select Customer
2. Select Template (filtered by service_type, contract_type, status=Approved)
3. Auto-fill:
   - contract_html ← fill template_html with customer/company/contract data
   - items ← copy from template.default_items (if contract has no items yet)
   - default_terms ← copy from template.default_terms
   - template_ref ← Link to template
   - template_version ← snapshot
4. Sales reviews + edits in Quill editor
5. Preview → Export PDF / DOCX → Submit for signing
```

### Template Version Warning

When a Draft contract's template has a newer version:

```
⚠️ Template "HĐ Dịch vụ Viễn thông" has been updated

Current version on this contract: v2 (applied 10/04)
Latest version: v3 (updated 15/04)

Changes: "Added data security clause §12"

[Apply new template]  [Keep v2]  [View comparison]
```

- **[Apply new template]:** Re-fill contract_html from v3. Per-contract additions preserved at the end.
- **[Keep v2]:** Dismiss warning.
- **[View comparison]:** Dialog showing HTML diff between v2 and v3 template.

> **Why warning doesn't block:** Sales may be mid-negotiation with client on v2. Forcing upgrade breaks their flow. Sales decides.

### Edge Cases

1. **Sales picks wrong template, wants to switch:** "Switch template" button with confirm: "Switching template will overwrite current contract content. Per-contract edits will be lost. Continue?" Stronger warning if `contract_html_edited = True`.

2. **Template archived after contract created:** Contract keeps its reference. Archived ≠ deleted. Export still works.

3. **Contract is Active/Signed:** `contract_html` becomes read-only. No editing. Export PDF/DOCX still works. This is the signed version.

4. **Re-apply template on contract with edits:** Confirm: "You have edited X sections. Applying the new template will keep your additions at the end, but the body will update to the new template. [Preview before applying]"

## 6. Document Export

### PDF Export

```
contract_html → Frappe Print Format "Hợp Đồng Chuẩn"
             → wkhtmltopdf (Frappe built-in)
             → CSS @page: A4, margins, headers, footers, page numbers
```

Reuse existing print format. Update `before_print()`:

```python
def before_print(self, settings=None):
    if self.contract_html:
        self.contract_html_rendered = self.contract_html
    else:
        # Backward compat: old contracts without template
        from dcnet_contract.dcnet_contract.utils.docx_generator import (
            generate_html_for_print,
            generate_appendix_html_for_print,
        )
        self.contract_html_rendered = generate_html_for_print(self.name)
        self.appendix_html = generate_appendix_html_for_print(self.name)
```

### DOCX Export

```
template.template_file (.docx original)
  → python-docx fill placeholders (existing engine, 677 lines)
  → inject per-contract edits (if contract_html_edited)
  → save as Frappe File attachment
```

**Per-contract edit injection:**

```python
def export_docx_with_edits(contract_name):
    contract = frappe.get_doc("DCNET Contract", contract_name)
    template = frappe.get_doc("DCNET Contract Template", contract.template_ref)

    # 1. Fill .docx original (existing engine — 100% Word formatting)
    filled_path = generate_document(contract_name, template.name, "docx")

    # 2. If sales edited HTML → extract additions → inject into .docx
    if contract.contract_html_edited:
        additions = _extract_additions(
            original_html=_fill_template_html(template.template_html, contract),
            edited_html=contract.contract_html,
        )
        if additions:
            _inject_paragraphs(filled_path, additions)
            # Convert HTML paragraphs to python-docx paragraphs
            # Insert after "Điều khoản bổ sung" section marker

    return filled_path
```

> **Tradeoff:** Per-contract HTML edits injected into DOCX preserve basic formatting (bold, italic, underline, lists, tables). Complex formatting (images, merged cells) may not roundtrip perfectly. For most contract amendments (text clauses), this is sufficient.

## 7. Permission Model

| Action | Sales User | Sales Manager | Contract Template Manager | CEO | System Manager |
|--------|:-:|:-:|:-:|:-:|:-:|
| View Approved templates | ✅ | ✅ | ✅ | ✅ | ✅ |
| View Draft templates | ❌ | ✅ | ✅ | ✅ | ✅ |
| Create/edit templates | ❌ | ❌ | ✅ | ✅ | ✅ |
| Upload .docx | ❌ | ❌ | ✅ | ✅ | ✅ |
| Edit template_html | ❌ | ❌ | ✅ | ✅ | ✅ |
| Submit for review | ❌ | ❌ | ✅ | ✅ | ✅ |
| Review template | ❌ | ✅ | ❌ | ✅ | ✅ |
| Approve template | ❌ | ❌ | ❌ | ✅ | ✅ |
| Archive template | ❌ | ❌ | ❌ | ✅ | ✅ |
| Create/edit contracts | ✅ (Draft) | ✅ | ❌ | ✅ | ✅ |
| Edit contract_html | ✅ (Draft) | ✅ | ❌ | ✅ | ✅ |
| Export PDF/DOCX | ✅ | ✅ | ✅ | ✅ | ✅ |
| Switch template on contract | ✅ (Draft) | ✅ | ❌ | ✅ | ✅ |
| Add placeholder mapping | ❌ | ❌ | ❌ | ✅ | ✅ |

## 8. Migration Path

### Existing templates (8 seeded records)

`after_migrate` hook:

1. Read `template_file` (.docx) → mammoth → `template_html`
2. Set `status = "Approved"` (bypass approval — already in use)
3. Set `version = 1`
4. Re-scan placeholders with dual-language support
5. Generate `placeholder_guide_html`

### Existing contracts (created before template system)

- `template_ref = NULL` — no impact
- `contract_html = NULL` — `before_print()` falls back to `generate_html_for_print()` (existing behavior)
- Fully backward compatible — no breaking changes

## 9. Scope

### In scope (v1)

- Template CRUD with dual-format (.docx archive + HTML operational)
- Placeholder dual-language (EN/VI) with guide, validation, typo detection, auto-fix
- Template approval workflow (Draft → Pending Review → Approved → Archived)
- Contract form template selection + auto-fill engine
- Contract HTML editing via Frappe Quill editor
- Template version tracking + outdated warning for Draft contracts
- Export PDF (Frappe Print + CSS @page) and DOCX (python-docx fill + edit injection)
- CSS @page print stylesheet for A4 professional output
- Migration of existing 6 .docx templates to dual format
- New Frappe role: Contract Template Manager

### Out of scope (v2+)

- Branch-specific templates
- Admin UI for adding placeholder mappings (v1 = dev adds to code)
- Template usage analytics / counter
- Co-editing templates (multiple users simultaneously)
- Digital signatures on PDF
- Template visual diff viewer (side-by-side)
- Template categories/tags for organization
- Template bulk import
- OnlyOffice integration (if Word-level editing needed later)

## 10. Dependencies

- `mammoth` (Python) — .docx → HTML conversion. Already in project.
- `python-docx` — .docx template filling. Already in project (docx_generator.py).
- `unidecode` (Python) — Vietnamese diacritics stripping for typo detection. Lightweight, MIT.
- Frappe Quill editor — built-in, no new dependency.
- wkhtmltopdf — Frappe built-in for PDF generation.

**No new heavy dependencies.** Only `unidecode` is new (~50KB).
