import swisseph as swe


def _round(value: float, precision: int):
    return round(value, precision)


def _normalize_angle(angle: float) -> float:
    return angle % 360.0


def get_houses(julian_day: float, lat: float, lon: float, precision: int = 4):
    cusps, ascmc = swe.houses_ex(julian_day, lat, lon, b"S", swe.FLG_SIDEREAL)
    ascendant = _normalize_angle(ascmc[0])
    cusp_start_idx = 1 if len(cusps) == 13 else 0
    final_cusps = [_normalize_angle(cusps[cusp_start_idx + i]) for i in range(12)]

    return {
        "ascendant": _round(ascendant, precision),
        "houses": [_round(c, precision) for c in final_cusps],
        "ayanamsa": _round(swe.get_ayanamsa_ut(julian_day), precision),
    }
