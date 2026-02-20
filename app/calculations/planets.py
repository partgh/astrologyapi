import swisseph as swe

PLANET_BASE_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}

NODE_MAP = {"true": swe.TRUE_NODE, "mean": swe.MEAN_NODE}


def _round(value: float, precision: int):
    return round(value, precision)


def _safe_calc_ut(julian_day: float, planet_id: int, flags: int):
    try:
        result, retflag = swe.calc_ut(julian_day, planet_id, flags)
        return result, retflag
    except Exception as exc:
        raise ValueError(
            {
                "error_type": "calc_ut_error",
                "planet_id": planet_id,
                "julian_day": julian_day,
                "flags": flags,
                "message": str(exc),
            }
        )


def get_planetary_positions(julian_day: float, node_type: str = "true", precision: int = 4):
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    positions = []

    for name, pid in PLANET_BASE_MAP.items():
        result, retflag = _safe_calc_ut(julian_day, pid, flags)
        longitude = result[0]
        speed_long = result[3]

        lon = longitude % 360.0
        speed = speed_long

        is_retrograde = speed < 0
        positions.append({
            "id": pid,
            "name": name,
            "longitude": _round(lon, precision),
            "is_retrograde": is_retrograde,
            "speed": _round(speed, precision)
        })

    node_pid = NODE_MAP.get(node_type, swe.TRUE_NODE)
    node_result, _ = _safe_calc_ut(julian_day, node_pid, flags)
    rahu_lon = node_result[0] % 360.0
    rahu_speed = node_result[3]

    positions.append({
        "id": node_pid,
        "name": "Rahu",
        "longitude": _round(rahu_lon, precision),
        "is_retrograde": rahu_speed < 0,
        "speed": _round(rahu_speed, precision)
    })

    ketu_lon = (rahu_lon + 180.0) % 360.0
    positions.append({
        "id": -1,
        "name": "Ketu",
        "longitude": _round(ketu_lon, precision),
        "is_retrograde": rahu_speed < 0,
        "speed": _round(rahu_speed, precision)
    })

    return positions
