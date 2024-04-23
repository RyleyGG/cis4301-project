from datetime import datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Optional, List

from models.db_models import FireIncident


class FireIncidentFilters(BaseModel):
    size_category: Optional[str] = None
    year_of_fire_max: Optional[int] = None
    year_of_fire_min: Optional[int] = None
    skip: Optional[int] = None
    take: Optional[int] = None


class TblSizeResp(BaseModel):
    fire_incident_size: int
    nwcg_unit_size: int
    reporting_agency_size: int
    total_size: int


class WildfireSizeBasedOnGeoFilters(BaseModel):
    startDate: datetime
    endDate: datetime
    geographicArea: str = None


class FireIncidentSearch(BaseModel):
    fire_incidents: List[FireIncident]
    total_count: int