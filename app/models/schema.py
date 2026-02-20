from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

class ChartRequest(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    timezone: str
    latitude: float
    longitude: float
    node_type: Literal["true", "mean"] = "true"
    precision: Literal[2, 3, 4] = 4
    house_system: Literal["placidus", "equal", "whole_sign"] = "placidus"
    aspect_orb: float = 3.0
    include_node_special_aspects: bool = False

class NakshatraInfo(BaseModel):
    id: int
    name: str
    pada: int
    fraction_traversed: float
    degrees_in_nakshatra: float

class PlanetPosition(BaseModel):
    id: int
    name: str
    longitude: float
    is_retrograde: bool
    speed: float
    nakshatra: Optional[NakshatraInfo] = None
    house: Optional[int] = None # Calculated house placement

class HouseInfo(BaseModel):
    house_number: int
    cusp_longitude: float

class PrecalculatedDasha(BaseModel):
    birth_nakshatra_index: int
    birth_dasha_lord: str
    total_dasha_years: int
    fraction_left: float
    balance_years: float
    current_dasha_end_date: str

class PlanetaryAspect(BaseModel):
    planet: str
    aspecting: str
    type: str # 7th, 4th, etc.
    angle: float
    orb: float

class ChartResponse(BaseModel):
    ascendant: float
    ayanamsa: float
    planets: List[PlanetPosition]
    houses: List[float] # List of cusps
    nakshatra_data: Dict[str, NakshatraInfo] # Map planet name/id to nakshatra
    vimshottari_dasha: PrecalculatedDasha
    aspects: List[PlanetaryAspect]
