// Vietnam Administrative Divisions API (2025 reform)
// Source: openapi.json (provinces.open-api.vn/api/v2)
// 2025 reform: 63 tỉnh → 34 tỉnh, bỏ cấp quận/huyện, chỉ còn tỉnh → xã/phường
const VN_API = 'https://provinces.open-api.vn/api/v2';

let _provinces_cache = null;
const _wards_cache = {};

export async function fetchVnProvinces() {
  if (_provinces_cache) return _provinces_cache;
  try {
    const res = await fetch(`${VN_API}/p/`);
    if (!res.ok) return [];
    _provinces_cache = await res.json();
    return _provinces_cache;
  } catch {
    return [];
  }
}

export async function fetchVnWards(provinceCode) {
  if (!provinceCode) return [];
  const key = String(provinceCode);
  if (_wards_cache[key]) return _wards_cache[key];
  try {
    const res = await fetch(`${VN_API}/p/${provinceCode}?depth=2`);
    if (!res.ok) return [];
    const data = await res.json();
    _wards_cache[key] = data.wards || [];
    return _wards_cache[key];
  } catch {
    return [];
  }
}
