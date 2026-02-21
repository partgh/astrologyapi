import swisseph as swe
from datetime import datetime

from app.calculations.aspects import get_planetary_aspects
from app.calculations.dasha import get_vimshottari_dasha
from app.calculations.nakshatra import get_nakshatra
from app.models.schema import NakshatraInfo, PlanetPosition
from app.utils.swiss_init import initialize_sidereal_mode
import pytz


def _round(value: float, precision: int):
    return round(value, precision)


def _normalize_angle(angle: float) -> float:
    return angle % 360.0


def calculate_house(planet_longitude: float, asc_longitude: float) -> int:
    planet_rashi = int((planet_longitude % 360.0) // 30) + 1
    asc_rashi = int((asc_longitude % 360.0) // 30) + 1
    return ((planet_rashi - asc_rashi + 12) % 12) + 1


def calculate_chart_data(request):
    precision = request.precision
    sidereal_flag = swe.FLG_SIDEREAL | swe.FLG_SWIEPH

    # Rule 1 + Rule 2: initialize Swiss Ephemeris and set Lahiri once.
    initialize_sidereal_mode()

    try:
        # Rule 3: localize to timezone, convert to UTC, extract decimal UTC hour.
        local_tz = pytz.timezone(request.timezone)
        dt_local = local_tz.localize(
            datetime(
                request.year,
                request.month,
                request.day,
                request.hour,
                request.minute,
                request.second,
            )
        )
        dt_utc = dt_local.astimezone(pytz.UTC)
        hour_decimal_utc = (
            dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
        )

        # Rule 4: Julian day in UTC with Gregorian calendar.
        jd_ut = swe.julday(
            dt_utc.year,
            dt_utc.month,
            dt_utc.day,
            hour_decimal_utc,
            swe.GREG_CAL,
        )
    except Exception as exc:
        raise ValueError({"error_type": "time_conversion_error", "message": str(exc)})

    ayanamsa = _normalize_angle(swe.get_ayanamsa_ut(jd_ut))

    house_cusps, ascmc = swe.houses_ex(
        jd_ut,
        request.latitude,
        request.longitude,
        b"S",
        swe.FLG_SIDEREAL,
    )
    ascendant = _normalize_angle(ascmc[0])
    cusp_start_idx = 1 if len(house_cusps) == 13 else 0
    house_cusps = [
        _normalize_angle(house_cusps[cusp_start_idx + i]) for i in range(12)
    ]
    asc_rashi = int(ascendant // 30) + 1

    # Rule 5: use only swe.calc_ut(jd_ut, planet_id) for these planets.
    planet_ids = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
    }

    raw_positions = []
    for name, planet_id in planet_ids.items():
        result, _ = swe.calc_ut(jd_ut, planet_id, sidereal_flag)
        longitude = _normalize_angle(result[0])
        speed = result[3]
        raw_positions.append(
            {
                "id": planet_id,
                "name": name,
                "longitude": longitude,
                "is_retrograde": speed < 0,
                "speed": speed,
            }
        )

    # Rule 6: Ketu from Rahu only.
    rahu = next(p for p in raw_positions if p["name"] == "Rahu")
    ketu_longitude = _normalize_angle(rahu["longitude"] + 180.0)
    raw_positions.append(
        {
            "id": -1,
            "name": "Ketu",
            "longitude": ketu_longitude,
            "is_retrograde": rahu["is_retrograde"],
            "speed": rahu["speed"],
        }
    )

    # Rule 11: required debug output.
    print("DEBUG JD_UT:", jd_ut)
    print("DEBUG AYANAMSA:", ayanamsa)
    print("DEBUG ASCENDANT:", ascendant)
    print("DEBUG CUSPS:", house_cusps)

    enriched_planets = []
    nakshatra_map = {}

    for p in raw_positions:
        p_lon = _normalize_angle(p["longitude"])
        rashi_number = int(p_lon // 30) + 1
        house_num = calculate_house(p_lon, ascendant)
        nak_info = get_nakshatra(p_lon)

        nakshatra_map[p["name"]] = {
            "id": nak_info["id"],
            "name": nak_info["name"],
            "pada": nak_info["pada"],
            "fraction_traversed": _round(nak_info["fraction_traversed"], precision),
            "degrees_in_nakshatra": _round(nak_info["degrees_in_nakshatra"], precision),
        }

        print(
            f"DEBUG PLANET: {p['name']} longitude={p_lon} "
            f"rashi={rashi_number} house={house_num}"
        )

        enriched_planets.append(
            PlanetPosition(
                id=p["id"],
                name=p["name"],
                longitude=_round(p_lon, precision),
                rashi_number=rashi_number,
                is_retrograde=p["is_retrograde"],
                speed=_round(p["speed"], precision),
                nakshatra=NakshatraInfo(**nakshatra_map[p["name"]]),
                house=house_num,
            )
        )

    moon_data = next((p for p in raw_positions if p["name"] == "Moon"), None)
    if not moon_data:
        raise ValueError(
            {"error_type": "missing_planet_error", "message": "Moon not found"}
        )

    birth_date = datetime(
        request.year,
        request.month,
        request.day,
        request.hour,
        request.minute,
        request.second,
    )
    dasha_info = get_vimshottari_dasha(moon_data["longitude"], birth_date)

    aspects = get_planetary_aspects(
        raw_positions,
        orb=request.aspect_orb,
        include_node_special_aspects=request.include_node_special_aspects,
        precision=precision,
    )

    return {
        "ascendant_longitude": _round(ascendant, precision),
        "ascendant_rashi": asc_rashi,
        "ascendant": _round(ascendant, precision),
        "ayanamsa": _round(ayanamsa, precision),
        "planets": enriched_planets,
        "houses": [_round(c, precision) for c in house_cusps],
        "nakshatra_data": nakshatra_map,
        "vimshottari_dasha": dasha_info,
        "aspects": aspects,
    }
