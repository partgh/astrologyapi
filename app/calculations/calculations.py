import swisseph as swe

from app.calculations.aspects import get_planetary_aspects
from app.calculations.dasha import get_vimshottari_dasha
from app.calculations.houses import get_houses
from app.calculations.nakshatra import get_nakshatra
from app.calculations.planets import get_planetary_positions
from app.models.schema import NakshatraInfo, PlanetPosition
from app.utils.swiss_init import initialize_sidereal_mode
from app.utils.time_conversion import get_julian_day


def _round(value: float, precision: int):
    return round(value, precision)


def calculate_chart_data(request):
    precision = request.precision
    initialize_sidereal_mode()
    swe.set_topo(request.longitude, request.latitude, 0)

    try:
        jd = get_julian_day(
            request.year,
            request.month,
            request.day,
            request.hour,
            request.minute,
            request.second,
            request.timezone,
        )
    except Exception as exc:
        raise ValueError({"error_type": "time_conversion_error", "message": str(exc)})
    print("DEBUG AYANAMSA:", swe.get_ayanamsa_ut(jd))

    try:
        ayanamsa = swe.get_ayanamsa_ut(jd)
    except Exception as exc:
        raise ValueError(
            {"error_type": "ayanamsa_error", "julian_day": jd, "message": str(exc)}
        )

    planets = get_planetary_positions(
        jd,
        node_type=request.node_type,
        precision=precision,
    )

    house_data = get_houses(
        jd,
        request.latitude,
        request.longitude,
        house_system=request.house_system,
        precision=precision,
        ayanamsa=ayanamsa,
    )

    ascendant = house_data["ascendant"]
    house_cusps = house_data["houses"]

    enriched_planets = []
    nakshatra_map = {}

    for p in planets:
        nak_info = get_nakshatra(p["longitude"])
        nakshatra_map[p["name"]] = {
            "id": nak_info["id"],
            "name": nak_info["name"],
            "pada": nak_info["pada"],
            "fraction_traversed": _round(nak_info["fraction_traversed"], precision),
            "degrees_in_nakshatra": _round(nak_info["degrees_in_nakshatra"], precision),
        }

        p_lon = p["longitude"]
        placed_house = -1
        for i in range(12):
            current_cusp = house_cusps[i]
            next_cusp = house_cusps[(i + 1) % 12]
            if current_cusp < next_cusp:
                if current_cusp <= p_lon < next_cusp:
                    placed_house = i + 1
                    break
            else:
                if p_lon >= current_cusp or p_lon < next_cusp:
                    placed_house = i + 1
                    break

        enriched_planets.append(
            PlanetPosition(
                **p,
                nakshatra=NakshatraInfo(**nakshatra_map[p["name"]]),
                house=placed_house,
            )
        )

    moon_data = next((p for p in planets if p["name"] == "Moon"), None)
    if not moon_data:
        raise ValueError({"error_type": "missing_planet_error", "message": "Moon not found"})

    from datetime import datetime

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
        planets,
        orb=request.aspect_orb,
        include_node_special_aspects=request.include_node_special_aspects,
        precision=precision,
    )

    return {
        "ascendant": _round(ascendant, precision),
        "ayanamsa": _round(ayanamsa, precision),
        "planets": enriched_planets,
        "houses": house_cusps,
        "nakshatra_data": nakshatra_map,
        "vimshottari_dasha": dasha_info,
        "aspects": aspects,
    }
