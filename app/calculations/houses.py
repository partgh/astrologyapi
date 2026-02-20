import swisseph as swe

HOUSE_SYSTEM_CODE = {
    "placidus": b'P',
    "equal": b'E',
}


def _round(value: float, precision: int):
    return round(value, precision)


def _build_whole_sign_cusps(ascendant: float):
    sign_start = int((ascendant % 360.0) // 30) * 30.0
    return [((sign_start + 30.0 * i) % 360.0) for i in range(12)]


def get_houses(
    julian_day: float,
    lat: float,
    lon: float,
    house_system: str = "placidus",
    precision: int = 4,
    ayanamsa: float = None,
):
    flags = swe.FLG_SIDEREAL
    try:
        _, ascmc = swe.houses_ex(julian_day, lat, lon, b'P', flags)
        ascendant = ascmc[0] % 360.0

        if house_system == "whole_sign":
            final_cusps = _build_whole_sign_cusps(ascendant)
        else:
            code = HOUSE_SYSTEM_CODE.get(house_system, b'P')
            cusps, ascmc = swe.houses_ex(julian_day, lat, lon, code, flags)
            ascendant = ascmc[0] % 360.0
            start_idx = 1 if len(cusps) == 13 else 0
            final_cusps = [cusps[start_idx + i] % 360.0 for i in range(12)]
    except Exception as exc:
        raise ValueError(
            {
                "error_type": "houses_error",
                "julian_day": julian_day,
                "latitude": lat,
                "longitude": lon,
                "house_system": house_system,
                "message": str(exc),
            }
        )

    final_ayanamsa = swe.get_ayanamsa_ut(julian_day) if ayanamsa is None else ayanamsa

    return {
        "ascendant": _round(ascendant, precision),
        "houses": [_round(c, precision) for c in final_cusps],
        "ayanamsa": _round(final_ayanamsa, precision)
    }
