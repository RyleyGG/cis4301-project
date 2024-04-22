from datetime import datetime
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Optional, List


class FireIncidentFilters(BaseModel):
    size_category: Optional[str] = None
    year_of_fire_max: Optional[int] = None
    year_of_fire_min: Optional[int] = None


class TblSizeResp(BaseModel):
    fire_incident_size: int
    nwcg_unit_size: int
    reporting_agency_size: int
    total_size: int

class WildFireChangesInSizeAndFrequencyFilters(BaseModel):
    startDate: datetime
    endDate: datetime

class WildfireTypesBasedOnGeoFilters(BaseModel):
    startDate: datetime
    endDate: datetime
    geographicArea: str
    wildfireType: str

class AgencyContaintmentTimeFilters(BaseModel):
    startDate: datetime
    endDate: datetime
    ReportingAgency: str

class SizeOfWildfireTypesFilters(BaseModel):
    startDate: datetime
    endDate: datetime
    reportingAgency: str
    wildfireType: str

class wildfireSizeBasedOnGeoFilters(BaseModel):
    startDate: datetime
    endDate: datetime
    geographicArea: str