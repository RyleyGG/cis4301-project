from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum
from pydantic import BaseModel, UUID4
from typing import Optional, List

from models.db_models import FireIncident, NWCGUnit, ReportingAgency


class BaseFilterObj(BaseModel):
    skip: Optional[int] = None
    take: Optional[int] = None


class FireIncidentFilters(BaseFilterObj):
    size_category: Optional[str] = None
    year_of_fire_max: Optional[int] = None
    year_of_fire_min: Optional[int] = None


class NWCGUnitFilters(BaseFilterObj):
    agency_name: Optional[str] = None
    wildland_role: Optional[str] = None
    geographic_area_code: Optional[str] = None


class ReportingAgencyFilters(BaseFilterObj):
    agency_code: Optional[str] = None
    reporting_unit_id: Optional[str] = None
    reporting_unit_name: Optional[str] = None


class FireIncidentSearch(BaseModel):
    fire_incidents: List[FireIncident]
    total_count: int


class NWCGUnitSearch(BaseModel):
    nwcg_units: List[NWCGUnit]
    total_count: int


class ReportingAgencySearch(BaseModel):
    reporting_agencies: List[ReportingAgency]
    total_count: int


class TblSizeResp(BaseModel):
    fire_incident_size: int
    nwcg_unit_size: int
    reporting_agency_size: int
    total_size: int


# Size And Frequency Filters and DTO
class WildFireChangesInSizeAndFrequencyFilters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class WildFireChangesInSizeAndFrequency(BaseModel):
    year_of_fire: Optional[int] = None
    avg_fire_size: Optional[float] = None
    total_number_of_fires: Optional[int] = None
    total_fires_size: Optional[float] = None


# Types based on Geo Filters and DTO
class WildfireTypesBasedOnGeoFilters(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    geographic_area: Optional[List[str]] = None
    cause_description: Optional[List[str]] = None


class UnitInformation(BaseModel):
    unit_name: str
    geographic_area_code: str


class WildfireTypesBasedOnGeo(BaseModel):
    year_of_fire: int
    cause_description: Optional[str] = None
    geographic_area_code: Optional[str] = None
    avg_fire_size: float
    total_number_of_fires: int
    total_fires_size: float
    cause_description_count: int


# Agency Containment Filters and DTO
class AgencyContaintmentTimeFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reporting_agency: Optional[str] = None


class AgencyContaintmentTime(BaseModel):
    year_of_fire: Optional[int] = None
    reporting_unit_name: Optional[str] = None
    time_to_contain: Optional[datetime] = None
    total_fires: Optional[int] = None
    avg_size_of_fires: Optional[float] = None


# Size Of Types Filters and DTO

class SizeOfWildfireTypesData(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    reporting_agency: Optional[str] = None
    wildfire_type: Optional[str] = None


class SizeOfWildfireTypesFilters(BaseModel):
    year_of_fire: Optional[int] = None
    reporting_unit_name: Optional[str] = None
    fires: Optional[int] = None
    avg_fire_size: Optional[float] = None
    largest_fire_size: Optional[int] = None


# WildFire Sizes Based on Geographical Area

class WildFireSizesBasedOnGeo(BaseModel):
    year_of_fire: Optional[int] = None
    state_affiliation: Optional[str] = None
    avg_fire_size: Optional[float] = None
    largest_fire_size: Optional[int] = None


class WildfireSizeBasedOnGeoFilters(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    geographic_area: Optional[str] = None
