from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class EngineOptions:
    node_type: Literal["true", "mean"] = "true"
    precision: int = 4
    house_system: Literal["sripati", "ascendant_based"] = "ascendant_based"
    aspect_orb: float = 3.0
    include_node_special_aspects: bool = False
