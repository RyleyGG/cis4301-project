from datetime import datetime
from sqlmodel import SQLModel, Field
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
    start_date: datetime
    end_date: datetime

class WildfireTypesBasedOnGeoFilters(BaseModel):
    start_date: datetime
    end_date: datetime
    geographic_area: str
    wildfire_type: str
    
class WildfireTypesBasedOnGeo(BaseModel):
    year_of_fire: int 
    wildfire_type: str
    avg_fire_size: int 
    total_number_of_fires: int
    total_fires_size: int 
    fire_type: int 

class AgencyContaintmentTimeFilters(BaseModel):
    start_date: datetime
    end_date: datetime
    reporting_agency: str

class SizeOfWildfireTypesFilters(BaseModel):
    start_date: datetime
    end_date: datetime
    reporting_agency: str
    wildfire_type: str

class wildfireSizeBasedOnGeoFilters(BaseModel):
    start_date: datetime
    end_date: datetime
    geographic_area: str