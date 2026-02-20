BASE_ASPECTS = [("7th", 180.0)]
SPECIAL_ASPECTS = {
    "Mars": [("4th", 90.0), ("8th", 210.0)],
    "Jupiter": [("5th", 120.0), ("9th", 240.0)],
    "Saturn": [("3rd", 60.0), ("10th", 270.0)],
}
NODE_EXTRA_ASPECTS = [("5th", 120.0), ("9th", 240.0)]


def _round(value: float, precision: int):
    return round(value, precision)


def get_planetary_aspects(
    planets_data: list,
    orb: float = 3.0,
    include_node_special_aspects: bool = False,
    precision: int = 4,
):
    aspects = []

    for p1 in planets_data:
        p1_name = p1["name"]
        target_aspects = list(BASE_ASPECTS)
        target_aspects.extend(SPECIAL_ASPECTS.get(p1_name, []))
        if include_node_special_aspects and p1_name in ("Rahu", "Ketu"):
            target_aspects.extend(NODE_EXTRA_ASPECTS)

        for p2 in planets_data:
            if p1_name == p2["name"]:
                continue

            angle_forward = (p2["longitude"] - p1["longitude"]) % 360.0

            best_match = None
            for aspect_type, target_angle in target_aspects:
                current_orb = abs(angle_forward - target_angle)
                if current_orb <= orb:
                    if best_match is None or current_orb < best_match["orb"]:
                        best_match = {
                            "type": aspect_type,
                            "target_angle": target_angle,
                            "orb": current_orb,
                        }

            if best_match is not None:
                aspects.append(
                    {
                        "planet": p1_name,
                        "aspecting": p2["name"],
                        "type": best_match["type"],
                        "angle": _round(angle_forward, precision),
                        "orb": _round(best_match["orb"], precision),
                    }
                )

    return aspects
