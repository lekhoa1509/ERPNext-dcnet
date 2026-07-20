"""EasyInvoice XML builder — pure functions, no Frappe ORM, easily unit-testable.

Builds XmlData payload for API #1 importInvoice per
EasyInvoice_TaiLieuTichHop_v8.0 doc, sec V (Cấu trúc XML).
"""
from datetime import date, datetime
from xml.sax.saxutils import escape as _xml_escape


# Standard VN VAT rates that map to themselves as integers in EasyInvoice schema.
_STANDARD_VAT_RATES = (0, 5, 8, 10)


def xml_escape(s) -> str:
    """Escape `<>&"'` for safe XML text content.

    Accepts non-string (None/int/float) and coerces to str first.
    """
    if s is None:
        return ""
    return _xml_escape(str(s), {'"': "&quot;", "'": "&apos;"})


def format_amount(n) -> str:
    """Format numeric value for XML.

    `12345.0`  → `"12345"` (strip trailing zero on integer-valued floats)
    `12345.5`  → `"12345.5"` (keep decimals)
    `12345`    → `"12345"`
    None/empty → `"0"`

    No thousand separators (XML decimal uses `.` only).
    """
    if n is None or n == "":
        return "0"
    try:
        f = float(n)
    except (TypeError, ValueError):
        return str(n)
    if f.is_integer():
        return str(int(f))
    # Normalize trailing zeros e.g. 12.50 → 12.5
    s = f"{f:.6f}".rstrip("0").rstrip(".")
    return s if s else "0"


def format_date_dmy(d) -> str:
    """date or datetime → "dd/MM/yyyy" string."""
    if d is None:
        return ""
    if isinstance(d, datetime):
        d = d.date()
    if isinstance(d, date):
        return d.strftime("%d/%m/%Y")
    # Accept already-formatted string fallthrough
    return str(d)


def infer_vat_rate_int(rate):
    """Map a VAT rate (numeric) → (vat_rate_int, vat_rate_other_str_or_None).

    Standard rates {0, 5, 8, 10} → (rate_int, None).
    Non-standard positive rate (e.g. 15.5) → (-3, "15.5") per EasyInvoice convention.
    None → (None, None) — caller decides (often -1 = không chịu thuế).
    """
    if rate is None or rate == "":
        return (None, None)
    try:
        r = float(rate)
    except (TypeError, ValueError):
        return (None, None)
    # If exactly equal to a standard rate (0/5/8/10), return integer form
    if r == int(r) and int(r) in _STANDARD_VAT_RATES:
        return (int(r), None)
    return (-3, format_amount(r))


def build_product_xml(prod: dict) -> str:
    """Build a single <Product>...</Product> block.

    Required keys in prod: no, code, name, unit, qty, price, total, vat_rate, vat_amount, amount.
    Optional: feature (default 1), vat_rate_other (only if vat_rate==-3).
    """
    feature = prod.get("feature", 1)
    vat_rate, vat_rate_other = _vat_for_product(prod)

    parts = [
        "<Product>",
        f"<No>{xml_escape(prod.get('no', 1))}</No>",
        f"<Code>{xml_escape(prod.get('code', ''))}</Code>",
        f"<Feature>{xml_escape(feature)}</Feature>",
        f"<ProdName>{xml_escape(prod.get('name', ''))}</ProdName>",
        f"<ProdUnit>{xml_escape(prod.get('unit', ''))}</ProdUnit>",
        f"<ProdQuantity>{format_amount(prod.get('qty'))}</ProdQuantity>",
        f"<ProdPrice>{format_amount(prod.get('price'))}</ProdPrice>",
        f"<Total>{format_amount(prod.get('total'))}</Total>",
        f"<VATRate>{xml_escape(vat_rate) if vat_rate is not None else ''}</VATRate>",
    ]
    if vat_rate_other is not None:
        parts.append(f"<VATRateOther>{xml_escape(vat_rate_other)}</VATRateOther>")
    parts.extend([
        f"<VATAmount>{format_amount(prod.get('vat_amount', 0))}</VATAmount>",
        f"<Amount>{format_amount(prod.get('amount'))}</Amount>",
        "</Product>",
    ])
    return "".join(parts)


