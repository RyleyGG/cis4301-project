from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey


class Dummy(SQLModel, table=True):
    __tablename__ = 'Dummy'
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    some_str: str = Field(sa_column=Column(String(255)))


class FireIncident(SQLModel, table=True):
    __tablename__ = 'FireIncident'
    id: int = Field(primary_key=True)
    cause_code: str = Field(sa_column=Column(String(255)))
    cause_description: str = Field(sa_column=Column(String(255)))
    discovery_datetime: datetime = Field()
    discovery_date: datetime = Field()
    containment_date: datetime = Field()
    containment_datetime: datetime = Field()
    size: float = Field()
    size_class: str = Field(sa_column=Column(String(50)))
    size_category: str = Field(sa_column=Column(String(50)))
    year: int = Field()
    fire_name: str = Field(sa_column=Column(String(255)))
    fips_code: str = Field(sa_column=Column(String(10)))
    longitude: float = Field()
    latitude: float = Field()
    fire_code: str = Field(sa_column=Column(String(50)))
    fire_name_alt: str = Field(sa_column=Column(String(255)))
    fire_project_id: int = Field()
    agency_code_id: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255), ForeignKey('ReportingAgency.agency_code'))
    )


class ReportingAgency(SQLModel, table=True):
    __tablename__ = 'ReportingAgency'
    agency_code: str = Field(sa_column=Column(String(255), primary_key=True))
    reporting_unit_id: Optional[int] = Field(default=None, foreign_key='NWCGUnit.unit_id')
    reporting_unit_code: str = Field(sa_column=Column(String(50)))


class NWCGUnit(SQLModel, table=True):
    __tablename__ = 'NWCGUnit'
    unit_id: int = Field(default=None, primary_key=True)
    parent_agency: str = Field(sa_column=Column(String(255)))
    agency_name: str = Field(sa_column=Column(String(255)))
    department_or_state: str = Field(sa_column=Column(String(255)))
    country_code: str = Field(sa_column=Column(String(50)))
    wildland_role: str = Field(sa_column=Column(String(50)))
    gacc: str = Field(sa_column=Column(String(50)))
    unit_name: str = Field(sa_column=Column(String(255)))
    unit_type: str = Field(sa_column=Column(String(50)))
    geographic_area_code: str = Field(sa_column=Column(String(50)))
    unit_code: str = Field(sa_column=Column(String(50)))
    state_federal_id: str = Field(sa_column=Column(String(255)))
    country: str = Field(sa_column=Column(String(255)))
