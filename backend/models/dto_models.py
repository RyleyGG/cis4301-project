from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Optional, List


class FireIncidentFilters(BaseModel):
    size_category: Optional[str] = None
    year_of_fire_max: Optional[int] = None
    year_of_fire_min: Optional[int] = None