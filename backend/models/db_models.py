from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, ForeignKey, ForeignKeyConstraint


class Dummy(SQLModel, table=True):
    __tablename__ = 'Dummy'
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    some_str: str = Field(sa_column=Column(String(255)))


class FireIncident(SQLModel, table=True):
    __tablename__ = 'FireIncident'
    id: int = Field(primary_key=True)
    cause_code: float = Field()
    cause_description: str = Field(sa_column=Column(String(100)))
    discovery_datetime: Optional[datetime] = Field(default=None)
    containment_datetime: Optional[datetime] = Field(default=None)
    size_acres: float = Field()
    size_category: str = Field(sa_column=Column(String(1)))
    year_of_fire: int = Field()
    fips_name: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    fips_code: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    longitude: float = Field()
    latitude: float = Field()
    fire_name: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    fire_code: Optional[str] = Field(default=None, sa_column=Column(String(10)))
    agency_code_id: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    reporting_unit_id: Optional[str] = Field(default=None, sa_column=Column(String(255)))

    __table_args__ = (
        ForeignKeyConstraint(['agency_code_id', 'reporting_unit_id'],
                             ['ReportingAgency.agency_code', 'ReportingAgency.reporting_unit_id']),
    )


class ReportingAgency(SQLModel, table=True):
    __tablename__ = 'ReportingAgency'
    agency_code: str = Field(sa_column=Column(String(255), primary_key=True))
    agency_name: Optional[str] = Field(sa_column=Column(String(255)))
    # This is purposefully not a foreign key to NWCGUnit to allow us to store data
    # on agencies that may not have associated NWCGUnit entries
    reporting_unit_id: str = Field(sa_column=Column(String(255), primary_key=True))
    reporting_unit_name: str = Field(sa_column=Column(String(255)))


class NWCGUnit(SQLModel, table=True):
    __tablename__ = 'NWCGUnit'
    unit_id: str = Field(sa_column=Column(String(255), primary_key=True))
    parent_agency: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    agency_name: Optional[str] = Field(sa_column=Column(String(255)))
    agency_code: str = Field(default=None, sa_column=Column(String(255)))
    department_or_state: Optional[str] = Field(default=None, sa_column=Column(String(255)))
    wildland_role: str = Field(sa_column=Column(String(50)))
    geographic_area_code: str = Field(sa_column=Column(String(50)))
    unit_name: str = Field(sa_column=Column(String(255)))
    unit_type: str = Field(sa_column=Column(String(50)))
    unit_code: str = Field(sa_column=Column(String(50)))
    state_affiliation: str = Field(sa_column=Column(String(255)))
    country: str = Field(sa_column=Column(String(255)))
