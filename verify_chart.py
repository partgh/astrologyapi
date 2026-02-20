from app.utils.time_conversion import get_julian_day, set_ephemeris_path
from app.calculations.planets import get_planetary_positions
from app.calculations.houses import get_houses
from app.calculations.nakshatra import get_nakshatra
from app.calculations.dasha import get_vimshottari_dasha
from datetime import datetime
import json

# Set up test case (Example from prompt or a known date)
# Let's use current date: 2026-02-20, 12:00 PM, New Delhi
TEST_DATA = {
    "year": 2026,
    "month": 2,
    "day": 20,
    "hour": 12,
    "minute": 0,
    "second": 0,
    "timezone": "Asia/Kolkata",
    "latitude": 28.6139,
    "longitude": 77.2090
}

def verify():
    print("Setting ephemeris path...")
    set_ephemeris_path()
    
    print("Calculating Julian Day...")
    jd = get_julian_day(
        TEST_DATA["year"], TEST_DATA["month"], TEST_DATA["day"],
        TEST_DATA["hour"], TEST_DATA["minute"], TEST_DATA["second"],
        TEST_DATA["timezone"]
    )
    print(f"Julian Day: {jd}")
    
    # Calculate Planets
    print("Calculating Planets...")
    planets = get_planetary_positions(jd)
    
    # Check for forbidden planets
    forbidden = ["Uranus", "Neptune", "Pluto"]
    for p in planets:
        if p['name'] in forbidden:
             print(f"ERROR: Forbidden planet found: {p['name']}")
        print(f"{p['name']}: {p['longitude']:.9f}") # High precision print
        
    print("Calculating Houses...")
    houses = get_houses(jd, TEST_DATA["latitude"], TEST_DATA["longitude"])
    print(f"Ascendant: {houses['ascendant']:.4f}")
    print(f"Ayanamsa: {houses['ayanamsa']:.4f}")
    print("Cusps:", houses["houses"])
    
    # Verify Nakshatra for Moon
    moon = next(p for p in planets if p["name"] == "Moon")
    nak = get_nakshatra(moon["longitude"])
    print(f"Moon Nakshatra: {nak['name']} (Pada {nak['pada']})")
    
    # Verify Dasha
    dt = datetime(TEST_DATA["year"], TEST_DATA["month"], TEST_DATA["day"], TEST_DATA["hour"], TEST_DATA["minute"], TEST_DATA["second"])
    dasha = get_vimshottari_dasha(moon["longitude"], dt)
    print("Dasha Balance:", dasha)

if __name__ == "__main__":
    verify()