def _vat_for_product(prod):
    """Return (vat_rate_int, vat_rate_other) for a product dict.

    If prod already carries `vat_rate` as -3 + `vat_rate_other`, pass through.
    Else infer from `vat_rate` numeric value.
    """
    raw = prod.get("vat_rate")
    raw_other = prod.get("vat_rate_other")
    if raw == -3 and raw_other is not None:
        return (-3, str(raw_other))
    if raw is None:
        return (None, None)
    try:
        if int(raw) == raw and int(raw) in _STANDARD_VAT_RATES + (-1, -2):
            return (int(raw), None)
    except (TypeError, ValueError):
        pass
    return infer_vat_rate_int(raw)


def build_invoice_xml(inv: dict) -> str:
    """Build complete <Invoices>...</Invoices> root XML for API #1 importInvoice.

    Required keys in inv: ikey, customer_code, customer_name, address, tax_id,
    arising_date, currency, exchange_rate, products (list of product dicts),
    total, vat_rate, vat_amount, amount, amount_in_words.
    Optional: payment_method (default "TM/CK"), email, phone, discount_amount.
    """
    products_xml = "".join(build_product_xml(p) for p in inv.get("products", []))
    arising = inv.get("arising_date")
    if isinstance(arising, (date, datetime)):
        arising = format_date_dmy(arising)

    inv_root_vat_rate, inv_root_vat_other = _vat_for_invoice(inv)

    parts = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<Invoices>",
        "<Inv>",
        "<Invoice>",
        f"<Ikey>{xml_escape(inv.get('ikey', ''))}</Ikey>",
        f"<CusCode>{xml_escape(inv.get('customer_code', ''))}</CusCode>",
        f"<Buyer>{xml_escape(inv.get('customer_name', ''))}</Buyer>",
        f"<CusName>{xml_escape(inv.get('customer_name', ''))}</CusName>",
        f"<CusAddress>{xml_escape(inv.get('address', ''))}</CusAddress>",
        f"<CusTaxCode>{xml_escape(inv.get('tax_id', ''))}</CusTaxCode>",
        f"<Email>{xml_escape(inv.get('email', ''))}</Email>",
        f"<CusPhone>{xml_escape(inv.get('phone', ''))}</CusPhone>",
        f"<PaymentMethod>{xml_escape(inv.get('payment_method', 'TM/CK'))}</PaymentMethod>",
        f"<ArisingDate>{xml_escape(arising or '')}</ArisingDate>",
        f"<CurrencyUnit>{xml_escape(inv.get('currency', 'VND'))}</CurrencyUnit>",
        f"<ExchangeRate>{format_amount(inv.get('exchange_rate', 1))}</ExchangeRate>",
        "<Products>",
        products_xml,
        "</Products>",
        f"<Total>{format_amount(inv.get('total'))}</Total>",
        f"<VATRate>{xml_escape(inv_root_vat_rate) if inv_root_vat_rate is not None else ''}</VATRate>",
    ]
    if inv_root_vat_other is not None:
        parts.append(f"<VATRateOther>{xml_escape(inv_root_vat_other)}</VATRateOther>")
    parts.extend([
        f"<VATAmount>{format_amount(inv.get('vat_amount', 0))}</VATAmount>",
        f"<Amount>{format_amount(inv.get('amount'))}</Amount>",
        f"<DiscountAmount>{format_amount(inv.get('discount_amount', 0))}</DiscountAmount>",
        f"<AmountInWords>{xml_escape(inv.get('amount_in_words', ''))}</AmountInWords>",
        "</Invoice>",
        "</Inv>",
        "</Invoices>",
    ])
    return "".join(parts)


def _vat_for_invoice(inv):
    raw = inv.get("vat_rate")
    raw_other = inv.get("vat_rate_other")
    if raw == -3 and raw_other is not None:
        return (-3, str(raw_other))
    if raw is None:
        return (None, None)
    try:
        if int(raw) == raw and int(raw) in _STANDARD_VAT_RATES + (-1, -2):
            return (int(raw), None)
    except (TypeError, ValueError):
        pass
    return infer_vat_rate_int(raw)
