import sys
sys.path.append(r'c:\Users\lenovo\Desktop\self made kundli engine')
from app.utils.time_conversion import get_julian_day
from app.calculations.planets import get_planetary_positions
from app.calculations.houses import get_houses
import swisseph as swe

swe.set_ephe_path('ephemeris/')
swe.set_sid_mode(swe.SIDM_LAHIRI)

jd = get_julian_day(2009, 4, 12, 7, 23, 0, 'Asia/Kolkata')
print('JD:', jd)
planets = get_planetary_positions(jd)
for p in planets:
    if p['name'] in ['Sun', 'Moon', 'Rahu']:
        print(p['name'], p['longitude'])
        
houses = get_houses(jd, 28.4089, 77.3178)
print('Ayanamsa:', houses['ayanamsa'])
print('Ascendant:', houses['ascendant'])
