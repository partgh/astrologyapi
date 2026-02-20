import swisseph as swe
import time

def test_house_sidereal():
    # Set Ephemeris Path (adjust if needed or rely on default if files missing)
    # swe.set_ephe_path("ephemeris/")
    
    # 1. Get Tropical Houses (Standard)
    # 2. Set Sidereal Mode
    # 3. Get Houses again
    # 4. Compare
    
    # Date: 2026-02-20
    jd = swe.julday(2026, 2, 20, 12.0)
    lat = 28.6139
    lon = 77.2090
    
    # --- Case A: No Sidereal Mode Set (Default Tropical) ---
    # Reset to random or just don't set? 
    # Actually can't unset easily, but let's assume default start.
    # But strictly:
    
    print("--- Testing House Behavior ---")
    
    # Set Tropical (by not setting sidereal? Or setting 0?)
    # swe.set_sid_mode(0,0,0) # SIDM_FAGAN_BRADLEY is 0? No.
    # There isn't a direct "Switch to Tropical" function except not using FLG_SIDEREAL in calc.
    # But houses_ex doesn't take flags.
    
    # Let's see what happens if we assume SIDM_LAHIRI is set globally
    
    # Get Ayanamsa
    ay = swe.get_ayanamsa_ut(jd)
    print(f"Ayanamsa: {ay}")
    
    # Get Houses
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'S')
    asc = ascmc[0]
    print(f"Ascendant (with SIDM_LAHIRI set): {asc}")
    
    # Calculate Sun position Sidereal to compare
    flags_sid = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
    res = swe.calc_ut(jd, swe.SUN, flags_sid)
    sun_sid = res[0][0]
    print(f"Sun Sidereal: {sun_sid}")
    
    # Calculate Sun Tropical
    flags_trop = swe.FLG_SWIEPH | swe.FLG_SPEED
    res_trop = swe.calc_ut(jd, swe.SUN, flags_trop)
    sun_trop = res_trop[0][0]
    print(f"Sun Tropical: {sun_trop}")
    
    # Check difference
    print(f"Sun Diff (Trop - Sid): {sun_trop - sun_sid}")
    print(f"Ascendant Check: If Asc is Tropical, it should be notably different from expected Sidereal Asc.")
    
    # Expected Sidereal Asc for Delhi ~12pm 20 Feb 2026?
    # Sun is in Aquarius (Trop) / Capricorn (Sid)?
    # 20 Feb: Sun Trop ~ 1 Pisces. Sid ~ 6 Aquarius.
    # Ascendant at noon is usually east.
    # Let's check if Ascendant looks "Tropical" or "Sidereal".
    # Just mathematically: Is Ascendant approx Sun_Trop - Ay or Sun_Trop?
    
    # If Asc ~ Sun_Trop (ignoring time of day for a moment), it's Tropical.
    # Basically, if Ascendant matches Tropical values, then `houses_ex` ignores `set_sid_mode`.
    
if __name__ == "__main__":
    test_house_sidereal()
