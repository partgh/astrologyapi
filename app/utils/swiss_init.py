from pathlib import Path

import swisseph as swe


_SWE_INITIALIZED = False


def initialize_sidereal_mode():
    global _SWE_INITIALIZED
    if _SWE_INITIALIZED:
        return

    default_ephe_path = Path("/usr/share/ephe")
    if default_ephe_path.exists():
        swe.set_ephe_path(str(default_ephe_path))
    else:
        ephe_dir = Path(__file__).resolve().parents[2] / "ephemeris"
        swe.set_ephe_path(str(ephe_dir))

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    _SWE_INITIALIZED = True
