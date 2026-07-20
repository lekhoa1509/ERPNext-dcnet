# API Reference: enhance_security.py

**Language**: Python

**Source**: `patches/v10_0/enhance_security.py`

---

## Functions

### execute()

The motive of this patch is to increase the overall security in frappe framework

Existing passwords won't be affected, however, newly created accounts
will have to adheare to the new password policy guidelines. Once can always
loosen up the security by modifying the values in System Settings, however,
we strongly advice against doing so!

Security is something we take very seriously at frappe,
and hence we chose to make security tighter by default.

**Returns**: (none)


