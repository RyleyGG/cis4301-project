from datetime import datetime
from sqlmodel import SQLModel, Field
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


class WildFireChangesInSizeAndFrequencyFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class WildFireChangesInSizeAndFrequency(BaseModel):
    year_of_fire: Optional[int] = None
    avg_fire_size: Optional[float] = None
    total_number_of_fires: Optional[int] = None
    total_fires_size: Optional[float] = None


class WildfireTypesBasedOnGeoFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    geographic_area: Optional[str] = None
    wildfire_type: Optional[str] = None


class WildfireTypesBasedOnGeo(BaseModel):
    year_of_fire: Optional[int] = None
    wildfire_type: Optional[str] = None
    avg_fire_size: Optional[int] = None
    total_number_of_fires: Optional[int] = None
    total_fires_size: Optional[int] = None
    fire_type: Optional[int] = None


class AgencyContaintmentTimeFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reporting_agency: Optional[str] = None


class SizeOfWildfireTypesFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reporting_agency: Optional[str] = None
    wildfire_type: Optional[str] = None


class FireIncidentSearch(BaseModel):
    fire_incidents: List[FireIncident]
    total_count: int


class wildfireSizeBasedOnGeoFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    geographic_area: Optional[str] = None