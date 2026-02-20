def initialize_sidereal_mode():
    import swisseph as swe

    CUSTOM_AYANAMSA_OFFSET = -0.88  # AstroSage calibration

    swe.set_ephe_path('.')  # keep existing path if already set
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, CUSTOM_AYANAMSA_OFFSET)
